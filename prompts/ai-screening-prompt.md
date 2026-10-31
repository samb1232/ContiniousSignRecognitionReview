You are the project manager coordinating a research team of AI agents.

Screen all 34 candidates in this project’s saved candidate table for eligibility in the continuous sign language recognition (CSLR) literature review. Update each paper’s AI screening decision and create a separate Markdown report explaining the assessment.

### Scope and rules

- Use the existing candidate set, saved search results, and project screening protocol. Do not run new discovery searches or add candidates.
- Read AGENTS.md and the current protocol before starting. Apply the established M1–M3 eligibility criteria and stage-specific rules; do not introduce new criteria.
- Start with title/abstract screening. Exclude only when available evidence clearly demonstrates failure of a criterion. Retain broader reviews when qualifying CSLR coverage remains possible.
- If full text is examined, record that stage and apply the protocol’s project-specific CSLR coverage threshold.
- Use saved source material first. If needed, retrieve abstracts or full texts for existing candidates and save their provenance.
- Do not infer content or findings from titles alone. Missing abstracts, inaccessible full text, or unresolved metadata require further assessment, state that explicitly if occured.

### Decisions and evidence

Use the project’s stored verdicts: include, exclude, uncertain, or not_screened. Record the screening stage so that include clearly means either advancement to full-text assessment or proposed eligibility after full-text assessment.

For each assessed paper:

- Explain the verdict briefly.
- Link every failed criterion for an exclusion and provide paper-specific supporting evidence.
- For uncertain, state the unresolved issue and the next action needed.
- Identify the evidence source and level (metadata_only, abstract_only, or full_text), with a relevant passage or page, section, or table reference.
- Never invent evidence or claim to have inspected unavailable material. If assessment cannot be completed, explicitly record the limitation.

### Deliverables

1. Update the saved screening records and regenerate the HTML report’s AI screening decision column. Preserve the candidate table, identifiers, discovery provenance, and independent manual decisions.
2. Create one Markdown report per candidate, using its stable candidate ID in the filename. Include:
   - Title, year, candidate ID, and DOI/OpenAlex ID.
   - Sources inspected, evidence level, and screening stage.
   - A brief description supported by the inspected material.
   - Assessment against M1–M3, proposed verdict, and concise rationale.
   - Supporting evidence, unresolved issues, and next action where applicable.
3. Link each candidate’s AI decision to its Markdown report and any applicable criterion anchors.
4. Edit source data and the report generator rather than generated HTML directly. Run the project’s report-generation and verification commands, and check that all 34 candidates, verdicts, counts, and links agree.

Finish with a concise summary of proposed decisions by stage, unresolved assessments, changed files, and verification results.