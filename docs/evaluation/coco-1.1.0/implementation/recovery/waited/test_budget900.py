"""Pin the same actor-only budget adjustment for both arms and resumed calls."""
import importlib.util
from pathlib import Path
import unittest
from unittest import mock
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('budget900',HERE/'budget900_run.py')
run=importlib.util.module_from_spec(spec);spec.loader.exec_module(run)
class BudgetBindings(unittest.TestCase):
    def test_actor_and_owner_budgets_are_identical_between_arms(self):
        for arm in ['current','candidate']:
            for thread in [None,'same-owned-thread']:
                for source,expected in [(420,900),(90,90)]:
                    with self.subTest(arm=arm,thread=thread,source=source),mock.patch.object(run,'ORIGINAL_NATIVE',return_value={'ok':True}) as native:
                        self.assertEqual(run.native(arm,'record',1,'unchanged prompt',thread,source),{'ok':True})
                        native.assert_called_once_with(arm,'record',1,'unchanged prompt',thread=thread,timeout=expected)
    def test_unknown_budget_is_not_silently_reinterpreted(self):
        with mock.patch.object(run,'ORIGINAL_NATIVE') as native:
            with self.assertRaises(ValueError):run.native('current','record',1,'prompt',timeout=999)
            native.assert_not_called()
if __name__=='__main__':unittest.main()
