#!/usr/bin/env python3
"""Generate a standalone, printable search-methods report from saved research inputs.

Usage: python3 work/scripts/html_report.py
       python3 work/scripts/html_report.py --check
Writes html-report/index.html and html-report/search-data.json. No network,
third-party packages, or manual duplication of result counts is required.
The main report.py pipeline rebuilds this page automatically.
"""
from collections import Counter
from html import escape
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT / 'work'
OUT = ROOT / 'html-report'


def read(path):
    return json.loads(path.read_text())


def h(value):
    return escape(str(value), quote=True)


def link(url, label):
    return f'<a href="{h(url)}">{h(label)}</a>'


def table(headers, rows, caption):
    return ('<div class="table-wrap"><table><caption>' + h(caption) + '</caption><thead><tr>'
            + ''.join(f'<th scope="col">{h(x)}</th>' for x in headers)
            + '</tr></thead><tbody>'
            + ''.join('<tr>' + ''.join(f'<td>{cell}</td>' for cell in row) + '</tr>' for row in rows)
            + '</tbody></table></div>')


def main(check=False):
    analysis = read(WORK / 'analysis_config.json')
    summary = read(WORK / 'summary.json')
    screening = read(WORK / 'screening.json')
    records = screening['records']
    corpus = {x['work']['id'].rsplit('/', 1)[-1]: x for x in read(WORK / 'corpus.json')}
    evidence = {x['openalex_id']: x for x in read(WORK / 'evidence.json')['reviews']}
    ai = Counter(r['ai_decision'] for r in records)
    human = Counter(r['human_decision'] for r in records)
    assert len(records) == len(corpus) == summary['screened_unique_including_verification']
    assert dict(ai) == summary['ai_decisions'], 'Rebuild summary with report.py first'
    assert dict(human) == summary['human_decisions'], 'Rebuild summary with report.py first'
    stages = Counter((r['stage'], r['ai_decision']) for r in records)
    queries = []
    manifests = {}
    for runid in analysis['search_runs'] + analysis['verification_runs']:
        run = WORK / 'runs' / runid
        config = read(run / 'config.json')
        manifest = read(run / 'manifest.json')
        manifests[runid] = manifest
        for query in config['queries']:
            state = manifest['queries'][query['id']]
            params = {**config['common_params'], **query['params']}
            query_count = next(c for c in summary['query_counts']
                               if c['run'] == runid and c['query'] == query['id'])
            assert query_count['retrieved'] == sum(len(read(run / p['body'])['results']) for p in state['pages'])
            queries.append({'id': query['id'], 'run': runid, 'params': params,
                            'pages': len(state['pages']), 'retrieved': query_count['retrieved'],
                            'reported_total': state['total'], 'complete': state['complete'],
                            'cursor_start': '*',
                            'role': 'discovery' if runid in analysis['search_runs'] else 'DOI verification'})
    discovery = [q for q in queries if q['role'] == 'discovery']
    main_queries = [q for q in discovery if not q['id'].startswith('s')]
    sensitivity = [q for q in discovery if q['id'].startswith('s')]
    main_occurrences = sum(q['retrieved'] for q in main_queries)
    sensitivity_occurrences = sum(q['retrieved'] for q in sensitivity)
    main_run_ids = {q['run'] for q in main_queries}
    sensitivity_run_ids = {q['run'] for q in sensitivity}
    main_ids = {wid for wid, item in corpus.items()
                if any(r['run'] in main_run_ids for r in item['discovery_routes'])}
    sensitivity_ids = {wid for wid, item in corpus.items()
                       if any(r['run'] in sensitivity_run_ids for r in item['discovery_routes'])}
    sensitivity_added = len(sensitivity_ids - main_ids)
    occurrences = sum(q['retrieved'] for q in discovery)
    unique = summary['discovery_unique']
    assert occurrences == summary['discovery_occurrences']
    doi_added = len(corpus) - unique
    full_text = sum(r['stage'] == 'full_text' for r in records)
    pending = human['not_checked']
    sections = [f'''<header><p class="meta">OpenAlex · Search date {h(analysis['date'])}</p>
<h1>Continuous sign language recognition reviews</h1>
<p>Open-access reviews focused on CSLR · 2020–2026</p>
<p class="status">AI screening recommendations; {pending} records await researcher decisions.</p>
</header>
<div class="totals" aria-label="Screening results">
<div><strong>{len(records)}</strong>assessed</div><div><strong>{ai['include']}</strong>recommended</div>
<div><strong>{ai['uncertain']}</strong>unresolved</div><div><strong>{ai['exclude']}</strong>excluded</div></div>''']
    sections.append('<section id="papers"><h2>Recommended reviews</h2>')
    picked = []
    unresolved = []
    for r in records:
        wid = r['openalex_id']; w = corpus[wid]['work']; e = evidence.get(wid, {})
        if r['ai_decision'] == 'include':
            label = f"{e['authors']} ({e['year']}) — {w['display_name']}"
            qualification = 'Open review.'
            if e.get('integrity_note'):
                qualification = 'Expression of Concern issued 22 July 2026.'
            elif e.get('publication_status'):
                qualification = e['publication_status'].capitalize() + '.'
            picked.append([link(e['url'], label), h(e['methods']), h(qualification)])
        elif r['ai_decision'] == 'uncertain':
            reason = 'Conflicting publication dates; eligibility unresolved.' if e.get('date_conflict') else 'Open full-text access not verified.'
            label = f"{e.get('authors', w['display_name'])} ({e.get('year', w['publication_date'][:4])})"
            unresolved.append(link(e.get('url', w.get('doi') or w['id']), label) + ' — ' + h(reason))
    sections.append(table(['Review / full text', 'Coverage', 'Qualification'], picked,
                          'Inclusion recommendations based on inspected full text'))
    gaps = read(WORK / 'evidence.json')['gap_hypotheses']
    sections.append('<p><strong>Potential review gaps:</strong> '
                    + h('; '.join(g['topic'] for g in gaps))
                    + '. These concern inspected review coverage, not proven gaps in the research literature.</p></section>')
    sections.append(f'''<section id="selection"><h2>Search and selection</h2>
<p class="flow"><strong>{occurrences}</strong> search occurrences → <strong>{unique}</strong> unique records + <strong>{doi_added}</strong> reference-based DOI candidate → <strong>{len(records)}</strong> assessed.</p>
<p>Deduplicated by OpenAlex ID and normalized DOI. Titles and available abstracts were screened for CSLR-focused reviews; {full_text} records reached full-text screening ({stages['full_text', 'include']} recommended, {stages['full_text', 'exclude']} excluded). {stages['title_abstract', 'exclude']} further exclusions were suggested at title/abstract stage; {ai['uncertain']} cases remain unresolved.</p>
<ul><li><strong>Include:</strong> reviews synthesizing multiple CSLR studies, dated 2020-01-01–2026-10-25, with lawful public full text. Repository reviews are eligible with peer-review status labeled.</li>
<li><strong>Exclude:</strong> broader recognition/translation or isolated-sign reviews where CSLR is not central; primary research; unrelated work; proceedings volumes/notices; confirmed out-of-range publications.</li>
<li><strong>Uncertain:</strong> missing text, unclear access rights or conflicting dates. These are not content-based exclusions.</li></ul>
</section>''')
    sections.append('''<section id="queries"><h2>Executed searches</h2>
<p><strong>Discovery filters:</strong> 2020-01-01–2026-10-25 inclusive; core + expansion corpus; publication date ascending; 100 results/page; cursor pagination. No OA, language or citation filter. Open access was checked during screening.</p>''')
    query_rows = []
    for q in queries:
        params = q['params']
        field = next((k for k in params if k.startswith('search.')), None)
        if field:
            scope = 'Title only' if field == 'search.title' else 'Title / abstract / keywords'
            filters = 'Dates + type:review' if 'type:review' in params.get('filter', '') else 'Dates'
            search = params[field]
        else:
            scope = 'Exact DOI'
            search = params['filter'].removeprefix('doi:')
            filters = 'DOI only; no date filter'
        query_rows.append([h(q['id']), '<code>' + h(search) + '</code>', h(scope), h(filters), h(q['retrieved'])])
    sections.append(table(['ID', 'Query', 'Fields', 'Filters', 'Found'], query_rows,
                          'Result counts overlap across queries'))
    completion = 'All configured queries completed.' if all(q['complete'] for q in queries) else 'Some configured queries are incomplete; see the data snapshot.'
    sections.append(f'<p>{main_occurrences} main-query occurrences; {sensitivity_occurrences} title-sensitivity occurrences ({sensitivity_added} new IDs). The separate DOI check followed a cited review with conflicting dates. Pilot pages were reused without double counting. {h(completion)} OpenAlex indexing and exact phrases limit recall.</p></section>')
    sections.append('<section id="unresolved"><h2>Unresolved candidates</h2><ul>'
                    + ''.join('<li>' + item + '</li>' for item in unresolved)
                    + '</ul></section>')
    sections.append('''<footer><a href="../work/screening.csv">Full screening log</a> · <a href="../work/evidence.json">Evidence</a> · <a href="../protocol.md">Protocol</a> · <a href="search-data.json">Exact search data</a> · <a href="../README.md">Reproduction</a></footer>''')
    css = '''*{box-sizing:border-box}body{margin:0;background:#f5f6f7;color:#243241;font:15px/1.55 system-ui,-apple-system,"Segoe UI",sans-serif}main{max-width:1080px;margin:32px auto;padding:32px 36px;background:white}h1,h2{color:#17384f;line-height:1.25}h1{font-size:1.9rem;margin:8px 0}h2{font-size:1.15rem;margin:0 0 12px}p{margin:10px 0}.meta,caption,footer{font-size:.8rem;color:#526474}.status{color:#815b13;font-size:.88rem}.totals{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:22px 0}.totals div{border:1px solid #dbe3e9;padding:12px;font-size:.85rem}.totals strong{display:block;color:#17384f;font-size:1.6rem}section{border-top:1px solid #dbe3e9;padding:22px 0}.table-wrap{overflow-x:auto}table{width:100%;border-collapse:collapse;font-size:.82rem}caption{text-align:left;padding:0 0 8px}th,td{padding:10px 8px;border-bottom:1px solid #e0e6eb;text-align:left;vertical-align:top}th{background:#eff3f6}a{color:#155e91;text-underline-offset:3px}code{font: .78rem/1.5 ui-monospace,Consolas,monospace;overflow-wrap:anywhere}li{margin:7px 0}footer{border-top:1px solid #dbe3e9;padding-top:18px}.flow{background:#f3f7f9;padding:12px}@media(max-width:650px){main{margin:0;padding:24px 16px}h1{font-size:1.5rem}.totals{gap:6px}.totals div{padding:8px}}@media print{@page{margin:14mm}body{background:white;font-size:9pt}main{margin:0;padding:0;max-width:none}h1{font-size:18pt}section{padding:14px 0}.table-wrap{overflow:visible}table{font-size:8pt}tr{break-inside:avoid}thead{display:table-header-group}h2{break-after:avoid}a{color:inherit}}'''
    document = ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
                '<meta name="viewport" content="width=device-width, initial-scale=1">'
                '<meta name="description" content="Reproducible OpenAlex search and selection methods for CSLR-focused reviews since 2020.">'
                '<title>CSLR reviews — search and selection report</title><style>' + css
                + '</style></head><body><main>' + '\n'.join(sections) + '</main></body></html>\n')
    snapshot = {'analysis': analysis, 'summary': summary, 'queries': queries, 'screening': screening,
                'corpus': list(corpus.values()), 'evidence': list(evidence.values()),
                'merge_decisions': read(WORK / 'merge_decisions.json'),
                'run_manifest_paths': {k: f'work/runs/{k}/manifest.json' for k in manifests}}
    snapshot_text = json.dumps(snapshot, indent=2, ensure_ascii=False) + '\n'
    if check:
        for name, expected in [('index.html', document), ('search-data.json', snapshot_text)]:
            path = OUT / name
            if not path.exists() or path.read_text() != expected:
                raise ValueError(f'{name} is stale; run python3 work/scripts/report.py')
        print('PASS: HTML report and snapshot match current research inputs.')
        return
    OUT.mkdir(exist_ok=True)
    (OUT / 'index.html').write_text(document)
    (OUT / 'search-data.json').write_text(snapshot_text)
    print('Generated html-report/index.html and html-report/search-data.json')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Fail if generated files are stale; do not write files.')
    main(check=parser.parse_args().check)
