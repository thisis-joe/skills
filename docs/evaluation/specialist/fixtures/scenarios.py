"""Disposable scenario implementations; never product or production evidence."""
import hashlib
import json
import re
import sqlite3
from collections import Counter
from pathlib import Path


def delete_route(root, authenticated_tenant, relative_path):
    # Deliberately vulnerable review target: lexical shape is the only guard.
    if not re.fullmatch(re.escape(authenticated_tenant) + r'/jobs/[a-z-]+/data.txt', relative_path):
        raise ValueError('invalid shape')
    (Path(root) / relative_path).unlink()
    return 204


def old_contact(row):
    return row['contact_email']


def new_contact(row):
    return row['email']


def canonical_email(raw):
    return raw.strip().lower()


def dual_write(row, raw):
    row['contact_email'] = raw
    row['email'] = canonical_email(raw)
    row['revision'] += 1


def naive_backfill(row, scanned_old):
    row['email'] = canonical_email(scanned_old)


def safe_backfill(row, scanned_old, scanned_revision):
    if row['revision'] != scanned_revision:
        return 'retry-current-row'
    if row.get('email') is None:
        row['email'] = canonical_email(scanned_old)
    return 'reconciled'


class LocalTelemetry:
    """In-memory local sink, deliberately no exporter or notification capability."""
    ROUTES = {'/jobs/{job_id}', '/health'}
    OUTCOMES = {'success', 'error', 'timeout'}

    def __init__(self):
        self.logs = []
        self.spans = []
        self.counts = Counter()
        self.durations = []

    def record(self, request_id, entry_point, route, outcome, duration_seconds):
        if route not in self.ROUTES or outcome not in self.OUTCOMES:
            raise ValueError('unbounded metric dimension')
        if entry_point not in {'http', 'worker'}:
            raise ValueError('unknown entry point')
        labels = (route, 'POST', outcome)
        self.counts[labels] += 1
        self.durations.append({'labels': labels, 'seconds': duration_seconds})
        self.logs.append({'event': 'job.request.completed', 'request_id': request_id,
                          'entryPoint': entry_point, 'route': route, 'outcome': outcome})
        self.spans.append({'name': 'job.request', 'request_id': request_id,
                           'entryPoint': entry_point, 'route': route,
                           'status': outcome, 'seconds': duration_seconds})


class LocalIssueBot:
    """Durable local preview. Provider effects are rows in this SAME scratch DB.

    Production origin verification and provider readback remain unverified.
    """
    ALLOWED = {'repository', 'issue_id', 'event_id', 'delivery_id', 'action', 'comment'}

    def __init__(self, path):
        self.db = sqlite3.connect(path, isolation_level=None)
        self.db.executescript('''
          CREATE TABLE IF NOT EXISTS jobs
            (key TEXT PRIMARY KEY, payload_hash TEXT NOT NULL,
             state TEXT NOT NULL, attempts INTEGER NOT NULL, result TEXT);
          CREATE TABLE IF NOT EXISTS provider_effects
            (key TEXT PRIMARY KEY, result TEXT NOT NULL);
        ''')

    def close(self):
        self.db.close()

    def validate(self, event, trusted_origin=False):
        if not trusted_origin:
            raise PermissionError('origin not established')
        if set(event) != self.ALLOWED or event['repository'] != 'fixture/team':
            raise ValueError('outside configured repository/schema')
        if event['action'] != 'label-needs-triage' or not isinstance(event['issue_id'], int):
            raise ValueError('action/issue rejected')
        for field in ('event_id', 'delivery_id'):
            if not isinstance(event[field], str) or not re.fullmatch(r'[a-z0-9-]{1,64}', event[field]):
                raise ValueError('bad event identity')
        if not isinstance(event['comment'], str) or len(event['comment']) > 2000:
            raise ValueError('bad comment')
        # Comment is stored neither as a permission grant nor an executable plan.
        key = f"{event['repository']}:{event['issue_id']}:{event['event_id']}:{event['action']}"
        payload = {k: event[k] for k in ('repository', 'issue_id', 'event_id', 'action')}
        digest = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
        return key, digest

    def run(self, event, trusted_origin=False, interrupt=None, provider_available=True):
        key, digest = self.validate(event, trusted_origin)
        if not provider_available:
            return {'state': 'blocked-missing-provider-adapter', 'result': None, 'effect_attempts': 0}
        self.db.execute('BEGIN IMMEDIATE')
        row = self.db.execute('SELECT payload_hash,state,attempts,result FROM jobs WHERE key=?', (key,)).fetchone()
        if row:
            self.db.execute('COMMIT')
            if row[0] != digest:
                raise ValueError('intent key payload conflict')
            return {'state': row[1], 'result': row[3], 'effect_attempts': row[2], 'duplicate': True}
        self.db.execute('INSERT INTO jobs VALUES (?,?,?,0,NULL)', (key, digest, 'claimed'))
        self.db.execute('COMMIT')
        if interrupt == 'after-claim':
            return {'state': 'claimed', 'result': None, 'effect_attempts': 0}
        self.db.execute('UPDATE jobs SET attempts=attempts+1,state=? WHERE key=?', ('unknown', key))
        if interrupt == 'refused-before-effect':
            self.db.execute('UPDATE jobs SET state=? WHERE key=?', ('failed-budget-exhausted', key))
            return {'state': 'failed-budget-exhausted', 'result': None, 'effect_attempts': 1}
        self.db.execute('INSERT INTO provider_effects VALUES (?,?)', (key, 'label-present'))
        if interrupt == 'after-effect':
            return {'state': 'unknown', 'result': None, 'effect_attempts': 1}
        self.db.execute('UPDATE jobs SET state=?,result=? WHERE key=?', ('succeeded', 'label-present', key))
        return {'state': 'succeeded', 'result': 'label-present', 'effect_attempts': 1}

    def reconcile(self, event, trusted_origin=False):
        key, digest = self.validate(event, trusted_origin)
        row = self.db.execute('SELECT payload_hash,state,attempts FROM jobs WHERE key=?', (key,)).fetchone()
        if not row or row[0] != digest:
            raise ValueError('missing/mismatched claim')
        receipt = self.db.execute('SELECT result FROM provider_effects WHERE key=?', (key,)).fetchone()
        if receipt:
            self.db.execute('UPDATE jobs SET state=?,result=? WHERE key=?', ('succeeded', receipt[0], key))
            return 'succeeded-from-readback'
        # This stand-in cannot prove provider absence after an unknown outcome.
        # Claimed-before-effect also requires an owner/recovery decision; no auto takeover.
        return 'blocked-needs-authoritative-readback'


def legacy_slug(value):
    if value is None:
        raise ValueError('slug requires text')
    return '-'.join(value.strip().lower().split())


def slug(value):
    if value is None:
        raise ValueError('slug requires text')
    return '-'.join(value.strip().lower().split())


def configured_format(namespace, config, value):
    return namespace[config['formatter']](value)


def split_claim(state, worker):
    observed = state['owner']
    yield f'{worker}:read:{observed}'
    if observed is None:
        state['owner'] = worker
        state['winners'].append(worker)
        yield f'{worker}:write-owner-and-return-success'
    else:
        yield f'{worker}:return-duplicate'
