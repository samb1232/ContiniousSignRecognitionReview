## 1. Paper identification

- **Local ID:** Not provided. The filename prefix “9” is not treated as a confirmed study ID.
- **Title:** *Reviewing 25 years of continuous sign language recognition research: Advances, challenges, and prospects.*
- **Authors:** Sarah Alyami, Hamzah Luqman, Mohammad Hammoudeh.
- **Publication:** 2024, *Information Processing and Management*, 61, 103774.
- **DOI:** [10.1016/j.ipm.2024.103774](https://doi.org/10.1016/j.ipm.2024.103774). Bibliographic details verified on PDF p. 1.
- **Paper type:** Survey/review.
- **CSLR scope:** **CSLR-focused**. The review explicitly addresses continuous video-to-gloss recognition, distinguishes it from SLT, and organizes methods by spatial, temporal, and alignment components. Joint CSLR–SLT systems are included where recognition is involved. [PDF pp. 3–4, §§2–3]
- **Inspection:** All 32 pages were inspected, including references, tables, and figures. No access or readability limitations prevented assessment. PDF page numbers match printed pagination.


## 2. Table 1 — Survey characteristics

| ID | Title and DOI/URL | Period Covered | CSLR scope (CSLR-focused or broader survey with CSLR coverage) | Main Emphasis | Number of Included Studies and Previous Surveys | Number of previous surveys compared | Sign Languages Corpora | Input Data / Modalities | Claimed Contribution |
|---|---|---|---|---|---|---|---|---|---|
| Not provided | *Reviewing 25 years of continuous sign language recognition research: Advances, challenges, and prospects*. [DOI](https://doi.org/10.1016/j.ipm.2024.103774) | **1997–2023** in Table 1; search reportedly covers publications **until March 2024**. Preserve both statements. [p. 3, §2, Table 1] | **CSLR-focused**; discusses related SLT and joint recognition–translation architectures. [pp. 3–4] | Evolution and comparison of traditional and deep CSLR methods, emphasizing acquisition, modalities, manual/non-manual cues, spatial–temporal–alignment architectures, and benchmark performance. [pp. 13–24, §§4–5] | **126 studies reported**, reduced from 306 retrieved papers. Primary-study versus prior-survey breakdown: **Not reported**. [p. 3, §2] | **7**, counted from the seven prior-survey rows in Table 1, excluding “Our survey.” [p. 3] | **17 identifiable corpus entries** compared in Table 2: American—Purdue RVL-SLLL ASL, RWTH-BOSTON-104, ASL-Homework; German—SIGNUM, RWTH-PHOENIX-Weather, RWTH-PHOENIX-Weather-2014, RWTH-PHOENIX-Weather-2014-T, Scene-PHOENIX; Chinese—CSL, LMSLR, CSL-Daily; Arabic—Assaleh et al. (2010) corpus, ArSL for Deaf Drivers, ArabSign; Russian—TheRuSLan; Greek—Continuous GrSL; Kazakh-Russian—FluentSigners-50. [p. 7, Table 2] Other private collections and additional sign languages appear in the method review. [pp. 16, 21–22] | CSLR-specific: RGB, depth, skeleton/keypoints, optical flow, and multimodal combinations; sensor-derived hand/motion data, EMG, IMU, WiFi, RF, and radar signals. [pp. 8–11, §§3.3–3.4] | **Author claim:** comprehensive CSLR review spanning 25 years; seven-dimensional literature taxonomy; additional spatial/temporal/alignment classification of deep models; synthesis of challenges, datasets, non-manual cues, and research gaps. Positioned as broader and more CSLR-specific than preceding surveys. [pp. 1–3; p. 26, §7] |

## 3. Table 2 — CSLR thematic coverage

**Scoring:** `+` means substantive CSLR coverage is established; `−` means it is not established. Positive scores do not imply comprehensive treatment of every subtopic.

| ID | Title and DOI/URL | Publication year | Publication venue | Corpora | Data acquisition methods | CSLR challenges | Manual and non-manual cues | Visual feature models | Temporal approaches | Alignment and decoding approaches | Learning strategies and knowledge transfer | Data augmentation | Language models | Generative models | Taxonomy | Applications | Ethical risks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not provided | *Reviewing 25 years of continuous sign language recognition research: Advances, challenges, and prospects*. [DOI](https://doi.org/10.1016/j.ipm.2024.103774) | 2024 [p. 1] | *Information Processing and Management*, 61, 103774 [p. 1] | **17 identifiable entries:** Purdue RVL-SLLL ASL; RWTH-BOSTON-104; SIGNUM; Assaleh et al. (2010) corpus; RWTH-PHOENIX-Weather; RWTH-PHOENIX-Weather-2014; RWTH-PHOENIX-Weather-2014-T; CSL; TheRuSLan; ArSL for Deaf Drivers; LMSLR; Continuous GrSL; CSL-Daily; ArabSign; FluentSigners-50; ASL-Homework; Scene-PHOENIX. [p. 7, Table 2] Total including unnamed private collections: **Unclear**. | **+** Camera and sensor capture, recording settings, and device trade-offs. [pp. 6, 8–9] | **+** Boundaries, epenthesis, co-articulation, dependencies, signer variation, and generalization. [pp. 4–6, 25–26] | **+ Both:** hands, face, mouthing, head/body pose, and gaze; integration and recognition roles. [pp. 10–13] | **+** CNN/3DCNN, GCN, ViT, and handcrafted feature approaches. [pp. 14–19] | **+** RNN/LSTM/GRU, temporal convolutions, Transformers, and trade-offs. [pp. 15–18, 22–23] | **+** HMM, CTC, modified CTC, RL, DTW, and RNN-Transducer. [pp. 12–15, 19] | **+** Pretraining, pseudo-label training, distillation, multilingual and cross-lingual learning. [pp. 15–18, 22] | **+** Paired video–gloss augmentation, LM-guided augmentation, and artificial backgrounds. [pp. 6, 16, 23] | **+** RNN/n-gram and BERT-based language information for recognition/training; no substantive modern generative-LLM treatment identified. [pp. 16–19] | **+** DBN as a generative feature model for sensor-based CSLR; GAN-based gloss production also described. No diffusion coverage identified. [pp. 18–19] | **+** Explicit multidimensional taxonomy and classification of reviewed architectures. [p. 5, Fig. 3; p. 24, Table 9] | **+** Deployment requirements for online/mobile CSLR and interactive recognition with user corrections. [pp. 18, 24–26] | **−** Not found after full-text inspection; technical diversity and robustness discussion does not establish ethical-risk analysis. |

## 4. Evidence and concerns report

### Table 1 — Period Covered

- **Value/decision:** 1997–2023; stated search cutoff March 2024.
- **Evidence and reasoning:** The “Our survey” row specifies 1997–2023, whereas §2 states that relevant publications were reviewed until March 2024. [PDF p. 3, Table 1, §2]
- **Concerns:** These statements are inconsistent. The method tables also contain 2024 studies, so 2023 should not be presented as an unqualified final cutoff. [PDF pp. 20–21, Table 8]
- **Manual verification:** Preserve separate fields for the stated coverage interval and search cutoff.

### Table 1 — CSLR scope (CSLR-focused or broader survey with CSLR coverage)

- **Value/decision:** CSLR-focused.
- **Evidence and reasoning:** The review defines recognition as mapping frames to ordered glosses, explicitly distinguishes SLT, and reports excluding isolated SLR and studies not focused on recognition. [PDF pp. 3–4, §§2–3]
- **Concerns:** Individual entries include joint recognition–translation systems and some task-boundary ambiguities. A CSLR focus does not guarantee that every cited study is exclusively CSLR.
- **Manual verification:** Check ambiguous individual studies before reusing the authors’ 126-study set as a screened CSLR bibliography.

### Table 1 — Main Emphasis

- **Value/decision:** Technical evolution, categorization, and performance comparison of CSLR.
- **Evidence and reasoning:** Section 4 reviews traditional and deep architectures; §5 synthesizes acquisition, modality, cue, architecture, and benchmark trends. Table 9 explicitly separates spatial, temporal, and alignment methods. [PDF pp. 14–19, §4; pp. 22–24, §5, Table 9]
- **Concerns:** Reported benchmark results come from cited studies, not a common experimental evaluation performed by the survey authors.
- **Manual verification:** Not required for this characterization.

### Table 1 — Number of Included Studies and Previous Surveys

- **Value/decision:** 126 reported studies from 306 retrieved papers; primary-study/prior-survey breakdown Not reported.
- **Evidence and reasoning:** The retrieval and reduction figures appear explicitly in §2; the conclusion repeats the 126-study total. [PDF p. 3, §2; p. 26, §7]
- **Concerns:** The paper does not clearly reconcile this total with prior surveys or provide a separate count for primary research. Bibliography length and repeated benchmark rows are unsuitable substitutes.
- **Manual verification:** Verify the membership of the 126-study set before treating it as 126 distinct primary CSLR studies.

### Table 1 — Number of previous surveys compared

- **Value/decision:** **7, independently counted.**
- **Evidence and reasoning:** Table 1 compares Aloysius and Geetha; Wadhawan and Kumar; Rastgoo et al.; Adeyanju et al.; Al-Qurishi et al.; Papastratis, Chatzikonstantinou, et al.; and El-Alfy and Luqman. Section 2 discusses their respective limitations. The current survey’s own row is excluded. [PDF p. 3, Table 1, §2]
- **Concerns:** This is the number explicitly compared, not the number of all prior surveys cited or included within the reported 126.
- **Manual verification:** Not required.

### Table 1 — Sign Languages Corpora

- **Value/decision:** The 17 identifiable corpus entries listed below, plus discussion of additional private collections.
- **Evidence and reasoning:** Each language–corpus mapping is explicitly provided in Table 2. Broader research coverage includes additional languages in the method tables and language-distribution figure. [PDF p. 7, Table 2; pp. 16, 21, Tables 7–8; p. 22, Fig. 9]
- **Concerns:** The prose says available datasets cover six languages, but Table 2 separately labels FluentSigners-50 “Kazakh-Russian.” Preserve this label without inferring its linguistic composition. [PDF pp. 6–7]
- **Manual verification:** Resolve the language-label discrepancy and the corpus-count qualifications below.

### Table 1 — Input Data / Modalities

- **Value/decision:** Visual, pose, motion, physiological, and signal-based inputs.
- **Evidence and reasoning:** Sections 3.3–3.4 explain camera and wearable/non-wearable acquisition, RGB/depth/skeleton representations, and optical flow. The review discusses modality combinations and their recognition benefits. [PDF pp. 8–11, §§3.3–3.4, Tables 3–5]
- **Concerns:** Acquisition devices and input representations are different categories. Table 3 appears to reverse the RF/radar references relative to the prose. [PDF pp. 9–10]
- **Manual verification:** Check the RF/radar mapping before extracting device-specific study assignments.

### Table 1 — Claimed Contribution

- **Value/decision:** Author-claimed comprehensive CSLR taxonomy and synthesis of methods, resources, challenges, and gaps.
- **Evidence and reasoning:** The introduction lists contributions; §2 positions the review against earlier surveys; the conclusion specifies seven dimensions and the additional spatial/temporal/alignment classification. [PDF p. 2, §1; p. 3, §2; p. 26, §7]
- **Concerns:** Comprehensiveness and novelty are author claims, not independently established findings.
- **Manual verification:** Not required to record the claims; independent comparison is needed to assess them.

### Table 2 — Corpora

- **Value/decision:** **17 identifiable qualifying corpus entries**, counted from Table 2. The exhaustive total including unnamed private datasets is **Unclear**.
- **Evidence and reasoning:** Table 2 provides a substantive comparison by language, vocabulary, sentences, signers, samples, modality, and domain. Each entry therefore qualifies even where accompanying prose is brief.

| # | Corpus name as presented or identified in the PDF | Language as reported | Individual evidence |
|---|---|---|---|
| 1 | Purdue RVL-SLLL ASL | American | [PDF p. 7, Table 2, corresponding row] |
| 2 | RWTH-BOSTON-104 | American | [PDF p. 7, Table 2, corresponding row] |
| 3 | SIGNUM | German | [PDF p. 7, Table 2, corresponding row] |
| 4 | Assaleh et al. (2010) corpus; no dataset name supplied | Arabic | [PDF p. 7, Table 2, author-labelled row] |
| 5 | RWTH-PHOENIX-Weather | German | [PDF p. 7, Table 2, corresponding row] |
| 6 | RWTH-PHOENIX-Weather-2014 | German | [PDF p. 7, Table 2, corresponding row] |
| 7 | RWTH-PHOENIX-Weather-2014-T | German | [PDF p. 7, Table 2, corresponding row] |
| 8 | CSL | Chinese | [PDF p. 7, Table 2, corresponding row] |
| 9 | TheRuSLan | Russian | [PDF p. 7, Table 2, corresponding row] |
| 10 | ArSL for Deaf Drivers | Arabic | [PDF p. 7, Table 2, corresponding row] |
| 11 | LMSLR | Chinese | [PDF p. 7, Table 2, corresponding row] |
| 12 | Continuous GrSL | Greek | [PDF p. 7, Table 2, corresponding row] |
| 13 | CSL-Daily | Chinese | [PDF p. 7, Table 2, corresponding row] |
| 14 | ArabSign | Arabic | [PDF p. 7, Table 2, corresponding row] |
| 15 | FluentSigners-50 | Kazakh-Russian | [PDF p. 7, Table 2, corresponding row] |
| 16 | ASL-Homework | American | [PDF p. 7, Table 2, corresponding row] |
| 17 | Scene-PHOENIX | German | [PDF p. 7, Table 2, corresponding row] |

- **Concerns:** The count is an extraction from this review, not external validation of dataset suitability. The following counting decisions apply:

| Item | Treatment and reason |
|---|---|
| PHOENIX releases and Scene-PHOENIX | Counted separately because the paper identifies distinct releases, annotations, or augmented data. [PDF p. 6, §3.2] |
| Phoenix2014SI | Not added: described as a signer-independent split of Phoenix2014. [PDF p. 6] |
| CSL Split I/II; GrSL-SI/SD | Not added: evaluation partitions/protocols, not additional corpora. [PDF p. 6; p. 21, Table 8; pp. 23–24] |
| How2Sign | Excluded from the confirmed CSLR count: explicitly introduced as an SLT dataset in the acquisition discussion. [PDF p. 19, §5] |
| BSL-1K | Not added: no substantive corpus comparison or description establishing qualification was found; citation and bibliography presence are insufficient. [PDF pp. 8, 11, 22, 27] |
| Kinetics-400, Sports1M, UCF101 | Excluded: discussed as action-recognition pretraining sources, not CSLR corpora. [PDF p. 22, §5] |
| Unnamed/private collections | Additional candidates exist, but “Private” labels and sentence-count descriptions do not reliably establish distinct identities or eliminate reuse. [PDF pp. 16, 21, Tables 7–8] |

- **Manual verification:** Confirm whether the comparison database should record **17 identifiable corpora** or attempt a larger count including private collections. The latter cannot be reliably finalized from the PDF alone.

### Table 2 — Data acquisition methods

- **Value/decision:** `+`.
- **Evidence and reasoning:** The review explains camera recording, Kinect, gloves, EMG/IMU armbands, motion capture, smartwatches, WiFi, RF, and radar. It compares practical limitations such as cost, intrusiveness, noise, occlusion, and operating distance. Recording environments and crowdsourced smartphone capture are also discussed. [PDF p. 6, §3.2; pp. 8–9, §3.3]
- **Concerns:** Strong technical capture coverage does not establish coverage of recruitment ethics or consent.
- **Manual verification:** Check the RF/radar table discrepancy noted above.

### Table 2 — CSLR challenges

- **Value/decision:** `+`.
- **Evidence and reasoning:** The review explains boundary detection, movement epenthesis, co-articulation, dependencies between signs, embedded fingerspelling, and signer variation. Later sections discuss constrained datasets, unseen signers, multimodal complexity, and real-time limitations. [PDF pp. 4–5, §3.1; pp. 25–26, §6]
- **Concerns:** Some challenges also apply to broader SLR, but their connection to continuous recognition is explicit.
- **Manual verification:** Not required.

### Table 2 — Manual and non-manual cues

- **Value/decision:** `+`, **both**.
- **Evidence and reasoning:** Section 3.5 analyzes hand features and non-manual face, mouth, head, body, and gaze cues, explaining linguistic roles and integration into recognition systems. Table 6 organizes studies by cue combinations. [PDF pp. 10–13, §3.5, Table 6]
- **Concerns:** Performance improvements described for individual studies are not pooled estimates.
- **Manual verification:** Not required.

### Table 2 — Visual feature models

- **Value/decision:** `+`.
- **Evidence and reasoning:** The review examines handcrafted features, CNN and 3DCNN backbones, skeleton GCNs, and ViTs, including architectural comparisons and limitations. [PDF pp. 14–19, §§4.1–4.2; p. 24, Table 9]
- **Concerns:** Several architectures combine visual and temporal processing; categories overlap.
- **Manual verification:** Not required.

### Table 2 — Temporal approaches

- **Value/decision:** `+`.
- **Evidence and reasoning:** RNNs, LSTMs/BLSTMs, GRUs, temporal convolutions, and self-attention are reviewed in relation to sequence dependencies, variable sign lengths, and online processing. [PDF pp. 15–18, §§4.2.2–4.2.7; pp. 22–23, §5]
- **Concerns:** The temporal role of a Transformer is distinguished from its use as a visual backbone.
- **Manual verification:** Not required.

### Table 2 — Alignment and decoding approaches

- **Value/decision:** `+`.
- **Evidence and reasoning:** Section 3.6 explains frame–gloss alignment, HMMs, CTC, modified CTC objectives, and RL. Traditional methods and RNN-Transducer receive further discussion. [PDF pp. 12–15, §§3.6–4.1; p. 19, §4.2.9]
- **Concerns:** Coverage is stronger for alignment and training objectives than for detailed decoding/search algorithms.
- **Manual verification:** Not required for the positive decision.

### Table 2 — Learning strategies and knowledge transfer

- **Value/decision:** `+`.
- **Evidence and reasoning:** The review explains iterative pseudo-label training, isolated-sign pretraining, self-mutual knowledge distillation, shared multilingual backbones, and cross-lingual use of additional signs. It also compares action-recognition pretraining sources. [PDF pp. 15–17, §§4.2.2–4.2.4; p. 22, §5]
- **Concerns:** The positive score does not imply a comprehensive self-supervised-learning survey. Few-shot and semi-supervised learning appear principally as future directions. [PDF p. 25, §6.2]
- **Manual verification:** Not required.

### Table 2 — Data augmentation

- **Value/decision:** `+`.
- **Evidence and reasoning:** CMA is explained through paired deletion, substitution, and addition operations on glosses and corresponding video frames; PA-CMA uses a language model to propose labels. Scene-PHOENIX introduces artificial backgrounds, and the discussion connects augmentation with unseen-sentence recognition. [PDF p. 6, §3.2; p. 16, §4.2.2; p. 23, §5]
- **Concerns:** This is substantive but selective coverage, not a comprehensive inventory of spatial and temporal augmentation.
- **Manual verification:** Not required.

### Table 2 — Language models

- **Value/decision:** `+`.
- **Evidence and reasoning:** Concrete CSLR roles include generating augmentation labels, encoding gloss sequences with RNNs, n-gram modeling, BERT-based contextual training, and cross-modal sequence transduction. [PDF pp. 16–19, §§4.2.2–4.2.8]
- **Concerns:** Conventional and BERT-based language modeling are covered. This does not establish coverage of modern generative LLMs; a model name containing “BERT” alone is not sufficient evidence.
- **Manual verification:** Not required.

### Table 2 — Generative models

- **Value/decision:** `+`, narrowly supported; **diffusion not covered**.
- **Evidence and reasoning:** The review explicitly identifies DBN as a generative graphical model and explains its use to extract WiFi features before HMM temporal recognition. It also describes SLRGAN’s GAN-generated glosses followed by Transformer translation. [PDF p. 19, §4.2.9; p. 18, §4.2.7]
- **Concerns:** The stronger evidence concerns generative architectures used for recognition, not synthetic-video generation. GAN coverage is brief. Sign-language generation is proposed as a topic for future reviews. [PDF p. 26, §7]
- **Manual verification:** Retain `+` under the supplied broad definition. Recode if the intended column is specifically about generative **training-data synthesis**.

### Table 2 — Taxonomy

- **Value/decision:** `+`.
- **Evidence and reasoning:** Figure 3 explicitly organizes CSLR by acquisition, cues, datasets, modalities, evaluation, and approaches. Section 4 classifies methods, and Table 9 assigns studies to spatial, temporal, and alignment categories. [PDF p. 5, Fig. 3; pp. 13–19, §4; p. 24, Table 9]
- **Concerns:** Figure 3’s branch labels do not correspond exactly to the seven dimensions stated in the abstract/conclusion.
- **Manual verification:** Preserve the distinction between the claimed seven-dimensional taxonomy and the displayed diagram when reproducing it.

### Table 2 — Applications

- **Value/decision:** `+`.
- **Evidence and reasoning:** Beyond the introductory list of possible uses, the review discusses online-recognition constraints, mobile/selfie-view deployment requirements, and interactive CSLR that incorporates user corrections. [PDF p. 18, §4.2.5; p. 24, §5; pp. 25–26, §6]
- **Concerns:** Coverage concerns deployment requirements and proposed scenarios; it does not establish validated adoption or user benefit in operational deployments.
- **Manual verification:** Not required under a definition accepting substantive deployment discussion.

### Table 2 — Ethical risks

- **Value/decision:** `−`.
- **Evidence and reasoning:** **Not found after full-text inspection.** No substantive analysis was identified of consent, video privacy, community governance, representational harms, or consequences of recognition errors.
- **Concerns:** Discussion of signer diversity, underserved languages, accessibility, and technical generalization does not by itself establish ethical analysis. The competing-interest statement concerns publication disclosure. [PDF pp. 25–27]
- **Manual verification:** Not required for this coding decision.

## 5. Brief synthesis

- **Main emphasis:** A technically broad, CSLR-focused review connecting acquisition, linguistic cues, architectures, alignment, and reported benchmark performance.
- **Material limits:** Ethical risks are not substantively reviewed; generative-model and application coverage is narrower than the binary positive scores might suggest.
- **Priority checks:** Preserve the conflicting coverage dates, avoid interpreting 126 as a verified primary-study count, and retain the distinction between 17 identifiable corpus entries and an unresolved total including private collections.