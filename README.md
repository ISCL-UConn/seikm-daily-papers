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

### Latest issue — October 28, 2026

**52** new papers across **8** topic areas · [read on the web](https://iscl-uconn.github.io/seikm-daily-papers/) · [markdown](digests/2026-10-28.md)

**Systems Engineering and Complex Systems** (1)

- [MARQ: A Modular, LLM-Agnostic Requirement Quality Assessor Infused with Systems Engineering Knowledge](https://arxiv.org/abs/2610.36234)

**Informatics for Design and Manufacturing** (14)

- [OA-RAG: Ontology-based Agentic RAG for Faithful LLM Reasoning](https://arxiv.org/abs/2610.36335)
- [Grounding LLM Agents in Business Processes: Process-Aware Knowledge Graphs for Reliable Multi-Step Service Invocation](https://arxiv.org/abs/2610.37242)
- [SFE-O: An Ontology for Knowledge-Grounded AI in Supercritical CO₂ Biomass Extraction and Fractionation](https://arxiv.org/abs/2610.37123)
- _…11 more_

**Design, Simulation and Optimization for Advanced Manufacturing** (3)

- [When Can a Learned Design Surrogate Be Trusted in a Self-Driving Microfluidics Laboratory? An Offline Closed-Loop Framework Built and Tested on Six Public Tables](https://arxiv.org/abs/2610.36395)
- [Finite Element Modeling of Fracture in Brittle Foods with Physically Consistent Parameter Calibration: A Practical Case Study on Cooled Dark Chocolate](https://arxiv.org/abs/2610.37124)
- [Co-Optimization of Network Topology and Variable Impedance Devices under Dynamic Line Ratings Using Iterative McCormick Relaxation](https://arxiv.org/abs/2610.36871)

**Digital Twins, Manufacturing Systems, and Supply Chains** (7)

- [Robust global supply chain reconfiguration under tariff and geopolitical uncertainty](https://arxiv.org/abs/2610.36977)
- [Pneuma: A Large-Scale Real-World Time Series Benchmark for Commercial Aircraft Predictive Maintenance](https://arxiv.org/abs/2610.37563)
- [ObjectTwin: Measuring the Asset Correspondence Gap for Capture-Anchored Digital Twins](https://arxiv.org/abs/2610.35904)
- _…4 more_

**Engineering Knowledge and Physics-Informed AI/ML** (14)

- [QD-PINN:A Physics-Informed Neural Network Approach to Bayesian Quickest Detection in High-Dimensional Diffusions](https://arxiv.org/abs/2610.37473)
- [AMOR: Adaptive Modal Operator Refinement for Operator Learning on Arbitrary Meshes and Irregular 3D Geometries](https://arxiv.org/abs/2610.37485)
- [Physics-Guided Flow Matching: A Generative AI Framework for Global Total Electron Content Forecasting](https://arxiv.org/abs/2610.37159)
- _…11 more_

**Systems Design** (4)

- [A Bi-level Co-design Framework for Lunar Monoped with 2D Jump and Landing Control](https://arxiv.org/abs/2610.37199)
- [Condition-Enhanced Generative Adversarial Network for Aerodynamic Configuration Design of Commercial Aircraft](https://arxiv.org/abs/2610.35963)
- [Structure-Actuation Co-Design of All-Electric Heavy-Duty Robotic Manipulators](https://arxiv.org/abs/2610.36996)
- _…1 more_

**Emerging Topics in SEIKM** (6)

- [VLA-Stem: A Lightweight Safety Mechanism for Vision-Language-Action Models via Reinforcement Learning](https://arxiv.org/abs/2610.37378)
- [Understanding Human-Robot Collaboration through Joint Action](https://arxiv.org/abs/2610.37298)
- [Tokens of Motion: Primitive Motion Learning for Human-Humanoid Skill Transfer](https://arxiv.org/abs/2610.37330)
- _…3 more_

**SEIKM General** (3)

- [Generation and Verification: Human-Agent Collaboration for Safety-Critical Automotive Software Engineering](https://arxiv.org/abs/2610.35982)
- [Beyond Geometry: Hole-Edge Atomic Configuration as a Design Variable in Graphyne Kirigami](https://arxiv.org/abs/2610.36468)
- [When AI Can Build It, What Should We Assess? Rethinking Evidence of Engineering Competence](https://arxiv.org/abs/2610.36413)

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
