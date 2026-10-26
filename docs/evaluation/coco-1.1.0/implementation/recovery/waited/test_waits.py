"""Cooldown accounting regression tests; no native calls."""
import importlib.util
from pathlib import Path
import unittest
from unittest import mock
import tempfile
import json

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('waited',HERE/'run.py')
run=importlib.util.module_from_spec(spec);spec.loader.exec_module(run)
START=1760000000.0

def line(offset,delay):
    date=run.datetime.fromtimestamp(START+offset,run.timezone.utc).isoformat().replace('+00:00','Z')
    return date+'  WARN codex_core::responses_retry: stream disconnected - retrying sampling request (1/5 in '+str(delay)+'s)... sampling_error=exceeded retry limit, last status: 429 Too Many Requests'

class WaitBudgets(unittest.TestCase):
    def test_explicit_model_binding_for_initial_and_resumed_native_calls(self):
        initial=['codex','exec','--ignore-user-config','--approve-for-me','--json','-C','/fixture','-']
        resumed=initial[:-1]+['resume','01234567-1234-1234-1234-0123456789ab','-']
        options=['--model','gpt-6.1-sol','-c','model_reasoning_effort="high"']
        for original in [initial,resumed]:
            actual=run.model_selection.bind_args(original)
            index=actual.index('resume')+1 if 'resume' in actual else 2
            self.assertEqual(actual[index:index+4],options)
            self.assertEqual(actual[:index]+actual[index+4:],original)
            self.assertNotIn('--dangerously-bypass-approvals-and-sandbox',actual)
        argv=initial.copy();fake=mock.Mock()
        run.model_selection.ModelSubprocess(fake).Popen(argv,stdin='input')
        self.assertEqual(argv,run.model_selection.bind_args(initial))
        fake.Popen.assert_called_once_with(argv,stdin='input')
    def test_model_verification_requires_current_invocation_context(self):
        result={'thread':'fixture','started_at':'2026-10-26T12:00:00+00:00','finished_at':'2026-10-26T12:00:30+00:00'}
        matching={'model':'gpt-6.1-sol','effort':'high','turn_id':'current'}
        cases=[({**matching,'timestamp':'2026-10-26T11:59:59Z'},False),
               ({**matching,'timestamp':'2026-10-26T12:00:10Z','model':'gpt-6-sol'},False),
               ({**matching,'timestamp':'2026-10-26T12:00:10Z'},True)]
        for context,expected in cases:
            with self.subTest(context=context):
                self.assertEqual(run.model_selection.verify_contexts(result,[context])['verified'],expected)
    def test_classifier_can_wait_longer_than_its_active_budget_but_not_compute_longer(self):
        text=line(10,514)
        ongoing=run.budget(text,START,START+300,300,90)
        self.assertEqual(ongoing['charged_remainder_seconds'],10)
        self.assertIsNone(ongoing['stop_reason'])
        done=run.budget(text,START,START+604,604,90)
        self.assertEqual(done['credited_cooldown_estimate_seconds'],514)
        self.assertEqual(done['charged_remainder_seconds'],90)
        self.assertEqual(done['stop_reason'],'non_cooldown_budget_exhausted')
    def test_duplicates_overlaps_and_future_notices_cannot_inflate_credit(self):
        text='\n'.join([line(10,50),line(10,50),line(30,60),line(1000,50)])
        state=run.budget(text,START,START+100,100,90)
        self.assertEqual(state['credited_cooldown_estimate_seconds'],80)
        self.assertEqual(state['charged_remainder_seconds'],20)
    def test_missing_or_malformed_notice_gives_no_credit_and_hard_cap_survives(self):
        malformed=line(0,500).replace('2025-10-09','2026-99-26')
        self.assertIn('2026-99-26',malformed)
        state=run.budget('429 Too Many Requests\n'+malformed,START,START+91,91,90)
        self.assertEqual(state['credited_cooldown_estimate_seconds'],0)
        self.assertEqual(state['stop_reason'],'non_cooldown_budget_exhausted')
        state=run.budget(line(0,10000),START,START+1890,1890,90)
        self.assertEqual(state['credited_cooldown_estimate_seconds'],1800)
        self.assertEqual(state['stop_reason'],'wall_budget_exhausted')
    def test_cumulative_wait_cap_includes_prior_calls_without_extra_compute(self):
        state=run.budget(line(10,500),START,START+110,110,90,previous_cooldown=5300)
        self.assertEqual(state['charged_remainder_seconds'],10)
        self.assertEqual(state['cohort_cooldown_estimate_seconds'],5400)
        self.assertEqual(state['stop_reason'],'cohort_cooldown_budget_exhausted')
    def test_completion_between_polls_cannot_hide_an_exhausted_budget(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            over=run.budget('',START,START+91,91,90)
            result={'exit':0,'thread_started':True,'process_started':True,'usage_events':[{}],'timeout':False,'seconds':91}
            with mock.patch.object(run.previous,'RUN_ROOT',root),mock.patch.object(run,'LAST_NATIVE_START',None),mock.patch.object(run.base.engine,'native',return_value=result),mock.patch.object(run,'budget',return_value=over):
                actual=run.native(root,root/'record',1,'question',timeout=90)
            self.assertFalse(run.base.stable(actual))
            self.assertIn('non_cooldown_budget_exhausted',actual['error'])
            self.assertTrue((root/'STOP').exists())
    def test_cancelled_malformed_or_incomplete_native_success_is_invalid(self):
        for fault in [{'interrupted':True},{'event_errors':[{'line':1}]},{'usage_events':[]}]:
            with self.subTest(fault=fault),tempfile.TemporaryDirectory() as directory:
                root=Path(directory)
                result={'exit':0,'thread_started':True,'process_started':True,'usage_events':[{}],'timeout':False,'seconds':1,**fault}
                with mock.patch.object(run.previous,'RUN_ROOT',root),mock.patch.object(run,'LAST_NATIVE_START',None),mock.patch.object(run.base.engine,'native',return_value=result):
                    actual=run.native(root,root/'record',1,'question',timeout=90)
                self.assertFalse(run.base.stable(actual))
                self.assertTrue((root/'STOP').exists())
    def test_partial_collection_ignores_admission_and_cooldown_receipts(self):
        spec=importlib.util.spec_from_file_location('partial_collector',HERE/'collect.py')
        collect=importlib.util.module_from_spec(spec);spec.loader.exec_module(collect)
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);record=root/'record';(record/'owner').mkdir(parents=True)
            (record/'turn-1.json').write_text(json.dumps({'exit':0,'state':'completed','seconds':1}))
            (record/'turn-1.events.jsonl').write_text(json.dumps({'type':'thread.started','thread_id':'test'})+'\n'+json.dumps({'type':'turn.completed','usage':{'input_tokens':1,'output_tokens':1}})+'\n')
            for suffix in ['admission','cooldown']:
                (record/('turn-1.'+suffix+'.json')).write_text('{}')
                (record/'owner'/('turn-3.'+suffix+'.json')).write_text('{}')
            (record/'owner/turn-3.json').write_text(json.dumps({'messages':['{"questions":[]}']}))
            target=root/'packet';collect.packet_trial({'record':str(record),'kind':'primary','seed':0},target)
            self.assertEqual(len(json.loads((target/'owner-events.json').read_text())),1)
            self.assertTrue((target/'worker-1-status.json').exists())
            self.assertEqual(len(list(target.glob('worker-*-status.json'))),1)
            for number in [9,10]:(record/'owner'/('turn-%d.json' % number)).write_text('{}')
            self.assertEqual([p.name for p in collect.metadata_paths(record/'owner')],['turn-3.json','turn-9.json','turn-10.json'])
            for kind in ['known','unknown']:
                target=root/kind;collect.packet_trial({'record':str(record),'kind':kind,'seed':0},target)
                context=json.loads((target/'context.json').read_text())
                if kind=='unknown':self.assertIn('Undecided',context['settled_truth']['identity'])
                else:self.assertIn('Originally preserve case',context['original_and_change'])
    def test_strict_range_and_owner_instrument_still_passes(self):
        spec=importlib.util.spec_from_file_location('strict_tests',HERE.parent/'revision2/test_instrument.py')
        inherited=importlib.util.module_from_spec(spec);spec.loader.exec_module(inherited)
        inherited.run=run
        result=unittest.TestResult()
        unittest.defaultTestLoader.loadTestsFromTestCase(inherited.RecoveryInstrument).run(result)
        self.assertTrue(result.wasSuccessful(),str(result.errors)+str(result.failures))

if __name__=='__main__':unittest.main()
