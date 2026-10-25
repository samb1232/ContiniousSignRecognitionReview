# Decisions

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
