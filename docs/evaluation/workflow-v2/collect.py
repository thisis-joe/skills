"""Collect per-case procedure outcomes and retain reproducible native evidence."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import statistics
import subprocess
import tarfile
import tempfile

from grade import AXES

ARMS=['current','published','bare']


def read(path):return json.loads(Path(path).read_text())
def save(path,value):Path(path).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')


def spread(values):
    values=[v for v in values if v is not None]
    return dict(n=len(values),median=statistics.median(values) if values else None,
                minimum=min(values) if values else None,maximum=max(values) if values else None)


def grades(root,mapping):
    combined={};errors=[]
    for path in sorted((root/'judgments').glob('*/result.json')):
        data=read(path)
        if not data.get('stable') or not data.get('evidence_unchanged') or not isinstance(data.get('grades'),dict):
            errors.append(dict(record=str(path),reason='Judgment unavailable/invalid'));continue
        expected=set(data['expected_ids'])
        for ident in expected-set(data['grades']):errors.append(dict(id=ident,reason='Missing grade'))
        for ident,verdict in data['grades'].items():
            if ident not in expected or ident not in mapping:
                errors.append(dict(id=ident,reason='Unknown/out-of-packet grade'));continue
            if ident in combined:raise ValueError('Duplicate grade: '+ident)
            if not isinstance(verdict,dict) or not isinstance(verdict.get('scores'),dict):
                errors.append(dict(id=ident,reason='Missing structured scores'));continue
            scored={};valid=set(verdict['scores'])==set(AXES)
            if not valid:
                errors.append(dict(id=ident,reason='Omitted/unknown score axis'));continue
            applicable={'selection'} if mapping[ident]['family']=='selection' else {'clarity','consistency','pickup'}
            for axis,items in AXES.items():
                value=verdict['scores'].get(axis)
                if value is None:scored[axis]=None;continue
                if not isinstance(value,dict) or set(value)!=set(items):valid=False;break
                if any(x is not None and (type(x) is not int or x not in [0,1,2]) for x in value.values()):valid=False;break
                if axis not in applicable and any(x is not None for x in value.values()):valid=False;break
                scored[axis]=value
            if valid:combined[ident]={**verdict,'scores':scored}
            else:errors.append(dict(id=ident,reason='Invalid subitems/score type'))
    return combined,errors


def collect(root,packets,output):
    root=Path(root);packets=Path(packets);output=Path(output);output.mkdir(parents=True,exist_ok=True)
    control=read(root/'control.json');mapping=read(root/'blind-mapping.json');judged,errors=grades(root,mapping)
    adjudications=read(root/'audit-adjudication.json') if (root/'audit-adjudication.json').exists() else {}
    control_reviews=read(root/'sensitivity-adjudication.json') if (root/'sensitivity-adjudication.json').exists() else {}
    registered={Path(name).parts[0] for name in control['snapshots']['current'] if Path(name).parts[0].startswith('coco-')}
    rows=[]
    for trial in control['trials']:
        data=read(Path(trial['record'])/'result.json');turns=data['turns'];audit=[]
        for turn in turns:
            for action in turn.get('commands',[]):
                cmd=action.get('command','')
                if re.search(r'\.codex/(?:skills|sessions)|\.claude/skills|CODEX_HOME|/snapshots/|/control\.json|/records/|recent_skills|read_thread|git push|gh pr|git config --global',cmd):
                    audit.append(dict(command=cmd,turn=turn['turn']))
        body_unchanged=(data['guide_after']==control['snapshots'][trial['arm']]) if trial['arm']!='bare' and data['stable'] else None
        audit_result=adjudications.get(trial['id'])
        eligible=bool(data['stable'] and audit_result and audit_result.get('status')=='eligible'
                      and body_unchanged is not False)
        value=dict(id=trial['id'],seed=trial['seed'],family=trial['family'],arm=trial['arm'],
                   eligible=eligible,audit_adjudication=audit_result,
                   stable=data['stable'],guide_unchanged=body_unchanged,audit_flags=audit,
                   seconds=sum(t['seconds'] for t in turns),turns=len(turns),
                   commands=sum(len(t.get('commands',[])) for t in turns),
                   per_worker=[dict(turn=t['turn'],seconds=t['seconds'],commands=len(t.get('commands',[])),
                                    usage=t['usage'],thread=t.get('thread')) for t in turns],
                   outcomes={phase:{k:v['passed'] for k,v in outcomes.items()}
                             for phase,outcomes in data['outcomes'].items()},
                   advice_files_unchanged=(data['states'].get('writer',{}).get('files')==data['states']['before']['files'])
                       if trial['family']=='selection' and data['stable'] else None,
                   judgment=judged.get(trial['id']))
        if trial['family']=='selection' and turns and turns[0].get('messages'):
            final=turns[0]['messages'][-1]
            value['registered_procedure_references']=sorted(name for name in registered
                if re.search(r'(?<![\w-])'+re.escape(name)+r'(?![\w-])',final))
            value['whitespace_word_count']=len(final.split())
        rows.append(value)
    sensitivity={}
    for ident,meta in mapping.items():
        if not meta.get('control'):continue
        verdict=judged.get(ident);status='unavailable'
        if verdict:
            scores=verdict['scores']
            if meta['family']=='handoff':
                values=[(scores.get('consistency') or {}).get('truth'),(scores.get('pickup') or {}).get('completion')]
            else:values=[(scores.get('selection') or {}).get(k) for k in ['appropriate','boundary']]
            if all(v is not None for v in values):
                if not all(v<2 for v in values):status='failed'
                elif control_reviews.get(ident,{}).get('status') in ['passed','failed']:
                    status=control_reviews[ident]['status']
        sensitivity[ident]=dict(mapping=meta,judgment=verdict,status=status,
                               reason_review=control_reviews.get(ident))
    grading_validated=len(sensitivity)==2 and all(v['status']=='passed' for v in sensitivity.values())
    groups=[]
    for family in ['handoff','selection']:
        for arm in ARMS:
            all_rows=[r for r in rows if r['family']==family and r['arm']==arm]
            selected=[r for r in all_rows if r['eligible']]
            applicable=['selection'] if family=='selection' else ['clarity','consistency','pickup']
            stats={}
            for axis in applicable:
                values=[r['judgment']['scores'].get(axis) for r in selected if r['judgment']] if grading_validated else []
                stats[axis]=dict(graded=sum(v is not None and all(v.get(k) is not None for k in AXES[axis]) for v in values),
                    fully_clear_correct=sum(v is not None and all(v.get(k)==2 for k in AXES[axis]) for v in values),
                    subitems={item:spread(v.get(item) for v in values if v is not None) for item in AXES[axis]})
            groups.append(dict(family=family,arm=arm,n=len(all_rows),eligible=len(selected),excluded_or_unavailable=len(all_rows)-len(selected),axes=stats,
                 seconds=spread(r['seconds'] for r in selected),commands=spread(r['commands'] for r in selected),
                 independent_summary_pass=sum(r['outcomes'].get('receiver',{}).get('summary_outcome') is True for r in selected),
                 writer_import_pass=sum(all(r['outcomes'].get('writer',{}).get(k) is True for k in ['import_outcome','import_boundaries']) for r in selected) if family=='handoff' else None,
                 receiver_import_pass=sum(all(r['outcomes'].get('receiver',{}).get(k) is True for k in ['import_outcome','import_boundaries']) for r in selected) if family=='handoff' else None))
    archive=output/'native-evidence.tar.gz'
    with tempfile.TemporaryDirectory(prefix='workflow-git-evidence-') as temporary:
        history=Path(temporary)
        for t in control['trials']:
            subprocess.run(['git','bundle','create',str(history/(t['id']+'.bundle')),'--all'],cwd=t['project'],check=True,capture_output=True)
        with tarfile.open(archive,'w:gz') as stream:
            for name in ['control.json','execution.log','snapshots','records','judgments','blind-mapping.json','judge-packets.json','audit-adjudication.json','sensitivity-adjudication.json']:
                if (root/name).exists():stream.add(root/name,arcname=name)
            source=Path(__file__).resolve().parents[3]
            frozen={**{('docs/evaluation/workflow-v2/'+k):v for k,v in control['protocol_and_harness'].items()},
                    **control['dependencies']}
            for name,digest in frozen.items():
                blob=subprocess.check_output(['git','show',control['driver_head']+':'+name],cwd=source)
                if hashlib.sha256(blob).hexdigest()!=digest:raise ValueError('Frozen source identity mismatch: '+name)
                info=tarfile.TarInfo('frozen-source/'+name);info.size=len(blob);stream.addfile(info,io.BytesIO(blob))
            for name in ['grade.py','collect.py']:
                stream.add(Path(__file__).parent/name,arcname='analysis-source/'+name)
            for t in control['trials']:
                project=Path(t['project'])
                for path in sorted(project.rglob('*')):
                    rel=path.relative_to(project)
                    if path.is_file() and not any(p in {'.git','.guide','__pycache__'} for p in rel.parts):
                        stream.add(path,arcname='projects/'+t['id']+'/'+rel.as_posix())
                stream.add(history/(t['id']+'.bundle'),arcname='history/'+t['id']+'.bundle')
            for path in sorted(packets.rglob('*')):
                rel=path.relative_to(packets)
                if path.is_file() and not any(p in {'.git','__pycache__'} for p in rel.parts):stream.add(path,arcname='blind-packets/'+rel.as_posix())
    result=dict(schema=1,candidate=control['candidate'],driver_head=control['driver_head'],
                published_integrity=control['published_integrity'],cli=control['cli'],groups=groups,rows=rows,
                sensitivity=sensitivity,grading_validated=grading_validated,grade_errors=errors,
                archive_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),
                limits=['Five matched samples per arm/family; selection cases heterogeneous.',
                        'Native successors and advice properties are proxies; humans were not recruited.',
                        'No overall cross-axis score or causal speed claim. Audit flags require manual adjudication.',
                        'Model identity unpinned when absent from native events; global catalog metadata remains discoverable.'])
    save(output/'results.json',result)
    print(json.dumps(dict(rows=len(rows),graded=len(judged),errors=errors,archive_bytes=archive.stat().st_size,
                          archive_sha256=result['archive_sha256'])))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,required=True)
    p.add_argument('--packets',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();collect(a.root,a.packets,a.output)
