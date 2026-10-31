#!/usr/bin/env python3
"""Rebuild merged corpus, screening exports, counts, and comparison from saved inputs.

Usage: python3 work/scripts/report.py
No network. Manual inputs: analysis_config.json, screening.json, evidence.json.
"""
import csv
from collections import Counter
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT / 'work'

def read(path): return json.loads(path.read_text())
def save(path, data): path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')
def cell(value): return str(value).replace('|', '\\|').replace('\n', ' ')

def main():
    config = read(WORK / 'analysis_config.json')
    corpus = {}; occurrences = 0; queries = []; statuses = []
    for runid in config['search_runs'] + config['verification_runs']:
        folder = WORK / 'runs' / runid
        manifest = read(folder / 'manifest.json'); statuses.append(manifest['status'])
        counts = read(folder / 'counts.json')
        role = 'discovery' if runid in config['search_runs'] else 'targeted DOI verification'
        if role == 'discovery': occurrences += counts['retrieved_occurrences']
        for qid, state in counts['per_query'].items():
            queries.append({'run':runid,'role':role,'query':qid,**state})
        for item in read(folder / 'works.json'):
            wid = item['work']['id'].split('/')[-1]
            if wid not in corpus:
                corpus[wid] = {**item, 'discovery_routes': []}
            else:
                corpus[wid]['provenance'].extend(item['provenance'])
            corpus[wid]['discovery_routes'].append({'run':runid,'role':role})
    # Cross-run DOI grouping is explicit and must be adjudicated if conflicting.
    dois = {}
    for wid, item in corpus.items():
        if item['normalized_doi']: dois.setdefault(item['normalized_doi'], []).append(wid)
    conflicts = {doi:ids for doi,ids in dois.items() if len(ids)>1}
    if conflicts: raise ValueError('Cross-run DOI conflicts require a merge decision: ' + str(conflicts))
    screening = read(WORK / 'screening.json')
    rows = {row['openalex_id']:row for row in screening['records']}
    if set(rows) != set(corpus): raise ValueError('Screening records do not match saved corpus')
    evidence = read(WORK / 'evidence.json')
    assertions = {item['openalex_id']:item for item in evidence['reviews']}
    for wid, row in rows.items():
        if row['ai_decision'] == 'include' and wid not in assertions:
            raise ValueError('Included review lacks evidence: ' + wid)
    reserved = sum(read(p).get('credits_reserved',0) for p in (WORK / 'runs').glob('*/manifest.json'))
    observed = sum(float(r['headers'].get('x-ratelimit-credits-used',0))
                   for p in (WORK / 'runs').glob('*/manifest.json') for r in read(p)['requests'] if r.get('outcome') == 'success')
    counts = {'discovery_occurrences':occurrences,
              'discovery_unique':sum(any(r['role']=='discovery' for r in i['discovery_routes']) for i in corpus.values()),
              'screened_unique_including_verification':len(corpus),
              'ai_decisions':dict(Counter(row['ai_decision'] for row in rows.values())),
              'human_decisions':dict(Counter(row['human_decision'] for row in rows.values())),
              'by_stage':dict(Counter(row['stage'] for row in rows.values())),
              'search_runs_complete':all(status=='complete' for status in statuses),
              'task_budget_credits':300, 'credits_reserved':reserved,'observed_successful_credits':observed,
              'query_counts':queries,'cross_run_doi_conflicts':conflicts}
    save(WORK / 'corpus.json', list(corpus.values())); save(WORK / 'summary.json', counts)
    fields=['openalex_id','title','ai_decision','human_decision','stage','evidence_level','reason','source_ids']
    with (WORK / 'screening.csv').open('w',newline='') as handle:
        writer=csv.DictWriter(handle, fieldnames=fields);writer.writeheader()
        for wid, row in rows.items():
            writer.writerow({**{f:row.get(f,'not_checked') for f in fields},'title':corpus[wid]['work']['display_name'],
                             'source_ids':'|'.join(row['source_ids'])})
    (WORK / 'report.md').write_text('# CSLR search and screening report\n\n34 candidates; AI and manual screening: Not screened. See [HTML report](../html-report/index.html) for exact retrieval filters and M1–M3.\n')
    from html_report import main as build_html
    build_html()
    print(json.dumps({k:v for k,v in counts.items() if k!='query_counts'},indent=2))

if __name__=='__main__':main()
