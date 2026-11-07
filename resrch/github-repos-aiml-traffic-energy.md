# GitHub Repositories for AI/ML in Smart Cities: Traffic Forecasting, Ride-Hailing & Energy ML

**Deep-research dossier — web research only, no code cloned**
**Date of research:** November 2026
**Scope:** 50+ repositories across four categories: (1) Traffic forecasting frameworks, (2) Ride-hailing / mobility ML, (3) Energy ML, (4) Air quality ML (optional bonus).

**How to read each entry:** full URL, stars, language, license, last activity, maintainer; what it implements (papers/models); key modules; datasets; quality signals (docs, tests, CI, pretrained weights, Docker); limitations; best-fit use; and a VERDICT (`essential` / `useful` / `niche` / `stale`). Star counts are as observed during this research pass (late 2026) and drift over time.

---

## Executive summary

The smart-city ML GitHub ecosystem splits into two very different populations:

1. **Paper-one-off reference implementations** — the majority of traffic-forecasting repos (DCRNN, GMAN, AGCRN, MTGNN, ASTGCN, T-GCN, STGCN). These are single-model repos from 2017–2021 papers, mostly TensorFlow 1.x or early PyTorch, with minimal tests, no CI, no Docker, and stale maintenance. They remain *citation-canonical* (you must compare against them) but are rarely production-usable as-is.
2. **Engineered libraries and platforms** — LibCity, TorchSpatiotemporal (tsl), PyTorch Geometric Temporal, Nixtla's NeuralForecast, Google's TimesFM, OpenSTEF, OSMnx, CityLearn. These have packaging, docs, releases, CI and sometimes pretrained weights; they are where real work should start.

Key findings:
- **Traffic:** LibCity (1.1k+ stars) is the closest thing to a "one library for all traffic tasks" but has gone stale (~2 years since last push). PyTorch Geometric Temporal (3.0k stars) and TorchSpatiotemporal/tsl (388 stars, actively maintained) are the healthiest library-style options. Foundation-model entrants OpenCity (189★) and UrbanGPT (462★) are interesting but research-grade. LargeST (299★) is the dataset to use for realistic scale (8,600 sensors).
- **Ride-hailing/mobility:** OSMnx (5.9k★) is the standout — production-quality, actively maintained, MIT. Trajectron++ (833★) is the trajectory-prediction standard. The classic demand-prediction papers (DeepST, DMVST-Net, CSTN) have tiny, incomplete, often TF1 repos.
- **Energy:** The strongest engineering lives in NeuralForecast (4.2k★), TimesFM (35k★, with license caveats on v3 weights), and OpenSTEF (180★, LF Energy-hosted, full pipeline + Docker). Demand response has CityLearn (649★, MIT, RL environment). EV charging has good datasets (ST-EVCDP 266★) but mostly paper-scale forecasting code.
- **Air quality:** Small but viable — AirFormer (163★), Air-DualODE (ICLR'25), AirPhyNet, ST-CausalConvNet.

**Bottom line:** For a new smart-city project: start with **tsl or PyTorch Geometric Temporal** for spatiotemporal modelling, **LibCity** if you need the full traffic task zoo (accept the staleness), **NeuralForecast/TimesFM** for energy time series, **OSMnx** for network construction, **CityLearn** for demand-response RL, and **LargeST/BDG2/ST-EVCDP** for realistic datasets.

---

# CATEGORY 1: TRAFFIC FORECASTING FRAMEWORKS

## 1.1 LibCity — Bigscity-LibCity (the big one)

- **URL:** https://github.com/LibCity/Bigscity-LibCity
- **Stars:** ~1,167 (forks ~194)
- **Language:** Python (PyTorch)
- **License:** Apache-2.0
- **Last commit:** Created Dec 2020; last meaningful push ~2023–2024 (star trackers report "last push 2 years ago" as of late 2026) — **effectively stale**
- **Maintainer:** LibCity org, Beihang University BIGSCity lab (Jingyuan Wang, Jiawei Jiang, Wenjun Jiang, Chao Li, Wayne Xin Zhao / batmanfly). Org based in China; 9 public repos; 157 followers.

**What it implements:** LibCity is *the* comprehensive urban spatial-temporal data mining library. Papers: "LibCity: An Open Library for Traffic Prediction" (ACM SIGSPATIAL 2021) and the extended TKDE/journal version "LibCity: A Unified Library Towards Efficient and Comprehensive Urban Spatial-Temporal Prediction". Claims **74+ reproduced models across 9 traffic prediction tasks** and **52 datasets**, up from the 42 models/29 datasets of the original paper. Tasks covered: traffic state prediction (flow/speed), on-demand service prediction (ride-hailing demand), OD-matrix prediction, traffic accident prediction, trajectory next-location prediction, ETA (estimated time of arrival), map matching, and road network representation learning. Model warehouse includes essentially every canonical STGNN: STGCN, DCRNN, GWNET, ASTGCN, STSGCN, AGCRN, MTGNN, GMAN, GTS, STGODE, DGCRN, MSDR, RGSL, STG-NCDE, plus newer transformers (PDFormer and friends) and non-deep baselines (HA, ARIMA-style, etc.).

**Key modules:** unified **atomic-file** data format (`.zip` per dataset) as the core abstraction; `libcity/config` (JSON config-driven experiments), `libcity/data` (pipelines/atomic readers), `libcity/model` (task-organized model zoo), `libcity/evaluator` (masked MAE/RMSE/MAPE, grid/graph/trajectory evaluators), `libcity/pipeline` (run_model.py entrypoint), cache layer for precomputed tensors (DTW matrices, adjacency). Companion repos: **Bigscity-LibCity-Datasets** (245★ — conversion tools from raw sources into atomic files), **Bigscity-LibCity-PaperList** (233★ — curated traffic-prediction paper list 2016–2021+), **Bigscity-LibCity-WebTool** (69★ — experiment management/visualization web UI), Docs repos (EN/ZH).

**Datasets supported:** METR-LA, PEMS-BAY, PEMS03/04/07/08, PeMSD7, NYC Taxi (grid), CHIBike, T-Drive, TaxiBJ/BikeNYC-era grid datasets, ride-hailing OD sets, accident datasets, trajectory datasets (Foursquare/Twitter/Porto-style), road networks — 52 total per README.

**Quality signals:** ✅ extensive English + Chinese docs (readthedocs), ✅ config-driven reproducibility, ✅ leaderboard/website (libcity.ai), ✅ evaluator standardization; ❌ no CI visible, ❌ no Docker, ❌ no pretrained weights, ❌ no test suite of note, ❌ install-from-source only.

**Limitations:** stale (2+ years without pushes — new PyTorch versions may break); heavy dependency surface; docs drift from code; per-model performance sometimes below original papers (acknowledged by authors); big install footprint; Chinese-first communication for some issues.

**Best-fit use:** researchers and grad students who need to run 30+ traffic baselines under one config system, or practitioners who want OD/ETA/accident tasks (not just speed forecasting) in one framework.

**VERDICT: ESSENTIAL (with staleness caveat)** — the reference framework for the field; budget time to pin dependency versions.

## 1.2 TorchSpatiotemporal (tsl)

- **URL:** https://github.com/TorchSpatiotemporal/tsl
- **Stars:** ~388 (forks ~37, open issues ~22)
- **Language:** Python (PyTorch, PyG, PyTorch Lightning)
- **License:** MIT
- **Last commit:** created Mar 2022; **actively maintained** (recent version constraints: NumPy ≥1.26 <3, PyTorch ≥2.2 <2.13, PyG ≥2.4 <3 — indicates current maintenance into 2025/2026)
- **Maintainer:** TorchSpatiotemporal open-source collective (docs at torch-spatiotemporal.readthedocs.io)

**What it implements:** A modern *library* (not a paper repo) for neural spatiotemporal processing with GNN focus, built on PyTorch + PyG + Lightning. It packages literature baselines (ASTGCN/STGCN-style attention models, recurrent GCNs, transformers) behind a unified `Dataset`/`Model`/`Experiment` API, and is the library that **natively hosts the LargeST dataset loader** (`tsl.datasets.large_st` — downloads CA/GLA/GBA/SD subsets from HuggingFace, handles resampling to 15-min, adjacency, imputation).

**Key modules:** `tsl.datasets` (METR-LA, PEMS-BAY, PeMS, LargeST, synthetic; `DatetimeDataset` prototypes), `tsl.nn` (backbones, embeddings, graph learning layers), `tsl.experiment` (predictive experiment harness, imputation support), `tsl.connectors` (PyG/Lightning glue), preprocessing/normalization, optional `torch-sparse` acceleration, index-batching for memory efficiency.

**Datasets:** the standard traffic sets plus LargeST; supports both forecasting and imputation tasks.

**Quality signals:** ✅ readthedocs docs, ✅ pip-installable, ✅ modern dependency ranges, ✅ handles large-scale data, ✅ HuggingFace-hosted processed datasets; ❌ smaller community (22 open issues), ❌ no Docker, ❌ benchmark results不如 LibCity breadth.

**Limitations:** fewer reproduced models than LibCity; smaller user base means fewer answered questions; some datasets require download pipelines that can break when hosting moves.

**Best-fit use:** building *new* spatiotemporal models (research or product) on a clean, maintained codebase; the natural choice if you need LargeST-scale data.

**VERDICT: ESSENTIAL** for new development — the most technically current traffic/ST library in this survey.

## 1.3 PyTorch Geometric Temporal

- **URL:** https://github.com/benedekrozemberczki/pytorch_geometric_temporal
- **Stars:** ~3.0k (forks 403)
- **Language:** Python (PyG)
- **License:** MIT
- **Last commit:** active — 2,062 commits; PGT-I scaling paper (arXiv 2507.11683, 2025) shows ongoing research maintenance
- **Maintainer:** Benedek Rozemberczki (AstraZeneca) + large contributor list (Paul Scherer, Yixuan He, et al.); CIKM 2021 resource paper.

**What it implements:** Temporal/dynamic extension of PyTorch Geometric with 30+ spatiotemporal models from papers: **DCRNN, GConvGRU/GConvLSTM, T-GCN, A3T-GCN, AGCRN, STGCN, ASTGCN/MSTGCN, GMAN, MTGNN, EvolveGCN, LRGCN, MPNN-LSTM, 2S-AGCN, DNNTSP** plus auxiliary convolutions (TemporalConv, DConv, ChebConvAttention, AVWGCN). Also epidemiological forecasting, sharing-economy, energy production and web-traffic benchmark datasets.

**Key modules:** `nn.recurrent`, `nn.attention`, `nn` (aux graph convs), `signal` (snapshot iterators), `dataset` loaders, train-test splitters, GPU support; index-batching + Dask-DDP distributed training; PyTorch Lightning integration; notebooks/case studies in `examples/` and `notebooks/`; pytest suite (`python -m pytest test`).

**Datasets:** traffic (METR-LA/PEMS-BAY-era), epidemic (England/COVID-style), energy production, bike-share/mobility, web traffic.

**Quality signals:** ✅ tests (pytest), ✅ CI workflows (`.github/workflows`), ✅ readthedocs, ✅ pip install `torch-geometric-temporal`, ✅ contributing guide, ✅ releases/PyPI package used widely; ❌ no Docker, ❌ no pretrained weights.

**Limitations:** research-library orientation — abstractions can fight you for exotic models; PGT performance on traffic benchmarks trails specialized repos; dependency on PyG version pinning.

**Best-fit use:** when you want *many* STGNN variants with one API — especially if your graph data is dynamic/irregular or your domain is epidemiology/energy rather than pure traffic.

**VERDICT: ESSENTIAL** — best-documented multi-model GNN-temporal library with actual tests/CI.

## 1.4 DL-Traff (Jiang et al. benchmark) — Graph & Grid

- **URLs:**
  - https://github.com/deepkashiwa20/DL-Traff-Graph (~182★, PyTorch)
  - https://github.com/deepkashiwa20/DL-Traff-Grid (TensorFlow counterpart; stars ~150s, unverified in this pass)
- **Language:** Python (PyTorch 1.6 main branch / TF for grid)
- **License:** not stated in README (effectively all-rights-reserved by default — **check before commercial use**)
- **Last commit:** ~2021–2022 era (paper CIKM 2021); stale
- **Maintainer:** Renhe Jiang (Univ. of Tokyo / SUSTECH) — also LibCity contributor, MegaCRN author.

**What it implements:** CIKM 2021 Best Resource Paper Runner-Up: "DL-Traff: Survey and Benchmark of Deep Learning Models for Urban Traffic Prediction". Graph side integrates **HistoricalAverage, CopyLastSteps, LSTNet, STGCN, DCRNN, GraphWaveNet, ASTGCN, GMAN, MTGNN, AGCRN, TGCN** under *identical data processing, hyperparameters and compute environment*; Grid side covers ST-ResNet/DeepSTN+/STDN-class CNN models. Deliberately standardized (not fully converged per-model) so architecture comparisons are fair.

**Key modules:** per-dataset work folders (`workMETRLA`, `workPEMSBAY`, `workPEMSD7M`), shared `parameter.py` + per-model overrides, unified prediction CSV outputs, adjacency generators.

**Datasets:** METR-LA, PeMS-BAY, PeMSD7(M) bundled; grid datasets (TaxiBJ/BikeNYC-style) on the Grid repo.

**Quality signals:** ✅ ships data in-repo (zipped h5), ✅ README tables of results, ✅ same-hyperparameter fairness design; ❌ no tests/CI/Docker, ❌ pinned to PyTorch 1.6, ❌ authors admit models don't reach full convergence, ❌ license unspecified.

**Limitations:** benchmark-frozen in 2021; running requires old torch; not a library you extend — a *report* with code.

**Best-fit use:** reproducing an apples-to-apples baseline table for a paper; educational comparison.

**VERDICT: USEFUL** (research citation value) / **STALE** for new work.

## 1.5 STG4Traffic benchmark

- **URL:** https://github.com/trainingl/STG4Traffic
- **Stars:** small (unverified in this pass)
- **Language:** Python (PyTorch 1.8)
- **License:** unverified
- **Last commit:** ~2022–2023 (paper: "STG4Traffic: A Survey and Benchmark of Spatial-Temporal Graph Neural Networks for Traffic Prediction", Scientific Reports)
- **Maintainer:** trainingl (academic author group)

**What it implements:** Unified benchmark of **16 models**: STGCN, DCRNN, T-GCN, GWNET, ASTGCN, STSGCN, AGCRN, MTGNN, GMAN, GTS, STGODE, DGCRN, TrendGCN, GMSDR, RGSL, STG-NCDE — with standardized splits (7:1:2 speed / 6:2:2 flow), early stopping, masked metrics, and faithful-then-tuned hyperparameters.

**Key modules:** `TrafficFlow/` and `TrafficSpeed/` trees with decoupled `data`, `lib` (loaders, metrics, graph construction), `model`, `log` directories.

**Datasets:** METR-LA, PEMS-BAY, PEMSD4, PEMSD8.

**Quality signals:** ✅ decoupled structure, ✅ experiment protocol documented; ❌ old torch, ❌ no CI/tests/Docker, ❌ single-maintainer.

**Best-fit use:** alternative to DL-Traff/LibCity when you want a lean benchmark of the 16 most-cited STGNNs.

**VERDICT: USEFUL / NICHE** — good benchmark protocol, weak engineering.

## 1.6 Graph WaveNet (official)

- **URL:** https://github.com/nnzhan/Graph-WaveNet
- **Stars:** ~822 (forks 231)
- **Language:** Python (PyTorch)
- **License:** MIT
- **Last commit:** created May 2019; maintenance sporadic — open issues (28) with latest activity ~2024; effectively **unmaintained**
- **Maintainer:** Zonghan Wu (UTS) — same author as MTGNN; contributions from sshleifer et al.

**What it implements:** Official PyTorch implementation of "Graph WaveNet for Deep Spatial-Temporal Graph Modeling" (IJCAI 2019): self-adaptive adjacency matrix learned from node embeddings + stacked dilated causal 1D convolutions for long sequences.

**Key modules:** `train.py` (flags `--gcn_bool --adjtype doubletransition --addaptadj --randomadj`), `generate_training_data.py`, `model/` (graph conv + gated TCN blocks), `metrics.py`.

**Datasets:** METR-LA, PEMS-BAY (downloaded from DCRNN's Google Drive/Baidu links).

**Quality signals:** ✅ MIT, ✅ canonical implementation cited everywhere, ✅ simple single-file training; ❌ no tests/CI/Docker/docs beyond README, ❌ data hosted on personal Drive links (fragile), ❌ TF-era code style, ❌ open issue backlog.

**Best-fit use:** reproducing the GWNET baseline; adaptive-adjacency ideas to port into your own model.

**VERDICT: USEFUL** (canonical baseline) / **STALE** (maintenance).

## 1.7 DCRNN (liyaguang/DCRNN)

- **URL:** https://github.com/liyaguang/DCRNN
- **Stars:** ~1,455 (forks 427)
- **Language:** Python (**TensorFlow 1.x**)
- **License:** MIT
- **Last commit:** created Dec 2017; maintainer publicly stated (Mar 2023, issue #77) he has **no capacity to port to TF2** — stale
- **Maintainer:** Yaguang Li (Google DeepMind), co-authors Rose Yu, Cyrus Shahabi, Yan Liu (ICLR 2018).

**What it implements:** Official TF implementation of Diffusion Convolutional Recurrent Neural Network for traffic forecasting — diffusion convolution over road graph + GRU encoder-decoder with scheduled sampling. The **primary source of the METR-LA and PEMS-BAY datasets** (Google Drive/Baidu links reused by half this category).

**Key modules:** `src/` models (DCRNN cell, decoder), `data/` preprocessing scripts, `scripts/` adjacency generation, config YAMLs.

**Datasets:** METR-LA, PEMS-BAY — the field's de-facto standard.

**Quality signals:** ✅ MIT, ✅ canonical + dataset provider, ✅ clean paper-faithful code; ❌ TF1 only (`rnn_decoder` removed in TF2 — code no longer runs on modern TF), ❌ no tests/CI/Docker, ❌ dead issue tracker for runtime questions.

**Best-fit use:** downloading the datasets; citing the baseline; porting logic to PyTorch (many ports exist, e.g., LeiBAI/DCRNN_Pytorch, cdsnlab/traffic-pytorch).

**VERDICT: USEFUL for data/citation / STALE as runnable code** — do not plan to execute it on modern stacks.

## 1.8 STGCN original (VeritasYin/STGCN_IJCAI-18)

- **URL:** https://github.com/VeritasYin/STGCN_IJCAI-18
- **Stars:** ~1,246 (forks 326)
- **Language:** Python (TensorFlow)
- **License:** BSD 2-Clause
- **Last commit:** created Apr 2018; occasional maintenance (star trackers show updates into 2026 — likely light housekeeping); core code unchanged
- **Maintainer:** Haoteng Yin (Purdue University) — IJCAI 2018 paper with Bing Yu, Zhanxing Zhu.

**What it implements:** Original STGCN: two ST-Conv blocks (temporal gated conv → spatial graph conv → temporal gated conv) + FC head; first purely-convolutional spatiotemporal architecture for traffic.

**Key modules:** `main.py`, `modules/` (graph conv, gated temporal conv), `prepare_data.py`, bundled `dataset/PeMSD7_M`.

**Datasets:** PeMSD7(M) included; METR-LA supported via DCRNN data.

**Quality signals:** ✅ BSD-2, ✅ canonical, ✅ data in-repo; alternative implementations listed (TensorFlow PKUAI26, MXNet Davidham3, PyTorch FelixOpolka); ❌ TF1-era, ❌ no tests/CI, ❌ README-level docs.

**Best-fit use:** baseline reproduction; understanding ST-Conv block design.

**VERDICT: USEFUL / STALE** — cite and port rather than run.

## 1.9 ASTGCN-pytorch (guoshnBJTU/ASTGCN-2019-pytorch)

- **URL:** https://github.com/guoshnBJTU/ASTGCN-2019-pytorch
- **Stars:** unverified in this pass (community fork widely referenced; the MXNet original Davidham3/ASTGCN is the citation source)
- **Language:** Python (PyTorch)
- **License:** unverified (check repo)
- **Last commit:** ~2019–2021 era; stale
- **Maintainer:** guoshnBJTU (Beijing Jiaotong University)

**What it implements:** PyTorch port of ASTGCN (AAAI 2019, Guo et al.) and MSTGCN — multi-component attention (recent/temporal-period/spatial-period) with graph conv; note README states only the *recent* component is implemented in this port since components share architecture.

**Key modules:** `train_ASTGCN_r.py`, `prepareData.py`, `configurations/*.conf` (loss `masked_mae`, mask-aware metrics).

**Datasets:** PEMS04, PEMS08.

**Quality signals:** ✅ config-file UX, ✅ masked loss/metric handling documented; ❌ partial model (recent component only), ❌ no tests/CI, stale.

**Best-fit use:** quick ASTGCN baseline on PEMS04/08 in PyTorch.

**VERDICT: NICHE / STALE** — use ASTGCN via tsl/PyG Temporal/LibCity instead.

## 1.10 GMAN (zhengchuanpan/GMAN) + GMAN-PyTorch

- **URLs:**
  - https://github.com/zhengchuanpan/GMAN — ~534★, Python, Apache-2.0, last topic update Apr 2022 (**stale**), maintainer Chuanpan Zheng (Xiamen Univ.) with Xiaoliang Fan (paper co-author)
  - https://github.com/VincLee8188/GMAN-PyTorch — ~175★, PyTorch reimplementation ("for learning purpose"), no license file noted, created Sep 2020
- **What it implements:** GMAN (AAAI 2020): encoder-decoder with ST-Attention blocks, transform attention between encoder/decoder to mitigate error propagation, spatio-temporal embeddings (SE files).
- **Key modules:** `PeMS/utils.py` (seq2instance, loadData with SE + time embeddings), model with STAtt blocks, `main.py`.
- **Datasets:** Xiamen volume data + PEMS-BAY speed (via DCRNN links); spatial embedding files (`SE(METR-LA).txt`).
- **Quality signals:** ✅ Apache-2.0 (original), ✅ clear structure, third-party PyTorch port exists (also reimplemented in tsl, OpenCity, traffic-pytorch); ❌ TF 1.14 pinned, stale, no tests/CI/Docker.
- **Limitations:** original is TF1; PyTorch port is unlicensed and unverified for accuracy.
- **Best-fit use:** long-horizon (1h) baseline reproduction.
- **VERDICT: USEFUL / STALE** (TF1); the PyTorch port is **NICHE**.

## 1.11 AGCRN (LeiBAI/AGCRN)

- **URL:** https://github.com/LeiBAI/AGCRN
- **Stars:** ~444 (forks 97)
- **Language:** Python (PyTorch)
- **License:** MIT
- **Last commit:** created Jul 2020; last update Feb 2024 (per star trackers) — dormant
- **Maintainer:** Lei Bai (Shanghai AI Laboratory)

**What it implements:** NeurIPS 2020 "Adaptive Graph Convolutional Recurrent Network for Traffic Forecasting" — node adaptive embedding + data-driven graph structure learning feeding GRU cells (AVWGCN). Also the source repo for **STGODE** and **MegaCRN** (README links), making it a mini-family.

**Key modules:** `model/AGCRN.py` (PEACE cell: node embeddings, adaptive graph), `lib/` (loaders, normalization, masked metrics), `data/` PEMSD4+PEMSD8 bundled.

**Datasets:** PEMSD4, PEMSD8 included; METR-LA/PEMS-BAY via DCRNN.

**Quality signals:** ✅ MIT, ✅ data in-repo, ✅ small & readable, widely ported (tsl, PyG Temporal, LargeST, OpenCity all include AGCRN); ❌ no tests/CI/Docker, minimal README, stale since 2024.

**Best-fit use:** adaptive-graph baseline; starting point for graph-learning extensions.

**VERDICT: USEFUL** (canonical, MIT, clean) — mildly stale.

## 1.12 MTGNN (nnzhan/MTGNN)

- **URL:** https://github.com/nnzhan/MTGNN
- **Stars:** ~948 (forks 251)
- **Language:** Python (PyTorch)
- **License:** MIT
- **Last commit:** created May 2020; issues open into 2024, no recent feature work — **stale**
- **Maintainer:** Zonghan Wu (UTS/Monash)

**What it implements:** KDD 2020 "Connecting the Dots: Multivariate Time Series Forecasting with Graph Neural Networks" — graph learning layer (kNN-sparse adaptive adjacency), mix-hop propagation (directed GCN), dilated inception temporal conv; works with *or without* predefined graphs.

**Key modules:** `net.py` (MTGNN core), `train_single_step.py` / `train_multi_step.py`, graph learning module, `modules/`.

**Datasets:** Solar-Energy, Traffic (862 nodes), Electricity, Exchange-rate (from laiguokun/multivariate-time-series-data), METR-LA, PEMS-BAY.

**Quality signals:** ✅ MIT, ✅ versatile (traffic + generic MTS), ✅ documented CLI; ❌ no tests/CI/Docker, ❌ sparse docs, stale issue handling (feature requests from 2023–2024 unanswered).

**Best-fit use:** multivariate time series where graph structure is unknown; energy/solar series with spatial nodes.

**VERDICT: USEFUL / STALE** — strong baseline, poor maintenance.

## 1.13 T-GCN (lehaifeng/T-GCN)

- **URL:** https://github.com/lehaifeng/T-GCN
- **Stars:** ~1,789 (forks 472) — highest-starred single traffic model repo after DCRNN
- **Language:** Python + Jupyter Notebook; **both TensorFlow and PyTorch implementations** in-repo
- **License:** LICENSE file present in PyTorch subfolder (verify terms; historically Apache-ish — **check**)
- **Last commit:** created Nov 2018; PyTorch port with pytorch-lightning added later (light activity thereafter); largely dormant
- **Maintainer:** Ling Zhao et al. (Zhengzhou University / Central South), IEEE T-ITS 2019/2020 paper.

**What it implements:** T-GCN = GCN (spatial) + GRU (temporal); the repo also frames the authors' broader graph-representation-learning program. Baselines in-repo: HA, ARIMA, SVR, GCN, GRU.

**Key modules:** `T-GCN/T-GCN-TensorFlow/` (tgcn.py RNNCell), `T-GCN/T-GCN-PyTorch/` (pytorch-lightning training, `--model_name TGCN`), `baselines.py`.

**Datasets:** SZ-taxi (Shenzhen, 156 roads), Los-loop (207 LA sensors) bundled; METR-LA supported.

**Quality signals:** ✅ dual framework ports, ✅ pytorch-lightning + requirements/pyproject in PyTorch port, ✅ notebooks for teaching; ❌ TF branch is TF1 (`tf.contrib`), ❌ no tests/CI/Docker, stale.

**Best-fit use:** pedagogical baseline; simple GCN+GRU architecture to adapt.

**VERDICT: USEFUL / STALE** — great star count, dated code.

## 1.14 PDFormer (BUAABIGSCity/PDFormer)

- **URL:** https://github.com/BUAABIGSCity/PDFormer
- **Stars:** ~297
- **Language:** Python (PyTorch, built on LibCity skeleton)
- **License:** unverified (check repo; LibCity lineage suggests Apache-2.0)
- **Last commit:** created 2022–2023; maintained into 2024 (active research repo, 3 open issues)
- **Maintainer:** Beihang BIGSCity lab (Jiawei Jiang, Chengkai Han, Wayne Xin Zhao, Jingyuan Wang)

**What it implements:** AAAI 2023 "PDFormer: Propagation Delay-aware Dynamic Long-range Transformer for Traffic Flow Prediction" — spatial self-attention with short/long-range graph masking matrices, delay-aware feature transformation (models propagation time-lag), temporal self-attention; attention-map interpretability.

**Key modules:** `libcity/model/traffic_flow_prediction/PDFormer.py`, `libcity/cache/dataset_cache/` (**precomputed DTW matrices and traffic-pattern sets for all 6 datasets** — saves hours), JSON config files per dataset, `run_model.py` CLI.

**Datasets:** PeMS04/07/08 (graph) + NYCTaxi, CHIBike, T-Drive (grid, via TrafficStateGridEvaluator) — in LibCity atomic format from Google Drive.

**Quality signals:** ✅ built on LibCity's unified pipeline (evaluators, metrics), ✅ cached expensive preprocessing shipped, ✅ AAAI-cited; ❌ no CI/tests/Docker, requires LibCity install.

**Limitations:** inherits LibCity's staleness; DTW precompute is dataset-specific.

**Best-fit use:** state-of-the-art-ish transformer baseline for flow prediction including citywide grid taxi/bike data.

**VERDICT: USEFUL** (one of the best modern traffic model repos with a maintained research group behind it).

## 1.15 STAEformer (XDZhelheim/STAEformer)

- **URL:** https://github.com/XDZhelheim/STAEformer
- **Stars:** 247 (verified on GitHub page), forks 33, 14 open issues, 26 commits
- **Language:** Python (PyTorch ≥1.11)
- **License:** unverified (no license badge visible — **default all-rights-reserved**)
- **Last commit:** created 2023; issue replies into Nov 2024 — semi-active, small commit count
- **Maintainer:** Zheng Dong / Hangchen Liu et al. (CSU + Univ. of Tokyo group; CIKM 2023)

**What it implements:** CIKM 2023 short paper: "Spatio-Temporal Adaptive Embedding Makes Vanilla Transformer SOTA for Traffic Forecasting" — feature embedding + periodicity embedding + **spatio-temporal adaptive embedding (Ea)** on a *vanilla* alternating temporal-transformer / spatial-transformer stack. Beats GWNet/DCRNN/AGCRN/GMAN/PDFormer/STID on 6 benchmarks with far simpler architecture.

**Key modules:** `model/STAEformer.py` (AttentionLayer over nodes/time dims), `model/train.py` (`python train.py -d <dataset> -g <gpu>`), `data/`, `lib/`.

**Datasets:** METRLA, PEMS-BAY, PEMS03, PEMS04, PEMS07, PEMS08.

**Quality signals:** ✅ extremely simple to run (single command), ✅ strong reported SOTA table in README/paper, ✅ hyperparameter-insensitive per authors; ❌ tiny repo (26 commits), ❌ no license, ❌ no tests/CI/Docker, ❌ authors concede very-large graphs (>~1000 nodes) untested (issue #19).

**Limitations:** no license = risky for commercial reuse; limited to ~1k nodes validated; research-grade docs.

**Best-fit use:** *the* first model to try if you want a strong, simple, modern traffic forecaster; excellent ablation reference for embedding design.

**VERDICT: USEFUL (near-essential baseline)** — high value-per-line-of-code; resolve the license question first.

## 1.16 LargeST (liuxu77/LargeST)

- **URL:** https://github.com/liuxu77/LargeST
- **Stars:** 299 (verified), forks 36, 13 commits
- **Language:** Python (PyTorch 1.12)
- **License:** **code MIT; dataset CC BY-NC 4.0** (non-commercial data!)
- **Last commit:** created Jun 2023 (NeurIPS 2023 D&B track); low commit cadence — dataset/benchmark frozen
- **Maintainer:** Xu Liu, Yutong Xia, Yuxuan Liang, Lei Bai, Chao Huang, Roger Zimmermann et al. (NUS/HKUST/SCUT/Shanghai AI Lab)

**What it implements:** Benchmark dataset for *large-scale* traffic forecasting: **8,600 California sensors, 5 years (2017–2021), full metadata** (lat/lng, district, county, freeway, lanes, direction) + 12 baseline implementations: HL, LSTM, DCRNN, AGCRN, STGCN, GWNET, ASTGCN, STTN, STGODE, DSTAGNN, DGCRN, D2STGNN.

**Key modules:** `data/` (Kaggle download scripts, `process_ca_his.ipynb`, `generate_data_for_training.py`, subset generators for GLA/GBA/SD), `experiments/<model>/run.sh`, `src/` with `BaseModel`/`BaseEngine` extension points for plugging in your model.

**Datasets:** CA (8,600 nodes), GLA (3,834), GBA (2,352), SD (716) — hosted on Kaggle (`liuxu77/largest`); also mirrored/usable through tsl's LargeST loader on HuggingFace.

**Quality signals:** ✅ documented 3-step "evaluate your model" extension guide, ✅ run.sh per baseline, ✅ metadata richness, ✅ NeurIPS-reviewed; ❌ only 13 commits, ❌ no CI/tests/Docker, ❌ PyTorch 1.12 pinned, ❌ **data license CC BY-NC forbids commercial use** (check PeMS terms for production).

**Limitations:** heavy data (GB-scale); non-commercial data license; baseline code quality varies (ported from original repos).

**Best-fit use:** the realistic-scale benchmark — if your deployment has hundreds/thousands of sensors, METR-LA (207 nodes) results won't transfer; LargeST will tell you what will.

**VERDICT: ESSENTIAL (as dataset) / USEFUL (as code)** — must-know for credible large-scale traffic work.

## 1.17 OpenCity (HKUDS/OpenCity) — foundation model

- **URL:** https://github.com/HKUDS/OpenCity
- **Stars:** 189 (verified), forks 32, 12 commits, 9 open issues
- **Language:** Python (PyTorch 1.9 pinned in README)
- **License:** MIT (verified on page)
- **Last commit:** created Aug 2024 (paper arXiv 2408.10269; later published — ACM DOI 10.1145/3773912, 2025); low commit count since release
- **Maintainer:** Data Intelligence Lab @ University of Hong Kong (Zhonghang Li, Chao Huang) + Baidu collaborators

**What it implements:** Open spatio-temporal **foundation model** for traffic: Transformer + GNN hybrid pretrained on heterogeneous web-platform traffic data for **zero-shot generalization** across cities and long horizons; reports scaling laws. Ships three sizes: **OpenCity-plus / base / mini** with weights on HuggingFace (`hkuds/OpenCity-Plus`).

**Key modules:** `model/OpenCity/` (+ 11 baseline models: AGCRN, ASTGCN, GWN, MSDR, MTGNN, PDFormer, STGCN, STSGCN, STWA, TGCN), `Run.py` (modes: `pretrain`, `test`, `ori`), `conf/`, `model_weights/`, `lib/`.

**Datasets:** OpenCity-dataset on HuggingFace covering traffic flow, taxi demand, bicycle trajectories, traffic speed, traffic-index stats across NYC, Chicago, LA, Bay Area, Shanghai, Shenzhen, Chengdu.

**Quality signals:** ✅ MIT, ✅ pretrained weights released (3 scales), ✅ datasets on HuggingFace, ✅ baselines in-repo, ✅ clear pretrain/test commands; ❌ 12 commits (research dump), ❌ pinned torch 1.9, ❌ no CI/tests/Docker, ❌ 3 open PRs unmerged.

**Limitations:** research-grade; heavy pretraining compute if self-hosting; zero-shot claims need validation on your city; the ACM publication happened 2025 so citations are still ramping.

**Best-fit use:** cross-city transfer without per-city labels; long-horizon forecasting; smart-city proposals needing "foundation model" capability.

**VERDICT: USEFUL (cutting-edge)** — the most credible open traffic foundation model; treat as research, not product.

## 1.18 UrbanGPT (HKUDS/UrbanGPT)

- **URL:** https://github.com/HKUDS/UrbanGPT
- **Stars:** ~462 (forks 58)
- **Language:** Python (PyTorch, LLM fine-tuning stack)
- **License:** Apache-2.0
- **Last commit:** created Feb 2024 (KDD 2024); scripts updated 2024; semi-active
- **Maintainer:** HKU Data Intelligence Lab (Zhonghang Li, Lianghao Xia, Chao Huang) + SCUT/Baidu

**What it implements:** KDD 2024 "UrbanGPT: Spatio-Temporal Large Language Models" — a **TCN-based spatio-temporal encoder** (gated dilated conv + multi-level correlation injection) aligned to a **Vicuna-7B-v1.5-16k** LLM via instruction tuning; produces `<ST_PRE>` predictive tokens mapped through a regression head; designed for **zero-shot cross-region** urban prediction (taxi/bike/crime flows).

**Key modules:** `urbangpt/train/`, `urbangpt/eval/run_urbangpt.py`, `instruction_generate/` (prompt construction with spatial/temporal/POI instructions), `ST_Encoder` pretrained weights, `urbangpt_train.sh` (8-GPU torchrun, wandb), `urbangpt_eval.sh`.

**Datasets:** NYC taxi/bike/crime pretraining data (HuggingFace), cross-region transfer eval sets; requires Vicuna checkpoint download.

**Quality signals:** ✅ Apache-2.0, ✅ weights + data links, ✅ project page + demo video, ✅ training/eval shell scripts; ❌ needs 8 GPUs for realistic training, ❌ heavy LLM stack (flash-attn, deepspeed era dependencies), ❌ no CI/tests, ❌ research-only quality.

**Limitations:** compute-hungry; LLM adds little for pure numerical forecasting vs. small ST models (a common critique); dependency rot risk in fast-moving LLM tooling.

**Best-fit use:** multimodal urban prediction where you need textual/POI reasoning or instruction-driven querying of forecasts; zero-shot transfer demos.

**VERDICT: NICHE / USEFUL for research** — impressive but heavy; not the right tool for a 207-sensor speed model.

## 1.19 Other traffic repos verified in passing (quick entries)

- **cdsnlab/traffic-pytorch** — https://github.com/cdsnlab/traffic-pytorch ; PyTorch framework with ASTGCN/DCRNN/GMAN/STGCN/WaveNet under one dataloader; reports MAE/RMSE tables for PEMS-Bay & PEMS; small stars, academic lab (CDSN), no license noted; **VERDICT: NICHE** (useful as a multi-model PyTorch reference if LibCity too heavy).
- **FelixOpolka/STGCN-PyTorch** — https://github.com/FelixOpolka/STGCN-PyTorch ; minimal PyTorch STGCN with METR-LA example; stars unverified (~200s historically); no license noted; stale since ~2018–2019; **VERDICT: NICHE** (teaching demo).
- **tijsmaas/TrafficPrediction** — https://github.com/tijsmaas/TrafficPrediction ; 31★, "Other" license; unified dataloader/eval for DCRNN + GraphWaveNet + GMAN with **pretrained checkpoints** for METR-LA (rare quality signal: ships `pretrained/` weights incl. FC-LSTM); roadmap incomplete; explicitly "preliminary"; **VERDICT: NICHE** — but noteworthy for pretrained weights.
- **Davidham3/STSGCN** — referenced by STG4Traffic/DL-Traff as the canonical STSGCN (AAAI 2020) implementation (MXNet/PyTorch); included in downstream benchmarks; **VERDICT: USEFUL (baseline)** — verify stars/license before use.
- **LeiBAI/STG2Seq** — 33★, multi-step passenger demand forecasting (ride-hailing adjacent, IJCAI 2019); **VERDICT: NICHE**.
- **ShuhaoLii/LaneLevel-Traffic-Benchmark** (TITS'24) — lane-level benchmark with 12+ reproduced models (HGCN, DGCN, MDL, TM-CNN, CNN-LSTM, GCN-GRU, STMGG + AGCRN/MTGNN); public lane-level test datasets; **VERDICT: USEFUL** if you work at lane granularity — a genuinely differentiated dataset/benchmark.

---

# CATEGORY 2: RIDE-HAILING / MOBILITY ML

## 2.1 OSMnx (gboeing/osmnx)

- **URL:** https://github.com/gboeing/osmnx/
- **Stars:** ~5,870 (forks 894, open issues 5!)
- **Language:** Python
- **License:** MIT (OpenStreetMap attribution required for derivatives)
- **Last commit:** **very active** — v2.1.1 released Jul 2026; ~190 PyPI downloads/day, ~468k/month; conda-forge 2.4M downloads; trending regularly
- **Maintainer:** Geoff Boeing (Professor of Urban Planning & Spatial Analysis, USC); 4,035 contributions; Zephyr Foundation Exceptional Technical Achievement Award 2025.

**What it implements:** Not an ML repo — the foundational **urban network analysis toolkit**: download/model/analyze/visualize street networks (walk/drive/bike) from OpenStreetMap in one line; routing, travel times, street orientations, building footprints, transit stops, POIs/amenities, elevation. Cite: Boeing, G. (2025) "Modeling and Analyzing Urban Networks and Amenities with OSMnx," *Geographical Analysis*.

**Key modules:** graph_from_place/by_point/dist APIs, `osmnx.routing`, `osmnx.geometries`/`features` (POIs), `osmnx.elevation`, `osmnx.bearing`, `osmnx.stats` (network indicators), GeoPandas/NetworkX interop, simplified graph models.

**Datasets:** live pulls from Overpass API (OpenStreetMap) — no bundled data needed.

**Quality signals:** ✅ full readthedocs User Reference + examples gallery (osmnx-examples), ✅ CI/coverage badges, ✅ PyPI + conda-forge, ✅ extremely low open-issue count (5), ✅ StackOverflow support channel, ✅ textbook adoption; ❌ not ML itself (you add the models).

**Limitations:** subject to OSM data quality/completeness and Overpass rate limits; requires attribution; heavy API pulls need caching for production.

**Best-fit use:** **the** way to build road-graph inputs for any traffic/ride-hailing model — adjacency matrices, OD networks, accessibility analysis, isochrones for demand models.

**VERDICT: ESSENTIAL** — highest-quality, best-maintained repo in this entire survey.

## 2.2 Trajectron++ (StanfordASL/Trajectron-plus-plus)

- **URL:** https://github.com/StanfordASL/Trajectron-plus-plus
- **Stars:** ~833 (forks 221)
- **Language:** Jupyter Notebook / Python (PyTorch)
- **License:** MIT (verified in LICENSE file)
- **Last commit:** created Jan 2020; periodic maintenance; open issues ~17; community forks actively extend it
- **Maintainer:** Stanford Autonomous Systems Lab — Tim Salzmann, Boris Ivanovic, Punarjay Chakravarty (Ford), Marco Pavone; ECCV 2020.

**What it implements:** "Trajectron++: Dynamically-Feasible Trajectory Forecasting With Heterogeneous Data" — modular **graph-structured recurrent** multi-agent trajectory forecaster: node/edge encoding (LSTM edge dynamics + additive attention), CVAE multimodality (GMM output), dynamics-constrained decoding (unicycle model), HD-map/semantic-map encoding, ego-conditioned prediction. Table in paper shows it as the only open-source method checking all boxes (general # agents, dynamics, heterogeneous data, future-conditional, open source).

**Key modules:** `trajectron/` (model, encoder_map, dynamical_system), `experiments/` (pedestrians ETH/UCY, vehicles, autonomous driving nuScenes-style), process_data scripts, visualization notebooks, evaluation (miss rate, ADE/FDE).

**Datasets:** ETH/UCY pedestrian, Stanford Drone, nuScenes/Argoverse-adjacent vehicle setups, neurodata-style processed sets.

**Quality signals:** ✅ MIT, ✅ extensive notebooks/docs, ✅ widely cited (thousands), ✅ pip mirror `trajectron` (unofficial), ✅ actively forked (continued community maintenance); ❌ notebook-first code (hard to productionize), no CI/Docker, dependency age (older torch), weights not officially hosted.

**Limitations:** research notebook style; training cost for new scenes; unmaintained upstream risks with new Python versions.

**Best-fit use:** pedestrian/vehicle trajectory prediction for AV and urban safety applications; anytime you need multimodal, map-aware agent forecasts.

**VERDICT: ESSENTIAL** for trajectory forecasting (the field's default open baseline).

## 2.3 DeepST lineage (grid crowd-flow / taxi demand)

- **URLs:**
  - Original referenced: lucktroy/DeepST (Microsoft Research lineage; not re-verified this pass)
  - Rebuild: https://github.com/TolicWang/DeepST — **116★**, Python, TF 1.5 reconstruction, no license noted, last updates 2019–2020, maintainer TolicWang
- **What it implements:** SIGSPATIAL 2016 demo "Deep Spatio-Temporal Residual Networks for Citywide Crowd Flows Prediction" (Zhang, Zheng, Qi et al., Microsoft) — DeepST = temporal closeness/period/seasonal-trend instances + CNN spatial deps + early/late fusion; ancestor of ST-ResNet; used in the UrbanFlow real-time system.
- **Key modules:** `exptTaxiBJ.py`, data prep for TaxiBJ h5 files, convolutional CPT/CPTM variants.
- **Datasets:** TaxiBJ (in/out flows 2013–2016 + meteorology + holidays), BikeNYC, TaxiGY, LoopGY (download links in README).
- **Quality signals:** ✅ simple run path, ✅ real dataset recipes; ❌ TF1.5, ❌ Chinese-only README in rebuild, ❌ stale, no license/tests/CI.
- **Best-fit use:** understanding the grid-flow formulation; historical baseline.
- **VERDICT: STALE / NICHE** — cite ST-ResNet instead of running this.

## 2.4 DMVST-Net (huaxiuyao/DMVST-Net)

- **URL:** https://github.com/huaxiuyao/DMVST-Net
- **Stars:** 109 (forks 50)
- **Language:** Python (Keras/TF 1.x, Python 2.7!)
- **License:** MIT
- **Last commit:** created Feb 2018; stale; README says "**I only put the model part on it. Other parts will be put soon**" — never completed
- **Maintainer:** Huaxiu Yao (AAAI 2018; Didi Chuxing intern work)

**What it implements:** AAAI 2018 "Deep Multi-View Spatial-Temporal Network for Taxi Demand Prediction" — three views: local CNN (spatial), LSTM (temporal), semantic graph (LINE embeddings of functionally-similar regions via DTW similarity). Historical SOTA for ride-hailing demand.

**Key modules:** model code only (partial), semantic view construction described but code incomplete.
**Datasets:** **not provided** (Didi privacy policy); pointer to Didi outreach program; NYC re-implementation by others exists (niloofarzarghampour fork, 3★, C++/Python with full preprocessing scripts).

**Quality signals:** ✅ MIT, ✅ citation correct; ❌ incomplete ("model part only"), ❌ Python 2.7, ❌ no data, ❌ no tests/CI — practically unusable directly.

**Best-fit use:** architecture reference for multi-view demand models; the third-party NY fork has the fuller preprocessing.

**VERDICT: STALE** (paper-only release) — reimplement rather than run.

## 2.5 Taxi OD demand: CSTN (liulingbo918/CSTN)

- **URL:** https://github.com/liulingbo918/CSTN
- **Stars:** 54 (forks 21)
- **Language:** Python (Keras 2.1.4 / TF 1.14)
- **License:** unverified
- **Last commit:** created Jul 2019; stale
- **Maintainer:** Lingbo Liu et al. (SCUT)

**What it implements:** IEEE T-ITS 2019 "Contextualized Spatial-Temporal Network for Taxi Origin-Destination Demand Prediction" — LSC (local spatial CNN), TEC (temporal evolution), GCC (global correlation context over region pairs) for **O-D matrix prediction** (not just per-region demand).

**Key modules:** `train_test.sh`, NYC-TOD preprocessing; requires Keras 2.1.4 + TF 1.14 pinned.
**Datasets:** NYC-TOD (Dropbox/BaiduYun links).
**Quality signals:** ✅ paper-faithful, script-driven; ❌ old pins, no tests/CI, small community.
**Best-fit use:** OD-matrix demand (fleet repositioning) baseline.
**VERDICT: NICHE / STALE** — valuable task coverage; dated stack.

## 2.6 Multi-model demand frameworks

- **cdsnlab/demand-pytorch** — https://github.com/cdsnlab/demand-pytorch ; **7★**, last push Dec 2024; PyTorch framework implementing **ConvLSTM, STResNet, DeepSTN, DMVST-Net, STMetaNet** for bike-sharing/public-transit/taxi demand with config/`trainer`/`evaluation` structure, Beijing & NYC preprocessed data included; results table partially empty (incomplete). **VERDICT: NICHE** — interesting modern re-implementation, low adoption.
- **TUMFTM/mod-prediction-framework** — https://github.com/TUMFTM/mod-prediction-framework ; 1★, LGPL-2.1, poetry + pre-commit (unusually good engineering hygiene for a thesis repo); models: ConvLSTM variants, citywide LSTM, SARIMAX, historical average, persistence; Munich ridesourcing fleet-strategy thesis (2022). **VERDICT: NICHE** — good template for grid demand pipelines with events support.
- **giallo41/taxi-demand** — 6★, TGNet (temporal-guided U-Net) for Seoul & NYC taxi requests; reports beating DMVST/STDN on NYC (MAPE 15.62%). **VERDICT: NICHE**.

## 2.7 Bike-sharing demand (Kaggle-style strong repos)

- **qinhanmin2014/kaggle-bike-sharing-demand** — https://github.com/qinhanmin2014/kaggle-bike-sharing-demand ; **14★**, Jupyter/Python, Gradient Boost + Random Forest, **rank 24/3251 (top 1%) in 60 lines of code**; no license stated; created 2019. **VERDICT: NICHE but high-signal** — a masterclass in feature-light GBM performance.
- **shashankvmaiya/Bike-Sharing-Demand-Prediction** — 15★, stacking ensemble (Linear/Ridge/RF/GBM/AdaBoost → meta models) on Capital Bikeshare DC data; documented EDA of workday vs weekend patterns. **VERDICT: NICHE** (good teaching artifact).
- **deerishi/ensemble-of-sarima-random-forests-and-gradient-boosting-trees** — 9★; residual-SARIMA-after-trees hybrid on Kaggle bike data; 2016-era. **VERDICT: NICHE**.
- Note: Kaggle bike-sharing demand is a solved classic; these repos matter as *feature-engineering templates* for any station-level micromobility demand model, not as libraries.

## 2.8 LibCity's on-demand service prediction (mentioned for completeness)

LibCity's "On-Demand Service Prediction" task and **Bigscity-LibCity-Datasets** (245★, Apache-2.0) host converted ride-hailing/OD grid datasets (e.g., NYC Taxi, CHIBike, T-Drive used by PDFormer). For ride-hailing demand at citywide scale, **PDFormer (grid mode) + LibCity datasets** is currently the most usable open stack — more so than the 2018 paper repos above.

**Section 2 verdict summary:** OSMnx and Trajectron++ are the keepers; demand-prediction classics are mostly museum pieces — rebuild on tsl/LibCity grids instead.

---

# CATEGORY 3: ENERGY ML

## 3.1 Nixtla NeuralForecast

- **URL:** https://github.com/Nixtla/neuralforecast/
- **Stars:** ~4,174 (forks 494, open issues 23)
- **Language:** Python (PyTorch / PyTorch Lightning)
- **License:** Apache-2.0
- **Last commit:** **very active** — v3.3.0 on PyPI; recent security-hardened model serialization (safetensors default, pickle opt-in) shows mature release engineering
- **Maintainer:** Nixtla (company) — part of the "Nixtlaverse" with StatsForecast, MLForecast, HierarchicalForecast, TimeGPT.

**What it implements:** 30+ neural forecasting architectures behind one sklearn-style `.fit()/.predict()` API: **MLP, LSTM, GRU, RNN, TCN, BiTCN, TimesNet, DeepAR, NBEATS, NBEATSx (official), NHITS (official, AAAI 2023), TiDE, DeepNPTS, TSMixer(x), DLinear, NLinear, TFT, Informer, AutoFormer, FedFormer, PatchTST, iTransformer, StemGNN, TimeLLM, MLPMultivariate**. For load forecasting: NBEATS/NHITS/PatchTST/TFT/iTransformer are the go-to models; exogenous regressors (weather, holidays, price) supported via `futr_exog_list`/`hist_exog_list`.

**Key modules:** `neuralforecast/models/*` (one file per model), `core.py` (NeuralForecast class), losses (MAE/MSE/quantile/likelihood), `tsdataset` loaders, interpretability (trend/seasonality decomposition, IntegratedGradients/Shapley), probabilistic adapters, auto-tuning via **Ray/Optuna**, HierarchicalForecast reconciliation hooks.

**Datasets:** bring-your-own long-format panels (utils include AirPassengers demo); pairs naturally with Monash/other public load datasets.

**Quality signals:** ✅ Apache-2.0, ✅ pip/conda, ✅ extensive readthedocs (nixtlaverse), ✅ official author implementations (NHITS, NBEATSx), ✅ auto-HPO, ✅ probabilistic + interpretable forecasts, ✅ active issue response, ✅ hardened serialization; ❌ no Docker image officially, weights are trained-on-your-data (no pretrained load model), ⚠️ TimeLLM carries LLM licensing considerations.

**Limitations:** panel-format onboarding (long DataFrames); neural models still require tuning vs. statistical baselines (StatsForecast) on small data.

**Best-fit use:** **default choice for load/energy demand forecasting** — day-ahead and intra-day electric load, district heating, building consumption, EV aggregate load.

**VERDICT: ESSENTIAL**

## 3.2 Google TimesFM

- **URL:** https://github.com/google-research/timesfm
- **Stars:** ~35,258 (trending: +410/week at research time; 34.6k→35.3k in Oct–Nov 2026)
- **Language:** Python (JAX/Flax + PyTorch backends)
- **License:** **Apache-2.0 for code AND weights ≤ v2.5; TimesFM 3.0 weights under separate `timesfm-non-commercial-license-v1.0` (non-commercial/non-production only; commercial use via BigQuery ML/Vertex)**
- **Last commit:** v3.0.0 release Aug 2026; last commit Sep 2026 — **actively maintained**; 159 open issues
- **Maintainer:** Google Research (Rajat Sen, Yichen Zhou, Abhimanyu Das, Petros Mol et al.); ICML 2024 paper "A decoder-only foundation model for time-series forecasting."

**What it implements:** Decoder-only pretrained **time-series foundation model** — 200M params (v2.5), 16k context, pretrained on 100B+ real-world points; zero-shot forecasting ranked #1 on TIME Benchmark (50 domains) and GIFT-Eval; continuous quantile head for probabilistic output; XReg covariate support; LoRA fine-tuning example; in-context fine-tuning (ICF); `AGENTS.md`/`SKILL.md` for agent tooling.

**Key modules:** `src/timesfm` (v2.5/3.0 code), archived `v1`, huggingface checkpoints (`google/timesfm-2.5-200m-pytorch`, `google/timesfm-3.0-pytorch`), BigQuery ML `AI.FORECAST` integration.

**Datasets:** pretrained generically (Google Trends, Wikipedia, synthetic) — apply zero-shot to load curves, irradiance, traffic series.

**Quality signals:** ✅ CI-scale engineering, ✅ HF checkpoints, ✅ quantile forecasts, ✅ docs + agent skill files, ✅ massive community; ⚠️ "not an officially supported Google product" disclaimer for the open repo; ⚠️ v3 weights non-commercial.

**Limitations:** contiguous-history requirement (impute gaps first); GPU/Flax benefits for 16k contexts; forecasting only (no anomaly detection); license bifurcation for commercial deployments.

**Best-fit use:** zero-shot baseline for *any* city energy series (load, EV, solar) before training custom models; strong with few labels.

**VERDICT: ESSENTIAL** (mind the v3 weight license for commercial products)

## 3.3 BuildingsBench (NatLabRockies/BuildingsBench)

- **URL:** https://github.com/NatLabRockies/BuildingsBench
- **Stars:** 119 (forks 24)
- **Language:** Python (PyTorch)
- **License:** BSD 3-Clause
- **Last commit:** created Jun 2023 (NeurIPS 2023 D&B); homepage maintained; low activity since
- **Maintainer:** Natural Resources Canada / CanmetENERGY "NatLabRockies" team.

**What it implements:** Platform for **large-scale pretraining and benchmarking of short-term load forecasting (STLF)** using the synthetic **Buildings-900K** dataset (statistically representative of the entire US building stock, from the NLR End-Use Load Profiles DB), benchmarked on zero-shot STLF and transfer learning across real building datasets. Baselines from persistence to transformers (Gaussian and token-based probabilistic heads); public **leaderboard with downloadable checkpoints on AWS S3**.

**Key modules:** index-based PyTorch Dataset for pretraining, loaders for multiple real building datasets (tensors or DataFrames), baseline models, metrics (NRMSE, RPS/Gaussian CRPS), checkpoint zoo.

**Datasets:** Buildings-900K (synthetic, pretraining) + real public building-energy datasets for eval.

**Quality signals:** ✅ BSD-3, ✅ NeurIPS-reviewed, ✅ **pretrained checkpoints published**, ✅ leaderboard/docs site, ✅ paper + docs; ❌ small community (119★), no CI visible, activity slowed post-publication.

**Best-fit use:** building-level STLF research, pretraining energy foundation models, zero-shot generalization studies.

**VERDICT: USEFUL (essential if doing building STLF)** — rare combination of dataset + pretrained weights + benchmark.

## 3.4 Short-term load forecasting classics

- **yalickj/load-forecasting-resnet** — https://github.com/yalickj/load-forecasting-resnet ; **108★**, Python, **MIT**, created 2018, 38 contributions by maintainer (Kunjin Chen et al.); implements "Short-term Load Forecasting with Deep Residual Networks" (IEEE Trans. Smart Grid 2018) incl. `ResNetPlus_ISONE.py`; **data bundled: ISO-NE load+temperature 2003–2014**, North American test case added 2021; PyTorch version ranked **5th in a day-ahead electricity demand competition (post-COVID)**. **VERDICT: USEFUL** — small but real, MIT, with data; good ResNet-STLF reference.
- **ki-ljl/LSTM-Load-Forecasting** — https://github.com/ki-ljl/LSTM-Load-Forecasting ; **278★**, Python, **MIT**, created 2022; LSTM/BiLSTM for univariate-single-step, multivariate-single-step and multivariate-multi-step electric load forecasting; **trained `.pkl` model checkpoints included in `models/`**, clean `args/data_process/util` structure, sample CSV data. **VERDICT: USEFUL** (educational + runnable) — good starter for utilities teams.
- **KEV0143/Comparative-analysis-of-hourly-load-forecasting-using-PatchTST-TFT-NHiTS-and-CatBoost** — https://github.com/KEV0143/... ; **950★ claimed, 0 forks** (⚠️ **star anomaly — treat with suspicion**, possible inflated counts), Python, Apache-2.0, created Sep 2025, last push Apr 2026, 2 contributors; benchmarks PatchTST vs TFT vs N-HiTS vs CatBoost for 24-hour load prediction with preprocessing/validation/viz. **VERDICT: NICHE** — content matches a useful benchmark, but verify star legitimacy before citing popularity.
- **KIT-IAI/load-forecasting-benchmark** — https://github.com/KIT-IAI/load-forecasting-benchmark ; **2★**, Python, license "Other", created Jul 2026 (brand new), maintainer hertelm (Karlsruhe Institute of Technology); benchmarks electrical load forecasting models on **UCI Electricity (2011–2014) + FeederBW + TransnetBW** with ERA5 weather covariates; W&B logging; config-driven; publishes best-model predictions for comparison. **VERDICT: USEFUL (emerging)** — new but from a serious energy-institute group with proper data licensing (CC BY 4.0 sources).
- **austnbell/energyDemand** — https://github.com/austnbell/energyDemand ; 18★, Jupyter/Python, 2020; STGNN variants (**STGCN, STGCN+metadata, STG-LSTM**) for node-level load forecasting on **RE-Europe** (1,496 buses, 2,156 lines). **VERDICT: NICHE** — nice example of traffic STGNNs transferred to power grids.
- **OpenSTEF (see 3.6)** and **LSTM-Load-Forecasting** cover most practitioner needs alongside NeuralForecast.

## 3.5 Building energy data: Building Data Genome 2

- **URL:** https://github.com/buds-lab/building-data-genome-project-2
- **Stars:** ~274 (release page reference)
- **Language:** Jupyter Notebook / Python (pandas)
- **License:** repo license updated Oct 2023 (data published for research — **verify CC terms in LICENSE before redistribution**)
- **Last commit:** Oct 2023 (license/weather fixes) — dormant but data is frozen/stable
- **Maintainer:** C. Miller, D. Rojas (Univ. of Southern California BUDS Lab), ponybiam et al.

**What it implements:** The **BDG2 dataset** itself: 3,053 energy meters from 1,636 non-residential buildings, hourly, full years 2016–2017, electricity/heating/cooling/steam/irrigation/solar/gas/water meters + rich metadata (Energy Star scores, EUI, floor area, use category, timezone, LEED) + weather. Subset = **ASHRAE Great Energy Predictor III (GEPIII)** competition data (2,380 meters / 1,449 buildings).

**Key modules:** `data/meters/{raw,cleaned,kaggle}`, `data/metadata`, `data/weather`, notebooks for EDA (metadata, weather, all-meters joins), wiki documenting every metadata feature.

**Datasets:** BDG2 + GEPIII Kaggle-aligned files.

**Quality signals:** ✅ versioned release (v1.0), ✅ extensive wiki, ✅ science-paper preprint (STBE), ✅ widely cited in building-energy ML; ❌ notebooks not a library, no CI, dormant since 2023.

**Best-fit use:** *the* standard open non-residential building energy dataset — load forecasting, M&V, anomaly detection, building archetype studies.

**VERDICT: ESSENTIAL (as dataset)** / code is just EDA notebooks.

## 3.6 OpenSTEF (Open Short-Term Energy Forecasting)

- **URL:** https://github.com/OpenSTEF/openstef
- **Stars:** ~180 (forks 64, open issues 58)
- **Language:** Python (≥3.12 for v4)
- **License:** MPL-2.0
- **Last commit:** **active** — v4.0.0 architectural refactor (monorepo), GitHub releases, SonarQube quality gate badges (coverage/maintainability/security)
- **Maintainer:** LF Energy project (hosted at Linux Foundation Energy); community of grid operators (originally TenneT-adjacent Dutch ecosystem), vendors, researchers; Slack + 4-weekly community meetings.

**What it implements:** End-to-end **probabilistic short-term load/generation forecasting pipelines** for grid operators: data validation → feature engineering (energy-specific: solar position/atmospheric features) → training any scikit-learn-compatible model (linear, XGBoost, LightGBM, meta-ensembles) → probabilistic forecasts with uncertainty bands → delivery via API/GUI; fallback forecast strategies for resilience; split forecasts by energy source (wind/solar share per EU Reg. 543/2013); supports foundation time-series models too.

**Key modules:** monorepo packages `openstef-core`, `openstef-models`, `openstef-beam` (backtesting/evaluation/metrics), `openstef-meta` (base-learner ensembles); companion repos: `openstef-reference` (30★ — full Docker Compose stack: forecast engine + InfluxDB/MySQL + **Grafana dashboards**), `openstef-offline-example` (notebooks), `openstef-dbc` (DB connectors).

**Datasets:** BYO time series (net load/generation) + weather/market-price externals.

**Quality signals:** ✅ MPL-2.0, ✅ **Docker/Compose reference deployment**, ✅ API + GUI + Grafana, ✅ CI/quality gates/coverage badges, ✅ CII Best Practices, ✅ PyPI package, ✅ docs site, ✅ probabilistic + fallback design (production thinking); ⚠️ 58 open issues, ⚠️ smaller model zoo than NeuralForecast (sklearn-based, not deep nets by default).

**Limitations:** Python 3.12 requirement (v4) limits legacy environments; energy-sector-specific assumptions; deep-learning models optional rather than core.

**Best-fit use:** **production-grade short-term forecasting for grid operators/energy companies** — the closest thing in this survey to a deployable energy forecasting *system* rather than a model zoo.

**VERDICT: ESSENTIAL (for operational energy forecasting)**

## 3.7 Solar/renewables: Solar Forecast Arbiter

- **URL (core):** https://github.com/solararbiter/solarforecastarbiter-core
- **Stars:** 47 (org: 7 repos — dashboard 11★, api 11★)
- **Language:** Python (Flask for API)
- **License:** MIT (all components)
- **Last commit:** dashboard last push May 2023; project transitioned to **EPRI stewardship (2022)**, hosted at forecastarbiter.epri.com — maintenance slowed; 152 open issues on core
- **Maintainer:** SolarArbiter org (formerly NREL/Sandia/DOE SETO-funded; now EPRI)

**What it implements:** Infrastructure for **impartial, repeatable, auditable solar/net-load forecast evaluation** — data gathering, validation, probabilistic metrics (CRPS, calibration, skill scores), reporting; originally DOE Solar Energy Technologies Office award DE-EE0008214. Three-part system: Core package + HTTP API (with OpenAPI spec via apispec) + Flask dashboard.

**Key modules:** observation/forecast lifecycles, bias/clear-sky index metrics, probabilistic scoring, JSON API, dashboard templates.

**Datasets:** user-registered sites/forecasts; reference datasets for solar irradiance/power.

**Quality signals:** ✅ MIT, ✅ readthedocs, ✅ OpenAPI spec, ✅ releases (dashboard 28 releases, v1.0.13), ✅ mission-critical evaluation semantics documented; ⚠️ issue backlog (152), activity slowed post-EPRI transition.

**Limitations:** evaluation platform, not an ML model zoo — you bring forecasts; heavy operational assumptions; aging codebase.

**Best-fit use:** benchmarking competing solar/irrigance forecasts with rigorous probabilistic metrics; regulatory-grade forecast evaluation.

**VERDICT: NICHE → USEFUL** if you need *forecast evaluation governance* rather than models; **STALE-ish** but stable.

## 3.8 EV charging prediction/optimization

- **IntelligentSystemsLab/ST-EVCDP** — https://github.com/IntelligentSystemsLab/ST-EVCDP ; **266★**, Python, **MIT**, created Nov 2023, **actively updated through Mar 2025**; hosts the **ST-EVCDP Shenzhen dataset** (18,061 public charging piles, 30 days @5-min, 247 traffic-zone nodes/1,006 edges) and successor **UrbanEV** (24,798 piles, 6 months, station-level, published in *Scientific Data* 2025; companion repo `IntelligentSystemsLab/UrbanEV` + Dryad mirror). Includes runnable **PAG** (physics-informed attention graph) model with LSTM/GCN-LSTM/GAT-LSTM baselines; weather data; sibling project **ChatEV** (LLM-based EV demand forecasting, TRD 2024). **VERDICT: ESSENTIAL (dataset) / USEFUL (code)** — best open spatio-temporal EV charging data available.
- **LSY-Cython/DiffPLF** — https://github.com/LSY-Cython/DiffPLF ; 40★, Python, last push Jun 2024; PSCC 2024 "Conditional Diffusion Model for Probabilistic Forecasting of EV Charging Load" (HKUST-GZ); pipeline `main.py` with isTrain/isCollect/isRefine stages; datasets from Kaggle California EV usage + Meteostat forecasts. **VERDICT: USEFUL (research)** — modern probabilistic (diffusion) approach for charging load intervals.
- **XingshuaiHuang/MetaProbformer** — https://github.com/XingshuaiHuang/MetaProbformer ; 30★, Python, **MIT**, 2023; T-ITS meta-learning + Informer for **probabilistic** charging-load forecasting; 4 real datasets (Palo, Boulder, NL, Perth) with dataset stats documented. **VERDICT: USEFUL (research baseline)**.
- **fbohu/Deep-Spatio-Temporal-Forecasting-of-Electrical-Vehicle-Charging-Demand** — 46★, Jupyter/Python, 2021; deep spatio-temporal forecasting with 7-day/30-day forecast visualizations; README thin ("will be updated"). **VERDICT: NICHE**.
- **Ubaid014/DeepBoost-for-EVs-charging-station-load-forecasting** — 4★, notebooks, 2024–2025; CatBoost+XGBoost+LSTM+LR ensemble ("DeepBoost") vs Informer on ACN data; paper: Alexandria Engineering Journal 2025. **VERDICT: NICHE**.
- **IasonKyriakopoulos/electric-vehicle-charging-load-forecasting** — 7★, MIT, Nov 2025 (fresh); ML comparison study (TensorFlow 2.13, XGBoost, ARIMA/pmdarima), `run_all.sh` one-command pipeline, Singularity container env — unusually reproducible for its size; depends on `ev-load-open-data`. **VERDICT: USEFUL (reproducibility-minded small benchmark)**.

## 3.9 GAN / synthetic energy data

- **jsyoon0823/TimeGAN** — https://github.com/jsyoon0823/TimeGAN ; stars unverified in this pass (historically ~1.5–2k); Python, **TensorFlow 1.x**, NeurIPS 2019 (Yoon, Jarrett, van der Schaar); canonical codebase for time-series GANs with **energy dataset included** (UCI Appliances energy prediction, `data/energy_data.csv` ~4.4MB) plus sine/stock; metrics suites (discriminative, predictive, PCA/t-SNE visualization); tutorial notebook. Warning: logs show TF-contrib deprecation — **runs only on legacy TF**. **VERDICT: USEFUL (citation/canonical) / STALE (runtime)** — the standard for synthetic energy-profile generation papers.
- **MODERATE-Project/Synthetic-Load-Profiles** — https://github.com/MODERATE-Project/Synthetic-Load-Profiles ; stars unverified; GAN synthesizing **annual hourly electrical load profiles** per household for privacy-preserving research (EU MODERATE project); simple CSV input contract (365–368 days × columns per household). **VERDICT: USEFUL (niche)** — directly targets the "synthetic load profiles for DR training" use case.
- **ShashankAsre/TimevariantGAN-AEMO-dataset** — TimeGAN applied to AEMO Australian NEM price/demand (2020, 5 states); Colab notebook with added classification metrics. **VERDICT: NICHE** (dataset-specific derivative).

## 3.10 Demand response / building flexibility

- **citylearn-project/CityLearn** — https://github.com/citylearn-project/CityLearn ; **649★** (forks 219), Python, **MIT**, created 2019, **actively maintained (v3)**; official **Gymnasium RL environment for building energy coordination, demand response and load shaping**: buildings + thermal systems + PV + batteries + EVs + flexible loads with electrical limits, local energy sharing (energy communities), member/asset churn, failure injection; datasets incl. `citylearn_challenge_2022_phase_all_plus_evs`; pip-installable (`pip install citylearn`); baseline agents (BusinessAsUsual etc.), KPI reporting; lineage from CityLearn challenges (NeurIPS-affiliated competitions). **VERDICT: ESSENTIAL for DR/RL work** — the standard open environment for smart-grid building coordination.
- **srmadani/Demand-Response-in-Commercial-Buildings** — stars unverified; **MIT**; implements **SACD, PPOD, D3QN, DDPG, TD3, PPO** for HVAC (discrete) + lighting (continuous) control with real data (CA-QC hourly, LMP prices, temperature); reports 27% peak reduction, 5.8% cost savings, 4.9% CO₂ reduction with VaR/CVaR risk metrics; `report.ipynb` reproduces paper results. **VERDICT: USEFUL (research)** — strongest single DR-RL research code found.
- **LBNL-ETA/DFLEXLIBS** — https://github.com/LBNL-ETA/DFLEXLIBS ; forks 3, stars ~11; license "Other"; **LBNL** library for portable **HVAC demand-flexibility controls** using semantic models (Open DF Control Sequence spec): shed/shift/composite zone controls + plant-level chiller-water reset, plus Annex-81 KPI analytics; designed for deployment across buildings with minimal per-building code. **VERDICT: USEFUL (institutional)** — not an ML repo, but the LBNL production-grade flexibility-controls layer that ML DR policies eventually wrap.
- **alwaysbyx/e2e-DR-learning** — 10★, MIT, ACM e-Energy 2022; OptNet gradient-based **demand response model identification** (storage, building pool, electricity consumer models) vs IO/NN baselines. **VERDICT: NICHE (interesting theory)**.
- **kgrajski/agentic_bems_paper** — 0★, MIT, Aug 2026; LangGraph multi-agent BEMS MVP (DR bidding advisor, cross-system optimizer, BESS balancer) with cvxpy perfect-foresight LP baselines — early-stage agentic-AI-for-buildings artifact. **VERDICT: NICHE (watchlist)**.

*(OPENEF note: the Enel "OPENEF" open energy forecasting framework was not located as a currently active public GitHub repository in this pass; the closest open, grid-operator-grade equivalents are OpenSTEF (LF Energy) and the Nixtla stack. `theMomax/openefs` — a 2-star Go/Python "Open Energy Forecasting Service" from 2019 — exists but is dormant and tiny: **VERDICT: STALE**.)*

---

# CATEGORY 4 (BONUS): AIR QUALITY ML

- **yoshall/AirFormer** — https://github.com/yoshall/airformer ; **163★**, Python (PyTorch 1.10), license unverified; AAAI 2023 "Predicting Nationwide Air Quality in China with Transformers" — 72-hour predictions at thousands of stations; ships a tiny (60-instance) sample of the >500GB dataset for code comprehension. **VERDICT: USEFUL** — strongest AQI transformer repo here.
- **decisionintelligence/Air-DualODE** — https://github.com/decisionintelligence/Air-DualODE ; 24★, Python, created Feb 2025; **ICLR 2025** "Air Quality Prediction with Physics-Guided Dual Neural ODEs in Open Systems" (physics dynamics + data-driven dynamics + fusion); `create_graph.py` for new datasets; Beijing (KDD Cup 2018) + KnowAir data. **VERDICT: USEFUL (research, current)**.
- **kethmih/AirPhyNet** — https://github.com/kethmih/airphynet ; 42★, Python, **MIT**, 2023; physics-guided neural ODE network for 72h AQ prediction; Beijing sample data on Google Drive; based on STDEN training framework. **VERDICT: NICHE/USEFUL**.
- **leizhang-geo/ST-CausalConvNet** — https://github.com/leizhang-geo/ST-CausalConvNet ; 73★, Python, **Apache-2.0**; *Computers & Geosciences* 2021 — spatiotemporal **causal** convolutional network for hourly PM2.5 in Beijing; includes Microsoft Urban Computing air data + station-correlation preprocessing + RNN/GRU/LSTM comparators. **VERDICT: USEFUL** (well-licensed, causal framing).
- **txytju/air-quality-prediction** — 54★, KDD Cup 2018 (rank 31): seq2seq + XGBoost for Beijing/London 48h AQ; rich EDA notebooks. **VERDICT: NICHE (competition reference)**.

Air quality as a whole is a healthy small niche: physics-guided models (DualODE, AirPhyNet) dominate recent work; standard datasets are KDD Cup 2018 Beijing/London and KnowAir.

---

# FINAL SUMMARY TABLE

| # | Repo | Stars | Language | Models / What it is | Verdict |
|---|------|-------|----------|----------------------|---------|
| 1 | LibCity/Bigscity-LibCity | ~1,167 | Python (PyTorch) | 74 models, 9 tasks, 52 datasets | **ESSENTIAL** (stale) |
| 2 | TorchSpatiotemporal/tsl | ~388 | Python (PyTorch/PyG) | ST library + LargeST loader | **ESSENTIAL** |
| 3 | benedekrozemberczki/pytorch_geometric_temporal | ~3,000 | Python (PyG) | 30+ STGNNs (DCRNN→GMAN/MTGNN) | **ESSENTIAL** |
| 4 | deepkashiwa20/DL-Traff-Graph (+Grid) | ~182 | Python (PyTorch/TF) | Fair-hyperparameter benchmark, 12 models | USEFUL (stale) |
| 5 | trainingl/STG4Traffic | small | Python (PyTorch) | 16-model STGNN benchmark | USEFUL/NICHE |
| 6 | nnzhan/Graph-WaveNet | ~822 | Python (PyTorch) | GWNET (adaptive adj + dilated TCN) | USEFUL (stale) |
| 7 | liyaguang/DCRNN | ~1,455 | Python (TF1) | DCRNN + METR-LA/PEMS-BAY source | USEFUL data / STALE code |
| 8 | VeritasYin/STGCN_IJCAI-18 | ~1,246 | Python (TF) | STGCN original (BSD-2) | USEFUL (stale) |
| 9 | guoshnBJTU/ASTGCN-2019-pytorch | unverified | Python (PyTorch) | ASTGCN/MSTGCN (recent component) | NICHE (stale) |
| 10 | zhengchuanpan/GMAN (+PyTorch port) | ~534 (+175) | Python (TF1) | GMAN encoder-decoder attention | USEFUL (stale) |
| 11 | LeiBAI/AGCRN | ~444 | Python (PyTorch) | AGCRN (+STGODE/MegaCRN family) | USEFUL |
| 12 | nnzhan/MTGNN | ~948 | Python (PyTorch) | MTGNN graph-learning MTS | USEFUL (stale) |
| 13 | lehaifeng/T-GCN | ~1,789 | Python (TF + PyTorch) | T-GCN = GCN+GRU | USEFUL (stale) |
| 14 | BUAABIGSCity/PDFormer | ~297 | Python (PyTorch/LibCity) | PDFormer (delay-aware transformer) | USEFUL |
| 15 | XDZhelheim/STAEformer | 247 | Python (PyTorch) | STAEformer — vanilla transformer SOTA | USEFUL (license?) |
| 16 | liuxu77/LargeST | 299 | Python (PyTorch) | 8,600-sensor benchmark + 12 baselines | **ESSENTIAL dataset** |
| 17 | HKUDS/OpenCity | 189 | Python (PyTorch) | Traffic foundation model, zero-shot, 3 sizes + weights | USEFUL (research) |
| 18 | HKUDS/UrbanGPT | ~462 | Python (PyTorch/LLM) | Spatio-temporal LLM (Vicuna-7B) | NICHE/USEFUL |
| 19 | cdsnlab/traffic-pytorch | small | Python (PyTorch) | ASTGCN/DCRNN/GMAN/STGCN/GWNET framework | NICHE |
| 20 | FelixOpolka/STGCN-PyTorch | ~200s | Python (PyTorch) | Minimal STGCN demo | NICHE |
| 21 | tijsmaas/TrafficPrediction | 31 | Python | DCRNN+GWNET+GMAN **with pretrained weights** | NICHE |
| 22 | ShuhaoLii/LaneLevel-Traffic-Benchmark | small | Python | 12+ lane-level models + datasets | USEFUL (lane niche) |
| 23 | gboeing/osmnx | ~5,870 | Python | Urban street-network download/analysis (MIT) | **ESSENTIAL** |
| 24 | StanfordASL/Trajectron-plus-plus | ~833 | Python/Notebook (PyTorch) | Multi-agent trajectory forecasting (MIT) | **ESSENTIAL** |
| 25 | TolicWang/DeepST (lucktroy lineage) | 116 | Python (TF1) | Crowd-flow CNN (DeepST/ST-ResNet ancestor) | STALE/NICHE |
| 26 | huaxiuyao/DMVST-Net | 109 | Python (Keras/Py2) | Multi-view taxi demand (incomplete) | STALE |
| 27 | liulingbo918/CSTN | 54 | Python (Keras/TF1) | Taxi O-D demand (T-ITS'19) | NICHE (stale) |
| 28 | cdsnlab/demand-pytorch | 7 | Python (PyTorch) | ConvLSTM/STResNet/DeepSTN/DMVST/STMetaNet | NICHE |
| 29 | TUMFTM/mod-prediction-framework | 1 | Python (TF) | Munich ridesourcing demand (ConvLSTM/SARIMAX) | NICHE |
| 30 | qinhanmin2014/kaggle-bike-sharing-demand | 14 | Python | GBM+RF top-1% Kaggle solution | NICHE (high-signal) |
| 31 | Nixtla/neuralforecast | ~4,174 | Python (PyTorch) | 30+ models: NBEATS/NHITS/PatchTST/TFT/... | **ESSENTIAL** |
| 32 | google-research/timesfm | ~35,258 | Python (JAX/PyTorch) | TimesFM foundation model (weights ≤2.5 Apache; 3.0 non-comm.) | **ESSENTIAL** |
| 33 | NatLabRockies/BuildingsBench | 119 | Python (PyTorch) | Buildings-900K STLF benchmark + checkpoints (BSD-3) | USEFUL |
| 34 | yalickj/load-forecasting-resnet | 108 | Python | ResNet STLF (ISO-NE data, MIT) | USEFUL |
| 35 | ki-ljl/LSTM-Load-Forecasting | 278 | Python (PyTorch) | LSTM/BiLSTM load forecast + weights (MIT) | USEFUL |
| 36 | KEV0143/PatchTST-TFT-NHiTS-CatBoost | 950⚠️ | Python | Load forecast benchmark (Apache-2.0) | NICHE (star anomaly) |
| 37 | KIT-IAI/load-forecasting-benchmark | 2 | Python | UCI/FeederBW/TransnetBW load benchmark | USEFUL (emerging) |
| 38 | austnbell/energyDemand | 18 | Python/Notebook | STGNN node-level load (RE-Europe) | NICHE |
| 39 | buds-lab/building-data-genome-project-2 | ~274 | Python/Notebook | BDG2 building energy dataset (3,053 meters) | **ESSENTIAL dataset** |
| 40 | OpenSTEF/openstef (+reference) | ~180 (+30) | Python | Production probabilistic load/gen pipelines (MPL-2.0, Docker) | **ESSENTIAL** |
| 41 | SolarArbiter/solarforecastarbiter-core | 47 | Python | Solar forecast evaluation platform (MIT, EPRI) | NICHE/USEFUL |
| 42 | IntelligentSystemsLab/ST-EVCDP (+UrbanEV) | 266 | Python (PyTorch) | Shenzhen EV charging datasets + PAG model (MIT) | **ESSENTIAL dataset** |
| 43 | LSY-Cython/DiffPLF | 40 | Python | Diffusion probabilistic EV load (PSCC'24) | USEFUL (research) |
| 44 | XingshuaiHuang/MetaProbformer | 30 | Python | Meta-learning Informer for EV prob. forecast (MIT) | USEFUL (research) |
| 45 | fbohu/...EV-Charging-Demand | 46 | Python/Notebook | Deep spatio-temporal EV demand | NICHE |
| 46 | jsyoon0823/TimeGAN | ~1.5k (unverified) | Python (TF1) | Time-series GAN with energy data | USEFUL cite / STALE |
| 47 | MODERATE-Project/Synthetic-Load-Profiles | small | Python | GAN annual load-profile synthesis | NICHE/USEFUL |
| 48 | citylearn-project/CityLearn | ~649 | Python (Gymnasium) | DR/RL building-energy environment (MIT, v3) | **ESSENTIAL** |
| 49 | srmadani/Demand-Response-in-Commercial-Buildings | unverified | Python | SACD/PPO/TD3/DDPG DR control (MIT) | USEFUL |
| 50 | LBNL-ETA/DFLEXLIBS | ~11 | Python | Semantic HVAC demand-flexibility controls | USEFUL (institutional) |
| 51 | yoshall/AirFormer | 163 | Python (PyTorch) | Nationwide AQ transformer (AAAI'23) | USEFUL |
| 52 | decisionintelligence/Air-DualODE | 24 | Python (PyTorch) | Physics-guided dual-ODE AQ (ICLR'25) | USEFUL |
| 53 | kethmih/AirPhyNet | 42 | Python (PyTorch) | Physics-guided AQ ODE net (MIT) | NICHE/USEFUL |
| 54 | leizhang-geo/ST-CausalConvNet | 73 | Python (PyTorch) | Causal conv PM2.5 forecast (Apache-2.0) | USEFUL |

*(Stars marked "unverified" were not confirmed with a direct page fetch in this pass; "small" = below ~100 or not surfaced by search.)*

---

# STRATEGIC RECOMMENDATIONS

**If you are building a smart-city ML platform, adopt this stack:**

1. **Road/graph construction:** OSMnx (production-quality, MIT) → adjacency for any STGNN.
2. **Spatiotemporal modelling core:** `tsl` (TorchSpatiotemporal) or PyTorch Geometric Temporal — maintained, tested, pip-installable; port LibCity configs for tasks it lacks.
3. **Traffic baselines to beat:** STAEformer (simple, strong), PDFormer (transformer SOTA), AGCRN (adaptive graph), GWNET, GMAN (long horizon) — all reproducible via LibCity/tsl/LargeST harnesses.
4. **Scale validation:** always run on **LargeST** (8,600 sensors), not just METR-LA (207).
5. **Ride-hailing demand:** LibCity on-demand task + PDFormer grid mode on NYC Taxi/CHIBike atomic datasets; Trajectron++ if you need agent trajectories.
6. **Energy load:** NeuralForecast (model zoo) + TimesFM ≤2.5 weights (zero-shot, Apache) for baselines; **OpenSTEF** for the operational probabilistic pipeline with API/Grafana; BuildingsBench for building-level pretraining.
7. **EV charging:** ST-EVCDP/UrbanEV datasets + DiffPLF/MetaProbformer for probabilistic intervals.
8. **Demand response:** CityLearn (RL env) + LBNL DFLEXLIBS (control semantics); DR-RL research baselines from srmadani repo.
9. **Synthetic profiles:** TimeGAN-style generation (port to TF2/PyTorch) or MODERATE load-profile GAN for privacy-preserving training data.
10. **Air quality:** AirFormer/Air-DualODE if your scope extends to AQI.

**Risks to manage:** (a) TF1-era canonical repos (DCRNN, GMAN, STGCN, T-GCN-TF, TimeGAN, DMVST) will not run on modern stacks — plan ports; (b) missing licenses (STAEformer, several small repos) block commercial use; (c) LargeST data is CC BY-NC (non-commercial); TimesFM 3.0 weights are non-commercial; (d) LibCity staleness means pinning old dependencies; (e) verify star counts on outlier repos (KEV0143 benchmark) before trusting popularity signals.

**Repo-count: 54 detailed entries (target was ≥30). Category coverage: Traffic 22, Mobility 8, Energy 20, Air quality 5 (some repos span categories).**
