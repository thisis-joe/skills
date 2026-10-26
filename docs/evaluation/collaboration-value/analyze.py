"""Describe paired observations; do not turn procedure compliance into quality."""
import argparse
import json
from pathlib import Path
import statistics

PRIVATE = {'identity', 'collision', 'invalid', 'report'}
PUBLIC = {'import_contract', 'summary_contract', 'remaining_scope'}
ARMS = ('coco', 'bare')
FAMILIES = ('lifecycle', 'review')
ACCEPTANCE_FIELDS = ('initial_first_pass', 'initial_final_pass', 'changed_checkpoint_pass',
                     'resumed_first_pass', 'resumed_final_pass')
QUESTION_METRICS = ('private_choices_requested', 'settled_private_topic_requests',
                    'resumed_settled_private_requests', 'public_contract_topic_requests',
                    'resumed_public_contract_requests', 'procedure_questions')
NUMERIC_METRICS = ('actor_seconds', 'actor_turns', 'actor_commands',
                   'owner_messages_delivered', 'correction_messages',
                   'synthetic_owner_seconds', 'synthetic_owner_calls')


def load(path):
    return json.loads(Path(path).read_text())


def spread(values):
    values = [v for v in values if v is not None]
    return dict(n=len(values), median=statistics.median(values) if values else None,
                minimum=min(values) if values else None,
                maximum=max(values) if values else None,
                total=sum(values) if values else None)


def divide(left, right):
    return left / right if left is not None and right is not None and right > 0 else None


def question_metrics(events):
    """Use actual question spans; corrections disclose facts but ask no choices."""
    requested, delivered, newly_requested = set(), set(), set()
    private_reasks = public_requests = resumed_private = resumed_public = procedures = 0
    for event in events:
        questions = event.get('questions', [])
        topics = {t for q in questions for t in q.get('topics', [])}
        private = topics & PRIVATE
        requested.update(private)
        newly_requested.update(private & set(event.get('new_topics', [])))
        if event.get('delivered'):
            delivered.update(private)
        repeated = private & set(event.get('repeated_topics', []))
        private_reasks += len(repeated)
        public_requests += len(topics & PUBLIC)
        procedures += sum(q.get('kind') == 'procedure' for q in questions)
        if event.get('phase') == 'resumed':
            resumed_private += len(repeated)
            resumed_public += len(topics & PUBLIC)
    return dict(private_topics_requested=sorted(requested),
                private_choices_requested=len(requested),
                private_topics_delivered_in_question_answers=sorted(delivered),
                private_new_topics_requested=sorted(newly_requested),
                settled_private_topic_requests=private_reasks,
                resumed_settled_private_requests=resumed_private,
                public_contract_topic_requests=public_requests,
                resumed_public_contract_requests=resumed_public,
                procedure_questions=procedures)


def raw_records(root):
    if root is None:
        return {}
    control = load(root / 'control.json')
    records = {}
    for pair in control['pairs']:
        for trial in pair['trials']:
            # Prefer a relocated archive's own records over old absolute paths.
            local = root / 'records' / trial['id'] / 'result.json'
            path = local if local.exists() else Path(trial['record']) / 'result.json'
            if path.exists():
                records[trial['id']] = load(path)
    return records


def boolean_counts(values):
    values = list(values)
    return dict(true=sum(v is True for v in values), false=sum(v is False for v in values),
                unknown=sum(v is not True and v is not False for v in values))


def lifecycle_completed(row):
    """Require observed final acceptance and operational closure together."""
    closure = row.get('closure') or {}
    return (row.get('stable') is True and row.get('resumed_final_pass') is True
            and row.get('statuses', {}).get('resumed') == 'ready'
            and closure.get('owned_work_committed') is True
            and closure.get('feature_branch') is True)


def group_description(selected, family, arm, scope):
    metrics = {name: spread(r.get(name) for r in selected) for name in NUMERIC_METRICS}
    for name in QUESTION_METRICS:
        metrics[name] = spread(r['question_metrics'][name] if r['question_metrics'] else None
                               for r in selected)
    usage = [r.get('actor_usage', {}) for r in selected]
    for name in ['input_tokens', 'cached_input_tokens', 'output_tokens']:
        metrics[name] = spread(u.get(name) if u.get('recorded_turns', 0) > 0 else None for u in usage)
    quality = None
    if family == 'lifecycle':
        quality = {name: boolean_counts(r.get(name) for r in selected)
                   for name in (*ACCEPTANCE_FIELDS, 'pending_summary_exposure', 'stable')}
        for name in ['owned_work_committed', 'feature_branch']:
            quality[name] = boolean_counts((r.get('closure') or {}).get(name) for r in selected)
    return dict(family=family, arm=arm, scope=scope, n=len(selected), metrics=metrics,
                lifecycle_boolean_counts=quality,
                lifecycle_completion=(dict(demonstrated=sum(lifecycle_completed(r) for r in selected),
                    not_demonstrated=sum(not lifecycle_completed(r) for r in selected))
                    if family == 'lifecycle' else None),
                review_quality='Separate blinded judge required' if family == 'review' else None,
                usage_coverage=dict(
                    recorded_turns=sum(u.get('recorded_turns', 0) for u in usage),
                    unavailable_turns=sum(u.get('unavailable_turns', 0) for u in usage),
                    complete_projects=sum(u.get('unavailable_turns', 0) == 0 and
                                          u.get('recorded_turns', 0) > 0 for u in usage)))


def paired_distributions(pair_rows):
    """Use exactly the same matched rows for cost and intervention contrasts."""
    distributions = {}
    for name in (*NUMERIC_METRICS, *QUESTION_METRICS):
        differences, ratios = [], []
        for pair in pair_rows:
            values = {arm: (pair[arm]['question_metrics'].get(name)
                            if pair[arm]['question_metrics'] else None)
                      if name in QUESTION_METRICS else pair[arm].get(name) for arm in ARMS}
            left, right = values['coco'], values['bare']
            differences.append(left - right if left is not None and right is not None else None)
            ratios.append(divide(left, right))
        distributions[name] = dict(coco_minus_bare=spread(differences),
                                   coco_divided_by_bare=spread(ratios))
    return distributions


def describe(results, root=None):
    records = raw_records(root)
    rows, seen, missing_questions = [], set(), []
    for original in results['rows']:
        row = dict(original)
        key = row['family'], row['seed'], row['arm']
        if key in seen:
            raise ValueError('Duplicate family/seed/arm observation: %r' % (key,))
        seen.add(key)
        if row['family'] not in FAMILIES or row['arm'] not in ARMS:
            raise ValueError('Unexpected comparison condition: %r' % (key,))
        raw = records.get(row['id'])
        row['question_metrics'] = question_metrics(raw['owner_events']) if raw else None
        if raw is None:
            missing_questions.append(row['id'])
        rows.append(row)
    groups = []
    for family in FAMILIES:
        for arm in ARMS:
            selected = [r for r in rows if r['family'] == family and r['arm'] == arm]
            groups.append(group_description(selected, family, arm, 'all_attempts'))
    pairs = []
    for family in FAMILIES:
        for seed in sorted({r['seed'] for r in rows if r['family'] == family}):
            pair = {r['arm']: r for r in rows if r['family'] == family and r['seed'] == seed}
            if set(pair) != set(ARMS):
                pairs.append(dict(family=family, seed=seed, complete=False, available=sorted(pair)))
                continue
            c, b = pair['coco'], pair['bare']
            detail = dict(family=family, seed=seed, complete=True, ids={a: pair[a]['id'] for a in ARMS},
                          actor_seconds={a: pair[a]['actor_seconds'] for a in ARMS},
                          actor_seconds_ratio=divide(c['actor_seconds'], b['actor_seconds']),
                          actor_seconds_difference=c['actor_seconds'] - b['actor_seconds'],
                          actor_commands={a: pair[a]['actor_commands'] for a in ARMS},
                          statuses={a: pair[a]['statuses'] for a in ARMS},
                          stable={a: pair[a].get('stable') for a in ARMS},
                          interventions={a: {k: pair[a].get(k) for k in
                                            ['owner_messages_delivered', 'correction_messages']}
                                         for a in ARMS},
                          question_metrics={a: pair[a]['question_metrics'] for a in ARMS})
            if family == 'lifecycle':
                detail['acceptance'] = {name: {a: pair[a].get(name) for a in ARMS} for name in
                    (*ACCEPTANCE_FIELDS, 'pending_summary_exposure')}
                detail['completion_demonstrated'] = {a: lifecycle_completed(pair[a]) for a in ARMS}
            pairs.append(detail)
    paired = []
    for family in FAMILIES:
        complete = [p for p in pairs if p['family'] == family and p['complete']]
        paired.append(dict(family=family, n=len(complete),
                           scope='all_available_pairs_including_unfinished_attempts',
                           cost_increase_pairs=sum(p['actor_seconds_difference'] > 0 for p in complete),
                           actor_seconds_ratio=spread(p['actor_seconds_ratio'] for p in complete),
                           actor_seconds_difference=spread(p['actor_seconds_difference'] for p in complete),
                           procedure_screen='Not decided: requires acceptance, blinded review and source/rework audit; cost alone is not a causal rule attribution.'))
    joint_seeds = [p['seed'] for p in pairs if p['family'] == 'lifecycle' and p['complete']
                   and all(p['completion_demonstrated'].values())]
    joint_rows = [{arm: next(r for r in rows if r['family'] == 'lifecycle' and r['seed'] == seed
                            and r['arm'] == arm) for arm in ARMS} for seed in joint_seeds]
    jointly_completed = dict(family='lifecycle', n=len(joint_seeds), seeds=joint_seeds,
        scope='Same matched seeds with demonstrated completion in both arms; failures remain in all-attempt results.',
        groups=[group_description([p[arm] for p in joint_rows], 'lifecycle', arm,
                                   'jointly_completed_pairs') for arm in ARMS],
        paired_distributions=paired_distributions(joint_rows),
        cost_increase_pairs=sum(p['coco']['actor_seconds'] > p['bare']['actor_seconds'] for p in joint_rows))
    return dict(schema=2, candidate=results.get('candidate'), driver_head=results.get('driver_head'),
                groups=groups, pairs=pairs, paired_costs=paired,
                jointly_completed=jointly_completed,
                incomplete=results.get('incomplete', []),
                question_records_unavailable=missing_questions,
                limits=[
                    'Five paired projects per family when complete; lifecycle stages are not independent samples.',
                    'All-attempt costs include unfinished work. Lower intervention on an unfinished attempt is not completion efficiency.',
                    'Jointly completed distributions use the same matched seeds in both arms and condition on observed completion; they are descriptive, not a causal success-adjusted estimate.',
                    'Completion requires stable observation, final resume acceptance, ready resume status, committed owned work and a feature branch. Unknown evidence cannot demonstrate completion.',
                    'Descriptive observations only: no significance test, overall quality score or causal speedup claim.',
                    'Actor elapsed time is not human effort or monetary price; synthetic owner costs remain separate.',
                    'Unavailable usage is not zero. Partially recorded token totals are lower bounds; inspect coverage.',
                    'Private elicitation uses actual questions only, excluding corrective fact disclosure. Raw records are required.',
                    'Public contract requests and already-settled private requests are separate; neither automatically proves waste.',
                    'Review quality requires separate blinded grading; report status and source checks are not defect recall.',
                    'Procedure reduction requires the frozen quality/rework screen and later single-rule ablation.'])


def number(value):
    if value is None:
        return 'unavailable'
    if isinstance(value, float):
        return ('%.3f' % value).rstrip('0').rstrip('.')
    return str(value)


def distribution(metric):
    return ('%s [%s, %s]; n=%s' % tuple(number(metric[k]) for k in
            ['median', 'minimum', 'maximum', 'n'])) if metric['n'] else 'unavailable; n=0'


def both(values, formatter=number):
    return ' / '.join(formatter(values[a]) for a in ARMS)


def acceptance(value):
    return 'pass' if value is True else 'fail' if value is False else 'unavailable'


def markdown(data):
    lines = ['# Descriptive paired collaboration observations', '',
             'All paired cells show **COCO / no skills**. Distributions show median [minimum, maximum].', '',
             'Five projects per family when complete. Lifecycle stages belong to the same projects; '
             'they are not independent trials. No overall quality score or significance claim is calculated.', '',
             'All-attempt costs retain failures and unfinished work. A lower intervention count on unfinished work '
             'does not demonstrate a more efficient completed task.', '',
             '## Paired actor cost: all attempts', '',
             '| Family | Seed | Seconds COCO / no skills | COCO/no-skills ratio | Difference seconds |',
             '| --- | ---: | ---: | ---: | ---: |']
    for pair in data['pairs']:
        if not pair['complete']:
            lines.append('| %s | %s | incomplete | unavailable | unavailable |' % (pair['family'], pair['seed']))
        else:
            lines.append('| %s | %s | %s | %s | %s |' % (pair['family'], pair['seed'],
                         both(pair['actor_seconds']), number(pair['actor_seconds_ratio']),
                         number(pair['actor_seconds_difference'])))
    lines += ['', '| Family | Available matched pairs | COCO cost increased | Paired ratio distribution |',
              '| --- | ---: | ---: | --- |']
    for family in data['paired_costs']:
        lines.append('| %s | %s | %s | %s |' % (family['family'], family['n'],
                     family['cost_increase_pairs'], distribution(family['actor_seconds_ratio'])))
    lines += ['', '## Lifecycle acceptance', '',
              'First-pass and after-repair outcomes are retained separately; unavailable is neither pass nor fail.', '',
              '| Seed | Initial first | Initial final | Changed checkpoint | Resume first | Resume final | Pending summary exposed |',
              '| ---: | --- | --- | --- | --- | --- | --- |']
    for pair in data['pairs']:
        if pair['family'] == 'lifecycle' and pair['complete']:
            outcome = pair['acceptance']
            cells = [both(outcome[k], acceptance) for k in
                     ['initial_first_pass', 'initial_final_pass', 'changed_checkpoint_pass',
                      'resumed_first_pass', 'resumed_final_pass']]
            cells.append(both(outcome['pending_summary_exposure']))
            lines.append('| %s | %s |' % (pair['seed'], ' | '.join(cells)))
    lifecycle_groups = {g['arm']: g for g in data['groups'] if g['family'] == 'lifecycle'}
    lines += ['', 'Boolean observations below show **true / false / unknown** counts. Pending summary exposure '
              'is a context observation; first-pass failures can subsequently pass after repair.', '',
              '| Lifecycle observation | COCO true / false / unknown | No skills true / false / unknown |',
              '| --- | --- | --- |']
    for name in (*ACCEPTANCE_FIELDS, 'pending_summary_exposure', 'stable', 'owned_work_committed', 'feature_branch'):
        cells = [' / '.join(str(lifecycle_groups[arm]['lifecycle_boolean_counts'][name][k])
                            for k in ['true', 'false', 'unknown']) for arm in ARMS]
        lines.append('| %s | %s |' % (name, ' | '.join(cells)))
    lines += ['', '| Lifecycle completion | COCO | No skills |', '| --- | ---: | ---: |']
    for name in ['demonstrated', 'not_demonstrated']:
        lines.append('| %s | %s |' % (name, ' | '.join(str(lifecycle_groups[a]['lifecycle_completion'][name]) for a in ARMS)))
    joint = data['jointly_completed']
    lines += ['', '## Jointly completed lifecycle pairs', '',
              'Both arms demonstrated completion for %s matched seeds: %s. Completion requires stable observation, '
              'final resume acceptance, ready resume status, committed owned work and a feature branch. '
              'The table conditions on that same subset in both arms; excluded attempts remain above. '
              'This is descriptive selection, not a causal success-adjusted estimate.' %
              (joint['n'], ', '.join(str(s) for s in joint['seeds']) or 'none'), '',
              '| Metric | COCO median [min, max] | No skills median [min, max] | Paired COCO minus no skills |',
              '| --- | --- | --- | --- |']
    joint_groups = {g['arm']: g for g in joint['groups']}
    for name in ['actor_seconds', 'actor_commands', 'owner_messages_delivered', 'correction_messages',
                 'private_choices_requested', 'resumed_public_contract_requests', 'procedure_questions']:
        lines.append('| %s | %s | %s | %s |' % (name,
                     distribution(joint_groups['coco']['metrics'][name]),
                     distribution(joint_groups['bare']['metrics'][name]),
                     distribution(joint['paired_distributions'][name]['coco_minus_bare'])))
    lines += ['', 'Review completion/quality remains subject to the separate blinded judge. '
              'All question metrics are classifier-based observations; uncovered actor finals require the owner audit.', '',
              '## Cost distributions and usage coverage: all attempts', '',
              '| Family | Arm | Metric | Median [min, max]; projects observed | Total |',
              '| --- | --- | --- | --- | ---: |']
    for group in data['groups']:
        for name in ['actor_seconds', 'actor_turns', 'actor_commands', 'input_tokens',
                     'cached_input_tokens', 'output_tokens', 'synthetic_owner_seconds', 'synthetic_owner_calls']:
            metric = group['metrics'][name]
            lines.append('| %s | %s | %s | %s | %s |' % (group['family'], group['arm'], name,
                         distribution(metric), number(metric['total'])))
        coverage = group['usage_coverage']
        lines.append('| %s | %s | usage coverage | %s recorded turns; %s unavailable turns | %s complete projects |' %
                     (group['family'], group['arm'], coverage['recorded_turns'],
                      coverage['unavailable_turns'], coverage['complete_projects']))
    lines += ['', 'Token totals with unavailable turns are lower bounds. They must not be compared as complete costs.', '',
              '## Owner intervention and elicitation: all attempts', '',
              'Counts are synthetic proxies, not measured human time. Private choices are distinct topics actually asked per project; '
              'correction messages do not create elicitation credit. Public requests can be first disclosure or recall.', '',
              '| Family | Arm | Metric | Median [min, max]; projects observed | Total |',
              '| --- | --- | --- | --- | ---: |']
    for group in data['groups']:
        for name in ['owner_messages_delivered', 'correction_messages', 'private_choices_requested',
                     'settled_private_topic_requests', 'resumed_settled_private_requests',
                     'public_contract_topic_requests', 'resumed_public_contract_requests', 'procedure_questions']:
            metric = group['metrics'][name]
            lines.append('| %s | %s | %s | %s | %s |' % (group['family'], group['arm'], name,
                         distribution(metric), number(metric['total'])))
    lines += ['', '## Limits', ''] + ['- ' + item for item in data['limits']]
    if data['question_records_unavailable']:
        lines += ['', 'Raw question records unavailable for: ' + ', '.join(data['question_records_unavailable']) + '.']
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--results', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--root', type=Path, help='Execution root containing control.json and raw records; needed for question-only elicitation.')
    args = parser.parse_args()
    data = describe(load(args.results), args.root)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / 'analysis.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    (args.output / 'tables.md').write_text(markdown(data))
    print(json.dumps(dict(output=str(args.output), pairs=len(data['pairs']),
                          incomplete_pairs=sum(not p['complete'] for p in data['pairs']),
                          question_records_unavailable=len(data['question_records_unavailable']))))


if __name__ == '__main__':
    main()
