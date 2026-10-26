"""Frozen single-factor native comparisons; active skill paths are never written."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import difflib
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import uuid

from fixtures import DOMAINS, WORKFLOW, observe_discovery, prepare, prompt, workflow
from variants import CHANGED, apply
from engine import native

SOURCE=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
FAMILIES={'R5':'discovery','R2':'handoff','R7':'selection'}
FROZEN=['protocol.md','run.py','fixtures.py','variants.py']
DEPENDENCIES=['docs/evaluation/collaboration-value/engine.py','docs/evaluation/collaboration-value/lifecycle.py','docs/evaluation/workflow-v2/cases.py','docs/specs/procedure-refinement.md']


def save(path,value):
    Path(path).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')


def hashes(root,exclude=()):
    root=Path(root)
    return {p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob('*')) if p.is_file()
            and not any(x in {'.git','__pycache__',*exclude} for x in p.relative_to(root).parts)}


def frozen():
    return {str(p.relative_to(SOURCE)):hashlib.sha256(p.read_bytes()).hexdigest()
            for p in [*(HERE/n for n in FROZEN),*(SOURCE/n for n in DEPENDENCIES)]}


def state(project):
    return dict(head=workflow.git(project,'rev-parse','HEAD'),branch=workflow.git(project,'branch','--show-current'),
                status=workflow.git(project,'status','--porcelain'),files=hashes(project,('.guide',)))


def stable(turn):
    return turn.get('exit')==0 and not turn.get('timeout') and not turn.get('error') and turn.get('thread_started')


def setup(root):
    root=Path(root);root.mkdir(parents=True,exist_ok=False)
    snapshots=root/'snapshots';snapshots.mkdir();current=snapshots/'current';current.mkdir()
    for name in workflow.git(SOURCE,'ls-tree','-r','--name-only','622975e','skills').splitlines():
        dest=current/Path(name).relative_to('skills');dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_bytes(subprocess.check_output(['git','show','622975e:'+name],cwd=SOURCE))
    manifests={'current':hashes(current)};diffs={}
    for variant in FAMILIES:
        candidate=snapshots/variant;shutil.copytree(current,candidate);apply(candidate,variant)
        manifests[variant]=hashes(candidate)
        changed=sorted(n for n in manifests['current'] if manifests['current'][n]!=manifests[variant][n])
        if changed!=sorted(CHANGED[variant]):raise ValueError('Proposal touched unexpected files')
        diffs[variant]='\n'.join(''.join(difflib.unified_diff((current/n).read_text().splitlines(True),(candidate/n).read_text().splitlines(True),fromfile=n,tofile=n)) for n in changed)
    trials=[]
    for variant,family in FAMILIES.items():
        for seed in range(5):
            arms=['current',variant] if seed%2==0 else [variant,'current']
            for arm in arms:
                ident=uuid.uuid4().hex[:12];project=root/'projects'/ident;prepare(project,seed,family)
                shutil.copytree(snapshots/arm,project/'.guide')
                record=root/'records'/ident;record.mkdir(parents=True)
                trials.append(dict(id=ident,seed=seed,family=family,factor=variant,arm=arm,project=str(project),record=str(record)))
    owner=root/'owner';owner.mkdir();workflow.git(owner,'init','-b','main')
    save(root/'control.json',dict(candidate=workflow.git(SOURCE,'rev-parse','622975e'),driver_head=workflow.git(SOURCE,'rev-parse','HEAD'),
         hashes=frozen(),manifests=manifests,diffs=diffs,trials=trials,domains=DOMAINS,
         cli=workflow.call(SOURCE,['codex','--version'])['stdout'].strip()))
    print(json.dumps(dict(prepared=str(root),projects=len(trials))),flush=True)


def observe(project,seed):
    with tempfile.TemporaryDirectory(prefix='discovery-observer-') as directory:
        copy=Path(directory)/'project';shutil.copytree(project,copy,ignore=shutil.ignore_patterns('.guide','__pycache__'))
        return observe_discovery(copy,seed)


def classify(root,trial,turn,number):
    domain=DOMAINS[trial['seed']];directory=Path(trial['record'])/'owner'
    final=turn['messages'][-1] if turn.get('messages') else ''
    instruction='''Classify the actual final owner-facing request below. Use no tools or files.
Return exactly JSON {"topics": [topic IDs], "question_spans": [verbatim spans]}.
Select only business topics actually requested, including a proposed default
explicitly put to the owner for approval. A request for all remaining business
choices can cover all topics. A completion report, rhetorical heading or offer
to implement something is not a policy question. You do not know answer values.
Keep exact request spans supporting the topics; no topic without a supporting
span. For no policy question both arrays are empty.\n'''+json.dumps(dict(topic_meanings=domain['topics'],message=final),ensure_ascii=False)
    attempts=[]
    for retry in range(2):
        result=native(root/'owner',directory,number*2+retry+1,instruction,timeout=90);attempts.append(result)
        try:
            value=json.loads(result['messages'][-1])
            if not stable(result) or result.get('commands') or result.get('tool_items'):raise ValueError('Owner classifier did not remain tool-free')
            if set(value)!={'topics','question_spans'}:raise ValueError('Owner schema')
            if not isinstance(value['topics'],list) or len(set(value['topics']))!=len(value['topics']) or any(x not in domain['topics'] for x in value['topics']):raise ValueError('Owner topic')
            if not isinstance(value['question_spans'],list) or any(not isinstance(x,str) or not x.strip() or x not in final for x in value['question_spans']):raise ValueError('Owner span')
            if bool(value['topics'])!=bool(value['question_spans']):raise ValueError('Unbacked owner topic')
        except (ValueError,KeyError,IndexError,TypeError) as exc:
            save(directory/('classification-'+str(number)+'-'+str(retry)+'.json'),dict(error=repr(exc),attempt=result))
            continue
        return dict(**value,attempts=attempts,valid=True)
    return dict(topics=[],question_spans=[],attempts=attempts,valid=False)


def discovery(root,trial,result):
    project=Path(trial['project']);record=Path(trial['record']);seed=trial['seed']
    delivered=set();events=[];questions=0;corrected=False;continuation=False;thread=None;pending=None
    text=prompt(seed,'discovery')
    for index in range(1,6):
        before=state(project);turn=native(project,record,index,text,thread=thread,timeout=420);result['turns'].append(turn)
        if pending is not None and turn.get('process_started') and turn.get('thread_started'):
            previous,topics=pending;previous['delivered']=True;delivered.update(topics)
        pending=None
        if not stable(turn):break
        thread=turn['thread'];after=state(project)
        shutil.copytree(project,record/('checkpoint-'+str(index)),ignore=shutil.ignore_patterns('.guide','__pycache__'))
        outcomes=observe(project,seed)
        if after['files']!=state(project)['files']:raise RuntimeError('Observer changed actor tree')
        result['states'][str(index)]=after;result['outcomes'][str(index)]=outcomes
        classification=classify(root,trial,turn,index)
        event=dict(turn=index,known_before=sorted(delivered),classification=classification,
                   observed_implementation=outcomes['implemented'],passed=outcomes['passed'],delivered=False)
        events.append(event)
        if not classification['valid']:result['owner_error']=True;break
        requested=classification['topics']
        if requested and questions<3 and index<5:
            text='\n'.join(DOMAINS[seed]['facts'][topic] for topic in requested)
            questions+=1;event.update(reply=text,kind='policy',new_topics=sorted(set(requested)-delivered))
            pending=(event,requested)
            continue
        if outcomes['implemented'] and not outcomes['policy_passed'] and not corrected and index<5:
            text='The real CLI outcome does not match our business agreement. Here are the required choices:\n'+'\n'.join(DOMAINS[seed]['facts'].values())+'\nPlease repair the behavior, check it and commit. Preserve the original expectation and explain the actual correction and its reason/effect in your final report.'
            event.update(reply=text,kind='correction',new_topics=sorted(set(DOMAINS[seed]['topics'])-delivered))
            pending=(event,list(DOMAINS[seed]['topics']));corrected=True;continue
        if not outcomes['implemented'] and not requested and not continuation and index<5:
            text='Continue the requested work under the existing technical grant; ask any unresolved business decision instead of choosing it for me.'
            event.update(reply=text,kind='continuation',new_topics=[]);pending=(event,[]);continuation=True;continue
        break
    result['owner_events']=events


def one(root,trial):
    project=Path(trial['project']);record=Path(trial['record'])
    if (record/'result.json').exists():return
    if (record/'turn-1.json').exists():raise RuntimeError('Partial trial cannot be silently restarted')
    result=dict(trial=trial,turns=[],states={'before':state(project)},outcomes={})
    if trial['family']=='discovery':discovery(root,trial,result)
    else:
        turn=native(project,record,1,prompt(trial['seed'],trial['family']),timeout=420);result['turns'].append(turn)
        if stable(turn):
            result['states']['writer']=state(project)
            if trial['family']=='handoff':
                shutil.copytree(project,record/'writer-project',ignore=shutil.ignore_patterns('.guide','__pycache__'))
                result['outcomes']['writer']=workflow.observe(project,trial['seed'])
                if result['states']['writer']['files']!=state(project)['files']:raise RuntimeError('Observer changed handoff source')
                receiver=native(project,record,2,workflow.RECEIVER,timeout=420);result['turns'].append(receiver)
                if stable(receiver):
                    result['states']['receiver']=state(project);result['outcomes']['receiver']=workflow.observe(project,trial['seed'])
    result['stable']=all(stable(t) for t in result['turns']) and not result.get('owner_error')
    result['guide_after']=hashes(project/'.guide') if result['stable'] else None
    if result['stable']:
        result['states']['final']=state(project)
        shutil.copytree(project,record/'final-project',ignore=shutil.ignore_patterns('.guide','__pycache__'))
    save(record/'result.json',result)
    print(json.dumps(dict(finished=trial['id'],factor=trial['factor'],arm=trial['arm'],seed=trial['seed'],stable=result['stable'],turns=len(result['turns']))),flush=True)


def run(root,factor,workers):
    root=Path(root);control=json.loads((root/'control.json').read_text())
    if frozen()!=control['hashes']:raise ValueError('Frozen protocol or dependency changed')
    if factor=='R2' and not (root/'R5-observation.json').exists():raise ValueError('Record R5 outcome before R2')
    def guarded(trial):
        try:one(root,trial)
        except Exception as exc:
            save(Path(trial['record'])/'driver-error.json',dict(error=repr(exc)))
            print(json.dumps(dict(error=trial['id'],detail=repr(exc))),flush=True)
    with ThreadPoolExecutor(max_workers=workers) as pool:list(pool.map(guarded,[t for t in control['trials'] if t['factor']==factor]))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('action',choices=['prepare','run']);parser.add_argument('--root',type=Path,required=True)
    parser.add_argument('--factor',choices=list(FAMILIES));parser.add_argument('--workers',type=int,choices=[1,2,3],default=3);args=parser.parse_args()
    if args.action=='prepare':setup(args.root)
    else:run(args.root,args.factor,args.workers)
