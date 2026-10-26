"""Reuse the blind rubric and retain partial turns without treating receipts as turns."""
import argparse
import importlib.util
import json
from pathlib import Path
import re
import shutil

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('waited_collector', HERE.parent/'revision2/collect.py')
collector = importlib.util.module_from_spec(spec);spec.loader.exec_module(collector)
spec = importlib.util.spec_from_file_location('waited_adapter',HERE/'run.py')
adapter = importlib.util.module_from_spec(spec);spec.loader.exec_module(adapter)
collector.run = adapter.base
collector.HERE = HERE
original_packet_trial = collector.packet_trial


def metadata_paths(directory):
    return sorted((p for p in Path(directory).glob('turn-*.json') if re.fullmatch(r'turn-[0-9]+\.json',p.name)),
                  key=lambda p:int(p.stem.split('-')[1]))


def packet_trial(trial,target):
    record=Path(trial['record'])
    if (record/'result.json').exists(): return original_packet_trial(trial,target)
    target.mkdir()
    errors={p.name:p.read_text() for p in record.glob('*error*.json')}
    turns=metadata_paths(record)
    context=dict(kind=trial['kind'],stable=False,
        execution_state='partial_infrastructure_stop' if turns else 'not_attempted',
        unavailable=errors or ('Driver stopped before finalizing the native trial.' if turns else 'Queue stopped before admission; no actor was launched.'),
        public_contract=collector.run.PUBLIC,settled_truth=collector.run.facts(collector.run.PROFILES[trial['seed']]))
    if trial['kind']=='unknown':
        context['settled_truth']['identity']='Undecided: dependent behavior must remain pending.'
    if trial['kind']=='known':
        context['original_and_change']='Originally preserve case; owner superseded with lowercase keys because suppliers send case variants. Saved spec/plan supplied before actor.'
    collector.run.save(target/'context.json',context)
    recovered=[];parsed={}
    for path in turns:
        number=int(path.stem.split('-')[1]);parsed[number]=collector.write_turn(record,target,number,json.loads(path.read_text()))
    for number in sorted(parsed):
        matching=[p for p in metadata_paths(record/'owner') if int(p.stem.split('-')[1]) in {number*2+1,number*2+2}]
        if not matching:continue
        classification=json.loads(matching[-1].read_text())
        body=(classification.get('messages') or [''])[-1]
        if body.startswith('```json') and body.endswith('```'):body=body[7:-3].strip()
        try:value=json.loads(body)
        except ValueError:value={'unparsed_message':body}
        prompt=record/('turn-%d.prompt.txt' % (number+1))
        recovered.append(dict(turn=number,classification=value,actual_next_prompt=prompt.read_text() if prompt.exists() else None,
            delivered=bool(number+1 in parsed and parsed[number+1]['thread_started']),
            provenance='Recovered exact native metadata only; admission/cooldown receipts are not model turns. No missing settlement inferred.'))
    collector.run.save(target/'owner-events.json',recovered)
    for path in sorted(record.glob('checkpoint-*')):shutil.copytree(path,target/path.name)
    post=record/'post-stop-observation.json'
    collector.run.save(target/'public-outcomes.json',{'post_stop':json.loads(post.read_text())} if post.exists() else {})
    if (record/'post-stop-project').exists():shutil.copytree(record/'post-stop-project',target/'post-stop-project')


collector.packet_trial=packet_trial

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['prepare','validate']);parser.add_argument('--root',type=Path,required=True)
    parser.add_argument('--packet',type=Path,required=True);args=parser.parse_args()
    (collector.prepare if args.action=='prepare' else collector.validate)(args.root,args.packet)
