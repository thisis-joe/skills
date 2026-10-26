"""Wait within one native call on explicit 429 cooldowns; keep all old cohorts intact."""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import re
import time

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('waited_revision2', HERE.parent/'revision2/run.py')
previous = importlib.util.module_from_spec(spec); spec.loader.exec_module(previous)
base = previous.base
ROOT = previous.ROOT
model_spec = importlib.util.spec_from_file_location('waited_model_selection', HERE/'model_selection.py')
model_selection = importlib.util.module_from_spec(model_spec); model_spec.loader.exec_module(model_selection)
base.engine.subprocess = model_selection.ModelSubprocess(base.engine.subprocess)
ORIGINAL_FACTS = previous.ORIGINAL_FACTS
RANGE_FACT = previous.RANGE_FACT
prepare_project = previous.prepare_project
observe = previous.observe
COOLDOWN_ALLOWANCE = 1800.0
COHORT_COOLDOWN_ALLOWANCE = 5400.0
MIN_NATIVE_START_GAP = 30.0
LAST_NATIVE_START = None
RETRY = re.compile(r'^(?P<time>\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?Z)\s+.*codex_core::responses_retry:.*retrying sampling request \(\d+/\d+ in (?P<delay>\d+(?:\.\d+)?)s\).*429 Too Many Requests')


def budget(stderr, started_utc, now_utc, elapsed, active_limit, previous_cooldown=0):
    """Provider-advertised overlap is an estimate, explicitly bounded and not CPU time."""
    intervals = []
    notices = []
    for line in stderr.splitlines():
        match = RETRY.match(line)
        if not match: continue
        try:
            timestamp = datetime.fromisoformat(match['time'].replace('Z', '+00:00')).timestamp()
        except (ValueError, OverflowError, OSError):
            continue
        delay = float(match['delay'])
        if not math.isfinite(delay) or delay < 0: continue
        notices.append(dict(timestamp_utc=match['time'], delay_seconds=delay))
        left = max(started_utc, timestamp)
        right = min(now_utc, timestamp + delay)
        if right > left: intervals.append((left, right))
    merged = []
    for left, right in sorted(intervals):
        if merged and left <= merged[-1][1]: merged[-1][1] = max(merged[-1][1], right)
        else: merged.append([left, right])
    overlap = sum(right-left for left, right in merged)
    credit = min(elapsed, overlap, COOLDOWN_ALLOWANCE)
    charged = max(0.0, elapsed-credit)
    wall_limit = active_limit + COOLDOWN_ALLOWANCE
    cohort_total = previous_cooldown+credit
    reason = ('cohort_cooldown_budget_exhausted' if cohort_total >= COHORT_COOLDOWN_ALLOWANCE else
              'wall_budget_exhausted' if elapsed >= wall_limit else
              'non_cooldown_budget_exhausted' if charged >= active_limit else None)
    return dict(wall_seconds=round(elapsed, 3), announced_cooldown_overlap_seconds=round(overlap, 3),
                credited_cooldown_estimate_seconds=round(credit, 3), charged_remainder_seconds=round(charged, 3),
                non_cooldown_budget_seconds=active_limit, cooldown_allowance_seconds=COOLDOWN_ALLOWANCE,
                cohort_cooldown_estimate_seconds=round(cohort_total, 3),
                cohort_cooldown_allowance_seconds=COHORT_COOLDOWN_ALLOWANCE,
                hard_wall_budget_seconds=wall_limit, stop_reason=reason, retry_notices=notices,
                limitation='Announced retry-window overlap is an estimate, not measured model compute time.')


def frozen():
    paths = [HERE/'protocol.md', HERE/'run.py', HERE/'test_waits.py', HERE/'collect.py', HERE/'model_selection.py',
             HERE.parent/'revision2/protocol.md', HERE.parent/'revision2/run.py',
             HERE.parent/'revision2/test_instrument.py', HERE.parent/'revision2/collect.py',
             HERE.parent/'protocol.md', previous.PARENT/'protocol.md', previous.PARENT/'run.py',
             previous.PARENT/'collect.py', Path(base.life.__file__), Path(base.engine.__file__),
             ROOT/'tests/fixtures/collaboration_catalog_control.py']
    return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}


def native(project, record, number, prompt, thread=None, timeout=420):
    global LAST_NATIVE_START
    if previous.stop_requested(): raise previous.AdmissionStopped('Queue admission stopped before this call')
    pacing_path = previous.RUN_ROOT/'last-native-start.json'
    if pacing_path.exists():
        persisted = json.loads(pacing_path.read_text())['monotonic']
        if persisted > time.monotonic(): raise RuntimeError('Clock/reset invalidates frozen admission pacing')
        LAST_NATIVE_START = max(LAST_NATIVE_START or 0, persisted)
    waiting = time.monotonic()
    while LAST_NATIVE_START is not None and time.monotonic()-LAST_NATIVE_START < MIN_NATIVE_START_GAP:
        if previous.stop_requested(): raise previous.AdmissionStopped('Queue stopped during pacing')
        time.sleep(0.25)
    LAST_NATIVE_START = time.monotonic()
    base.save(pacing_path, dict(monotonic=LAST_NATIVE_START, utc=datetime.now(timezone.utc).isoformat()))
    started_utc = datetime.now(timezone.utc).timestamp()
    record = Path(record)
    receipt = record/('turn-%d.cooldown.json' % number)
    stderr = record/('turn-%d.stderr.txt' % number)
    prior_cooldown = sum(json.loads(p.read_text())['credited_cooldown_estimate_seconds']
                         for p in previous.RUN_ROOT.rglob('turn-*.cooldown.json') if p != receipt)
    base.save(record/('turn-%d.admission.json' % number), dict(
        started_utc=datetime.now(timezone.utc).isoformat(), pacing_seconds=LAST_NATIVE_START-waiting,
        minimum_start_gap_seconds=MIN_NATIVE_START_GAP, non_cooldown_budget_seconds=timeout,
        hard_wall_budget_seconds=timeout+COOLDOWN_ALLOWANCE))
    latest = None
    prior_notices = 0
    def monitor():
        nonlocal latest, prior_notices
        elapsed = time.monotonic()-LAST_NATIVE_START
        content = stderr.read_text(errors='replace') if stderr.exists() else ''
        latest = budget(content, started_utc, datetime.now(timezone.utc).timestamp(), elapsed, timeout, prior_cooldown)
        if len(latest['retry_notices']) != prior_notices:
            prior_notices = len(latest['retry_notices'])
            base.save(receipt, latest)
            print(json.dumps(dict(capacity_wait=str(record), turn=number, notices=latest['retry_notices'])), flush=True)
        return previous.stop_requested() or latest['stop_reason'] is not None
    result = base.engine.native(project, record, number, prompt, thread=thread,
                                timeout=timeout+COOLDOWN_ALLOWANCE, interrupt=monitor)
    monitor()
    latest['native_original_exit'] = result.get('exit')
    latest['native_seconds'] = result.get('seconds')
    invalid = []
    if result.get('interrupted') or result.get('cancellation') is not None:
        invalid.append('native cancellation occurred')
    if result.get('event_errors'): invalid.append('malformed native events')
    if not result.get('process_started') or not result.get('usage_events'):
        invalid.append('missing process start or completed-turn event')
    if invalid: result['error'] = '; '.join([result.get('error', ''), *invalid]).strip('; ')
    if latest['stop_reason'] is not None and base.stable(result):
        result['error'] = 'Completed after the prospectively bounded budget: '+latest['stop_reason']
    if result.get('process_started') and result.get('started_at'):
        model_receipt = model_selection.session_model(result)
        base.save(record/('turn-%d.model.json' % number), model_receipt)
        result['model_selection'] = model_receipt
        if not model_receipt['verified']:
            result['error'] = '; '.join([result.get('error', ''), 'Native model/effort could not be verified']).strip('; ')
    latest['effective_native_valid'] = base.stable(result)
    base.save(receipt, latest)
    result['cooldown'] = latest
    result['capacity_observed'] = bool(latest['retry_notices']) or (stderr.exists() and '429 Too Many Requests' in stderr.read_text(errors='replace'))
    if not base.stable(result):
        previous.request_stop(dict(reason=latest['stop_reason'] or 'native_operational_failure',
            record=str(record), turn=number, exit=result.get('exit'), timeout=result.get('timeout'), error=result.get('error')))
    return result


previous.native = native
previous.frozen = frozen
base.native = native
base.frozen = frozen


def prepare(root, candidate):
    previous.prepare(root, candidate)
    path = Path(root)/'control.json'; control = json.loads(path.read_text())
    control.update(model=model_selection.MODEL, reasoning_effort=model_selection.EFFORT, recovery='waited', predecessor='revision2_stopped_not_resumed',
                   active_budgets={'actor':420, 'classifier':90}, cooldown_allowance_seconds=COOLDOWN_ALLOWANCE,
                   cohort_cooldown_allowance_seconds=COHORT_COOLDOWN_ALLOWANCE,
                   hard_wall_budgets={'actor':2220,'classifier':1890}, minimum_native_start_gap=30, workers=1)
    base.save(path, control)


def controls(root):
    previous.RUN_ROOT = Path(root)
    tests = [
        ('May we reject prices above 9223372036854775807 because SQLite uses signed 64-bit integers?', {'storage_range'}, False),
        ('Should the stored and displayed SKU retain the first spelling or use the canonical lowercase key?', {'identity'}, False),
        ('What should the list JSON fields and ordering be?', {'public_contract'}, False),
        ('Should we email a purchasing manager whenever an import is rejected?', set(), True),
    ]
    results = []
    for number, (question, topics, unresolved) in enumerate(tests, 1):
        try: value = base.classify(Path(root)/'owner', Path(root)/'waited-classifier-controls', number, question)
        except previous.AdmissionStopped:
            base.save(Path(root)/'classifier-controls.json', dict(passed=False,results=results,stopped=True)); return
        actual = set(t for q in value['questions'] for t in q['topics'])
        answer = base.reply(value['questions'], 0)
        passed = bool(value['valid'] and value['questions'] and actual == topics and bool(answer['unresolved']) == unresolved)
        results.append(dict(question=question,expected_topics=sorted(topics),result=value,answer=answer,passed=passed))
        base.save(Path(root)/'classifier-controls.json',dict(passed=len(results)==4 and all(r['passed'] for r in results),results=results))
        print(json.dumps(dict(control=number,passed=passed)),flush=True)
        if not passed:
            previous.request_stop(dict(reason='classifier_control_failed',control=number));return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['prepare','controls','run']);parser.add_argument('--root',type=Path,required=True)
    parser.add_argument('--candidate');args=parser.parse_args()
    if args.action=='prepare':
        if not args.candidate:parser.error('--candidate committed ref required')
        prepare(args.root,args.candidate)
    elif args.action=='controls':controls(args.root)
    else:previous.run(args.root,1)
