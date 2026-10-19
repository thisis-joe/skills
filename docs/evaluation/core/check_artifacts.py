from pathlib import Path
import hashlib, json, subprocess
r=Path(__file__).parent
results={}
for name in ['start','clarify','research','design','spec','plan','build','debug','verify','review','context','triage']:
    results[name]={'input_exists':(r/name/'input.md').is_file(),'output_exists':(r/name/'output.md').is_file()}
    assert all(results[name].values())
rows=[json.loads(p.read_text()) for p in (r/'plan/tasks/invoice-export').glob('*.json')]
byid={row['id']:row for row in rows}; visiting=set(); done=set()
def walk(id):
    if id in visiting: raise AssertionError('cycle '+id)
    if id in done: return
    visiting.add(id)
    for blocker in byid[id]['blockers']:
        assert blocker in byid
        walk(blocker)
    visiting.remove(id); done.add(id)
for id in byid: walk(id)
results['plan_dag']={'tasks':len(rows),'acyclic':True,'frontier':sorted(row['id'] for row in rows if not row['blockers'])}
def scope(file): return json.loads(json.loads((r/'review/evidence'/file).read_text())['stdout'])
before=scope('before.json'); after=scope('after.json'); current=scope('current-bundle-after.json')
assert before==after==current
assert {f['path']:f['layers'] for f in before['files']}=={'discount.py':['untracked'],'tests/test_discount.py':['worktree']}
results['review_scope']={'before_equals_after_and_current_collector':True,'snapshot':before['snapshot'],'has_changes':before['has_changes']}
state=json.loads((r/'build/task-state.json').read_text());commit=state['T1']['commit']
assert subprocess.check_output(['git','show','--format=','--name-only',commit],cwd=r/'build/repo',text=True).split()==['greet.py','tests/test_greet.py']
assert hashlib.sha256((r/'build/repo/NOTES.md').read_bytes()).hexdigest()==(r/'build/user-dirty-sha256.txt').read_text().strip()
results['build_ownership']={'commit':commit,'task_paths_only':True,'user_dirty_file_unchanged':True}
old=json.loads((r/'context/task-state.before.json').read_text());new=json.loads((r/'context/task-state.json').read_text())
assert old['T1']['status']=='open' and new['T1']['status']=='done'
assert subprocess.check_output(['git','rev-list','--count','HEAD'],cwd=r/'context/repo',text=True).strip()=='2'
results['context_recovery']={'stale_state_preserved':True,'done_commit':new['T1']['commit'],'no_resume_product_commit':True}
initial=json.loads((r/'bundle-snapshot.json').read_text()); final=json.loads((r/'bundle-snapshot.final.json').read_text())
changed=[p for p in initial if initial[p]!=final[p]]
results['bundle_integrity']={'global_snapshot_stayed_fixed':not changed,'changed_paths':changed,'note':'Read-only target changed during this run; evaluator wrote only /tmp artifacts. Frozen final copy retained.'}
for name,h in final.items():
    copy=r/'frozen-current-bundle'/Path(name).relative_to('/Users/Joseph/workspaces/skills')
    assert hashlib.sha256(copy.read_bytes()).hexdigest()==h
results['frozen_current_bundle_copy_matches_manifest']=True
(r/'artifact-integrity.json').write_text(json.dumps(results,indent=2))
print(json.dumps(results,indent=2))
