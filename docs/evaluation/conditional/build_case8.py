from pathlib import Path
import subprocess,json,os,hashlib,shutil
r=Path('/tmp/lets-conditional-validation/case8-quality');r.mkdir();(r/'evidence').mkdir()
(r/'setup-brief.md').write_text('Establish one standing quality bar for this small Python CLI. No existing bar. Use unittest and a fast syntax check already documented in README/CI; enforce the quality floor. This is an unattended setup draft; coverage target is unset, so record the existing coverage artifact as measured-only. No dependencies/CI activation authorized. Owner is the project maintainer.\n')
(r/'audit-brief.md').write_text('Audit the existing quality bar on the complete feature task diff relative to fixture/main, including new files. Report weakened assertions, lower thresholds and bad exceptions. Do not fix code or change policy, install tools, or recalculate existing coverage by rerunning tests only for that metric.\n')
env={**os.environ,'GIT_CONFIG_NOSYSTEM':'1','GIT_CONFIG_GLOBAL':'/dev/null','GIT_AUTHOR_NAME':'Fixture Validator','GIT_AUTHOR_EMAIL':'fixture@example.invalid','GIT_COMMITTER_NAME':'Fixture Validator','GIT_COMMITTER_EMAIL':'fixture@example.invalid','PYTHONDONTWRITEBYTECODE':'1'}
logs=[]
def run(cmd,cwd,label):
    p=subprocess.run(cmd,cwd=cwd,env=env,text=True,capture_output=True)
    (r/'evidence'/f'{label}.txt').write_text(p.stdout+p.stderr)
    logs.append({'command':cmd,'cwd':str(cwd),'exit':p.returncode,'evidence':f'evidence/{label}.txt'});return p
# Preserve provenance for the shipped executable, copied only into disposable validation root.
scope_src=Path('/tmp/lets-frozen-candidate/skills/_lets-shared/tools/review_scope.py')
shutil.copy2(scope_src,r/'review_scope.py')
(r/'scope-source.json').write_text(json.dumps({'source':str(scope_src),'sha256':hashlib.sha256(scope_src.read_bytes()).hexdigest(),'purpose':'unmodified shipped collector used by demonstration guard'},indent=2)+'\n')
guard=r'''#!/usr/bin/env python3
"""Validation-created heuristic floor guard; shipped review_scope is the actual scope collector."""
import argparse,ast,json,re,subprocess,sys
from pathlib import Path

def git(repo,*args):
    p=subprocess.run(['git','-C',str(repo),*args],capture_output=True,text=True)
    if p.returncode: raise ValueError('git comparison unavailable')
    return p.stdout

def ast_contracts(text):
    tree=ast.parse(text)
    tests={x.name for x in ast.walk(tree) if isinstance(x,(ast.FunctionDef,ast.AsyncFunctionDef)) and x.name.startswith('test')}
    assertions={ast.dump(x,include_attributes=False) for x in ast.walk(tree) if isinstance(x,ast.Assert) or (isinstance(x,ast.Call) and isinstance(x.func,ast.Attribute) and x.func.attr.startswith('assert'))}
    return tests,assertions

def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',required=True);p.add_argument('--base',required=True);a=p.parse_args();repo=Path(a.repo)
    try:
        s=subprocess.run([sys.executable,str(Path(__file__).with_name('review_scope.py')),'--repo',str(repo),'--base',a.base],capture_output=True,text=True)
        if s.returncode:raise ValueError('scope/merge-base unavailable')
        scope=json.loads(s.stdout);findings=[]
        base=scope['comparison_commit']
        def old(path):
            p=subprocess.run(['git','-C',str(repo),'show',base+':'+path],capture_output=True,text=True)
            if p.returncode and p.stderr.startswith('fatal: path'): return ''
            if p.returncode:raise ValueError('baseline file unavailable')
            return p.stdout
        for f in scope['files']:
            path=f['path'];target=repo/path
            if target.is_symlink():raise ValueError('linked file requires separate review')
            current=target.read_text() if target.exists() else ''
            before=old(path)
            if path=='quality.json':
                prior=json.loads(before) if before else {}; now=json.loads(current)
                key='minimum_coverage_percent'
                if key in prior and (key not in now or now[key]<prior[key]):findings.append({'rule':'lowered-threshold','path':path,'line':1,'baseline':prior[key],'current':now.get(key)})
                prior_ex=prior.get('exceptions',[])
                for ex in now.get('exceptions',[]):
                    if ex not in prior_ex:
                        required={'rule','path','reason','owner','tracking','review_date'}
                        if not required.issubset(ex) or any(not ex.get(x) for x in required):findings.append({'rule':'incomplete-new-exception','path':path,'line':1})
            if path.endswith('.py'):
                for line_no,line in enumerate(current.splitlines(),1):
                    if line not in before.splitlines() and re.search(r'@(?:unittest\.)?skip|#\s*(?:noqa|type:\s*ignore)',line):
                        findings.append({'rule':'added-skip-or-suppression','path':path,'line':line_no})
                if ('/test' in path or path.startswith('tests/')) and before:
                    old_tests,old_asserts=ast_contracts(before);new_tests,new_asserts=ast_contracts(current)
                    if old_tests-new_tests:findings.append({'rule':'removed-test','path':path,'line':1})
                    if old_asserts-new_asserts:findings.append({'rule':'changed-or-weakened-assertion','path':path,'line':1,'interpretation':'heuristic; inspect exact test contract'})
        # Text comparison is deliberately heuristic, not a secret/semantic completeness claim.
        result={'outcome':'violation' if findings else 'clean','scope':scope,'findings':findings,'guard_kind':'validation-authored heuristic; inspect findings, not malicious-intent proof'}
        print(json.dumps(result,indent=2));return 1 if findings else 0
    except (ValueError,OSError,SyntaxError,UnicodeError,json.JSONDecodeError) as e:
        print(json.dumps({'outcome':'unavailable','reason':str(e),'findings':None}));return 2
if __name__=='__main__':sys.exit(main())
'''
(r/'floor_guard.py').write_text(guard)
for name in ['setup-project','audit-project']:
    p=r/name;(p/'src').mkdir(parents=True);(p/'tests').mkdir();(p/'artifacts').mkdir();(p/'.github/workflows').mkdir(parents=True)
    (p/'src/report.py').write_text('def report(items):\n    return "empty" if not items else "\\n".join(items)\n')
    (p/'tests/test_report.py').write_text('import unittest\nfrom src.report import report\nclass ReportTests(unittest.TestCase):\n    def test_empty(self):\n        self.assertEqual(report([]), "empty")\n')
    (p/'artifacts/coverage.json').write_text(json.dumps({'metric':'line coverage','percent':82.5,'kind':'supplied prior-run fixture measurement; not measured by this validation','environment':'Python CLI, full suite','measurement_id':'coverage-fixture-2026-10-16'},indent=2)+'\n')
    (p/'README.md').write_text('Python standard-library CLI. Syntax: python3 -m py_compile src/report.py. Tests: python3 -m unittest discover -s tests -v. No dependency manager. Task state is TASKS.md.\n')
    (p/'.github/workflows/check.yml').write_text('steps:\n  - run: python3 -m py_compile src/report.py\n  - run: python3 -m unittest discover -s tests -v\n')
    (p/'TASKS.md').write_text('Fixture task: quality setup/audit. This file remains fixture input; audit does not change it.\n')
    run(['git','init','-b','fixture/main'],p,name+'-init')
    if name=='audit-project':
        (p/'CONSTRAINTS.md').write_text('Canonical quality policy. Require minimum coverage 80 percent; quality.json owns numeric threshold. Do not lower thresholds, weaken tests or introduce suppressions. Existing exceptions need owner/tracking/review date. Read artifacts/coverage.json; do not rerun just to extract the metric.\n')
        (p/'quality.json').write_text(json.dumps({'minimum_coverage_percent':80,'exceptions':[{'rule':'legacy ownership','path':'src/legacy.py','reason':'upstream interface pending','owner':'maintainer','tracking':'Q-12','review_date':'2026-11-01'}]},indent=2)+'\n')
    baseline_files=['src/report.py','tests/test_report.py','artifacts/coverage.json','README.md','.github/workflows/check.yml','TASKS.md']+(['CONSTRAINTS.md','quality.json'] if name=='audit-project' else [])
    run(['git','add','--',*baseline_files],p,name+'-stage');run(['git','commit','-m','fixture: establish baseline'],p,name+'-baseline')
    run(['git','switch','-c','feature/'+name],p,name+'-branch')
# Setup establishes one new policy, takes no arbitrary coverage target from thin air.
setup=r/'setup-project'; setup_base=run(['git','rev-parse','fixture/main'],setup,'setup-base').stdout.strip()
constraints=f'''# Standing quality bar — local preparation v1
Owner: project maintainer; setup owner lets-start. Execution/fixes/real project commit belong to lets-build. Canonical policy is this file, linked by project README. No prior bar exists. Branch feature/setup-project, base {setup_base}; initial fixture was clean. Project is Python stdlib CLI, documented syntax/unittest commands match CI; task state stays TASKS.md.

| Rule/reason | Exact checker | Scope/stage | Disposition |
|---|---|---|---|
| Preserve floor: lower thresholds, weaker/deleted assertions/tests, new skips/suppressions/exceptions require review | python3 {r}/floor_guard.py --repo . --base fixture/main | complete committed/staged/unstaged/untracked task scope; task closure and proposed CI | Exit 0 clean, 1 heuristic violation needs review, 2 unavailable blocks claim. Prototype detects a subset; manual floor inspection remains required. |
| Valid Python syntax | python3 -m py_compile src/report.py | changed source during edit/task closure | blocking on failure |
| Public CLI behavior remains correct | python3 -m unittest discover -s tests -v | task closure/CI | blocking on failure |
| Coverage observation | read artifacts/coverage.json, percent 82.5, line coverage, prior fixture measurement, full-suite Python CLI conditions | review/CI evidence reuse | measured-only; no target/noise tolerance set by user. No invented ratchet or rerun just for metrics. |

Unattended setup uses the floor and flags unset policy, no interview. Coverage target/ratchet and edit-loop latency budget remain maintainer decisions before enforcing those optional dimensions. No exception currently exists for this setup. Future exception must name rule/path/reason/owner/tracking/review date and have actual authorization. No web UI exists, so browser performance/accessibility dimensions are not applicable. Independent external quality scanner unavailable; self-authored heuristic is not that independent assessment. No checkers/dependencies/hooks/CI schedule are installed or activated by this draft.
'''
(setup/'CONSTRAINTS.md').write_text(constraints)
with (setup/'README.md').open('a') as f:f.write('Canonical quality policy: CONSTRAINTS.md.\n')
setup_cmd=['python3',str(r/'floor_guard.py'),'--repo',str(setup),'--base','fixture/main'];clean=run(setup_cmd,setup,'setup-floor-clean');assert clean.returncode==0
run(['python3','-m','py_compile','src/report.py'],setup,'setup-syntax');run(['python3','-m','unittest','discover','-s','tests','-v'],setup,'setup-tests')
# Audit fixture includes all four Git layers and intentionally deficient changes.
audit=r/'audit-project'; audit_base=run(['git','rev-parse','fixture/main'],audit,'audit-base').stdout.strip()
(audit/'src/report.py').write_text('def report(items):\n    return "empty" if not items else "\\n".join(items)  # type: ignore\n')
run(['git','add','--','src/report.py'],audit,'audit-committed-stage');run(['git','commit','-m','fixture: add source suppression'],audit,'audit-committed-change')
quality=json.loads((audit/'quality.json').read_text());quality['minimum_coverage_percent']=65;quality['exceptions'].append({'rule':'skip tests','path':'tests/test_new.py','reason':'temporary'})
(audit/'quality.json').write_text(json.dumps(quality,indent=2)+'\n');run(['git','add','--','quality.json'],audit,'audit-staged-policy')
(audit/'tests/test_report.py').write_text('import unittest\nfrom src.report import report\nclass ReportTests(unittest.TestCase):\n    def test_empty(self):\n        self.assertTrue(True)\n')
(audit/'tests/test_new.py').write_text('import unittest\n@unittest.skip("temporary")\nclass NewTests(unittest.TestCase):\n    def test_future(self):\n        self.assertTrue(True)\n')
# Freeze audit scope before read-only audit. The fixture-generation step above is explicit.
def state_hash(p):
    data={str(f.relative_to(p)):hashlib.sha256(f.read_bytes()).hexdigest() for f in p.rglob('*') if f.is_file() and '.git' not in f.parts and '__pycache__' not in f.parts}
    return hashlib.sha256(json.dumps(data,sort_keys=True).encode()).hexdigest()
before=state_hash(audit);coverage_before=hashlib.sha256((audit/'artifacts/coverage.json').read_bytes()).hexdigest()
violation=run(['python3',str(r/'floor_guard.py'),'--repo',str(audit),'--base','fixture/main'],audit,'audit-floor-violation');assert violation.returncode==1
unavailable=run(['python3',str(r/'floor_guard.py'),'--repo',str(audit),'--base','does-not-exist'],audit,'audit-floor-unavailable');assert unavailable.returncode==2
result=json.loads(violation.stdout); scope=result['scope']; findings=result['findings'];layers={layer for f in scope['files'] for layer in f['layers']}
assert layers=={'committed','staged','worktree','untracked'}
assert before==state_hash(audit) and coverage_before==hashlib.sha256((audit/'artifacts/coverage.json').read_bytes()).hexdigest()
assert {f['rule'] for f in findings}>={'lowered-threshold','incomplete-new-exception','added-skip-or-suppression','changed-or-weakened-assertion'}
(r/'evidence/audit-scope.json').write_text(json.dumps(scope,indent=2)+'\n')
(r/'OUTCOMES.md').write_text('''# Setup and audit have different owners
Setup brief → lets-start. Establishing the absent standing bar produced setup-project/CONSTRAINTS.md, linked from its README, using real discovered Python syntax/unittest commands and a quality-floor guard receipt. Floor outcome is clean (exit 0) on the setup diff. Syntax and public fixture tests pass. Coverage 82.5 percent is inherited synthetic prior-run input, kept measured-only because no target/ratchet is authorized. No interview, guessed threshold, new dependency, installed hook, or CI activation occurred. Missing independent scanner and maintainer metric decisions are explicit. This is a prepared setup draft, not an independently approved project enforcement claim.

Audit brief → lets-verify. The canonical audit-project/CONSTRAINTS.md and quality.json already exist, so the audit reads them instead of establishing another bar or editing policy. Frozen base/HEAD/paths/layers/snapshot are in evidence/audit-scope.json from the actual shipped review_scope.py. The disposable audit fixture was generated before freeze; the audit afterward changed no source/policy/task file.

Concrete audit findings: committed src/report.py adds a type suppression; staged quality.json lowers minimum coverage 80→65 and adds an incomplete exception without owner/tracking/review date; unstaged tests/test_report.py replaces the observable report([]) assertion with assertTrue(True); untracked tests/test_new.py adds a skip. Heuristic guard outcome is violation (exit 1); reviewer inspection confirms those specific changes from fixture content. Assertions/skips are reported as weakened evidence, not a claim of malicious intent. The supplied existing coverage is 82.5%, above the original 80%; that observation does not authorize lowering the threshold. Its source is a fixture prior-run artifact, not a metric measured here, and no suite was rerun merely to read it. Actual coverage calculation/provider independence is unavailable.

Invalid base returns unavailable (exit 2), never clean. This demonstrates 0/1/2 distinguishability using a validation-authored demonstration guard with the unmodified shipped scope collector, not a claim that LET'S ships a full semantic scanner. The demonstration guard omits many semantic/security checks and supplies no exhaustive secret scanner. No audit fix, policy change, commit or install was made after freezing the audit snapshot. Build owns any later accepted remedy/commit; start owns a justified change in the standing bar. Future work requires only those owners' requested scoped actions, not a new audit-owned policy.
''')
(r/'checks.json').write_text(json.dumps({'setup_owner':'lets-start','audit_owner':'lets-verify','setup_guard_exit':clean.returncode,'audit_guard_exit':violation.returncode,'unavailable_guard_exit':unavailable.returncode,'audit_layers':sorted(layers),'audit_findings':findings,'audit_snapshot':scope['snapshot'],'audit_files_unchanged':before==state_hash(audit),'coverage_artifact_unchanged':True,'collector_source':'scope-source.json','guard_source':'validation-created floor_guard.py, not a shipped checker','activation':'none'},indent=2)+'\n')
(r/'evidence/commands.json').write_text(json.dumps(logs,indent=2)+'\n')
print(json.dumps({'case':8,'owners':['lets-start','lets-verify'],'exits':[clean.returncode,violation.returncode,unavailable.returncode],'layers':sorted(layers),'findings':len(findings)}))
