# CSLR review search and screening

**[Open the project report →](html-report/index.html)**

The report presents exact saved retrieval filters, M1–M3, and all 34 candidates. AI screening decisions are proposals; independent manual decisions remain Not screened. Each AI verdict links to a concise paper report, with detailed evidence in linked JSON.

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
