"""Three-arm native workflow/pickup experiment. No active skill changes."""
import argparse
import base64
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import uuid

from cases import AUTH, PROFILES, RECEIVER, SELECT, call, git, observe, prepare, writer_prompt
from engine import native

SOURCE=Path(__file__).resolve().parents[3]
CANDIDATE='622975e'
INTEGRITY='hD0WIpwClXm9ODj/2Q63bp3lOgEMcC/dy73MwuVAYFaHJvI7P0Cjsjgr7E7gi6sv9CJandGFoQyALza7SEGWWg=='
DEPENDENCIES=['docs/evaluation/collaboration-value/engine.py',
              'docs/evaluation/collaboration-value/lifecycle.py',
              'docs/specs/workflow-value-v2.md']
HARNESSES=['cases.py','run.py','protocol.md']


def harness_hashes():
    return {name:hashlib.sha256((Path(__file__).parent/name).read_bytes()).hexdigest() for name in HARNESSES}


def save(path,value):
    Path(path).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')


def hashes(root,excluded=()):
    root=Path(root)
    return {p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob('*')) if p.is_file()
            and not any(x in {'.git','__pycache__',*excluded} for x in p.relative_to(root).parts)}


def setup(root,archive):
    root=Path(root);root.mkdir(parents=True,exist_ok=False)
    snapshots=root/'snapshots';snapshots.mkdir()
    current=snapshots/'current';current.mkdir()
    for path in git(SOURCE,'ls-tree','-r','--name-only',CANDIDATE,'skills').splitlines():
        dest=current/Path(path).relative_to('skills');dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_bytes(subprocess.check_output(['git','show',CANDIDATE+':'+path],cwd=SOURCE))
    if base64.b64encode(hashlib.sha512(Path(archive).read_bytes()).digest()).decode()!=INTEGRITY:
        raise ValueError('Published baseline integrity mismatch')
    published=snapshots/'published';published.mkdir()
    with tarfile.open(archive) as stream:
        for member in stream.getmembers():
            parts=Path(member.name).parts
            if parts[:2]!=('package','skills') or len(parts)<3:continue
            if '..' in parts or member.issym() or member.islnk():raise ValueError('Unsafe archive')
            dest=published.joinpath(*parts[2:])
            if member.isdir():dest.mkdir(parents=True,exist_ok=True)
            elif member.isfile():
                dest.parent.mkdir(parents=True,exist_ok=True)
                with stream.extractfile(member) as source:dest.write_bytes(source.read())
    trials=[]
    for seed in range(5):
        arms=['current','published','bare'];arms=arms[seed%3:]+arms[:seed%3]
        for family in ['handoff','selection']:
            for arm in arms:
                ident=uuid.uuid4().hex[:12];project=root/'projects'/ident
                initial=prepare(project,seed,family)
                if arm!='bare':shutil.copytree(snapshots/arm,project/'.guide')
                record=root/'records'/ident;record.mkdir(parents=True)
                trials.append(dict(id=ident,seed=seed,family=family,arm=arm,project=str(project),
                                   record=str(record),initial_commit=initial))
    save(root/'control.json',dict(schema=1,candidate=git(SOURCE,'rev-parse',CANDIDATE),
         driver_head=git(SOURCE,'rev-parse','HEAD'),profiles=PROFILES,trials=trials,
         snapshots={arm:hashes(snapshots/arm) for arm in ['current','published']},
         dependencies={name:hashlib.sha256((SOURCE/name).read_bytes()).hexdigest() for name in DEPENDENCIES},
         published_integrity='sha512-'+INTEGRITY,
         protocol_and_harness=harness_hashes(),
         cli=call(SOURCE,['codex','--version'])['stdout'].strip()))
    print(json.dumps(dict(prepared=str(root),projects=len(trials))),flush=True)


def stable(turn):
    return turn.get('exit')==0 and not turn.get('timeout') and not turn.get('error') and turn.get('thread_started')


def state(project):
    return dict(head=git(project,'rev-parse','HEAD'),branch=git(project,'branch','--show-current'),
                status=git(project,'status','--porcelain'),log=git(project,'log','--format=%H %s'),
                files=hashes(project,('.guide',)))


def execute_trial(trial):
    project=Path(trial['project']);record=Path(trial['record'])
    if (record/'result.json').exists():return
    # Never restart a partial trial over its already-open native evidence.
    if (record/'turn-1.json').exists():raise RuntimeError('Partial trial requires explicit audit, not automatic replay')
    before=state(project)
    first=native(project,record,1,SELECT if trial['family']=='selection' else writer_prompt(trial['seed']),timeout=420)
    turns=[first];outcomes={};states={'before':before}
    if stable(first):
        states['writer']=state(project)
        if trial['family']=='handoff':
            shutil.copytree(project,record/'writer-project',
                            ignore=shutil.ignore_patterns('.guide','__pycache__'))
            outcomes['writer']=observe(project,trial['seed']);save(record/'writer-outcome.json',outcomes['writer'])
            if states['writer']['files']!=state(project)['files']:
                raise RuntimeError('Observer changed actor artifacts; successor not started')
            # A genuinely fresh native thread gets only the original surviving files.
            second=native(project,record,2,RECEIVER,timeout=420);turns.append(second)
            if stable(second):
                states['receiver']=state(project);outcomes['receiver']=observe(project,trial['seed'])
                save(record/'receiver-outcome.json',outcomes['receiver'])
    result=dict(trial=trial,turns=turns,states=states,outcomes=outcomes,
                stable=all(stable(t) for t in turns),
                guide_after=hashes(project/'.guide') if all(stable(t) for t in turns) and (project/'.guide').exists() else {})
    save(record/'result.json',result)
    print(json.dumps(dict(finished=trial['id'],family=trial['family'],seed=trial['seed'],arm=trial['arm'],
                         stable=result['stable'],turns=len(turns),seconds=round(sum(t['seconds'] for t in turns),3))),flush=True)


def execute(root,workers):
    control=json.loads((Path(root)/'control.json').read_text())
    if not 1<=workers<=3:raise ValueError('Frozen concurrency cap is 1–3 workers')
    for name,digest in control['dependencies'].items():
        if hashlib.sha256((SOURCE/name).read_bytes()).hexdigest()!=digest:raise ValueError('Frozen dependency changed: '+name)
    if harness_hashes()!=control['protocol_and_harness']:raise ValueError('Frozen protocol/harness changed')
    def run(trial):
        try:execute_trial(trial)
        except Exception as exc:
            save(Path(trial['record'])/'driver-error.json',dict(error=repr(exc)))
            print(json.dumps(dict(error=trial['id'],detail=repr(exc))),flush=True)
    with ThreadPoolExecutor(max_workers=workers) as pool:list(pool.map(run,control['trials']))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['prepare','run'])
    p.add_argument('--root',type=Path,required=True);p.add_argument('--archive',type=Path)
    p.add_argument('--workers',type=int,choices=[1,2,3],default=3);a=p.parse_args()
    if a.action=='prepare':setup(a.root,a.archive)
    else:execute(a.root,a.workers)
