# GitHub Repositories for Smart-City AI/ML: A Research Dossier

**Scope:** Vision, LLMs, datasets, simulators, federated/edge ML, environment ML, and public-safety ML for smart-city systems.
**Method:** Web research only (GitHub pages, papers, docs, package indexes). No repositories were cloned and no code was executed. Star counts, commit counts, and activity markers are as reported by GitHub/search indexes at research time and may drift.
**Categories:** (1) Environment ML, (2) Public Safety / Vision, (3) Urban Vision, (4) LLM / Foundation Models for Cities, (5) Federated / Edge / TinyML, (6) City Simulators & Datasets.
**Verdicts:** Each repository ends with **essential**, **useful**, **niche**, or **stale**.

---

## 1. Environment ML

Urban environmental monitoring—air quality, flooding, waste, urban heat, and water quality—is one of the most mature application areas for smart-city ML. The repos below span official research code, production data clients, and lightweight benchmarks.

### 1.1 `iipr/air-quality` — Spatio-temporal air-quality forecasting (ST-AQF)

- **URL:** https://github.com/iipr/air-quality
- **Stars / language / license / activity:** Low single-digit stars (~9 commits observed); Python; GPL-3.0; early-stage academic code.
- **Maintainer:** Institute for Interdisciplinary Research in Science (IIPR)–affiliated authors.
- **What it implements:** The ST-AQF (Spatio-Temporal Air Quality Forecasting) approach—graph/spatio-temporal modeling of pollutant time series (PM2.5, PM10, NO₂, O₃, etc.) across monitoring stations, combining temporal convolutions or RNN-style encoders with spatial dependence over the sensor graph.
- **Key modules:** Data ingestion for station readings, graph construction from station coordinates, spatio-temporal encoder, forecasting head, training/eval scripts.
- **Datasets:** Public air-quality station networks (typically city-scale OpenAQ-style or municipal feeds).
- **Quality signals:** Minimal—no visible CI, limited docs, small commit history; paper-aligned but not productized.
- **Limitations:** Sparse documentation, unclear long-term maintenance, limited baselines and error analysis.
- **Best fit:** Researchers wanting a compact reference implementation of spatio-temporal AQ forecasting to extend; not a production monitoring stack.
- **VERDICT: niche**

### 1.2 `openaq/openaq-python` (+ OpenAQ org: `awesome-air-quality`)

- **URL:** https://github.com/openaq/openaq-python ; https://github.com/openaq ; https://github.com/openaq/awesome-air-quality
- **Stars / language / license / activity:** `openaq-python` ≈ 22★; `awesome-air-quality` ≈ 71★; Python / Markdown; Apache-2.0 / CC0 respectively; actively maintained by the OpenAQ non-profit.
- **Maintainer:** OpenAQ (global open air-quality data platform).
- **What it implements:** Official Python client for the OpenAQ API—query, paginate, and normalize ground-station measurements worldwide; plus a curated awesome-list of AQ tools, datasets, and papers.
- **Key modules:** API client, models/typed responses, examples; awesome-list categories (sensors, models, dashboards).
- **Datasets:** Access to OpenAQ’s aggregated global observations (thousands of stations, dozens of pollutant types).
- **Quality signals:** Typed client, releases on PyPI, org-level governance, clear docs; not an ML model itself.
- **Limitations:** Data coverage and latency vary by country; license of underlying measurements can differ by provider.
- **Best fit:** Any smart-city AQ pipeline’s data layer—fetch and normalize observations before modeling.
- **VERDICT: essential** (as data infrastructure; models must be built on top)

### 1.3 `google-research/flood-forecasting`

- **URL:** https://github.com/google-research/flood-forecasting
- **Stars / language / license / activity:** Research repo from Google Research; Python; Apache-2.0; associated with Google flood-forecasting publications (Gauge+ML ensembles, nowcasting).
- **Maintainer:** Google Research (Hydro/Climate team lineage).
- **What it implements:** Machine-learning flood forecasting components—imputation of gauge series, sequence models for river discharge/nowcast, and integration patterns used in Google’s flood alerts (inference over global river networks).
- **Key modules:** Data preprocessing/imputation, model definitions (GRU/Transformer-style sequence models), evaluation on river gauges.
- **Datasets:** Global river gauge networks and related hydrological inputs (paired with Google’s public gauge data releases).
- **Quality signals:** Clean research code, Apache license, strong paper lineage; narrower than the full production alert system.
- **Limitations:** Not an end-to-end civic alerting platform; requires significant data engineering and local calibration.
- **Best fit:** Teams building regional flood nowcasts who want a reputable sequence-model baseline.
- **VERDICT: essential**

### 1.4 `garythung/trashnet` — Waste image classification

- **URL:** https://github.com/garythung/trashnet
- **Stars / language / license / activity:** Classic small dataset repo; Python (original Torch/Lua lineage); MIT; older but stable reference.
- **Maintainer:** Gary Thung & Mindy Yang (Stanford CS229 project lineage).
- **What it implements:** Convolutional network classification of waste images into 6 classes (glass, paper, cardboard, plastic, metal, trash); ~2,527 images; reported ~75% accuracy in original work.
- **Key modules:** Dataset images, simple CNN training scripts, evaluation.
- **Datasets:** TrashNet itself (the de-facto small public waste-classification benchmark).
- **Quality signals:** Widely cited, tiny and easy to reproduce; no modern MLOps, tests, or pretrained SOTA weights.
- **Limitations:** Small, class-imbalanced, low resolution; accuracy far below modern vision transformers; not industrial-waste-grade.
- **Best fit:** Teaching, smoke tests, and baselines for waste-sorting camera PoCs.
- **VERDICT: useful**

### 1.5 `arielyosua/Waste-Classification-Using-Convolutional-Neural` (WasteNet-adjacent)

- **URL:** https://github.com/arielyosua/Waste-Classification-Using-Convolutional-Neural
- **Stars / language / license / activity:** ≈ 2★; Python; minimal activity (student-scale project).
- **What it implements:** CNN-based waste classification (related to the WasteNet paper lineage: dual input—image + metadata / hybrid features for recycling).
- **Datasets:** TrashNet and/or related waste corpora.
- **Quality signals:** Very low—single-author notebook-style code, no CI.
- **Limitations:** Not official WasteNet code; weak docs and evaluation.
- **Best fit:** Only as a citation pointer; prefer training your own model on TrashNet or a larger modern waste dataset.
- **VERDICT: stale**

### 1.6 `CityMind-Lab/DeepUHI` — Deep Urban Heat Island modeling

- **URL:** https://github.com/CityMind-Lab/DeepUHI
- **Stars / language / license / activity:** Official code for KDD 2025 paper; Python/PyTorch; MIT; recent academic release (small commit count but current).
- **Maintainer:** CityMind Lab (corresponding authors of the DeepUHI paper).
- **What it implements:** Deep learning for urban heat island (UHI) intensity prediction—fusing land-use, building morphology, weather, and remote-sensing features to estimate intra-city heat patterns.
- **Key modules:** Feature pipelines for urban morphology, model training, evaluation; associated **SeoulTemp** dataset release.
- **Datasets:** SeoulTemp (and related urban climate inputs).
- **Quality signals:** Peer-reviewed (KDD 2025), official repo, MIT license, dataset published; limited engineering polish (research-grade scripts).
- **Limitations:** City-specific features; limited transferability without feature re-engineering; small community so far.
- **Best fit:** Heat-risk mapping and climate-adaptation planning research; a template for fusing GIS + weather + ML.
- **VERDICT: useful**

### 1.7 Water-quality ML (representative: `SayamAlt/Water-Quality-Prediction`, `Nelvinebi/Water-Quality-Index-Prediction-...`)

- **URLs:** https://github.com/SayamAlt/Water-Quality-Prediction ; https://github.com/Nelvinebi/Water-Quality-Index-Prediction-Using-ML-XGBoost-RF-LSTM-
- **Stars / language / license / activity:** Single-digit to ~16★; Python notebooks; MIT (some); mostly course/portfolio projects with sparse commits.
- **What it implements:** Tabular ML for potability classification or Water Quality Index (WQI) regression—LogReg/SVM/RF/XGBoost/LSTM over physicochemical features (pH, hardness, TDS, chlorides, turbidity…).
- **Datasets:** Common `water_potability.csv` (≈3,276 samples) or synthetic WQI series.
- **Quality signals:** Low—notebook-only, synthetic or small CSV, limited validation rigor; one has a Streamlit dashboard.
- **Limitations:** Not sensor-stream or network-scale; heavy class imbalance; poor external validity for municipal water systems.
- **Best fit:** Quick demos of WQI prediction; replace data with real utility feeds before any deployment.
- **VERDICT: niche**

---

## 2. Public Safety / Vision

This category covers crime/hotspot prediction, crowd counting, fall detection, epidemic modeling, and multi-object tracking—core public-safety analytics.

### 2.1 `Lakshigashree/Crime-Hotspot-Prediction`

- **URL:** https://github.com/Lakshigashree/Crime-Hotspot-Prediction
- **Stars / language / license / activity:** Very small (~3 commits observed); Python; license unclear/minimal; student-scale.
- **What it implements:** XGBoost-based crime hotspot classification with **SHAP** explainability over spatio-temporal features (time, location, historical counts, socio-economic covariates).
- **Key modules:** Feature engineering, XGBoost training, SHAP summary plots.
- **Datasets:** Open police incident data (city open-data portals).
- **Quality signals:** Uses a modern, explainable baseline (XGBoost+SHAP) but no tests, CI, or docs depth.
- **Limitations:** Small scale; ethical/fairness analysis incomplete (critical for predictive policing); not the CIKM DeepCrime architecture.
- **Verdict note:** Distinct from the academic DeepCrime (CIKM’18) paper, which has no widely maintained official GitHub release under that name (see 2.6).
- **Best fit:** Starting point for explainable hotspot PoCs with public incident CSVs.
- **VERDICT: niche**

### 2.2 `priyanka-kasture/Crowd-Counting-with-MCNNs`

- **URL:** https://github.com/priyanka-kasture/Crowd-Counting-with-MCNNs
- **Stars / language / license / activity:** ≈ 24★; Python; MIT; unofficial re-implementation.
- **What it implements:** Multi-column CNN (MCNN, Zhang et al., CVPR 2016) for density-map crowd counting on **ShanghaiTech** (Part A/B), UCF_CC_50, etc.
- **Key modules:** MCNN architecture, density-map generation from dots, train/eval.
- **Datasets:** ShanghaiTech (referenced; download scripts/links).
- **Quality signals:** Simple educational repo; not the authors’ official code; limited tracking of SOTA (CSRNet, CAN, transformers).
- **Limitations:** Older architecture; weak documentation; no pretrained weights guarantees.
- **Best fit:** Learning density-map crowd counting; for production events analytics, compare against CSRNet and newer counters.
- **VERDICT: useful**

### 2.3 `IKKIM00/fall-detection-and-predction-using-GRU-and-LSTM-with-Transfer-Learning` (SmartFall lineage)

- **URL:** https://github.com/IKKIM00/fall-detection-and-predction-using-GRU-and-LSTM-with-Transfer-Learning
- **Stars / language / license / activity:** ≈ 40★; Python; academic/student repo; moderate activity.
- **What it implements:** Wearable-sensor fall detection via GRU/LSTM with transfer learning on accelerometer/gyroscope streams; SmartFall / MobiAct-style datasets.
- **Key modules:** Signal windowing, sequence models, transfer-learning heads, evaluation (accuracy/F1, confusion matrix).
- **Datasets:** SmartFall, MobiAct (referenced).
- **Quality signals:** Reasonable README and metrics; not medical-device certified; limited edge-deployment code.
- **Limitations:** Dataset bias (synthetic falls, limited demographics); no tinyML export path in-repo.
- **Best fit:** Baseline for elderly-monitoring wearables; pair with `tflite-micro` for on-device inference (Category 5).
- **VERDICT: useful**

### 2.4 `cmillevoi/EpiPINN` — Physics-informed epidemic (SIR) learning

- **URL:** https://github.com/cmillevoi/EpiPINN
- **Stars / language / license / activity:** ≈ 6★; Python/PyTorch; arXiv 2311.09944; small academic repo.
- **What it implements:** Physics-informed neural networks (PINNs) for compartmental **SIR/SEIR** epidemic dynamics—embedding ODE residuals into the loss to forecast infection curves with sparse observations.
- **Key modules:** ODE residual losses, training on case time series, parameter inference (β, γ).
- **Datasets:** Public COVID/influenza case curves.
- **Quality signals:** Peer-reviewed preprint, compact code; limited multi-city scale and uncertainty quantification.
- **Limitations:** PINNs can struggle with sharp waves; not agent-based; few baselines vs. classical fits.
- **Best fit:** Hybrid mechanistic–ML outbreak modeling for city health departments’ early-warning prototypes.
- **VERDICT: niche**

### 2.5 `shaoshengsong/DeepSORT` + `nwojke/deep_sort` — Multi-object tracking

- **URLs:** https://github.com/shaoshengsong/DeepSORT ; https://github.com/nwojke/deep_sort
- **Stars / language / license / activity:** `shaoshengsong/DeepSORT` ≈ 1,008★ (C++17/Qt/ONNX, pluggable **ByteTrack / OC-SORT / DeepSORT**); `nwojke/deep_sort` original Python (GPL-3.0, ~38 commits, older).
- **Maintainers:** Community C++ port vs. original Deep SORT authors’ repo.
- **What it implements:** Online multi-object tracking: detection association with motion (Kalman) + appearance (ReID) features; Hungarian/greedy matching; configurable trackers for video analytics (surveillance, traffic cameras).
- **Key modules:** Tracker state, ReID feature extraction (ONNX in the C++ port), association costs, visualization.
- **Datasets:** MOTChallenge-style sequences (person/vehicle detection outputs).
- **Quality signals:** C++ port has active commits, ONNX runtime integration, CI-ish structure; original `nwojke/deep_sort` is reference but dated.
- **Limitations:** Depends on upstream detectors (YOLO etc.); ReID privacy concerns for municipal video.
- **Best fit:** Real-time CCTV/traffic-camera tracking pipelines; start from the C++/ONNX port for performance.
- **VERDICT: essential** (C++ port) / **useful** (original repo as reference)

### 2.6 DeepCrime (CIKM 2018) — note on code availability

- **Paper:** Huang et al., “DeepCrime: Attentive Hierarchical Recurrent Networks for Crime Prediction,” CIKM 2018.
- **Code status (research finding):** No widely adopted **official** public GitHub for the crime-prediction DeepCrime was confirmed; `dlfaults/deepcrime` is an unrelated **mutation-testing** tool (≈14★) and must not be confused with it. Follow-on works (ST-HSL, ST-SHHOL, ST-SHN) do publish code (e.g., `LZH-YS1998/STHSL`, `akaxlh/ST-SHN`).
- **Best fit:** Cite DeepCrime; implement via successor repos or re-implement hierarchical GRU+attention over crime tensors.
- **VERDICT (code): stale / non-existent under that name** — treat the paper as essential, the named repo as absent.

---

## 3. Urban Vision

License-plate recognition, smart parking, geospatial segmentation, and remote-sensing vision-language models.

### 3.1 `szad670401/HyperLPR` — Chinese license-plate recognition

- **URL:** https://github.com/szad670401/HyperLPR
- **Stars / language / license / activity:** ≈ 6,271★; multi-language (Java/Python/C++/Kotlin/JS ports); Apache-2.0; long-lived, actively maintained.
- **Maintainer:** HyperLPR community (originally from Chinese plate-recognition ecosystem).
- **What it implements:** Real-time vehicle license-plate detection + recognition optimized for **Chinese plates** (blue/green/new-energy), with lightweight CNN/anchors and multi-platform SDKs.
- **Key modules:** Plate detection, character recognition, multi-language bindings, Android/iOS/desktop examples.
- **Datasets:** Internal Chinese plate corpora (not fully open).
- **Quality signals:** High stars, many bindings, production usage in China; limited English docs.
- **Limitations:** Plate formats region-specific (poor for EU/US plates out of the box); training data closed.
- **Best fit:** tolling/parking gates in Chinese-plate jurisdictions; for other regions use OpenALPR-class tools or train custom models.
- **VERDICT: essential** (CN context) / **useful** (elsewhere)

### 3.2 `openalpr/openalpr` — Automatic license plate recognition

- **URL:** https://github.com/openalpr/openalpr
- **Stars / language / license / activity:** Historic high-adoption ALPR; C++ core with bindings; **AGPL-3.0** (commercial licenses available via company); large commit history (≈1,387 commits observed).
- **Maintainer:** OpenALPR (commercial open-source model).
- **What it implements:** End-to-end ALPR: plate detection, character segmentation/recognition, configurable country templates (US/EU), video and still-image pipelines; cloud & on-prem options historically.
- **Datasets:** Proprietary training sets; evaluation on public plate benchmarks referenced.
- **Quality signals:** Mature C++, Docker/docs, but AGPL copyleft and shifting corporate stewardship create adoption friction.
- **Limitations:** AGPL for many smart-city procurements; model accuracy lags modern YOLO+CRNN stacks; maintenance cadence uneven vs. HyperLPR.
- **Best fit:** Teams that can accept AGPL or buy commercial license; otherwise prefer HyperLPR or self-hosted modern ALPR.
- **VERDICT: useful** (license-constrained)

### 3.3 `your-ai-solution/object-detection-parking-spot` — YOLO smart parking

- **URL:** https://github.com/your-ai-solution/object-detection-parking-spot
- **Stars / language / license / activity:** ≈ 3 commits observed; Python; Apache-2.0; early PoC.
- **What it implements:** YOLOv8-based parking-space detection/occupancy estimation from camera feeds (bounding boxes on parking bays → free/occupied).
- **Key modules:** YOLO inference, bay annotation/mapping, occupancy overlay.
- **Datasets:** Custom parking images (small).
- **Quality signals:** Minimal—no CI, thin README; uses a modern detector family though.
- **Limitations:** Not a full parking-management system (no payments, reservations, edge fleet mgmt).
- **Best fit:** Prototype occupancy counting for lot cameras; productionize with larger annotated bay datasets.
- **VERDICT: niche**

### 3.4 `segment-geospatial` (SAMgeo) — Geospatial segmentation with SAM/SAM2/SAM3

- **URL:** https://github.com/opengeos/segment-geospatial (docs: samgeo.gishub.org)
- **Stars / language / license / activity:** High-growth geospatial AI repo from the GIS community; Python; MIT; actively maintained with frequent releases.
- **Maintainer:** OpenGeo / Xiaochuan Tong (opengeos ecosystem).
- **What it implements:** Wraps Meta’s **Segment Anything** (and successors) for geospatial rasters—automatic building/road/water/land-cover mask generation, text-prompted (`SamGeo` text prompts), tiling for large GeoTIFFs, vector export to GeoPackage.
- **Key modules:** Raster tiling, SAM inference wrappers, interactive vs. automatic modes, GIS I/O (GDAL/rasterio).
- **Datasets:** Works on any aerial/satellite imagery; example notebooks with public imagery.
- **Quality signals:** Excellent docs/notebooks, PyPI packaging, active issues; heavy GPU requirements for large areas.
- **Limitations:** Foundation-model masks still need QA for cadastral/official mapping; license of underlying SAM weights (Apache-2.0) is fine but attribution required.
- **Best fit:** Rapid building-footprint and land-cover extraction for digital-twin basemaps.
- **VERDICT: essential**

### 3.5 `ChenDelong1999/RemoteCLIP` — Remote-sensing vision-language model

- **URL:** https://github.com/ChenDelong1999/RemoteCLIP
- **Stars / language / license / activity:** Official repo of IEEE TGRS 2024 paper; Python (OpenCLIP-based); Apache-2.0; checkpoints on Hugging Face (`gzqy1026/RemoteCLIP`); active since 2023 with dataset release 2024.
- **Maintainer:** Fan Liu, Delong Chen et al. (Zhejiang/Griffith collaboration lineage).
- **What it implements:** First vision-language foundation model specialized for **remote sensing**—CLIP continual pretraining on scaled image-text pairs (B2C box-to-caption, M2B mask-to-box conversions + UAV imagery, 12× data scaling); supports zero-shot classification, retrieval, few-shot, object counting (RemoteCount benchmark).
- **Key modules:** Model loading via OpenCLIP, retrieval eval scripts, integration with Autodistill (`autodistill-remote-clip`).
- **Datasets:** RET-3, SEG-4, DET-10 training corpus (HF); RSITMD/RSICD/UCM retrieval; 16 downstream sets.
- **Quality signals:** Peer-reviewed (TGRS), weights released, Apache-2.0, third-party integrations (Roboflow Autodistill).
- **Limitations:** Remote-sensing-specific prompts; not a full change-detection pipeline; compute cost for large tiles.
- **Best fit:** Semantic search / zero-label triage of satellite archives for flood, urban sprawl, and land-use monitoring—pairs with SAMgeo for masks.
- **VERDICT: essential**

---

## 4. LLM / Foundation Models for Cities

City-scale instruction tuning, spatio-temporal LLMs, planning agents, and traffic-foundation-model orchestration.

### 4.1 `tsinghua-fib-lab/CityGPT` — Urban spatial cognition LLM framework

- **URL:** https://github.com/tsinghua-fib-lab/CityGPT
- **Stars / language / license / activity:** KDD 2025 Research Track; Python; MIT; modest commit count (research release) but current (2024–2025).
- **Maintainer:** Tsinghua FIB Lab (Jie Feng, Yong Li et al.).
- **What it implements:** Systematic framework to inject a city-scale “world model” into LLMs: **CityInstruction** dataset (CityQA, CityWalk, CityReasoning), **SWFT** self-weighted fine-tuning over ChatGLM3-6B / Llama3-8B / Qwen2.5-7B, and **CityEval** text-based spatial benchmark; includes `citysim`/`citymap`/`simulate` submodules and LLaMA-Factory integration.
- **Key modules:** `train/`, `evaluate/` (OpenCompass scripts), `citysim/`, `simulate/`, `serving/`, `LLAMA-Factory/`.
- **Datasets:** CityInstruction + CityEval for 4 cities (Hugging Face: CityGPT-Data); extensible to new cities via `task_gen`.
- **Quality signals:** Top-tier venue, MIT, modular repo, companion **UrbanLLaVA** (ICCV 2025); still research-grade ops (submodules, scripts vs. library API).
- **Limitations:** Chinese-city-centric data; eval mostly text (vision via UrbanLLaVA); fine-tuning cost non-trivial.
- **Best fit:** Building urban-reasoning assistants (planning Q&A, spatial QA) with reproducible benchmarks.
- **VERDICT: essential**

### 4.2 `tsinghua-fib-lab/UrbanLLaVA` — Multi-modal urban intelligence

- **URL:** https://github.com/tsinghua-fib-lab/UrbanLLaVA
- **Stars / language / license / activity:** ≈ 80★; ICCV 2025; Python; MIT; successor to CityGPT with multi-modal spatial reasoning.
- **What it implements:** Multi-modal LLM for urban scenes—aligning satellite/street imagery with language for spatial reasoning and understanding tasks beyond text-only CityGPT.
- **Quality signals:** ICCV acceptance, same lab lineage, MIT.
- **Limitations:** Newer, smaller community; heavy vision-language fine-tuning requirements.
- **Best fit:** City digital-twin copilots that must “see” maps/aerial photos and answer in language.
- **VERDICT: useful**

### 4.3 `HKUDS/UrbanGPT` — Spatio-temporal large language model

- **URL:** https://github.com/HKUDS/UrbanGPT
- **Stars / language / license / activity:** ≈ 460★; Python/PyTorch; Apache-2.0; KDD 2024; 38 commits; weights/checkpoints referenced (`st_encoder`).
- **Maintainer:** HKU Data Intelligence Lab (Chao Huang et al.) + collaborators (SCUT, Baidu).
- **What it implements:** Spatio-temporal dependency encoder (multi-level TCN) + instruction-tuning paradigm aligning time-space signals with LLM knowledge for zero/few-shot urban prediction (taxi flow, crime, bike demand).
- **Key modules:** `urbangpt/`, `instruction_generate/`, `checkpoints/st_encoder/`, train/eval scripts, `tests/`.
- **Datasets:** NYC taxi/bike/crime spatio-temporal series (pretrain + downstream public sets).
- **Quality signals:** KDD paper, Apache-2.0, released encoder weights, some tests; still script-oriented.
- **Limitations:** Prediction-as-text generation can underperform dedicated ST-GNNs on pure forecasting metrics; data-scarcity claims need careful baselining.
- **Best fit:** Unified zero-shot spatio-temporal question answering and multi-task urban forecasting under label scarcity.
- **VERDICT: essential**

### 4.4 `lijlansg/TrafficGPT` — LLM × traffic foundation models

- **URL:** https://github.com/lijlansg/TrafficGPT
- **Stars / language / license / activity:** Demo repo for Transport Policy 2024 paper (Zhang, Fu, Liang, Zhang, Yu, Cai, Yao); Python; research release; cite via arXiv 2309.06719.
- **What it implements:** Orchestration framework fusing LLMs with **Traffic Foundation Models (TFMs)**—prompt layers let the LLM view/analyze traffic data, decompose tasks, invoke TFMs sequentially, and iterate with human feedback for management decisions.
- **Key modules:** Prompt/task-decomposition pipeline, TFM tool adapters (data access, simulation, control), interactive feedback loop.
- **Datasets/TFMs:** Plugs into traffic datasets and foundation models (varies by demo config).
- **Quality signals:** Peer-reviewed, clear system paper; repo more demo than library; depends on external API/TFM availability.
- **Limitations:** Not autonomous closed-loop control by itself; prompt reliability and TFM licensing vary.
- **Best fit:** NL interfaces for traffic ops centers—“show congestion hotspots for 8–10am, then simulate a signal-plan tweak.”
- **VERDICT: useful**
- **Caution:** `YasodGinige/TrafficGPT` is a **different** project (encrypted network-traffic classification) and must not be cited as urban TrafficGPT.

### 4.5 PlanGPT (paper; GitHub status)

- **Paper:** arXiv 2402.19273 (ACL Industry 2025 lineage: PlanGPT; EMNLP 2025: PlanGPT-VL).
- **Code status (research finding):** Official implementation was not confirmed as a widely published public GitHub in these searches; the work describes PlanAgent, Vector-LLM/PlanRAG, local fine-tuned LLM, and tool-LLM for urban planning regulation workflows (with Chinese Academy of Urban Planning collaboration).
- **VERDICT: useful as paper/system design; code availability niche/uncertain** — monitor author pages before adoption.

---

## 5. Federated / Edge / TinyML

Cross-silo/cross-device learning for privacy-sensitive city data, plus MCU deployment for always-on sensing.

### 5.1 `adap/flower` (Flower / flower-labs lineage) — Federated learning framework

- **URL:** https://github.com/adap/flower (Flower Labs ecosystem; PyPI `flwr`)
- **Stars / language / license / activity:** ≈ 6,922★ observed in org listings; Python; Apache-2.0; very large commit history (≈5,131 commits); continuous releases.
- **Maintainer:** Flower Labs / academia–industry consortium.
- **What it implements:** Framework-agnostic federated learning: client/server APIs, strategies (FedAvg, FedProx, FedOpt, etc.), simulation engine, production deployments (edge devices, phones, cloud), and **Flower Datasets**.
- **Key modules:** `flwr` client/server, strategies, simulation, ray-based scale-out, docs site.
- **Datasets:** Flower Datasets library + user data (hospital, telco, city IoT examples in docs).
- **Quality signals:** Top OSS quality (docs, tests, CI, examples, papers Flower I/II); Apache-2.0; broad ecosystem.
- **Limitations:** FL non-IID pitfalls; security (poisoning) out of the box is limited; ops complexity for true cross-silo city deployments.
- **Best fit:** Default choice for privacy-preserving model training across utilities, hospitals, and agencies.
- **VERDICT: essential**

### 5.2 `FedML-AI/FedML` — Unified distributed + federated ML

- **URL:** https://github.com/FedML-AI/FedML
- **Stars / language / license / activity:** ≈ 4.1k★; Python; Apache-2.0; ≈12,120 commits; active (TensorOpera branding).
- **Maintainer:** FedML Inc. (Chaoyang He, Salman Avestimehr et al. academic roots).
- **What it implements:** Research library + MLOps: cross-silo (**Octopus**), cross-device (**Beehive**), simulation (**Parrot**), browser FL (**Spider**); communication backends (MPI, gRPC, PyTorch RPC, MQTT+S3); differential privacy; FedLLM experiments; Android/iOS folders.
- **Quality signals:** Huge commit count, examples/, research/ folders, Apache-2.0; commercial TensorOpera platform alongside.
- **Limitations:** Broad surface area can overwhelm newcomers; some paths tuned to their cloud product; OpenSSF scorecard mixed (token permissions).
- **Best fit:** Teams needing FL + distributed training + mobile clients in one stack; pair with Flower when you want minimal FL-only API.
- **VERDICT: essential**

### 5.3 `OpenFederatedLearning/openfl` — Intel OpenFL

- **URL:** https://github.com/OpenFederatedLearning/openfl (historically `intel/openfl`)
- **Stars / language / license / activity:** Python; Apache-2.0; ≈250+ commits on the org mirror (upstream lineage longer); docs on Read the Docs; aggregator & workflow APIs.
- **Maintainer:** Intel Labs → LF AI & Data / Open Federated Learning community.
- **What it implements:** Production-oriented FL for collaborative training without sharing raw data—**Aggregator-based** and **Workflow** APIs; TF/PyTorch/NumPy backends; FedAvg, FedOpt, FedProx, FedCurv; originally healthcare (medical imaging) but industry-agnostic.
- **Datasets:** User-supplied silo data (examples in tutorials/notebooks).
- **Quality signals:** Peer-reviewed (Phys. Med. Biol.), security policy, tests/, tutorials; stable enterprise pedigree.
- **Limitations:** Smaller community than Flower; some star counts on mirrors can be misleading—verify upstream org; fewer cutting-edge strategies.
- **Best fit:** Regulated cross-silo deployments (health, finance, municipal records) wanting Intel-grade process docs.
- **VERDICT: useful**

### 5.4 `google-parfait/tensorflow-federated` (TFF)

- **URL:** https://github.com/google-parfait/tensorflow-federated (canonical TensorFlow Federated)
- **Stars / language / license / activity:** ≈ 2.5k★; Python; Apache-2.0; active releases (0.8x series); heavy research pedigree.
- **Maintainer:** Google (TensorFlow Federated team).
- **What it implements:** Two-layer API: **FL API** (`tff.learning` algorithms incl. FedAvg/AdamW optimizers, DP noise calibration) and **Federated Core** for declarative federated computations; single/multi-machine simulation; federated analytics primitives.
- **Datasets:** EMNIST and simulation datasets built-in; custom `ClientData`.
- **Quality signals:** Official Google project, tutorials on tensorflow.org, extensive type system; OpenSSF scorecard mixed (some token/permission findings).
- **Limitations:** TF-centric (JAX interop evolving); steep learning curve for FC API; production multi-host stories less turnkey than Flower/FedML.
- **Best fit:** Research on new FL algorithms and typed federated computations; education on FL fundamentals.
- **VERDICT: useful**

### 5.5 `mit-han-lab/mcunet` — TinyML system design (MCUNet / MCUNetV2)

- **URL:** https://github.com/mit-han-lab/mcunet
- **Stars / language / license / activity:** ≈ 718★; Python + C (inference); MIT; NeurIPS 2020/2021 papers; CI via `.github/workflows`.
- **Maintainer:** MIT HAN Lab (Song Han group).
- **What it implements:** Co-design of efficient neural architectures + inference engine for **microcontrollers** (48–320KB flash): MCUNet (tiny NAS + TFLM-based engine) and MCUNetV2 (patch-based inference reducing peak memory).
- **Datasets:** ImageNet-subset / CIFAR-style benchmarks for edge accuracy–latency tradeoffs.
- **Quality signals:** Top-venue papers, MIT, CI, widely cited; model zoo for MCU-scale nets.
- **Limitations:** Not a full city IoT stack; older than current TinyML NAS; tied to TFLM-era tooling.
- **Best fit:** Designing always-on environmental/safety classifiers that must run on battery MCUs.
- **VERDICT: essential** (edge design methodology)

### 5.6 `tensorflow/tflite-micro` — TensorFlow Lite for Microcontrollers

- **URL:** https://github.com/tensorflow/tflite-micro
- **Stars / language / license / activity:** High-traffic Google repo; C++ (+ Python tools); Apache-2.0; ≈2,154 commits; rolling `0.dev` PyPI builds (pin SHAs—no semver tags); CI for Linux/Windows/Cortex-M/Xtensa/RISC-V/Hexagon.
- **Maintainer:** Google (LiteRT/TFLM team).
- **What it implements:** Inference runtime for deep models on bare-metal MCUs/DSPs with tens–hundreds of KB RAM: memory planning, optimized kernels (CMSIS-NN etc.), micro interpreter, model compression tooling, QEMU/Renode emulation.
- **Datasets/models:** Any `.tflite` model; hello_world and example zoo in-repo; community ports (Arduino, ESP32, Renesas…).
- **Quality signals:** Excellent CI matrix, docs (memory, error handling, porting), MLSys 2021 paper; canonical TinyML framework.
- **Limitations:** Rolling releases require SHA pinning; no built-in training on device; operator coverage subset of full TF.
- **Best fit:** Deploying fall-detection / acoustic / air-quality models on municipal sensor nodes and wearables.
- **VERDICT: essential**

---

## 6. City Simulators & Datasets

Traffic microsimulation, RL traffic control, building/energy loops, agent-based modeling, map graph tooling, and large AV/trajectory datasets.

### 6.1 `cityflow-project/CityFlow` — City-scale traffic microsimulation

- **URL:** https://github.com/cityflow-project/CityFlow
- **Stars / language / license / activity:** Apache-2.0; ≈75 commits observed on mainline; C++ core + Python API; research origin (HKUST) with continued academic use.
- **What it implements:** High-performance city-scale traffic simulator—road networks, traffic lights, vehicles; JSON roadnet/flow configs; RL environment wrapper; claims faster-than-SUMO execution for large networks.
- **Key modules:** Engine, Python `cityflow` bindings, example networks (e.g., Hangzhou-scale), RL env APIs.
- **Datasets:** Built-in example roadnets/flows; interoperable with real-world network exports.
- **Quality signals:** Cited traffic-RL literature, Apache-2.0; smaller contributor base than SUMO; docs thinner than SUMO’s.
- **Limitations:** Fewer traffic-signal plans/edge cases than SUMO; visualization tooling lighter.
- **Best fit:** RL traffic-signal control at city scale when SUMO performance becomes the bottleneck.
- **VERDICT: essential**

### 6.2 `citylearn-project/CityLearn` — Building energy demand-response env

- **URL:** https://github.com/CityLearn/CityLearn (citylearn-project lineage)
- **Stars / language / license / activity:** MIT; ≈1,372 commits; Python; active releases; OpenAI Gym-style API; extensive `tests/`, `docs/`.
- **What it implements:** Multi-building energy management environment—battery/heat-pump/HVAC control, carbon-aware and cost-aware demand response, RL baselines, and standard CityLearn datasets (district-scale building models).
- **Key modules:** Environment, agents (rule-based + RL), datasets (reference buildings), evaluation metrics.
- **Datasets:** CityLearn v1/v2 district datasets (building thermal models, loads, prices, weather).
- **Quality signals:** Peer-reviewed (CityLearn challenge lineage), tests, docs, MIT, stable API—best-in-class among city RL envs here.
- **Limitations:** Buildings-focused (not traffic); domain randomization depth varies by dataset version.
- **Best fit:** Grid-interactive building fleets and campus microgrids in smart-city energy programs.
- **VERDICT: essential**

### 6.3 `eclipse-sumo/sumo` — Simulation of Urban MObility

- **URL:** https://github.com/eclipse-sumo/sumo
- **Stars / language / license / activity:** One of the most starred traffic sims; C++/Python; **EPL-2.0**; enormous commit history; continuous releases; Windows/Linux/macOS.
- **Maintainer:** Eclipse SUMO community (German aerospace/transport research lineage).
- **What it implements:** Microscopic multi-modal traffic simulation—vehicles, pedestrians, public transport; TraCI remote control; route planning; co-simulation hooks (with CARLA, Flow); traffic demand generation (duarouter, od2trips).
- **Datasets:** OSM network imports; standard test networks; integrates with external demand data.
- **Quality signals:** Elite OSS practices (docs, CI, releases, community); EPL-2.0 is business-friendly with obligations.
- **Limitations:** Learning curve; GUI performance on huge nets; pure-Python SUMO variants (TraCI) can be slow without libsumo.
- **Best fit:** Default city traffic digital twin—signal timing, transit, emissions scenarios.
- **VERDICT: essential**

### 6.4 `flow-project/flow` — RL for traffic control (SUMO/RLlib)

- **URL:** https://github.com/flow-project/flow
- **Stars / language / license / activity:** MIT; ≈3,718 commits; Python; docs/coverage badges; Berkeley Mobile Sensing Lab + AWS research support; activity slower in recent years but still referenced.
- **What it implements:** Computational framework for deep RL and control in traffic microsimulation—mixed-autonomy scenarios (ramp metering, signal control, AV platoons) on top of **SUMO** + **RLlib/Ray**; benchmark suite for RL traffic papers.
- **Key modules:** Scenario definitions, RLlib env wrappers, benchmarks, tutorials, Docker.
- **Datasets/networks:** Built-in ring/merge/grid networks; imports from SUMO.
- **Quality signals:** Seminal CoRL/ITSC papers, tests, tutorials; aging dependency pins (old RLlib/SUMO versions can bit-rot).
- **Limitations:** Maintenance cadence modest vs. CityFlow/CityLearn; upgrade friction for modern Ray.
- **Best fit:** Reproducing mixed-autonomy RL benchmarks; new projects may prefer CityFlow for speed or wrap SUMO directly.
- **VERDICT: useful** (slightly stale on deps)

### 6.5 `carla-simulator/carla` — Open urban driving simulator

- **URL:** https://github.com/carla-simulator/carla
- **Stars / language / license / activity:** ≈ 15k★ (≈14.5k star-history); C++/Python (Unreal Engine); MIT for CARLA code (assets CC-BY; UE5 separate); ≈7,200 commits; active (ue58-dev default branch, updated 2026).
- **Maintainer:** CVC Barcelona / CARLA org (Intel Labs lineage).
- **What it implements:** 3D urban driving simulator—sensors (camera, LiDAR, radar), Traffic Manager, ScenarioRunner/OpenDRIVE maps, ROS bridge, leaderboard, co-simulation with SUMO; training stacks for imitation/RL AV agents.
- **Key modules:** `PythonAPI`, `LibCarla`, `Unreal/`, scenario tools, leaderboard repos in org.
- **Datasets:** Synthetic (procedural maps + assets); bridges to real AV datasets (nuScenes/Waymo) for transfer studies.
- **Quality signals:** Massive community, CoRL’17 paper, extensive docs, MIT code; heavy GPU/engine builds.
- **Limitations:** Unreal build complexity; not a city-scale traffic solver (pair with SUMO); asset licenses need care.
- **Best fit:** AV perception/planning sims and synthetic data generation for urban vision models.
- **VERDICT: essential**

### 6.6 `mesa/mesa` (+ `mesa-geo`) — Agent-based modeling for cities

- **URL:** https://github.com/mesa/mesa ; https://github.com/mesa/mesa-geo
- **Stars / language / license / activity:** ≈ 3.9k★ (PyPI-verified ≈3,878); Python; Apache-2.0; ≈3,258 commits; active (Mesa 3.5.x stable, Mesa 4 pre-releases); `mesa-geo` ≈ 238★; JOSS 2025 paper.
- **Maintainer:** Project Mesa community (international).
- **What it implements:** Python ABM framework—agents, schedulers, grids, data collection, browser viz; **mesa-geo** adds GIS layers (raster/vector) for urban growth, GeoSIR epidemics, population models; **mesa-llm** (≈81★) plugs LLMs into agents.
- **Datasets:** Example library (Schelling, forest fire, urban growth, GeoSIR); user-supplied GIS.
- **Quality signals:** Excellent docs, tests, CI, citation DOI, active GSoC—mature scientific software.
- **Limitations:** Not a traffic microsim; performance needs mesa-frames for very large populations; LLM extension still young.
- **Best fit:** Policy ABMs—land use, evacuation, disease, retail adoption—before wiring ML surrogates.
- **VERDICT: essential**

### 6.7 `gboeing/osmnx` — OpenStreetMap network graphs

- **URL:** https://github.com/gboeing/osmnx
- **Stars / language / license / activity:** ≈ 5.8k★; Python; MIT; ≈4,653 commits; maintained (2.1.1 release 2026); tests/, docs, pre-commit, PyPI/conda.
- **Maintainer:** Geoff Boeing + contributors.
- **What it implements:** One-line download/model/analyze/visualize of street networks and amenities from OSM—walking/driving/biking graphs as NetworkX, routing, street orientation, elevation, building footprints, transit stops; geopandas interop.
- **Quality signals:** Textbook-grade docs (Geographical Analysis 2025 paper), CI, examples gallery; production-stable.
- **Limitations:** Depends on Overpass API rate limits; OSM completeness varies by city; not an ML model.
- **Best fit:** Foundational graph layer for any urban mobility ML (GNN traffic, accessibility, logistics).
- **VERDICT: essential**

### 6.8 `nutonomy/nuscenes-devkit` — nuScenes AV dataset toolkit

- **URL:** https://github.com/nutonomy/nuscenes-devkit
- **Stars / language / license / activity:** ≈ 2.8k★ (≈713 forks); Python; permissive-ish (MIT for devkit code; **dataset** free for non-commercial, commercial by agreement); active (org updated 2026; pip `nuscenes-devkit` 1.2.0).
- **Maintainer:** Motional (nuTonomy).
- **What it implements:** Official devkit for nuScenes/nuImages—scene browsing, 3D boxes, lidarseg, panoptic, map expansion, detection/tracking/prediction **evaluation metrics**, tutorials (Colab).
- **Datasets:** nuScenes (1,000 scenes, 6 cameras + lidar + radar), nuImages, map expansion.
- **Quality signals:** Canonical AV benchmark, tutorials, releases, AWS open-data hosting; OpenSSF scorecard mid (token permissions noted).
- **Limitations:** Dataset license not fully open for commercial; TF-era packaging quirks; large downloads.
- **Best fit:** Training/evaluating urban perception (detection, tracking, prediction) with a standard benchmark.
- **VERDICT: essential**

### 6.9 `waymo-research/waymo-open-dataset` — Waymo Open Dataset

- **URL:** https://github.com/waymo-research/waymo-open-dataset
- **Stars / language / license / activity:** Apache-2.0 for most code (some `wdl_limited` BSD+patent; **dataset** non-commercial terms); Python/C++ (Bazel); ≈149 commits (release-oriented); updated through 2025 (motion v1.3.1, sdc_paths).
- **Maintainer:** Waymo (Alphabet).
- **What it implements:** Format + evaluation code for Perception (2,030 segments), Motion (103k+ scenes), and End-to-End Driving datasets—metrics in C++, TF helpers, tutorials.
- **Datasets:** Waymo Open Perception/Motion/E2E (high-res lidar/camera, trajectories, maps).
- **Quality signals:** State-of-the-art scale/quality; challenge ecosystem; heavy install (Bazel, TF versions).
- **Limitations:** Non-commercial dataset license blocks product use; large infra; some metrics code patents constrained.
- **Best fit:** Research-grade AV and urban-motion benchmarks (complement to nuScenes).
- **VERDICT: essential** (research) / **niche** (commercial prod—license)

### 6.10 `liuxu77/LargeST` — Large-scale traffic dataset (NeurIPS 2023)

- **URL:** https://github.com/liuxu77/LargeST
- **Stars / language / license / activity:** NeurIPS 2023 D&B; Python; MIT; dataset-focused release (2023) with benchmark code.
- **What it implements:** **8,600 sensors**, California-scale highway traffic dataset (largest widely used graph traffic set at release) + baselines for spatio-temporal forecasting.
- **Datasets:** LargeST (CA highways, 5-min resolution).
- **Quality signals:** Top venue, MIT, standard for scaling ST-GNN research; storage-heavy.
- **Limitations:** US-highway bias; download size; less multimodal than city transit sets.
- **Best fit:** Stress-testing traffic foundation models and GNN scalability.
- **VERDICT: essential**

### 6.11 METR-LA / PEMS-BAY via `liyaguang/DCRNN` (+ mirrors)

- **URL:** https://github.com/liyaguang/DCRNN (canonical data home); mirrors e.g. `hazdzz/dcrnn_data`, HF `witgaw/METR-LA`.
- **Stars / language / license / activity:** DCRNN (ICLR 2018) repo; Python; data widely mirrored; low commit activity on data-only mirrors (e.g., 4 commits) but datasets remain standard.
- **What it implements:** Diffusion-Convolutional RNN paper code + **METR-LA** (207 LA sensors, Mar–Jun 2012) and **PEMS-BAY** (325 Bay Area sensors, 2017) at 5-minute intervals; adjacency/distance matrices included.
- **Datasets:** METR-LA, PEMS-BAY (also PEMS-D3/4/7/8 via related repos—see LibCity raw-data index).
- **Quality signals:** Benchmark status in dozens of ST-GNN papers; simple CSV/npz layouts; mirrors ease hosting.
- **Limitations:** Aging code vs. modern frameworks; single-city highway speed/flow only.
- **Best fit:** Default sanity benchmarks for any urban forecasting model before LargeST.
- **VERDICT: essential**

### 6.12 Additional dataset/tooling pointers (brief)

- **`CommonRoad/commonroad-carla-interface`** — GPL-3.0, ≈409 commits, tests/CI/pre-commit: bridges CommonRoad scenarios ↔ CARLA for motion planning research. **VERDICT: useful** (planning benchmarks).
- **NYC taxi/bike trip data** — via TLC/BikeNYC open portals (referenced in dataset indexes rather than a single “official GitHub”); used heavily by UrbanGPT/CityGPT-style instruction sets. **VERDICT: essential** (data), tooling scattered.
- **NS-3 / OMNeT++** — network simulators often cited with urban IoT; not deep-dived here (no confirmed dedicated smart-city ML GitHub under a single canonical repo in these searches). **VERDICT: niche** for ML-focused readers.

---

## 7. Cross-cutting observations

1. **Layered stacks win.** Production smart-city ML is almost never one repo: OSMnx (graph) → SUMO/CityFlow/CARLA (sim) → Flower/FedML (privacy) → tflite-micro/MCUNet (edge) → CityGPT/UrbanGPT (language layer).
2. **Licensing is a procurement filter.** AGPL (OpenALPR), non-commercial dataset terms (Waymo, nuScenes), and EPL (SUMO) matter as much as accuracy for municipal buyers.
3. **Research ≠ product.** KDD/ICCV releases (CityGPT, DeepUHI, UrbanGPT) are excellent method sources but need data pipelines, monitoring, and fairness review before touching live services.
4. **Explainability is mandatory in safety domains.** XGBoost+SHAP crime code and PINN residuals are patterns to keep; black-box hotspot maps create legal and ethical exposure.
5. **Watch for name collisions.** DeepCrime (crime vs. mutation testing), TrafficGPT (urban vs. encrypted traffic), and OpenFL mirrors vs. upstream orgs are common citation errors.

---

## 8. Final summary table

| Repo | Stars (≈) | Language | Category | Verdict |
|------|-----------|----------|----------|---------|
| iipr/air-quality | <10 | Python | Environment | niche |
| openaq/openaq-python | 22 | Python | Environment | essential |
| openaq/awesome-air-quality | 71 | Markdown | Environment | useful |
| google-research/flood-forecasting | research | Python | Environment | essential |
| garythung/trashnet | research | Python | Environment | useful |
| arielyosua/Waste-Classification-CNN | 2 | Python | Environment | stale |
| CityMind-Lab/DeepUHI | research | Python | Environment | useful |
| SayamAlt/Water-Quality-Prediction | 8 | Python | Environment | niche |
| Nelvinebi/WQI-XGBoost-RF-LSTM | 16 | Python | Environment | niche |
| Lakshigashree/Crime-Hotspot-Prediction | ~3 commits | Python | Public Safety | niche |
| priyanka-kasture/Crowd-Counting-MCNNs | 24 | Python | Public Safety | useful |
| IKKIM00/SmartFall-GRU-LSTM | 40 | Python | Public Safety | useful |
| cmillevoi/EpiPINN | 6 | Python | Public Safety | niche |
| shaoshengsong/DeepSORT | 1,008 | C++ | Public Safety | essential |
| nwojke/deep_sort | research | Python | Public Safety | useful |
| DeepCrime (CIKM’18) official code | n/a | — | Public Safety | stale/absent |
| szad670401/HyperLPR | 6,271 | Multi | Urban Vision | essential (CN) |
| openalpr/openalpr | high (hist.) | C++ | Urban Vision | useful (AGPL) |
| your-ai-solution/parking-spot-YOLO | ~3 commits | Python | Urban Vision | niche |
| opengeos/segment-geospatial (SAMgeo) | high | Python | Urban Vision | essential |
| ChenDelong1999/RemoteCLIP | research | Python | Urban Vision | essential |
| tsinghua-fib-lab/CityGPT | research | Python | LLM/City | essential |
| tsinghua-fib-lab/UrbanLLaVA | ~80 | Python | LLM/City | useful |
| HKUDS/UrbanGPT | 460 | Python | LLM/City | essential |
| lijlansg/TrafficGPT | research | Python | LLM/City | useful |
| PlanGPT (paper; code TBD) | n/a | — | LLM/City | useful (paper) |
| adap/flower (Flower) | ~6,922 | Python | Federated/Edge | essential |
| FedML-AI/FedML | ~4,100 | Python | Federated/Edge | essential |
| OpenFederatedLearning/openfl | org-varies | Python | Federated/Edge | useful |
| google-parfait/tensorflow-federated | ~2,500 | Python | Federated/Edge | useful |
| mit-han-lab/mcunet | 718 | Python/C | Federated/Edge | essential |
| tensorflow/tflite-micro | high | C++/Python | Federated/Edge | essential |
| cityflow-project/CityFlow | research | C++/Python | Simulators/Datasets | essential |
| CityLearn/CityLearn | research | Python | Simulators/Datasets | essential |
| eclipse-sumo/sumo | very high | C++/Python | Simulators/Datasets | essential |
| flow-project/flow | research | Python | Simulators/Datasets | useful |
| carla-simulator/carla | ~15,000 | C++/Python | Simulators/Datasets | essential |
| mesa/mesa (+mesa-geo) | ~3,900 | Python | Simulators/Datasets | essential |
| gboeing/osmnx | ~5,800 | Python | Simulators/Datasets | essential |
| nutonomy/nuscenes-devkit | ~2,800 | Python | Simulators/Datasets | essential |
| waymo-research/waymo-open-dataset | research | Python/C++ | Simulators/Datasets | essential (research) |
| liuxu77/LargeST | research | Python | Simulators/Datasets | essential |
| liyaguang/DCRNN (METR-LA/PEMS-BAY) | research | Python | Simulators/Datasets | essential |
| CommonRoad/commonroad-carla-interface | research | Python | Simulators/Datasets | useful |

**Repository count covered:** 43 entries (including 2 data-canonical repos and 1 paper-without-confirmed-code), spanning all six categories—exceeding the ≥30 target.

---

*Research-only dossier. Star counts and activity are approximate as of research time (2026). Verify live GitHub metrics before procurement or citation-sensitive use.*
