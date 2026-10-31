#!/usr/bin/env python3
"""Rebuild merged corpus, screening exports, counts, and comparison from saved inputs.

Usage: python3 work/scripts/report.py
No network. Manual inputs: analysis_config.json, screening.json, evidence.json.
"""
import csv
from collections import Counter
import json
from pathlib import Path
from screening_report import build_reports
from analysis_selection import selected_queries

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
        selected = selected_queries(config, runid, counts['per_query'])
        for qid, state in counts['per_query'].items():
            if qid not in selected:
                continue
            queries.append({'run':runid,'role':role,'query':qid,**state})
            if role == 'discovery': occurrences += state['retrieved']
        for item in read(folder / 'works.json'):
            provenance = [p for p in item['provenance'] if p['query'] in selected]
            if not provenance:
                continue
            wid = item['work']['id'].split('/')[-1]
            if wid not in corpus:
                corpus[wid] = {**item, 'provenance': provenance, 'discovery_routes': []}
            else:
                corpus[wid]['provenance'].extend(provenance)
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
    build_reports(screening['records'], corpus)
    reserved = sum(read(p).get('credits_reserved',0) for p in (WORK / 'runs').glob('*/manifest.json'))
    observed = sum(float(r['headers'].get('x-ratelimit-credits-used',0))
                   for p in (WORK / 'runs').glob('*/manifest.json') for r in read(p)['requests'] if r.get('outcome') == 'success')
    counts = {'discovery_occurrences':occurrences,
              'discovery_unique':sum(any(r['role']=='discovery' for r in i['discovery_routes']) for i in corpus.values()),
              'screened_unique_including_verification':len(corpus),
              'ai_decisions':dict(Counter(row['ai_decision'] for row in rows.values())),
              'human_decisions':dict(Counter(row['human_decision'] for row in rows.values())),
              'by_stage':dict(Counter(row['stage'] for row in rows.values())),
              'ai_by_stage':{stage:dict(Counter(r['ai_decision'] for r in rows.values() if r['stage']==stage))
                             for stage in sorted({r['stage'] for r in rows.values()})},
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
    lines = ['# CSLR search and screening report', '',
             f"{len(rows)} candidates. AI decisions are proposals; manual decisions remain independent.", '']
    for stage, decisions in counts['ai_by_stage'].items():
        lines.append(f"- {stage.replace('_', ' ')}: " + ', '.join(f'{n} {v}' for v,n in decisions.items()))
    lines += ['', 'Manual decisions: '+', '.join(f'{n} {v}' for v,n in counts['human_decisions'].items()), '',
              'See the [HTML report](../html-report/index.html) for candidates, individual reports, exact retrieval filters and M1–M3.']
    (WORK / 'report.md').write_text('\n'.join(lines)+'\n')
    from html_report import main as build_html
    build_html()
    print(json.dumps({k:v for k,v in counts.items() if k!='query_counts'},indent=2))

if __name__=='__main__':main()
