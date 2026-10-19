from pathlib import Path
import os,json,subprocess,time,hashlib
r=Path('/tmp/lets-conditional-validation/case5-cleanup');r.mkdir(); (r/'evidence').mkdir()
repo=r/'repo'; env={**os.environ,'GIT_CONFIG_NOSYSTEM':'1','GIT_CONFIG_GLOBAL':'/dev/null','GIT_AUTHOR_NAME':'Fixture Validator','GIT_AUTHOR_EMAIL':'fixture@example.invalid','GIT_COMMITTER_NAME':'Fixture Validator','GIT_COMMITTER_EMAIL':'fixture@example.invalid'}
logs=[]
def run(cmd,cwd=r):
    p=subprocess.run(cmd,cwd=cwd,env=env,text=True,capture_output=True);logs.append({'command':cmd,'cwd':str(cwd),'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr});return p
assert run(['git','init','-b','fixture/main',str(repo)]).returncode==0
(repo/'tracked.txt').write_text('base\n');(repo/'.gitignore').write_text('ignored.env\n.cache/\n')
run(['git','add','--','tracked.txt','.gitignore'],repo);run(['git','commit','-m','fixture: baseline'],repo)
base=run(['git','rev-parse','HEAD'],repo).stdout.strip()
active=r/'active-dirty'; merged=r/'merged-unused'
run(['git','worktree','add','-b','feature/active-task',str(active)],repo)
run(['git','worktree','add','-b','feature/completed-task',str(merged)],repo)
(merged/'complete.txt').write_text('completed fixture work\n');run(['git','add','--','complete.txt'],merged);run(['git','commit','-m','fixture: complete independent task'],merged)
run(['git','merge','--ff-only','feature/completed-task'],repo)
(active/'tracked.txt').write_text('uncommitted active work\n');(active/'untracked.txt').write_text('preserve\n');(active/'ignored.env').write_text('FAKE_ONLY=ignored-value\n');(active/'.cache').mkdir();(active/'.cache/fixture.bin').write_bytes(b'0'*4096)
ownership={'observation_kind':'simulated runtime/chat metadata, not host API output','worktrees':[{'path':str(repo),'managed':False,'owner':'fixture-validator','chat_active':True,'chat_pinned':False,'purpose':'primary fixture repository'},{'path':str(active),'managed':False,'owner':'active-fixture-chat','chat_active':True,'chat_pinned':True,'purpose':'active user task; no removal authorization'},{'path':str(merged),'managed':False,'owner':'fixture-validator','chat_active':False,'chat_pinned':False,'purpose':'completed unused fixture; plan-only scope'}]}
(r/'ownership.fixture.json').write_text(json.dumps(ownership,indent=2)+'\n')
# Real owned process, used solely to establish an observable active-cwd hold.
process=subprocess.Popen(['python3','-c','import time; time.sleep(300)'],cwd=active,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
try:
    inventory=run(['git','worktree','list','--porcelain'],repo).stdout
    (r/'evidence/worktrees.porcelain').write_text(inventory)
    proc=run(['lsof','-a','-p',str(process.pid),'-d','cwd','-Fn'])
    (r/'evidence/process-use.txt').write_text(proc.stdout+proc.stderr)
    entries=[]
    for item in ownership['worktrees']:
        path=Path(item['path']); branch=run(['git','branch','--show-current'],path).stdout.strip();head=run(['git','rev-parse','HEAD'],path).stdout.strip(); mb=run(['git','merge-base','HEAD','fixture/main'],path).stdout.strip()
        ancestor=run(['git','merge-base','--is-ancestor','HEAD','fixture/main'],path)
        status=run(['git','status','--short','--untracked-files=all'],path).stdout
        ignored=run(['git','ls-files','--others','--ignored','--exclude-standard'],path).stdout
        size=run(['du','-sk',str(path)]).stdout.strip()
        entries.append({**item,'branch':branch,'head':head,'base_at_creation':base,'current_merge_base':mb,'head_merged_into_fixture_main':ancestor.returncode==0,'status':status,'ignored_paths':ignored.splitlines(),'du_sk':size,'active_cwd_pid':process.pid if path==active else None,'decision':'HOLD primary' if path==repo else ('HOLD dirty+active+pinned+ignored data' if path==active else 'CANDIDATE plan only; no deletion performed'),'recovery':('Uncommitted tracked/untracked/ignored data must be preserved; a commit-only backup is insufficient' if path==active else 'Committed history retained in fixture/main and feature/completed-task; eventual git worktree remove only after fresh ownership/inactivity/status check')})
finally:
    process.terminate();process.wait(timeout=5)
sim={'observation_kind':'synthetic Apple simulator service inventory; not actual simctl output','devices':{'com.apple.CoreSimulator.SimRuntime.iOS-18-0':[{'udid':'11111111-1111-4111-8111-111111111111','name':'Task-owned obsolete fixture','state':'Shutdown','isAvailable':False,'owner':'fixture-validator','active_tests':False,'persistent_developer_data':False,'estimated_fixture_bytes':4096},{'udid':'22222222-2222-4222-8222-222222222222','name':'Developer persistent phone','state':'Booted','isAvailable':True,'owner':'developer','active_tests':True,'persistent_developer_data':True,'estimated_fixture_bytes':8192}]},'runtimes':[{'identifier':'com.apple.CoreSimulator.SimRuntime.iOS-18-0','isAvailable':False,'owner':'unknown shared platform','delete_decision':'HOLD: shared ownership and no exact deletion authorization'}]}
(r/'simulators.fixture.json').write_text(json.dumps(sim,indent=2)+'\n')
(r/'inventory.json').write_text(json.dumps({'initial_base':base,'worktrees':entries,'owned_process_stopped_after_inventory':True,'simulator_observations':'fixture only','deletions':[],'reclaimed_bytes':0},indent=2)+'\n')
after=run(['git','worktree','list','--porcelain'],repo).stdout
assert inventory==after and all(Path(x['path']).exists() for x in entries)
(r/'evidence/worktrees-after-plan.porcelain').write_text(after);(r/'evidence/commands.json').write_text(json.dumps(logs,indent=2)+'\n')
(r/'PLAN.md').write_text('''# Cleanup inventory and hold report
Owner: lets-context, conditional owned-resource cleanup. Requested output is a plan; zero deletion commands executed, zero reclaimed bytes. Worktree Git/status/du observations are real temporary local measurements. Chat ownership/pinning is supplied synthetic fixture metadata. Simulator data is synthetic service input, never a physical device observation.

Actual worktree inventory is in evidence/worktrees.porcelain; branch/base/HEAD/merge/size/status/ignored data and decisions are in inventory.json. `active-dirty` is held: tracked change, untracked content, ignored env/cache, simulated active+pinned owner and a real process cwd observed by lsof. The owned probe process was stopped after inventory; no application or developer process was touched. `merged-unused` is clean, merged by actual fast-forward, owned and unused according to the supplied fixture metadata. It is a candidate for a later normal git worktree remove after a fresh inactivity/status/ownership check. No forced or recursive deletion fallback is proposed. Primary repository is held. Commit recovery for unused work is fixture/main plus feature/completed-task; ignored/uncommitted active contents require a separate intentional preservation plan.

Simulator plan: exact synthetic shutdown/unavailable task-owned device `11111111-1111-4111-8111-111111111111` may be a future exact-ID candidate after deletion authorization and data-loss review. Hold booted developer device `22222222-2222-4222-8222-222222222222` with active tests and persistent data. Hold the shared runtime because ownership is unknown; an unavailable runtime label does not prove deletion safety. No actual simctl inventory, delete, cache deletion, or runtime removal ran. Platform cleanup/reclaimed space is unavailable from these fixture observations. Before a real operation use supported device/runtime inventory and exact IDs, preserve required state, act only within the explicit device set, and re-inventory afterward. Do not infer actual bytes from fixture estimates.

For managed real worktrees prefer the host's recoverable archive facility; these are plain Git fixtures, so that facility is not applicable. The same actual Git worktrees remain in evidence/worktrees-after-plan.porcelain, and all directories are still present. Evidence lives outside candidate directories. This report creates no cleanup schedule and needs no private-history mining.
''')
print(json.dumps({'case':5,'actual_worktrees':len(entries),'dirty_active_held':True,'merged_candidate_held_for_plan':True,'deletions':0}))
