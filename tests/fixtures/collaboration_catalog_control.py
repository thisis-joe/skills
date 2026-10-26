"""Test-only reference CLI for falsifying the lifecycle observer.

Tests copy this file into disposable projects. Its private configuration is
never supplied to comparison actors and is not an alternate actor solution.
"""
import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import sqlite3
import sys


def configuration():
    return json.loads(Path(__file__).with_name('_catalog_control.json').read_text())


def connect(path, changed):
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    columns = [row[1] for row in connection.execute('PRAGMA table_info(catalog)')]
    if not changed:
        connection.execute('CREATE TABLE IF NOT EXISTS catalog ('
                           'sku TEXT PRIMARY KEY, name TEXT NOT NULL, '
                           'price_cents INTEGER NOT NULL)')
        return connection
    with connection:
        connection.execute('BEGIN')
        if columns and 'supplier' not in columns:
            connection.execute('ALTER TABLE catalog RENAME TO old_catalog')
        connection.execute('CREATE TABLE IF NOT EXISTS catalog ('
                           'supplier TEXT NOT NULL, sku TEXT NOT NULL, '
                           'name TEXT NOT NULL, price_cents INTEGER NOT NULL, '
                           'PRIMARY KEY (supplier, sku))')
        if columns and 'supplier' not in columns:
            connection.execute('INSERT INTO catalog '
                               "SELECT 'legacy', sku, name, price_cents FROM old_catalog")
            connection.execute('DROP TABLE old_catalog')
        connection.execute('CREATE TABLE IF NOT EXISTS batches ('
                           'supplier TEXT NOT NULL, batch_id TEXT NOT NULL, '
                           'digest TEXT NOT NULL, PRIMARY KEY (supplier, batch_id))')
    return connection


def canonical(raw, profile, fault):
    fold = profile['identity'] == 'fold'
    if fault == 'identity':
        fold = not fold
    return raw.strip().lower() if fold else raw.strip()


def read_rows(source, profile, fault):
    reader = csv.DictReader(io.StringIO(source.decode('utf-8')))
    if reader.fieldnames != ['sku', 'name', 'price_cents']:
        raise ValueError('CSV needs sku,name,price_cents headers')
    selected = {}
    skipped = 0
    for row in reader:
        try:
            if None in row or any(row[key] is None for key in reader.fieldnames):
                raise ValueError('wrong number of columns')
            sku = canonical(row['sku'], profile, fault)
            name = row['name'].strip()
            amount = int(row['price_cents'])
            if not sku or not name or amount < 0:
                raise ValueError('invalid SKU, name or price')
        except (ValueError, TypeError):
            if profile['invalid'] == 'atomic':
                raise ValueError('malformed row; import rejected') from None
            skipped += 1
            continue
        if sku in selected:
            if profile['collision'] == 'error':
                raise ValueError('duplicate SKU in input')
            if profile['collision'] == 'first':
                continue
        selected[sku] = (name, amount)
    if skipped:
        print('Skipped %d malformed rows' % skipped, file=sys.stderr)
    return selected


def import_rows(connection, args, config):
    profile, phase = config['profile'], config['phase']
    changed = phase != 'initial'
    fault = config.get('fault')
    source = Path(args.path).read_bytes()
    supplier, batch_id = args.supplier, args.batch_id
    digest = hashlib.sha256(source).hexdigest()
    if changed and batch_id is not None:
        previous = connection.execute(
            'SELECT digest FROM batches WHERE supplier = ? AND batch_id = ?',
            (supplier, batch_id)).fetchone()
        if previous:
            if previous['digest'] != digest:
                raise ValueError('batch ID conflicts with previous contents')
            if fault != 'replay':
                return
    selected = read_rows(source, profile, fault)
    with connection:
        for sku, (name, amount) in selected.items():
            if changed:
                connection.execute(
                    'INSERT INTO catalog VALUES (?, ?, ?, ?) '
                    'ON CONFLICT(supplier, sku) DO UPDATE SET '
                    'name = excluded.name, price_cents = excluded.price_cents',
                    (supplier, sku, name, amount))
            else:
                exists = connection.execute(
                    'SELECT 1 FROM catalog WHERE sku = ?', (sku,)).fetchone()
                if exists and profile['collision'] == 'error':
                    raise ValueError('SKU collides with existing catalog')
                if exists and profile['collision'] == 'first':
                    continue
                connection.execute('INSERT INTO catalog VALUES (?, ?, ?) '
                                   'ON CONFLICT(sku) DO UPDATE SET '
                                   'name = excluded.name, price_cents = excluded.price_cents',
                                   (sku, name, amount))
        if changed and batch_id is not None:
            connection.execute('INSERT OR IGNORE INTO batches VALUES (?, ?, ?)',
                               (supplier, batch_id, digest))


def summary(connection, config):
    exclude = config['profile']['report'] == 'exclude-zero'
    if config.get('fault') == 'summary':
        exclude = not exclude
    condition = ' WHERE price_cents > 0' if exclude else ''
    rows = connection.execute('SELECT supplier, COUNT(*) AS count, '
                              'SUM(price_cents) AS total_cents FROM catalog' +
                              condition + ' GROUP BY supplier ORDER BY supplier')
    return [dict(row) for row in rows]


def main():
    config = configuration()
    parser = argparse.ArgumentParser()
    parser.add_argument('--db', required=True)
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('list')
    importer = commands.add_parser('import')
    importer.add_argument('path')
    importer.add_argument('--supplier', default='legacy')
    importer.add_argument('--batch-id')
    commands.add_parser('summary')
    args = parser.parse_args()
    connection = connect(args.db, config['phase'] != 'initial')
    try:
        if args.command == 'import':
            import_rows(connection, args, config)
            print(json.dumps({'imported': True}))
        elif args.command == 'list':
            order = 'supplier, sku' if config['phase'] != 'initial' else 'sku'
            rows = connection.execute('SELECT * FROM catalog ORDER BY ' + order)
            print(json.dumps([dict(row) for row in rows]))
        else:
            print(json.dumps(summary(connection, config)))
    except (ValueError, OSError, UnicodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    finally:
        connection.close()
    return 0


if __name__ == '__main__':
    sys.exit(main())
