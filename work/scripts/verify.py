#!/usr/bin/env python3
"""Verify raw-response integrity, pagination, exports and screening reconciliation offline.

Usage: python3 work/scripts/verify.py
"""
import hashlib
import json
from pathlib import Path
import sys
import csv
import re
from collections import Counter
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from retrieve import export
from analysis_selection import selected_queries

ROOT=Path(__file__).resolve().parents[2]

class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=[]; self.links=[]
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if 'id' in attrs:self.ids.append(attrs['id'])
        if 'href' in attrs:self.links.append(attrs['href'])

def verify_screening():
    from screening_report import build_reports
    records=json.loads((ROOT/'work/screening.json').read_text())['records']
    corpus={i['work']['id'].split('/')[-1]:i for i in json.loads((ROOT/'work/corpus.json').read_text())}
    analysis=json.loads((ROOT/'work/analysis_config.json').read_text())
    expected=analysis['expected_candidate_count']
    assert len(records)==len(corpus)==expected
    assert len({r['openalex_id'] for r in records})==expected
    assert {r['openalex_id'] for r in records}==set(corpus)
    assert all(r['human_decision']=='not_screened' for r in records)
    build_reports(records, corpus, check=True)
    summary=json.loads((ROOT/'work/summary.json').read_text())
    assert summary['ai_decisions']==dict(Counter(r['ai_decision'] for r in records))
    for stage, decisions in summary['ai_by_stage'].items():
        assert decisions==dict(Counter(r['ai_decision'] for r in records if r['stage']==stage))
    rows=list(csv.DictReader((ROOT/'work/screening.csv').open()))
    assert len(rows)==expected
    by_id={r['openalex_id']:r for r in records}
    for row in rows:
        assert all(row[k]==by_id[row['openalex_id']][k] for k in ('stage','ai_decision','human_decision'))
    page=ROOT/'html-report/index.html'; parser=Links(); parser.feed(page.read_text())
    assert len(parser.ids)==len(set(parser.ids)), 'Duplicate HTML anchors'
    def check_link(url, base):
        parts=urlsplit(url)
        if parts.scheme or parts.netloc:return
        target=(base.parent/unquote(parts.path)).resolve() if parts.path else base
        assert target.is_file(), f'Broken link: {url} in {base}'
        if parts.fragment and target==page:
            assert parts.fragment in parser.ids, f'Broken anchor: {url}'
    for url in parser.links:check_link(url,page)
    for md in (ROOT/'html-report/support/papers').glob('*.md'):
        for url in re.findall(r'\]\(([^)]+)\)',md.read_text()):check_link(url,md)
    print(f'PASS: {expected} screening records and concise paper reports; decisions, evidence, counts and local links agree.')

def verify_selection():
    """Reconcile the active corpus and route provenance against selected raw pages."""
    work=ROOT/'work'
    analysis=json.loads((work/'analysis_config.json').read_text())
    corpus=json.loads((work/'corpus.json').read_text())
    expected_ids=set(); expected_routes={}; counts={}; occurrences=0
    for runid in analysis['search_runs'] + analysis['verification_runs']:
        run=work/'runs'/runid
        manifest=json.loads((run/'manifest.json').read_text())
        for qid in selected_queries(analysis, runid, manifest['queries']):
            ids=[r['id'] for p in manifest['queries'][qid]['pages']
                 for r in json.loads((run/p['body']).read_text())['results']]
            counts[(runid,qid)]=len(ids)
            expected_ids.update(ids)
            for wid in ids: expected_routes.setdefault(wid,set()).add(qid)
            if runid in analysis['search_runs']: occurrences+=len(ids)
    actual_ids={wid for i in corpus for wid in [i['work']['id']]+i['aliases']}
    assert actual_ids==expected_ids, 'Active corpus differs from selected raw results'
    for i in corpus:
        routes=set().union(*(expected_routes.get(wid,set()) for wid in [i['work']['id']]+i['aliases']))
        assert {p['query'] for p in i['provenance']}==routes
    summary=json.loads((work/'summary.json').read_text())
    assert summary['discovery_occurrences']==occurrences
    assert {(q['run'],q['query']):q['retrieved'] for q in summary['query_counts']}==counts
    print('PASS: Active query counts, corpus and provenance match selected saved responses.')

def main():
    checked=0
    for run in sorted((ROOT/'work/runs').glob('*')):
        if not (run/'manifest.json').exists():continue
        m=json.loads((run/'manifest.json').read_text())
        cfg=json.loads((run/'config.json').read_text())
        assert m['credits_reserved']==sum(r['reserved_credits'] for r in m['requests'])
        for r in m['requests']:
            if r.get('body'):
                assert hashlib.sha256((run/r['body']).read_bytes()).hexdigest()==r['sha256']
        before=(run/'works.json').read_bytes(),(run/'works.csv').read_bytes(),(run/'counts.json').read_bytes()
        counts=export(run)
        assert before==((run/'works.json').read_bytes(),(run/'works.csv').read_bytes(),(run/'counts.json').read_bytes())
        exported=json.loads((run/'works.json').read_text())
        actual_ids={w['id'] for state in m['queries'].values() for p in state['pages']
                    for w in json.loads((run/p['body']).read_text())['results']}
        exported_ids={i for item in exported for i in [item['work']['id']]+item['aliases']}
        assert actual_ids==exported_ids
        for item in exported:
            for provenance in item['provenance']:
                response_ids={w['id'] for w in json.loads((run/provenance['body']).read_text())['results']}
                assert response_ids.intersection({item['work']['id'],*item['aliases']})
        for qid,state in m['queries'].items():
            seen=set(); previous='*'; ids=[]
            for p in state['pages']:
                assert p['cursor']==previous
                assert p['cursor'] not in seen
                seen.add(p['cursor'])
                raw=(run/p['body']).read_bytes()
                assert hashlib.sha256(raw).hexdigest()==p['sha256']
                data=json.loads(raw);previous=data['meta'].get('next_cursor')
                ids.extend(w['id'] for w in data['results'])
            assert len(ids)==len(set(ids)),f'Pagination duplicated IDs in {qid}'
            if state['complete']:
                assert state['pages']
                assert previous is None or not data['results']
                assert len(ids)==state['total'],f'Count disagreement in {qid}'
            for page in state['pages']:
                for w in json.loads((run/page['body']).read_text())['results']:
                    date=w['publication_date']
                    if 'from_publication_date:' in cfg['common_params'].get('filter',''):
                        assert '2020-01-01'<=date<='2026-10-25'
        checked+=1
    summary=json.loads((ROOT/'work/summary.json').read_text())
    assert summary['credits_reserved']<=summary['task_budget_credits']
    assert sum(summary['ai_decisions'].values())==summary['screened_unique_including_verification']
    assert sum(summary['human_decisions'].values())==summary['screened_unique_including_verification']
    for path in (ROOT/'work/sources').glob('*.json'):
        d=json.loads(path.read_text())
        if d.get('body'):assert hashlib.sha256((path.parent/d['body']).read_bytes()).hexdigest()==d['sha256']
    from html_report import main as check_html
    check_html(check=True)
    verify_selection()
    verify_screening()
    (ROOT/'work/verification.json').write_text(json.dumps({
        'status':'passed', 'checks':'Saved runs, source hashes, screening records, paper reports, HTML and local links',
        'candidate_count':summary['screened_unique_including_verification'],
        'ai_by_stage':summary['ai_by_stage'], 'human_decisions':summary['human_decisions']
    }, indent=2)+'\n')
    print(f'PASS: {checked} runs; raw hashes, cursor termination, query counts, offline exports, source hashes, budget and screening reconciliation.')

if __name__=='__main__':main()
