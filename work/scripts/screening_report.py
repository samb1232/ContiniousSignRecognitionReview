#!/usr/bin/env python3
"""Validate screening proposals and generate concise per-paper reports offline.

Usage: imported by python3 work/scripts/report.py and work/scripts/verify.py.
Detailed evidence stays in JSON; Markdown contains only a description and verdict.
"""
import json
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'html-report/support'
VERDICTS = {'include', 'exclude', 'uncertain', 'not_screened'}
STAGES = {'title_abstract', 'full_text'}
CRITERIA = {'M1', 'M2', 'M3'}


def verdict_label(record):
    value, stage = record['ai_decision'], record['stage']
    if value == 'not_screened':
        return 'Not screened'
    if value == 'include':
        return 'Proposed eligible review' if stage == 'full_text' else 'Proposed advance to full text'
    return {'exclude': 'Proposed exclusion', 'uncertain': 'Uncertain'}[value]


def validate_record(record):
    wid = record['openalex_id']
    assert record['ai_decision'] in VERDICTS, wid
    assert record['human_decision'] in VERDICTS, wid
    assert record['stage'] in STAGES, wid
    if record['ai_decision'] == 'not_screened':
        return
    assert record['description'] and record['reason'], wid
    assert record['evidence_level'] in {'metadata_only', 'abstract_only', 'full_text'}, wid
    assert set(record['criteria']) == CRITERIA, wid
    assert all(c['status'] in {'pass', 'fail', 'uncertain'} and c['reason']
               for c in record['criteria'].values()), wid
    assert record['evidence'], wid
    sources = set(record['source_ids'])
    for e in record['evidence']:
        assert e['source_id'] in sources and e['url'] and e['locator'] and e['passage'], wid
        path = (ROOT / e['path']).resolve()
        assert path.is_relative_to(ROOT) and path.is_file(), (wid, e['path'])
        if e.get('sha256'):
            assert hashlib.sha256(path.read_bytes()).hexdigest() == e['sha256'], (wid, 'Evidence changed')
    failed = set(record.get('failed_criteria', []))
    assert failed <= CRITERIA, wid
    assert failed == {k for k, c in record['criteria'].items() if c['status'] == 'fail'}, wid
    if record['ai_decision'] == 'exclude':
        assert failed, wid
    else:
        assert not failed, wid
    if record['ai_decision'] == 'uncertain':
        assert record['unresolved_issues'] and record['next_action'], wid
    if record['stage'] == 'full_text':
        assert record['evidence_level'] == 'full_text', wid
        assert any(a['stage'] == 'title_abstract' for a in record['assessments']), wid
        if record['ai_decision'] == 'include':
            assert all(c['status'] == 'pass' for c in record['criteria'].values()), wid
            assert record['classification'] in {'dedicated', 'broader'}, wid
            assert len(record['qualifying_studies']) >= 2, wid
            assert len(set(record['qualifying_studies'])) >= 2, wid


def markdown_report(record, work):
    title = work['display_name'].replace('\n', ' ')
    if record['ai_decision'] == 'not_screened':
        return f'# {title}\n\nAssessment pending.\n\n**Not screened.**\n'
    stage = {'title_abstract': 'title/abstract', 'full_text': 'full text'}[record['stage']]
    criteria = ', '.join(f'[{c}](../../index.html#{c})' for c in record['failed_criteria'])
    rationale = record['reason']
    if criteria:
        rationale += f' Failed criteria: {criteria}.'
    if record['ai_decision'] == 'uncertain':
        rationale += ' Next: ' + record['next_action']
    return (f'# {title}\n\n{record["description"]}\n\n'
            f'**{verdict_label(record)} ({stage}).** {rationale} '
            f'[Evidence](../evidence/{record["openalex_id"]}.json).\n')


def build_reports(records, corpus, check=False):
    # These two directories contain only generated per-candidate artifacts.
    # Retired records and evidence are preserved separately in work/archive/.
    for folder, suffix in [('papers', '.md'), ('evidence', '.json')]:
        for path in (OUT / folder).glob('W[0-9]*' + suffix):
            if path.stem not in corpus:
                if check:
                    raise AssertionError(f'Retired candidate still published: {path}')
                path.unlink()
    for record in records:
        validate_record(record)
        wid = record['openalex_id']
        work = corpus[wid]['work']
        md = markdown_report(record, work)
        assert len(md.split()) <= 150, f'{wid}: report exceeds 150 words'
        detail = {'paper': {'title': work['display_name'], 'year': work['publication_year'],
                            'doi': work.get('doi'), 'openalex_url': work['id']}, **record}
        outputs = {OUT / 'papers' / f'{wid}.md': md,
                   OUT / 'evidence' / f'{wid}.json': json.dumps(detail, indent=2, ensure_ascii=False) + '\n'}
        for path, content in outputs.items():
            if check:
                assert path.exists() and path.read_text() == content, f'Stale report: {path}'
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content)
    if check:
        assert {p.stem for p in (OUT / 'papers').glob('*.md')} == set(corpus)
        assert {p.stem for p in (OUT / 'evidence').glob('*.json')} == set(corpus)
