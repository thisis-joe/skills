#!/usr/bin/env python3
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
