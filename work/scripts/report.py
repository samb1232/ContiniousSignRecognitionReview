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
    lines=['# Open-access CSLR-focused reviews since 2020', '',
           'Search cutoff: 25 October 2026. This is an evidence-backed AI screening and comparison; final researcher decisions are pending.', '',
           '## Search criteria and completeness', '',
           'OpenAlex discovery searched titles, abstracts and keywords for each combination of “continuous sign language recognition” / “continuous sign recognition” with “review” / “survey” / “systematic literature review”, plus two supplementary `type:review` routes. Dates: 2020-01-01–2026-10-25 inclusive; corpus: all; sort: publication date ascending; page size: 100; cursor pagination; no OA, language, citation-count or ranking cutoff. Two logged title-based sensitivity searches added review/survey/challenges/understanding/critical-study terms. Exact parameters are in the saved configurations and run manifests.', '',
           'Eligibility requires CSLR to be the review’s central subject and synthesis of multiple prior studies. Publisher or lawful author/repository full text must be accessible. Broad SLR/translation reviews are outside the researcher-selected scope. Unavailable full text leaves relevance/access uncertain rather than supporting a content exclusion.', '',
           f"The discovery routes returned **{counts['discovery_occurrences']} occurrences and {counts['discovery_unique']} unique records**. A reference-triggered DOI verification added one date-disputed candidate, making **{len(corpus)} screened records**. All configured queries terminated; the sensitivity routes added no new IDs. Pilot pages were reused in the main full run. This describes query completeness, not exhaustive coverage of the literature.", '',
           f"AI suggestions: {counts['ai_decisions']}. Human decisions: {counts['human_decisions']}. Cost: **{reserved:g}/300 credits** reserved; {observed:g} successful-request credits observed. No paid OpenAlex PDF downloads or reranking. Account allowance and request-level costs are saved in the manifests.", '',
           '## Reviews recommended for inclusion', '',
           '| Review and open full text | Methods and representations | Datasets and evaluation | Challenges and limits of coverage |',
           '|---|---|---|---|']
    integrity_notes = []
    for wid, row in rows.items():
        if row['ai_decision']!='include': continue
        e=assertions[wid]; title=corpus[wid]['work']['display_name']
        lines.append('| '+ ' | '.join(cell(x) for x in [f"[{e['authors']} ({e['year']}), {title}]({e['url']})", e['methods'],e['datasets_evaluation'],e['limitations']])+ ' |')
        if e.get('integrity_note'): integrity_notes.append(e['integrity_note'])
    for note in integrity_notes:
        lines += ['',note]
    lines += ['', 'Section/page evidence, publication-date corrections, access verification and interpretation labels are recorded in `evidence.json`. Numerical results quoted within reviews were not independently revalidated against their primary studies.', '',
              '## Focused candidates with unresolved eligibility', '',
              '| Candidate | What the inspected source supports | Why unresolved |', '|---|---|---|']
    for wid,row in rows.items():
        if row['ai_decision']!='uncertain':continue
        e=assertions.get(wid,{}); w=corpus[wid]['work']
        lines.append('| '+' | '.join(cell(x) for x in [f"[{w['display_name']}]({e.get('url',w.get('doi') or w['id'])})", e.get('coverage_summary','Content comparison not completed.'),row['reason']])+' |')
    lines += ['', '## Potential gaps to investigate', '']
    lines += [f"- **{g['topic']}** — {g['interpretation']} Evidence: {g['support']}." for g in evidence['gap_hypotheses']]
    lines += ['', 'These are hypotheses about the inspected review coverage, not claims that the wider CSLR literature lacks such research. Signer independence, non-manual features and real-time recognition are already discussed in the inspected reviews; a new review would need more than listing these familiar challenges.', '',
              '## Scope and evidence limitations', '',
              'The CSLR-focused restriction excludes useful broad surveys, including Koller’s 2020 quantitative survey. Restrictive phrases and OpenAlex indexing/date errors can miss eligible reviews. One focused review was found through a reference and required a separate DOI check because OpenAlex dates it before 2020. Web searches were used to locate copies and verify already identified candidates; incidental web results were not silently added.', '',
              'Publisher-access failures and uncertainty about author-upload rights prevent treating every focused candidate as verified open access. Full-text comparisons are restricted to accessible, inspected documents. An Expression of Concern is reported as a publication-status fact, without speculating about its cause. Human confirmation of screening, date conventions and the comparison remains the next research decision.', '',
              '## Reproduction', '',
              'Run `python3 work/scripts/report.py` to regenerate this report, corpus, screening CSV and summary from saved runs and manual inputs. Run `python3 work/scripts/verify.py` for offline reconciliation. See the README for retrieval, source download and test commands.', '']
    (WORK / 'report.md').write_text('\n'.join(lines))
    from html_report import main as build_html
    build_html()
    print(json.dumps({k:v for k,v in counts.items() if k!='query_counts'},indent=2))

if __name__=='__main__':main()
