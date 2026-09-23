# SEIKM Daily Papers

**A daily, automated scan of new arXiv preprints, sorted into the topic areas of the ASME IDETC-CIE SEIKM technical committee.**

📄 **[Read it on the web →](https://iscl-uconn.github.io/seikm-daily-papers/)**  ·  [Archive](https://iscl-uconn.github.io/seikm-daily-papers/archive/)  ·  [RSS](https://iscl-uconn.github.io/seikm-daily-papers/feed.xml)

Every weekday morning this repository queries arXiv, filters out everything that
isn't plausibly engineering research, sorts what's left into the seven SEIKM
topic areas, and publishes the result as a web page, a Markdown file, and an RSS
feed. Nothing is hand-picked.

It exists to do three things for the committee:

1. **Give the TC a shared window** on what's moving in our topic areas between annual meetings.
2. **Pressure-test the 2027 topic structure.** If a topic area stays empty for weeks, or SEIKM General fills up with one recurring theme, that's evidence about where the tracks should go next.
3. **Surface corresponding authors** who are publishing in scope but haven't submitted to IDETC-CIE.

<!-- SEIKM:LATEST:START -->

### Latest issue — September 23, 2026

**46** new papers across **8** topic areas · [read on the web](https://iscl-uconn.github.io/seikm-daily-papers/) · [markdown](digests/2026-09-23.md)

**Systems Engineering and Complex Systems** (2)

- [From functioning to evolving: A complex systems perspective on future self-organised federated energy communities](https://arxiv.org/abs/2609.25425)
- [Teaching Reinforcement Learning and Humanoid Robotics to High-School Students: An Expert-Validated Curriculum Design on a Low-Cost Open Platform](https://arxiv.org/abs/2609.25674)

**Informatics for Design and Manufacturing** (14)

- [Reducing Hallucinations in Large Language Models Through Integrated Self-Verification and Retrieval-Augmented Generation](https://arxiv.org/abs/2609.26229)
- [ArticleMiner: Ontology-Guided Knowledge Graph Construction from Scientific Publications](https://arxiv.org/abs/2609.25607)
- [TCMaster: Confidence-Aware Querying and Workload-Guided Physical Design for Multi-Source Traditional Chinese Medicine Knowledge Graphs](https://arxiv.org/abs/2609.25712)
- _…11 more_

**Design, Simulation and Optimization for Advanced Manufacturing** (3)

- [DeepFEAv2: Deep Learning for Transient Finite Element Analysis Beyond Structured Meshes](https://arxiv.org/abs/2609.26426)
- [Multimaterial Topology Optimization using SIMP, DMO, and gSF: A comparative study with Honeycomb tessellations](https://arxiv.org/abs/2609.25976)
- [Topology-Stratified Materials Discovery with A Flow-Based Generative Model](https://arxiv.org/abs/2609.26547)

**Digital Twins, Manufacturing Systems, and Supply Chains** (4)

- [Human-Centricity in Industry 5.0: A Survey of Worker Sensing, Adaptive Operations, and Human-in-the-Loop Systems](https://arxiv.org/abs/2609.26245)
- [Bridging the Data Gap: Digital Twin as a New Paradigm for AI-based Radio Sensing](https://arxiv.org/abs/2609.26214)
- [Multi-Term Fourier Graph Neural Network with Sample Relationship Learning for Enhanced Remaining Useful Life Prediction](https://arxiv.org/abs/2609.25179)
- _…1 more_

**Engineering Knowledge and Physics-Informed AI/ML** (5)

- [Probabilistic Physics-Informed Neural Solvers for Woods-Saxon Parameter Identification: A Coupled Forward-Inverse Approach](https://arxiv.org/abs/2609.26169)
- [Variational objectives for amortized Bayesian inference in inverse problems: The role of posterior conditioning](https://arxiv.org/abs/2609.25145)
- [Predictive Uncertainty for Neural CAE Surrogates](https://arxiv.org/abs/2609.25430)
- _…2 more_

**Systems Design** (1)

- [Zephyron: Integrated Design and Analytical Evaluation of a Solar-Assisted Mobile Manipulator for Multimodal Environmental Reconnaissance and Distributed Visual Inference](https://arxiv.org/abs/2609.25709)

**Emerging Topics in SEIKM** (14)

- [Imperfection for Precision: Upcycling Imperfect Data for High-Precision Robotic Manipulation](https://arxiv.org/abs/2609.26672)
- [MATE: Multi-Agent Virtual Teleoperation Platform for Humanoid Collaboration Data Collection](https://arxiv.org/abs/2609.26520)
- [Towards Systematic Qualification of Vision-Language Models for Automotive Perception Systems](https://arxiv.org/abs/2609.25945)
- _…11 more_

**SEIKM General** (3)

- [Differentiable Policy Transport over Multi-Layer Network Feasibility Geometry](https://arxiv.org/abs/2609.26068)
- [Learning from Humans for Proactive Assistance in Human-Robot Collaborative Transport](https://arxiv.org/abs/2609.25351)
- [Analysis of trade-offs in urban heat mitigation using a Bayesian Optimization framework for an urban canopy layer model](https://arxiv.org/abs/2609.25953)

<!-- SEIKM:LATEST:END -->

---

## The topic areas

These follow the SEIKM 2027 track proposal. Each links to its live section.

| | Topic | Scope |
|---|---|---|
| `SEIKM-01` | **Systems Engineering and Complex Systems** | MBSE, system architecture, decomposition, integration and system analysis — including research that does not use AI. |
| `SEIKM-02` | **Informatics for Design and Manufacturing** | Engineering information and knowledge management, interoperability, LLMs and agent architectures. |
| `SEIKM-03` | **Design, Simulation and Optimization for Advanced Manufacturing** | Broadened beyond additive manufacturing while explicitly retaining it. Joint topic with AMS. |
| `SEIKM-04` | **Digital Twins, Manufacturing Systems, and Supply Chains** | Design-to-operation models, production planning, scheduling and supply-chain decisions. A digital twin is not required. |
| `SEIKM-05` | **Engineering Knowledge and Physics-Informed AI/ML** | Joint with AI/ML, including scientific machine learning. |
| `SEIKM-06` | **Systems Design** | Proposed joint topic with DTM: design methods and early design decisions connected to requirements, architectures, MBSE and trade-off analysis. |
| `SEIKM-07` | **Emerging Topics in SEIKM** | Human–AI teaming, robotics and physical AI; deployability, reproducibility and reuse; cyber-physical-social systems. |
| `SEIKM-GEN` | **SEIKM General** | Fundamental and applied SEIKM research outside the named topics — deliberately kept as the catch-all and as a source of future topic areas. |

## How it works

```
arXiv RSS  →  relevance gate  →  topic scoring  →  veto  →  caps  →  publish
 17 cats       engineering        weighted         drop        readable
 3 requests    context?           phrase           adjacent    per-topic
                                  evidence         ML work     limits
```

1. **Harvest.** arXiv's daily announcement feeds are read across seventeen categories, from `cs.CE` and `eess.SY` through `cs.LG` and `math.OC`, in three requests. Newly submitted and newly cross-listed papers are kept; revisions of older work are not. The feeds carry the full day's listing, so all the filtering happens locally in the steps below. (The search API is available as a fallback and for backfill, but arXiv returns HTTP 429 to shared cloud IP ranges — which includes every CI runner — so the feeds are the primary source.)
2. **Gate.** Each paper is scored against a list of engineering-context terms. Below the threshold it is dropped. This is what keeps the digest from filling with unrelated machine learning.
3. **Score.** Each of the seven topics carries `strong` / `medium` / `weak` phrase lists. A hit in the title counts double; repeated hits get diminishing returns, so one repeated phrase can't dominate. Highest-scoring topic becomes the paper's primary topic, runners-up become `also SEIKM-0x` tags.
4. **Veto.** A paper matching an out-of-scope marker (image generation, clinical, genomics…) is dropped unless its topic evidence is strong enough to override.
5. **Rank.** Papers that only just clear the gate are ranked down, so core SEIKM work outranks a generic agentic-AI paper that happened to match a few terms.
6. **General.** Anything that clears the gate but fits no named topic lands in SEIKM General rather than being discarded.

Papers already published in an earlier issue are never repeated (`data/seen.json`), and the harvest window is wider than a day so a failed run self-heals the next morning.

## Tuning it — no code required

**The taxonomy is one editable YAML file: [`config/topics.yaml`](config/topics.yaml).**

Adding a phrase to a topic's `strong` list is a one-line pull request. Thresholds, arXiv queries and per-topic caps live in [`config/settings.yaml`](config/settings.yaml).

Every change is checked against [a labelled set of 45 real papers](tests/fixtures.yaml) before it can merge, so widening one topic can't quietly break another. See [CONTRIBUTING.md](CONTRIBUTING.md).

```bash
git clone https://github.com/ISCL-UConn/seikm-daily-papers && cd seikm-daily-papers
pip install -r requirements.txt

python3 tests/test_classifier.py -v            # see how every fixture is classified
python3 scripts/run_daily.py --dry-run         # harvest + classify, write nothing
python3 scripts/run_daily.py --source api --lookback 7   # backfill a week
```

## Following it

- **Web** — <https://iscl-uconn.github.io/seikm-daily-papers/>
- **RSS** — <https://iscl-uconn.github.io/seikm-daily-papers/feed.xml>
- **GitHub** — *Watch → Custom → Releases + Pushes* for a notification each morning
- **Markdown archive** — [`digests/`](digests/), one file per issue
- **JSON** — [`docs/latest.json`](docs/latest.json), if you want to build on it

## Caveats, stated plainly

- **Inclusion is not endorsement.** These are unreviewed preprints selected by keyword matching, not by a person and not by peer review.
- **It will mis-file things.** The classifier reads titles and abstracts only. When it gets one wrong, that's a bug report against `config/topics.yaml`.
- **Quiet days are normal.** arXiv announces Sunday through Thursday at 20:00 US Eastern. Outside that cycle the feeds are empty and no issue is published — the previous one stays up rather than being replaced by a blank page.
- **arXiv is not all of SEIKM.** A great deal of the committee's work appears in ASME journals and conference proceedings that never touch arXiv. This digest sees preprints, and preprints skew toward AI/ML-adjacent work. Read the topic distribution with that in mind.
- **It is not an ASME publication.** This is a working tool maintained for the committee, not an official society product.

## Credits

Maintained for the **ASME IDETC-CIE Systems Engineering, Information and Knowledge Management** technical committee by [Farhad Imani](mailto:farhad.imani@uconn.edu), University of Connecticut.

Paper metadata comes from the [arXiv API](https://info.arxiv.org/help/api/index.html). Thank you to arXiv for use of its open access interoperability.

Code released under the MIT License; paper metadata and abstracts remain under their original terms.
