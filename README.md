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

### Latest issue — October 6, 2026

**58** new papers across **7** topic areas · [read on the web](https://iscl-uconn.github.io/seikm-daily-papers/) · [markdown](digests/2026-10-06.md)

**Informatics for Design and Manufacturing** (14)

- [Agentic-ZTA: A Multi-Agent Architecture for Autonomous Zero Trust Enforcement](https://arxiv.org/abs/2610.05782)
- [CADForge: Agentic Single-View CAD Reconstruction with Explicit Geometry Reasoning](https://arxiv.org/abs/2610.04262)
- [Agentic schema-guided extraction of materials process knowledge from scientific literature](https://arxiv.org/abs/2610.06322)
- _…11 more_

**Design, Simulation and Optimization for Advanced Manufacturing** (3)

- [Generative World Models Enable Predictive Control of Laser Melt Pool Dynamics](https://arxiv.org/abs/2610.06250)
- [An End-to-End Framework for Modelling Pneumatic Soft Robots Based on Differentiable Finite Element Methods](https://arxiv.org/abs/2610.04612)
- [Polynomial neural surrogates for designing photonic quantum experiments](https://arxiv.org/abs/2610.06032)

**Digital Twins, Manufacturing Systems, and Supply Chains** (6)

- [Integrating Survival-Based Aging Models with Data-Driven RUL Prognostics](https://arxiv.org/abs/2610.06128)
- [GrayShield: Bit-Level Sanitization for Transformer Model Supply-Chain Security](https://arxiv.org/abs/2610.04319)
- [Detecting Defects that Matter: An Application-Driven Benchmark for Anomaly Detection in Manufacturing and Retail Logistics (VAND 4.0 Challenge)](https://arxiv.org/abs/2610.04392)
- _…3 more_

**Engineering Knowledge and Physics-Informed AI/ML** (14)

- [Label-free physics-informed strength reduction and a neural operator for the reliability of spatially variable slopes](https://arxiv.org/abs/2610.04828)
- [CEENs: Causality-enforced evolutional networks for solving time-dependent partial differential equations](https://arxiv.org/abs/2610.04405)
- [Component-Level Evaluation of Adaptive PINN Training for CFD-Oriented Crystal Growth Simulation](https://arxiv.org/abs/2610.05127)
- _…11 more_

**Systems Design** (3)

- [AnchorGen: Anchored Optimization for Customizable Generative 3D Design](https://arxiv.org/abs/2610.06135)
- [Adaptive Partitioning Schemes for Optimistic Optimization](https://arxiv.org/abs/2610.04039)
- [Adaptive Inductor and Frequency Management for Integrated Power Converters](https://arxiv.org/abs/2610.06555)

**Emerging Topics in SEIKM** (14)

- [Beyond LLM Serving: Characterizing Vision-Language-Action Workloads for Embodied AI System Design](https://arxiv.org/abs/2610.05062)
- [Now You Feel It, Now You See Me: Digital-Twin-based Teleoperation Interface for Dexterous Manipulation](https://arxiv.org/abs/2610.05081)
- [Grounded in Time: A Multi-Source Dataset and Benchmark for Temporal Grounding in Robotic Manipulation](https://arxiv.org/abs/2610.04255)
- _…11 more_

**SEIKM General** (4)

- [Model-Guided Design of Nanoparticle Dispersity through Process-Chain Optimization](https://arxiv.org/abs/2610.06155)
- [Shapley-based Structural Analysis of Neural Calibration for Stochastic Volatility Models](https://arxiv.org/abs/2610.03076)
- [Visual Swarm Navigation via Deep Reinforcement Learning and Evolutionary Hybrid Design](https://arxiv.org/abs/2610.06400)
- _…1 more_

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
