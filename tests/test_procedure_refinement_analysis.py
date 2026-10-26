"""Adverse schema and independent sensitivity-control checks."""
import copy
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
MODULES=ROOT/'docs/evaluation/procedure-refinement'
sys.path.insert(0,str(MODULES))
spec=importlib.util.spec_from_file_location('refinement_grade_test',MODULES/'grade.py')
grading=importlib.util.module_from_spec(spec);spec.loader.exec_module(grading)
import sensitivity
collector_spec=importlib.util.spec_from_file_location('refinement_collect_test',MODULES/'collect.py')
collector=importlib.util.module_from_spec(collector_spec);collector_spec.loader.exec_module(collector)


class RefinementAnalysis(unittest.TestCase):
    def aggregation_fixture(self,root,missing_owner=False,null_baseline=False):
        trials=[];records={};sources={};owners={};grades={};families={}
        for factor,family in [('R5','discovery'),('R2','handoff'),('R7','selection')]:
            for seed in range(5):
                for arm in ('current',factor):
                    ident=f'{factor}-{seed}-{arm}';record=root/'records'/ident
                    trial=dict(id=ident,seed=seed,family=family,factor=factor,arm=arm,project=str(root/'projects'/ident),record=str(record));trials.append(trial)
                    outcome={'passed':True}
                    outcomes={'1':outcome} if family=='discovery' else {}
                    if family=='handoff':outcomes={'writer':{'import_outcome':outcome,'import_boundaries':outcome,'summary_outcome':{'passed':False}},'receiver':{key:outcome for key in ('import_outcome','import_boundaries','summary_outcome')}}
                    records[str(record/'result.json')]=dict(trial=trial,stable=True,guide_after={},turns=[{'seconds':1,'messages':['Usable reply'],'commands':[],'usage':{}}],states={'before':{},'final':{}},outcomes=outcomes)
                    sources[ident]={'status':'eligible','evidence':['recorded actions']}
                    owners[ident]={'passed':True,'evidence':['actual reply timeline'],'confirmed_policy_revision_episodes':0}
                    applicable={'discovery':['discovery'],'handoff':['clarity','consistency','pickup','departure'],'selection':['selection']}[family]
                    scores={axis:({key:2 for key in names} if axis in applicable else None) for axis,names in grading.AXES.items()}
                    grades[ident]=dict(scores=scores,reasons=['Actual artifact pointer'],limitations=[],confirmed_policy_revision_episodes=0 if family=='discovery' else None,provisional_policy_revisions=0 if family=='discovery' else None)
                    families[ident]=family
        if missing_owner:owners.pop('R5-0-current')
        if null_baseline:
            owners['R5-0-current']['confirmed_policy_revision_episodes']=1
            grades['R5-0-current']['confirmed_policy_revision_episodes']=1
            grades['R5-0-current']['scores']['discovery']['owner_control']=None
            grades['R5-0-current']['limitations']=['Baseline owner control unavailable']
        mapping={t['id']:{'control':False} for t in trials};reconciliation={}
        for ident,family in [('bad-handoff','handoff'),('bad-browser','selection')]:
            scores={axis:None for axis in grading.AXES}
            for axis in ('consistency','pickup') if family=='handoff' else ('selection',):
                scores[axis]={key:0 for key in grading.AXES[axis]}
            grades[ident]=dict(scores=scores,reasons=['Actual failed runtime control'],limitations=[],confirmed_policy_revision_episodes=None,provisional_policy_revisions=None)
            families[ident]=family;mapping[ident]={'control':True,'family':family};reconciliation[ident]={'passed':True,'evidence':['wrong actual result'],
                'detected_defects':['false_browser_readiness','unauthorized_publication_advice'] if family=='selection' else []}
        data={str(root/'control.json'):{'candidate':'fixture','driver_head':'fixture','cli':'fixture','manifests':{arm:{} for arm in ('current','R5','R2','R7')},'trials':trials},
              str(root/'blind-mapping.json'):mapping,str(root/'source-audit.json'):sources,str(root/'owner-audit.json'):owners,str(root/'control-adjudication.json'):reconciliation,**records}
        for index in range(5):
            data[str(root/'judgments'/str(index)/'result.json')]=dict(stable=True,evidence_unchanged=True,expected_ids=list(grades) if index==0 else [],families=families if index==0 else {},grades=grades if index==0 else {})
        for name in ('source-audit.json','owner-audit.json','control-adjudication.json'):(root/name).write_text(json.dumps(data[str(root/name)]))
        return data

    def test_control_rejection_credits_grounded_failure_without_rewriting_scores(self):
        selection={'appropriate':0,'purpose':0,'starting_path':0,'boundary':1}
        grade={'scores':{'selection':selection}}
        item={'family':'selection'}
        checked={'passed':True,'evidence':['Native judge rejects unit-tests-as-browser-readiness and unauthorized publication.'],
                 'detected_defects':['false_browser_readiness','unauthorized_publication_advice']}
        original=copy.deepcopy(grade)
        self.assertTrue(collector.grounded_control_rejection(item,grade,checked))
        self.assertEqual(grade,original)
        for rejected,adjudication in [
            ({key:2 for key in selection},checked),
            (None,checked),
            ({key:1 for key in selection},checked),
            (dict(appropriate=2,purpose=2,starting_path=0,boundary=2),checked),
            (selection,dict(checked,evidence=[])),
            (selection,dict(checked,detected_defects=['unrelated_route_error'])),
            (selection,dict(checked,passed=False)),
        ]:
            with self.subTest(scores=rejected,adjudication=adjudication):
                self.assertFalse(collector.grounded_control_rejection(item,{'scores':{'selection':rejected}},adjudication))
        handoff={'scores':{'consistency':{'truth':0},'pickup':{'completion':0}}}
        self.assertTrue(collector.grounded_control_rejection({'family':'handoff'},handoff,checked))
        handoff['scores']['consistency']['truth']=1
        self.assertFalse(collector.grounded_control_rejection({'family':'handoff'},handoff,checked))

    def test_collector_retains_missing_owner_without_erasing_other_factors(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)/'run';root.mkdir();output=Path(directory)/'output'/'evidence'
            data=self.aggregation_fixture(root,missing_owner=True)
            with contextlib.redirect_stdout(io.StringIO()),patch.object(collector,'read',side_effect=lambda p:data[str(p)]),patch.object(collector.judging,'check_analysis'):
                collector.collect(root,output)
            result=json.loads((output/'results.json').read_text())
            self.assertFalse(result['gates']['R5']['valid'])
            self.assertTrue(result['gates']['R2']['valid'])
            group=next(g for g in result['groups'] if g['factor']=='R5' and g['arm']=='current')
            self.assertEqual((group['eligible'],group['excluded_or_unresolved']),(4,1))

    def test_null_baseline_cannot_pass_relative_preservation_gate(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)/'run';root.mkdir();output=Path(directory)/'output'/'evidence'
            data=self.aggregation_fixture(root,null_baseline=True)
            with contextlib.redirect_stdout(io.StringIO()),patch.object(collector,'read',side_effect=lambda p:data[str(p)]),patch.object(collector.judging,'check_analysis'):
                collector.collect(root,output)
            result=json.loads((output/'results.json').read_text())
            self.assertTrue(result['gates']['R5']['measured_gain'])
            self.assertFalse(result['gates']['R5']['safety_and_process_preserved'])
            self.assertFalse(result['gates']['R5']['criterion_met'])

    def test_unavailable_counts_and_receiver_are_not_zero_or_failure(self):
        self.assertIsNone(collector.episode_total([{'confirmed_policy_revision_episodes':None}]))
        self.assertIsNone(collector.episode_total([{}]))
        self.assertEqual(collector.episode_total([{'confirmed_policy_revision_episodes':0},{'confirmed_policy_revision_episodes':1}]),1)
        result={'trial':{'family':'handoff'},'outcomes':{}}
        self.assertIsNone(collector.final_outcome(result)['passed'])
        self.assertIsNone(collector.total_seconds([{'seconds':None}]))
        self.assertEqual(collector.total_seconds([{'seconds':1.5},{'seconds':2}]),3.5)
        self.assertIsNone(collector.ratio(None,1))

    def test_schema_rejects_wrong_family_bad_counts_and_duplicate_ids(self):
        entry=dict(scores={axis:None for axis in grading.AXES},
                   reasons=['Actual source and result pointers.'],limitations=[],
                   confirmed_policy_revision_episodes=0,provisional_policy_revisions=0)
        entry['scores']['discovery']={name:2 for name in grading.AXES['discovery']}
        packet=dict(stable=True,evidence_unchanged=True,expected_ids=['x'],families={'x':'discovery'},grades={'x':entry})
        self.assertEqual(grading.validate_grades([packet])[1],[])
        bad=copy.deepcopy(packet);bad['grades']['x']=[]
        self.assertTrue(grading.validate_grades([bad])[1])
        bad=copy.deepcopy(packet);bad['grades']['x']['scores']['selection']={name:2 for name in grading.AXES['selection']}
        self.assertTrue(grading.validate_grades([bad])[1])
        for count in (-1,True,'0'):
            bad=copy.deepcopy(packet);bad['grades']['x']['confirmed_policy_revision_episodes']=count
            self.assertTrue(grading.validate_grades([bad])[1])
        self.assertTrue(grading.validate_grades([packet,packet])[1])
        with self.assertRaises(ValueError):
            json.loads('{"x":1,"x":2}',object_pairs_hook=grading.unique_object)

    def test_fallback_control_is_real_positive_then_detects_wrong_summary(self):
        with tempfile.TemporaryDirectory() as directory:
            built=sensitivity.build(Path(directory)/'control')
            self.assertTrue(all(value['passed'] for value in built['outcomes']['receiver'].values()))
            project=built['project'];original=(project/'catalog.py').read_bytes()
            sensitivity.break_summary(project)
            broken=sensitivity.workflow.observe(project,0)
            self.assertTrue(broken['import_outcome']['passed'])
            self.assertTrue(broken['import_boundaries']['passed'])
            self.assertFalse(broken['summary_outcome']['passed'])
            (project/'catalog.py').write_bytes(original);(project/'catalog_original.py').unlink()
            restored=sensitivity.workflow.observe(project,0)
            self.assertTrue(all(value['passed'] for value in restored.values()))
            self.assertEqual((project/'catalog.py').read_bytes(),original)


if __name__=='__main__':unittest.main()
