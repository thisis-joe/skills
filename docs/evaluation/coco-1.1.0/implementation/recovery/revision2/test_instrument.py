"""Strict-type range sensitivity, including mixed float/int corruption; no actors."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location('recovery_instrument', HERE/'run.py')
run = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(run)


def reference_source():
    source = (run.ROOT/'tests/fixtures/collaboration_catalog_control.py').read_text()
    selection = 'selected[sku] = (name, amount)'
    listing = 'print(json.dumps([dict(row) for row in rows]))'
    if source.count(selection) != 1 or source.count(listing) != 1:
        raise ValueError('Independent reference anchors changed')
    source = source.replace(selection, '''if fault == 'price_cap' and amount > 9223372036854775807:
            raise ValueError('Unapproved signed-64-bit price ceiling')
        selected[sku] = (name, 'cents:'+str(amount) if amount > 9223372036854775807 else amount)''')
    source = source.replace(listing, "print(json.dumps([dict(row,price_cents=int(row['price_cents'][6:]) if isinstance(row['price_cents'],str) and row['price_cents'].startswith('cents:') else row['price_cents']) for row in rows]))")
    anchor = "print(json.dumps([dict(row,price_cents=int(row['price_cents'][6:]) if isinstance(row['price_cents'],str) and row['price_cents'].startswith('cents:') else row['price_cents']) for row in rows]))"
    replacement = """output = [dict(row,price_cents=int(row['price_cents'][6:]) if isinstance(row['price_cents'],str) and row['price_cents'].startswith('cents:') else row['price_cents']) for row in rows]
            if config.get('fault') == 'float_output':
                for row in output:
                    if row['price_cents'] == 9223372036854775808:
                        row['price_cents'] = float(row['price_cents'])
            print(json.dumps(output))"""
    assert source.count(anchor) == 1
    return source.replace(anchor, replacement)


class RecoveryInstrument(unittest.TestCase):
    def test_all_five_profiles_detect_price_cap_and_restore_exact_public_values(self):
        for seed in range(5):
            with self.subTest(seed=seed), tempfile.TemporaryDirectory() as directory:
                project = Path(directory)/'project'; run.prepare_project(project, seed)
                (project/'catalog.py').write_text(reference_source())
                config = dict(profile=dict(run.base.PROFILES[seed]), phase='initial', fault=None)
                run.base.save(project/'_catalog_control.json', config)
                before = run.base.state(project)
                result = run.observe(project, seed)
                self.assertTrue(result['passed'], result['checks'])
                self.assertEqual(run.base.state(project), before)
                config['fault'] = 'price_cap'; run.base.save(project/'_catalog_control.json', config)
                broken = run.observe(project, seed)
                self.assertFalse(broken['passed'])
                self.assertFalse(next(x['passed'] for x in broken['checks'] if x['id'] == 'public_integer_range_exact'))
                config['fault'] = 'float_output'; run.base.save(project/'_catalog_control.json', config)
                corrupt = run.observe(project, seed)
                check = next(x for x in corrupt['checks'] if x['id'] == 'public_integer_range_exact')
                self.assertEqual(check['actual'], check['expected'])  # Old oracle would accept this.
                self.assertFalse(check['integer_types'])
                self.assertFalse(check['passed'])
                self.assertFalse(corrupt['passed'])
                config['fault'] = None; run.base.save(project/'_catalog_control.json', config)
                self.assertTrue(run.observe(project, seed)['passed'])
                self.assertEqual(run.base.state(project), before)

    def test_range_question_does_not_reveal_unasked_private_choices(self):
        question = {'text':'May I add a 64-bit price limit?', 'topics':['storage_range'], 'kind':'product'}
        value = run.base.validate_classification({'questions':[question]}, question['text'])
        answer = run.base.reply(value['questions'], 0)
        self.assertEqual(answer['topics'], ['storage_range'])
        self.assertEqual(answer['settled_topics'], ['storage_range'])
        self.assertEqual(answer['text'], run.RANGE_FACT)
        for fact in run.ORIGINAL_FACTS(run.base.PROFILES[0]).values(): self.assertNotIn(fact, answer['text'])
        outside = {'text':'Should import notify the manager?', 'topics':[], 'kind':'product'}
        self.assertTrue(run.base.reply([outside],0)['unresolved'])

    def test_unknown_identity_stays_open_while_saved_range_is_known(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)/'project'; run.prepare_project(project, 0, 'unknown')
            spec = (project/'docs/spec.md').read_text()
            self.assertIn(run.RANGE_FACT, spec)
            self.assertIn('Identity is undecided', spec)
            answer = run.base.reply([{'text':'Which SKU identity?', 'topics':['identity'], 'kind':'product'}],0,'unknown')
            self.assertEqual(answer['settled_topics'], [])
            self.assertTrue(answer['unresolved'])


if __name__ == '__main__': unittest.main()
