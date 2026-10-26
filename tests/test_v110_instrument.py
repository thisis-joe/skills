"""Decision-observer sensitivity and honest owner-delivery boundaries."""
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('v110_instrument', ROOT/'docs/evaluation/coco-1.1.0/implementation/run.py')
run = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(run)
COLLECT_SPEC = importlib.util.spec_from_file_location('v110_collection', ROOT/'docs/evaluation/coco-1.1.0/implementation/collect.py')
collect = importlib.util.module_from_spec(COLLECT_SPEC); COLLECT_SPEC.loader.exec_module(collect)


class V110Instrument(unittest.TestCase):
    def reference(self, project, seed):
        run.prepare_project(project, seed)
        shutil.copyfile(ROOT/'tests/fixtures/collaboration_catalog_control.py', project/'catalog.py')
        config = dict(profile=dict(run.PROFILES[seed]), phase='initial', fault=None)
        run.save(project/'_catalog_control.json', config)
        return config

    def test_all_profiles_pass_fail_on_policy_mutations_then_restore(self):
        for seed in range(5):
            with self.subTest(seed=seed), tempfile.TemporaryDirectory() as directory:
                project = Path(directory)/'project'; config = self.reference(project, seed)
                original = json.loads(json.dumps(config)); before = run.state(project)
                self.assertTrue(run.observe(project, seed)['passed'])
                self.assertEqual(run.state(project), before)
                for key, mutation, target in [
                    ('identity', 'exact' if config['profile']['identity'] == 'fold' else 'fold', 'chosen_emitted_sku'),
                    ('collision', 'first' if config['profile']['collision'] != 'first' else 'last', 'chosen_stored_collision'),
                    ('invalid', 'skip' if config['profile']['invalid'] == 'atomic' else 'atomic', 'chosen_malformed_policy'),
                ]:
                    changed = json.loads(json.dumps(original)); changed['profile'][key] = mutation
                    run.save(project/'_catalog_control.json', changed)
                    result = run.observe(project, seed)
                    self.assertFalse(result['passed'], (seed, key))
                    self.assertFalse(next(x['passed'] for x in result['checks'] if x['id'] == target), (seed, key))
                    run.save(project/'_catalog_control.json', original)
                    self.assertTrue(run.observe(project, seed)['passed'])
                self.assertEqual(run.state(project), before)

    def test_question_outside_known_topics_reaches_owner_as_unresolved(self):
        final = 'Should we email the buyer whenever import fails?'
        value = {'questions': [{'text': final, 'topics': [], 'kind': 'product'}]}
        classified = run.validate_classification(value, final)
        answer = run.reply(classified['questions'], 0)
        self.assertEqual(answer['topics'], [])
        self.assertEqual(answer['unresolved'], [final])
        self.assertIn(final, answer['text'])
        self.assertIn('Keep dependent behavior pending', answer['text'])
        self.assertNotIn('lowercase', answer['text'])

    def test_emitted_identity_answer_is_complete_and_does_not_reveal_other_choices(self):
        ask = [{'text': 'What SKU spelling should list emit?', 'topics': ['identity'], 'kind': 'product'}]
        for seed in range(5):
            answer = run.reply(ask, seed)
            self.assertEqual(answer['topics'], ['identity'])
            self.assertIn('Store and emit', answer['text'])
            self.assertNotIn(run.facts(run.PROFILES[seed])['collision'], answer['text'])
            self.assertNotIn(run.facts(run.PROFILES[seed])['invalid'], answer['text'])
        unresolved = run.reply(ask, 0, 'unknown')
        self.assertTrue(unresolved['unresolved'])
        self.assertIn('not decided', unresolved['text'])
        self.assertNotIn('Store and emit', unresolved['text'])

    def test_nonfinal_or_fabricated_question_span_is_rejected(self):
        with self.assertRaises(ValueError):
            run.validate_classification({'questions': [{'text': 'Old question?', 'topics': ['identity'], 'kind': 'product'}]}, 'Current final reply.')

    def test_failed_receiving_invocation_is_not_delivered_owner_answer(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); project = root/'project'; record = root/'record'; record.mkdir()
            run.prepare_project(project, 0); (project/'.guide').mkdir()
            trial = dict(id='trial', kind='primary', seed=0, arm='candidate', project=str(project), record=str(record))
            first = dict(exit=0, process_started=True, thread_started=True, thread='fake', messages=['How should SKU case work?'])
            failed = dict(exit=1, process_started=False, thread_started=False, messages=[])
            classification = dict(valid=True, questions=[{'text': first['messages'][0], 'topics': ['identity'], 'kind': 'product'}], attempts=[])
            with patch.object(run, 'native', side_effect=[first, failed]), patch.object(run, 'classify', return_value=classification):
                run.one(root, trial)
            result = json.loads((record/'result.json').read_text())
            self.assertFalse(result['stable'])
            self.assertFalse(result['owner_events'][0]['delivered'])
            self.assertFalse((record/'final-project').exists())

    def test_known_and_unknown_sources_keep_distinct_surviving_state(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for kind in ['known', 'unknown']:
                project = root/kind; run.prepare_project(project, 0, kind)
                spec = (project/'docs/spec.md').read_text(); plan = (project/'docs/plan.md').read_text()
                self.assertIn(run.facts(run.PROFILES[0])['collision'], spec)
                self.assertIn('Sole execution state', plan)
                if kind == 'known':
                    self.assertIn('Originally preserve SKU case', spec)
                    self.assertIn('owner now chose lowercase', spec)
                    self.assertIn('suppliers send case variants', spec)
                else:
                    self.assertIn('Identity is undecided', spec)
                    self.assertNotIn('Store and emit', spec)
                    self.assertIn('dependent implementation remains pending', plan)

    def test_blind_controls_have_real_wrong_output_and_missing_runtime(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); wrong = root/'wrong'; browser = root/'browser'
            collect.wrong_output(wrong); collect.browser_pending(browser)
            observed = json.loads((wrong/'public-outcomes.json').read_text())['final']
            self.assertTrue(observed['implemented'])
            self.assertFalse(observed['passed'])
            self.assertFalse(next(x['passed'] for x in observed['checks'] if x['id'] == 'chosen_emitted_sku'))
            self.assertIn('All required CLI checks passed', (wrong/'worker-1-final.md').read_text())
            self.assertEqual(json.loads((browser/'public-outcomes.json').read_text())['required_browser'], 'unavailable')
            self.assertIn('verification complete', (browser/'worker-1-final.md').read_text())
            before = collect.artifact_hashes(wrong)
            head = wrong/'final-project/.git/HEAD'; head.write_text('ref: refs/heads/altered\n')
            self.assertNotEqual(collect.artifact_hashes(wrong), before)


if __name__ == '__main__': unittest.main()
