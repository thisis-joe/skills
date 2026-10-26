"""Execute matched collaboration projects; rubric/owner state stay outside them."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import time
import uuid

from engine import native, classify_question
from lifecycle import AUTH, CHANGE, RESUME, PROFILES, call, facts, git, prepare, verify
import review_case

SOURCE = Path(__file__).resolve().parents[3]
CANDIDATE = '622975e'
PRIVATE_TOPICS = {'identity','collision','invalid','report'}
PUBLIC_TOPICS = {'import_contract','summary_contract','remaining_scope'}
TOPICS = PRIVATE_TOPICS | PUBLIC_TOPICS
CONTINUE = '''The initial authorization still applies. Continue the requested current
slice and actual checks using established decisions. If a product decision is
still missing, ask that exact question. No new business defaults are granted.
'''
REVIEW_AUTH = '''Work only in this project. Read the product contract and actual Git diff.
If .guide exists use those local procedures. Do not load personal/global skill
bodies, other projects, source archives or experiment-control files. This request
authorizes read-only review, not implementation or commits. Separate specialist
examinations are declined; ordinary correctness/security inspection remains.
Use local shell/Git/Python stdlib and actual CLI checks. No nested agents, installs,
external services, publishing or global changes. Ask a genuinely needed decision
in the final response; otherwise return the review findings and limitations.
'''


def save(path, data):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')


def failed_execution(turn):
    return (turn is None or turn.get('timeout') or turn.get('error')
            or turn.get('exit') != 0 or turn.get('resume_safe') is False
            or not turn.get('thread_started'))


def hashes(project, exclude=()):
    return {p.relative_to(project).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(Path(project).rglob('*')) if p.is_file()
            and not any(part in {'.git','__pycache__',*exclude} for part in p.relative_to(project).parts)}


def setup(root):
    root=Path(root);root.mkdir(parents=True,exist_ok=False)
    snapshot=root/'snapshot';snapshot.mkdir()
    tracked=git(SOURCE,'ls-tree','-r','--name-only',CANDIDATE,'skills').splitlines()
    for path in tracked:
        p=snapshot/Path(path).relative_to('skills');p.parent.mkdir(parents=True,exist_ok=True)
        p.write_bytes(subprocess.check_output(['git','show',CANDIDATE+':'+path],cwd=SOURCE))
    pairs=[]
    for seed in range(5):
        for family in ['lifecycle','review']:
            trials=[]
            order=['coco','bare'] if seed%2==0 else ['bare','coco']
            for arm in order:
                ident=uuid.uuid4().hex[:12];project=root/'projects'/ident
                if family=='lifecycle': meta=dict(initial_commit=prepare(project,seed))
                else: meta=review_case.prepare(project,seed)
                if arm=='coco':shutil.copytree(snapshot,project/'.guide')
                record=root/'records'/ident;record.mkdir(parents=True)
                owner=root/'owner-projects'/ident;owner.mkdir(parents=True)
                git(owner,'init','-b','main')
                trials.append(dict(id=ident,seed=seed,family=family,arm=arm,
                                   project=str(project),record=str(record),owner=str(owner),**meta))
            pairs.append(dict(seed=seed,family=family,trials=trials))
    save(root/'control.json',dict(schema=1,candidate_commit=git(SOURCE,'rev-parse',CANDIDATE),
         driver_head=git(SOURCE,'rev-parse','HEAD'),snapshot=hashes(snapshot),
         harness_hashes=hashes(Path(__file__).parent),profiles=PROFILES,pairs=pairs,
         cli=call(SOURCE,['codex','--version'])['stdout'].strip()))
    print(json.dumps(dict(prepared=str(root),pairs=len(pairs),projects=20)),flush=True)


def snapshot(trial, label):
    project=Path(trial['project'])
    data=dict(head=git(project,'rev-parse','HEAD'),branch=git(project,'branch','--show-current'),
              status=git(project,'status','--porcelain'),
              log=git(project,'log','--format=%H %s'),files=hashes(project,('.guide',)))
    save(Path(trial['record'])/(label+'-snapshot.json'),data);return data


def committed_product_delta(project,base):
    head=git(project,'rev-parse','HEAD')
    if head==base:return []
    paths=git(project,'diff','--name-only',base,head).splitlines()
    product=[p for p in paths if p.endswith('.py') and not Path(p).name.startswith('test')]
    if not product:return []
    if call(project,['git','diff','--quiet','HEAD','--','*.py'])['exit']:return []
    untracked=git(project,'ls-files','--others','--exclude-standard').splitlines()
    if any(p.endswith('.py') and not Path(p).name.startswith('test') for p in untracked):return []
    return product


class Session:
    def __init__(self,trial):
        self.trial=trial;self.project=Path(trial['project']);self.record=Path(trial['record'])
        self.turns=[];self.owner_events=[];self.revealed=[];self.thread=None;self.owner_number=0
        self.profile=PROFILES[trial['seed']]

    def actor(self,prompt,phase,fresh=False,interrupt=None):
        if (self.record.parents[1]/'STOP').exists():return None
        elapsed=sum(t['seconds'] for t in self.turns)
        remaining=1800-elapsed if self.trial['family']=='lifecycle' else 1800-elapsed
        if remaining<=0:return None
        pending=None
        for event in reversed(self.owner_events):
            if not event.get('delivered') and event['reply']==prompt:
                pending=event;event['attempted']=True;break
        result=native(self.project,self.record,len(self.turns)+1,prompt,
                      thread=None if fresh else self.thread,interrupt=interrupt,
                      timeout=min(420,remaining))
        result['phase']=phase;self.turns.append(result);self.thread=result.get('thread')
        reached=bool(result.get('process_started') and result.get('thread_started'))
        if pending is not None:
            pending['delivered']=reached
            if reached:self.revealed.extend(t for t in pending.get('new_topics',[]) if t not in self.revealed)
            save(self.record/'owner-events.json',self.owner_events)
        if phase=='change' and prompt==CHANGE and reached:
            self.revealed.extend(t for t in PUBLIC_TOPICS if t not in self.revealed)
        save(self.record/'progress.json',dict(turns=self.turns,owner_events=self.owner_events))
        return result

    def public_facts(self,phase):
        if phase=='initial':
            return dict(import_contract='Use catalog.py --db PATH import CSV_PATH and list. CSV fields are sku,name,price_cents; preserve existing stored rows and the list interface. Prices are nonnegative integer cents; SKU/name must be nonempty.',
                        summary_contract='Summary is a JSON array of objects with supplier legacy, count and total_cents; no items means []. Whether to include zero-price entries is the separate business choice.',
                        remaining_scope='First complete and commit the runnable import/list slice, then stop for my trial before implementing summary.')
        return dict(import_contract=CHANGE.split('Complete and commit')[0].strip(),
                    summary_contract='Summary returns one {supplier,count,total_cents} object per nonempty supplier group, sorted by supplier, respecting our previously agreed zero-price rule; no groups means [].',
                    remaining_scope='Finish the remaining purchasing summary, preserve and verify the supplier/batch import behavior, and commit. Check actual files/Git rather than repeating completed work.')

    def private_facts(self,phase):
        known=facts(self.profile)
        if phase!='initial':
            within={'first':'keep the first row for repeated keys',
                    'last':'use the last row for repeated keys',
                    'error':'reject repeated keys, even identical duplicate rows'}[self.profile['collision']]
            known['collision']=('Within one file '+within+'. A later ordinary batch updates an existing entry for the same supplier/SKU; this replaces the earlier stored-row collision rule.')
        return known

    def answer(self,turn,phase):
        final=turn['messages'][-1] if turn.get('messages') else ''
        classification=None
        for attempt in range(2):
            self.owner_number+=1
            classification=classify_question(Path(self.trial['owner']),self.record/'owner',
                self.owner_number,final,self.revealed)
            if not classification.get('parse_error'):break
            owner_run=classification.get('owner_record',{})
            if owner_run.get('timeout') or owner_run.get('resume_safe') is False or owner_run.get('exit') is None:
                break  # Do not launch a retry beside an unconfirmed predecessor.
        if classification.get('parse_error'):
            save(self.record/'owner-failure.json',classification)
            return None
        questions=classification.get('questions',[])
        topics=sorted({topic for q in questions for topic in q.get('topics',[]) if topic in TOPICS}) if self.trial['family']=='lifecycle' else []
        new=[t for t in topics if t not in self.revealed]
        repeated=[t for t in topics if t in self.revealed]
        known=self.private_facts(phase) | self.public_facts(phase)
        reply='\n'.join(known[topic] for topic in topics)
        if any(q.get('kind')=='procedure' for q in questions):
            reply+='\nThe initial technical authorization already applies. Use the described local workflow and descriptive branch without Jira. Separate specialist examinations remain declined; keep ordinary controls and checks.'
        if questions and not reply.strip():
            reply=('Review against README.md and the supplied actual Git base/diff. The requirements are already stated there. Report concrete defects and limitations; do not modify code.' if self.trial['family']=='review' else
                   'There is no additional business preference beyond the request and decisions already supplied. Choose reversible implementation details and continue; ask a concrete unresolved business question if needed.')
        if not questions:reply=CONTINUE
        event=dict(phase=phase,kind='answer' if questions else 'no-question-continuation',
                   questions=questions,topics=topics,new_topics=new,repeated_topics=repeated,
                   reply=reply,owner_record=classification,delivered=False)
        self.owner_events.append(event)
        save(self.record/'owner-events.json',self.owner_events)
        return reply,event

    def correction(self,outcome,phase):
        failed=[c['id'] for c in outcome['checks'] if not c['passed']]
        topics=set()
        for label in failed:
            if 'identity' in label:topics.add('identity')
            if 'collision' in label:topics.add('collision')
            if 'malformed' in label or 'skipped' in label:topics.add('invalid')
            if 'summary' in label:topics.update(['report','summary_contract'])
        if phase!='initial' and any('summary' not in x and x not in
             {'unrelated_file_preserved','unrelated_file_uncommitted'} for x in failed):
            topics.add('import_contract')
        selected=sorted(topics)
        known=self.private_facts(phase) | self.public_facts(phase)
        reply=('My actual trial did not match the agreed result. Failing observations: '+', '.join(failed)+'.\n'+
               '\n'.join(known[t] for t in selected)+
               '\nPlease repair the current slice, preserve unrelated data and rerun the affected real CLI checks. Existing agreed requirements remain in force.' )
        event=dict(phase=phase,kind='quality-correction',failed=failed,topics=selected,
                   new_topics=[t for t in selected if t not in self.revealed],
                   repeated_topics=[],reply=reply,delivered=False)
        self.owner_events.append(event)
        save(self.record/'owner-events.json',self.owner_events)
        return reply

    def initial(self):
        prompt=AUTH;answers=0;no_question=0;corrected=False;first=None
        for _ in range(6):
            turn=self.actor(prompt,'initial')
            if failed_execution(turn):return dict(status='execution-failed',first=first)
            ready=verify(self.project,self.profile,'initial',milestone=True)
            ready['committed_product']=bool(committed_product_delta(self.project,self.trial['initial_commit']))
            save(self.record/('initial-milestone-%d.json'%len(self.turns)),ready)
            answer=self.answer(turn,'initial')
            if answer is None:return dict(status='owner-failed',first=first)
            next_prompt,event=answer
            material=[q for q in event['questions'] if q.get('kind')!='checkpoint']
            if material:
                if answers>=4:return dict(status='answer-budget',first=first,milestone=ready)
                prompt=next_prompt;answers+=1;continue
            if ready['passed'] and ready['committed_product']:
                outcome=verify(self.project,self.profile,'initial')
                save(self.record/('initial-outcome-%d.json'%len(self.turns)),outcome)
                if first is None:first=outcome
                if outcome['passed']:return dict(status='ready',first=first,final=outcome)
                if corrected:return dict(status='quality-failed',first=first,final=outcome)
                prompt=self.correction(outcome,'initial');corrected=True;continue
            if answers>=4:return dict(status='answer-budget',first=first,milestone=ready)
            prompt=next_prompt;answers+=1
            if event['kind']=='no-question-continuation':
                no_question+=1
                if no_question>1:return dict(status='premature-stop',first=first,milestone=ready)
        return dict(status='turn-budget',first=first)

    def change(self):
        start=git(self.project,'rev-parse','HEAD');prompt=CHANGE;answers=0;no_question=0
        captured={};last_head=None
        def observe():
            nonlocal last_head
            head=git(self.project,'rev-parse','HEAD')
            if head==start or head==last_head:return False
            product=committed_product_delta(self.project,start)
            if not product:return False
            ready=verify(self.project,self.profile,'changed',milestone=True)
            if ready['passed']:
                captured.update(head=head,milestone=ready,product_paths=product);return True
            # Retry new commits, not transient polling of identical committed code.
            last_head=head;return False
        for _ in range(5):
            # Managed-host preflight could not establish tool-child cancellation.
            # Stop at the shared requested checkpoint; never race a fresh actor
            # against an unconfirmed live predecessor.
            turn=self.actor(prompt,'change')
            if turn is None:return dict(status='actor-budget')
            if failed_execution(turn):return dict(status='execution-failed')
            if observe():
                state=snapshot(self.trial,'interruption');outcome=verify(self.project,self.profile,'changed')
                save(self.record/'change-checkpoint-outcome.json',outcome)
                return dict(status='checkpoint-stop',capture=captured,snapshot=state,checkpoint=outcome)
            if answers>=4:return dict(status='answer-budget')
            answer=self.answer(turn,'change')
            if answer is None:return dict(status='owner-failed')
            prompt,event=answer;answers+=1
            if event['kind']=='no-question-continuation':
                no_question+=1
                if no_question>1:return dict(status='premature-stop')
        return dict(status='turn-budget')

    def resumed(self):
        self.thread=None;prompt=AUTH+'\n'+RESUME;answers=0;no_question=0;corrected=False;first=None
        for index in range(6):
            turn=self.actor(prompt,'resumed',fresh=index==0)
            if failed_execution(turn):return dict(status='execution-failed',first=first)
            outcome=verify(self.project,self.profile,'resumed')
            save(self.record/('resumed-outcome-%d.json'%len(self.turns)),outcome)
            # Ask genuine questions before treating a not-yet-implemented command as a wrong result.
            answer=self.answer(turn,'resumed')
            if answer is None:return dict(status='owner-failed',first=first)
            next_prompt,event=answer
            material=[q for q in event['questions'] if q.get('kind')!='checkpoint']
            if material:
                if answers>=4:return dict(status='answer-budget',first=first,final=outcome)
                prompt=next_prompt;answers+=1;continue
            if outcome['passed']:
                if first is None:first=outcome
                return dict(status='ready',first=first,final=outcome)
            if first is None:first=outcome
            if not corrected:
                prompt=self.correction(outcome,'resumed');corrected=True;continue
            return dict(status='quality-failed',first=first,final=outcome)
        return dict(status='turn-budget',first=first)

    def review(self):
        prompt=REVIEW_AUTH+'\n'+self.trial['prompt']
        turn=self.actor(prompt,'review')
        if failed_execution(turn):return dict(status='execution-failed')
        answer=self.answer(turn,'review')
        # The read-only contract/base are complete. An optional offer to fix code
        # never causes an unrequested second review or an artificial owner reply.
        return dict(status='reported',question_observation_failed=answer is None,
                    report=turn['messages'][-1] if turn.get('messages') else '')

    def run(self):
        start_snapshot=snapshot(self.trial,'start')
        if self.trial['family']=='review':
            stages=dict(review=self.review())
        else:
            stages=dict(initial=self.initial())
            if stages['initial']['status']=='ready':
                snapshot(self.trial,'first-slice');stages['change']=self.change()
                if stages['change']['status']=='checkpoint-stop':
                    before_resume=verify(self.project,self.profile,'resumed')
                    save(self.record/'before-resume-outcome.json',before_resume)
                    summary=next((c for c in before_resume['checks'] if c['id']=='summary_uses_agreed_rule'),None)
                    stages['resume_exposed_pending_summary']=None if summary is None else not summary['passed']
                    stages['resumed']=self.resumed()
        stable=not any(t.get('timeout') or t.get('error') or t.get('exit') != 0
                       or t.get('resume_safe') is False for t in self.turns)
        state=(snapshot(self.trial,'final') if stable else
               dict(head=None,branch=None,status=None,files={},unstable=True,
                    reason='Owned-session quiescence unavailable; project quarantined, no immutable outcome claim.'))
        review_unchanged=(state['head']==start_snapshot['head'] and all(
            state['files'].get(path)==digest for path,digest in start_snapshot['files'].items())) if stable and self.trial['family']=='review' else None
        statuses=(state['status'] or '').splitlines()
        closure=dict(owned_work_committed=all(line=='?? personal-notes.txt' for line in statuses) if stable else None,
                     feature_branch=state['branch'] not in ('main','master','') if stable else None)
        result=dict(trial=self.trial,stages=stages,turns=self.turns,owner_events=self.owner_events,
                    facts_revealed=self.revealed,final_state=state,
                    controller_stop=(self.record.parents[1]/'STOP').exists(),
                    final_observation_stable=stable,
                    closure=closure,review_source_unchanged=review_unchanged,
                    guide_after=(hashes(self.project/'.guide') if (self.project/'.guide').exists() else {}) if stable else None)
        save(self.record/'result.json',result)
        print(json.dumps(dict(finished=self.trial['id'],family=self.trial['family'],arm=self.trial['arm'],
              seed=self.trial['seed'],statuses={k:v.get('status') for k,v in stages.items() if isinstance(v,dict)},
              seconds=round(sum(t['seconds'] for t in self.turns),3))),flush=True)
        return result


def execute(root,workers):
    root=Path(root);control=json.loads((root/'control.json').read_text())
    def pair_work(pair):
        for trial in pair['trials']:
            if (root/'STOP').exists():return
            if (Path(trial['record'])/'result.json').exists():continue
            try:Session(trial).run()
            except Exception as exc:
                save(Path(trial['record'])/'driver-error.json',dict(error=repr(exc)))
                print(json.dumps(dict(error=trial['id'],detail=repr(exc))),flush=True)
    with ThreadPoolExecutor(max_workers=workers) as pool:
        list(pool.map(pair_work,control['pairs']))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['prepare','run'])
    p.add_argument('--root',type=Path,required=True);p.add_argument('--workers',type=int,default=2)
    a=p.parse_args()
    if a.action=='prepare':setup(a.root)
    else:execute(a.root,a.workers)
