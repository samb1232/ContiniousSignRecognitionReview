# AGENTS.md

## Project

I am conducting a research on continuous sign language recognition and aim to identify recent literature reviews in the field. My goal is to understand the main methods, datasets, and open challenges, and identify missed spots in literature review.

## Working approach

- Follow the current research protocol and query configuration when available. Record changes to scope, queries, or selection criteria with their rationale.
- Work in small, verifiable stages.
- Prefer simple Python scripts and JSON/CSV outputs.
- For each script write a brief descrtiption on what it does and how to use it.
- Explain important technical and methodological decisions briefly as for a beginner researcher.

## Evidence

- Check official OpenAlex documentation for API behavior relevant to the task (the docs are at help.openalex.org).
- Never invent publications, identifiers, quotations, findings, or successful executions.
- Support claims about a paper’s content with its DOI or OpenAlex ID and a page or section reference when available.
- Distinguish full-text evidence, abstract-only evidence, and unverified information. Keep missing values explicit (or don't mention them at all).

## Reproducibility

- Preserve raw API responses. Save new search runs separately rather than overwriting previous results.
- Record exact information and configuration needed to reproduce a run.
- Respect API limits. For one task use no more than a 300 OpenAlex tokens (out of 1000 daily)
- Deduplicate using OpenAlex IDs and normalized DOIs while retaining query provenance. Inspect possible preprint/published-version pairs before merging.
- Read API keys from environment variables.

## Verification

- Run checks appropriate to the change. Verify pagination, deduplication, and agreement between exports and saved responses when relevant.
- Finish with a concise account of changed files, findings, limitations.