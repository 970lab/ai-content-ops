#!/usr/bin/env python3
"""Offline consistency checks; never dereferences evidence references."""
import argparse
from datetime import datetime, timezone
import json
import math
from pathlib import Path

LAYERS = ('source', 'checks', 'delivery', 'access', 'experience', 'record')


def timestamp(value):
    if not isinstance(value, str):
        raise ValueError('timestamp must be a string')
    value = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if value.tzinfo is None:
        raise ValueError('timestamp requires timezone')
    return value


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def validate(packet, now=None, max_age_hours=24):
    errors = []
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None or not math.isfinite(max_age_hours) or max_age_hours <= 0:
        return {'outcome': 'blocker', 'errors': ['invalid review clock or freshness window']}
    if not isinstance(packet, dict) or packet.get('schema_version') != 1:
        return {'outcome': 'blocker', 'errors': ['expected schema_version 1 object']}
    if packet.get('claim') == 'none':
        valid = nonempty(packet.get('reason')) and packet.get('evidence') == {}
        return {'outcome': 'no_candidate' if valid else 'blocker',
                'errors': [] if valid else ['no-claim requires reason and empty evidence']}
    if packet.get('claim') != 'delivery':
        errors.append('claim must be delivery or none')
    for field in ('project', 'revision'):
        if not nonempty(packet.get(field)):
            errors.append('missing ' + field)
    if packet.get('audience') not in ('local', 'public'):
        errors.append('audience must be local or public')
    rows = packet.get('evidence')
    if not isinstance(rows, dict):
        rows = {}
        errors.append('evidence must be an object')
    if set(rows) != set(LAYERS):
        errors.append('evidence must contain exactly the six required layers')
    for layer in LAYERS:
        row = rows.get(layer)
        if not isinstance(row, dict):
            errors.append(layer + ': missing evidence object')
            continue
        for field in ('project', 'revision'):
            if row.get(field) != packet.get(field):
                errors.append(layer + ': mismatched ' + field)
        if row.get('result') != 'observed':
            errors.append(layer + ': result is not observed')
        if not nonempty(row.get('ref')):
            errors.append(layer + ': missing evidence ref')
        try:
            age = (now - timestamp(row.get('observed_at'))).total_seconds() / 3600
            if age < 0 or age > max_age_hours:
                errors.append(layer + ': future or stale observation')
        except (ValueError, TypeError, OverflowError):
            errors.append(layer + ': invalid observation timestamp')
        if layer == 'access' and row.get('surface') != packet.get('audience'):
            errors.append('access: evidence surface does not match audience')
        if layer == 'experience':
            negative = row.get('negative_path')
            valid_negative = (negative == 'observed' and nonempty(row.get('negative_ref')))
            scoped_out = (negative == 'not-applicable' and nonempty(row.get('negative_reason')))
            if not (valid_negative or scoped_out):
                errors.append('experience: missing negative-path check or scoped reason')
        if layer == 'record':
            issues = row.get('remaining_issues')
            if not isinstance(issues, list) or any(not nonempty(item) for item in issues):
                errors.append('record: remaining_issues must be an explicit list')
            elif issues:
                errors.append('record: unresolved remaining issues require review')
    return {'outcome': 'blocker' if errors else 'candidate', 'errors': errors}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('packet')
    parser.add_argument('--now', help='timezone-aware replay clock, not current evidence')
    parser.add_argument('--max-age-hours', type=float, default=24)
    args = parser.parse_args()
    try:
        with Path(args.packet).open('rb') as stream:
            raw = stream.read(1048577)
        if len(raw) > 1048576:
            raise ValueError('packet exceeds 1 MiB')
        packet = json.loads(raw)
        result = validate(packet, timestamp(args.now) if args.now else None, args.max_age_hours)
    except (OSError, ValueError, TypeError, RecursionError):
        result = {'outcome': 'blocker', 'errors': ['cannot parse packet or review clock']}
    print(json.dumps(result, sort_keys=True))
    return 1 if result['outcome'] == 'blocker' else 0


if __name__ == '__main__':
    raise SystemExit(main())
