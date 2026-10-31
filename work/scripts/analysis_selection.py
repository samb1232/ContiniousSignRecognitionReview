"""Select active queries from immutable saved runs.

Usage: imported by report.py, html_report.py and verify.py; no network requests.
"""


def selected_queries(analysis, runid, available):
    available = set(available)
    selected = set(analysis.get('selected_queries', {}).get(runid, available))
    if not selected <= available:
        raise ValueError(f'Unknown selected queries in {runid}: {selected - available}')
    return selected
