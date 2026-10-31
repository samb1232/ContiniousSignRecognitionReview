# Screening execution instructions

Apply the user task in ai-screening-prompt.md and the current protocol, with these approved plan refinements:

- Screen the fixed 34 candidates using three agents, assigned sorted OpenAlex IDs round-robin. The lead integrates records and audits evidence.
- Start with title/abstract assessment. Inspect available full text for plausible or unresolved candidates. Retrieve missing material only for existing candidates through publisher/DOI and one repository or author route; do not run discovery searches.
- Preserve separate title/abstract history when progressing to full text. Apply M1–M3 and the project-specific full-text comparison threshold, naming at least two distinct prior CSLR studies for eligible reviews.
- Keep human decisions not_screened. AI verdicts are proposals. Record access limitations and date conflicts separately from eligibility.
- Store a short description, rationale, criterion assessments, evidence source/path/URL/locator/passage, unresolved issues, next action, and classification in structured records. Exclusions require failed criteria and evidence; uncertain verdicts require an unresolved issue and next action.
- Generate a concise, human-readable Markdown report per candidate: title, short description, and proposed verdict/stage with a short explanation. Include concise criterion/evidence links within that explanation. Cap the entire report at 150 words. Detailed audit metadata stays in JSON.
- Regenerate and verify after each integrated batch. Preserve discovery provenance and the existing HTML layout.
