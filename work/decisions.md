# Decisions

- 2026-10-25: Made the concise HTML report the primary project output at the researcher's request. Kept findings, queries/filters, counts, screening rules and unresolved cases; moved detailed audit material behind links. README and AGENTS.md require updates after every new result; report.py automatically regenerates the HTML/data snapshot and verify.py rejects stale outputs. No research decisions or retrieved data changed.

- 2026-10-25: Added a standalone HTML search-methods report at the researcher's request. It reads saved configurations and responses, screening inputs, corpus and evidence; no new retrieval or selection changes. All manuscript-facing counts distinguish overlapping occurrences, unique records, DOI verification, AI recommendations and pending human adjudication.

- 2026-10-25: Researcher selected **CSLR-focused only**, excluding broader recognition/translation surveys even when they have a dedicated CSLR section. Requested a reproducible comparison and explicit search criteria.
- 2026-10-25: Date range fixed to 2020-01-01–2026-10-25 inclusive. No OA filter at retrieval; verify publisher/repository access during screening to reduce OA-indexing false negatives.
- 2026-10-25: Use the explicit 300-credit task cap from supplied instructions and accepted plan, rather than the on-disk percentage rule. Current docs specify 10 credits/search ($0.001). Save conservative attempt reservations; retry failures do not create extra budget.
- 2026-10-25: No protocol, scripts, queries, or previous runs existed. Version 1 establishes the baseline. Full retrieval reuses pilot pages rather than paying for them twice; the full run records parent provenance and copied response bytes.
- 2026-10-25: Standard-library-only Python for retrieval and reporting; preserve raw bytes, source snapshots and explicit AI/human decision separation. Human confirmation remains outstanding unless the researcher supplies decisions.

## Official API documentation consulted

Accessed 2026-10-25:

- https://help.openalex.org/api/llm-quick-reference/ — endpoint, corpus selection, field selection.
- https://help.openalex.org/api/searching/ — `search.title_abstract_keywords`, quoted phrases, Boolean AND, keyword expansion and 10-credit search cost.
- https://help.openalex.org/api/authentication/ — bearer authentication, rate-limit headers, `/rate-limit`, account allowance.
- https://help.openalex.org/api/paging/ — supported 100-record page size, cursor progression and terminal empty page.
- https://help.openalex.org/access/example-costs/ — credit/USD relationship, free singleton lookups; no reranking or content API planned.

- 2026-10-25: Full-text reference inspection identified a potentially relevant 2020 review (Ibrahim et al., Advances, challenges and opportunities) absent from the eight main queries. Added a separately saved title-based sensitivity configuration with review/survey/challenges/understanding/critical-study terms, retaining both CSLR phrase variants, dates, corpus and budget. Main search and configuration remain unchanged. Targeted web searches locate access copies and verify metadata only; incidental web candidates are not silently included.

- 2026-10-25: Inspected Moni/Prakash and Cai full texts cover broad SLR despite CSLR-like titles; suggested exclusions reflect content. Similar titles do not establish duplicate publications.
- 2026-10-25: Retain Khan et al. with publisher Expression of Concern flag (issued 2026-07-22). Notice is not another review. No inference about the reason.
- 2026-10-25: Offline tests prompted fixes retaining DOI-alias provenance and conservative account debits across retries. Verification caught empty-field export schema drift; omitted empty alias metadata and restored identical derived export before successful verification. Raw bodies unchanged. Final code fixes tested offline; no extra live searches needed.

Current eligibility reset: revised M1–M3 invalidate previous screening. All candidates are not screened by AI or humans. Historical run snapshots are unchanged.
