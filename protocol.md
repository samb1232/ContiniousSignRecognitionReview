# Research protocol — CSLR reviews

Version 1, fixed 2026-10-25 before retrieval.

## Current eligibility amendment

Previous eligibility judgments were cleared before this screening pass. Current AI proposals and their stage-specific evidence are recorded in work/screening.json; independent manual decisions remain not_screened. Retrieval restrictions describe executed searches; manual criteria govern subsequent eligibility assessment.

M1 — Review purpose: include narrative reviews, surveys, systematic reviews, scoping reviews and mapping studies synthesizing previous research. Exclude primary method, dataset or experimental papers with background-only literature discussion.

M2 — CSLR coverage: recognition of sequences of linguistic signs in continuous signing; broader SLR/translation surveys may qualify.

M3 — Vision-based scope: include video/RGB, depth and pose/skeleton approaches; exclude sensor-only reviews without vision-based CSLR coverage.

At title/abstract stage exclude only on clear evidence of failure. Retain potentially qualifying broader surveys. At full text confirm M1–M3 using the project-specific threshold: an identifiable section, comparative table or sustained discussion comparing at least two prior CSLR studies on methods, datasets or evaluation. Classify eligible reviews as dedicated or broader with qualifying coverage.

Citation count, venue prestige, OA status and missing review-method reporting are not exclusion grounds. Missing abstracts, unavailable full text and language difficulties require further assessment, recorded separately. Date conflicts require verification against the saved publication window, not invented eligibility decisions.

Verdicts: not_screened, include, exclude, uncertain. AI verdicts are proposals; human verdicts are independent. Exclusions require criterion IDs, paper-specific reasons and inspectable evidence; uncertainty requires the issue and next action. Evidence identifies source and passage, metadata field or page/section/table.

## Retrieval

OpenAlex-only discovery; historical executable settings are in `work/queries.json` and immutable run configurations. Active query selection is recorded in `work/analysis_config.json`. Search title/abstract/keywords for each combination of two quoted phrases (`continuous sign language recognition`, `continuous sign recognition`) and three review terms (`review`, `survey`, `systematic literature review`). The original retrieval also executed two phrase searches restricted to `type:review`; these are retired from the active report as documented below. Search core and expansion corpora, without an OA filter, citation threshold, ranking cutoff, or desired paper count. Retrieve by publication date ascending, 100 results per page, with cursors. A pilot caps each query at one page; full retrieval follows pagination to termination within budget. Keyword matching can broaden phrase matches; eligibility requires source inspection.

## Screening and evidence

Deduplicate OpenAlex IDs and normalized DOIs, retaining query/run/page provenance. Flag conflicting metadata and possible version pairs for explicit merge decisions. First screen titles/abstracts, then inspect plausible reviews' full texts. AI suggestions are inputs in `work/screening.json`, never final human decisions; record model, prompt, and available evidence. All final human decisions initially remain `not_screened`.

Extract method families, temporal alignment, representations, datasets/sign languages, metrics/splits, generalization, reproducibility, and challenges into `work/evidence.json`. Each content assertion needs an OpenAlex ID or DOI, source URL, evidence level (`metadata_only`, `abstract_only`, `full_text`), locator and supporting passage or faithful paraphrase. Separate author statements from analyst interpretations. Use `not_reported` only after checking the relevant full text, `not_screened` when not assessed, and `unavailable` when the source cannot be obtained. An unmentioned topic is a potential review gap, not proof of an absence in the literature.

## Budget, preservation, and synthesis

Task cap: 300 OpenAlex credits cumulatively across pilot, full run, and retries. This explicit user-supplied cap takes precedence over the different percentage limit in the current on-disk AGENTS.md. Search costs 10 credits per call under documentation accessed 2026-10-25; no reranking or OpenAlex content downloads. Check account allowance before collection, reserve the request cost before sending, retain conservative charges for failed/unknown outcomes, and stop before either cap is exceeded. Do not purchase usage. Credentials use environment first, then `.env`; never save credentials in requests or logs.

Save immutable new run directories containing raw response bytes, sanitized request records, manifest, configuration/source snapshots, UTC times, outcomes, costs and cursor progress. Resume requires identical configuration and an event record. Reconstruct exports offline. Compare included AI recommendations separately from human-confirmed inclusions, reconcile all counts, and report budget/access limitations and OpenAlex-only discovery limits.

## Logged sensitivity addition

After main retrieval, inspect a separate title-based sensitivity search (`work/queries-sensitivity.json`), broadening review terms to challenges, understanding, and critical study. Union and deduplicate its results with the main full run; preserve separate route provenance. This is an explicitly post-pilot amendment prompted by a cited candidate missed by the main search.

## Active selection amendment — 1 November 2026

At the user's request, retain q11, q12, q13, q21, q22, q23 and s1 in the current analysis. Retire s2 (zero results), q1r and q2r (no unique candidates beyond retained main searches). These are reporting selections made after retrieval, not claims that those searches were never executed. No active query requires `type:review`.

Remove the doi-ibrahim route and its sole candidate W2992983807 from the active set. The user could not locate the source paper and elected to apply its OpenAlex date, 2019-12-02, outside the 2020 start. Previously saved conflicting dates remain unresolved and archived; no new M1–M3 failure or human screening verdict is assigned. This leaves 33 candidates, with their existing AI and independent manual decisions unchanged.

The archived assessment, evidence, previous selection and removal reasons are in `work/archive/2026-11-01-selection-revision.json`. All original raw responses and run exports remain unchanged. Active provenance and counts use only selected queries; historical budget usage still includes all executed requests. No new searches were run for this amendment.
