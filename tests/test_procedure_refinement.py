"""Public observer sensitivity and sandbox source-boundary checks."""
import importlib.util
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
MODULES=ROOT/'docs/evaluation/procedure-refinement'
sys.path.insert(0,str(MODULES))
import fixtures as refinement_fixtures
import variants as refinement_variants

REFERENCE = [
    "result={'units':sum((x+29)//30 for x in rows)}",
    "result=sorted(x['id'] for x in rows if x['age_days']>30 and not x['pinned'])",
    "ordered=sorted(rows,key=lambda x:(-x['score'],x['name']));result=[]\nfor index,row in enumerate(ordered):\n rank=index+1 if index==0 or row['score']!=ordered[index-1]['score'] else result[-1]['rank']\n result.append({'name':row['name'],'rank':rank})",
    "result=[]\nfor start,end in sorted(x for x in rows if x[0]!=x[1]):\n if result and start<result[-1][1]:result[-1][1]=max(end,result[-1][1])\n else:result.append([start,end])",
    "saved={}\nfor row in rows:\n key=row['email'].strip().lower()\n if key not in saved:saved[key]={'email':key,'label':row['label']}\nresult=[saved[key] for key in sorted(saved)]",
]


class ProcedureRefinement(unittest.TestCase):
    def runner(self):
        spec=importlib.util.spec_from_file_location('procedure_refinement_runner',MODULES/'run.py')
        runner=importlib.util.module_from_spec(spec);spec.loader.exec_module(runner)
        return runner

    def test_real_public_oracles_detect_wrong_output_and_restore(self):
        for seed,logic in enumerate(REFERENCE):
            with self.subTest(seed=seed),tempfile.TemporaryDirectory() as directory:
                path=Path(directory)
                (path/'personal-notes.txt').write_text('unrelated project notes: preserve\n')
                original="import json,sys\nif sys.argv[1]=='--version':print('0.1');raise SystemExit\nrows=json.load(open(sys.argv[1]))\n"+logic+"\nprint(json.dumps(result))\n"
                (path/'app.py').write_text(original)
                self.assertTrue(refinement_fixtures.observe_discovery(path,seed)['passed'])
                (path/'app.py').write_text("import sys\nprint('0.1' if sys.argv[1]=='--version' else 'null')\n")
                broken=refinement_fixtures.observe_discovery(path,seed)
                self.assertFalse(broken['passed'])
                self.assertTrue(next(x['passed'] for x in broken['checks'] if x['id']=='preserved_version'))
                self.assertTrue(any(not x['passed'] for x in broken['checks'] if x['id'].startswith('policy_')))
                (path/'app.py').write_text(original)
                self.assertTrue(refinement_fixtures.observe_discovery(path,seed)['passed'])
                self.assertEqual((path/'app.py').read_text(),original)

    def test_proposals_only_mutate_owned_sandbox_paths(self):
        active_before={p.relative_to(ROOT/'skills').as_posix():p.read_bytes()
                       for p in (ROOT/'skills').rglob('*') if p.is_file()}
        # This historical snapshot is not an ancestor of the release-based branch.
        # Read its already-committed evidence, never the current active skill tree.
        archive=MODULES/'evidence/native-evidence.tar.gz'
        receipt=json.loads((MODULES/'evidence/archive.json').read_text())
        self.assertEqual(hashlib.sha256(archive.read_bytes()).hexdigest(),receipt['sha256'])
        originals={}
        with tarfile.open(archive,'r:gz') as evidence:
            members=evidence.getmembers()
            controls=[m for m in members if m.name=='run/control.json']
            self.assertEqual(len(controls),1)
            self.assertTrue(controls[0].isfile())
            control=json.load(evidence.extractfile(controls[0]))
            self.assertEqual(control['candidate'],'622975e349e6276b225aa9ef02ee69d664dd2927')
            manifest=control['manifests']['current']
            self.assertEqual(len(manifest),117)
            prefix='run/snapshots/current/'
            snapshot=[m for m in members if m.name.startswith(prefix) and not m.isdir()]
            self.assertEqual(len(snapshot),len(manifest))
            self.assertEqual({m.name[len(prefix):] for m in snapshot},set(manifest))
            for name,digest in manifest.items():
                path=PurePosixPath(name)
                self.assertFalse(path.is_absolute() or '..' in path.parts)
                self.assertEqual(path.as_posix(),name)
                member=evidence.getmember(prefix+name)
                self.assertTrue(member.isfile(),name)
                body=evidence.extractfile(member).read()
                self.assertEqual(hashlib.sha256(body).hexdigest(),digest,name)
                originals[name]=body
        for variant,expected in refinement_variants.CHANGED.items():
            with self.subTest(variant=variant),tempfile.TemporaryDirectory() as directory:
                copy=Path(directory)/'guide'
                for name,body in originals.items():
                    dest=copy/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(body)
                refinement_variants.apply(copy,variant)
                changed=sorted(n for n,b in originals.items() if (copy/n).read_bytes()!=b)
                self.assertEqual(changed,sorted(expected))
                self.assertEqual((copy/'_coco-shared/contracts.md').read_bytes(),originals['_coco-shared/contracts.md'])
                policy=(copy/'_coco-shared/workflow.md').read_text()
                for boundary in ('Manual is the default.','**before\npush**','saved spec and plan','Specialist consent and personal preferences'):
                    self.assertIn(boundary,policy)
        active_after={p.relative_to(ROOT/'skills').as_posix():p.read_bytes()
                      for p in (ROOT/'skills').rglob('*') if p.is_file()}
        self.assertEqual(active_after,active_before)

    def test_observer_runs_on_copy_without_changing_actor_or_git(self):
        runner=self.runner()
        with tempfile.TemporaryDirectory() as directory:
            project=Path(directory)/'project';refinement_fixtures.prepare_discovery(project,0)
            before=runner.state(project)
            outcome=runner.observe(project,0)
            self.assertFalse(outcome['passed'])
            self.assertFalse(outcome['implemented'])
            self.assertEqual(runner.state(project),before)

    def test_version_timeout_is_observed_not_driver_abort(self):
        with tempfile.TemporaryDirectory() as directory:
            project=Path(directory)/'project';refinement_fixtures.prepare_discovery(project,0)
            original=refinement_fixtures.workflow.call
            def failing_version(project,args,**kwargs):
                if '--version' in args:raise subprocess.TimeoutExpired(args,20)
                return original(project,args,**kwargs)
            with patch.object(refinement_fixtures.workflow,'call',side_effect=failing_version):
                result=refinement_fixtures.observe_discovery(project,0)
            version=next(c for c in result['checks'] if c['id']=='preserved_version')
            self.assertFalse(version['passed']);self.assertIn('TimeoutExpired',version['error'])

    def test_owner_uses_final_request_and_no_earlier_question_span(self):
        runner=self.runner()
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);record=root/'record';(record/'owner').mkdir(parents=True)
            trial={'seed':0,'record':str(record)}
            answer={'exit':0,'thread_started':True,'process_started':True,'commands':[],'tool_items':[],
                    'messages':['{"topics":[],"question_spans":[]}']}
            with patch.object(runner,'native',return_value=answer) as native:
                result=runner.classify(root,trial,{'messages':['Earlier superseded question?','Final request has no business question.']},1)
                prompt=native.call_args.args[3]
            self.assertTrue(result['valid'])
            self.assertNotIn('Earlier superseded question?',prompt)
            bad={**answer,'messages':['{"topics":["rounding"],"question_spans":["Earlier superseded question?"]}']}
            with patch.object(runner,'native',return_value=bad):
                self.assertFalse(runner.classify(root,trial,{'messages':['Earlier superseded question?','Final request.']},2)['valid'])

    def test_owner_reply_not_counted_if_receiving_actor_never_starts(self):
        runner=self.runner()
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);project=root/'project';record=root/'record';record.mkdir()
            refinement_fixtures.prepare_discovery(project,0)
            first={'exit':0,'thread_started':True,'process_started':True,'thread':'fake','messages':['Which policy?']}
            failed={'exit':1,'thread_started':False,'process_started':False,'messages':[]}
            result={'turns':[],'states':{},'outcomes':{}}
            outcome={'implemented':False,'policy_passed':False,'passed':False}
            classification={'valid':True,'topics':['rounding'],'question_spans':['Which policy?'],'attempts':[]}
            with patch.object(runner,'native',side_effect=[first,failed]),patch.object(runner,'observe',return_value=outcome),patch.object(runner,'classify',return_value=classification):
                runner.discovery(root,{'project':str(project),'record':str(record),'seed':0},result)
            self.assertEqual(len(result['owner_events']),1)
            self.assertFalse(result['owner_events'][0]['delivered'])
            self.assertEqual(result['owner_events'][0]['known_before'],[])


if __name__=='__main__':unittest.main()
