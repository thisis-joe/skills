from pathlib import Path
import hashlib,json,sys,unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from package_utils import validate_package
class FixtureChecks(unittest.TestCase):
    def test_full_package_validation(self):
        self.assertEqual(validate_package(ROOT)['skills'],['coco-build','coco-review'])
    def test_both_entrypoints_share_contract(self):
        for name in ['coco-build','coco-review']:
            self.assertIn('../_coco-shared/contracts.md',(ROOT/'skills'/name/'SKILL.md').read_text())
    def test_original_facts_and_invocation_policy_preserved(self):
        item=json.loads((ROOT/'sources/manifest.json').read_text())['files'][0]
        self.assertEqual(hashlib.sha256((ROOT/item['local']).read_bytes()).hexdigest(),item['sha256'])
        row=json.loads((ROOT/'sources/coverage.json').read_text())['entries'][0]
        self.assertEqual(row['essential_rules'],['Run pytest -q for every project before completion.'])
        for name in ['coco-build','coco-review']:
            ui=(ROOT/'skills'/name/'agents/openai.yaml').read_text()
            self.assertIn('allow_implicit_invocation: false',ui)
            self.assertIn('tools: []',ui)
            self.assertIn('$'+name,ui)
if __name__=='__main__': unittest.main()
