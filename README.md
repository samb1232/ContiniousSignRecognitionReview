# CSLR review search and comparison

**[Open the project report →](html-report/index.html)**

The HTML report presents saved retrieval filters, M1–M3 and all 34 candidates. Current AI and manual eligibility decisions are Not screened. Historical eligibility recommendations have been cleared.

Rebuild offline:

```sh
python3 work/scripts/report.py
python3 work/scripts/verify.py
```

Saved raw runs and source documents remain unchanged. The data snapshot is packaged with the HTML for local and nginx use. Report generation time is recorded in work/analysis_config.json; update it for a new reporting edition. No new retrieval is needed.
