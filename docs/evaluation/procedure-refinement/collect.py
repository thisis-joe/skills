"""Collect auditable per-case observations; claims require controls and audits."""
import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import re
import statistics
import tarfile

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('refinement_judgments',HERE/'grade.py')
judging=importlib.util.module_from_spec(spec);spec.loader.exec_module(judging)
save=judging.save


def read(path):return json.loads(Path(path).read_text())


def spread(values):
    values=[v for v in values if v is not None]
    return dict(n=len(values),median=statistics.median(values),minimum=min(values),maximum=max(values)) if values else dict(n=0)


def total_seconds(turns):
    values=[turn.get('seconds') for turn in turns]
    return sum(values) if values and all(type(v) in (int,float) and math.isfinite(v) and v>=0 for v in values) else None


def ratio(numerator,denominator):
    return numerator/denominator if numerator is not None and denominator is not None and denominator>0 else None


def median(values):
    values=[v for v in values if v is not None]
    return statistics.median(values) if values else None


def full(grade,axis):
    value=(grade or {}).get('scores',{}).get(axis)
    return isinstance(value,dict) and bool(value) and all(v==2 for v in value.values())


def final_outcome(result):
    if result['trial']['family']=='discovery':
        return result['outcomes'].get(str(len(result['turns'])),dict(passed=None,reason='No safe final observation'))
    receiver=result['outcomes'].get('receiver',{})
    if result['trial']['family']=='handoff':
        values=[receiver.get(k,{}).get('passed') for k in ('import_outcome','import_boundaries','summary_outcome')]
        return dict(passed=None,reason='Required receiver evidence unavailable') if any(v is None for v in values) else dict(passed=all(values))
    return {}


def episode_total(rows):
    values=[row.get('confirmed_policy_revision_episodes') for row in rows]
    return sum(values) if all(type(value) is int and value>=0 for value in values) else None


def grounded_control_rejection(item,grade,checked):
    scores=grade.get('scores',{})
    if item['family']=='handoff':
        observed=(scores.get('consistency') or {}).get('truth')==0 and (scores.get('pickup') or {}).get('completion')==0
    else:
        selection=scores.get('selection') or {}
        # The registered gate is grounded rejection, not a particular boundary
        # score. A judge may credit read-only restraint while rejecting readiness.
        detected=set(checked.get('detected_defects',[]))
        observed=any(selection.get(key)==0 for key in ('appropriate','purpose','boundary')) and {
            'false_browser_readiness','unauthorized_publication_advice'}<=detected
    return observed and checked.get('passed') is True and bool(checked.get('evidence'))


def collect(root,output):
    root=Path(root);output=Path(output);output.mkdir(parents=True,exist_ok=True)
    judging.check_analysis(root)
    control=read(root/'control.json');mapping=read(root/'blind-mapping.json')
    verdicts=[read(root/'judgments'/str(i)/'result.json') for i in range(5)]
    grades,errors=judging.validate_grades(verdicts)
    schema_errors=list(errors)
    source=read(root/'source-audit.json');owners=read(root/'owner-audit.json')
    reconciliation=read(root/'control-adjudication.json')
    controls={}
    for ident,item in mapping.items():
        if not item.get('control'):continue
        grade=grades.get(ident,{})
        checked=reconciliation.get(ident,{})
        controls[ident]=dict(mapping=item,grade=grade,grounded_rejection=grounded_control_rejection(item,grade,checked))
    controls_valid=len(controls)==2 and all(c['grounded_rejection'] for c in controls.values())
    if not controls_valid:errors.append('Negative control reconciliation missing/failed')
    registered={Path(n).parts[0] for n in control['manifests']['current'] if Path(n).parts[0].startswith('coco-')}
    rows=[];raw={}
    markers={'R5':'Before product implementation, show a short frontier',
             'R2':'For continuation of the same feature, inspect',
             'R7':'When a user explicitly already saw the introductory map'}
    for trial in control['trials']:
        ident=trial['id'];result=read(Path(trial['record'])/'result.json');raw[ident]=result
        turns=result['turns'];grade=grades.get(ident);audit=source.get(ident,{})
        if audit.get('status')!='eligible' or not audit.get('evidence'):errors.append('Unresolved/ineligible source audit '+ident)
        if result['stable'] and result['guide_after']!=control['manifests'][trial['arm']]:errors.append('Guide changed '+ident)
        if trial['family']=='discovery' and (owners.get(ident,{}).get('passed') is not True or not owners.get(ident,{}).get('evidence')):errors.append('Unresolved owner audit '+ident)
        commands=[c for turn in turns for c in turn.get('commands',[])]
        last=turns[-1]['messages'][-1] if turns and turns[-1].get('messages') else ''
        result_final=final_outcome(result)
        row={k:trial[k] for k in ('id','seed','family','factor','arm')}
        row.update(stable=result['stable'],source_eligibility=audit,judgment=grade,
                   measurement_eligible=audit.get('status')=='eligible' and (trial['family']!='discovery' or owners.get(ident,{}).get('passed') is True),
                   seconds=total_seconds(turns),turns=len(turns),commands=len(commands),
                   usage=[t.get('usage') for t in turns],outcome=result_final,
                   proposal_text_seen=trial['arm']!='current' and any(markers[trial['factor']] in c.get('aggregated_output','') for c in commands))
        if trial['family']=='selection':
            row.update(reply_words=len(last.split()) if last else None,registered_names=sorted(n for n in registered if re.search(r'(?<![\w-])'+re.escape(n)+r'(?![\w-])',last)),
                       advice_unchanged=result['stable'] and result['states']['before']==result['states']['final'])
        if trial['family']=='discovery':
            events=result.get('owner_events',[])
            row['correction_messages']=sum(e.get('delivered') and e.get('kind')=='correction' for e in events)
            row['policy_messages']=sum(e.get('delivered') and e.get('kind')=='policy' for e in events)
            row['first_ready_turn']=next((e['turn'] for e in events if e['observed_implementation'] and not e['classification']['topics']),None)
            row['first_ready_passed']=result['outcomes'].get(str(row['first_ready_turn']),{}).get('passed') if row['first_ready_turn'] else None
            row['confirmed_policy_revision_episodes']=owners.get(ident,{}).get('confirmed_policy_revision_episodes')
            if type(row['confirmed_policy_revision_episodes']) is not int or row['confirmed_policy_revision_episodes']<0:errors.append('Unresolved episode coding '+ident)
            if grade and row['confirmed_policy_revision_episodes']!=grade.get('confirmed_policy_revision_episodes') and not owners.get(ident,{}).get('episode_reconciliation'):
                errors.append('Unreconciled episode judgment '+ident)
        if trial['family']=='handoff':
            row['writer_import_only']=all(result.get('outcomes',{}).get('writer',{}).get(k,{}).get('passed',False) for k in ('import_outcome','import_boundaries')) and not result.get('outcomes',{}).get('writer',{}).get('summary_outcome',{}).get('passed',False)
        rows.append(row)
    if set(grades)!=set(mapping):errors.append('Grade coverage differs from blind mapping')
    groups=[]
    for factor in ('R5','R2','R7'):
        scheduled=[r for r in rows if r['factor']==factor]
        complete=lambda r: r['stable'] and (r.get('advice_unchanged') if factor=='R7' else r['outcome'].get('passed') is True) and (r.get('writer_import_only') if factor=='R2' else True)
        joint=[seed for seed in range(5) if all(complete(r) for r in scheduled if r['seed']==seed)]
        for arm in ('current',factor):
            all_attempts=[r for r in scheduled if r['arm']==arm]
            selected=[r for r in all_attempts if r['measurement_eligible']]
            groups.append(dict(factor=factor,arm=arm,n=len(all_attempts),eligible=len(selected),excluded_or_unresolved=len(all_attempts)-len(selected),
                stable=sum(r['stable'] for r in all_attempts),
                functional_passed=sum(r['outcome'].get('passed') is True for r in selected),
                functional_unavailable=sum(r['outcome'].get('passed') is None for r in selected) if factor!='R7' else 0,
                axes={axis:dict(full=sum(full(r['judgment'],axis) for r in selected),
                       available=sum(isinstance((r['judgment'] or {}).get('scores',{}).get(axis),dict) and any(v is not None for v in r['judgment']['scores'][axis].values()) for r in selected)) for axis in judging.AXES},
                seconds=spread([r['seconds'] for r in all_attempts]),eligible_seconds=spread([r['seconds'] for r in selected]),
                jointly_completed=dict(seeds=joint,seconds=spread([r['seconds'] for r in all_attempts if r['seed'] in joint])),
                commands=spread([r['commands'] for r in selected]),
                reply_words=spread([r.get('reply_words') for r in selected]),
                correction_messages=sum(r.get('correction_messages',0) for r in selected),
                confirmed_policy_revision_episodes=episode_total(selected) if factor=='R5' else None,
                proposal_text_seen=sum(r['proposal_text_seen'] for r in selected)))
    gates={};pairs=[]
    for factor in ('R5','R2','R7'):
        current=[r for r in rows if r['factor']==factor and r['arm']=='current']
        proposed=[r for r in rows if r['factor']==factor and r['arm']==factor]
        cost_ratio=ratio(median([r['seconds'] for r in proposed]),median([r['seconds'] for r in current]))
        cost_complete=all(r['seconds'] is not None for r in current+proposed)
        preserved=True
        axes={'R5':['discovery'],'R2':['clarity','consistency','pickup','departure'],'R7':['selection']}[factor]
        for seed in range(5):
            a=next(r for r in current if r['seed']==seed);b=next(r for r in proposed if r['seed']==seed)
            loss=[]
            for axis in axes:
                left=(a['judgment'] or {}).get('scores',{}).get(axis);right=(b['judgment'] or {}).get('scores',{}).get(axis)
                if not isinstance(left,dict) or any(v is None for v in left.values()):preserved=False
                if not isinstance(right,dict) or any(v is None for v in right.values()):preserved=False
                if factor!='R5' and not full(b['judgment'],axis):preserved=False
                if isinstance(left,dict) and isinstance(right,dict):
                    loss += [axis+'.'+key for key,value in left.items() if value is not None and (right.get(key) is None or right[key]<value)]
            if loss:preserved=False
            pairs.append(dict(factor=factor,seed=seed,current=a['id'],proposal=b['id'],seconds_ratio=ratio(b['seconds'],a['seconds']),process_losses=loss))
        safe=all(r['stable'] for r in proposed) and preserved
        safe=safe and all(r['measurement_eligible'] for r in current+proposed)
        if factor!='R7':safe=safe and all(r['outcome'].get('passed') for r in proposed)
        else:safe=safe and all(r['advice_unchanged'] for r in proposed)
        if factor=='R5':
            left,right=episode_total(current),episode_total(proposed)
            gain=right<left if left is not None and right is not None else None
        elif factor=='R2':gain=cost_complete and cost_ratio is not None and cost_ratio<=0.8 and all(r['writer_import_only'] for r in proposed)
        else:
            left,right=median([r['reply_words'] for r in current]),median([r['reply_words'] for r in proposed])
            gain=right<left if left is not None and right is not None else None
        factor_ids={r['id'] for r in current+proposed}
        known_ids={r['id'] for r in rows}
        factor_errors=[error for error in errors if not any(ident in error for ident in known_ids) or any(ident in error for ident in factor_ids)]
        gates[factor]=dict(valid=not factor_errors,errors=factor_errors,safety_and_process_preserved=safe,measured_gain=gain,
                           criterion_met=not factor_errors and safe and gain is True,group_median_seconds_ratio=cost_ratio,
                           cost_measurement_complete=cost_complete,
                           proposal_instruction_seen_in_all_cases=all(r['proposal_text_seen'] for r in proposed),
                           interpretation='sandbox-only; no adoption authority; descriptive small matched comparison')
    result=dict(schema=1,candidate=control['candidate'],driver_head=control['driver_head'],cli=control['cli'],
                groups=groups,rows=rows,pairs=pairs,gates=gates,controls=controls,
                grading_validated=not schema_errors and controls_valid,all_measurements_validated=not errors,errors=errors,
                limits=['Native default model is unpinned; catalog metadata remains available.',
                        'No humans, actual first-use learning, abrupt recovery, publication or combined-candidate release tested.',
                        'Source-read visibility does not establish adherence or a per-rule causal cost.',
                        'R5 discovery is five different domains, not five repeated samples in each domain.',
                        'Missing runtime/unsafe evidence is unavailable; all attempts retained.'])
    save(output/'results.json',result)
    for name in ('source-audit.json','owner-audit.json','control-adjudication.json'):
        (output/name).write_bytes((root/name).read_bytes())
    lines=['# Per-case refinement observations','','All values are current / isolated proposal. Process losses compare the same seed; no overall quality score.','',
           '| Factor | Seed | Stable | Final CLI pass | Seconds | Process losses |','| --- | --- | --- | --- | --- | --- |']
    for pair in pairs:
        a=next(r for r in rows if r['id']==pair['current']);b=next(r for r in rows if r['id']==pair['proposal'])
        left='unavailable' if a['seconds'] is None else f"{a['seconds']:.3f}"
        right='unavailable' if b['seconds'] is None else f"{b['seconds']:.3f}"
        lines.append(f"| {pair['factor']} | {pair['seed']+1} | {a['stable']} / {b['stable']} | {a['outcome'].get('passed','n/a')} / {b['outcome'].get('passed','n/a')} | {left} / {right} | {', '.join(pair['process_losses']) or 'none'} |")
    (output.parent/'case-table.md').write_text('\n'.join(lines)+'\n')
    unsafe={t['id'] for t in control['trials'] if not raw[t['id']]['stable']}
    archive=output/'native-evidence.tar.gz'
    def filter_member(member):
        parts=Path(member.name).parts
        if len(parts)>2 and parts[:2]==('run','projects') and parts[2] in unsafe:return None
        return member
    with tarfile.open(archive,'w:gz') as stream:stream.add(root,arcname='run',filter=filter_member)
    save(output/'archive.json',dict(sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),bytes=archive.stat().st_size,unsafe_live_projects_excluded=sorted(unsafe)))
    print(json.dumps(dict(rows=len(rows),grading_validated=result['grading_validated'],all_measurements_validated=not errors,errors=errors,gates=gates)),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--root',type=Path,required=True);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    collect(args.root,args.output)
