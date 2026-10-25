# Open-access CSLR-focused reviews since 2020

Search cutoff: 25 October 2026. This is an evidence-backed AI screening and comparison; final researcher decisions are pending.

## Search criteria and completeness

OpenAlex discovery searched titles, abstracts and keywords for each combination of “continuous sign language recognition” / “continuous sign recognition” with “review” / “survey” / “systematic literature review”, plus two supplementary `type:review` routes. Dates: 2020-01-01–2026-10-25 inclusive; corpus: all; sort: publication date ascending; page size: 100; cursor pagination; no OA, language, citation-count or ranking cutoff. Two logged title-based sensitivity searches added review/survey/challenges/understanding/critical-study terms. Exact parameters are in the saved configurations and run manifests.

Eligibility requires CSLR to be the review’s central subject and synthesis of multiple prior studies. Publisher or lawful author/repository full text must be accessible. Broad SLR/translation reviews are outside the researcher-selected scope. Unavailable full text leaves relevance/access uncertain rather than supporting a content exclusion.

The discovery routes returned **92 occurrences and 33 unique records**. A reference-triggered DOI verification added one date-disputed candidate, making **34 screened records**. All configured queries terminated; the sensitivity routes added no new IDs. Pilot pages were reused in the main full run. This describes query completeness, not exhaustive coverage of the literature.

AI suggestions: {'uncertain': 4, 'exclude': 27, 'include': 3}. Human decisions: {'not_checked': 34}. Cost: **101/300 credits** reserved; 101 successful-request credits observed. No paid OpenAlex PDF downloads or reranking. Account allowance and request-level costs are saved in the manifests.

## Reviews recommended for inclusion

| Review and open full text | Methods and representations | Datasets and evaluation | Challenges and limits of coverage |
|---|---|---|---|
| [Khan et al. (2025), Deep Learning Approaches for Continuous Sign Language Recognition: A Comprehensive Review](https://minhdl93.github.io/public/papers/asma_2025.pdf) | Spatial–temporal–alignment taxonomy; RGB, depth, pose and sensors; CNN/RNN/Transformer models, CTC and traditional approaches. | PHOENIX, CSL/CSL-Daily and other datasets; WER, signer-disjoint and unseen-sentence evaluation. Also includes isolated-sign and translation resources. | Authors discuss naturalistic data, signer diversity, non-manual cues and efficiency. Our interpretation: task mixing limits direct comparison; no reproducible review search strategy identified. |
| [SivaKumari and Raghavan (2025), A Critical Review on Video-Based Continuous Sign Language Recognition](https://www.atlantis-press.com/article/126017418.pdf) | Video feature extraction, CNN/RNN hybrids, Transformers, multimodal/gloss features, CTC and encoder–decoder recognition. | Dataset table and WER/BLEU explanations; comparisons include both continuous and isolated tasks. | Authors flag signer independence, model complexity and deployment. Our interpretation: accuracy results for isolated tasks cannot rank CSLR systems; reproducible search criteria are not reported. |
| [Kadam, More and Jadhav (2026), AI-Based Indian Sign Language Recognition](https://zenodo.org/records/23527485) | Continuous Indian SLR; summarizes multiple architectures/training methods, then concentrates on the SignFlow CNN–Transformer–CTC framework. | Indian datasets, WER versus keyword detection, pretraining/ablation and deployment results reported by SignFlow’s authors. | Explicitly critiques scripted data, signer independence, unpublished resources and non-manual omissions. Narrow, single-system emphasis; repository report with peer review unestablished, not a systematic field-wide synthesis. |

IEEE states that an Expression of Concern was issued on 22 July 2026. Retain the review as an eligible document with this explicit status flag; do not treat its claims as independently validated. [Publisher status](https://ieeexplore.ieee.org/abstract/document/10937713); notice DOI: 10.1109/ACCESS.2026.3715908. The reason for the notice was not inspected.

Section/page evidence, publication-date corrections, access verification and interpretation labels are recorded in `evidence.json`. Numerical results quoted within reviews were not independently revalidated against their primary studies.

## Focused candidates with unresolved eligibility

| Candidate | What the inspected source supports | Why unresolved |
|---|---|---|
| [Understanding vision-based continuous sign language recognition](https://link.springer.com/article/10.1007/s11042-020-08961-z) | Publisher abstract: vision-based CSLR, HMM/CRF/DTW, movement epenthesis, emerging deep learning, sensor background, benchmark datasets and performance evaluation. Omissions cannot be established from the abstract. | Centrally reviews CSLR; publisher is subscription-only and lawful open-access copy/rights not verified. Missing full text is not a content exclusion. |
| [Reviewing 25 years of continuous sign language recognition research: Advances, challenges, and prospects](https://www.sciencedirect.com/science/article/pii/S0306457324001341) | Publisher abstract: 126 studies across seven dimensions, including acquisition, cues, methods, datasets and performance; spatial/temporal/alignment taxonomy and non-manual challenges. Full-text omissions remain unchecked. | CSLR-focused review; publisher preview is paywalled, no verified public full text located. No content-based exclusion. |
| [A Critical Study of Recent Deep Learning-Based Continuous Sign Language Recognition](https://link.springer.com/article/10.1007/s12626-025-00180-y) | Publisher abstract: 32 studies and 12 benchmark datasets, movement epenthesis, HMM/CTC and deep learning, linguistic scope, acquisition, signer diversity and performance metrics. Omissions remain unchecked. | CSLR-centered review, subscription-only publisher preview; public full text not established. No content-based exclusion. |
| [Advances, Challenges and Opportunities in Continuous Sign Language Recognition](https://fci.stafpu.bu.edu.eg/Computer%20Science/1273/publications/nada%20bahaa%20ibrahim%20ahmed_1205-1227.pdf) | Inspected first page/abstract: hand tracking, facial expressions, movement epenthesis and benchmark comparison. Downloaded full text is largely scanned; whole-paper omissions were not assessed. | Focused review and public institutional PDF, but date conflict: OpenAlex 2019-12-02; PDF issue 2020; current publisher page says 2022-09-21. Retain for date/rights adjudication. |

## Potential gaps to investigate

- **A reproducible, current CSLR review** — A useful next review could publish exact searches, screening decisions and study-level extraction. The included documents did not provide a reproducible field-wide search procedure. Evidence: Khan entire paper; SivaKumari entire paper; Kadam Sections I–III.
- **Separate recognition tasks and compare compatible evaluations** — Keep isolated classification, continuous gloss recognition and spoken-language translation separate; stratify by dataset, signer split, pretraining and metric rather than ranking mixed accuracy/WER values. Evidence: Khan pp.8–9,12; SivaKumari Tables 1–3; Kadam IX.B.
- **Turn deployment challenges into an evidence audit** — Compare streaming causality, latency, hardware, unseen signers, OOV tests, public resources and uncertainty. These topics are discussed, but discussion alone does not supply a standardized cross-study audit. Evidence: Khan V; SivaKumari 3.2 and 5; Kadam IX–XI.

These are hypotheses about the inspected review coverage, not claims that the wider CSLR literature lacks such research. Signer independence, non-manual features and real-time recognition are already discussed in the inspected reviews; a new review would need more than listing these familiar challenges.

## Scope and evidence limitations

The CSLR-focused restriction excludes useful broad surveys, including Koller’s 2020 quantitative survey. Restrictive phrases and OpenAlex indexing/date errors can miss eligible reviews. One focused review was found through a reference and required a separate DOI check because OpenAlex dates it before 2020. Web searches were used to locate copies and verify already identified candidates; incidental web results were not silently added.

Publisher-access failures and uncertainty about author-upload rights prevent treating every focused candidate as verified open access. Full-text comparisons are restricted to accessible, inspected documents. An Expression of Concern is reported as a publication-status fact, without speculating about its cause. Human confirmation of screening, date conventions and the comparison remains the next research decision.

## Reproduction

Run `python3 work/scripts/report.py` to regenerate this report, corpus, screening CSV and summary from saved runs and manual inputs. Run `python3 work/scripts/verify.py` for offline reconciliation. See the README for retrieval, source download and test commands.
