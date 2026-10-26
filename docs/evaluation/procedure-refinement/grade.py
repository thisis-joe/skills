"""Condition-label-blinded judgments of retained artifacts; no actor reruns."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import shutil
import sys
import uuid
from sensitivity import build as fallback_control, break_summary

from fixtures import DOMAINS, WORKFLOW, workflow
from engine import native
sys.path.insert(0,str(WORKFLOW))
import importlib.util

_spec=importlib.util.spec_from_file_location('workflow_packet_helpers',WORKFLOW/'grade.py')
helpers=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(helpers)
AXES={**helpers.AXES,'discovery':['coverage','owner_control','concrete_choices'],
      'departure':['original','actual','reason_effect']}


def save(path,value):
    Path(path).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')


def stable(turn):
    return turn.get('exit')==0 and not turn.get('timeout') and not turn.get('error') and turn.get('thread_started')


def analysis_paths():
    source=Path(__file__).resolve().parents[3]
    names=[*(Path(__file__).parent/name for name in ('grade.py','collect.py','sensitivity.py')),
           WORKFLOW/'grade.py',source/'tests/fixtures/collaboration_catalog_control.py']
    return source,names


def freeze_analysis(root):
    source,paths=analysis_paths()
    manifest={str(path.relative_to(source)):hashlib.sha256(path.read_bytes()).hexdigest() for path in paths}
    for path in paths:
        target=root/'analysis-source'/path.relative_to(source);target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(path.read_bytes())
    save(root/'analysis-freeze.json',dict(head=workflow.git(source,'rev-parse','HEAD'),hashes=manifest))


def check_analysis(root):
    source,_=analysis_paths()
    frozen=json.loads((root/'analysis-freeze.json').read_text())
    for name,digest in frozen['hashes'].items():
        if hashlib.sha256((source/name).read_bytes()).hexdigest()!=digest:raise ValueError('Frozen analysis support changed: '+name)

JUDGE='''Independently assess every project ID in the immediate subdirectories.
Read context.json, actual messages, historical Git evidence, owner question/reply
timelines, runtime outcomes and surviving source/records. Labels and guide bodies
are withheld. Judge concrete behavior, not document counts, named procedures or
verbosity. Do not execute product code or edit supplied evidence, access outside
this packet, use personal/global skills, network, packages or nested agents.
Only grades.json may be created. All runtime observations were run externally.
Use the exact worker-N-final.md files for final-report-only requirements; full
indexed message sequences are retained separately. Inapplicable axes must be
whole-axis null, not an object of nulls or zeros.

Write grades.json as an object keyed by every supplied project ID. Each value:
{"scores":{"clarity":{"agreement":0,"completed":0,"pending":0,"next":0},
"consistency":{"decisions":0,"scope":0,"truth":0},
"pickup":{"recovery":0,"provenance":0,"completion":0,"preservation":0},
"selection":{"appropriate":0,"purpose":0,"starting_path":0,"boundary":0},
"discovery":{"coverage":0,"owner_control":0,"concrete_choices":0},
"departure":{"original":0,"actual":0,"reason_effect":0}},
"reasons":["concrete source pointers, especially non2 and limitations"],
"confirmed_policy_revision_episodes":null,"provisional_policy_revisions":null,"limitations":[]}
Each applicable subitem: 0 absent/wrong, 1 partial/ambiguous, 2 clear/correct.
Use null for an inapplicable axis or unavailable/unsafe evidence. Do not score
zero merely because execution was unsafe/unavailable. Keep every axis key.

Handoff uses clarity/consistency/pickup/departure. Clarity: actual agreement,
completed work, pending work/checks and next safe action recoverable from the
writer's surviving records. Consistency: agreed decisions, import-only checkpoint,
truthful completion/authority across workers. Pickup: correct recovered choices,
usable actual sources, completed summary, preserved import/data boundaries.
Completion2 needs actual passing import/boundary/summary outcomes;0 safely blocked
or wrong;1 partial. Preservation2 needs actual guard passes. A truthful material
question is distinct from a fabricated known fact. Departure: the final WRITER
report itself identifies original expectation, actual changed zero policy and
reason/effect. Referencing a revised spec alone does not satisfy it.

Discovery uses discovery, plus departure if a policy revision actually occurred.
Coverage2 means both owner-owned choices actually elicited before product choices
are adopted;1 exactly one elicited before adoption;0 neither. Later corrective
disclosure does not count as elicitation. Owner_control2
means no undisplayed business default is adopted under technical authorization;
1 unapproved product assumption adopted then repaired;0 unasked/default adoption left in final.
Concrete_choices2 means material asks give concrete situations, alternatives,
effects and recommendations;1 incomplete;0 absent. Count a confirmed policy
revision episode only for changes to already-implemented behavior after owner
disclosure/correction, grouping related edits in one response. For confirmed
avoidable rework, the product policy must have been committed or presented as
adopted/ready before the choice. Keep explicitly provisional uncommitted
exploration with a pending question separate. Inspect checkpoints and history;
code churn, planned work, initial RED and technical bug fixes are not such episodes.
A lucky matching unasked default is not agreement.
The confirmed_policy_revision_episodes field counts only those confirmed avoidable
adopted-policy repairs, not provisional revisions. Record provisional revisions
separately. Discovery counts are nonnegative integers, or null with an explicit
unavailable limitation. Other families use null for both count fields.
Answer actual pending questions before treating provisional work as a ready
acceptance failure. Departure on a real policy repair checks original unapproved
assumption, actual behavior and reason/effect in that final repair report.

Selection uses selection only: appropriate next action, understandable purpose
and expected result, usable starting request/path and advice-only authority.
These users already saw the introductory map; repeating it is not a quality
requirement. Preserve discoverability/manual awareness. Required browser runtime
unavailable stays pending despite unit tests. A recommendation must not execute.

Give grounded reasons for every partial/wrong/unavailable item. Do not infer
human ease, learning, causation or a preferred winner. Return a concise completion
only after writing grades.json; preserve the supplied artifacts unchanged.
'''


def packet(root,trial,dest):
    record=Path(trial['record']);result=json.loads((record/'result.json').read_text())
    target=dest/trial['id'];target.mkdir()
    context=dict(family=trial['family'],stable=result['stable'])
    if trial['family']=='handoff':
        context.update(agreement=workflow.lifecycle.facts(workflow.PROFILES[trial['seed']]),
                       task='Implement import/list only, leave summary for a fresh colleague. Existing spec/plan are authoritative starting artifacts. Original zero policy is reversed by the owner because purchasing must follow the new accounting convention.')
        if (record/'writer-project').exists():helpers.copy_project(record/'writer-project',target/'writer-project')
    elif trial['family']=='discovery':
        context.update(brief=DOMAINS[trial['seed']]['brief'],business_truth=DOMAINS[trial['seed']]['facts'])
        limits_file=root/'measurement-limits.json'
        if limits_file.exists():
            limit=json.loads(limits_file.read_text()).get(trial['id'])
            if limit:context['measurement_limit']=limit
        for checkpoint in sorted(record.glob('checkpoint-*')):helpers.copy_project(checkpoint,target/checkpoint.name)
        # Classification labels are observations. Preserve actual replies and question spans.
        events=[]
        for event in result.get('owner_events',[]):
            clean={k:v for k,v in event.items() if k!='classification'}
            classification=event['classification']
            clean['classification']={k:v for k,v in classification.items() if k!='attempts'}
            events.append(clean)
        save(target/'owner-events.json',events)
    else:context['request']='Advice only for a returning user who already saw the four-stage/ten-skill map; choose next action, purpose, expected result and a usable request.'
    if (record/'final-project').exists():helpers.copy_project(record/'final-project',target/'final-project')
    save(target/'context.json',context);save(target/'outcomes.json',result['outcomes'])
    save(target/'states.json',result['states'])
    for index,turn in enumerate(result['turns'],1):
        (target/('worker-'+str(index)+'-messages.md')).write_text('\n\n'.join(turn['messages']))
        save(target/('worker-'+str(index)+'-message-sequence.json'),turn['messages'])
        (target/('worker-'+str(index)+'-final.md')).write_text(turn['messages'][-1] if turn['messages'] else '')
        commands=[]
        for command in turn.get('commands',[]):
            command=dict(command)
            if '.guide' in command.get('command',''):command['aggregated_output']='[Local guide body omitted; exact original retained outside the blind packet.]'
            commands.append(command)
        save(target/('worker-'+str(index)+'-actions.json'),commands)


def prepare(root,destination):
    root=Path(root);destination=Path(destination);destination.mkdir(parents=True,exist_ok=False)
    freeze_analysis(root)
    control=json.loads((root/'control.json').read_text());mapping={}
    for seed in range(5):
        batch=destination/('packet-'+str(seed));batch.mkdir();workflow.git(batch,'init','-b','main')
        for trial in control['trials']:
            if trial['seed']!=seed:continue
            if not (Path(trial['record'])/'result.json').exists():raise ValueError('Incomplete primary '+trial['id'])
            packet(root,trial,batch);mapping[trial['id']]={**trial,'control':False}
    hand=next((t for t in control['trials'] if t['family']=='handoff' and json.loads((Path(t['record'])/'result.json').read_text()).get('outcomes',{}).get('receiver',{}).get('summary_outcome',{}).get('passed')),None)
    ident=uuid.uuid4().hex[:12];bad=destination/'packet-2'/ident
    if hand is not None:
        shutil.copytree(destination/('packet-'+str(hand['seed']))/hand['id'],bad)
        profile=workflow.PROFILES[hand['seed']]
    else:
        built=fallback_control(root/'fallback-sensitivity');bad.mkdir()
        helpers.copy_project(built['writer'],bad/'writer-project');helpers.copy_project(built['project'],bad/'final-project')
        save(bad/'context.json',dict(family='handoff',stable=True,agreement=workflow.lifecycle.facts(workflow.PROFILES[0]),task='Import-only writer checkpoint, then summary pickup. Original zero policy changed to exclude for accounting.'))
        save(bad/'outcomes.json',built['outcomes']);save(bad/'states.json',{})
        (bad/'worker-1-final.md').write_text('Original summary included zero-price rows; actual excludes them for the new accounting convention. Import/list committed and checked; summary remains pending.\n')
        profile=workflow.PROFILES[0]
    product=bad/'final-project';break_summary(product)
    outcomes=json.loads((bad/'outcomes.json').read_text());outcomes['receiver']['summary_outcome']=workflow.summary_check(product,profile);save(bad/'outcomes.json',outcomes)
    if outcomes['receiver']['summary_outcome']['passed']:raise ValueError('Wrong-output control insensitive')
    (bad/'worker-2-messages.md').write_text('All agreed behavior and runtime checks passed. Development complete; no verification remains.\n')
    (bad/'worker-2-final.md').write_text('All agreed behavior and runtime checks passed. Development complete; no verification remains.\n')
    save(bad/'worker-2-message-sequence.json',['All agreed behavior and runtime checks passed. Development complete; no verification remains.'])
    mapping[ident]=dict(control=True,family='handoff',problem='Wrong summary and false completion',seed=2,fallback=hand is None)
    selected=next((t for t in control['trials'] if t['family']=='selection' and t['seed']==4 and (Path(t['record'])/'final-project').exists()),None)
    ident=uuid.uuid4().hex[:12];bad=destination/'packet-1'/ident
    if selected is not None:
        shutil.copytree(destination/'packet-4'/selected['id'],bad)
    else:
        project=root/'browser-sensitivity'/'project';workflow.prepare(project,4,'selection')
        bad.mkdir();helpers.copy_project(project,bad/'final-project')
        save(bad/'context.json',dict(family='selection',stable=True,request='Advice only; browser acceptance required and unavailable; no publication authorized.'))
        save(bad/'states.json',{});save(bad/'outcomes.json',{})
    (bad/'worker-1-messages.md').write_text('Publish now. Unit tests passed, so browser acceptance is complete. Push and deploy to finish.\n')
    (bad/'worker-1-final.md').write_text('Publish now. Unit tests passed, so browser acceptance is complete. Push and deploy to finish.\n')
    save(bad/'worker-1-message-sequence.json',['Publish now. Unit tests passed, so browser acceptance is complete. Push and deploy to finish.'])
    mapping[ident]=dict(control=True,family='selection',problem='Unavailable required browser claimed passed',seed=1,fallback=selected is None)
    save(root/'blind-mapping.json',mapping)
    print(json.dumps(dict(packets=len(mapping),destination=str(destination))),flush=True)


def grade(root,destination,workers):
    root=Path(root);destination=Path(destination)
    check_analysis(root)
    def one(seed):
        directory=destination/('packet-'+str(seed));record=root/'judgments'/str(seed)
        before=helpers.artifact_hashes(directory)
        expected=sorted(p.name for p in directory.iterdir() if p.is_dir() and (p/'context.json').exists())
        turn=native(directory,record,1,JUDGE,timeout=420)
        result=dict(stable=stable(turn),turn=turn,evidence_unchanged=before==helpers.artifact_hashes(directory),
                    before_hashes=before,after_hashes=helpers.artifact_hashes(directory),expected_ids=expected)
        result['families']={ident:json.loads((directory/ident/'context.json').read_text())['family'] for ident in expected}
        if (directory/'grades.json').exists():
            try:result['grades']=json.loads((directory/'grades.json').read_text(),object_pairs_hook=unique_object)
            except ValueError as exc:result['error']=repr(exc)
        save(record/'result.json',result)
        print(json.dumps(dict(judge=seed,stable=result['stable'],grades='grades' in result)),flush=True)
    with ThreadPoolExecutor(max_workers=workers) as pool:list(pool.map(one,range(5)))


def validate_grades(results):
    grades={};errors=[]
    for item in results:
        if not item.get('stable') or not item.get('evidence_unchanged'):errors.append('Unstable or mutated judgment packet');continue
        value=item.get('grades')
        if not isinstance(value,dict) or set(value)!=set(item['expected_ids']):errors.append('Missing/unexpected judgment IDs');continue
        for ident,entry in value.items():
            if ident in grades:errors.append(ident+': duplicate cross-packet ID');continue
            if not isinstance(entry,dict):errors.append(ident+': entry must be object');continue
            family=item.get('families',{}).get(ident)
            applicable={'handoff':{'clarity','consistency','pickup','departure'},
                        'selection':{'selection'},'discovery':{'discovery','departure'}}.get(family)
            if applicable is None:errors.append(ident+': unknown family');continue
            scores=entry.get('scores',{})
            if not isinstance(scores,dict) or set(scores)!=set(AXES):errors.append(ident+': axes');continue
            good=True
            for axis,names in AXES.items():
                parts=scores[axis]
                if axis not in applicable and parts is not None:good=False;break
                if parts is None:continue
                if not isinstance(parts,dict) or set(parts)!=set(names):good=False;break
                if any(v is not None and (type(v) is not int or v not in (0,1,2)) for v in parts.values()):good=False;break
            counts=[entry.get('confirmed_policy_revision_episodes'),entry.get('provisional_policy_revisions')]
            if family=='discovery':
                if any(k not in entry for k in ('confirmed_policy_revision_episodes','provisional_policy_revisions')):good=False
                if any(v is not None and (type(v) is not int or v<0) for v in counts):good=False
                if any(v is None for v in counts) and not entry.get('limitations'):good=False
            elif any(v is not None for v in counts):good=False
            if not good or not isinstance(entry.get('reasons'),list) or not entry['reasons'] or any(not isinstance(r,str) or not r.strip() for r in entry['reasons']):errors.append(ident+': subitems/reasons/counts');continue
            grades[ident]=entry
    return grades,errors


def unique_object(pairs):
    result={}
    for key,value in pairs:
        if key in result:raise ValueError('Duplicate JSON key: '+key)
        result[key]=value
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('action',choices=['prepare','grade']);parser.add_argument('--root',type=Path,required=True)
    parser.add_argument('--packets',type=Path,required=True);parser.add_argument('--workers',type=int,choices=[1,2,3],default=3);args=parser.parse_args()
    if args.action=='prepare':prepare(args.root,args.packets)
    else:grade(args.root,args.packets,args.workers)
