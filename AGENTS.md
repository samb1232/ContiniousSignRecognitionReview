# AGENTS.md

## Goal

Build a reproducible OpenAlex search and selection workflow for recent literature reviews of continuous sign language recognition (CSLR). Compare their coverage of methods, datasets, evaluation, and open challenges, and identify potential gaps in existing reviews. Inspect papers from 2020 year to current date.

## OpenAlex and credentials

- Use the OpenAlex API at https://api.openalex.org.
- Before implementing or changing API queries, read https://help.openalex.org/api/llm-quick-reference/ and consult the relevant official documentation at https://help.openalex.org.
- Before filtering by an author, institution, source, topic, publisher, or funder, resolve it to an OpenAlex ID and verify the match. Do not filter by entity names or silently choose among ambiguous matches.
- `OPENALEX_API_KEY` is contained in the .env.

## Working approach

- Treat `html-report/index.html` as the project's main visual result. Keep it concise: current findings, exact searches and filters, reconciled counts, selection/exclusion rules, and material uncertainties. Link detailed logs and evidence instead of repeating them.
- After every new retrieval result, screening decision, evidence finding, or analysis change, update the saved inputs and selected runs in `work/analysis_config.json` as needed, then run `python3 work/scripts/report.py` and `python3 work/scripts/verify.py`. The report command also regenerates the HTML and its data snapshot. Verify the HTML agrees with the latest results before handing off; edit source inputs or the generator rather than the generated HTML.

- Work in small, verifiable stages.
- Prefer simple Python scripts and JSON/CSV outputs. Put reusable retrieval, transformation, and analysis scripts in `work/scripts/`.
- Any reported count, table, or figure derived from collected data must be reproducible from saved inputs using a script.
- Give each script a short description and usage example in its docstring. Document setup, dependencies, and reproduction commands in `README.md`.
- Explain consequential technical and methodological decisions briefly for a beginner researcher.

## Reproducibility

- Save each new search run under `work/runs/`, with raw responses, exports, and a run manifest. Never overwrite earlier search results.
- Reuse saved responses for debugging and verification when possible. Resume interrupted runs only with the same configuration and a logged resume event.

## API budget and reliability

- Default limit: **30% OpenAlex daily credits per task**, cumulative across all runs and retries for that task. Record the limit and usage in the configuration and run manifests. Change the limit only when it is nessecary. Explain your logic to user in that case.
- Respect documented rate limits. Use timeouts, bounded retries, and exponential backoff for transient failures; honor `Retry-After` when supplied.

## Evidence

- Never invent publications, identifiers, quotations, findings, metadata, or successful executions.
- Base content claims on inspected source material. Record the DOI or OpenAlex ID, evidence level (`metadata_only`, `abstract_only`, or `full_text`), and a supporting section, page, or passage when available. Label unverified claims explicitly or not mention unverified information at all.
- Do not infer a paper's findings from its title or bibliographic metadata. Distinguish author-stated conclusions from our interpretations.

## Deduplication and screening

- Deduplicate by OpenAlex ID and normalized DOI while retaining all query and run provenance.

## Verification

- Run checks appropriate to the change. Verify pagination, deduplication, and agreement between exports and saved responses when relevant.
- Finish with a concise account of changed files, findings, limitations.
