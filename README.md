# CSLR review search and comparison

**[Open the project report →](html-report/index.html)**

The HTML report is the project's main visual result: recommended reviews, search queries and filters, selection counts, exclusion rules and unresolved cases. Open it directly in a browser or print to PDF. Detailed [comparison](work/report.md), [protocol](protocol.md) and [screening decisions](work/screening.csv) provide supporting evidence.

Keep it current after every new result or decision: update the saved inputs and selected runs, then run `python3 work/scripts/report.py` and `python3 work/scripts/verify.py`. The report command automatically rebuilds the HTML and its JSON snapshot. Recommendations remain distinct from final researcher decisions. Do not edit generated reports directly.

## Setup

Python 3.9+; this execution used Python 3.14.2. Retrieval, reporting, verification and tests use only the standard library. Optional PDF extraction uses pypdf 6.21.2; DOCX and HTML extraction use the standard library.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

Set `OPENALEX_API_KEY` in the environment or supply it in an ignored local `.env`, following `.env.example`. Existing environment variables take precedence. Bearer authentication keeps credentials out of saved request parameters. No credentials are written to outputs.

## Reproduce offline

```sh
python3 work/scripts/report.py
python3 work/scripts/verify.py
python3 -m unittest discover -s work/scripts -p 'test_*.py' -v
```

`work/analysis_config.json` selects saved main, sensitivity and DOI-verification runs. `report.py` merges their records and generates the corpus, screening CSV, summary counts and report from explicit inputs `work/screening.json` and `work/evidence.json`. `work/merge_decisions.json` records inspected version relationships. Update manual inputs explicitly, log methodological changes, then rebuild. Human decisions are never automatically replaced.

`verify.py` checks response/source hashes, cursor chains and termination, per-query counts, date filters, exports, budget and screening reconciliation. It regenerates equivalent derived per-run exports; raw responses and manifests are unchanged. Tests cover budget stops before network calls, retry accounting, Retry-After, raw-byte preservation, credential echoes, and DOI-alias provenance.

## Repeat retrieval

Live reruns query a changing index; saved response bytes are the stable reproduction basis. Each new run has an immutable configuration/source snapshot, raw bodies, sanitized requests, UTC timestamps, outcomes and costs. Never delete earlier runs to reset the budget.

```sh
python3 work/scripts/retrieve.py --stage pilot
# Substitute the printed pilot directory:
python3 work/scripts/retrieve.py --stage full --reuse work/runs/PILOT_RUN_ID
python3 work/scripts/retrieve.py --stage full --config work/queries-sensitivity.json
python3 work/scripts/retrieve.py --stage full --config work/queries-doi-check.json
```

The main configuration has eight title/abstract/keyword queries. Two title-only sensitivity queries and one reference-triggered DOI check are separately preserved. The DOI check deliberately has no date filter. See the protocol and decision log for exact criteria and official documentation consulted.

The task cap is **300 cumulative credits across all manifests in `work/runs/`**, including the saved execution. Search costs 10 credits/call; DOI filtering costs 1. Recheck documentation before changing costs. `/rate-limit` establishes allowance before collection; costs are reserved durably before requests. Unknown failed outcomes retain conservative charges. A local lock serializes collectors; response headers update allowance. Other clients can change account allowance; server refusals are handled within the task cap. No usage is purchased. Requests have 40-second timeouts, up to three attempts, exponential backoff, one-second spacing and respect for Retry-After. Delays above 60 seconds stop for later resumption.

```sh
python3 work/scripts/retrieve.py --resume work/runs/INTERRUPTED_RUN_ID
python3 work/scripts/retrieve.py --resume work/runs/SENSITIVITY_RUN_ID --config work/queries-sensitivity.json
```

Resume requires identical configuration; completed runs cannot resume. Full runs may reuse identical pilot pages, preserving origin provenance without another charge. Executed code is saved in source snapshots. The original pilot manifest retains a historical stop diagnostic after successful resumption; final query states establish completion. Current code clears stale diagnostics on resume. Initial sandbox networking failed before any charged search; approved network access completed retrieval.

## Sources and interpretation

```sh
.venv/bin/python work/scripts/fetch_sources.py
```

This archives `work/sources.json` URLs, preserves response bytes/hashes, and extracts text. Successful downloads are cached; unsuccessful attempt records are retained separately. The script rejects OpenAlex API/content hosts to prevent bypassing budget accounting. Inspect content: HTTP 200 can be an abstract page, wrapper or metadata, rather than full text. Publisher wrappers and repository concept/version identifiers are recorded. No authors were contacted or access controls bypassed.

Some PDFs are scanned. The first page of the Ibrahim institutional PDF was inspected visually using this macOS command:

```sh
sips -s format png work/sources/ibrahim2020-author.pdf --out /tmp/cslr-ibrahim-first-page.png
```

`work/web_checks.json` records browser evidence where direct archiving failed or omitted a publication-status notice. These are manually recorded inputs, not raw HTTP archives. Targeted web searches located access copies and verified existing candidates; incidental results were not silently included.

Claims carry identifier, evidence level, locator and author-statement/analyst-interpretation labels. `not_reported` means absent from inspected relevant full text; `not_checked` means unassessed; `unavailable` means source/access could not be established. Numerical results within reviews were not independently rechecked against every primary study.

OpenAlex indexing, dates and exact phrases limit recall. The next researcher decision is to confirm AI screening (especially title-only exclusions and the repository report) and adjudicate unresolved access/date cases. Proposed gaps concern inspected review coverage and remain hypotheses about opportunities for a new review.
