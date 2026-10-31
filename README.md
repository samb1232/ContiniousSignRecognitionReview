# CSLR review search and screening

**[Open the project report →](html-report/index.html)**

The report presents exact saved retrieval filters, M1–M3, and all 33 active candidates. AI screening decisions are proposals; independent manual decisions remain Not screened. Each AI verdict links to a concise paper report, with detailed evidence in linked JSON.

Active runs and query IDs are selected in `work/analysis_config.json`. The 1 November 2026 revision retains q11–q13, q21–q23 and s1; it removes empty s2, redundant q1r/q2r, and the DOI-only Ibrahim candidate whose OpenAlex date is before 2020. Original runs remain immutable; the removed assessment, date-conflict evidence and previous configuration are preserved in `work/archive/2026-11-01-selection-revision.json`. The query configuration files describe the historical executions; rebuilding applies the active selection without rerunning searches.

Rebuild and verify offline with Python 3.10 or newer (standard library):

```sh
python3 work/scripts/report.py
python3 work/scripts/verify.py
python3 work/scripts/test_screening_report.py
```

`work/screening.json` is the source of current proposals and assessment histories. Paper descriptions, verdict explanations, and evidence files under `html-report/support/` are generated from those records. Each Markdown report contains only a short description and verdict explanation, capped at 150 words including the heading. Source URLs, passages, locators, access limitations, and assessment provenance remain in structured data.

Saved raw search runs are immutable. Screening uses saved abstracts and available full texts; targeted source acquisition adds no discovery candidates. New source responses and retrieval metadata are archived under `work/sources/`. Optional PDF extraction uses `pypdf` in the project virtual environment:

```sh
.venv/bin/python work/scripts/fetch_sources.py --input work/assessment_batches/batch0-sources.json --source-id SOURCE_ID
```

Use a selected source ID to avoid retrying unrelated failed requests. Update `work/analysis_config.json` with the report generation time for a new reporting edition; generation itself is deterministic and offline.

Serve the report locally by opening the HTML file, or package it with nginx:

```sh
docker build -t cslr-report html-report
docker run --rm -p 8080:80 cslr-report
```

The Docker image includes all generated paper reports and evidence JSON. Markdown reports are served as readable plain text.
