from evidence import *
import hashlib,re,shutil
before=json.loads((ROOT/'skill-hashes-before.json').read_text())
after={f:hashlib.sha256((Path('/Users/Joseph/workspaces/skills')/f).read_bytes()).hexdigest() for f in before}
(ROOT/'skill-hashes-after.json').write_text(json.dumps(after,indent=2)+'\n')
changes=[f for f in before if before[f]!=after[f]]
(ROOT/'skill-hash-comparison.json').write_text(json.dumps({'unchanged':not changes,'changed_files':changes},indent=2)+'\n')
results={}
for case,m in MANIFEST.items():
    here=ROOT/case
    status=run(case,'git','status','--porcelain=v1','-uall').stdout
    branch=run(case,'git','branch','--show-current').stdout.strip()
    head=run(case,'git','rev-parse','HEAD').stdout.strip()
    local=run(case,'git','show-ref').stdout
    remote=run(case,'git','ls-remote','--heads',m['remote']).stdout
    (here/'after-refs.txt').write_text(local+'\nREMOTE\n'+remote)
    shutil.copyfile(here/'jira/tasks.json',here/'after-task.json')
    run(case,'git','bundle','create',str(here/'local.bundle'),'--all')
    run(case,'git','--git-dir',m['remote'],'bundle','create',str(here/'remote.bundle'),'--all')
    run(case,'git','bundle','verify',str(here/'local.bundle'))
    run(case,'git','bundle','verify',str(here/'remote.bundle'))
    cmds=[json.loads(s) for s in (here/'commands.jsonl').read_text().splitlines()]
    adapter=[json.loads(s) for s in (here/'jira/adapter.jsonl').read_text().splitlines()]
    original=json.loads((here/'before-task.json').read_text());final=json.loads((here/'after-task.json').read_text())
    pins=json.loads((here/'pinned.json').read_text());decisions=[json.loads(s) for s in (here/'decisions.jsonl').read_text().splitlines()]
    push=[c for c in cmds if c['argv'][:2]==['git','push']]
    writes=[c for c in adapter if c['operation']=='update']
    tests=[c for c in cmds if c['argv']==['python3','-m','unittest','discover','-s','tests','-v']]
    fields={key:[f for f in old if old[f]!=final[key][f]] for key,old in original.items()}
    remote_refs={line.split('\t')[1]:line.split('\t')[0] for line in remote.strip().splitlines()}
    question=[d['question'] for d in decisions if d.get('question')]
    expected='published' if case in ('scope_drift','adequate_summary') else 'stopped_before_push'
    assertions={'clean_worktree':not status,'one_integration_round':True,'required_tests_passed':len(tests)==1 and tests[0]['exit']==0,'only_summary_description_and_adapter_version_changed':all(set(v)<={'summary','description','version'} for v in fields.values()),'no_force_push':all(not any(a in ('--force','--force-with-lease','--mirror','--all') for a in c['argv']) for c in push),'explicit_single_refspec':all(len(c['argv'])==4 and c['argv'][3].startswith(head+':refs/heads/') for c in push),'all_remote_destinations_local':all(Path(c['argv'][2]).resolve().is_relative_to(ROOT.resolve()) for c in push)}
    if case=='scope_drift':
        assertions.update({'published_final_oid':remote_refs['refs/heads/'+m['candidate_branch']]==head,'old_remote_preserved':remote_refs['refs/heads/'+m['old_branch']]==pins['old_remote_task'],'original_description_preserved':final[m['task_key']]['description'].startswith(original[m['task_key']]['description']),'summary_matches_branch':branch.split('-',1)[1]==final[m['task_key']]['summary'],'one_successful_jira_write':len(writes)==1 and writes[0]['exit']==0,'no_question':not question,'peer_ancestor':run(case,'git','merge-base','--is-ancestor',m['peer_commit'],head).returncode==0})
    elif case=='adequate_summary':
        assertions.update({'published_final_oid':remote_refs['refs/heads/'+m['old_branch']]==head,'branch_unchanged':branch==m['old_branch'],'jira_unchanged':final==original,'no_jira_write':not writes,'no_question':not question})
    else:
        assertions.update({'no_push_attempt':not push,'jira_unchanged':final==original,'old_remote_unchanged':remote_refs['refs/heads/'+m['old_branch']]==pins['old_remote_task']})
        if case=='jira_write_failure':assertions.update({'rename_partial_state_preserved':branch==m['candidate_branch'],'one_denied_write':len(writes)==1 and writes[0]['exit']==3,'new_remote_absent':'refs/heads/'+m['candidate_branch'] not in remote_refs})
        else:assertions.update({'branch_not_renamed':branch==m['old_branch'],'no_jira_write':not writes,'missing_decision_recorded':bool(question)})
        if case=='unrelated_collision':assertions['unrelated_candidate_untouched']=remote_refs['refs/heads/'+m['candidate_branch']]==m['collision_commit'];assertions['unrelated_local_untouched']=run(case,'git','rev-parse',m['candidate_branch']).stdout.strip()==m['collision_commit']
    result={'outcome':expected,'behavior_assessment':'passed' if all(assertions.values()) else 'failed','assertions':assertions,'local_branch':branch,'head':head,'pinned':pins,'remote_refs':remote_refs,'jira_field_changes':fields,'jira_operations':{'reads':sum(c['operation']=='read' for c in adapter),'searches':sum(c['operation']=='search-number' for c in adapter),'updates_attempted':len(writes),'updates_succeeded':sum(c['exit']==0 for c in writes)},'push_attempts':len(push),'test_count':int(re.search(r'Ran (\d+) tests',tests[0]['stderr']).group(1)),'questions':question,'evidence':{'commands':str(here/'commands.jsonl'),'decisions':str(here/'decisions.jsonl'),'adapter':str(here/'jira/adapter.jsonl'),'before_task':str(here/'before-task.json'),'after_task':str(here/'after-task.json'),'before_refs':str(here/'before-refs.txt'),'after_refs':str(here/'after-refs.txt'),'local_bundle':str(here/'local.bundle'),'remote_bundle':str(here/'remote.bundle')}}
    (here/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');results[case]=result
all_pass=all(r['behavior_assessment']=='passed' for r in results.values())
summary={'type':'bounded independent forward application of coco-push','fixed_version':not changes,'changed_skill_files':changes,'assessment':'passed_in_bounded_local_cases' if all_pass and not changes else 'mixed_or_version_changed','real_git':True,'jira':'LOCAL MOCK file-backed adapter only','external_writes':False,'fixture_count':len(results),'results':{k:{f:v[f] for f in ('outcome','behavior_assessment','local_branch','head','jira_operations','push_attempts','test_count','questions')} for k,v in results.items()},'limitations':['No real Jira connector, permissions, ADF-rich text, or authentication was tested.','No text conflict, concurrent write race, dual push URL, or retry-limit stress case was included.','This is one model-driven application pass with five designed fixtures, not a statistical reliability claim.','Original setup was revised before applying the skill so CSV implementation belongs to the feature diff and Python caches are ignored; discarded setup commands are retained separately.']}
(ROOT/'result.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2))
