# Deep Research Dossier: Reinforcement Learning for Smart Cities on GitHub

**Scope:** Traffic signal control, autonomous driving, building energy, networks/IoT/edge, multi-agent RL frameworks, and offline/safe RL libraries.
**Method:** Repository metadata verified via the GitHub API (stars, language, license, last push date, forks) on 2026-11-06, cross-checked against paper landing pages, project websites, and README contents. Paper implementations are only credited as "official" when the authors' own project page, paper PDF, or citation block links to that repository.
**Coverage:** 60+ repositories catalogued, 55 profiled in depth, with a consolidated verdict table at the end.

---

## Executive Summary

The smart-city RL ecosystem on GitHub is layered. At the bottom sit general-purpose infrastructure that almost everything else depends on: **SUMO**, **CityFlow**, **Gymnasium**, **Stable-Baselines3**, **Ray/RLlib**, and **PettingZoo**. These are large, actively maintained, well-tested projects with permissive licenses and should be treated as defaults rather than research choices.

Above them sit domain testbeds: **sumo-rl**, **RESCO**, **LibSignal**, and **Flow** for traffic; **CARLA**, **MetaDrive**, and **HighwayEnv** for driving; **CityLearn**, **Sinergym**, **BOPTEST**, and **EnergyPlus** wrappers for buildings; **ns3-gym** for networks; **DROO** and **UAV-DDPG** for edge offloading. These are the repos a smart-city project actually builds on.

At the top are paper-specific implementations: **IntelliLight**, **PressLight**, **CoLight**, **FRAP**, **MPLight** (via the traffic-signal-control sample code), **XLight** variants, **LLMLight**, **DTLight**, **Gnu-RL**, **mbrl-hvac**, **SafePO**, and the offline-RL stacks **d3rlpy** and **CORL**. Most of these are small, frozen after publication, often missing licenses, and useful mainly as reference implementations rather than as dependencies.

Key findings:

1. **The classic TSC paper repos (IntelliLight/PressLight/CoLight/FRAP) are official but stale and unlicensed.** They remain citable references, not living codebases.
2. **RESCO is the best-engineered RL benchmark for traffic signal control** (NeurIPS 2021 D&B, GPL-3.0, real-world scenarios, active maintenance through 2025).
3. **sumo-rl is the de facto Gymnasium/PettingZoo bridge to SUMO** and is the most actively maintained TSC environment (pushed 2026-03).
4. **Offline RL has matured tooling** (d3rlpy, CORL, Minari) but **no smart-city-specific offline benchmark** exists yet; DTLight's DTRL datasets are the closest precursor.
5. **Safe RL tooling (safety-gymnasium, safe-control-gym, SafePO) is generic**, not city-specific — safety constraints for traffic/building control must be hand-designed.
6. **Building-energy RL has strong simulators (EnergyPlus, BOPTEST) but fragmented wrappers**; Beobench tried to unify them and is now explicitly unmaintained.
7. **The network/edge slice of the ecosystem is thin**: ns3-gym is the only serious simulator binding; the rest are paper one-offs.
8. **MARL frameworks (PettingZoo, RLlib, MARLlib, PyMARL/EPyMARL, MADDPG)** are mature, but PyMARL-class repos are frozen circa 2022–2024.

**Recommended core stack for a new smart-city RL project:** Gymnasium + Stable-Baselines3 (or RLlib for multi-agent) + sumo-rl/RESCO for traffic + CityLearn or Sinergym for buildings + PettingZoo for MARL interfaces + d3rlpy if offline data is involved.

---

## Methodology and Caveats

- **Stars, license, language, and last-push dates** come from the GitHub REST API, queried 2026-11-06. Star counts drift; treat them as ±5%.
- **"Official" paper code** requires an explicit link from the paper or the authors' project page. Several famous methods (AttendLight, PDLight, MPLight-as-a-standalone-repo) have **no official standalone repository**; MPLight's code is distributed through the traffic-signal-control project's sample-code repository and Google Drive links.
- **License warnings matter.** Repositories with "none" (no LICENSE file) are legally reusable only with explicit permission — a real constraint for commercial smart-city deployments.
- **Staleness** is judged by last push relative to today (2026-11-06): active (<12 months), aging (12–36 months), stale (>36 months), fossil (>60 months).

---

## Category 1: Traffic Simulation Infrastructure

### 1. eclipse-sumo/sumo
- **URL:** https://github.com/eclipse-sumo/sumo
- **Stars / Language / License / Last commit / Maintainer:** 4,261★ | C++/Python | EPL-2.0 | 2026-11-06 | Eclipse SUMO team
- **Papers:** Not a paper repo; the de facto standard microscopic traffic simulator cited by virtually all TSC RL work (Behrisch et al., 2011).
- **Key modules:** `sumo`/`sumo-gui` binaries, TraCI Python control API, libsumo (in-process, faster), netconvert/route tools, fuzzing and regression test suites.
- **RL algorithms:** None natively — control is external via TraCI/libsumo subscriptions.
- **Simulator:** IS the simulator (microscopic, multimodal, city-scale capable).
- **Quality signals:** Extensive docs, CI, large test suite, Docker images, regular releases, active issue tracker, 4.2k stars, pushed same day as this research.
- **Limitations:** TraCI's client-server loop is slow for large networks (mitigate with libsumo); steep XML configuration learning curve; GUI is X11-dependent on some platforms.
- **Best fit:** Any traffic experiment needing realism, real networks (OSM import), or established baselines (fixed-time, actuated, max-pressure).
- **VERDICT:** ESSENTIAL.

### 2. cityflow-project/CityFlow
- **URL:** https://github.com/cityflow-project/CityFlow
- **Stars / Language / License / Last commit / Maintainer:** 1,031★ | C++ | Apache-2.0 | 2025-08-19 | cityflow-project (Penn State / HKUST lineage, Zhenhui Li group)
- **Papers:** WWW 2019 demo paper "CityFlow: A Multi-Agent Reinforcement Learning Environment for Large Scale City Traffic Scenario"; the simulator behind PressLight, CoLight, FRAP, MPLight, LLMLight, and the traffic-signal-control benchmark.
- **Key modules:** `cityflow.Engine` Python API, roadnet.json/flow.json formats, multithreaded simulation core, visualization frontend, Docker, conversion tools.
- **RL algorithms:** Environment only (multi-agent by construction: one agent per intersection).
- **Simulator:** IS the simulator (claims 30–40% faster than SUMO on large grids per CBLab comparisons).
- **Quality signals:** ReadTheDocs documentation, Azure CI, Dockerfile, tests/ directory, 1k stars; but only 75 commits total and last push mid-2025 — maintenance is slow.
- **Limitations:** Single-threaded Python API interaction still bottlenecks training; no PettingZoo/Gymnasium wrapper upstream (LibSignal and pytsc provide bridges); Windows support weaker than Linux.
- **Best fit:** Reproducing the CityFlow-paper lineage (PressLight/CoLight/FRAP/LLMLight) or training at city scale where SUMO is too slow.
- **VERDICT:** ESSENTIAL (for CityFlow-based research); note the maintenance slowdown.

### 3. caradryanl/CityBrainLab (CBEngine / CBLab)
- **URL:** https://github.com/caradryanl/CityBrainLab
- **Stars / Language / License / Last commit / Maintainer:** 51★ | Python/C++ | MIT | 2025-05-30 | Chumeng Liang / Zherui HKUST-SJTU group (original `CityBrainLab/CityBrainLab` now redirects here)
- **Papers:** KDD 2023 ADS track "CBLab: Supporting the Training of Large-scale Traffic Control Policies with Scalable Traffic Simulation" (arXiv:2210.00896); supported KDD Cup 2021 City Brain Challenge.
- **Key modules:** `cbengine` (microscopic simulator claiming 100k intersections / 1M vehicles at 1:1 real time), `CBData` (100-city road-network dataset + raw-OSM-to-simulation pipeline), `CBScenario` (policy benchmark incl. FixedTime, MaxPressure, SOTL, DQN), Docker image `citybrainlab/cbengine`.
- **RL algorithms:** Baseline DQN in CBScenario; framework is policy-agnostic.
- **Simulator:** Own C++ engine (benchmarked 30–40% faster than CityFlow, >90% faster than SUMO in the paper).
- **Quality signals:** MIT license, KDD paper, Docker, documentation site (cblab-documentation.readthedocs.io); but only 51 stars, 35 commits, and the org repo was transferred — fragmentation (several forks/betas exist).
- **Limitations:** Small community; visualization UI distributed via Google Drive; Linux-first; hard to find current support; benchmark scenarios fewer than RESCO.
- **Best fit:** Research explicitly on city-scale (thousands of intersections) simulation where SUMO/CityFlow cannot scale.
- **VERDICT:** NICHE (impressive scalability, weak ecosystem).

### 4. flow-project/flow
- **URL:** https://github.com/flow-project/flow
- **Stars / Language / License / Last commit / Maintainer:** 1,192★ | Python | MIT | 2024-07-27 | flow-project (UC Berkeley PATH lineage)
- **Papers:** Cai et al., "Flow: A Modular Learning Framework for Autonomous Driving" (IEEE T-ITS); underlies many RL-for-traffic-control and ramp-metering papers.
- **Key modules:** `flow.core.env` baseline, SUMO and CityFlow backends, benchmark suites (ring road, intersection merge, grid networks), generators for networks/flows, experiment runner with hyperparameter sweeps.
- **RL algorithms:** Wrappers for PPO, DQN, DDPG, plus imitation-learning baselines; integrates with rllab and Stable Baselines.
- **Simulator:** SUMO (default) and CityFlow backends.
- **Quality signals:** MIT, extensive tutorials/website, 1.2k stars, CI; but last push 2024-07 and dependency pins are aging (older TF/rllab era).
- **Limitations:** Documentation drift versus modern Gymnasium API; heavier setup than sumo-rl; some examples reference deprecated libraries.
- **Best fit:** Combined vehicle-level control (merging, ramp metering, AV insertion) rather than pure signal-phase control.
- **VERDICT:** USEFUL (mature but aging; prefer for AV/traffic-flow experiments).

---

## Category 2: Traffic Signal Control — Environments & Benchmarks

### 5. LucasAlegre/sumo-rl
- **URL:** https://github.com/LucasAlegre/sumo-rl
- **Stars / Language / License / Last commit / Maintainer:** 1,101★ | Python | MIT | 2026-03-08 | Lucas Alegre (UFRGS)
- **Papers:** Alegre et al., "SUMO-RL" (2019); cited by RESCO, EcoLight, curriculum-learning TSC papers, and dozens of applied studies (see README's "Papers" list).
- **Key modules:** `sumo_rl` envs (single-agent `sumo-rl-v0` and multi-agent PettingZoo `sumo_multi_agent-v0`), routelib generators, emissions/queuing metrics, CSV logging, smoke-test suite.
- **RL algorithms:** Environment only; documented integrations with Gymnasium, PettingZoo, Stable-Baselines3, Ray RLlib, and others.
- **Simulator:** SUMO via TraCI/libsumo.
- **Quality signals:** MIT, PyPI package, DOI (Zenodo), pre-commit, Black, pytest, GitHub Actions, active pushes into 2026, 1.1k stars. The README explicitly tracks downstream papers.
- **Limitations:** Requires a local SUMO install; reward-function choices are simple (pressure/queue-based) — advanced rewards must be coded; networks must be prepared as SUMO files.
- **Best fit:** The default starting point for any SUMO-based single- or multi-intersection RL project; also the substrate RESCO builds on.
- **VERDICT:** ESSENTIAL.

### 6. Pi-Star-Lab/RESCO
- **URL:** https://github.com/Pi-Star-Lab/RESCO
- **Stars / Language / License / Last commit / Maintainer:** 189★ | Python | GPL-3.0 | 2025-12-11 | Pi-Star Lab (James Ault & Guni Sharon, Texas A&M)
- **Papers:** Ault & Sharon, "Reinforcement Learning Benchmarks for Traffic Signal Control" (NeurIPS 2021 Datasets & Benchmarks); follow-up CIKM 2022 cooperative-MARL paper; AAMAS 2020 interpretable-policy paper.
- **Key modules:** `resco_benchmark` package, six real-world scenarios (Cologne, Luxembourg/Ingolstadt, Salt Lake City incl. one year of demand), StateBuilder/RewardBuilder interfaces, static baselines (Fixed Time, Max Pressure, Max Wave), COOM continuous-learning integration, PFRL algorithm integrations, docs/.
- **RL algorithms:** IDQN and other value-based/policy baselines via PFRL; configured state/reward/action spaces per scenario.
- **Simulator:** SUMO (subscription API; optional libsumo for speed).
- **Quality signals:** GPL-3.0, pyproject.toml, installation docs, releases v1.0/v2.0, NeurIPS benchmark citation, active (pushed 2025-12), real-world demand data with documented licenses (CC BY-NC-SA for Cologne scenarios — note this restricts commercial use of the data).
- **Limitations:** GPL-3.0 viral license; scenario data licenses vary; smaller algorithm zoo than LibSignal; Salt Lake scenarios are heavy to run.
- **Best fit:** Rigorous, reproducible benchmarking of TSC algorithms against standardized real-world scenarios; the closest thing to an "ImageNet moment" for traffic-signal RL.
- **VERDICT:** ESSENTIAL (benchmark standard; mind GPL + data licenses).

### 7. DaRL-LibSignal/LibSignal
- **URL:** https://github.com/DaRL-LibSignal/LibSignal
- **Stars / Language / License / Last commit / Maintainer:** 204★ | Python | **No license file** | 2025-09-19 | DaRL group (Hua Wei et al., Arizona State / Penn State)
- **Papers:** Mei et al., "LibSignal: an open library for traffic signal control," *Machine Learning* (Springer, 2023); NeurIPS 2022 RL4RealLife workshop short version; associated sim-to-real papers CDC 2023 (UGAT) and AAAI 2024 (PromptGAT).
- **Key modules:** `agent/` (DQN, PressLight, CoLight, MPLight, and classical MaxPressure/FixedTime/SOTL), `world/` (SUMO, CityFlow, CBEngine bindings), `dataset/`, `converter.py` (SUMO↔CityFlow net/flow conversion), Docker images, `awesome-RL-traffic-signal-control-papers.md` reading list.
- **RL algorithms:** Traditional TSC baselines + DQN-family RL + attention-based coordination (CoLight-style) + pressure methods (PressLight/MPLight).
- **Simulator:** Cross-simulator: SUMO, CityFlow, CBEngine (CBEngine marked "currently not available" in docs at times).
- **Quality signals:** Peer-reviewed journal paper, Docker one-liner for sim2real baselines, issue templates, active pushes (2025-09); community forks exist (e.g., a maintained classroom fork) because the upstream is slow.
- **Limitations:** **No LICENSE file — all rights reserved by default**; setup is notoriously fiddly (pinned Python 3.9/PyTorch 1.11 era); Ray RLlib support listed as "developing" since 2023; upstream activity modest.
- **Best fit:** One-stop shop to run many published TSC baselines across simulators, especially if you need sim-to-real transfer pipelines.
- **VERDICT:** USEFUL (breadth is unmatched; license and setup friction are real blockers).

### 8. rbokade/pytsc
- **URL:** https://github.com/rbokade/pytsc
- **Stars / Language / License / Last commit / Maintainer:** 19★ | Python | MIT | 2025-05-02 | Rohit Bokade & Xiaoning Jin (Northwestern)
- **Papers:** Bokade & Jin, "Pytsc: A unified platform for multi-agent reinforcement learning in traffic signal control," *Sensors* 25(5):1302, 2025.
- **Key modules:** Modular MDP formulation layer, SUMO and CityFlow backends, MARL training harness, hosted documentation (rbokade.github.io/pytsc), plot notebook.
- **RL algorithms:** MARL training via common libraries; MDP components (state/reward/transition) are swappable by design.
- **Simulator:** SUMO and CityFlow behind one interface.
- **Quality signals:** MIT, peer-reviewed Sensors paper, dedicated docs site, 268 commits, pushed 2025-05; but only 19 stars and zero forks — minimal adoption so far.
- **Limitations:** Very small user base; young project; algorithm coverage not yet comparable to LibSignal/RESCO.
- **Best fit:** Academic work needing clean, modular MDP experimentation across both major simulators.
- **VERDICT:** USEFUL (promising design, early stage).

### 9. traffic-signal-control/RL_signals (+ sample-code + project site)
- **URL:** https://github.com/traffic-signal-control/RL_signals (site: https://traffic-signal-control.github.io/)
- **Stars / Language / License / Last commit / Maintainer:** 202★ (RL_signals), 46★ (sample-code), 8★ (github.io) | Markdown/Python | MIT (site) / none (READMEs) | 2020-02-03 (RL_signals), 2020-02-12 (sample-code), 2024-07-11 (site) | Zhenhui Jessie Li & Hua Wei (Penn State) and collaborators
- **Papers:** Curates the MPLight (AAAI 2020), CoLight (CIKM 2019), PressLight (KDD 2019), FRAP (CIKM 2019), and IntelliLight (KDD 2018) lineage; hosts the open datasets (Hangzhou, New York, Jinan) used by nearly all CityFlow papers. **Official MPLight code is distributed here (sample-code + Drive links), not in a standalone MPLight repo.**
- **Key modules:** Paper table with code/demo/poster links, open roadnet/flow datasets, comprehensive TSC survey, `sample-code` implementations for CoLight/PressLight/FRAP/MPLight-class methods.
- **RL algorithms:** PressLight (max-pressure DQN), CoLight (graph attention coordination), MPLight (decentralized thousand-light variant), FRAP (phase competition), IntelliLight (phase-selection DQN/LSTM).
- **Simulator:** CityFlow.
- **Quality signals:** Canonical dataset source cited by hundreds of papers; MIT-licensed project site; but the repos themselves are frozen since 2020 and code READMEs lack licenses.
- **Limitations:** No unified install; code is research-grade snapshots; TF 1.x/2.x era dependencies; site's "Code" column sometimes links Google Drive.
- **Best fit:** Obtaining the canonical datasets and the reference implementations of the CityFlow paper family.
- **VERDICT:** ESSENTIAL (as a dataset/archive resource); the code itself is STALE but authoritative.

### 10. wingsweihua/IntelliLight
- **URL:** https://github.com/wingsweihua/IntelliLight
- **Stars / Language / License / Last commit / Maintainer:** 224★ | Python | **None** | 2023-05-05 | Hua Wei (ASU, formerly Penn State)
- **Papers:** Wei, Zheng, Yao, Li, "IntelliLight: A Reinforcement Learning Approach for Intelligent Traffic Light Control," KDD 2018 — the foundational deep-RL TSC paper.
- **Key modules:** Single-intersection environment, phase-selection DQN and LSTM-based pressure variants, training/eval scripts, CityFlow integration.
- **RL algorithms:** DQN, Double-DQN-style variants, LSTM policy for phase duration.
- **Simulator:** CityFlow.
- **Quality signals:** Official author repo, 224 stars, cited thousands of times; last push 2023-05 with minimal recent commits.
- **Limitations:** No license; single-intersection focus; aging dependencies; not packaged as an installable library.
- **Best fit:** Reproducing the KDD'18 baseline or citing provenance; rarely the right base for new systems.
- **VERDICT:** USEFUL (canonical baseline; treat as read-only reference).

### 11. wingsweihua/presslight
- **URL:** https://github.com/wingsweihua/presslight
- **Stars / Language / License / Last commit / Maintainer:** 76★ | Python | **None** | 2023-05-05 | Hua Wei
- **Papers:** Wei et al., "PressLight: Learning Max Pressure Control to Coordinate Traffic Signals in Arterial Network," KDD 2019.
- **Key modules:** Network-level pressure reward, coordination-aware training on arterial grids, CityFlow configs for Hangzhou/New York-style networks.
- **RL algorithms:** DQN with max-pressure reward shaping (PressLight); used as component inside MPLight.
- **Simulator:** CityFlow.
- **Quality signals:** Official repo; modest stars; frozen since 2023.
- **Limitations:** No license; narrow scope; overlapping code with sample-code repo.
- **Best fit:** Reference implementation of pressure-based coordination.
- **VERDICT:** USEFUL (canonical but frozen).

### 12. wingsweihua/colight
- **URL:** https://github.com/wingsweihua/colight
- **Stars / Language / License / Last commit / Maintainer:** 223★ | Python | **None** | 2023-05-05 | Hua Wei
- **Papers:** Zheng et al., "CoLight: Learning Network-level Cooperation for Traffic Signal Control," CIKM 2019.
- **Key modules:** Graph-attention neighborhood aggregation across intersections, phased action heads, CityFlow experiment configs.
- **RL algorithms:** DQN with graph-attention-based neighbor feature fusion (CoLight); basis for "Advanced/Efficient CoLight" variants.
- **Simulator:** CityFlow.
- **Quality signals:** Official, 223 stars, heavily cited (and re-implemented in LibSignal, LLMTSCS baselines, etc.); frozen since 2023.
- **Limitations:** No license; TF-era code; not installable.
- **Best fit:** Reference for attention-based multi-intersection coordination.
- **VERDICT:** USEFUL (canonical reference).

### 13. gjzheng93/frap-pub
- **URL:** https://github.com/gjzheng93/frap-pub
- **Stars / Language / License / Last commit / Maintainer:** 27★ | Python | **None** | 2019-12-07 | Guanjie Zheng (Penn State)
- **Papers:** Zheng, Liu, Li, "Learning Phase Competition for Traffic Signal Control," CIKM 2019 (FRAP).
- **Key modules:** Phase-reward decomposition (competition between phases), single-intersection CityFlow experiments.
- **RL algorithms:** DQN with phase-competition reward structure (FRAP).
- **Simulator:** CityFlow.
- **Quality signals:** Official code for a highly cited method; but 27 stars, no license, no commits since 2019 — a pure archival snapshot.
- **Limitations:** Effectively unmaintained; environment drift makes reproduction effortful.
- **Best fit:** Citation provenance and reward-design ideas; LibSignal/LLMTSCS carry more runnable copies.
- **VERDICT:** STALE (archival only).

### 14. LiangZhang1996/Efficient_XLight and LiangZhang1996/Advanced_XLight
- **URLs:** https://github.com/LiangZhang1996/Efficient_XLight | https://github.com/LiangZhang1996/Advanced_XLight
- **Stars / Language / License / Last commit / Maintainer:** 27★ and 53★ | Python | GPL-3.0 | 2024-02-28 (both) | Liang Zhang / HKUST(SZ) group
- **Papers:** XLight family — efficient and advanced variants of MPLight/PressLight/CoLight ("Efficient MPLight", "Advanced MaxPressure", etc.), used as the structural basis of LLMLight's baseline suite.
- **Key modules:** Shared training harness for Efficient/Advanced MPLight, PressLight, CoLight, MaxPressure; CityFlow configs (Jinan/Hangzhou/New York); checkpointing for RL weights used in LLM distillation.
- **RL algorithms:** Efficient-* (lightweight re-implementations) and Advanced-* (improved coordination) variants of the classic deep-RL TSC models.
- **Simulator:** CityFlow.
- **Quality signals:** GPL-3.0 (unlike the unlicensed upstream repos they re-implement), peer-reviewed lineage, pushed 2024-02; small star counts.
- **Limitations:** Sparse documentation; GPL obligations; niche adoption outside the LLMLight ecosystem.
- **Best fit:** Runnable, licensed implementations of the classic baselines; the code skeleton LLMLight builds on.
- **VERDICT:** USEFUL (licensed baseline suite).

### 15. usail-hkust/LLMTSCS (LLMLight)
- **URL:** https://github.com/usail-hkust/LLMTSCS
- **Stars / Language / License / Last commit / Maintainer:** 295★ | Python | **None** (README badge says MIT but no LICENSE file) | 2025-08-12 | USAIL lab, HKUST (Siqi Lai, Zhao Xu, Weijia Zhang, Hao Liu, Hui Xiong)
- **Papers:** Lai et al., "LLMLight: Large Language Models as Traffic Signal Control Agents," **KDD 2025** (arXiv:2312.16044); Geneva Inventions Fair 2025 award; KDD'25 Audience Appreciation Award.
- **Key modules:** `run_*.py` entry points for every baseline (FixedTime, MaxPressure, PressLight, MPLight, CoLight, AttendLight, Efficient/Advanced variants), `finetune/` for LightGPT imitation + critic-guided policy refinement, `prompts/`, HuggingFace LightGPT collection (Qwen2/Llama3 backbones), vLLM inference path, nine real/synthetic datasets (Jinan, Hangzhou, New York).
- **RL algorithms:** DNN-RL baselines (PressLight, MPLight, CoLight, AttendLight, Efficient/Advanced family) + LLM agents (GPT-3.5/4, Llama-2, LightGPT) + heuristic baselines.
- **Simulator:** CityFlow (Linux required).
- **Quality signals:** KDD 2025 acceptance, Zenodo DOI, 61 commits, active (2025-08), pretrained LightGPT weights on HuggingFace, tests badges in README; but **no LICENSE file** despite the badge.
- **Limitations:** TensorFlow-cpu 2.8 + transformers pins are fragile; API-key workflows for GPT baselines; license ambiguity; CityFlow-on-Linux requirement.
- **Best fit:** State-of-the-art LLM-based TSC and the most complete baseline suite in one repo; also the place to get AttendLight-class implementations (no official AttendLight repo exists).
- **VERDICT:** ESSENTIAL (for LLM-TSC and modern baselines); fix license clarity before commercial use.

### 16. XingshuaiHuang/DTLight
- **URL:** https://github.com/XingshuaiHuang/DTLight
- **Stars / Language / License / Last commit / Maintainer:** 15★ | Python | MIT | 2024-05-10 | Xingshuai Huang, Di Wu, Benoit Boulet (Colorado School of Mines)
- **Papers:** Huang, Wu, Boulet, "Traffic Signal Control Using Lightweight Transformers: An Offline-to-Online RL Approach" (arXiv:2312.07795).
- **Key modules:** `environments/` (eight RESCO-derived scenarios), `src/` decision-transformer agent, `offline_data_generator.py`, bundled **DTRL** offline datasets (16 datasets from EMP and IDQN behavior policies).
- **RL algorithms:** Offline-to-online decision transformer (DTLight); offline datasets enable CQL/BCQ/IQL-style comparisons too.
- **Simulator:** SUMO (via RESCO scenarios).
- **Quality signals:** MIT, explicit RESCO lineage, offline datasets shipped in-repo, conda env file; but 3 commits total, 15 stars — minimal maintenance.
- **Limitations:** Tiny repo; datasets partially excluded due to GitHub size limits (regenerable via script); no license issues but no community.
- **Best fit:** The closest existing benchmark for **offline RL on traffic signals** — valuable as a starting point for smart-city offline-RL work.
- **VERDICT:** USEFUL (strategic niche: offline TSC data).

### 17. cityflow-project/CityFlowER
- **URL:** https://github.com/cityflow-project/CityFlowER
- **Stars / Language / License / Last commit / Maintainer:** 26★ | C++/Makefile | Apache-2.0 | 2024-12-19 | cityflow-project (Longchao Da, Chen Chu, Weinan Zhang, Hua Wei)
- **Papers:** Da et al., "CityFlowER: An Efficient and Realistic Traffic Simulator with Embedded Machine Learning Models," ECML/PKDD 2024.
- **Key modules:** LibTorch-embedded car-following and lane-change models inside the CityFlow core, `Imitate_cityflow/` training examples, `control_config.xml` for per-vehicle model assignment, Docker, docs.
- **RL algorithms:** Not an RL repo per se — enables learned driving models to be simulated efficiently (relevant for RL environments with realistic AV behavior).
- **Simulator:** Extended CityFlow engine.
- **Quality signals:** Apache-2.0, same org as CityFlow, Dockerfile, tests/, ECML paper; only 12 commits and 26 stars.
- **Limitations:** Early-stage release; pre-trained model zoo promised but thin; niche audience.
- **Best fit:** Realistic heterogeneous driving behavior inside CityFlow-scale simulations.
- **VERDICT:** NICHE (promising, early).

### 18. Additional TSC repositories (compact profiles)

| Repo | Stars | License | Last push | Notes | Verdict |
|---|---|---|---|---|---|
| **AndreaVidali/Deep-QLearning-Agent-for-Traffic-Signal-Control** (https://github.com/AndreaVidali/Deep-QLearning-Agent-for-Traffic-Signal-Control) | 509★ | MIT | 2026-05-24 | Single 4-way intersection DQN in SUMO; modernized Nov 2025 (uv, Python 3.13, YAML configs, CLI `tlcs`); active maintainer, zero open issues | USEFUL (best-maintained teaching/single-intersection DQN) |
| **cts198859/deeprl_signal_control** (https://github.com/cts198859/deeprl_signal_control) | 426★ | MIT | 2022-05-31 | Older SUMO deep-RL TSC framework with multiple algorithms; well starred but frozen ~4.5 years | STALE (still forked, but frozen) |
| **bstriner/gym-traffic** (https://github.com/bstriner/gym-traffic) | 77★ | None | 2017-01-12 | Early OpenAI Gym env for a simple SUMO intersection + Keras DQN | STALE (historical curiosity) |
| **zyr17/UniLight** (https://github.com/zyr17/UniLight) | 39★ | MIT | 2025-03-23 | UniLight TSC method implementation | NICHE |
| **firepd/PI-Light** (https://github.com/firepd/PI-Light) | 12★ | None | 2023-12-13 | π-Light (large-scale decentralized TSC) code | NICHE (canonical for π-Light only) |
| **junfanlin/DenseLight** (https://github.com/junfanlin/DenseLight) | 3★ | None | 2023-05-23 | DenseLight method; effectively empty footprint | STALE |
| **Laysest/tslib** (https://github.com/Laysest/tslib) | 3★ | None | 2022-07-11 | TSLib unified TSC framework (IEEE BigData 2021); Docker image exists | STALE |
| **DerKevinRiehl/sumoITScontrol** (https://github.com/DerKevinRiehl/sumoITScontrol) | 11★ | GPL-3.0 | 2026-05-09 | Classical controllers (Max-Pressure, SCOOT/SCATS, ALINEA, HERO, METALINE) for SUMO; PyPI package, CI, docs — **not RL** but the right baseline library | USEFUL (as non-RL baselines) |
| **traffic-signal-control/traffic-signal-control.github.io** (https://github.com/traffic-signal-control/traffic-signal-control.github.io) | 8★ | MIT | 2024-07-11 | Project website source (benchmark portal) | USEFUL (portal) |

---

## Category 3: Autonomous Driving

### 19. carla-simulator/carla
- **URL:** https://github.com/carla-simulator/carla
- **Stars / Language / License / Last commit / Maintainer:** 14,572★ | C++/Python | MIT | 2026-11-06 | CARLA Simulator team (Intel Collaborative Institute / CVC)
- **Papers:** Dosovitskiy et al., "CARLA: An Open Urban Driving Simulator" (CoRL 2017); basis for Leaderboard, CARLA Autonomous Driving challenge, and countless perception/planning/RL papers.
- **Key modules:** Unreal Engine-based simulator, Python API (sync/async modes), sensor suite (RGB, depth, semantic, lidar, radar), scenario runner, leaderboard harness, OpenDRIVE maps, weather/traffic manager, Docker packaging.
- **RL algorithms:** Environment only; integrates with Stable-Baselines3, RLlib, and the leaderboard's privileged-learning protocols.
- **Simulator:** IS the simulator (photorealistic, Unreal-based).
- **Quality signals:** MIT, 14.6k stars, same-day activity, extensive docs, active releases, large community; heavy requirements (GPU, Unreal build for custom maps).
- **Limitations:** Resource-hungry; complex installation on some platforms; RL training throughput far lower than lightweight envs.
- **Best fit:** Realistic urban AV research, sensor-driven policies, sim-to-real transfer studies.
- **VERDICT:** ESSENTIAL (for realistic driving RL).

### 20. metadriverse/metadrive
- **URL:** https://github.com/metadriverse/metadrive
- **Stars / Language / License / Last commit / Maintainer:** 1,274★ | Python | Apache-2.0 | 2026-10-16 | MetaDriverSE (Lei Zhu et al.)
- **Papers:** Zhu et al., "MetaDrive: Generalizing Driving Policies to Diverse Driving Scenarios via Language Model" and the original MetaDrive procedural-generation paper (CoRL/ICRA lineage); used for driving-policy generalization research.
- **Key modules:** Procedural map generation (PG mode), object-pool scenarios, top-down and first-person rendering, manager-based architecture, gymnasium-compatible envs, policy distillation utilities.
- **RL algorithms:** Environment only; documented PPO/SAC/DQN experiments; language-model-guided policy work included.
- **Simulator:** Own lightweight 3D engine (Panda3D) — much faster than CARLA.
- **Quality signals:** Apache-2.0, 1.3k stars, active (2026-10), docs, CI, growing adoption as CARLA's fast alternative.
- **Limitations:** Less photorealistic than CARLA; sensor models simpler; smaller AV-industry footprint.
- **Best fit:** Fast RL training and generalization studies where photorealism is unnecessary.
- **VERDICT:** ESSENTIAL (fast generalizable driving benchmark).

### 21. Farama-Foundation/HighwayEnv
- **URL:** https://github.com/Farama-Foundation/HighwayEnv
- **Stars / Language / License / Last commit / Maintainer:** 3,341★ | Python | MIT | 2026-10-30 | Farama Foundation (originally Eleurent)
- **Papers:** Leurent, "An Environment for Autonomous Driving Decision-Making" (2018); behind the "highway driving" RL literature (merge, roundabout, intersection, parking).
- **Key modules:** `highway-env` package: HighwayEnv, MergeEnv, RoundaboutEnv, IntersectionEnv, ParkingEnv, LaneReservationEnv, plus kinematics/bicycle models, policy visualization.
- **RL algorithms:** Environment only; canonical examples for DQN/PPO/SAC in the docs.
- **Simulator:** Lightweight 2D/2.5D driving simulator (no external engine).
- **Quality signals:** MIT, part of Farama (same org as Gymnasium/PettingZoo), 3.3k stars, CI, docs, active (2026-10), pip-installable (`pip install highway-env`).
- **Limitations:** Simplified dynamics; not suitable for sensor-level or high-fidelity claims.
- **Best fit:** Tactical driving decisions, fast prototyping, MARL driving scenarios (intersection env supports multi-agent).
- **VERDICT:** ESSENTIAL (tactical/lightweight driving).

---

## Category 4: Building Energy & HVAC

### 22. citylearn-project/CityLearn
- **URL:** https://github.com/citylearn-project/CityLearn
- **Stars / Language / License / Last commit / Maintainer:** 659★ | Python | MIT | 2026-11-06 | CityLearn project (orig. Vrikis/CSIC lineage; note: `intellisys/CityLearn` is the wrong/old path)
- **Papers:** Vazquez-Canteli et al., "CityLearn: Standardizing Research in Multi-Agent Reinforcement Learning for Demand Response and Urban Energy Management" (NeurIPS 2021 D&B / arXiv:2012.10506); used in IEA EBC Annex 85 studies.
- **Key modules:** `citylearn` package with Gymnasium v3 API, district energy simulation (buildings with thermal storage, batteries, EVs, heat pumps, PV), reward functions (RBC, default, custom), non-stationary pricing/demand signals, data-driven building models (CITYDATA), MARL-ready multi-building districts.
- **RL algorithms:** Environment only; documented with Stable-Baselines3 and RLlib examples; includes rule-based controllers as baselines.
- **Simulator:** CityLearn's own building-energy simulator (EnergyPlus-compatible data; wrapper tools exist).
- **Quality signals:** MIT, 659 stars, **pushed 2026-11-06 (same day)**, v3 release with modern Gymnasium API, active issue tracker, pip-installable, well-documented tutorials — arguably the healthiest building-RL repo.
- **Limitations:** Not a full thermodynamic engine like EnergyPlus (fidelity tradeoff); district scale still modest; some features gated behind data downloads.
- **Best fit:** Multi-agent building energy management, demand response, grid-interactive buildings — the default starting point for building-energy RL.
- **VERDICT:** ESSENTIAL.

### 23. NatLabRockies/EnergyPlus
- **URL:** https://github.com/NatLabRockies/EnergyPlus (formerly NREL/EnergyPlus; org renamed)
- **Stars / Language / License / Last commit / Maintainer:** 1,614★ | C++ | BSD-3-Clause style (GitHub reports NOASSERTION) | 2026-11-06 | National Laboratory of the Rockies (formerly NREL) / IBPSA lineage
- **Papers:** The canonical building-energy simulation engine (Crawley et al.); the plant behind Sinergym, Energym, IBM's testbed, BOPTEST co-simulations, and BuildingsBench's 900K simulations.
- **Key modules:** IDF/epw simulation engine, Python API (EnergyPlus Python plugin / Python API bindings), WeatherFile tools, unit test suite, Docker.
- **RL algorithms:** None — simulator only; RL enters via wrappers.
- **Simulator:** IS the simulator (whole-building energy, HVAC, daylighting).
- **Quality signals:** Huge star count, decades of validation, active (same-day push), extensive documentation and standards compliance (ASHRAE/IEA BESTTEST).
- **Limitations:** Slow for RL training loops (thousands of timesteps per episode); setup complexity; plugin API learning curve.
- **Best fit:** Fidelity-critical HVAC/building RL evaluation; the ground truth to validate against after training in lighter wrappers.
- **VERDICT:** ESSENTIAL (simulator foundation).

### 24. ibpsa/project1-boptest
- **URL:** https://github.com/ibpsa/project1-boptest
- **Stars / Language / License / Last commit / Maintainer:** 185★ | Modelica/Python | NOASSERTION (BSD-style) | 2026-11-05 | IBPSA Project 1 (international building simulation org)
- **Papers:** The BOPTEST framework papers (Wetter et al., "BOPTEST: A Benchmarking Platform for Building Control Strategies," e-Energy/BuildSys lineage); standard for control-algorithm comparison.
- **Key modules:** Test cases (bestest_air, bestest_hydronic, bestest_hydronic_heat_pump, multizone_residential_hydronic, singlezone_commercial_hydronic), `boptest` REST/co-simulation API, forecast interfaces, rule-based + RL-ready actuators/sensors.
- **RL algorithms:** Environment only; used with SB3/RLlib in follow-up work; includes classical MPC baselines.
- **Simulator:** Modelica buildings (via co-simulation).
- **Quality signals:** IBPSA stewardship, active (pushed 2025-11-05), documentation, standardized metrics (energy, comfort, tracking); 185 stars modest but the audience is specialized.
- **Limitations:** Modelica toolchain friction; smaller test-case zoo than Sinergym's EnergyPlus suite; license field technically NOASSERTION.
- **Best fit:** Fair comparison of building controllers (MPC vs RL) on standardized cases.
- **VERDICT:** USEFUL (standardized control benchmark).

### 25. ugr-sail/sinergym
- **URL:** https://github.com/ugr-sail/sinergym
- **Stars / Language / License / Last commit / Maintainer:** 241★ | Python | MIT | 2026-09-18 | SAIL lab, University of Granada (Javier Jiménez-Rueda et al.)
- **Papers:** Jiménez-Rueda et al., "Sinergym: A Building Simulation and Control Environment for Training and Benchmarking Reinforcement Learning Algorithms" (e-Energy 2023 / arXiv:2210.07058); part of IEA EBC Annex 85.
- **Key modules:** `sinergym` package wrapping EnergyPlus into Gymnasium envs (5Zone, datacenter, IWMullion, demo), discrete/continuous/stochastic variants, weather-based randomization, `epw` preprocessing, rule-based baseline controllers, CSV logging, vectorized envs.
- **RL algorithms:** Environment only; documented SB3 examples (PPO, DQN, A2C) and WeatherWrapper for generalization.
- **Simulator:** EnergyPlus (bundled/pre-built binaries via pip extras).
- **Quality signals:** MIT, 241 stars, **active (2026-09)**, pip-installable (`pip install sinergym`), good docs, CI, stochastic variants for robustness research.
- **Limitations:** EnergyPlus speed limits throughput; building models fewer than CityLearn's district scale; docs uneven across versions.
- **Best fit:** The most practical EnergyPlus-to-Gymnasium bridge for HVAC RL with weather robustness.
- **VERDICT:** ESSENTIAL (EnergyPlus RL wrapper default).

### 26. bsl546/energym
- **URL:** https://github.com/bsl546/energym
- **Stars / Language / License / Last commit / Maintainer:** 88★ | Python | None declared | 2021-11-17 | BSL (Barcelona Supercomputing Center / UPC) team
- **Papers:** Perez et al., "Energym: A Gym environment for building control reinforcement learning" (e-Energy 2021).
- **Key modules:** 14 building models (Apartments, Offices, MixedUse, Seminarcenter, SimpleHouse, SwissHouse variants) on EnergyPlus, `energym` Gym API, weather files.
- **RL algorithms:** Environment only.
- **Simulator:** EnergyPlus.
- **Quality signals:** Peer-reviewed; still referenced (and wrapped by Beobench); but **no pushes since 2021-11** — five years stale, no license file.
- **Limitations:** Unmaintained; EnergyPlus version drift; installation pain widely reported.
- **Best fit:** Historical comparison or specific Swiss/apartment models; otherwise prefer Sinergym.
- **VERDICT:** STALE (superseded by Sinergym for most uses).

### 27. IBM/rl-testbed-for-energyplus
- **URL:** https://github.com/IBM/rl-testbed-for-energyplus
- **Stars / Language / License / Last commit / Maintainer:** 220★ | Python | MIT | 2025-09-18 | IBM Research
- **Papers:** Moustafa et al., "Reinforcement Learning for Control of HVAC Systems" and the IBM testbed papers (e-Energy 2019 lineage).
- **Key modules:** EnergyPlus + Python testbed, DQN/PPO agent implementations, observation/action abstractions, preprocessing scripts, evaluation metrics (energy + comfort).
- **RL algorithms:** DQN, PPO (TensorFlow-era implementations) with documented hyperparameters.
- **Simulator:** EnergyPlus.
- **Quality signals:** MIT, IBM stewardship, still pushed 2025-09, 220 stars; codebase aging internally (TF1/TF2 transition) but functional.
- **Limitations:** Not Gymnasium-native; docs thinner than Sinergym; smaller scenario set.
- **Best fit:** Reference DQN/PPO HVAC baselines from IBM's published experiments.
- **VERDICT:** USEFUL (credible baselines; wrapper dated).

### 28. vermouth1992/mbrl-hvac
- **URL:** https://github.com/vermouth1992/mbrl-hvac
- **Stars / Language / License / Last commit / Maintainer:** 43★ | Jupyter Notebook | MIT | 2023-10-04 | Di Wang et al. (MBRL for HVAC group)
- **Papers:** Wang et al., model-based RL for HVAC control (paper companion; uses PETS-style MBRL and related methods).
- **Key modules:** Notebook-based experiments, EnergyPlus environment glue, MBRL agent (PETS/MBPO-style), evaluation plots.
- **RL algorithms:** Model-based RL (PETS-style planning, MBPO-style actor-critic).
- **Simulator:** EnergyPlus (via wrapper).
- **Quality signals:** MIT, paper-linked, self-contained notebooks; 43 stars, last push 2023-10 — aging but not abandoned-by-community since notebooks remain runnable.
- **Limitations:** Research-notebook form (not a library); limited docs; small audience.
- **Best fit:** Studying model-based RL sample efficiency for HVAC.
- **VERDICT:** NICHE (MBRL-specific).

### 29. INFERLab/Gnu-RL
- **URL:** https://github.com/INFERLab/Gnu-RL
- **Stars / Language / License / Last commit / Maintainer:** 60★ | Jupyter Notebook/Python | MIT | 2026-03-15 | CMU INFERLab (Bingqing Chen, Mario Bergés); forked from BingqingChen/Gnu-RL
- **Papers:** Chen, Cai, Bergés, "Gnu-RL: A Precocial Reinforcement Learning Solution for Building HVAC Control Using a Differentiable MPC Policy," BuildSys 2019.
- **Key modules:** `diff_mpc/` (bundled mpc.pytorch differentiable MPC), `eplus_env/` (EnergyPlus models: 5Zone sim/control), `ssM_env/`, imitation pretraining (`Imit_EP.py`), online PPO-MPC (`PPO_MPC_EP.py`), demo notebook.
- **RL algorithms:** Imitation pretraining from historical controller data + PPO fine-tuning with a differentiable MPC policy (precocial/deployment-safe RL).
- **Simulator:** EnergyPlus via Gym-Eplus.
- **Quality signals:** MIT, BuildSys paper, recent push 2026-03, clear deployment-safety motivation; but notebook-centric and dependent on the aging Gym-Eplus package.
- **Limitations:** Gym-Eplus is poorly maintained; EnergyPlus 8.x assumptions; small codebase.
- **Best fit:** Warm-starting HVAC RL from existing controller logs (a very practical smart-building pattern).
- **VERDICT:** USEFUL (unique deployment-safe methodology).

### 30. rdnfn/beobench
- **URL:** https://github.com/rdnfn/beobench
- **Stars / Language / License / Last commit / Maintainer:** 42★ | Python | MIT | 2024-11-26 | Arduin Findeis et al. (Waterloo/SAP lineage)
- **Papers:** Findeis et al., "Beobench: A Toolkit for Unified Access to Building Simulations for Reinforcement Learning," e-Energy 2022.
- **Key modules:** Docker-based unified API over **BOPTEST, Energym, and Sinergym** envs, YAML experiment configs, Ray RLlib agent integration, readthedocs, PyPI package.
- **RL algorithms:** Any RLlib agent + user scripts.
- **Simulator:** Aggregates BOPTEST/Energym/Sinergym (EnergyPlus + Modelica).
- **Quality signals:** MIT, e-Energy paper, excellent docs; **README explicitly states "No longer actively maintained — I recommend using the integrated building simulation tools directly."**
- **Limitations:** Officially unmaintained; Docker overhead; superseded by direct Sinergym/CityLearn use.
- **Best fit:** Reference architecture for multi-simulator building benchmarks; historical value.
- **VERDICT:** STALE (explicitly deprecated by author; use its constituent envs instead).

### 31. NatLabRockies/BuildingsBench (supporting, forecasting)
- **URL:** https://github.com/NatLabRockies/BuildingsBench (NREL/BuildingsBench redirects here)
- **Stars / Language / License / Last commit / Maintainer:** 123★ | Python/Jupyter | BSD-3-Clause | 2026-02-25 | Patrick Emami et al. (NREL → National Laboratory of the Rockies)
- **Papers:** Emami, Sahu, Graf, "BuildingsBench: A Large-Scale Dataset of 900K Buildings and Benchmark for Short-Term Load Forecasting," NeurIPS 2023 Datasets & Benchmarks.
- **Key modules:** Buildings-900K pretraining corpus (EnergyPlus/ResStock/ComStock simulations), 1,900+ real buildings from 7 datasets, PyTorch dataloaders, persistence-to-transformer baselines, zero-shot + transfer STLF evaluation, faiss-based retrieval baselines.
- **RL algorithms:** None (forecasting benchmark) — but load forecasts are standard observations/reward inputs for building-RL and grid-RL.
- **Simulator:** Uses EnergyPlus-generated stock simulations; evaluation on real meter data.
- **Quality signals:** NeurIPS D&B, BSD-3-Clause, releases (v2.0 Nov 2024), docs, active push 2026-02, pip package `buildings_bench`.
- **Limitations:** 250GB+ data footprint; forecasting not control; EnergyPlus org rename confusion (NREL → NatLabRockies).
- **Best fit:** Pretraining energy foundation models or supplying realistic demand models to building/grid RL.
- **VERDICT:** USEFUL (strategic data asset for smart-energy RL).

---

## Category 5: Networks, IoT, and Edge Offloading

### 32. tkn-tub/ns3-gym
- **URL:** https://github.com/tkn-tub/ns3-gym
- **Stars / Language / License / Last commit / Maintainer:** 698★ | C++/Python | GPL-2.0 | 2026-02-05 | TKN (Technische Universität Berlin) / TUB
- **Papers:** Wieruch et al., "Flexible User-defined Control of Cellular Networks with ns-3 and OpenAI Gym" (as cited in project); the standard ns-3↔Gym binding for telecom RL.
- **Key modules:** ns-3 module (`nnb`/opengym), ZMQ-based Python bridge, OpenAI Gym-compatible env examples (handover, scheduling, slicing demos), CMake integration.
- **RL algorithms:** Environment only; pairs with any Gym agent (docs show DQN/PPO examples).
- **Simulator:** ns-3 (network simulator) with OpenGym interface.
- **Quality signals:** GPL-2.0, 698 stars, 221 forks, **active (2026-02)**, used by multiple follow-up papers; C++ build complexity is the main barrier.
- **Limitations:** GPL-2.0; ns-3 build system friction; ZMQ dependency; documentation sparse relative to demand.
- **Best fit:** Wireless/cellular protocol RL (handover, beamforming, slicing) inside city networks.
- **VERDICT:** ESSENTIAL (for network-layer smart-city RL).

### 33. jjalcaraz-upct/network-slicing
- **URL:** https://github.com/jjalcaraz-upct/network-slicing
- **Stars / Language / License / Last commit / Maintainer:** 69★ | Python | MIT | 2024-11-19 | UPCT (Universidad Politécnica de Cartagena) group
- **Papers:** Alcaraz et al., "Reinforcement-Learning Based Network Slicing Framework for Mission-Critical IoT in B5G/6G" (IEEE TVT 2023 lineage) and related slicing papers.
- **Key modules:** Gym-style slicing environments, RL agents (DDQN/PPO-class) for RAN slice allocation, latency/SLA reward functions, emulation glue.
- **RL algorithms:** Deep Q-networks and policy-gradient variants for slice resource allocation.
- **Simulator:** Lightweight custom/abstract network models (not ns-3).
- **Quality signals:** MIT, peer-reviewed lineage, maintained to 2024-11; modest adoption (69 stars, 18 forks).
- **Limitations:** Simplified network model vs ns-3 realism; documentation scattered across papers.
- **Best fit:** IoT/mission-critical slicing policy research without ns-3 build overhead.
- **VERDICT:** USEFUL (domain-specific).

### 34. lasseufpa/rrm-slice-rl
- **URL:** https://github.com/lasseufpa/rrm-slice-rl
- **Stars / Language / License / Last commit / Maintainer:** 23★ | Python | MIT | 2023-09-02 | LASSE/UFPA (Brazil)
- **Papers:** Companion code for radio-resource-management slicing RL papers from LASSE.
- **Key modules:** Slice-level RRM environments, DQN/PPO agents, 5G-ish abstraction metrics.
- **RL algorithms:** DQN-family and PPO for slice admission/resource allocation.
- **Simulator:** Abstract RRM simulator.
- **Quality signals:** MIT, paper-linked; 23 stars, last push 2023-09 — aging.
- **Limitations:** Very small community; narrow scope.
- **Best fit:** Citation/provenance for LASSE slicing work.
- **VERDICT:** NICHE.

### 35. revenol/DROO
- **URL:** https://github.com/revenol/DROO
- **Stars / Language / License / Last commit / Maintainer:** 675★ | Python | MIT | 2021-10-28 | Huikai Xie / Zhejiang University lineage (DROO paper authors)
- **Papers:** Huang et al., "DROO: Deep Reinforcement Learning for Online Offloading in Computation Offloading Systems" (IEEE TMC 2021 / MobiCom-lineage work); one of the most-cited MEC offloading repos.
- **Key modules:** Multi-user DDPG offloading environment, channel/edge-server abstraction, training scripts for static and mobile scenarios.
- **RL algorithms:** DDPG (central), multi-agent variants discussed.
- **Simulator:** Synthetic MEC simulator (channel models, server queues).
- **Quality signals:** MIT, 675 stars, 194 forks, widely cited; **last push 2021-10** — fossilized but stable (simple code tends to keep working).
- **Limitations:** TF-era code; no maintenance; synthetic traces; not Gymnasium-native.
- **Best fit:** Baseline reference for deep-RL computation offloading in edge/city IoT.
- **VERDICT:** USEFUL (canonical but frozen).

### 36. fangvv/UAV-DDPG
- **URL:** https://github.com/fangvv/UAV-DDPG
- **Stars / Language / License / Last commit / Maintainer:** 727★ | Python | **None** | 2026-10-08 | Fang et al. (UAV trajectory/offloading group)
- **Papers:** Companion to "DDPG-Based UAV Trajectory Design for Computation Offloading" (IEEE IoT-J 2021 lineage).
- **Key modules:** UAV trajectory + user association environment, DDPG agent, channel/rayleigh models, plotting utilities.
- **RL algorithms:** DDPG (single-agent continuous control of UAV trajectory/power).
- **Simulator:** Analytic wireless + UAV kinematics simulation.
- **Quality signals:** 727 stars, actively pushed 2026-10 (surprisingly active for a paper repo); **no license file**.
- **Limitations:** No license; docs minimal; research-grade structure.
- **Best fit:** UAV-assisted edge computing RL baseline.
- **VERDICT:** USEFUL (active-ish, widely forked; license caveat).

### 37. ahmadnagib/wireless-rl-envs
- **URL:** https://github.com/ahmadnagib/wireless-rl-envs
- **Stars / Language / License / Last commit / Maintainer:** 4★ | Python | None | 2025-05-18 | individual maintainer
- **Papers:** Small collection of wireless RL environments (handover/scheduling-class tasks).
- **Key modules:** Several Gym-style wireless envs.
- **RL algorithms:** Environment-only collection.
- **Simulator:** Custom lightweight models.
- **Quality signals:** Essentially no adoption (4 stars, 0 forks).
- **Limitations:** Tiny; unverified by community.
- **Best fit:** Only if a specific env here matches your need.
- **VERDICT:** STALE/NICHE (skip unless specific need).

---

## Category 6: Multi-Agent RL Frameworks

### 38. Farama-Foundation/PettingZoo
- **URL:** https://github.com/Farama-Foundation/PettingZoo
- **Stars / Language / License / Last commit / Maintainer:** 3,553★ | Python | MIT | 2026-10-30 | Farama Foundation
- **Papers:** Terry et al., "PettingZoo: An API for Multi-Agent Reinforcement Learning" (NeurIPS 2021 Datasets & Benchmarks).
- **Key modules:** AEC (Agent Environment Cycle) and parallel APIs, multi-agent Atari/MPE/Butterfly/Atari environments, `parallel_to_aec` converters, Gymnasium interop.
- **RL algorithms:** Environment API only; pairs with SB3 (via SB3-contrib/multi-agent wrappers), RLlib, EPymarl, MARLlib.
- **Simulator:** N/A (API + reference envs); sumo-rl and HighwayEnv expose PettingZoo-compatible interfaces.
- **Quality signals:** MIT, Farama stewardship (same as Gymnasium), 3.6k stars, CI, docs, active (2026-10).
- **Limitations:** Multi-agent training libraries beyond the API are still fragmented; conversion overhead between AEC/parallel.
- **Best fit:** **The standard interface** for any multi-intersection or multi-building MARL project.
- **VERDICT:** ESSENTIAL.

### 39. ray-project/ray (RLlib)
- **URL:** https://github.com/ray-project/ray
- **Stars / Language / License / Last commit / Maintainer:** 44,222★ | Python | Apache-2.0 | 2026-11-06 | Anyscale / Ray community
- **Papers:** Moritz et al., "Ray: A Distributed Framework for Emerging AI Applications" (OSDI 2018); RLlib is the most-cited scalable RL library.
- **Key modules:** RLlib (single/multi-agent, offline, hierarchical), Train, Tune, Serve, Data — full distributed stack; PettingZoo/Gymnasium env support; checkpointing and experiment tracking.
- **RL algorithms:** PPO, DQN (Rainbow), SAC, A3C, IMPALA, MARL (MAPPO/QMIX-class via RLlib), offline (CQL/IQL via algorithms catalog), model-based options.
- **Simulator:** N/A (framework); integrates with SUMO/CityFlow/Carla wrappers community-side.
- **Quality signals:** Apache-2.0, 44k stars, same-day activity, massive docs/tests/CI, industry adoption — the heavyweight option.
- **Limitations:** Heavy dependency footprint; API churn across Ray versions; overkill for single-intersection experiments.
- **Best fit:** Large-scale or distributed smart-city training (city-wide MARL, hyperparameter sweeps, production serving).
- **VERDICT:** ESSENTIAL (for scale).

### 40. Replicable-MARL/MARLlib
- **URL:** https://github.com/Replicable-MARL/MARLlib
- **Stars / Language / License / Last commit / Maintainer:** 1,355★ | Python | MIT | 2024-11-28 | Replicable-MARL (Shapley-value credit assignment group)
- **Papers:** Guo et al., "MARLlib: A Multi-Agent Reinforcement Learning Library" (arXiv:2211.15469); companion to Shapley-value MARL papers (EC3, QPLEX-lineage extensions).
- **Key modules:** Unified API over **10+ base algorithms × 15+ environment suites**, Shapley-value credit assignment module, env adapters (including MPE, SMAC, etc.), YAML-driven configs.
- **RL algorithms:** QMIX, QPLEX, VDN, MAPPO, HAPPO, MADDPG, and more — run through one interface.
- **Simulator:** Adapters to many MARL benchmarks (not city-specific by default; sumo-rl-style envs can be adapted).
- **Quality signals:** MIT, 1.4k stars, well-organized README matrix, NeurIPS-era paper; last push 2024-11 — aging ~1 year.
- **Limitations:** Not updated for newest Gymnasium/Ray releases; city-domain adapters must be written; heavier abstraction than PyMARL.
- **Best fit:** Comparing many MARL algorithms on a custom smart-city env with minimal glue.
- **VERDICT:** USEFUL (broad algorithm matrix; maintenance slowing).

### 41. oxwhirl/pymarl (and uoe-agents/epymarl)
- **URLs:** https://github.com/oxwhirl/pymarl | https://github.com/uoe-agents/epymarl
- **Stars / Language / License / Last commit / Maintainer:** PyMARL 2,223★ / EPyMARL 741★ | Python | Apache-2.0 | PyMARL 2022-12-08 / EPyMARL 2024-09-24 | Oxford WhiRL; Edinburgh EPyMARL (Raphael John et al.)
- **Papers:** Rashid et al., "QMIX: Monotonic Value Function Factorisation for Deep Multi-Agent Reinforcement Learning" (ICML 2018) — PyMARL is the official QMIX codebase; EPyMARL extends it (arXiv:2311.15649).
- **Key modules:** QMIX/VDN/QTRAN-style value factorisation, SMAC env integration, YAML experiment configs, multi-GPU training (PyMARL), EPyMARL's algorithm extensions and cleanups.
- **RL algorithms:** QMIX, VDN, QTRAN, QPLEX (PyMARL lineage); EPyMARL adds/repairs further value-based methods.
- **Simulator:** StarCraft Multi-Agent Challenge by default; custom envs via env registry.
- **Quality signals:** Apache-2.0, official QMIX provenance, thousands of citations; **PyMARL frozen since 2022**; EPyMARL newer but last push 2024-09.
- **Limitations:** Not Gymnasium/PettingZoo-native (older env API); SMAC dependency; frozen upstream.
- **Best fit:** Value-decomposition MARL baselines (still standard comparisons in MARL papers, including some TSC MARL work).
- **VERDICT:** USEFUL (canonical but frozen; prefer EPyMARL for patches).

### 42. openai/maddpg
- **URL:** https://github.com/openai/maddpg
- **Stars / Language / License / Last commit / Maintainer:** 1,983★ | Python | MIT | 2024-04-01 | OpenAI (archived-era codebase, community-maintained forks active)
- **Papers:** Lowe et al., "Multi-Agent Actor-Critic for Mixed Cooperative-Competitive Environments" (NeurIPS 2017).
- **Key modules:** Original MADDPG implementation, MPE environments, TensorFlow 1.x code.
- **RL algorithms:** MADDPG (centralized-critic continuous control).
- **Simulator:** Multi-Particle Environments (MPE).
- **Quality signals:** MIT, original OpenAI repo, 2k stars; maintenance is cosmetic (2024 push) — TF1 codebase.
- **Limitations:** Effectively unmaintained algorithmically; TF1; superseded by more modern MADDPG reimplementations in EPymarl/MARLlib/SB3-contrib ecosystems.
- **Best fit:** Citation-grade reference for the MADDPG algorithm.
- **VERDICT:** USEFUL (canonical reference; not a modern dependency).

---

## Category 7: Offline RL, Safe RL, and Core Libraries

### 43. takuseno/d3rlpy
- **URL:** https://github.com/takuseno/d3rlpy
- **Stars / Language / License / Last commit / Maintainer:** 1,688★ | Python | MIT | 2025-09-10 | Takuma Seno
- **Papers:** Seno & Michiaki, "d3rlpy: An Offline Deep Reinforcement Learning Library" (JMLR 2022).
- **Key modules:** Offline RL algorithms (CQL, BCQ, BEAR, TD3+BC, IQL, Cal-QL, Decision Transformer, behavior cloning), dataset loaders (D4RL/Minari-compatible), online fine-tuning APIs, scikit-learn-style `fit()` interface, ONNX export.
- **RL algorithms:** The broadest single-library coverage of offline RL + offline-to-online methods.
- **Simulator:** N/A (algorithm library); works with any Gymnasium env's datasets.
- **Quality signals:** MIT, JMLR paper, 1.7k stars, active (2025-09), clean API, extensive tests, pip-installable (`pip install d3rlpy`).
- **Limitations:** Not city-specific — you must build the datasets (DTLight's DTRL is a TSC example); GPU optional but training speed typical of research libs.
- **Best fit:** **The default offline-RL library** for smart-city projects with logged data (traffic histories, building meter logs, network traces).
- **VERDICT:** ESSENTIAL (offline RL stack).

### 44. corl-team/CORL (and tinkoff-ai/CORL legacy)
- **URLs:** https://github.com/corl-team/CORL | legacy: https://github.com/tinkoff-ai/CORL
- **Stars / Language / License / Last commit / Maintainer:** corl-team 664★ / tinkoff-ai 1,376★ | Python | Apache-2.0 | corl-team 2024-02-10 / tinkoff 2023-08-03 | CORL team (moved from Tinkoff to corl-team org)
- **Papers:** Tarasov et al., "CORL: Research-grade Offline and Online Reinforcement Learning Library" (JMLR 2024; arXiv:2210.07508).
- **Key modules:** Clean re-implementations of TD3+BC, CQL, IQL, BC, AWAC, TD-MPC and online RL counterparts, unified config system, D4RL/Minari dataset adapters, reproduction tables vs original papers.
- **RL algorithms:** Offline (CQL, IQL, TD3+BC, AWAC, BC) + online (SAC, TD3, PPO) with matched evaluation protocols.
- **Simulator:** N/A (library); designed for D4RL-style benchmarks.
- **Quality signals:** Apache-2.0, JMLR paper, high-fidelity reproductions, pre-commit/tests; **corl-team last push 2024-02** (~2.7 years ago) — maintenance has slowed; use the org repo (not the legacy Tinkoff path).
- **Limitations:** Slower release cadence than d3rlpy; fewer algorithms than d3rlpy's breadth; not city-domain.
- **Best fit:** Reproducible offline-RL baselines with paper-grade fidelity comparisons.
- **VERDICT:** USEFUL (reproduction gold standard; slower-moving than d3rlpy).

### 45. Farama-Foundation/Minari
- **URL:** https://github.com/Farama-Foundation/Minari
- **Stars / Language / License / Last commit / Maintainer:** 1,771★ | Python | NOASSERTION (Farama "Other"/MIT-family terms — verify before redistribution) | 2026-10-14 | Farama Foundation
- **Papers:** Dataset-format paper (NeurIPS D&B lineage) — the successor to D4RL's format.
- **Key modules:** Standard offline-dataset format, dataset hosting/versions, `minari` CLI, conversion from D4RL, integration with d3rlpy/CORL/Gymnasium.
- **RL algorithms:** N/A (dataset layer).
- **Simulator:** N/A.
- **Quality signals:** Farama stewardship, 1.8k stars, active (2026-10), docs, CI — the future-proof offline-data standard.
- **Limitations:** Dataset zoo still smaller than D4RL's; license field technically nonstandard (NOASSERTION); smart-city datasets barely present.
- **Best fit:** Storing/versioning your own smart-city offline datasets (traffic logs, HVAC traces) in a standard format.
- **VERDICT:** ESSENTIAL (offline data infrastructure).

### 46. PKU-Alignment/safety-gymnasium
- **URL:** https://github.com/PKU-Alignment/safety-gymnasium
- **Stars / Language / License / Last commit / Maintainer:** 600★ | Python | Apache-2.0 | 2026-07-21 | PKU-Alignment (Peking University)
- **Papers:** Ji et al., "Safety-Gymnasium: A Unified Safe Reinforcement Learning Benchmark" (NeurIPS 2023 Datasets & Benchmarks).
- **Key modules:** Safe navigation (Point/Car/Doggo/Racecar/Ant agents × Circle/Goal/Button/Push), safe velocity (MuJoCo locomotion), safe vision, safe multi-agent, Isaac Gym variants; cost-constraint API (`cost` in `step`); Builder API for custom tasks.
- **RL algorithms:** Environments + companion **SafePO** library (see below) with 16 SafeRL algorithms.
- **Simulator:** MuJoCo-based (modern mujoco bindings, no mujoco-py).
- **Quality signals:** Apache-2.0, NeurIPS D&B, 600 stars, docs, active (2026-07), PyPI (`pip install safety-gymnasium`), 17k monthly downloads.
- **Limitations:** Not city-domain (robotics-style tasks); safety constraints must be re-specified for traffic/buildings; MuJoCo dependency.
- **Best fit:** Algorithm-level safe-RL benchmarking before transferring constraint methods to city envs.
- **VERDICT:** ESSENTIAL (safe-RL benchmark standard).

### 47. PKU-Alignment/Safe-Policy-Optimization (SafePO)
- **URL:** https://github.com/PKU-Alignment/Safe-Policy-Optimization
- **Stars / Language / License / Last commit / Maintainer:** 427★ | Python | Apache-2.0 | 2024-03-20 | PKU-Alignment
- **Papers:** Ji et al., "Safe Policy Optimization: A Benchmark Repository for Safe Reinforcement Learning Algorithms" (NeurIPS 2023).
- **Key modules:** 16+ SafeRL algorithms (PPO-Lag, TRPO-Lag, CPO, PCPO, RCPO, CPPO-PID, FOCOPS, CUP, MACPO, MAPPO-Lag, HAPPO, etc.), Safety-Gymnasium integration, standardized constrained-MDP training loops.
- **RL algorithms:** The broadest SafeRL algorithm collection in one repo (policy optimization with cost constraints).
- **Simulator:** Safety-Gymnasium (and custom CDPs).
- **Quality signals:** Apache-2.0, NeurIPS, algorithm-to-paper provenance table in README; last push 2024-03 — ~2.6 years quiet (code stable, pace slowed).
- **Limitations:** Not updated for newest Gymnasium versions; city domains absent.
- **Best fit:** Implementing constraint-aware RL (e.g., comfort/queue-length constraints) with trustworthy baselines.
- **VERDICT:** USEFUL (SafeRL algorithm reference; frozen-ish).

### 48. learnsyslab/safe-control-gym
- **URL:** https://github.com/learnsyslab/safe-control-gym (formerly utiasDSL; org moved)
- **Stars / Language / License / Last commit / Maintainer:** 932★ | Python | MIT | 2026-04-29 | Learning & Systems Lab (UTIAS / Daniel Jacobson, Stephen Smith et al.)
- **Papers:** Zhang et al., "safe-control-gym: A Unified Benchmark Environment for Safe and Robust RL" (CoRL 2022 / arXiv:2210.00726).
- **Key modules:** PyBullet CartPole and Quadrotor envs, **CasADi symbolic a priori dynamics and constraints**, constraint definitions (hard/soft), disturbance injection, safe-RL and robust-RL baselines, benchmark protocols.
- **RL algorithms:** Safe RL baselines (Lagrangian PPO, etc.) + robust control comparisons.
- **Simulator:** PyBullet (lightweight) with symbolic models.
- **Quality signals:** MIT, 932 stars, active (2026-04), docs, cited benchmark; moved org (utiasDSL → learnsyslab) — update bookmarks.
- **Limitations:** Quadrotor/CartPole focus, not traffic/buildings; small env zoo.
- **Best fit:** Constraint-formalization patterns (how to encode safety as CasADi constraints) transferable to city control.
- **VERDICT:** USEFUL (safety formalization reference).

### 49. Farama-Foundation/Gymnasium
- **URL:** https://github.com/Farama-Foundation/Gymnasium
- **Stars / Language / License / Last commit / Maintainer:** 12,788★ | Python | MIT | 2026-10-29 | Farama Foundation
- **Papers:** Brockman et al., "OpenAI Gym" (2016); Gymnasium is the maintained successor paper/docs lineage.
- **Key modules:** `gymnasium.Env` API, spaces, wrappers, vectorization, registered classic control/box2d/atari/mujoco envs, migration guide from Gym.
- **RL algorithms:** N/A (API); every library in this dossier targets it.
- **Simulator:** N/A.
- **Quality signals:** MIT, 12.8k stars, PyPI millions of downloads, active (2026-10), strict versioning, huge third-party env catalog (sumo-rl, safety-gymnasium, HighwayEnv all listed).
- **Limitations:** API version breaks (v0.26 → v1.0) still cause dependency pain in older city repos.
- **Best fit:** The universal environment API — non-negotiable dependency.
- **VERDICT:** ESSENTIAL.

### 50. DLR-RM/stable-baselines3
- **URL:** https://github.com/DLR-RM/stable-baselines3
- **Stars / Language / License / Last commit / Maintainer:** 13,974★ | Python | MIT | 2026-10-26 | DLR-RM (German Aerospace Center) + contributors
- **Papers:** Raffin et al., "Stable-Baselines3: Reliable Reinforcement Learning Implementations" (JMLR 2021).
- **Key modules:** PPO, A2C, SAC, TD3, DQN, DDPG (+ contrib: HER, BCQ, CQL, TQC, TRPO), `VecEnv` wrappers, checkpointing, tensorboard, on-policy/off-policy utilities.
- **RL algorithms:** The standard reliable implementations of mainstream deep RL.
- **Simulator:** N/A (library); sumo-rl/CityLearn/Sinergym docs all show SB3 examples.
- **Quality signals:** MIT, 14k stars, JMLR, **active (2026-10)**, extensive tests, docs, tutorials — the default single-agent RL library.
- **Limitations:** Single-agent focus (use RLlib/PettingZoo integrations for MARL); no built-in offline algorithms (use d3rlpy/CORL).
- **Best fit:** Training agents on any smart-city env with minimal friction.
- **VERDICT:** ESSENTIAL.

### 51. Supporting core libraries (compact profiles)

| Repo | Stars | License | Last push | Role | Verdict |
|---|---|---|---|---|---|
| **Farama-Foundation/Shimmy** (https://github.com/Farama-Foundation/Shimmy) | 933★ | MIT | 2026-10-25 | Conversion bridge: PettingZoo/Gymnasium ↔ DeepMind Lab, dm-control, etc. | USEFUL (interop glue) |
| **openai/baselines** (https://github.com/openai/baselines) | 16,778★ | MIT | 2024-08-01 | Historical PPO/A2C/DDPG reference; unmaintained algorithmically | STALE (reference only) |
| **ikostrikov/pytorch-a2c-ppo-acktr-gail** (https://github.com/ikostrikov/pytorch-a2c-ppo-acktr-gail) | 3,909★ | MIT | 2022-05-29 | Classic PyTorch PPO/A2C reference, widely copied | STALE (reference only) |
| **DLR-RM/stable-baselines3** | (see #50) | | | Core trainer | ESSENTIAL |

---

## Cross-Cutting Analysis

### Quality signals across the ecosystem
- **Best engineering (docs + CI + tests + releases):** Gymnasium, Stable-Baselines3, Ray/RLlib, PettingZoo, SUMO, CARLA, Minari, d3rlpy, CityLearn, Sinergym.
- **Best domain benchmark:** RESCO (traffic) and Safety-Gymnasium (safe RL); CityLearn for multi-building districts.
- **Worst recurring problem:** missing LICENSE files on famous paper repos (IntelliLight, PressLight, CoLight, FRAP, LibSignal, LLMLight, UAV-DDPG). For any commercial or redistributed use, this is a hard blocker — prefer the GPL-licensed XLight re-implementations or write your own.
- **Second-worst problem:** dependency drift. Many 2019–2021 repos pin TensorFlow 1.x/2.8 or pre-Gymnasium APIs; budget migration time or containerize immediately.
- **Simulator speed vs fidelity tradeoff:** CityFlow/CBEngine ≈ fast, SUMO ≈ balanced, CARLA/EnergyPlus/Modelica ≈ slow but realistic. Training in fast envs and validating in slow ones is the standard pattern (LibSignal's converter and CityFlowER both target this).

### Gaps in the ecosystem (opportunities)
1. **No maintained, licensed, unified TSC library.** LibSignal is closest but unlicensed; sumo-rl/RESCO cover SUMO only; a MIT/Apache TSC suite spanning CityFlow+SUMO with modern Gymnasium APIs does not exist.
2. **No offline smart-city benchmark.** DTLight's DTRL is a start; Minari has no traffic/building datasets; an "offline CityLearn/RESCO dataset pack" would be high-impact.
3. **Safe-RL is not yet city-informed.** Safety-Gymnasium/safe-control-gym constraints (collision, torque) do not map to queue-length caps, comfort bands, or SLA violations — domain constraint libraries are missing.
4. **Network-layer RL lacks a PettingZoo-style standard.** ns3-gym is GPL and C++-heavy; no lightweight, permissively licensed city-network gym exists.
5. **LLM+RL for TSC is emerging fast** (LLMLight KDD'25) but license hygiene and API-cost reproducibility remain unsolved.

### Recommended stacks by scenario
- **Traffic signal control (research):** sumo-rl or RESCO + Stable-Baselines3 + RL_signals datasets; add LibSignal (containerized) if you need CityFlow paper baselines; LLMTSCS for LLM baselines.
- **Traffic at city scale:** CityFlow or CBEngine + LibSignal/pytsc glue + RLlib.
- **Autonomous driving:** HighwayEnv (fast) → MetaDrive (generalization) → CARLA (fidelity), same SB3/RLlib agents throughout.
- **Building energy:** CityLearn (multi-agent districts) + Sinergym (EnergyPlus fidelity) + BOPTEST (controller bake-off); d3rlpy if using meter-log offline data.
- **Networks/edge:** ns3-gym (protocol realism) or network-slicing/DROO (algorithmic abstractions); SB3 for training.
- **MARL anywhere:** PettingZoo interface + RLlib (scale) or MARLlib/EPyMARL (algorithm breadth).
- **Offline/safe:** Minari (data) + d3rlpy or CORL (offline algorithms) + Safety-Gymnasium/SafePO (constraint methods) + safe-control-gym (constraint formalization patterns).

---

## Final Summary Table

| # | Repository | Stars | Language | Category | Verdict |
|---|---|---|---|---|---|
| 1 | https://github.com/eclipse-sumo/sumo | 4,261 | C++/Python | Traffic simulator | ESSENTIAL |
| 2 | https://github.com/cityflow-project/CityFlow | 1,031 | C++ | Traffic simulator | ESSENTIAL |
| 3 | https://github.com/caradryanl/CityBrainLab | 51 | Python | Traffic simulator (city-scale) | NICHE |
| 4 | https://github.com/flow-project/flow | 1,192 | Python | AV/traffic RL framework | USEFUL |
| 5 | https://github.com/LucasAlegre/sumo-rl | 1,101 | Python | TSC environment | ESSENTIAL |
| 6 | https://github.com/Pi-Star-Lab/RESCO | 189 | Python | TSC benchmark | ESSENTIAL |
| 7 | https://github.com/DaRL-LibSignal/LibSignal | 204 | Python | TSC library (multi-sim) | USEFUL |
| 8 | https://github.com/rbokade/pytsc | 19 | Python | TSC MARL platform | USEFUL |
| 9 | https://github.com/traffic-signal-control/RL_signals | 202 | Markdown | TSC datasets/archive | ESSENTIAL |
| 10 | https://github.com/traffic-signal-control/sample-code | 46 | Python | Official MPLight/CoLight/PressLight/FRAP code | ESSENTIAL (archive) |
| 11 | https://github.com/wingsweihua/IntelliLight | 224 | Python | KDD'18 official | USEFUL |
| 12 | https://github.com/wingsweihua/presslight | 76 | Python | KDD'19 official | USEFUL |
| 13 | https://github.com/wingsweihua/colight | 223 | Python | CIKM'19 official | USEFUL |
| 14 | https://github.com/gjzheng93/frap-pub | 27 | Python | CIKM'19 official | STALE |
| 15 | https://github.com/LiangZhang1996/Efficient_XLight | 27 | Python | Licensed baselines | USEFUL |
| 16 | https://github.com/LiangZhang1996/Advanced_XLight | 53 | Python | Licensed baselines | USEFUL |
| 17 | https://github.com/usail-hkust/LLMTSCS | 295 | Python | LLM-TSC (KDD'25) | ESSENTIAL |
| 18 | https://github.com/XingshuaiHuang/DTLight | 15 | Python | Offline-to-online TSC | USEFUL |
| 19 | https://github.com/cityflow-project/CityFlowER | 26 | C++ | Realistic sim w/ ML models | NICHE |
| 20 | https://github.com/AndreaVidali/Deep-QLearning-Agent-for-Traffic-Signal-Control | 509 | Python | Single-intersection DQN | USEFUL |
| 21 | https://github.com/cts198859/deeprl_signal_control | 426 | Python | TSC deep RL | STALE |
| 22 | https://github.com/bstriner/gym-traffic | 77 | Python | Early Gym TSC env | STALE |
| 23 | https://github.com/zyr17/UniLight | 39 | Python | TSC method | NICHE |
| 24 | https://github.com/firepd/PI-Light | 12 | Python | π-Light official | NICHE |
| 25 | https://github.com/junfanlin/DenseLight | 3 | Python | DenseLight | STALE |
| 26 | https://github.com/Laysest/tslib | 3 | Jupyter | TSC framework | STALE |
| 27 | https://github.com/DerKevinRiehl/sumoITScontrol | 11 | Python | Classical TSC/ramp baselines | USEFUL |
| 28 | https://github.com/carla-simulator/carla | 14,572 | C++/Python | Autonomous driving | ESSENTIAL |
| 29 | https://github.com/metadriverse/metadrive | 1,274 | Python | Autonomous driving | ESSENTIAL |
| 30 | https://github.com/Farama-Foundation/HighwayEnv | 3,341 | Python | Tactical driving | ESSENTIAL |
| 31 | https://github.com/citylearn-project/CityLearn | 659 | Python | Building energy MARL | ESSENTIAL |
| 32 | https://github.com/NatLabRockies/EnergyPlus | 1,614 | C++ | Building simulator | ESSENTIAL |
| 33 | https://github.com/ibpsa/project1-boptest | 185 | Modelica | Building control benchmark | USEFUL |
| 34 | https://github.com/ugr-sail/sinergym | 241 | Python | EnergyPlus Gym wrapper | ESSENTIAL |
| 35 | https://github.com/bsl546/energym | 88 | Python | Building Gym envs | STALE |
| 36 | https://github.com/IBM/rl-testbed-for-energyplus | 220 | Python | HVAC RL baselines | USEFUL |
| 37 | https://github.com/vermouth1992/mbrl-hvac | 43 | Jupyter | MBRL HVAC | NICHE |
| 38 | https://github.com/INFERLab/Gnu-RL | 60 | Jupyter | Deployment-safe HVAC RL | USEFUL |
| 39 | https://github.com/rdnfn/beobench | 42 | Python | Unified building envs | STALE (deprecated) |
| 40 | https://github.com/NatLabRockies/BuildingsBench | 123 | Python | Load-forecast dataset | USEFUL |
| 41 | https://github.com/tkn-tub/ns3-gym | 698 | C++/Python | Network simulator binding | ESSENTIAL |
| 42 | https://github.com/jjalcaraz-upct/network-slicing | 69 | Python | 5G slicing RL | USEFUL |
| 43 | https://github.com/lasseufpa/rrm-slice-rl | 23 | Python | RRM slicing RL | NICHE |
| 44 | https://github.com/revenol/DROO | 675 | Python | MEC offloading | USEFUL |
| 45 | https://github.com/fangvv/UAV-DDPG | 727 | Python | UAV offloading | USEFUL |
| 46 | https://github.com/ahmadnagib/wireless-rl-envs | 4 | Python | Wireless envs | STALE/NICHE |
| 47 | https://github.com/Farama-Foundation/PettingZoo | 3,553 | Python | MARL API | ESSENTIAL |
| 48 | https://github.com/ray-project/ray | 44,222 | Python | Distributed RL (RLlib) | ESSENTIAL |
| 49 | https://github.com/Replicable-MARL/MARLlib | 1,355 | Python | MARL algorithm suite | USEFUL |
| 50 | https://github.com/oxwhirl/pymarl | 2,223 | Python | QMIX official | USEFUL (frozen) |
| 51 | https://github.com/uoe-agents/epymarl | 741 | Python | PyMARL successor | USEFUL |
| 52 | https://github.com/openai/maddpg | 1,983 | Python | MADDPG official | USEFUL (reference) |
| 53 | https://github.com/takuseno/d3rlpy | 1,688 | Python | Offline RL | ESSENTIAL |
| 54 | https://github.com/corl-team/CORL | 664 | Python | Offline RL | USEFUL |
| 55 | https://github.com/tinkoff-ai/CORL | 1,376 | Python | Offline RL (legacy path) | USEFUL (prefer corl-team) |
| 56 | https://github.com/Farama-Foundation/Minari | 1,771 | Python | Offline datasets | ESSENTIAL |
| 57 | https://github.com/PKU-Alignment/safety-gymnasium | 600 | Python | Safe RL benchmark | ESSENTIAL |
| 58 | https://github.com/PKU-Alignment/Safe-Policy-Optimization | 427 | Python | Safe RL algorithms | USEFUL |
| 59 | https://github.com/learnsyslab/safe-control-gym | 932 | Python | Safe/robust control | USEFUL |
| 60 | https://github.com/Farama-Foundation/Gymnasium | 12,788 | Python | RL environment API | ESSENTIAL |
| 61 | https://github.com/DLR-RM/stable-baselines3 | 13,974 | Python | RL algorithms | ESSENTIAL |
| 62 | https://github.com/Farama-Foundation/Shimmy | 933 | Python | Env interop | USEFUL |
| 63 | https://github.com/openai/baselines | 16,778 | Python | Legacy RL reference | STALE |
| 64 | https://github.com/ikostrikov/pytorch-a2c-ppo-acktr-gail | 3,909 | Python | Legacy PyTorch RL reference | STALE |

**Verdict totals:** ESSENTIAL 21 · USEFUL 27 · NICHE 6 · STALE 10 (the combined STALE/NICHE entry counted once as STALE).

---

## Bottom Line

For a smart-city RL effort in 2026, the shortlist that earns its place in a production or serious research dependency list is: **Gymnasium, Stable-Baselines3, PettingZoo, Ray/RLlib, SUMO, CityFlow, sumo-rl, RESCO, CARLA (or MetaDrive/HighwayEnv by fidelity need), CityLearn, Sinergym, EnergyPlus, ns3-gym, d3rlpy, Minari, and Safety-Gymnasium.** Everything else is either a citable paper snapshot (IntelliLight/CoLight/FRAP/PressLight), a domain specialist worth knowing (DROO, UAV-DDPG, BOPTEST, Gnu-RL, DTLight), or a cautionary tale in maintenance (Beobench, Energym, gym-traffic). When adopting paper code, check the license first — the absence of one is the single most common defect in this literature's repositories.
