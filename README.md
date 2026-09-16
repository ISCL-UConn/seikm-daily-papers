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

### Latest issue — September 16, 2026

**56** new papers across **8** topic areas · [read on the web](https://iscl-uconn.github.io/seikm-daily-papers/) · [markdown](digests/2026-09-16.md)

**Systems Engineering and Complex Systems** (1)

- [Models as Governed Interfaces for AI-Native MBSE: Read-Side Adequacy and Write-Side Admissibility](https://arxiv.org/abs/2609.16252)

**Informatics for Design and Manufacturing** (14)

- [Extracting ontology-compliant knowledge from scientific text describing irradiated materials using large language models](https://arxiv.org/abs/2609.17291)
- [Predicting Partial Answer Quality and Utility in Agentic Retrieval-Augmented Generation](https://arxiv.org/abs/2609.16453)
- [Symbolic Separation: Grounding Deep Agents in Knowledge Graphs for Trustworthy Operational Data Analytics](https://arxiv.org/abs/2609.17107)
- _…11 more_

**Design, Simulation and Optimization for Advanced Manufacturing** (2)

- [Extending high value components performances with Additive Manufacturing: application to naval applications](https://arxiv.org/abs/2609.17104)
- [Designing Homogeneous Ti-Nb-Fe-Sn β Titanium Alloys by PBF-LB: A Pre-Alloyed Powder Blend Strategy](https://arxiv.org/abs/2609.17476)

**Digital Twins, Manufacturing Systems, and Supply Chains** (8)

- [High-Fidelity Digital Twin Data Models by Randomized Dynamic Mode Decomposition and Deep Learning with Applications in Fluid Dynamics](https://arxiv.org/abs/2609.17101)
- [An Exemplar of a Digital Twin in Mechanical Engineering: Understanding Model Hybridization](https://arxiv.org/abs/2609.17258)
- [GANADI: Uncovering C/C++ OSS Reuse Genealogies via Pivotal Function-Based Clustering to Enhance Supply Chain Security](https://arxiv.org/abs/2609.17018)
- _…5 more_

**Engineering Knowledge and Physics-Informed AI/ML** (10)

- [Physics Informed Random Feature Neural Networks for Solving PDEs](https://arxiv.org/abs/2609.16406)
- [Development of a Physics-Informed Neural Framework, MEOWN, for Rapid Prediction of Muon Stopping Sites in Crystalline Materials, for understanding Quantum Magnet employing Muon Spectroscopy](https://arxiv.org/abs/2609.17063)
- [Stable by Construction: Variational Latent Markov Operators for Long-Horizon PDE Prediction](https://arxiv.org/abs/2609.16621)
- _…7 more_

**Systems Design** (1)

- [Towards Illusions Awareness in Cyber-Physical System's Design](https://arxiv.org/abs/2609.17260)

**Emerging Topics in SEIKM** (14)

- [SAVLA: Symmetry-Aware Vision-Language-Action Models for Robotic Manipulation](https://arxiv.org/abs/2609.16641)
- [CAD-Based Relation Learning and Geometric-Symbolic Planning for Robotic Assembly](https://arxiv.org/abs/2609.17263)
- [The Robot Data Factory](https://arxiv.org/abs/2609.16705)
- _…11 more_

**SEIKM General** (6)

- [RobResilience: Implementing and Evaluating a Resilience Framework for Cyber-Physical Embodied Systems](https://arxiv.org/abs/2609.17349)
- [A Set-Theoretic Evaluation Framework for Assessing Asset Administration Shell Instances: Towards Comparability and Suitability](https://arxiv.org/abs/2609.17062)
- [Privacy-Preserving Coordinated Operation of Multi-Player Industrial Network Using Secure Aggregation](https://arxiv.org/abs/2609.16402)
- _…3 more_

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
