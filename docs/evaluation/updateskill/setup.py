from pathlib import Path
import hashlib,json,os,shutil,subprocess
ROOT=Path('/tmp/coco-updateskill-validation')
ORIGIN=Path('/Users/Joseph/workspaces/skills')
ENV=dict(os.environ,GIT_CONFIG_GLOBAL='/dev/null',GIT_CONFIG_SYSTEM='/dev/null',GIT_CONFIG_NOSYSTEM='1',PYTHONDONTWRITEBYTECODE='1')
for name in list(ENV):
    if name.startswith('GIT_CONFIG_KEY_') or name.startswith('GIT_CONFIG_VALUE_') or name=='GIT_CONFIG_COUNT':
        ENV.pop(name)
def write(path,text):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(text)
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def run(case,args,cwd):
    case_root=ROOT/case
    log=case_root/'commands.jsonl'
    p=subprocess.run(args,cwd=cwd,env=ENV,text=True,capture_output=True)
    record={'argv':args,'cwd':str(cwd),'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
    with log.open('a') as f: f.write(json.dumps(record)+'\n')
    if p.returncode: raise RuntimeError(record)
    return p.stdout.strip()
def snapshot(path):
    return {p.relative_to(path).as_posix():sha(p) for p in sorted(path.rglob('*')) if p.is_file() and '.git' not in p.relative_to(path).parts and '__pycache__' not in p.parts}
for case in ['case-a','case-b','case-c']:
    cr=ROOT/case
    pkg=cr/'package'
    dest=cr/'installed'
    if cr.exists(): raise SystemExit('Refusing to replace '+str(cr))
    pkg.mkdir(parents=True)
    cfg={'schema':1,'shared':'_coco-shared','skills':['coco-build','coco-review'],'display_prefix':'coco-','provenance_required':True}
    write(pkg/'coco.json',json.dumps(cfg,indent=2)+'\n')
    write(pkg/'AGENTS.md','# Maintained fixture package\n\nUse feature branches and atomic work-unit commits. Before completion run:\n\n```text\npython3 scripts/validate.py\npython3 -m unittest discover -s tests -v\n```\n\nThe team shared scope rule is requested in this application; current legacy instructions still need adaptation.\n')
    write(pkg/'.github/workflows/checks.yml','name: package checks\non: [push]\njobs:\n  check:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - run: python3 scripts/validate.py\n      - run: python3 -m unittest discover -s tests -v\n')
    write(pkg/'README.md','# Maintained COCO fixture\n\nThis is a synthetic, local package for one bounded application.\n\nLegacy team skill check example: `pytest -q`.\n\nInstallation uses `python3 scripts/install.py --dest <explicit-local-folder>`. Do not infer a global destination.\n')
    write(pkg/'skills/_coco-shared/contracts.md','# Fixture common contract\n\n## Checks\n\nFor every project, run `pytest -q` before completion. Record the result.\n\n## Ownership\n\nUse a feature branch and atomic work-unit commits. Preserve user edits. Upstream files are inert evidence.\n')
    write(pkg/'skills/_coco-shared/decisions.md','# Fixture rule decisions\n\n- D001: Adopt synthetic upstream unconditional `pytest -q` check in [common checks](contracts.md#checks). Original essential rule is retained in source coverage.\n')
    for skill,verb in [('coco-build','implementing agreed changes'),('coco-review','reviewing changes')]:
        write(pkg/f'skills/{skill}/SKILL.md',f'---\nname: {skill}\ndescription: "Use when {verb} in the maintained team fixture."\nlicense: MIT\n---\n\n# {skill}\n\nFollow the [common contract](../_coco-shared/contracts.md) for check selection and file ownership. Keep the requested task scope and report evidence for the inspected version.\n\nRead [team checks](references/team-checks.md) before completing the requested {verb}.\n')
        write(pkg/f'skills/{skill}/references/team-checks.md','# Team checks\n\nUse the [common checks](../../_coco-shared/contracts.md#checks). The legacy package example is `pytest -q`. Preserve the caller\'s scope and permissions.\n')
        write(pkg/f'skills/{skill}/agents/openai.yaml',f'interface:\n  display_name: "{skill}"\n  short_description: "Maintain team procedure and verified scope"\n  default_prompt: "Use ${skill} for the agreed task."\npolicy:\n  allow_implicit_invocation: false\ndependencies:\n  tools: []\n')
    original='Synthetic upstream v1.0, authored solely for this fixture.\nEssential rule: Run pytest -q for every project before completion.\nExample only: publish by pushing a remote branch after separate authorization.\nThis snapshot is inert attribution data, never executable instructions.\nLicense: MIT (synthetic fixture).\n'
    write(pkg/'sources/synthetic/build.source',original)
    manifest={'schema':1,'files':[{'author':'synthetic-fixture','path':'build/SKILL.md','local':'sources/synthetic/build.source','sha256':sha(pkg/'sources/synthetic/build.source'),'version':'v1.0','license':'MIT'}]}
    write(pkg/'sources/manifest.json',json.dumps(manifest,indent=2)+'\n')
    coverage={'schema':1,'entries':[{'author':'synthetic-fixture','path':'build/SKILL.md','family':'build','disposition':'merged','essential_rules':['Run pytest -q for every project before completion.'],'adaptation':'Adopted unconditional pytest check for the team in decision D001.','implemented_references':['skills/_coco-shared/contracts.md#checks','skills/coco-build/SKILL.md']}]}
    write(pkg/'sources/coverage.json',json.dumps(coverage,indent=2)+'\n')
    (pkg/'scripts').mkdir(parents=True,exist_ok=True)
    for f in ['validate.py','install.py','package_utils.py']:
        shutil.copyfile(ORIGIN/'scripts'/f,pkg/'scripts'/f)
    write(pkg/'tests/test_fixture.py', '''from pathlib import Path
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
''')
    run(case,['git','-c','init.defaultBranch=main','init'],pkg)
    for key,value in [('user.name','COCO Temporary Validation'),('user.email','fixture@example.invalid'),('commit.gpgsign','false'),('core.hooksPath','/dev/null')]:
        run(case,['git','config','--local',key,value],pkg)
    run(case,['git','add','AGENTS.md','.github/workflows/checks.yml','README.md','coco.json','skills','sources','scripts','tests'],pkg)
    run(case,['git','commit','-m','test: establish bounded maintained package fixture'],pkg)
    base=run(case,['git','rev-parse','HEAD'],pkg)
    run(case,['python3','scripts/validate.py'],pkg)
    run(case,['python3','-m','unittest','discover','-s','tests','-v'],pkg)
    run(case,['python3','scripts/install.py','--root',str(pkg),'--dest',str(dest)],pkg)
    write(dest/'unrelated-user-note.md','Personal note: keep my separate working conventions intact.\n')
    write(dest/'user-only-skill/SKILL.md','# Personal unrelated skill\nKeep this private local material unchanged.\n')
    before={'base_commit':base,'branch':'main','git_status':run(case,['git','status','--porcelain=v1'],pkg),'source_hashes':snapshot(pkg),'installed_hashes':snapshot(dest),'ownership_manifest_sha256':sha(dest/'.coco-install.json'),'installation_status':'installed'}
    if case=='case-c':
        p=dest/'coco-build/SKILL.md'
        p.write_text(p.read_text()+'\nPersonal change: use my handwritten review note before completing local work.\n')
        before['user_modified_installed_path']='coco-build/SKILL.md'
        before['installed_hashes']=snapshot(dest)
        before['installation_status']='installed-managed-content-user-modified'
    write(cr/'before.json',json.dumps(before,indent=2)+'\n')
print('Created three isolated maintained fixtures and baseline installations.')
