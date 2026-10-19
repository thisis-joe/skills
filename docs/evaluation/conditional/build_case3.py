from pathlib import Path
import subprocess,json,difflib,os,hashlib
r=Path('/tmp/lets-conditional-validation/case3-precommit'); (r/'project/.githooks').mkdir(parents=True);(r/'project/scripts').mkdir(); (r/'evidence').mkdir()
p=r/'project'
package={'name':'commit-check-fixture','private':True,'packageManager':'npm@10.9.2','scripts':{'prepare':'node scripts/existing-prepare.mjs','policy:check':'node scripts/policy.mjs','test':'node --test scripts/example.test.mjs'},'devDependencies':{'prettier':'3.4.2','lint-staged':'15.2.10'}}
(p/'package.json').write_text(json.dumps(package,indent=2)+'\n')
(p/'package-lock.json').write_text(json.dumps({'name':package['name'],'lockfileVersion':3,'packages':{'':{'name':package['name'],'devDependencies':package['devDependencies']},'node_modules/prettier':{'version':'3.4.2'},'node_modules/lint-staged':{'version':'15.2.10'}}},indent=2)+'\n')
(p/'ci.yml').write_text('steps:\n  - run: npm ci --ignore-scripts\n  - run: npm test\n')
(p/'.prettierrc.json').write_text('{"semi": false, "singleQuote": true}\n')
(p/'.prettierignore').write_text('generated/\n')
(p/'scripts/existing-prepare.mjs').write_text('console.log("existing prepare retained");\n')
(p/'scripts/policy.mjs').write_text('console.log("existing policy retained");\n')
(p/'scripts/example.test.mjs').write_text('import {test} from "node:test"; import assert from "node:assert/strict"; test("public fixture behavior",()=>assert.equal(2+2,4));\n')
before='#!/bin/sh\nset -eu\nnpm run policy:check\n'
(p/'.githooks/pre-commit').write_text(before); (p/'.githooks/pre-commit').chmod(0o755)
(p/'README.md').write_text('The project uses .githooks with a local core.hooksPath. Existing prepare is independent. Formatting authority: .prettierrc.json/.prettierignore. Do not introduce Husky. Typecheck script is intentionally absent. Lock is a fixture inventory, not a complete installable lock.\n')
env={**os.environ,'GIT_CONFIG_NOSYSTEM':'1','GIT_CONFIG_GLOBAL':'/dev/null','GIT_AUTHOR_NAME':'Fixture Validator','GIT_AUTHOR_EMAIL':'fixture@example.invalid','GIT_COMMITTER_NAME':'Fixture Validator','GIT_COMMITTER_EMAIL':'fixture@example.invalid','npm_config_cache':str(r/'npm-cache'),'npm_config_update_notifier':'false','npm_config_offline':'true'}
logs=[]
def run(cmd,label):
    q=subprocess.run(cmd,cwd=p,env=env,text=True,capture_output=True)
    (r/'evidence'/f'{label}.txt').write_text(q.stdout+q.stderr)
    logs.append({'command':cmd,'exit':q.returncode,'output':f'evidence/{label}.txt'});return q
assert run(['git','init','-b','feature/commit-checks'],'git-init').returncode==0
files=['package.json','package-lock.json','ci.yml','.prettierrc.json','.prettierignore','scripts/existing-prepare.mjs','scripts/policy.mjs','scripts/example.test.mjs','.githooks/pre-commit','README.md']
run(['git','add','--',*files],'baseline-stage');run(['git','commit','-m','fixture: establish existing project policy'],'baseline-commit')
base=run(['git','rev-parse','HEAD'],'base').stdout.strip()
fmt_hash=hashlib.sha256((p/'.prettierrc.json').read_bytes()).hexdigest()
after='#!/bin/sh\nset -eu\nnpm exec --offline --no -- lint-staged\nnpm run policy:check\n# No typecheck script exists; this check remains unavailable.\nnpm test\n'
(p/'.githooks/pre-commit').write_text(after); (p/'.lintstagedrc.json').write_text('{"*": "prettier --ignore-unknown --write"}\n')
(r/'hook.diff').write_text(''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='a/.githooks/pre-commit',tofile='b/.githooks/pre-commit')))
run(['sh','-n','.githooks/pre-commit'],'shell-syntax')
run(['npm','test'],'existing-tests')
run(['git','config','--local','core.hooksPath','.githooks'],'local-hook-path')
(p/'supported.js').write_text('const value = "fixture";\n')
(p/'unrelated-user.txt').write_text('not staged; preserve me\n')
run(['git','add','--','.githooks/pre-commit','.lintstagedrc.json','supported.js'],'stage-owned')
blocked=run(['git','commit','-m','fixture: prepare commit-time checks'],'real-hook-commit')
newhead=run(['git','rev-parse','HEAD'],'head-after-hook').stdout.strip()
assert blocked.returncode!=0 and newhead==base
assert (p/'unrelated-user.txt').read_text()=='not staged; preserve me\n'
assert fmt_hash==hashlib.sha256((p/'.prettierrc.json').read_bytes()).hexdigest()
run(['git','status','--short'],'status')
(r/'checks.json').write_text(json.dumps({'base':base,'head_after_blocked_commit':newhead,'hook_blocked_commit':True,'block_cause':'missing local lint-staged in offline/no-install mode; not a demonstrated test failure','prepare_preserved':True,'format_policy_sha256_unchanged':fmt_hash,'missing_typecheck_reported':True,'unrelated_untracked_preserved':True,'real_format_staged_only':'unavailable: prettier/lint-staged absent','successful_real_hook_commit':'unavailable: dependencies absent','failing_test_blocks_hook':'unavailable: lint-staged prerequisite cannot run','actual_activation':'temporary fixture local core.hooksPath only; no project or global activation'},indent=2)+'\n')
(r/'evidence/commands.json').write_text(json.dumps(logs,indent=2)+'\n')
(r/'README.md').write_text('''# Case 3 — pre-commit verification preparation
Owner: lets-verify creates/tests the harness; lets-build owns an actual project change and reviewed commit.

Reused the supplied .githooks runner, npm manager declaration/lock/CI, .prettierrc.json and .prettierignore. The project did not choose Husky, so no second runner or new dependency was proposed. Existing prepare and policy check survive. `.lintstagedrc.json` formats known supported staged files through existing Prettier policy; hook runs the real npm lint-staged command first, preserves policy:check, then npm test. Missing typecheck is explicitly unavailable and no invented npm run typecheck is present. Fixture manifest already declares the tools but they are absent on disk; no dependency install ran. The fixture lock only inventories intended versions.

Actual checks: sh -n passed, the fixture's real npm test passed, a real Git commit invoked the hook and failed on absent lint-staged with offline/no-install flags, preserving HEAD and unrelated untracked data. Required successful format/staged-content/commit smoke and intentional test-failure smoke remain unavailable. A missing-tool block alone does not establish a fully functioning pre-commit setup. Files remain staged in the disposable fixture for inspection. No --no-verify, global hook setting, or repository hook activation was used.

This is prepared with gaps, not complete enforcement. Once already declared dependencies are available in an authorized project install, stage a supported file with an unrelated unstaged hunk, run npm exec --offline --no -- lint-staged, inspect index/worktree to prove only staged content is formatted, commit through the hook, then make the public test fail and prove that next commit is blocked. Add a typecheck script only after the project supplies/authorizes its real command. Rollback is the diff/config plus baseline commit in checks.json. [Official lint-staged documentation](https://github.com/lint-staged/lint-staged) is the current runner reference; no obsolete Husky header was copied.
''')
print(json.dumps({'case':3,'actual_blocked_commit_exit':blocked.returncode,'checks':'checks.json'}))
