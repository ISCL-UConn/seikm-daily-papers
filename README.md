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

### Latest issue — November 19, 2026

**60** new papers across **8** topic areas · [read on the web](https://iscl-uconn.github.io/seikm-daily-papers/) · [markdown](digests/2026-11-19.md)

**Systems Engineering and Complex Systems** (3)

- [Structure-Behavior Coalescence for Model-Based Systems Engineering](https://arxiv.org/abs/2611.23255)
- [Systematic Mapping Protocol. Generative AI-Augmented Requirements Engineering: A Systematic Mapping Study of Practices, Specifications, and Reuse in Software Development](https://arxiv.org/abs/2611.23349)
- [Software Engineering for LLM-Based Agents: A Lifecycle-Oriented Survey](https://arxiv.org/abs/2611.23260)

**Informatics for Design and Manufacturing** (13)

- [KnowledgeClaw: Towards Agentic Knowledge Engineering via Omnimodal Hypergraphs](https://arxiv.org/abs/2611.24294)
- [A Capability Framework for Evaluating Agentic AI Platforms in Regulated Enterprises](https://arxiv.org/abs/2611.24039)
- [NaviGATE: Noise-Aware Dual-View Generation for Multimodal Knowledge Graph Reasoning](https://arxiv.org/abs/2611.24552)
- _…10 more_

**Design, Simulation and Optimization for Advanced Manufacturing** (3)

- [Element-Wise Femoral Stress Prediction: A Hybrid Graph Neural Network Surrogate for Finite Element Analysis](https://arxiv.org/abs/2611.24274)
- [Measuring and Improving Transfer of Neural Surrogates for Vehicle Aerodynamics](https://arxiv.org/abs/2611.24843)
- [Axion: A differentiable, GPU-native finite element framework,demonstrated on phase-field fracture](https://arxiv.org/abs/2611.23682)

**Digital Twins, Manufacturing Systems, and Supply Chains** (7)

- [Optimal Production Scheduling for Multi-Product Mineral Manufacturing](https://arxiv.org/abs/2611.23699)
- [MANGO Arena: Same Seeds, Different Chains Evaluating LLM Agents in a Disrupted Supply Chain](https://arxiv.org/abs/2611.23613)
- [Conceptual full-vehicle modeling of a modular all-wheel-drive robotic ADS test platform as a foundation for a digital twin architecture](https://arxiv.org/abs/2611.24646)
- _…4 more_

**Engineering Knowledge and Physics-Informed AI/ML** (12)

- [A Systematic Analysis of a Small Optimal Subspace for Physics-Informed Neural Networks: n-DAS subset R^p](https://arxiv.org/abs/2611.23773)
- [GridForge: An Open Physics-Informed Digital Twin and Benchmark Suite for UK 11 kV Underground Distribution Cables](https://arxiv.org/abs/2611.23241)
- [LLM-Assisted Multi-Fidelity Bayesian Optimization: Fusing Expert Knowledge with Numerical Data](https://arxiv.org/abs/2611.24377)
- _…9 more_

**Systems Design** (1)

- [Architectural Design Decisions for Data Ingestion in Big Data Architectures](https://arxiv.org/abs/2611.23297)

**Emerging Topics in SEIKM** (13)

- [RePlan-VLA: Progress-Aware Replanning for Long-Horizon Vision-Language-Action Models](https://arxiv.org/abs/2611.23843)
- [ExecGap: Exploiting Command-Execution Gap for Patch Attacks on Vision-Language-Action Models](https://arxiv.org/abs/2611.23714)
- [Towards Pose-Robust Few-Shot Vision-Language-Action Models](https://arxiv.org/abs/2611.24360)
- _…10 more_

**SEIKM General** (8)

- [Gradient-Based Defensive Poisoning Against System Identification Attacks on Cyber-Physical Systems](https://arxiv.org/abs/2611.24662)
- [Plug-and-Play Sensor Evolution in Software-Defined Vehicles through Asset Administration Shells](https://arxiv.org/abs/2611.23298)
- [Panini- Feasible Grammar For Robot Designs](https://arxiv.org/abs/2611.23567)
- _…5 more_

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
