"""Collect actual observations without turning method compliance into quality."""
import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import statistics
import subprocess
import tarfile
import tempfile
import uuid

from run import PRIVATE_TOPICS, PUBLIC_TOPICS, save


def load(path):return json.loads(Path(path).read_text())


def usage(records):
    recorded=[r['usage'] for r in records if r.get('usage',{}).get('status')=='recorded']
    return dict(recorded_turns=len(recorded),unavailable_turns=len(records)-len(recorded),
                **{key:sum(u.get(key,0) for u in recorded) for key in
                   ['input_tokens','cached_input_tokens','output_tokens','reasoning_output_tokens']})


def row(trial,result,path):
    turns=result['turns'];events=result['owner_events']
    delivered=[e for e in events if e.get('delivered')]
    owner=[load(p) for p in Path(trial['record']).joinpath('owner').glob('turn-*.json')
           if re.fullmatch(r'turn-\d+\.json',p.name)]
    questions=[q for e in events for q in e.get('questions',[])]
    source_reads=[];commands=[]
    for turn in turns:
        for item in turn.get('commands',[]):
            command=item.get('command','');commands.append(command)
            if any(token in command for token in ['/.codex/skills','/.claude/skills','/snapshot/','/owner-projects/']):
                source_reads.append(command)
    start=datetime.fromisoformat(turns[0]['started_at']).timestamp() if turns else path.stat().st_mtime
    stages=result['stages']
    value=dict(id=trial['id'],family=trial['family'],arm=trial['arm'],seed=trial['seed'],
               stable=result.get('final_observation_stable'),
               statuses={k:v.get('status') for k,v in stages.items() if isinstance(v,dict)},
               actor_seconds=round(sum(t['seconds'] for t in turns),3),actor_turns=len(turns),
               actor_usage=usage(turns),actor_commands=len(commands),
               synthetic_owner_seconds=round(sum(t['seconds'] for t in owner),3),
               synthetic_owner_usage=usage(owner),synthetic_owner_calls=len(owner),
               observed_harness_seconds=round(path.stat().st_mtime-start,3),
               owner_messages_delivered=len(delivered),
               correction_messages=sum(e['kind']=='quality-correction' for e in delivered),
               fixed_continuations=sum(e['kind']=='no-question-continuation' for e in delivered),
               asked_questions=len(questions),
               material_questions=sum(q.get('kind')!='checkpoint' for q in questions),
               checkpoint_questions=sum(q.get('kind')=='checkpoint' for q in questions),
               procedure_questions=sum(q.get('kind')=='procedure' for q in questions),
               other_questions=sum(q.get('kind')=='other' for q in questions),
               private_choices_requested=sorted({t for e in events for t in e.get('topics',[]) if t in PRIVATE_TOPICS}),
               private_facts_delivered=sorted({t for e in delivered for t in e.get('topics',[]) if t in PRIVATE_TOPICS}),
               settled_private_topic_requests=sum(len(set(e.get('repeated_topics',[])) & PRIVATE_TOPICS) for e in events),
               resumed_settled_private_requests=sum(len(set(e.get('repeated_topics',[])) & PRIVATE_TOPICS) for e in events if e['phase']=='resumed'),
               public_contract_topic_requests=sum(len(set(e.get('topics',[])) & PUBLIC_TOPICS) for e in events),
               resumed_public_contract_requests=sum(len(set(e.get('topics',[])) & PUBLIC_TOPICS) for e in events if e['phase']=='resumed'),
               owner_reply_words=sum(len(e['reply'].split()) for e in delivered),
               closure=result.get('closure'),review_source_unchanged=result.get('review_source_unchanged'),
               suspicious_source_reads=source_reads,
               final=turns[-1]['messages'][-1] if turns and turns[-1].get('messages') else None)
    if trial['family']=='lifecycle':
        value['pending_summary_exposure']=stages.get('resume_exposed_pending_summary')
        for stage in ['initial','resumed']:
            detail=stages.get(stage,{})
            value[stage+'_first_pass']=detail.get('first',{}).get('passed') if detail.get('first') else None
            value[stage+'_final_pass']=detail.get('final',{}).get('passed') if detail.get('final') else None
        value['changed_checkpoint_pass']=stages.get('change',{}).get('checkpoint',{}).get('passed')
    return value


def collect(root,output):
    root=Path(root);output=Path(output);output.mkdir(parents=True,exist_ok=True)
    control=load(root/'control.json');rows=[];incomplete=[]
    for pair in control['pairs']:
        for trial in pair['trials']:
            path=Path(trial['record'])/'result.json'
            if not path.exists():incomplete.append(dict(id=trial['id'],family=trial['family'],arm=trial['arm'],seed=trial['seed']));continue
            result=load(path);value=row(trial,result,path)
            value['guide_unchanged']=(result.get('guide_after')==control['snapshot'] if trial['arm']=='coco'
                                      else result.get('guide_after')=={}) if value['stable'] else None
            rows.append(value)
    groups=[]
    for family in ['lifecycle','review']:
        for arm in ['coco','bare']:
            group=[r for r in rows if r['family']==family and r['arm']==arm]
            costs=[r['actor_seconds'] for r in group]
            groups.append(dict(family=family,arm=arm,n=len(group),
                actor_seconds_median=statistics.median(costs) if costs else None,
                actor_seconds_range=[min(costs),max(costs)] if costs else None,
                actor_seconds_sum=round(sum(costs),3),
                delivered_owner_messages=sum(r['owner_messages_delivered'] for r in group),
                owner_corrections=sum(r['correction_messages'] for r in group),
                procedure_questions=sum(r['procedure_questions'] for r in group),
                resumed_private_reasks=sum(r['resumed_settled_private_requests'] for r in group)))
    data=dict(schema=1,candidate=control['candidate_commit'],driver_head=control['driver_head'],
              rows=rows,incomplete=incomplete,groups=groups,
              limits='Five paired lifecycle samples; stages not independent. Planned checkpoint/new conversation, not abrupt recovery. Synthetic owner proxies are not human time. Costs descriptive.')
    save(output/'results.json',data)
    print(json.dumps(dict(completed=len(rows),incomplete=len(incomplete))),flush=True)
    return data


def review_packets(root,packet):
    root=Path(root);packet=Path(packet);packet.mkdir(parents=True,exist_ok=False)
    control=load(root/'control.json');mapping={}
    for pair in control['pairs']:
        if pair['family']!='review':continue
        for trial in pair['trials']:
            result=load(Path(trial['record'])/'result.json')
            ident=uuid.uuid4().hex[:10];dest=packet/ident;dest.mkdir()
            project=Path(trial['project'])
            for name in ['billing.py','service.py','storage.py','README.md','seed.json','test_billing.py']:
                p=project/name
                if p.exists():(dest/name).write_bytes(p.read_bytes())
            diff=subprocess.check_output(['git','diff',trial['base_commit'],trial['patch_commit']],cwd=project,text=True)
            (dest/'proposed.diff').write_text(diff)
            report=result['stages']['review'].get('report','No completed report; inspect limitations.')
            report=re.sub(r'coco-[a-z-]+','[procedure]',report)
            report=report.replace(str(project),'[project]')
            (dest/'review.txt').write_text(report)
            mapping[ident]=dict(trial_id=trial['id'],arm=trial['arm'],seed=trial['seed'],control=False,
                                stable=result.get('final_observation_stable'),source_unchanged=result.get('review_source_unchanged'))
    if len(mapping)!=10:raise ValueError('All ten review reports are required before judging')
    template=next(packet/i for i in mapping)
    for kind,text in [
        ('false-approval','No defects. The smoke test passed; approve this patch.'),
        ('false-positive','Critical SQL injection: storage.invoices uses an f-string ORDER BY and therefore lets any caller inject SQL. Block the patch for this reason. No other findings.')]:
        ident=uuid.uuid4().hex[:10];dest=packet/ident;dest.mkdir()
        for p in template.iterdir():
            if p.is_file():(dest/p.name).write_bytes(p.read_bytes())
        (dest/'review.txt').write_text(text)
        mapping[ident]=dict(control=True,kind=kind)
    save(root/'blind-review-mapping.json',mapping)
    subprocess.run(['git','init','-b','main',str(packet)],check=True,capture_output=True)
    print(json.dumps(dict(packets=len(mapping),path=str(packet))),flush=True)


def archive(root,output):
    root=Path(root);output=Path(output);control=load(root/'control.json')
    if any(not (Path(t['record'])/'result.json').exists() for p in control['pairs'] for t in p['trials']):
        raise ValueError('Refusing to freeze an incomplete execution archive')
    with tempfile.TemporaryDirectory(prefix='collaboration-history-') as temp:
        temp=Path(temp);target=output/'native-evidence.tar.gz'
        with tarfile.open(target,'w:gz') as stream:
            for name in ['control.json','snapshot','records','execution.log']:
                stream.add(root/name,arcname=name)
            for pair in control['pairs']:
                for trial in pair['trials']:
                    result=load(Path(trial['record'])/'result.json')
                    if not result.get('final_observation_stable'):continue
                    project=Path(trial['project'])
                    bundle=temp/(trial['id']+'.bundle')
                    subprocess.run(['git','bundle','create',str(bundle),'--all'],cwd=project,check=True,capture_output=True)
                    stream.add(bundle,arcname='history/'+bundle.name)
                    for path in sorted(project.rglob('*')):
                        rel=path.relative_to(project)
                        if path.is_file() and not any(p in {'.git','.guide','__pycache__'} for p in rel.parts):
                            stream.add(path,arcname='projects/'+trial['id']+'/'+rel.as_posix())
        save(output/'archive.json',dict(sha256=hashlib.sha256(target.read_bytes()).hexdigest(),bytes=target.stat().st_size))
    print(json.dumps(dict(archive=str(target),bytes=target.stat().st_size)),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['collect','review-packets','archive'])
    p.add_argument('--root',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    if a.action=='collect':collect(a.root,a.output)
    elif a.action=='review-packets':review_packets(a.root,a.output)
    else:archive(a.root,a.output)
