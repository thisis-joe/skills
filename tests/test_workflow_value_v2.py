"""Observers must reject wrong public outcomes and leave writer artifacts intact."""
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import subprocess

ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/'docs/evaluation/workflow-v2/cases.py'
spec=importlib.util.spec_from_file_location('workflow_value_v2_cases',PATH)
cases=importlib.util.module_from_spec(spec);spec.loader.exec_module(cases)


class WorkflowValueV2Tests(unittest.TestCase):
    def test_summary_observer_rejects_wrong_policy_and_detects_restoration(self):
        with tempfile.TemporaryDirectory() as temp:
            project=Path(temp);path=project/'catalog.py'
            correct='''import argparse,json,sqlite3,csv
p=argparse.ArgumentParser();p.add_argument('--db');p.add_argument('command');p.add_argument('path',nargs='?');a=p.parse_args()
c=sqlite3.connect(a.db);c.execute('CREATE TABLE IF NOT EXISTS catalog (sku TEXT,name TEXT,price_cents INTEGER)')
if a.command=='import':
 with open(a.path) as f: c.executemany('INSERT INTO catalog VALUES (?,?,?)',[(r['sku'],r['name'],int(r['price_cents'])) for r in csv.DictReader(f)])
 c.commit()
elif a.command=='summary':
 rows=list(c.execute('SELECT price_cents FROM catalog WHERE price_cents>0'))
 print(json.dumps([dict(supplier='legacy',count=len(rows),total_cents=sum(r[0] for r in rows))] if rows else []))
c.close()
'''
            path.write_text(correct)
            self.assertTrue(cases.summary_check(project,cases.PROFILES[0])['passed'])
            path.write_text(correct.replace('price_cents>0','price_cents>=0'))
            self.assertFalse(cases.summary_check(project,cases.PROFILES[0])['passed'])
            path.write_text(correct)
            self.assertTrue(cases.summary_check(project,cases.PROFILES[0])['passed'])

    def test_observations_do_not_seed_policy_or_change_original_project(self):
        with tempfile.TemporaryDirectory() as temp:
            project=Path(temp)/'project';cases.prepare(project,0,'handoff')
            before={p.relative_to(project):p.read_bytes() for p in project.rglob('*') if p.is_file()}
            result=cases.observe(project,0)
            after={p.relative_to(project):p.read_bytes() for p in project.rglob('*') if p.is_file()}
            self.assertEqual(before,after)
            self.assertFalse(result['import_outcome']['passed'])
            self.assertFalse(result['summary_outcome']['passed'])

    def test_broken_product_probe_is_a_recorded_failure_not_driver_abort(self):
        with tempfile.TemporaryDirectory() as temp:
            with patch.object(cases,'call',side_effect=subprocess.TimeoutExpired(['catalog.py'],20)):
                result=cases.summary_check(Path(temp),cases.PROFILES[0])
            self.assertFalse(result['passed'])
            self.assertTrue(any('error' in action for action in result['actions']))

    def test_selection_contexts_with_green_test_claims_are_real(self):
        with tempfile.TemporaryDirectory() as temp:
            for seed in [3,4]:
                project=Path(temp)/str(seed);cases.prepare(project,seed,'selection')
                result=cases.call(project,[sys.executable,'-m','unittest','discover','-v'])
                self.assertEqual(result['exit'],0,result)
                self.assertEqual(cases.git(project,'diff','--name-only','HEAD'),'')
