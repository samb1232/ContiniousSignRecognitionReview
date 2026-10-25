# Research protocol — CSLR reviews

Version 1, fixed 2026-10-25 before retrieval.

## Question and eligibility

Which open-access reviews published from 2020-01-01 through 2026-10-25 centrally review continuous sign language recognition (CSLR), and what do they cover or overlook?

Include scholarly narrative, systematic, or scoping reviews and surveys synthesizing multiple prior CSLR studies. CSLR must be the central subject, established from the abstract and, when accessible, the full text. Broader SLR/translation surveys with only a CSLR section are excluded by the researcher's explicit scope choice. Exclude primary methods, datasets, isolated-sign-only reviews, unrelated work, and out-of-range publications. No language restriction; inability to inspect a language is recorded as uncertainty. Repository author manuscripts and open preprints are eligible access copies; published versions take precedence. An unpaired scholarly review preprint is eligible but labeled unreviewed.

Open access means a lawful publisher or repository full text is publicly accessible at screening. Record the access URL and verification evidence separately from OpenAlex's OA flag. Missing full text or ambiguous relevance gives `uncertain`, not a content exclusion. Publication dates use OpenAlex metadata, checked against the source for included papers; discrepancies are documented.

## Retrieval

OpenAlex-only discovery; exact executable settings are in `work/queries.json`. Search title/abstract/keywords for each combination of two quoted phrases (`continuous sign language recognition`, `continuous sign recognition`) and three review terms (`review`, `survey`, `systematic literature review`). Add two phrase searches restricted to `type:review`; type is supplementary rather than mandatory. Search core and expansion corpora, without an OA filter, citation threshold, ranking cutoff, or desired paper count. Retrieve by publication date ascending, 100 results per page, with cursors. A pilot caps each query at one page; full retrieval follows pagination to termination within budget. Keyword matching can broaden phrase matches; eligibility requires source inspection.

## Screening and evidence

Deduplicate OpenAlex IDs and normalized DOIs, retaining query/run/page provenance. Flag conflicting metadata and possible version pairs for explicit merge decisions. First screen titles/abstracts, then inspect plausible reviews' full texts. AI suggestions are inputs in `work/screening.json`, never final human decisions; record model, prompt, and available evidence. All final human decisions initially remain `not_checked`.

Extract method families, temporal alignment, representations, datasets/sign languages, metrics/splits, generalization, reproducibility, and challenges into `work/evidence.json`. Each content assertion needs an OpenAlex ID or DOI, source URL, evidence level (`metadata_only`, `abstract_only`, `full_text`), locator and supporting passage or faithful paraphrase. Separate author statements from analyst interpretations. Use `not_reported` only after checking the relevant full text, `not_checked` when not assessed, and `unavailable` when the source cannot be obtained. An unmentioned topic is a potential review gap, not proof of an absence in the literature.

## Budget, preservation, and synthesis

Task cap: 300 OpenAlex credits cumulatively across pilot, full run, and retries. This explicit user-supplied cap takes precedence over the different percentage limit in the current on-disk AGENTS.md. Search costs 10 credits per call under documentation accessed 2026-10-25; no reranking or OpenAlex content downloads. Check account allowance before collection, reserve the request cost before sending, retain conservative charges for failed/unknown outcomes, and stop before either cap is exceeded. Do not purchase usage. Credentials use environment first, then `.env`; never save credentials in requests or logs.

Save immutable new run directories containing raw response bytes, sanitized request records, manifest, configuration/source snapshots, UTC times, outcomes, costs and cursor progress. Resume requires identical configuration and an event record. Reconstruct exports offline. Compare included AI recommendations separately from human-confirmed inclusions, reconcile all counts, and report budget/access limitations and OpenAlex-only discovery limits.
