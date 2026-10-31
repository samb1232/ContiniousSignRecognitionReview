#!/usr/bin/env python3
"""Generate a standalone, printable search-methods report from saved research inputs.

Usage: python3 work/scripts/html_report.py
       python3 work/scripts/html_report.py --check
Writes html-report/index.html and html-report/search-data.json. No network,
third-party packages, or manual duplication of result counts is required.
The main report.py pipeline rebuilds this page automatically.
"""
from collections import Counter
from datetime import datetime
from html import escape
import json
from pathlib import Path
from screening_report import verdict_label

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
    decisions = {r['openalex_id']: r for r in records}
    stage_summary = '; '.join(f"{count} {verdict_label({'ai_decision': verdict, 'stage': stage}).lower()} ({stage.replace('title_abstract', 'title/abstract').replace('full_text', 'full text')})"
                              for (stage, verdict), count in sorted(stages.items()))
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
    sections = [f'''<header>
<p class="eyebrow">Literature review · Search &amp; selection</p>
<h1>Finding reviews of continuous sign language recognition</h1>
<p class="lead">How the review candidates were retrieved from OpenAlex, and how they were assessed against the screening criteria.</p>
<div class="result"><div><span class="result-number">{len(records)}</span><strong>candidates collected</strong></div>
<p>{unique} from OpenAlex discovery searches + {doi_added} found through references and verified by DOI.</p></div>
<p class="status">AI proposals: {h(stage_summary)}. Manual assessment: {human['not_screened']} not screened.</p>
</header>
<nav aria-label="Report sections"><a href="#queries">1. Search rules</a><a href="#criteria">2. Screening criteria</a><a href="#candidates">3. Candidates</a></nav>''']
    def readable_date(value):
        return datetime.fromisoformat(value).strftime('%d %B %Y')

    retrieval_dates = sorted({readable_date(v['started_utc']) for v in manifests.values()})
    sections.append('<details class="metadata"><summary>Report metadata</summary><div class="details-body"><p>Publication window: 1 January 2020–25 October 2026 inclusive.</p><p>Retrieved: '+h(', '.join(retrieval_dates))+'</p><p>Report generated: '+h(readable_date(analysis['report_generated_utc']))+'</p></div></details>')
    sections.append('''<section id="queries"><p class="eyebrow">01 · Retrieval</p><h2>OpenAlex search rules</h2>
<p class="section-intro">These rules determined which records were retrieved. Eligibility is assessed afterwards using the screening criteria below.</p>
<div class="rules-grid"><article class="rule"><h3>Shared search restrictions</h3><p>Discovery searches cover <strong>1 January 2020–25 October 2026</strong>, inclusive. All routes use <code>corpus=all</code>.</p><p>No open-access, language, citation-count or ranking restriction was applied.</p></article>
<article class="rule"><h3>Route-specific restrictions</h3><p>Only <a href="#query-q1r">q1r</a> and <a href="#query-q2r">q2r</a> require <code>type:review</code>. The reference-triggered <a href="#query-doi-ibrahim">DOI lookup</a> has no publication-date filter.</p><p>Main queries search titles, abstracts and keywords; supplementary queries s1 and s2 search titles only.</p></article></div>
<h3>Exact queries and filters</h3><p>Search text and structured API filters are shown separately. Counts overlap across queries.</p>''')
    query_rows = []
    for q in queries:
        params = q['params']
        search_fields = [(k,v) for k,v in params.items() if k.startswith('search.')]
        field = '<br>'.join('<code>'+h(k)+'</code>' for k,v in search_fields) or 'Exact DOI lookup'
        terms = '<br>'.join('<code>'+h(v)+'</code>' for k,v in search_fields) or 'No text search'
        query_rows.append(['<span class="query-id" id="query-'+h(q['id'])+'">'+h(q['id'])+'</span>',field,terms,'<code>'+h(params.get('filter','None'))+'</code>',h(q['retrieved'])])
    sections.append(table(['Query ID','Search parameter','Exact search text','Structured API filters','Returned'],query_rows,'Executed queries · main search, supplementary title search, and DOI verification'))
    sections.append('<details class="execution"><summary>Execution details and exact API parameters</summary><div class="details-body"><p>Endpoint: <code>GET https://api.openalex.org/works</code>. Sort and page size are execution settings. Cursor pagination starts at <code>*</code>; full searches completed, reusing pilot pages without counting them twice.</p>'+''.join('<article><h3>'+h(q['id'])+'</h3><pre>'+h(json.dumps({**q['params'],'cursor':q['cursor_start']},indent=2))+'</pre></article>' for q in queries)+'</div></details>')
    sections.append(f'<p class="reconciliation">{occurrences} overlapping discovery occurrences → {unique} unique search candidates + {doi_added} reference candidate → <strong>{len(records)} candidates</strong>. Deduplicated by OpenAlex ID and normalized DOI. Supplementary title searches returned {sensitivity_occurrences} occurrences and added {sensitivity_added} new candidates.</p></section>')
    criteria = [('M1','Review purpose','Include narrative reviews, surveys, systematic reviews, scoping reviews and mapping studies synthesizing previous research. Exclude primary method, dataset or experimental papers whose literature discussion is only background.'),('M2','CSLR coverage','Include reviews of recognition of sequences of linguistic signs in continuous signing. Broader SLR/translation surveys may qualify.'),('M3','Vision-based scope','Include video/RGB, depth and pose/skeleton approaches. Exclude sensor-only reviews without vision-based CSLR coverage.')]
    sections.append('<section id="criteria"><p class="eyebrow">02 · Eligibility assessment</p><h2>Screening criteria</h2><p class="section-intro">Apply M1–M3 to each candidate. AI assessments are proposals; manual decisions are recorded independently.</p><div class="criteria-grid">'+''.join('<article class="criterion" id="'+i+'"><span class="criterion-id">'+i+'</span><h3>'+name+'</h3><p>'+text+'</p></article>' for i,name,text in criteria)+'</div>')
    sections.append('<h3>Verdicts and supporting evidence</h3>')
    sections.append(table(['Stored verdict','Title / abstract','Full text'],[
        ['<code>not_screened</code>','Not screened','Not assessed'],
        ['<code>include</code>','Advance to full-text assessment','Eligible review'],
        ['<code>exclude</code>','Clearly fails a criterion','Fails a criterion after assessment'],
        ['<code>uncertain</code>','Issue unresolved; seek full text or verification','Eligibility unresolved; record next action']], 'Meaning of each verdict by assessment stage'))
    sections.append('<p>Every exclusion requires a linked criterion, a paper-specific explanation and evidence identifying the source and relevant passage, metadata field or full-text page, section or table. Uncertainty requires the unresolved issue and proposed next action.</p></section>')
    rows=[]
    for number, (wid,item) in enumerate(corpus.items(), start=1):
        w=item['work']; routes=sorted({p['query'] for p in item['provenance']})
        paper=link(w.get('doi') or w['id'],w['display_name'])+'<br>'+h(w['publication_year'])+' · '+link(w['id'],wid)
        if w.get('doi'): paper+='<br>'+link(w['doi'],w['doi'])
        if wid=='W2992983807': paper+='<p>Date validation: OpenAlex 2019-12-02 falls outside the discovery window; saved institutional PDF says 2020 and publisher says 2022-09-21. Window compliance unresolved; verify publication date. DOI route did not enforce dates.</p>'
        record = decisions[wid]
        decision = link('support/papers/'+wid+'.md', verdict_label(record))
        if record['ai_decision'] != 'not_screened':
            decision += '<br><small>'+h(record['stage'].replace('title_abstract', 'title/abstract').replace('full_text', 'full text'))+'</small>'
            decision += '<p>'+h(record['reason'])+'</p>'
            if record['failed_criteria']:
                decision += 'Failed: ' + ', '.join(link('#'+c,c) for c in record['failed_criteria'])
            if record['ai_decision'] == 'uncertain':
                decision += '<p>Next: '+h(record['next_action'])+'</p>'
        human_label = {'not_screened':'Not screened','include':'Include','exclude':'Exclude','uncertain':'Uncertain'}[record['human_decision']]
        rows.append([h(number),paper, ' · '.join(link('#query-'+q,q) for q in routes),decision,h(human_label)])
    sections.append('<section id="candidates"><p class="eyebrow">03 · Collected records</p><h2>Candidates</h2><p class="section-intro">Query IDs link to exact searches. AI verdicts link to short paper reports and supporting evidence. AI proposals are separate from independent manual decisions.</p>'+table(['№','Paper','Discovery routes','AI screening decision','Manual screening decision'],rows,f'All {len(records)} candidates; AI proposals by assessment stage')+'</section>')
    css = '''
*{box-sizing:border-box}html{scroll-padding-top:24px}body{margin:0;background:#f3f5f7;color:#283642;font:16px/1.65 system-ui,-apple-system,"Segoe UI",sans-serif}
main{max-width:1180px;margin:32px auto;padding:48px 56px;background:#fff;border:1px solid #e1e7eb;border-radius:12px}
h1,h2,h3,h4{color:#163d4c;line-height:1.25}h1{max-width:850px;font-size:2.5rem;letter-spacing:-.035em;margin:12px 0 18px}h2{font-size:1.9rem;letter-spacing:-.025em;margin:8px 0 14px}h3{font-size:1.08rem;margin:22px 0 10px}h4{font-size:1rem;margin:0 0 10px}p{margin:10px 0}.eyebrow{font-size:.73rem;font-weight:750;letter-spacing:.12em;text-transform:uppercase;color:#397064}.lead,.section-intro{color:#52646f;max-width:850px}.lead{font-size:1.12rem}
a{color:#12627c;text-underline-offset:3px}a:hover{color:#0a4039}a:focus-visible,summary:focus-visible{outline:3px solid #ab6b14;outline-offset:4px}
.result{display:flex;align-items:center;gap:32px;margin:28px 0 12px;padding:22px 26px;background:#edf5f2;border-left:4px solid #397666;border-radius:0 8px 8px 0}.result>div{flex:0 0 180px}.result-number{display:block;font-size:2.8rem;font-weight:750;line-height:1.1;color:#1d594c}.result strong{font-size:.86rem}.result p{max-width:540px}.status{font-size:.9rem;color:#536570}
nav{display:flex;flex-wrap:wrap;gap:10px 24px;margin:28px 0 18px}nav a{font-size:.9rem;font-weight:650}details{border:1px solid #dbe4e8;border-radius:6px;margin:16px 0;background:#fafcfc}summary{padding:12px 16px;cursor:pointer;font-size:.9rem;font-weight:650;color:#375561}.details-body{padding:0 18px 18px}.metadata{font-size:.85rem}.metadata li{overflow-wrap:anywhere;margin:12px 0}
section{border-top:1px solid #dce5e8;padding:36px 0 8px;margin-top:30px}.rules-grid,.stages{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin:22px 0}.rule,.stages article{background:#f5f8fa;border:1px solid #e2e9ed;border-radius:8px;padding:20px}.rule h3{margin-top:0}.rule p,.stages p{font-size:.92rem}.criteria-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:24px 0 30px}.criterion{padding:22px;border:1px solid #cdded8;border-top:3px solid #397666;border-radius:6px}.criterion-id{display:inline-block;color:#245c4f;font-weight:750;font-size:.85rem}.criterion h3{margin:12px 0}.criterion p{font-size:.92rem}.assessment-note{padding:18px 22px;border-left:3px solid #ac8546;background:#faf7f0;margin:24px 0}.assessment-note h3{margin-top:0}.assessment-note p{font-size:.92rem}
.table-wrap{overflow-x:auto;margin:18px 0}table{width:100%;border-collapse:collapse;font-size:.82rem;line-height:1.55}caption{text-align:left;color:#596d78;font-size:.8rem;padding:0 0 12px}th,td{padding:14px 12px;border-bottom:1px solid #dfe7eb;text-align:left;vertical-align:top;overflow-wrap:anywhere}th{background:#edf3f6;font-weight:700;color:#2a4857}tbody tr:nth-child(even){background:#fafcfd}.query-id{font-weight:750;white-space:nowrap}#queries th:nth-child(3){width:32%}#queries th:nth-child(4){width:25%}#candidates th:first-child{width:4%}#candidates td:first-child{white-space:nowrap}#candidates th:nth-child(2){width:39%}#candidates th:nth-child(3){width:12%}#candidates th:nth-child(4){width:31%}#candidates th:nth-child(5){width:14%}#candidates td:nth-child(n+4){color:#596a74}code{font:.78rem/1.5 ui-monospace,Consolas,monospace;overflow-wrap:anywhere}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f0f4f6;padding:16px;border-radius:5px;font-size:.8rem}.reconciliation{font-size:.88rem;color:#526570;margin-top:22px}:target{outline:2px solid #bd9357;outline-offset:5px}
@media(max-width:760px){main{margin:0;border:0;border-radius:0;padding:28px 18px}h1{font-size:1.95rem}h2{font-size:1.55rem}.rules-grid,.criteria-grid,.stages{grid-template-columns:1fr}.result{gap:18px;padding:18px}.result>div{flex-basis:110px}.result p{font-size:.9rem}.result-number{font-size:2.3rem}th,td{padding:10px 8px}#queries table{min-width:660px}#candidates table{min-width:600px}section{padding-top:26px}}
@media print{@page{margin:14mm}body{background:#fff;font-size:9pt}main{margin:0;padding:0;border:0;max-width:none}h1{font-size:22pt}h2{font-size:16pt}h3{font-size:11pt}nav{display:none}section{margin-top:16px;padding:18px 0 0}.table-wrap{overflow:visible}table,#queries table,#candidates table{font-size:8pt;min-width:0;table-layout:fixed}th,td{padding:7px 5px}tr,.criterion,.rule,.stages article{break-inside:avoid}thead{display:table-header-group}h2,h3,h4{break-after:avoid}a{color:inherit}.criteria-grid{grid-template-columns:repeat(3,1fr);gap:10px}.criterion{padding:12px}.rules-grid,.stages{grid-template-columns:1fr 1fr;gap:12px}.criterion p,.rule p,.stages p,.assessment-note p{font-size:9pt}.result{margin:16px 0;padding:12px}.result-number{font-size:26pt}.metadata,.execution{display:none}.eyebrow{font-size:8pt}}
'''
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
