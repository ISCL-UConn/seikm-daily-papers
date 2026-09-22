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

### Latest issue — September 22, 2026

**60** new papers across **8** topic areas · [read on the web](https://iscl-uconn.github.io/seikm-daily-papers/) · [markdown](digests/2026-09-22.md)

**Systems Engineering and Complex Systems** (2)

- [Hierarchical Bayesian optimization of an aircraft-based multi-agent system-of-systems](https://arxiv.org/abs/2609.22130)
- [Efficient physiological control of an integrated system architecture for continuous-flow ventricular assist devices: in-silico study](https://arxiv.org/abs/2609.24966)

**Informatics for Design and Manufacturing** (11)

- [Semantics Delivery Network: Rethinking Web Retrieval Infrastructure for LLM Agents](https://arxiv.org/abs/2609.22486)
- [Schematize: An Agentic System for Generating and Refining Information-Extraction Schemas for Legal Research](https://arxiv.org/abs/2609.22209)
- [A Governance-Aware Large Language Model Orchestrated Agentic Digital Twin for Transmission System Operator Control Room Decision Support](https://arxiv.org/abs/2609.22476)
- _…8 more_

**Design, Simulation and Optimization for Advanced Manufacturing** (5)

- [A Monolithic Force-Proprioception Soft Acutuator Enabled by Single-Material 3D printing](https://arxiv.org/abs/2609.24499)
- [Artificial Neural Networks as Surrogate Models in Black Box Optimization](https://arxiv.org/abs/2609.22329)
- [K-TRAIL: Simulator-Guided Generative Design of EM/RF Circuits](https://arxiv.org/abs/2609.23183)
- _…2 more_

**Digital Twins, Manufacturing Systems, and Supply Chains** (10)

- [Benchmarking Hybrid Deep Learning Architectures for Predictive Maintenance in Industry 4.0](https://arxiv.org/abs/2609.22583)
- [Uncertainty and Business-Aware Remaining Useful Life Estimation for Semiconductor Manufacturing](https://arxiv.org/abs/2609.22160)
- [Contrastive Siamese Representation Learning for Predictive Maintenance of Electrical Submersible Pumps](https://arxiv.org/abs/2609.22360)
- _…7 more_

**Engineering Knowledge and Physics-Informed AI/ML** (10)

- [Physics-Informed Neural Network Surrogates with Polynomial Chaos-Based Uncertainty Propagation for Stochastic Model Predictive Control](https://arxiv.org/abs/2609.23077)
- [PINNForge: Execution-Grounded Evolutionary Design of Physics-Informed Neural Networks for PDE Solving via Large Language Models](https://arxiv.org/abs/2609.23023)
- [Adaptive Physics-Informed Neural Networks for the Blasius Boundary-Layer Problem](https://arxiv.org/abs/2609.22185)
- _…7 more_

**Systems Design** (2)

- [Task-Oriented Co-Design and Optimization of Geared Actuators for Robotic Applications](https://arxiv.org/abs/2609.22795)
- [NPU Accelerator: Quantized Real-Time Vehicle Detection on PYNQ-Z1 Using FINN](https://arxiv.org/abs/2609.24757)

**Emerging Topics in SEIKM** (10)

- [Toward Human-in-the-Loop Robot Failure Recovery: Bridging Communication Gaps in Human-Robot Collaboration](https://arxiv.org/abs/2609.24055)
- [ORDER: A Fictitious-World Benchmark for Domain-Adaptive Embodied AI](https://arxiv.org/abs/2609.22285)
- [AquaCap: A Training-Free Underwater Embodied Agent with Code-as-Policy](https://arxiv.org/abs/2609.23133)
- _…7 more_

**SEIKM General** (10)

- [From Documented Strengths to Force Limits: Material-Informed Robotic Insertion for Construction Assembly](https://arxiv.org/abs/2609.22609)
- [Co-occurrence Patterns of LoRA Adapters in Production Diffusion Model Inference Services](https://arxiv.org/abs/2609.23321)
- [SegTSim: A Big Data Driven Segmented Temporal Simulation Framework for Heterogeneous Multivariate Systems](https://arxiv.org/abs/2609.22192)
- _…7 more_

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
