"""Build condition-label-blinded owner-audit packets; perform no judgments."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import uuid

from lifecycle import AUTH, BRIEF, CHANGE, RESUME
from run import Session

MARKER = 'INPUT JSON:\n'


def load(path):
    return json.loads(Path(path).read_text())


def write(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def cleaner(root, trials):
    paths = {str(Path(t['project'])) for t in trials}
    paths.add(str(root))
    for path in list(paths):
        if path.startswith('/private/tmp/'):
            paths.add('/tmp/' + path[len('/private/tmp/'):])
    paths = sorted(paths, key=len, reverse=True)

    def clean(value):
        if isinstance(value, str):
            for path in paths:
                value = value.replace(path, '[project]' if path not in {str(root), '/tmp/' + str(root)[len('/private/tmp/'):]} else '[run]')
            return re.sub(r'coco-[a-zA-Z0-9_-]+', '[procedure]', value, flags=re.IGNORECASE)
        if isinstance(value, dict):
            return {key: clean(item) for key, item in value.items()}
        if isinstance(value, list):
            return [clean(item) for item in value]
        return value
    return clean


def prompt_input(native, root, record):
    """Recover the actual classifier input, never reconstruct a missing prompt."""
    original = native.get('records', {}).get('prompt')
    if not original:
        return dict(message=None, previously_supplied_topics=None,
                    error='Classifier prompt path unavailable')
    path = Path(original)
    candidates = [record / 'owner' / path.name, path]
    # Support relocated native archives whose original absolute paths disappeared.
    if '/records/' in str(path):
        candidates.insert(0, root / 'records' / str(path).split('/records/', 1)[1])
    selected = next((p for p in candidates if p.is_file()), None)
    if selected is None:
        return dict(message=None, previously_supplied_topics=None,
                    error='Classifier prompt file unavailable')
    text = selected.read_text()
    try:
        value = json.loads(text.split(MARKER, 1)[1])
        if not isinstance(value.get('message'), str):
            raise ValueError('message is not text')
        if not isinstance(value.get('previously_supplied_topics'), list):
            raise ValueError('previously_supplied_topics is not an array')
    except (IndexError, ValueError, AttributeError) as exc:
        return dict(message=None, previously_supplied_topics=None,
                    error='Classifier prompt could not be decoded: ' + str(exc))
    return dict(message=value['message'], previously_supplied_topics=value['previously_supplied_topics'], error=None)


def packet(trial, result, root, record):
    session = Session(trial)
    events, sources = [], []
    for index, event in enumerate(result.get('owner_events', []), 1):
        classification = event.get('owner_record')
        source = (prompt_input(classification.get('owner_record', {}), root, record)
                  if isinstance(classification, dict) else
                  dict(message=None, previously_supplied_topics=None,
                       error='No classifier applies to this event' if event.get('kind') == 'quality-correction'
                       else 'Classifier record unavailable'))
        sources.append(source)
        phase = event.get('phase')
        expected = (session.private_facts(phase) | session.public_facts(phase)) if phase in {'initial', 'change', 'resumed'} else None
        events.append(dict(event=index, phase=phase, kind=event.get('kind'),
                           questions=event.get('questions'), topics=event.get('topics'),
                           new_topics=event.get('new_topics'), repeated_topics=event.get('repeated_topics'),
                           delivered=event.get('delivered'), attempted=event.get('attempted'),
                           reply=event.get('reply'), failures=event.get('failed'),
                           actor_final=source['message'],
                           previously_supplied_topics=source['previously_supplied_topics'],
                           expected_full_fact_map=expected,
                           instrumentation=dict(prompt_error=source['error'],
                               owner_valid=classification.get('owner_valid') if isinstance(classification, dict) else None,
                               parse_error=classification.get('parse_error') if isinstance(classification, dict) else None)))
    attempts = []
    for path in sorted((record / 'owner').glob('turn-*.classification.json')):
        try:
            classification = load(path)
            source = prompt_input(classification.get('owner_record', {}), root, record)
            attempts.append(dict(actor_final=source['message'], previously_supplied_topics=source['previously_supplied_topics'],
                                 owner_valid=classification.get('owner_valid'), parse_error=classification.get('parse_error'),
                                 prompt_error=source['error'], questions=classification.get('questions')))
        except (OSError, ValueError, AttributeError) as exc:
            attempts.append(dict(actor_final=None, owner_valid=None, parse_error='Unreadable classifier record: ' + str(exc)))
    finals = []
    for index, turn in enumerate(result.get('turns', []), 1):
        final = turn['messages'][-1] if turn.get('messages') else None
        matches = [i + 1 for i, source in enumerate(sources) if final is not None and source['message'] == final]
        classified = [a for a in attempts if final is not None and a.get('actor_final') == final]
        finals.append(dict(turn=index, phase=turn.get('phase'), text=final,
                           classifier_event_coverage=bool(matches), matching_owner_events=matches,
                           classifier_attempts_matched=len(classified),
                           valid_classifier_coverage=any(a.get('owner_valid') is True for a in classified),
                           instrumentation=dict(state=turn.get('state'), exit=turn.get('exit'),
                                                timeout=turn.get('timeout'), error=turn.get('error'),
                                                thread_started=turn.get('thread_started'))))
    failures = {}
    for name in ['owner-failure.json', 'driver-error.json']:
        path = record / name
        if path.exists():
            try:
                failures[name] = load(path)
            except (OSError, ValueError) as exc:
                failures[name] = dict(error='Unreadable failure record: ' + str(exc))
    return dict(schema=1, events=events, actor_turn_finals=finals, classifier_attempts=attempts,
                statuses={name: detail.get('status') for name, detail in result.get('stages', {}).items()
                          if isinstance(detail, dict)},
                final_observation_stable=result.get('final_observation_stable'),
                controller_stop=result.get('controller_stop'), instrumentation_failures=failures,
                coverage_note='A completed change checkpoint can return before question classification. All actual turn finals are included; uncovered text must not be counted as no question. Corrections have no classifier input.')


def build(root, output):
    root, output = Path(root).resolve(), Path(output).resolve()
    if output.exists():
        raise FileExistsError('Refusing to overwrite audit packets: ' + str(output))
    control = load(root / 'control.json')
    trials = [trial for pair in control['pairs'] if pair['family'] == 'lifecycle' for trial in pair['trials']]
    if len(trials) != 10:
        raise ValueError('All ten lifecycle projects are required')
    completed = []
    for trial in trials:
        local = root / 'records' / trial['id']
        record = local if (local / 'result.json').is_file() else Path(trial['record'])
        path = record / 'result.json'
        if not path.is_file():
            raise ValueError('Lifecycle result is not complete: ' + trial['id'])
        result = load(path)
        if result.get('not_executed') or 'turns' not in result:
            raise ValueError('Not-executed markers are not completed lifecycle records: ' + trial['id'])
        completed.append((trial, result, record))
    clean = cleaner(root, trials)
    mapping = {}
    output.mkdir(parents=True, exist_ok=False)
    write(output / 'context.json', clean(dict(AUTH=AUTH, BRIEF=BRIEF, CHANGE=CHANGE, RESUME=RESUME,
          task='Audit whether actual questions were classified faithfully, supplied facts matched the question and phase, corrections remained distinct, and delivered-message claims matched instrumentation. Recover questions from any unclassified actor finals. Do not infer that absence of a classifier event means absence of a question.',
          limits='Condition labels and original project paths are withheld. Procedure names are redacted; business facts are preserved. This packet builder performs no execution or judgment.')))
    for trial, result, record in completed:
        ident = uuid.uuid4().hex[:12]
        while ident in mapping:
            ident = uuid.uuid4().hex[:12]
        write(output / (ident + '.json'), clean(packet(trial, result, root, record)))
        mapping[ident] = dict(trial_id=trial['id'], arm=trial['arm'], seed=trial['seed'])
    mapping_path = root / ('owner-audit-mapping-' + uuid.uuid4().hex[:12] + '.json')
    write(mapping_path, dict(packet_directory=str(output), mapping=mapping))
    subprocess.run(['git', 'init', '-b', 'main', str(output)], check=True, capture_output=True)
    print(json.dumps(dict(packets=len(mapping), output=str(output), mapping=str(mapping_path))))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    build(args.root, args.output)
