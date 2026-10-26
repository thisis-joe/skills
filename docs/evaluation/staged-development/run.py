"""Prepare frozen projects, execute native contexts and collect independent outputs.

Runs may require the host's approved local Codex access. No model override,
credential copying, global configuration change or external publishing is used.
"""
import argparse
import base64
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import os
from pathlib import Path
import random
import re
import shutil
import signal
import subprocess
import sys
import tarfile
import time
import uuid

from scenarios import CASES, command, prepare, verify

SOURCE = Path(__file__).resolve().parents[3]
EXPECTED_INTEGRITY = 'hD0WIpwClXm9ODj/2Q63bp3lOgEMcC/dy73MwuVAYFaHJvI7P0Cjsjgr7E7gi6sv9CJandGFoQyALza7SEGWWg=='


def save(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')


def hashes(root):
    return {p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(Path(root).rglob('*')) if p.is_file()}


def setup(root, archive):
    root=Path(root);root.mkdir(parents=True,exist_ok=False)
    archive=Path(archive)
    actual=base64.b64encode(hashlib.sha512(archive.read_bytes()).digest()).decode()
    if actual!=EXPECTED_INTEGRITY: raise ValueError('Published baseline integrity mismatch')
    snapshots=root/'snapshots';snapshots.mkdir()
    shutil.copytree(SOURCE/'skills',snapshots/'candidate')
    old=snapshots/'published';old.mkdir()
    with tarfile.open(archive) as stream:
        for member in stream.getmembers():
            parts=Path(member.name).parts
            if len(parts)<3 or parts[:2]!=('package','skills'): continue
            if '..' in parts or member.issym() or member.islnk(): raise ValueError('Unsafe archive member')
            dest=old.joinpath(*parts[2:])
            if member.isdir(): dest.mkdir(parents=True,exist_ok=True)
            elif member.isfile():
                dest.parent.mkdir(parents=True,exist_ok=True)
                with stream.extractfile(member) as src: dest.write_bytes(src.read())
    trials=[]
    rng=random.Random(20261023)
    for index,case in enumerate(CASES):
        arms=['candidate','published','bare'];rng.shuffle(arms)
        for arm in arms:
            ident=uuid.uuid4().hex[:12]; project=root/'projects'/ident
            initial=prepare(project,case)
            if arm!='bare': shutil.copytree(snapshots/arm,project/'.guide')
            evidence=root/'records'/ident;evidence.mkdir(parents=True)
            trials.append({'id':ident,'case':case,'arm':arm,'project':str(project),
                           'evidence':str(evidence),'initial_commit':initial,
                           'case_order':index})
    manifest={'schema':1,'source_head':command(SOURCE,['git','rev-parse','HEAD'])['stdout'].strip(),
              'published_git_head':'256c88073a1bfa858c6221197959d6ad1d7d8a5c',
              'published_integrity':'sha512-'+actual,
              'snapshots':{arm:hashes(snapshots/arm) for arm in ['candidate','published']},
              'cli':subprocess.check_output(['codex','--version'],text=True).strip(),
              'trials':trials,'protocol_sha256':hashlib.sha256((Path(__file__).parent/'protocol.md').read_bytes()).hexdigest()}
    save(root/'control.json',manifest)
    print(json.dumps({'prepared':str(root),'trials':len(trials),'snapshot':manifest['source_head']}),flush=True)


INITIAL = '''Work only in this project and preserve unrelated user files. Read BRIEF.md
and the existing code, then carry out the requested work. If .guide/ is present,
use those project-local procedures for selection and execution. Do not read
personal/global skill bodies or other projects. Use only shell/file operations
and local CLI/HTTP checks; do not spawn other agents, install packages, publish,
access external services, or change global configuration. Local Git identity is
already configured. Report the resulting state and checks truthfully. Stop for
decisions or selections that the applicable workflow requires.
'''

OWNER = '''For this change, adopt the concrete recommendations you have displayed
where they fit BRIEF.md. Automatically continue the basic technical steps only
for this specification, through implementation, review, verification and commits,
stopping before push. There is no Jira for this project: use descriptive feature
branching and preserve unrelated files. I decline any separately introduced
specialist examination for this change; keep all required behavior and ordinary
tests. If independent review cannot run here, I accept a clearly disclosed
same-agent formal review for this fixture; that does not waive actual runtime
checks. Missing browser acceptance must remain verification pending. Please
finish the authorized work, or identify the exact remaining material decision.
'''


def needs_followup(messages):
    """Triage final handoffs; reviewers still judge completion from the evidence."""
    final = messages[-1].lower() if messages else ''
    final = re.sub(r'\bno (?:formal )?review (?:is )?pending\b', '', final)
    if re.search(r'\b(?:formal )?review (?:is )?pending\b', final):
        return True
    return any(word in final for word in [
        'would you', 'shall i', 'which option', 'please choose', 'please select',
        'choose whether', '승인', '선택해', '진행할까요', '진행할지', '리뷰 대기', '검토 대기'])


def native(project, evidence, number, prompt, thread=None):
    args=['codex','exec','--ignore-user-config','--approve-for-me','--json','-C',str(project)]
    if thread: args+=['resume',thread]
    args+=['-']
    started=time.monotonic()
    process=subprocess.Popen(args,stdin=subprocess.PIPE,stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,text=True,start_new_session=True)
    timed_out=False
    try: stdout,stderr=process.communicate(prompt,timeout=540)
    except subprocess.TimeoutExpired:
        timed_out=True;os.killpg(process.pid,signal.SIGTERM)
        try: stdout,stderr=process.communicate(timeout=5)
        except subprocess.TimeoutExpired: os.killpg(process.pid,signal.SIGKILL);stdout,stderr=process.communicate()
    (evidence/('turn-%d.prompt.txt'%number)).write_text(prompt)
    (evidence/('turn-%d.events.jsonl'%number)).write_text(stdout)
    (evidence/('turn-%d.stderr.txt'%number)).write_text(stderr)
    events=[];messages=[];usage={}
    for line in stdout.splitlines():
        try: event=json.loads(line)
        except ValueError: continue
        events.append(event)
        if event.get('type')=='thread.started': thread=event.get('thread_id')
        item=event.get('item',{})
        if item.get('type')=='agent_message': messages.append(item.get('text',''))
        if event.get('type')=='turn.completed': usage=event.get('usage',{})
    result={'turn':number,'thread':thread,'exit':process.returncode,'timeout':timed_out,
            'seconds':round(time.monotonic()-started,3),'messages':messages,'usage':usage,
            'events':len(events),'invocation':args}
    save(evidence/('turn-%d.json'%number),result)
    return result


def run_trial(trial):
    project=Path(trial['project']);evidence=Path(trial['evidence'])
    if (evidence/'result.json').exists(): return json.loads((evidence/'result.json').read_text())
    turns=[];thread=None
    for number in range(1,4):
        turn=native(project,evidence,number,INITIAL if number==1 else OWNER,thread)
        turns.append(turn);thread=turn['thread']
        check=verify(project,trial['case']);save(evidence/('outcome-%d.json'%number),check)
        commits=command(project,['git','rev-list','--count',trial['initial_commit']+'..HEAD'])
        # A correctness pass alone does not resolve a manual handoff or formal review.
        waiting=needs_followup(turn['messages'])
        if turn['exit'] or turn['timeout']: break
        if check['functional_pass'] and commits['stdout'].strip()!='0' and not waiting: break
    result={**trial,'turns':turns,'outcome':check,'total_seconds':round(sum(t['seconds'] for t in turns),3),
            'guide_hashes_after':hashes(project/'.guide') if (project/'.guide').exists() else {},
            'implementation_artifacts':{p.relative_to(project).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
                for p in project.rglob('*') if p.is_file() and not any(part in {'.git','.guide','__pycache__'} for part in p.relative_to(project).parts)}}
    save(evidence/'result.json',result)
    print(json.dumps({'finished':trial['id'],'case':trial['case'],'arm':trial['arm'],
                      'outcome':check['functional_pass'],'turns':len(turns),'seconds':result['total_seconds']}),flush=True)
    return result


def execute(root, workers, limit):
    root=Path(root);control=json.loads((root/'control.json').read_text())
    trials=control['trials'][:limit] if limit else control['trials']
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures={executor.submit(run_trial,trial):trial for trial in trials}
        for future in as_completed(futures):
            trial=futures[future]
            try: future.result()
            except Exception as exc:
                save(Path(trial['evidence'])/'driver-error.json',{'error':repr(exc)})
                print(json.dumps({'error':trial['id'],'detail':repr(exc)}),flush=True)
    collect(root)


def collect(root):
    root=Path(root);control=json.loads((root/'control.json').read_text());rows=[]
    for trial in control['trials']:
        path=Path(trial['evidence'])/'result.json'
        if not path.exists(): rows.append({**trial,'status':'not completed'});continue
        result=json.loads(path.read_text())
        rows.append({'id':trial['id'],'case':trial['case'],'arm':trial['arm'],
                     'status':'executed','functional_pass':result['outcome']['functional_pass'],
                     'runtime':result['outcome']['required_runtime'],'turns':len(result['turns']),
                     'seconds':result['total_seconds'],'record':str(path)})
    save(root/'summary.json',{'trials':rows,'limits':'Six heterogeneous matched cases, synthetic owner, no human-time or speedup claim'})
    print(json.dumps({'summary':str(root/'summary.json'),'completed':sum(r['status']=='executed' for r in rows)}),flush=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['prepare','run','collect'])
    parser.add_argument('--root',type=Path,required=True)
    parser.add_argument('--archive',type=Path)
    parser.add_argument('--workers',type=int,default=3)
    parser.add_argument('--limit',type=int)
    args=parser.parse_args()
    if args.action=='prepare': setup(args.root,args.archive)
    elif args.action=='run': execute(args.root,args.workers,args.limit)
    else: collect(args.root)


if __name__=='__main__': main()
