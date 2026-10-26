"""One final prospective 900-second actor cohort; historical adapters stay unchanged."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('budget900_clock',HERE/'clock_fixed_run.py')
clock=importlib.util.module_from_spec(spec);spec.loader.exec_module(clock)
ORIGINAL_NATIVE=clock.native
ORIGINAL_FROZEN=clock.frozen


def native(project,record,number,prompt,thread=None,timeout=420):
    if timeout not in {420,90}:raise ValueError('Unexpected inherited actor/classifier budget')
    return ORIGINAL_NATIVE(project,record,number,prompt,thread=thread,
                           timeout=900 if timeout==420 else 90)


def frozen():
    result=ORIGINAL_FROZEN()
    for path in [HERE/'budget900-protocol.md',HERE/'budget900_run.py',HERE/'test_budget900.py']:
        result[str(path.relative_to(clock.ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest()
    return result


clock.previous.native=native
clock.base.native=native
clock.previous.frozen=frozen
clock.base.frozen=frozen


def prepare(root,candidate):
    clock.prepare(root,candidate)
    path=Path(root)/'control.json';value=json.loads(path.read_text())
    value.update(recovery='waited-clock-fixed-budget900',active_budgets={'actor':900,'classifier':90},
                 hard_wall_budgets={'actor':2700,'classifier':1890},
                 previous_420_second_cohort='retained incomplete; not resumed or pooled',
                 automatic_followup_cohorts_authorized=False,independent_judge='Sol family, xhigh; selected by root')
    clock.base.save(path,value)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['prepare','run']);parser.add_argument('--root',type=Path,required=True)
    parser.add_argument('--candidate');args=parser.parse_args()
    if args.action=='prepare':
        if not args.candidate:parser.error('--candidate committed ref required')
        prepare(args.root,args.candidate)
    else:clock.previous.run(args.root,1)
