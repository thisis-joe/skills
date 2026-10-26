"""Protect owner fact privacy and truthful intervention accounting."""
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
FOLDER=ROOT/'docs/evaluation/collaboration-value'
sys.path.insert(0,str(FOLDER))
spec=importlib.util.spec_from_file_location('collaboration_runner',FOLDER/'run.py')
runner=importlib.util.module_from_spec(spec);spec.loader.exec_module(runner)
from engine import _validated_classification


class OwnerBoundaryTests(unittest.TestCase):
    def session(self):
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup)
        root=Path(temp.name)
        return runner.Session(dict(project=str(root),record=str(root/'records'),
                                   owner=str(root/'owner'),family='lifecycle',seed=0))

    def question(self,session,topics,text='How should item identity work?'):
        classified=dict(questions=[dict(text=text,topics=topics,kind='product')],
                        completion_claim=False,parse_error=None)
        with patch.object(runner,'classify_question',return_value=classified):
            return session.answer(dict(messages=[text]),'resumed')

    def test_only_asked_facts_are_released_and_launch_failure_is_not_delivery(self):
        session=self.session();reply,event=self.question(session,['identity'])
        self.assertIn('lowercase SKU keys',reply)
        self.assertNotIn('Reject the entire import',reply)
        self.assertNotIn('zero-price',reply)
        self.assertEqual(session.revealed,[])
        failed=dict(seconds=.1,thread='requested-old-thread',messages=[],exit=1,
                    process_started=False,thread_started=False)
        with patch.object(runner,'native',return_value=failed):
            session.actor(reply,'resumed')
        self.assertFalse(event['delivered']);self.assertTrue(event['attempted'])
        self.assertEqual(session.revealed,[])

    def test_actual_thread_start_commits_fact_delivery_once(self):
        session=self.session();reply,event=self.question(session,['identity'])
        reached=dict(seconds=.1,thread='new-thread',messages=['done'],exit=0,
                     process_started=True,thread_started=True)
        with patch.object(runner,'native',return_value=reached):
            session.actor(reply,'resumed')
        self.assertTrue(event['delivered']);self.assertEqual(session.revealed,['identity'])
        again,event2=self.question(session,['identity'])
        self.assertEqual(event2['repeated_topics'],['identity'])
        self.assertEqual(event2['new_topics'],[])

    def test_summary_correction_does_not_disclose_unrelated_hidden_facts(self):
        session=self.session()
        reply=session.correction(dict(checks=[dict(id='summary_uses_agreed_rule',passed=False)]),'resumed')
        self.assertEqual(set(session.owner_events[-1]['topics']),{'report','summary_contract'})
        self.assertIn('excludes zero-price',reply)
        self.assertNotIn('lowercase SKU keys',reply)
        self.assertNotIn('Reject the entire import',reply)

    def test_public_resume_questions_get_real_contract_without_future_initial_leak(self):
        session=self.session();reply,event=self.question(session,['summary_contract','import_contract'])
        self.assertIn('supplier,count,total_cents',reply)
        self.assertIn('different bytes fails',reply)
        self.assertNotIn('excludes zero-price',reply)
        self.assertNotIn('batch',session.public_facts('initial')['import_contract'])

    def test_changed_collision_fact_does_not_reinstate_obsolete_stored_row_policy(self):
        session=self.session()
        for collision in ('first','error'):
            session.profile={**session.profile,'collision':collision}
            initial=session.private_facts('initial')['collision']
            changed=session.private_facts('resumed')['collision']
            self.assertIn('stored',initial)
            self.assertIn('later ordinary batch updates',changed)
            self.assertNotIn('keep an existing stored row',changed)
            self.assertNotIn('stored key also rejects',changed)

    def test_classifier_requires_verbatim_question_and_rejects_unknown_topics(self):
        text='How should SKU case work?'
        with self.assertRaises(ValueError):
            _validated_classification('{"questions":[{"text":"Invented question?","topics":["identity"],"kind":"product"}]}',text)
        with self.assertRaises(ValueError):
            _validated_classification('{"questions":[{"text":"How should SKU case work?","topics":["private-secret"],"kind":"product"}]}',text)

    def test_pending_product_question_precedes_quality_correction(self):
        session=self.session();session.trial['initial_commit']='base'
        turn=dict(messages=['How should duplicates work?'],exit=0,timeout=False,thread_started=True)
        answer=(dict(reply='Use last row',questions=[dict(text='How should duplicates work?',topics=['collision'],kind='product')]),)
        event=answer[0]
        observations=[dict(passed=True,checks=[],actions=[])]
        with patch.object(session,'actor',side_effect=[turn,None]), \
             patch.object(session,'answer',return_value=('Use last row',event)), \
             patch.object(runner,'verify',side_effect=observations), \
             patch.object(runner,'committed_product_delta',return_value=['catalog.py']), \
             patch.object(session,'correction') as correction:
            result=session.initial()
        correction.assert_not_called()
        self.assertEqual(result['status'],'execution-failed')

    def test_scheduled_trial_question_does_not_block_ready_checkpoint(self):
        session=self.session();session.trial['initial_commit']='base'
        text='Does the slice behave as expected in your trial?'
        turn=dict(messages=[text],exit=0,timeout=False,thread_started=True)
        classified=dict(questions=[dict(text=text,topics=[],kind='checkpoint')],
                        completion_claim=False,parse_error=None)
        observation=dict(passed=True,checks=[],actions=[])
        with patch.object(session,'actor',return_value=turn) as actor, \
             patch.object(runner,'classify_question',return_value=classified), \
             patch.object(runner,'verify',return_value=observation), \
             patch.object(runner,'committed_product_delta',return_value=['catalog.py']):
            result=session.initial()
        self.assertEqual(result['status'],'ready')
        self.assertEqual(actor.call_count,1)
        self.assertFalse(any(e.get('delivered') for e in session.owner_events))

    def test_lifecycle_resume_result_is_recorded_without_aliasing_outcome_as_snapshot(self):
        session=self.session();session.trial.update(id='synthetic',arm='bare',seed=0)
        state=dict(head='revision',files={},status='?? personal-notes.txt',branch='feature/example')
        outcome=dict(passed=False,checks=[dict(id='summary_uses_agreed_rule',passed=False)],actions=[])
        with patch.object(runner,'snapshot',return_value=state), \
             patch.object(session,'initial',return_value=dict(status='ready')), \
             patch.object(session,'change',return_value=dict(status='checkpoint-stop')), \
             patch.object(session,'resumed',return_value=dict(status='ready')), \
             patch.object(runner,'verify',return_value=outcome):
            result=session.run()
        self.assertTrue(result['stages']['resume_exposed_pending_summary'])
        self.assertIsNone(result['review_source_unchanged'])
        self.assertTrue((session.record/'result.json').exists())


if __name__=='__main__':unittest.main()
