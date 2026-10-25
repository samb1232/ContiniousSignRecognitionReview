#!/usr/bin/env python3
"""Budgeted OpenAlex retrieval, immutable runs and offline exports (stdlib only).

Usage: python3 work/scripts/retrieve.py --stage pilot
       python3 work/scripts/retrieve.py --stage full --reuse work/runs/RUN
       python3 work/scripts/retrieve.py --resume work/runs/RUN
       python3 work/scripts/retrieve.py --export work/runs/RUN
"""
import argparse
import csv
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
from email.utils import parsedate_to_datetime

ROOT = Path(__file__).resolve().parents[2]
RUNS = ROOT / 'work/runs'

def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()

def read(path):
    return json.loads(Path(path).read_text())

def save(path, value):
    path = Path(path)
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')
    temp.replace(path)

def key():
    env = ROOT / '.env'
    if env.exists():
        for line in env.read_text().splitlines():
            if line.strip().startswith('OPENALEX_API_KEY='):
                os.environ.setdefault('OPENALEX_API_KEY', line.split('=', 1)[1].strip().strip('\"\''))
    value = os.environ.get('OPENALEX_API_KEY')
    if not value:
        raise RuntimeError('OPENALEX_API_KEY is missing')
    return value

def total_reserved():
    return sum(read(p).get('credits_reserved', 0) for p in RUNS.glob('*/manifest.json'))

def headers_safe(headers):
    return {k.lower(): v for k, v in headers.items() if k.lower().startswith('x-ratelimit') or k.lower() in ('retry-after', 'content-type')}

def allowance(data):
    # API has used both top-level and rate_limit-wrapped responses.
    body = data.get('rate_limit', data)
    for field in ('credits_remaining', 'remaining_credits', 'remaining'):
        if field in body and isinstance(body[field], (int, float)):
            return float(body[field])
    raise RuntimeError('Cannot establish remaining account credits; inspect sanitized preflight schema')

def request(run, manifest, endpoint, params, secret, cost, account_remaining=None):
    cfg = read(run / 'config.json')
    attempts = cfg['max_attempts'] if cost else 1
    for retry in range(attempts):
        if total_reserved() + cost > cfg['task_budget_credits']:
            raise RuntimeError('task_budget_exhausted')
        if cost and (account_remaining is None or account_remaining < cost):
            raise RuntimeError('account_budget_exhausted_or_unknown')
        index = len(manifest['requests']) + 1
        record = {'index': index, 'utc': now(), 'endpoint': endpoint, 'params': params,
                  'reserved_credits': cost, 'attempt': retry + 1, 'outcome': 'pending'}
        manifest['requests'].append(record)
        manifest['credits_reserved'] += cost
        save(run / 'manifest.json', manifest)  # durable reservation before network
        url = 'https://api.openalex.org' + endpoint + '?' + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers={'Authorization': 'Bearer ' + secret,
                                                  'User-Agent': 'CSLRReview/1.0'})
        response_headers = {}
        try:
            with urllib.request.urlopen(req, timeout=cfg['timeout_seconds']) as response:
                raw = response.read()
                status = response.status
                response_headers = headers_safe(response.headers)
        except urllib.error.HTTPError as exc:
            raw, status = exc.read(), exc.code
            response_headers = headers_safe(exc.headers)
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            # Never print exception text: it may contain credentials or request details.
            raw, status = b'', None
            record['error_class'] = type(exc).__name__
        # If a service echoes a key, do not persist that body; explicitly record omission.
        if secret.encode() in raw:
            record['body_omitted'] = 'credential_echo'
        else:
            filename = f'raw/{index:04d}.json'
            (run / filename).write_bytes(raw)
            record['body'] = filename
            record['sha256'] = hashlib.sha256(raw).hexdigest()
        record.update(status=status, headers=response_headers,
                      outcome='success' if status == 200 else 'failed', finished_utc=now())
        save(run / 'manifest.json', manifest)
        if status == 200:
            return json.loads(raw), record
        if status not in (None, 429, 500, 502, 503, 504) or retry + 1 == attempts:
            raise RuntimeError(f'API_access_failure_status_{status}')
        if cost:
            account_remaining -= cost  # conservative debit for unknown failed outcomes
        delay = 2 ** retry
        retry_after = response_headers.get('retry-after')
        if retry_after:
            try:
                delay = max(delay, float(retry_after))
            except ValueError:
                delay = max(delay, (parsedate_to_datetime(retry_after) - dt.datetime.now(dt.timezone.utc)).total_seconds())
        if delay > 60:
            raise RuntimeError('retry_after_exceeds_60_seconds_resume_later')
        record['retry_delay_seconds'] = delay
        save(run / 'manifest.json', manifest)
        time.sleep(delay)

def export(run):
    manifest = read(run / 'manifest.json')
    by_id, doi_ids = {}, {}
    pages = []
    for qid, state in manifest['queries'].items():
        for page in state['pages']:
            payload = read(run / page['body'])
            pages.append((qid, page, payload))
            for work in payload['results']:
                wid = work['id']
                if wid not in by_id:
                    by_id[wid] = {'work': work, 'provenance': [], 'metadata_conflicts': []}
                elif any(by_id[wid]['work'].get(k) != work.get(k) for k in ('doi','display_name','publication_date')):
                    by_id[wid]['metadata_conflicts'].append({'query': qid, 'body': page['body']})
                by_id[wid]['provenance'].append({'run': page.get('origin_run', run.name), 'query': qid,
                                                'body': page['body'], 'cursor': page['cursor']})
    for wid, item in by_id.items():
        doi = (item['work'].get('doi') or '').lower().removeprefix('https://doi.org/').removeprefix('http://doi.org/').removeprefix('doi:').strip().rstrip('/')
        item['normalized_doi'] = doi or None
        if doi:
            doi_ids.setdefault(doi, []).append(wid)
    # DOI aliases are grouped, not silently dropped; conflicts need explicit adjudication.
    groups = []
    seen = set()
    for wid, item in by_id.items():
        if wid in seen:
            continue
        ids = doi_ids.get(item['normalized_doi'], [wid]) if item['normalized_doi'] else [wid]
        seen.update(ids)
        item['aliases'] = [other for other in ids if other != wid]
        groups.append(item)
    save(run / 'works.json', groups)
    with (run / 'works.csv').open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=['id','doi','title','publication_date','type','is_oa','oa_url','query_ids','aliases'])
        writer.writeheader()
        for item in groups:
            w = item['work']; oa = w.get('open_access') or {}
            writer.writerow(dict(id=w['id'], doi=w.get('doi') or 'not_reported', title=w['display_name'],
                publication_date=w['publication_date'], type=w['type'], is_oa=oa.get('is_oa'),
                oa_url=oa.get('oa_url') or 'not_reported', query_ids='|'.join(sorted({p['query'] for p in item['provenance']})), aliases='|'.join(item['aliases'])))
    counts = {'retrieved_occurrences': sum(len(p['results']) for _, _, p in pages),
              'unique_openalex_ids': len(by_id), 'unique_after_doi_grouping': len(groups),
              'doi_conflicts': {doi: ids for doi, ids in doi_ids.items() if len(ids) > 1},
              'metadata_conflicts': sum(bool(i['metadata_conflicts']) for i in by_id.values()),
              'per_query': {qid: {'retrieved': sum(len(read(run / p['body'])['results']) for p in state['pages']),
                                'reported_total': state.get('total'), 'complete': state['complete']}
                            for qid, state in manifest['queries'].items()}}
    save(run / 'counts.json', counts)
    return counts

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage', choices=['pilot','full'], default='pilot')
    parser.add_argument('--reuse', type=Path)
    parser.add_argument('--resume', type=Path)
    parser.add_argument('--export', type=Path)
    args = parser.parse_args()
    if args.export:
        print(json.dumps(export(args.export), indent=2)); return
    cfg = read(ROOT / 'work/queries.json')
    secret = key()
    RUNS.mkdir(parents=True, exist_ok=True)
    # Serialize collectors so cumulative task reservations cannot race.
    import fcntl
    lock = (RUNS / '.collection.lock').open('a')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    if args.resume:
        run = args.resume
        if read(run / 'config.json') != cfg:
            raise RuntimeError('Resume configuration differs')
        manifest = read(run / 'manifest.json')
        if manifest['status'] == 'complete':
            raise RuntimeError('Completed runs are immutable')
        args.stage = manifest['stage']
        manifest['events'].append({'event': 'resume', 'utc': now()})
    else:
        run = RUNS / (dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ') + '-' + args.stage)
        (run / 'raw').mkdir(parents=True)
        save(run / 'config.json', cfg)
        (run / 'source').mkdir()
        for path in [Path(__file__), ROOT / 'protocol.md', ROOT / 'work/decisions.md']:
            shutil.copyfile(path, run / 'source' / path.name)
        git = subprocess.run(['git','rev-parse','HEAD'], cwd=ROOT, capture_output=True, text=True)
        manifest = {'run_id': run.name, 'stage': args.stage, 'started_utc': now(), 'status': 'running',
                    'task_budget_credits': cfg['task_budget_credits'], 'credits_reserved': 0,
                    'code_version': git.stdout.strip() or 'uncommitted', 'python': platform.python_version(),
                    'dependencies': 'Python standard library only', 'requests': [], 'events': [],
                    'queries': {q['id']: {'pages': [], 'complete': False, 'cursor': '*'} for q in cfg['queries']}}
        if args.reuse:
            if read(args.reuse / 'config.json') != cfg:
                raise RuntimeError('Reuse configuration differs')
            parent = read(args.reuse / 'manifest.json')
            manifest['parent_run'] = args.reuse.name
            for qid, state in parent['queries'].items():
                for n, page in enumerate(state['pages']):
                    dest = f'raw/reused-{qid}-{n}.json'
                    shutil.copyfile(args.reuse / page['body'], run / dest)
                    manifest['queries'][qid]['pages'].append({**page, 'body': dest, 'origin_run': page.get('origin_run', args.reuse.name)})
                manifest['queries'][qid].update({k: v for k, v in state.items() if k != 'pages'})
    save(run / 'manifest.json', manifest)
    print('Run:', run.relative_to(ROOT), flush=True)
    try:
        data, record = request(run, manifest, '/rate-limit', {}, secret, 0)
        remaining = allowance(data)
        manifest['account_remaining_at_start'] = remaining
        save(run / 'manifest.json', manifest)
        for query in cfg['queries']:
            state = manifest['queries'][query['id']]
            while not state['complete']:
                if args.stage == 'pilot' and len(state['pages']) >= 1:
                    break
                params = {**cfg['common_params'], **query['params'], 'cursor': state['cursor']}
                payload, record = request(run, manifest, '/works', params, secret, cfg['search_cost_credits'], remaining)
                if 'body' not in record:
                    raise RuntimeError('Response body unavailable')
                results, meta = payload['results'], payload['meta']
                state['pages'].append({'body': record['body'], 'cursor': state['cursor'], 'sha256': record['sha256']})
                state['total'] = meta['count']
                next_cursor = meta.get('next_cursor')
                state['complete'] = not results or next_cursor is None
                if not state['complete'] and next_cursor == state['cursor']:
                    raise RuntimeError('Repeated cursor')
                state['cursor'] = next_cursor
                hremaining = record['headers'].get('x-ratelimit-remaining')
                remaining = min(remaining - cfg['search_cost_credits'], float(hremaining)) if hremaining else remaining - cfg['search_cost_credits']
                save(run / 'manifest.json', manifest)
                print(query['id'], len(results), 'of', meta['count'], 'complete=', state['complete'], flush=True)
                time.sleep(cfg['minimum_interval_seconds'])
        manifest['status'] = 'complete' if all(s['complete'] for s in manifest['queries'].values()) else 'pilot_limited'
    except Exception as exc:
        manifest['status'] = 'stopped'
        manifest['stop_reason'] = str(exc) if isinstance(exc, RuntimeError) else type(exc).__name__
        print('Stopped:', manifest['stop_reason'], flush=True)
    finally:
        manifest['finished_utc'] = now()
        manifest['task_credits_reserved_at_finish'] = total_reserved()
        save(run / 'manifest.json', manifest)
        print(json.dumps(export(run), indent=2))

if __name__ == '__main__':
    main()
