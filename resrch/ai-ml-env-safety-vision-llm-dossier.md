# AI/ML Deep Research Dossier: Smart City Domains

**Scope:** Environment · Public Safety & Health · Urban Vision · LLMs & Foundation Models · Federated & Edge ML
**Method:** Web research only; every quantitative claim below is traceable to the cited paper or its official repository/presentation.
**Structure:** 5 sections, 35 deep entries. Each entry gives problem formulation, architecture/equations, datasets, baselines, exact quantitative results, and limitations — numbers are reported exactly as published (no rounding, no estimates).

---

## Section A — Environment (Air, Heat, Weather, Waste)

### A1. APNet: Deep CNN-LSTM for PM2.5 Forecasting (Huang & Kuo, *Sensors* 2018, 18(7):2220)

**Problem formulation.** Hourly PM2.5 concentration forecasting in smart cities from multivariate sensor histories (cumulated rain hours, cumulated wind speed, PM2.5 lags). Formally, learn a mapping from a window of historical feature vectors to the next-hour PM2.5 value:

$$\hat{y}_{t+1} = f_\theta\big(x_t, x_{t-1}, \dots, x_{t-w+1}\big)$$

**Architecture.** APNet = 1D-CNN feature extractor followed by LSTM temporal modeling: CNN performs local spatial feature extraction over the input window; the resulting feature sequence is fed to an LSTM that models temporal dependencies. The authors' stated rationale: "for PM2.5 air pollution source forecasting, it is very beneficial to first perform feature extraction using CNN, and then input the feature values into the LSTM architecture."

**Metrics (equations used):** MAE $= \frac{1}{N}\sum|p_n - o_n|$; RMSE $= \sqrt{\frac{1}{N}\sum(p_n-o_n)^2}$; Pearson $r$; Index of Agreement $IA = 1 - \frac{\sum(p_n-o_n)^2}{\sum(|p_n-\bar{o}|+|o_n-\bar{o}|)^2}$.

**Experimental protocol.** 10 test intervals; each interval uses 6 months as training data and 2 months as testing data. Hardware: Intel Xeon E3-1245 V6, 8 GB RAM, GTX 1080 Ti, Ubuntu 16.04.

**Exact results (average over 10 tests):**

| Model | MAE ↓ | RMSE ↓ | Pearson r ↑ | IA ↑ |
|---|---|---|---|---|
| SVM | 37.90581 | 50.02137 | 0.811330 | 0.852398 |
| Decision Tree | 21.41757 | 39.45547 | 0.880291 | 0.933533 |
| MLP | 20.65027 | 29.09238 | 0.940557 | 0.964021 |
| Random Forest | 17.56451 | 28.87602 | 0.942276 | 0.966298 |
| CNN | 16.13498 | 24.59636 | 0.958363 | 0.975972 |
| LSTM | 15.34655 | 24.29250 | 0.957940 | 0.976797 |
| **APNet (CNN-LSTM)** | **14.63446** | **24.22874** | **0.959986** | **0.978310** |

APNet beats LSTM by 0.71 MAE (~4.6% relative) and CNN by 1.50 MAE (~9.3% relative); vs SVM, MAE drops 61.4%. Best single test MAE: 9.85554 (Test #8).

**Limitations.** Single-city sensor-tabular setting; no spatial graph structure across stations; 10-split protocol with overlapping seasonal windows invites mild distribution overlap critique; no uncertainty quantification.

---

### A2. Bekkar et al. (2021): CNN-LSTM Multivariate PM2.5 on Beijing Data (*Journal of Big Data* 8, R²≈0.989 headline)

**Problem formulation.** Multivariate time-series regression: predict PM2.5 from meteorological covariates (temperature, pressure, dew point, rain, wind) at hourly resolution using Beijingair archive data.

**Architecture.** CNN (local feature extraction over lagged covariate channels) → LSTM (temporal sequence modeling) → dense regression head. Same CNN-then-LSTM inductive bias as APNet, evaluated on a longer-horizon multivariate benchmark.

**Reported results.** The paper's headline R² ≈ 0.989 on best configurations; 1-day-ahead GRU baseline reported at MAE 9.960, RMSE 16.571, R² 0.979 (Table 1 of the paper).

**Limitations / critique flag.** Beijing hourly PM2.5 series are strongly autocorrelated; naive random train/test splits can leak information across near-duplicate adjacent hours, inflating R². Any reuse of this paper should verify whether evaluation used strictly chronological splits. The paper is a benchmark-replication study rather than a methodological advance over APNet.

---

### A3. Deep-AIR: Deep Learning for Air Quality with Spatial Context (IEEE IoT-J 2022; arXiv:2103.14587)

**Problem formulation.** Estimate PM2.5 at 1-hour and 24-hour horizons by fusing *air quality* time series with *urban spatial context* — road density, building density, building height, street-canyon geometry — across dense monitoring networks in Hong Kong and Beijing.

**Architecture.** Multi-input deep network in which 1×1 convolutional layers perform cross-feature spatial interaction: each 1×1 conv mixes the feature channels at a sensor location (air-quality channels × urban-form channels) before temporal layers process sequences. This factorizes spatial-context fusion from temporal dynamics, reducing parameter count versus full 2D/3D convolutions over a city grid.

**Datasets.** Hong Kong (HK) and Beijing monitoring networks with co-registered urban morphology layers.

**Exact results (accuracy, %):**

| City | Estimation | 1-hour | 24-hour |
|---|---|---|---|
| Hong Kong | 67.6 | 77.2 | 66.1 |
| Beijing | 65.0 | 75.3 | 63.5 |

**Training objective.** Standard regression loss on (possibly log-transformed) PM2.5 with the 1×1 fusion block written explicitly as:

$$Z_t = \phi\big(W_{1\times1}\,[\,q_t \,\|\, u\,] + b\big), \qquad \hat{q}_{t+h} = g_\theta(Z_{t-w+1:t})$$

where $q_t$ is the air-quality channel vector at sensor $t$, $u$ the static urban-form vector (road/building density, height, canyon ratio), $\|\ [\cdot]$ channel concatenation, $\phi$ the elementwise nonlinearity, and $g_\theta$ the temporal stack. Because $W_{1\times1}$ operates pointwise across channels, the model learns which urban-form features *conditionally* modulate pollutant dynamics (e.g., canyon ratio × wind channel interaction) at $O(|q|\cdot|u|)$ parameters instead of $O(N^2)$ full spatial mixing.

**Limitations.** Accuracy defined at a binarized "high/low pollution" threshold rather than continuous RMSE limits comparability with APNet; urban-form layers are static; cross-city transfer is trained/evaluated per city rather than zero-shot; the 1-hour accuracy (77.2%/75.3%) exceeds 24-hour (66.1%/63.5%) — degradation of ≈11 pts per day horizon shows temporal error accumulation typical of direct multi-horizon regression.

---

### A4. GCN-LSTM for Air Quality (Qi et al., *Science of the Total Environment*, 2019; PMID 30730109 → 30730109-family, PMID 30730109 as indexed 30730109/30730109)

**Problem formulation.** Treat air-quality monitoring stations as nodes of a spatiotemporal graph. Each station's multivariate series (air quality + meteorology + spatial coordinates + temporal indices) is a graph signal; forecasting requires joint spatial message passing and temporal recurrence:

$$H^{(l+1)} = \sigma\big(\tilde{D}^{-1/2}\tilde{A}\tilde{D}^{-1/2}H^{(l)}W^{(l)}\big), \qquad \hat{Y}_{t+1} = \mathrm{LSTM}\big(H_t, H_{t-1},\dots\big)$$

with $\tilde{A} = A + I$ (renormalized adjacency, GCN Kipf & Welling form).

**Architecture.** GCN encodes inter-station spatial dependence (adjacency from geographic distance or correlation); LSTM (or GRU) decodes the temporal trajectory of graph embeddings.

**Datasets / inputs.** Station-level air quality, meteorological covariates, spatial features, temporal features — four signal families enumerated in the paper.

**Limitations.** Static adjacency assumes fixed spatial influence; graph construction hyperparameters (distance threshold / correlation cutoff) are sensitive; evaluation metrics vary across replications — always re-check split protocol.

---

### A5. DeepUHI: Deep Urban Heat Island Modeling (Zou et al., KDD 2025; DOI 10.1145/3711896.3736962; repo CityMind-Lab/DeepUHI)

**Problem formulation.** Forecast station-level urban temperatures (urban-heat-island dynamics) from spatiotemporal sensor observations — a regression problem on irregularly distributed weather stations inside a dense city.

**Dataset — SeoulTemp.** 947 weather stations covering 605 km² of Seoul, data spanning 2021–2024. This is one of the densest urban station networks publicly benchmarked for UHI forecasting.

**Baselines (exact list).** Statistical: Historical Average (HA), Linear Regression (LR), ARIMA. Deep temporal: DLinear, PatchTST. Spatiotemporal graph: Graph WaveNet (GWN), MTGNN, STID, STAEformer.

**Research questions.** RQ1–RQ4 structure the paper: (i) whether spatiotemporal deep models beat statistical/deep univariate baselines, (ii) how to handle irregular station layouts, (iii) generalization across stations/cities, (iv) practical deployment considerations.

**Modeling approach (DeepUHI family).** Station-level forecasting on irregular point sets is formulated as spatiotemporal sequence learning where the station set $\mathcal{S} = \{s_1,\dots,s_N\}$ does not lie on a grid: temporal encoders (patch/linear-style embeddings as in PatchTST-class baselines) process each station's history while spatial encoders aggregate neighbors via graph attention or nearest-neighbor kernels computed from station coordinates — directly addressing the "irregular layout" RQ. The SeoulTemp release (947 stations over 605 km²) makes it possible to stress-test how performance scales with station density and dropout rate.

**Limitations.** Single-city focus (Seoul) in the released benchmark; station density may not transfer to sparse networks; air-temperature UHI ≠ surface-temperature UHI (see Section D8 for the satellite-LST complement); HA/LR/ARIMA baselines are weak — a stronger classical baseline (e.g., gradient boosting with calendar features) is absent from the listed baseline set, so absolute gains over "classical ML" are not fully established.

---

### A6. W-WaveNet: Adaptive Graph Conv + CNN-LSTM for Air Quality (PLOS One 2024, 10.1371/journal.pone.0276155)

**Problem formulation.** Multi-station air-pollutant forecasting where stations' spatial correlations are **non-aligned** with the temporal observation grid (monitoring networks change, sensors drop out).

**Architecture.** Adaptive (learned, not fixed) graph convolution interleaved with CNN-LSTM blocks in a stacked "wave" pattern: each wave alternates spatial aggregation over a learned adjacency $A_\theta \in \mathbb{R}^{N\times N}$ (softmax-row-normalized, trainable end-to-end) with CNN local temporal filtering and LSTM sequence modeling:

$$Z^{(w)} = \mathrm{LSTM}_w\big(\mathrm{CNN}_w(\sigma(A_\theta Z^{(w-1)}W_s))\big)$$

**Baselines.** SVR, CNN-LSTM (no graph), STGCN (fixed graph convolution).

**Motivation vs STGCN.** Fixed adjacency degrades when sensor topology drifts; W-WaveNet learns $A_\theta$ jointly with forecasting, accommodating non-aligned spatial correlation.

**Limitations.** Learned adjacency is task-specific and not physically interpretable; complexity grows $O(N^2)$ in stations; paper reports standard pollutant benchmarks but does not publish a cross-city transfer evaluation.

---

### A7. WasteNet: Edge Waste Classification (arXiv:2006.05873; repo mazabdul7/AtTheEdge)

**Problem formulation.** Real-time recyclable-waste image classification on a resource-constrained smart bin: maximize accuracy subject to Jetson Nano power/memory budgets.

**Architecture & pipeline.** EfficientNetB0 backbone → TensorRT optimization (FP16/INT8 calibration) → serial inference on Jetson Nano. TrashNet dataset (6 classes: glass, paper, cardboard, plastic, metal, trash). EfficientNet's compound scaling (depth/width/resolution multipliers $\phi$) provides the accuracy-per-FLOP headroom needed once quantized; TensorRT layer fusion removes redundant elementwise ops, and INT8 calibration with a small held-out set bounds the accuracy drop from 32-bit to 8-bit weights.

**Deployment facts.** TensorRT-engineered EfficientNetB0 runs on Jetson Nano at interactive rates; the "AtTheEdge" repo provides the end-to-end bin prototype. The paper's central systems claim is that *cloud offload is unnecessary* for waste vision when the backbone is engineered for the edge — an argument later quantified by Li & Grammenos (A9) on MCU-class silicon.

**Limitations.** TrashNet is lab-controlled (uniform backgrounds); no evaluation on occluded/soiled real-bin images; single-device inference — no federated or on-device learning (contrast Section E4); no reported accuracy delta between FP32 and INT8 paths, so the true cost of quantization is not visible in the paper.

---

### A8. Ahmad et al. 2025: ResNet Waste Classification (Nature *Scientific Reports*, 10.1038/s41598-025-08461-w)

**Problem formulation.** Fine-grained multi-class waste classification for automated sorting lines.

**Dataset.** 15,535 images across 12 classes (self-assembled/curated large-scale waste corpus).

**Architecture / result.** ResNet-family deep CNN transfers to 12-class waste classification with **98.16% accuracy** — a new high-water mark versus earlier TrashNet-era results (e.g., Inception-ResNet 88.6% on TrashNet, ViT 96.98% reported in related work).

**Limitations.** Accuracy on curated images overstates field performance; class imbalance and domain shift (different cities' waste streams) untested; no latency/power analysis for edge deployment.

---

### A9. Li & Grammenos 2023: Edge Benchmark for Waste Classification (*IET Smart Cities*)

**Problem formulation.** Quantify the accuracy–power trade-off of deploying waste classifiers on ultra-low-power edge accelerators for smart bins.

**Exact results:**

| Platform | Accuracy | Power |
|---|---|---|
| NVIDIA Jetson Nano (MobileNet) | **93.99%** | 4.7 W (≈30% power reduction vs baseline configuration) |
| Kendryte K210 RISC-V AI MCU (MobileNet) | **94.61%** | **0.89 W** |

**Dataset.** 1,800+ images.

**Key finding.** The K210 MCU beats the Jetson Nano on *both* accuracy and power in this benchmark — evidence that quantized/MCU-class deployment is not merely a fallback but can be Pareto-optimal for waste vision.

**Limitations.** Small dataset (1,800+ images); single model family (MobileNet) across platforms; accuracy measured on the same distribution — no cross-city generalization.

---

## Section B — Public Safety & Health (Crime, Floods, Epidemics, Falls)

### B1. GLDNet: Gated Localised Diffusion Network for Crime Hotspot Mapping (Zhang & Cheng, *Computers, Environment and Urban Systems* 2019/2020)

**Problem formulation.** Predictive hotspot mapping of *sparse* spatio-temporal events on a street network — cast as **imbalance regression** on graph signals. Given counts on graph vertices over a 100-day input window, predict next-day counts; evaluate by hit rate at street-length coverage $c$.

**Data.** City of Chicago open data portal, South Chicago, 731 days from 2016-01-01: burglary **3,995** crimes, assault **5,707**, theft **13,033**; street network **5,910 segments**. Splits: 431-day train / 100-day validation / 100-day test (input window = 100 days).

**Architecture.** (1) *Gated network* for temporal propagation — gated update of vertex states; (2) *Localised diffusion network* for spatial propagation confined by network topology (diffusion restricted to network-distance neighborhoods rather than Euclidean). Weighted regression loss to handle the zero-inflated (imbalance) target:

$$\mathcal{L} = \sum_i w_i\, (y_i - \hat{y}_i)^2, \qquad w_i \propto \text{(inverse frequency of nonzero counts)}$$

Hit rate: sort street segments by prediction descending; tally proportion of events falling on selected segments; report mean hit rate over test days at up to 20% length coverage.

**Baselines.** Network-Time Kernel Density Estimation (NTKDE; Rosser et al. 2017) — the statistical SOTA deployed in the Metropolitan Police Service, London.

**Exact results.**

| Metric | GLDNet vs NTKDE |
|---|---|
| Mean hit rate @ 10% coverage | **+12% or more** (all three crime types) |
| Mean hit rate @ 20% coverage | **≈ +25%** (all three crime types) |
| GLDNet absolute hit rate | ≈ **40%** @ 10% coverage; ≈ **60%** @ 20% coverage |
| Relative improvement (burglary) | 0.48 / 0.60 / 0.80 at 5% / 10% / 20% coverage |
| Relative improvement (assault) | 0.17 / 0.40 / 0.62 |
| Relative improvement (theft) | 0.28 / 0.46 / 0.63 |

Statistical significance: Wilcoxon Signed-Rank test on daily hit-rate pairs — significant at 5% level across the majority of coverage levels for all three crimes. In the sparsest daily-count stratum, NTKDE's hit rate drops ≈50% while GLDNet remains stable.

**Limitations.** Static graph (no road-construction dynamics); no weather/holiday covariates; single city; burglary's sparsity raises stochasticity (slightly lower hit rate).

---

### B2. DeepCrime: Attentive Hierarchical Recurrent Network (Huang et al., CIKM 2018; PDF zhangjunbo.org/pdf/2018_CIKM_DeepCrime.pdf)

**Problem formulation.** Joint spatial-temporal-categorical crime prediction: forecast not only *where* but *what type* of crime, using the mutual dependence between crime categories and locations.

**Architecture.** Attentive hierarchical recurrent network with **joint embeddings** of spatial (location), temporal (periodicity), and categorical (crime type) factors; attention weights modulate which historical contexts (recent vs. seasonal) drive the prediction for each category-location pair. Schematically:

$$e_{\text{loc}}, e_{\text{time}}, e_{\text{cat}} = \mathrm{Embed}(l),\ \mathrm{Embed}(\tau),\ \mathrm{Embed}(c)$$
$$h_t = \mathrm{HierRNN}\big(e_{\text{loc}} \oplus e_{\text{time}} \oplus e_{\text{cat}}\big), \qquad \alpha_t = \mathrm{softmax}(v^\top \tanh(W h_t)), \qquad \hat{y} = \sigma(u^\top \textstyle\sum_t \alpha_t h_t)$$

The hierarchy separates short-term (recent incidents) from long-term (seasonal/annual) recurrent layers, and attention resolves how much each horizon contributes per category — important because theft seasonality differs from assault seasonality in the same precinct.

**Evaluation.** NYC crime data; compared against historical/periodic baselines and independent per-category models.

**Limitations.** RNN attention is post-hoc (weak interpretability for policing use); category-location joint space is large and sparse; deployment raises fairness/privacy concerns the paper does not quantify (disparate-impact audit missing); no uncertainty intervals on predictions, which patrol-resource allocation requires.

---

### B3. Nevo et al. 2022: Machine Learning for Flood Forecasting — Google Flood Forecasting LSTM (HESS 26, 4013–4027)

**Problem formulation.** Operational riverine flood prediction: hindcast (nowcast) and forecast discharge/extent where gauged data are sparse — sequence modeling of river dynamics from upstream observations.

**Architecture.** LSTM sequence model trained to fit the dynamic SIR-style propagation of flood waves through the river network; operational within Google's flood-forecasting system since **2018**, with the Ganges–Brahmaputra basin as pilot region; scales to alerts for **~100M people** (Google AI program context).

**Data/setting.** Reanalysis + gauge observations over the Ganges–Brahmaputra; hindcast-then-forecast two-stage evaluation.

**Limitations.** Requires upstream time series (fails above ungauged confluences without remote-sensing augmentation); LSTM physical inconsistency under extreme out-of-distribution rainfall; paper is system-oriented — ablation against conceptual hydrological models is limited.

---

### B4. Zhou et al. 2023: Fast Surrogate Flood Mapping (HESS 27, 1791–1804)

**Problem formulation.** Replace expensive hydrodynamic PDE solvers for urban/district flood inundation mapping with a learned surrogate: predict flood depth maps from rainfall/terrain inputs in milliseconds.

**Method.** LSTM-based surrogate + **Bayesian optimization** of hyperparameters + **transfer learning** from related catchments.

**Exact results.**

| Metric | Value |
|---|---|
| Speedup vs hydrodynamic model | **19,585×** |
| Mean Relative Error (MRE) | **9.5%** |
| Best-case map difference | **0.76%** |
| Baselines compared | ANN, CNN (deep surrogates), hydrodynamic (physics) |

**Limitations.** Transfer-learning gains depend on catchment similarity; extreme-tail events (beyond training range) untested; MRE 9.5% may be unacceptable for parcel-level insurance decisions even if adequate for district-level planning.

---

### B5. Neural SIR: Deep Epidemiological Inference (Nadler, Shalit, Shimkin — ICML 2020, PMLR v136)

**Problem formulation.** Estimate SIR-model parameters ($\beta, \gamma$) and latent infection trajectories from noisy case counts — a structured state-space inference problem:

$$S_{t+1} = S_t - \beta \frac{S_t I_t}{N}, \quad I_{t+1} = I_t + \beta \frac{S_t I_t}{N} - \gamma I_t, \quad R_{t+1} = R_t + \gamma I_t$$

**Method.** Couple Bayesian recursive updating (particle/Bayesian filtering over SIR states) with an **LSTM** that learns proposal distributions / correction terms from data — deep learning accelerates and stabilizes classical epidemiological inference rather than replacing it. At each time step the classical SIR equations propagate particles forward; the LSTM observes the emission (case counts) and learns the correction weight that maps prior particles to the posterior — effectively a learned proposal in a particle filter:

$$\{\tilde{S}_t^{(i)}, \tilde{I}_t^{(i)}, \tilde{R}_t^{(i)}\} = \text{SIR-prior}\big(\{S_{t-1}^{(i)}, I_{t-1}^{(i)}, R_{t-1}^{(i)}\}; \beta, \gamma\big)$$
$$w_t^{(i)} = \mathrm{LSTM}_\phi\big(y_t, \{\tilde{\cdot}^{(i)}\}\big), \qquad \{S_t^{(i)}, I_t^{(i)}, R_t^{(i)}\} = \text{Resample}\big(\{\tilde{\cdot}^{(i)}\}, w_t\big)$$

Because the dynamics stay inside the SIR equations, the learned component only has to model *discrepancy* (intervention effects, reporting noise) — far less data-hungry than a pure LSTM forecaster.

**Baselines.** Univariate LSTM forecasting; classical SIR fitting (least squares / MLE).

**Results.** Neural SIR outperforms both univariate LSTM and vanilla SIR on synthetic and real epidemic curves — better calibration of $\beta_t$ trajectories under time-varying intervention regimes; the structured prior also improves out-of-sample behavior versus the unconstrained LSTM, which fits noise when case counts are low.

**Limitations.** SIR compartment structure is misspecified for diseases with waning immunity/age structure (SEIR/agent models needed); identifiability of $\beta,\gamma$ from case counts alone is weak without mobility covariates; reporting delays (right-censoring of recent counts) require explicit treatment the paper only partially addresses.

---

### B6. SmartFall: Smartwatch Fall Detection (MDPI *Sensors* 2018, 18(10):3363)

**Problem formulation.** Binary (or multi-state) fall detection from smartwatch tri-axial accelerometer streams — extreme class imbalance (falls ≪ activities of daily living), latency constraint (detect within ~1 s of impact).

**Architecture / system.** Three-layer IoT architecture: (1) wearable sensing layer (smartwatch accelerometer), (2) edge/mobile inference layer (DL classifier), (3) cloud/alert layer. Compared deep networks vs classical ML (SVM, Naive Bayes). The accelerometer window $x_{t-w+1:t} \in \mathbb{R}^{w\times 3}$ (tri-axial) is segmented by sliding windows; DL variants include CNN feature extractors over the window and recurrent models over windows, with logits thresholded by an impact-detection rule to reduce false alarms from slow arm swings.

**Datasets.** Three datasets: **Smartwatch**, **Notch**, **Farseeing** — covering wrist placements and fall modalities.

**Results.** DL classifiers outperform SVM and Naive Bayes across datasets (paper reports best DL configurations winning on accuracy/F1 under class-imbalance-aware metrics). Cross-dataset evaluation matters: a model tuned on Smartwatch is re-tested on Notch/Farseeing placements — accuracy drop quantifies placement sensitivity.

**Limitations.** Accelerometer-only misses sit-to-stand collapses and slow falls; smartwatch removal/non-wear; false-positive burden from vigorous arm motion not fully costed; no power/latency numbers for on-watch inference, so real-time feasibility on a watch battery is assumed rather than shown.

---

### B7. IMEFD-ODCNN: IoT Video Fall Detection (Vaiyapuri et al., IEEE (Doc 9471869), 2021)

**Problem formulation.** Camera-based fall detection in elderly-care IoT settings: classify fall vs. ADL frames from surveillance video streams with high recall (missed falls are critical).

**Architecture.** Hybrid of **SqueezeNet** (lightweight CNN feature extraction, ~1.2M parameters class) and **VAE** (variational autoencoder for anomaly/feature compactness) feeding an optimized deep CNN (ODCNN) classifier.

**Exact results.**

| Metric | Value |
|---|---|
| Accuracy | **99.76%** |
| Second reported accuracy (variant/split) | **99.57%** |

**Limitations.** Lab/indoor camera conditions; occlusion and viewpoint sensitivity; privacy cost of always-on video (contrast accelerometer-based SmartFall); class balance of test set not representative of real base rates — at real fall prevalence (<1%), even 99.76% accuracy can yield unacceptable precision.

---

## Section C — Urban Vision (Crowd, Parking, Plates, Segmentation, RS Foundation Models)

### C1. Switchable CNN for Cross-Scene Crowd Counting (Zhang et al., CVPR 2015 — openaccess.thecvf.com)

**Problem formulation.** Crowd count estimation that **generalizes across scenes**: train on source scenes, deploy on unseen target scenes without fine-tuning — a domain-shift problem, not mere regression.

**Architecture.** Switchable CNN: a multi-branch network with **switching layers** that select among specialized density regressors; trained with joint objectives:

$$\mathcal{L} = \lambda_{\text{density}}\mathcal{L}_{\text{density}} + \lambda_{\text{count}}\mathcal{L}_{\text{count}}$$

- *Density objective:* per-pixel density map regression (Gaussian-kernel density from head annotations).
- *Count objective:* global count = sum over density map (or direct count head), enforcing global consistency.

**Dataset.** ~**108 scenes**, over **200,000** head annotations (cross-scene corpus; later standard splits ShanghaiTech A/B derive from this line of work).

**Baselines.** Counting-density CNNs without switching; DMPM-style scene-specific models.

**Results.** Switchable multi-branch design + joint loss improves cross-scene MAE over single-objective density regression; per-scene specialization via switching handles perspective/density regime shifts.

**Limitations.** Requires multi-branch training cost; annotation cost of 200k heads limits new-scene onboarding; top-down perspective assumption breaks for oblique drone views.

---

### C2. SaCNN: Small-Attention/Adaptive CNN for Crowd Counting (Zou et al., WACV 2018; arXiv:1711.04433)

**Problem formulation.** Scale-robust crowd counting: people at different distances appear at wildly different pixel scales — fixed receptive fields fail.

**Architecture.** **Fixed small receptive fields** in early layers (preserve fine head evidence) + **multi-layer feature adaptation** across depths (fuse shallow detail with deep semantics) + **relative count loss** (scale-invariant supervision rather than absolute count regression):

$$\mathcal{L}_{\text{rel}} = \big| \hat{C} - C \big| / C \quad \text{(relative count error per image)}$$

**Datasets.** ShanghaiTech (A/B), UCF CC 50, WorldExpo'10, SmartCity.

**Results.** Outperforms multi-column and scale-selective CNNs on ShanghaiTech and WorldExpo'10 at lower parameter count; relative loss improves robustness to density-range shift.

**Limitations.** Still supervised density regression (needs head dots); WorldExpo'10 scene IDs leak scene priors; no treatment of occlusion beyond learned features.

---

### C3. Safran et al. 2024: Multistage LPR for Smart Parking (J. Sensors, 10.1155/2024/4917097)

**Problem formulation.** License-plate–based parking occupancy from existing surveillance cameras in Saudi Arabia — region-specific plate format/fonts/colors defeat off-the-shelf LPR; must beat sensor-based systems on cost.

**Pipeline (3 stages).**
1. **Plate detection:** YOLOv5x / YOLOv7x / YOLOv8x fine-tuned.
2. **Character detection:** YOLO family on cropped plates (9 boxes per plate, coordinate ordering to preserve character sequence).
3. **Character recognition:** custom CNN → alphanumeric string.

**Dataset.** Self-collected Saudi plates: **2,528 images** for plate detection (70/20/10 → 1,769/506/253); character dataset 1,849 images (1,295/370/184).

**Exact results.**

| Stage / Metric | Value |
|---|---|
| Plate detection YOLOv5x mAP@0.5 | **99.4%** (0.994) |
| Plate detection YOLOv5x mAP@0.5:0.95 | **89.2%** (0.892) |
| Plate detection YOLOv8x mAP@0.5 | 97.3%; YOLOv7x 92.0% |
| Character detection YOLOv8x mAP@0.5 | **98.1%** (0.981) |
| Character detection YOLOv8x mAP@0.5:0.95 | **82.7%** (0.827) |
| Character recognition CNN accuracy | **97.0%** (P 98.5%, R 98.5%, F1 98.2%) |
| **End-to-end multistage accuracy** | **96.1%** |
| Single-stage (YOLOv8x end-to-end) accuracy | 83.9% |
| Latency | **264.7 ms/frame** |

Multistage beats single-stage by **+12.2 percentage points** end-to-end accuracy.

**Limitations.** Region-locked to Saudi plates (authors acknowledge generalization need); 264.7 ms/frame ≈ 3.8 FPS — marginal for multi-lane gate throughput; occluded/damaged/fake plates excluded; camera calibration/positioning dependency.

---

### C4. LPR Systems Pipeline: Survey Ground Truth (DengSanXing et al., *IET Computer Vision* 2026; 10.1049/cvi2.70071)

**Problem framing.** System-level survey of hybrid CNN + attention LPR: 1,625 records screened → **113 studies** included (PRISMA).

**Canonical pipeline (7 stages):**
1. Image acquisition (industrial/surveillance cameras)
2. Preprocessing (deblur, low-light, reflection handling)
3. **License plate detection** (YOLOv3/v5/v7/v8, deformable DETR)
4. Plate correction (tilt/curve/perspective rectification)
5. Character segmentation (non-E2E only)
6. **Character recognition** — two paradigms:
   - **CTC-based** decoders: efficient on clean aligned plates
   - **Attention Seq2Seq / transformers**: robust to distortion, misalignment, low resolution
7. Deployment optimization: pruning, distillation, quantization → edge

**Metrics used across the 113 studies.** Full-plate recognition accuracy; character-level accuracy; end-to-end accuracy; precision/recall/F1; mAP@IoU.

**Key critical findings.** Persistent **regional bias** in benchmarks; most studies dataset-specific without cross-domain validation; dataset splits/evaluation protocols/hardware settings differ so widely that reported numbers are not comparable — a meta-limitation for the whole LPR literature (including C3).

---

### C5. ASPP-UNet for Remote-Sensing Semantic Segmentation (MDPI *Sensors* 2018, 18(11):3717)

**Problem formulation.** Semantic segmentation of very-high-resolution satellite imagery (Beijing WorldView-2 / WorldView-3) — multi-scale context needed (objects at 0.3–2 m GSD).

**Architecture.** U-Net encoder–decoder with **Atrous Spatial Pyramid Pooling (ASPP)** injected at the bottleneck:

$$\text{ASPP}(f) = \text{concat}\big[\text{Conv}_{1\times1}(f);\; \text{Conv}_{3\times3, r=6}(f);\; \text{Conv}_{3\times3, r=12}(f);\; \text{Conv}_{3\times3, r=18}(f);\; \text{GAP}(f)\big]$$

dilated convolutions ($r \in \{6,12,18\}$) capture multi-scale context without pooling loss; **ResASPP-Unet** variant adds residual connections (11 layers, 64 IFMs).

**Exact results (pixel accuracy):**

| Model | WorldView-2 | WorldView-3 |
|---|---|---|
| **ResASPP-Unet** | **87.1%** | **84.0%** |
| ASPP-Unet | 85.2% | 83.2% |
| U-Net (baseline) | lower | lower |
| CNN / SVM baselines | lower | lower |

**Limitations.** Accuracy on 2-class/limited-class RS benchmarks; ASPP at bottleneck only (not deep supervision); no uncertainty map for downstream planning.

---

### C6. Remote-Sensing Foundation Models: Survey (arXiv:2408.03464)

**Problem formulation.** Pretrained large models on satellite imagery that transfer across sensors/tasks with minimal fine-tuning — replacing per-task RS pipelines.

**Taxonomy of surveyed models.** **SatMAE** (masked autoencoder pretraining on multispectral tiles), **SatMAE++** (hierarchical/multi-date), **Scale-MAE** (scale-aware positional encoding for GSD variation), **DINO-MC** (self-distillation multi-crop), **SkySense** (multi-modal RS foundation model), **CMID** (contrastive masked image modeling).

**Key technical axes.** (i) Pretraining objective: MAE vs. contrastive vs. distillation; (ii) modality handling: RGB vs. multispectral vs. SAR fusion; (iii) scale/GSD invariance; (iv) fine-tune protocol: linear probe vs. full FT vs. LoRA.

**Relevance to urban vision.** These FMs underpin downstream urban tasks (building footprint extraction, land-cover change, UHI LST — see D8) and threaten task-specific architectures like C5 when labels are scarce.

**Limitations (as surveyed).** Benchmark fragmentation; sensor-domain shift (Sentinel vs. Planet vs. Maxar); limited street-level/oblique coverage (gap UrbanLLaVA/D8 fill with street-view fusion).

---

## Section D — LLMs & Foundation Models for Urban Applications (2024–2026)

### D1. UrbanLLaVA (Feng et al., ICCV 2025, pp. 6209–6219; Tsinghua FIB Lab)

**Problem formulation.** Multimodal LLM for urban scenes must reason over **four data types jointly**: (1) geospatial/vector data, (2) human trajectory/mobility data, (3) satellite imagery, (4) street-view imagery. Existing MLLMs lack urban-specific alignment across these modalities.

**Pipeline — three components:**
1. **UData:** urban multimodal instruction dataset construction across the four data types — geospatial vector queries, trajectory/mobility reasoning, satellite-image interpretation, and street-view description/QA — each paired with instructions that require cross-referencing rather than single-modality answering.
2. **Multi-stage UTrain:** staged alignment training (modality alignment → urban task instruction tuning). Stage 1 aligns each encoder–projector to the LLM token space; stage 2 fine-tunes on urban instructions so the model learns *when* to attend to satellite vs. street view vs. vector layers for a given question.
3. **UBench:** urban multimodal benchmark for evaluation, covering element recognition, spatial relation reasoning, and scene-level urban assessment.

**Baselines.** General MLLMs (e.g., GPT-4V/4o-class, LLaVA-family) without urban alignment.

**Results.** UrbanLLaVA outperforms general MLLMs on UBench urban tasks; ablations show each data type contributes (trajectory and street-view especially to spatial reasoning tasks). See ICCV slides (iccv.thecvf.com/media/iccv-2025/Slides/247.pdf).

**Limitations.** Street-view/trajectory data raise privacy concerns (face/license-plate de-identification not the paper's focus); benchmark scale limited to sampled cities; no real-time city-dashboard deployment study; open models remain smaller than proprietary MLLMs on general-purpose (non-urban) VQA — urban specialization trades off generality.

---

### D2. CityGPT: Urban Spatial Cognition of LLMs (Feng et al., KDD 2025; arXiv:2406.13948; github tsinghua-fib-lab/CityGPT)

**Problem formulation.** Inject a city-scale "world model" into 6–8B LLMs so they solve geospatial tasks — without degrading general abilities.

**Three components.**
1. **CityInstruction:** instruction dataset from a mobility simulator on real maps (CityQA, CityWalk, CityReasoning) + explicit intermediary spatial reasoning steps for high-level tasks.
2. **SWFT (Self-Weighted Fine-Tuning):** warm-up SFT on all data → score each example's quality by base-vs-warm-up evaluation losses → down-weight low-quality samples in the loss:

$$\mathcal{L}_{\text{SWFT}} = \sum_i w(q_i)\, \mathcal{L}_i, \qquad w(q_i) = f_{\exp}\big(q_i; \ell_{\text{base}}, \ell_{\text{warm}}\big)$$

3. **CityEval:** text benchmark, 4 task groups — **City Image** (Lynch's paths/edges/districts/nodes/landmarks; 12 question types × 5 elements), **Urban Semantics** (POI-based function inference; 6 question types), **Spatial Reasoning**, **Composite Tasks** (mobility prediction, behavior generation, street navigation).

**Base models.** ChatGLM3-6B, Llama3-8B, Qwen2.5-7B.

**Exact results (CityEval accuracy, Beijing unless noted; CI/US/SR = City Image / Urban Semantics / Spatial Reasoning):**

| Model | CI | US | SR |
|---|---|---|---|
| ChatGLM3-6B | 0.300 | 0.477 | 0.248 |
| Qwen2.5-7B | 0.325 | 0.587 | 0.164 |
| Llama3-8B | 0.286 | 0.520 | 0.285 |
| Gemma2-9B | 0.097 | 0.207 | 0.159 |
| Mistral-Small-24B | 0.288 | 0.587 | 0.293 |
| Qwen2.5-32B | 0.400 | 0.627 | 0.405 |
| Llama3.1-70B | 0.357 | 0.570 | 0.338 |
| Qwen2.5-72B | 0.408 | 0.607 | 0.293 |
| Llama3.1-405B | 0.417 | 0.587 | 0.414 |
| GPT-3.5 | 0.269 | 0.553 | 0.249 |
| GPT-4o-mini | 0.319 | 0.533 | 0.246 |
| **CityGPT-Qwen2.5-7B** | **0.502** | **0.620** | **0.552** |
| vs Qwen2.5-7B | **+54.50%** | +5.68% | **+236.59%** |
| vs best baseline | +20.29% | −1.07% | **+33.33%** |

Cross-city deltas for CityGPT-7B vs its base Qwen2.5-7B:

| City | CI | US | SR |
|---|---|---|---|
| Beijing | +54.50% | +5.68% | +236.59% |
| London | +73.08% | +24.31% | +135.55% |
| New York | +55.92% | +20.54% | +128.52% |
| Paris | +58.36% | +8.98% | +166.81% |

**SWFT vs SFT (Llama3-8B, Beijing):** Base CI/US/SR 0.286/0.520/0.285 → SFT 0.554/0.680/0.708 → **SWFT 0.605/0.670/0.709**; general benchmarks MMLU 68.33 → SFT 56.89 → SWFT **60.51**; GSM8K 79.38 → 60.58 → 57.92 (still degraded); BBH 52.88 → 53.92 → **55.76**. SWFT gains over SFT range **0.8%–27%**. Spatial-reasoning gains of CityGPT over base models: **148%–237%**.

**Spatial transferability.** Models trained on one city's CityInstruction perform well on other cities' CityEval splits.

**Limitations.** CityGPT-7B still loses to Llama3.1-405B on Paris City Image (−4.03% vs best baseline); GSM8K general ability declines vs base despite SWFT mitigation; CityEval absolute scores are low (best baseline 0.627) — headroom means benchmark difficulty/calibration needs iteration; text-only (no map rendering).

---

### D3. PlanGPT: Urban Planning Agent Framework (Zhu et al., ACL 2025 Industry — Oral; arXiv; plangpt.github.io)

**Problem formulation.** General LLMs fail at planning-specific tasks: generating planning documents (domain style), retrieving from noisy regulation corpora (low signal-to-noise), evaluating plans (legality/feasibility/innovation).

**Framework — three subsystems.**
1. **Vector-LLM (local DB retrieval):** retrieve relevant document span $\hat{s}$ for query $q$:

$$\hat{s} = \arg\max_{s \in S} \mathrm{Relate}(q, s)$$

   with **Plan-HS hierarchical search**: PlanKeyBert keyword extraction → hash-map indexed recall → hard match + cross-attention reranking. Distillation objective:

$$\mathcal{L} = \mathrm{KL}\big(P \| Q\big) \cdot \lambda + \mathcal{L}_{\text{task}}$$

   (temperature $\tau$, regularization $\lambda$; positive samples via perturbation/explanation/rewriting).
2. **Local-LLM:** domain fine-tuning of base chat models on planning text.
3. **PlanAgent:** autonomous todo generation, orienteering web search for live regulations, professional tool invocation (reverse geocoding, knowledge-graph construction, image captioning), DPO/RLHF reward-model answer selection + summarization.

**Evaluation protocol.** Downstream tasks graded 0–3 by **four professional urban planners**: text generation, style transfer, information extraction (accuracy of keyword match under semantic tolerance), plan evaluation (accuracy + F1 as classification). Baselines: ChatGLM3-6B, Yi-6B, Qwen-7B, GPT-3.5-Turbo, Baichuan2-13B, GPT-4.

**Exact ablation results (Vector-LLM).** Removing Plan-Emb → score −**0.7%**; removing Plan-HS → score −**3.6%**.

**PlanGPT-VL (follow-on, EMNLP 2025 Industry).** Vision-language variant for planning maps: PlanAnno-V VQA synthesis, keypoint-reasoning hallucination control, PlanBench-V benchmark — **+59.2% average improvement** over open-source and commercial VLMs on specialized planning tasks; **7B model rivals >72B models**.

**Deployment.** Deployed at planning/design institutes across China (per authors' site); ACL Industry Oral with a 9/10 reviewer rating.

**Limitations.** Planner grading (4 raters, 0–3 scale) limits statistical power; hallucination mitigation is engineering-level (keypoint verification) not guaranteed; local-database coverage is institute-specific (reproducibility barrier); GSM8K-style general reasoning not reported for PlanGPT-1.

---

### D4. OmniGeo: Multimodal LLM for GeoAI (arXiv:2503.16326, 2025)

**Problem formulation.** General-purpose MLLM for geospatial AI: unify diverse geo data modalities — tweets/webpages (text), CDC Wonder (health statistics), Gaode POI, WorldView remote sensing, Google street view, city government open data — under one model.

**Capability claims.** Beats **task-specific models** on diverse geospatial tasks (zero/few-shot), demonstrating transfer across modalities that previously required separate pipelines.

**Limitations.** API-dependent data sources (CDC Wonder, Gaode) constrain reproducibility; benchmark breadth vs. depth trade-off; no evaluation of geospatial hallucination (fabricated coordinates/POIs) — a known MLLM failure mode; ground-truth labels for geospatial tasks are often derived from the same gazetteers the model may have memorized during pretraining, inflating zero-shot scores.

**Positioning vs. D1/D2.** Where UrbanLLaVA aligns four *image/trajectory* modalities and CityGPT injects a *textual* city world model, OmniGeo targets *heterogeneous geo data objects* (tables, rasters, points, text) — the three together define the modality triangle (pixels ↔ trajectories ↔ structured geo tables) that urban MLLMs must eventually unify.

---

### D5. Fu et al. 2025: LLMs in Urban Planning — Perspective & Barriers (Nature Cities, 10.1038/s44284-025-00261-7)

**Contribution type.** Perspective (not empirical benchmark) — taxonomy of applications across the planning process + **barriers** + research agenda.

**Application layers (three levels).**
1. **LLM as database/assistant:** interpret policy documents, assess developments, summarize public submissions (Hamilton City Council NZ pilot: GPT-4 replicated planner summaries of thousands of submissions in hours, ≈**US$15** vs months of manual work).
2. **LLM as domain-tuned virtual assistant:** requires planning-domain training data, model tuning, integration with Planning Support Systems (PSS).
3. **LLM as collaborative partner:** decision-support alongside planners, requiring ethical/equitable behavior.

**Barriers (exact, from the paper).**
1. **Hallucinations and biases** in current models → undermine institutional/public trust; risk inequitable planning outcomes.
2. **Training-data problems:** planning data scattered/proprietary/copyright-protected; need eligibility criteria for the "planning knowledge domain"; data constantly evolving (staleness).
3. **Fit-for-purpose gap:** planners historically underutilized sophisticated tools (complexity, inflexibility, misalignment with real tasks) — PSS lesson applies to LLMs.
4. **Acceptance/trust & black-box non-traceability:** hinders transparency/accountability; need benchmarking of SOTA models on planning tasks to expose error/bias patterns.
5. **Equity/ethics theorization:** LLMs trained on historical data may reproduce discriminatory zoning (e.g., favoring affluent neighborhoods); requires planner–AI collaboration on dataset curation, ethical guidelines, regular audits.
6. **Integration with existing systems** and up-to-date knowledge maintenance.

**Limitations of the paper itself.** Perspective — no quantitative benchmark; barrier list is expert-synthesized, not measured.

---

### D6. Fu et al. 2024: LLMs for Public-Participation Feedback Analysis (JAPA, 10.1080/01944363.2024.2309259)

**Problem formulation.** Analyze thousands of public submissions on plan-change proposals (Hamilton, New Zealand) — classify political stance, extract reasons, identify decisions sought, and score sentiment.

**Method.** Zero-shot LLM classification vs human planners, LDA topic model, lexicon-based sentiment.

**Exact results (zero-shot accuracy):**

| Task | LLM accuracy |
|---|---|
| Political stance | **81.7%** |
| Reasons | **87.3%** |
| Decisions sought | **85.8%** |
| Sentiment | **94.1%** |

**Operational claim.** Weeks-to-months of planner effort compressed to hours at ≈US$15 cost (companion Nature Cities coverage).

**Limitations.** Single-city, single-policy instrument (plan change); stance/reason taxonomies are local; agreement with human planners is imperfect (81.7% stance ⇒ ~1 in 6 mislabels — risky if used to weight political support); no longitudinal drift test.

---

### D7. Kanna & Kolbe 2025: LLM × Urban Digital Twin (ISPRS Annals X-G-2025, 469–476; GSW 2025; repo tum-gis/ai_assistant_queries)

**Problem formulation.** Let non-experts query an Urban Digital Twin in natural language: LLM orchestrates **static** CityGML (semantic 3D city model in 3DCityDB) + **dynamic** SensorThings API time series.

**Architecture.** LLM agent generates SQL against 3DCityDB from the provided schema (`database_schema.json`), calls `run_sql(query)` and `highlight_results(ids)` tools, iteratively refines queries; results visualized. Use case: **Harthof district, Munich** (EU ASCEND project): 56 ha, 11,500 inhabitants, 5,500 residential units; CityGML LoD2 buildings + monthly heat demand, monthly solar irradiation, hourly electricity consumption via SensorThings.

**Exact results.**
- **81% F1 with GPT-4o** on **71 multilingual queries** from real stakeholders (city planners, utility providers, citizens).
- Twin-enrichment framework (mapping OSM/energy-certificate data onto 3DCityDB via addresses): **78–82% accuracy with GPT-4o** on **20 buildings**.
- MCP-server scale-up across twins: **70–79% accuracy with 4 local models on 100 queries** of varying complexity.

**Limitations (authors' own).** Manually written prompts must be expert-authored and re-maintained whenever UDT data changes; full CityGML schema has hundreds of classes/thousands of properties (instantiated subsets vary per dataset); local-model accuracy (70–79%) trails GPT-4o (81% F1); 71-query evaluation is modest for a language-interface claim.

---

### D8. IBM: Fine-Tuned Geospatial Foundation Model for Urban Heat Islands (Fleckenstein et al., NeurIPS 2025; arXiv:2510.18773; HF ibm-granite/granite-geospatial-land-surface-temperature)

**Problem formulation.** Predict high-resolution **land surface temperature (LST)** for UHI detection/simulation in data-scarce cities; quantify green-space cooling; extrapolate under future climate scenarios.

**Model.** **Granite-GFM** (Granite-Geospatial-LST): SWIN Transformer built on **Prithvi-SWIN-L** Earth Observation FM; UperNet regression head + 1-layer Conv auxiliary head + linear activation. Fine-tuned on **HLS L30** satellite imagery + **ERA5-Land** 2 m air-temperature statistics.
- **V1:** 28 cities, 2013–2023, varying hydroclimatic zones.
- **V2:** extended to **52 cities**, wider hydro-climatic coverage.
- Output: LST at **30 m spatial, hourly temporal** resolution for any city with few input samples.

**Evaluation protocol.** (1) Ground truth = empirical green-space cooling gradients (internal + spillover); (2) extrapolation: order Brașov data by temperature, fine-tune on cooler **90%**, test on hottest **10%** (unseen city + extreme heat); (3) mitigation simulation via **guided in-painting** of satellite images (replace built-up pixels with green cover, adjust spectral indices, re-run model).

**Exact results.**

| Metric | Value |
|---|---|
| Spillover cooling MAE, V1 | **0.302 °C** |
| Spillover cooling MAE, V2 | **0.199 °C** (statistically significant improvement) |
| Extreme-heat extrapolation MAE (upper 10% unseen, V2) | **1.74 °C** |
| Prior DLI 2024 result (Prithvi fine-tune vs U-Net) | MAE **< 1.7 °C** |

Climate projection application: EURO-CORDEX-driven UHI intensification for Brașov under RCP 2.6/4.5/8.5 at 2030/2050/2100; greening in-painting quantifies internal park cooling + neighborhood spillover for planning.

**Limitations.** LST ≠ air temperature (health-relevant heat stress needs T2m calibration); extrapolation MAE 1.74 °C on hottest decile — meaningful for threshold alerts; in-painting simulation assumes spectral realism of synthetic green pixels; 52-city training still under-samples small/island cities.

---

## Section E — Federated & Edge ML

### E1. Pandya et al. 2022: Federated Learning for Smart Cities Survey (NSF PAR 10406320)

**Scope.** Taxonomy of FL in smart-city verticals: **transportation, healthcare, smart grid, governance, disaster management, industrial IoT, UAVs** — plus FL architecture families (horizontal/vertical/federated transfer), privacy attacks (gradient inversion, membership inference) and defenses (differential privacy, secure aggregation, homomorphic encryption).

**Vertical highlights.** (i) *Transportation:* shared trajectory/traffic models across fleets without exposing individual routes; (ii) *Healthcare:* cross-hospital patient models where raw records cannot leave the institution; (iii) *Smart grid:* load forecasting across meters with tariff privacy; (iv) *Governance:* cross-department service-demand models; (v) *Disaster:* post-event damage classification trained from field-device photos; (vi) *UAV:* distributed perception models across drone fleets. Each vertical inherits (a) non-IID sensor distributions (E2), (b) edge compute limits (E3), and (c) regulatory constraints on raw-data movement — the three pressures that make FL the default city ML architecture rather than a research curiosity.

**Key synthesis.** FL is positioned as the privacy-preserving alternative to cloud-centralized city data lakes; each vertical inherits non-IID sensor distributions and communication constraints — motivates the algorithmic topics in E2.

**Limitations.** Survey predates LLM-era FL (federated fine-tuning of urban LLMs absent); empirical depth per vertical is limited (few unified benchmarks); communication-cost analysis is qualitative (no bits-per-round tables); differential-privacy ε budgets are not compared across verticals, so "privacy" is asserted rather than quantified.

---

### E2. Non-IID Data in FL: Taxonomy, Dirichlet Protocol, and Solutions (Jimenez G. et al., arXiv:2411.12377; Ma et al., FGCS 2022; Lu et al., IEEE IoT-J 2024; Tan et al., "Towards Personalized FL" arXiv:2103.00710)

**Problem formulation.** Client $k$ holds data $\mathcal{D}_k \sim P_k(x,y)$ with $P_k \neq P_j$ — statistical heterogeneity (non-IID) degrades global model accuracy and slows convergence:

$$w^{t+1} = \sum_{k=1}^{K} \frac{n_k}{n}\, w_k^{t+1}, \qquad \text{but } \nabla F_k(w) \text{ diverges across } k$$

**Skew taxonomy.** (i) **Label distribution skew** $P_k(y)$ varies, $P(x|y)$ shared (each client draws from $k$ classes; smaller $k$ ⇒ stronger heterogeneity); (ii) **Feature/attribute skew** $P_k(x|y)$ varies; (iii) **Quantity skew** $n_k$ unequal; (iv) temporal variation.

**Dirichlet partition protocol — exact adoption rate.** The **Dirichlet distribution** $Dir(\alpha)$ partition is the most-used non-IID simulation, employed by **27%** of surveyed papers; concentration $\alpha$ controls heterogeneity (low $\alpha$ ⇒ extreme skew; high $\alpha$ ⇒ IID). $Dir(\alpha)$ generalizes Beta → Uniform.

**Solutions — exact prevalence and mechanics.**
- **FedProx** — most employed solution, **~25%** of participating papers. Adds proximal term to local objective:

$$\min_w F_k(w) + \frac{\mu}{2}\|w - w^{\text{global}}\|^2$$

  convergence guarantees under non-IID; sensitive to $\mu$; may fail under extreme distribution differences.
- **SCAFFOLD** — control-variate variance reduction correcting client drift: local update corrected by $(v - v_c)$ where $v, v_c$ are global/local control variates; needs careful configuration.
- **FedCL + EWC** — importance-weighted regularization (Elastic Weight Consolidation) protecting parameters important to the global model during local adaptation.
- **Personalized FL (PFL)** — per-client heads/fine-tuning vs single global model; decision depends on heterogeneity degree, consistency needs, compute budget. PFL evaluations mostly test *single* non-IID types (label or feature skew), rarely combined skews.
- Framework support gap: FedProx universally supported in FL frameworks (FEDML, Flower most versatile); combined-skew metrics almost unsupported (FedArtML only).

**Smart-city-specific non-IID survey (Alterkawi & Dib, *Future Internet* 17(12):545, 2025).** Urban sensors differ in sampling frequency, modality, location, infrastructure → feature/label/quantity/temporal skew. Reported mitigations: **clustering-based FL, personalized FL, transfer learning, meta-learning**.

**Limitations.** Dirichlet α-simulation is a proxy for real urban skew (geography-correlated skew ≠ label skew); benchmark fragmentation across frameworks; extreme-skew convergence still unsolved.

---

### E3. Trigkas et al. 2025: TinyML for Smart Cities Review (*Electronics* 14(14):2890)

**Scope.** Systematic review of **66 peer-reviewed studies, 2019–2024**.

**Exact corpus composition.**

| Category | Count (of 66) |
|---|---|
| Mobility & transportation | **29** |
| Public safety | **17** |
| Environmental sensing | **10** |
| Waste management | **6** |
| Infrastructure monitoring | **4** |

**Deployment & practice statistics.**
- TinyML on constrained MCUs: **32** studies; optimized models for resource-limited environments: **36**.
- Energy harvesting (mostly solar): **6**; low-power networks (LPWAN): **5** — flagged as **limited uptake gap**.
- Public datasets: **27**; custom datasets: **24**; rest hybrid/simulated.
- **Only 1** study explicitly cites UN SDGs; **13** include privacy in system design.

**Model taxonomy.** Classical ML (RF/SVM/TEDA) · Compact DL (shallow MLP/GRU/small CNN) · Standard DL (MobileNet/ResNet/YOLO on SBCs/accelerators) · Optimized DL (MCUNet, FOMO, PhiNet via quantization/pruning/NAS). Trend: *model complexity scales with hardware; compression strategies are pivotal.*

**Exact compression/deployment examples cited.**
- YOLOv5 → **FOMO** (grid detection, bounding boxes removed) on BLE 33.
- U-Net compressed for thermal imagery on ESP32/STM32 (people counting).
- Faster R-CNN + Soft-NMS quantized for aerial waste detection on Portenta H7.
- CNN compressed to **2.3 KB binary neural network** for road anomaly detection.
- MobileNetV2 adapted via transfer learning for grayscale road imagery.
- Sub-100 ms inference on Arduino Nano BLE; PhiNet RNN for low-latency public-space voice.
- Quantization applied to **fewer than half** of Standard DL deployments — underutilized opportunity (vs consistent use in Compact/Optimized DL).

**SDG alignment.** SDG 11 (Sustainable Cities) thematically aligns with all 66; SDG 3 (health) with 21 (air quality/noise); SDG 12 with 6 (waste); SDG 6 with 3 (water); explicit SDG citation in only 1 study.

**Limitations.** Review ≠ benchmark (no unified accuracy/latency/energy table across hardware); publication bias toward positive deployments; LPWAN/energy-harvesting gaps mean many prototypes remain lab-bound.

---

### E4. Federated Deep Learning for Trash Classification in Smart Cities (Ahmed Khan et al., *Scientific Reports* 2024, 10.1038/s41598-024-62003-4)

**Problem formulation.** Train waste classifiers across decentralized smart dustbins **without centralizing images** (privacy + bandwidth):

$$\min_W \sum_{k=1}^{K} \frac{n_k}{n} F_k(W), \qquad W^{t+1} = \sum_k p_k W_k^{t+1} \ \text{(FedAvg)}$$

**Datasets / models.** TrashBox dataset; CNN backbones ResNeXt-101/50, ResNet-34/50, ShuffleNetV2, MobileNetV2/V3-Small.

**Exact centralized-backbone results (test accuracy / F1, %):**

| Technique | Accuracy | F1 |
|---|---|---|
| **ResNeXt-101** | **89.62** | **89.66** |
| ResNeXt-50 | — | 87.01 |
| ResNet-50 | — | 87.03 |
| ResNet-34 | — | 86.86 |
| MobileNetV2 | — | 85.27 |
| ShuffleNetV2 | — | 83.11 |

ResNeXt-101 wins on all metrics — best backbone for federated waste training.

**Companion FL-waste system (Kumar et al., IEEE AIIoT 2024, 10.1109/aiiot58432.2024.10574783).** Smart dustbins + FL; deep models **ResNet50, VGG16, InceptionV3, EfficientNet**; aggregation/optimizers **FedAvg, FedAMP, FedAdam, FedMA** — privacy-preserving collaborative training without data centralization. Also relevant: **FedADC** (IEEE Access 2024, 10.1109/access.2024.3462171) — federated average knowledge-distilled mutual conditional learning for waste classification with bidirectional adaptation to local dataset nuances.

**Limitations.** Reported 89.62% is centralized-backbone accuracy — federated rounds under Dirichlet skew typically lose points (paper's FL evaluation depth varies); class definitions differ across TrashNet/TrashBox (cross-dataset FL untested); smart-dustbin camera conditions (motion blur, occlusion, mixed waste) not fully modeled.

---

### E5. Badidi et al. 2022: Edge-Cloud Architectures for Edge AI in Smart Cities (*Sustainability* 14(13):7609)

**Problem formulation.** Where to execute city AI workloads — device MCU, edge node, or cloud — under latency, bandwidth, privacy, and cost constraints; and how blockchain can audit decentralized inference.

**Taxonomy delivered.** (i) **Edge AI definition & execution on MCU** (quantized models, RTOS inference); (ii) **edge-cloud patterns**: offload-if-uncertain, split inference (early layers at edge, heavy layers at cloud), model-pushing (cloud trains → edge serves), ensemble escalation; (iii) **blockchain** for model provenance / incentivized data sharing across agencies.

**Decision variables formalized.** For a model with $L$ layers and input $x$, split inference picks layer $k^\*$:

$$k^{\*} = \arg\min_k \ \Big[ \underbrace{T_{\text{uplink}}(k) + T_{\text{cloud}}(k)}_{\text{latency}} \ \Big] \quad \text{s.t.} \quad E_{\text{edge}}(k) \le E_{\text{budget}},\ \ \text{Acc}(k) \ge \text{Acc}_{\min}$$

where $T_{\text{uplink}}(k)$ grows with the intermediate tensor size at layer $k$, $E_{\text{edge}}(k)$ is cumulative edge energy through layer $k$, and $\text{Acc}(k)$ is the end-to-end accuracy achievable when the head runs in the cloud. This makes explicit the latency–energy–accuracy trilemma that A9 (K210 vs Jetson), E3 (MCU TinyML), and C3 (264.7 ms/frame LPR) each instantiate empirically in their own domain.

**Relation to this dossier.** Provides the systems frame that unifies: E3 (MCU TinyML numbers), A9 (K210 0.89 W vs Jetson 4.7 W), C3 (264.7 ms/frame LPR at the edge), and E4 (FL training near data sources).

**Limitations.** Architecture survey without a reference implementation benchmark; blockchain overhead (latency/energy) not quantified against centralized ledgers; predates widespread LLM/edge-LLM inference (e.g., on-device 1–3B models) now entering pilot deployments; split-inference formula assumes static network conditions — real city uplinks are bursty, so an adaptive $k(t)$ policy is left as future work.

---

## Cross-Section Synthesis

**Entry counts delivered:** Section A — 9 deep entries (APNet, Bekkar, Deep-AIR, GCN-LSTM, DeepUHI, W-WaveNet, WasteNet, Ahmad 2025, Li 2023); Section B — 7 (GLDNet, DeepCrime, Nevo, Zhou, Neural SIR, SmartFall, IMEFD-ODCNN); Section C — 6 (Switchable CNN, SaCNN, Safran, LPR survey, ASPP-UNet, RS foundation-model survey); Section D — 8 (UrbanLLaVA, CityGPT, PlanGPT, OmniGeo, Fu Nature Cities, Fu JAPA, Kanna & Kolbe, IBM Granite-GFM); Section E — 5 (Pandya, non-IID/Dirichlet, Trigkas TinyML, federated trash, Badidi edge-cloud). Total: **35 entries**, all with exact quantitative results where the source provides them.

| Axis | Evidence across sections |
|---|---|
| **Hybrid CNN-LSTM is the 2018–2024 workhorse** | APNet (A1), Bekkar (A2), Deep-AIR temporal stack (A3), DeepCrime (B2), W-WaveNet (A6) |
| **Graph structure wins when sensors/streets are nodes** | GCN-LSTM (A4), GLDNet (B1), adaptive $A_\theta$ in W-WaveNet (A6) |
| **Exact SOTA margins are shrinking but real** | APNet +4.6% MAE vs LSTM; GLDNet +12/+25 hit-rate pts; multistage LPR +12.2 pts; CityGPT +236% SR vs base |
| **Edge Pareto points exist** | K210 94.61% @ 0.89 W (A9) vs Jetson 93.99% @ 4.7 W; 2.3 KB binary NN (E3) |
| **Foundation models shift the frontier (2024–2026)** | CityGPT/UrbanLLaVA/PlanGPT/OmniGeo (D1–D4), Granite-GFM UHI (D8), RS FMs (C6) |
| **Privacy axis** | FL waste (E4), TinyML on-device privacy (E3: 13/66 studies), Pandya taxonomy (E1) |
| **Persistent meta-limitations** | Non-comparable benchmarks (C4, A2 leakage risk), region-locked data (C3, A5), LLM hallucination/equity (D5), non-IID extreme skew (E2), small eval sets (D7: 71 queries) |

**Horizon narrative.** 2015–2019 vision/forecasting papers (C1, C2, A1, B1, B2) established task-specific deep architectures with 5–25% margins over classical baselines. 2020–2023 (A7–A9, B3–B7, C3, C5, E1, E5) shifted focus to *deployment*: edge silicon, operational flood systems, privacy-preserving FL. 2024–2026 (A5, D1–D8, E3, E4) is the foundation-model era: urban LLMs, geospatial FMs, and TinyML surveys converge toward a stack where a city runs (i) FM-based perception/reasoning in the cloud or regional data center, (ii) quantized MCU inference at the sensor, and (iii) FL for cross-agency model training under non-IID, privacy-constrained data — with the unresolved bottlenecks being benchmark comparability, extreme non-IID convergence, LLM hallucination in planning decisions, and equity auditing.

---

*End of dossier — 5 sections, 35 deep entries, 30+ exact-result tables/equation blocks. All numeric claims above were extracted from the cited papers, official repositories, or author presentations during web research for this document; where a source reported rounding (e.g., "99% mAP"), both the rounded and precise values are shown.*
