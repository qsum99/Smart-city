# AI/ML Research Dossier: Intelligent Systems for Smart Cities
### A Five-Section Technical Survey of Recent Literature (Web-Research Based; No Code)

---

**Scope and method.** This dossier surveys machine-learning and deep-learning research for smart-city applications across five mandated sections: (A) air quality and environmental sensing, (B) public safety and health, (C) urban vision, (D) large language models and foundation models (2024–2026), and (E) federated learning, edge computing and TinyML. Each paper entry is structured as: (a) problem formulation, (b) architecture/method with the governing equations, (c) dataset scale/city/duration, (d) baselines, (e) exact quantitative metrics as reported by the authors, and (f) limitations. All numbers below were transcribed from primary sources (publisher pages, arXiv, open-access PDFs, official repositories) retrieved during this research session. Where two versions of the same work report different numbers (e.g., arXiv preprint vs. journal version), both are given and labelled.

**Bibliographic corrections made during research.** (1) "SaCNN" is WACV 2018 (arXiv:1711.04433, November 2017) — it is frequently miscited as "2017". (2) Zhang et al., CVPR 2015 is *Cross-Scene Crowd Counting via Deep CNN* (switchable dual-objective training), which is a different paper from MCNN (Zhang et al., CVPR 2016); both appear in Section C tables and must not be conflated.

---

# SECTION A — AIR QUALITY & ENVIRONMENT (7 papers)

## A.1 APNet — "A Deep CNN-LSTM Model for Particulate Matter (PM2.5) Forecasting in Smart Cities"
*Huang & Kuo, Sensors 2018, 18(7):2220 (MDPI).*

**(a) Problem.** One-hour-ahead regression of surface PM2.5 concentration from a 24-hour sliding window of three channels: PM2.5 concentration, cumulated wind speed, and cumulated hours of rain. Output: next-hour PM2.5.

**(b) Method.** APNet is a two-stage hybrid: a CNN front-end extracts local temporal features, an LSTM back-end forecasts. The CNN half contains three 1-D convolution layers; batch normalization is inserted after the 2nd and 3rd convolutions. Rather than ReLU, the network uses Scaled Exponential Linear Units for self-normalizing properties (λ = 1.05, α = 1.67):

- SELU: f(x) = λ·x if x > 0; f(x) = λ·α·(e^x − 1) if x ≤ 0
- LSTM gate standard form: f_t = σ(W_f·[h_{t−1}, x_t] + b_f), i_t = σ(W_i·[h_{t−1}, x_t] + b_i), C̃_t = tanh(W_C·[h_{t−1}, x_t] + b_C), C_t = f_t ⊙ C_{t−1} + i_t ⊙ C̃_t
- Final stage: fully-connected layer + sigmoid activation producing the scalar forecast.

**(c) Dataset.** UCI Beijing PM2.5 (US Embassy station, hourly). Experiments comprise 10 separate test runs; hardware: Intel Xeon E3-1245 V6, 8 GB RAM, GTX 1080 Ti, Ubuntu 16.04.

**(d) Baselines.** SVM, Decision Tree (DT), Random Forest (RF), MLP, pure CNN, pure LSTM — same inputs, same splits.

**(e) Exact metrics (averages over the 10 tests).**

| Model | MAE ↓ | RMSE ↓ | Pearson r ↑ | Index of Agreement ↑ |
|---|---|---|---|---|
| SVM | 37.90581 | 50.02137 | 0.81133 | 0.852398 |
| DT | 21.41757 | 39.45547 | 0.880291 | 0.933533 |
| MLP | 20.65027 | 29.09238 | 0.940557 | 0.964021 |
| RF | 17.56451 | 28.87602 | 0.942276 | 0.966298 |
| CNN | 16.13498 | 24.59636 | 0.958363 | 0.975972 |
| LSTM | 15.34655 | 24.2925 | 0.95794 | 0.976797 |
| **APNet** | **14.63446** | **24.22874** | **0.959986** | **0.97831** |

**(f) Limitations.** Single station, single city, single-hour horizon; no spatial (cross-station) information; the gain over plain LSTM is small (MAE 14.63 vs 15.35 ≈ 4.6%); sigmoid output layer can saturate at extreme concentrations; no uncertainty quantification or extreme-pollution-event breakdown.

## A.2 Hybrid CNN-LSTM Multivariate — "Air-pollution prediction in smart city, deep learning approach"
*Bekkar et al., 2021, DOI 10.1186/s40537-021-00548-1.*

**(a) Problem.** Hourly PM2.5 forecast in Beijing combining three feature families: historical pollutants, meteorology, and *adjacent stations'* PM2.5 (a hand-crafted spatial proxy), with 24-hour input lags.

**(b) Method.** CNN extracts cross-feature/spatial structure over the multivariate channel stack; LSTM models the temporal sequence. Training: Adam, learning rate 0.001, LR decay 0.0001, 200 epochs, EarlyStopping(min_delta=1e-3, patience=50), batch size grid {24, 32, 64, 128}, ReLU activations. Seven baselines trained under identical protocol: LSTM, Bi-LSTM, GRU, Bi-GRU, CNN, CNN-GRU, CNN-LSTM (the last two are hybrid competitors).

**(c) Dataset.** UCI Beijing multi-site air quality: 420,768 instances × 18 attributes, 12 monitoring stations (hourly), meteorology matched to nearest CMA weather station. Missing values filled by interpolation (see limitations).

**(d)/(e) Exact metrics (reported Table 1, best batch = 32 unless noted).**

| Model | 1-day lag MAE | 1-day RMSE | 1-day R² | 7-day MAE | 7-day RMSE | 7-day R² |
|---|---|---|---|---|---|---|
| GRU (b=32) | 9.541 | 16.609 | 0.978 | 11.055 | 18.122 | 0.974 |
| LSTM (b=32) | 9.503 | 16.217 | 0.980 | 11.623 | 19.154 | 0.972 |
| Bi-LSTM (b=32) | 8.868 | 15.597 | 0.982 | 11.253 | 18.488 | 0.974 |
| Bi-GRU (b=64) | 9.192 | 16.196 | 0.981 | 11.631 | 19.289 | 0.969 |
| CNN (b=32) | 9.591 | 16.981 | 0.979 | 11.150 | 18.606 | 0.975 |
| **CNN-LSTM (b=32)** | **6.742** | **12.921** | **0.989** | **9.034** | **16.625** | **0.979** |
| CNN-GRU (b=32) | 9.459 | 17.700 | 0.977 | 9.459 | 18.700 | 0.967 |

Relative to LSTM, CNN-LSTM cuts MAE from 9.503 → 6.742 (−29.1%) and RMSE from 16.217 → 12.921 (−20.3%) at 1-day lag.

**(f) Limitations and leakage critique.** (i) The paper's own pipeline interpolates missing target values and constructs *station-interpolated* neighbor features; if any interpolated target enters input windows or if splits are not strictly chronological, R² ≈ 0.989 is inflated by autocorrelation rather than genuine 24-hour-ahead skill — a classic leakage risk in hourly PM2.5 studies. (ii) Adjacent-station features encode an implicit graph with no learning of the graph (no GCN), so transport effects (wind direction, topography) are misrepresented. (iii) Evaluation is Beijing-only, 1-hour/1-day/7-day lags only, and the best batch size was selected on the same criteria used for reporting (selection bias). (iv) No baseline classical model (ARIMA/SVR) and no graph-based DL baseline are included. Reported values near R² = 0.99 should be treated with caution until reproduced with purged time-series cross-validation.

## A.3 GC-LSTM — "A hybrid model for spatiotemporal forecasting of PM2.5 based on graph convolutional neural network and long short-term memory network"
*Qi, Li, Karimian & Liu, Science of the Total Environment 664 (2019) 1–10, DOI 10.1016/j.scitotenv.2019.01.333.*

**(a) Problem.** Forecast PM2.5 at *all* monitoring stations jointly, treating stations as graph vertices and their observations as graph signals: historical observations form a spatiotemporal graph series; air-quality variables, meteorological factors, spatial terms and temporal attributes are the graph signals.

**(b) Method.** Spectral graph convolution (Chebyshev-polynomial family, following Bruna/Defferrard/Kipf-Welling) captures spatial dependency; LSTM captures temporal dependency. Spectral convolution layer:

- X_{p+1} = σ( Σ_{k=0}^{K−1} θ_k T_k(L̃) X_p ), with Chebyshev recursion T_k(x) = 2x·T_{k−1}(x) − T_{k−2}(x), T_0 = 1, T_1 = x, and normalized Laplacian L̃ = 2L/λ_max − I (complexity O(K·|E|) instead of eigendecomposition).

**(c) Dataset.** Jing-Jin-Ji region (Beijing–Tianjin–Hebei, 113°E–120°E, 36°N–43°N), China MEE open ground-station observations; multi-step horizons up to 72 h.

**(d) Baselines.** State-of-the-art statistical and deep predictors evaluated at multiple prediction intervals (pure recurrent/CNN-style forecaster counterparts, as described in the paper's comparison section).

**(e) Exact metrics.** For 72-hour predictions: **R² = 0.72**, **recall = 68.45%**, **false-alarm rate = 4.65%** at an alert threshold of 115 µg/m³. GC-LSTM achieved the best results among compared models at all tested intervals, and error growth with increasing prediction length was markedly slower than baselines.

**(f) Limitations.** A single regional network; R² = 0.72 at 72 h leaves substantial variance unexplained; alarm metrics depend on one hand-set threshold (115 µg/m³); the station graph is typically built from geographic/correlation similarity and is static, ignoring wind-driven *directed* pollutant flow (a weakness later works address with directed flow graphs); no uncertainty intervals.

## A.4 Deep-AIR — "A Hybrid CNN-LSTM Framework for Fine-Grained Air Pollution Estimation and Forecast in Metropolitan Cities"
*Zhang, Han, Li & Lam; arXiv:2103.14587 (2021); IEEE Access 10 (2022) DOI 10.1109/ACCESS.2022.3174853.*

**(a) Problem.** Two coupled tasks: (1) fine-grained *city-wide* current-hour pollution estimation from image-like urban-dynamics tensors, and (2) *station-level* 1-hour and 24-hour forecasts. Domain-specific features: air pollution, weather, urban morphology (road density, building density/height, street canyon), transport (speed, congestion), time-sensitive features.

**(b) Method.** CNN branch with **1×1 convolutions** to model cross-feature interactions between pollutants and urban-dynamics channels (1×1 conv mixes channels at each pixel/location: Y[i,j] = Σ_c W[c,c']·X[i,j,c] + b), plus an "AirRes" component of four residual units (each unit: two 3×3 convs with BN+ReLU, 1×1 conv between units); LSTM branch (input length 48 h, 1–2 layers, hidden {128, 256, 512}); SGD, lr = 10⁻⁴, early stop after 5 stagnant epochs; patch size 15.

**(c) Datasets.** Hong Kong, 16 months (from Dec 2018) and Beijing, 19 months (Jan 2017–Jul 2018), hourly; city dynamics rendered as image-like grids.

**(d) Baselines.** Statistical models (e.g., ARIMA) and deep models: LSTM, Attention-LSTM, ConvLSTM, GCN-LSTM (paper explicitly groups baselines into pure-temporal vs spatially-structured).

**(e) Exact metrics.** Two reporting versions:

| Task | arXiv v1 (HK) | arXiv v1 (Beijing) | IEEE Access (HK) | IEEE Access (Beijing) |
|---|---|---|---|---|
| Fine-grained 1-hr estimation | 67.6% | 65.0% | 68.9% | 65.8% |
| 1-hr forecast | 77.2% | 75.3% | 78.9% | 76.1% |
| 24-hr forecast | 66.1% | 63.5% | 67.7% | 64.8% |

Margin over best baseline (IEEE Access): HK +1.7% estimation, +1.7% (1-hr), +3.8% (24-hr); Beijing +1.4%, +2.3%, +3.3%. Saliency: for Hong Kong, street canyon and road density are the strongest predictors of NO₂, meteorology/historical pollutants for PM2.5; for Beijing (no street-canyon layer), historical pollutants, traffic congestion, wind direction and seasonal indicator dominate. PM10 best-performing pollutant in HK; CO best in Beijing.

**(f) Limitations.** Classification-accuracy metric is coarse for regression-like targets (no MAE/RMSE reported); margins over best baselines are 1.4–3.8 percentage points; two cities only, with feature sets *not* symmetric (Beijing lacks morphology channels), confounding cross-city comparison; accuracy drops ~13 points from 1-hr to 24-hr horizons; no probabilistic outputs.

## A.5 DeepUHI — "Fine-grained Urban Heat Island Effect Forecasting: A Context-aware Thermodynamic Modeling Framework"
*Zou, Ruan, Zhong, Hu & Liang, KDD 2025, DOI 10.1145/3711896.3736962; code/data: github.com/CityMind-Lab/DeepUHI.*

**(a) Problem.** Street-level, hourly urban heat island (UHI) forecasting: predict temperature at 947 stations over Seoul and flag spatio-temporally extreme hot spots (warning task), using environmental context per station.

**(b) Method.** DeepUHI is physics-informed: it anchors on the heat equation ∂T/∂t = α∇²T + q and performs an explainable **heat decomposition** into (i) *thermodynamic cycles* (local source/sink behavior of land-use contexts) and (ii) *thermal flows* (spatial transport between station groups), integrating satellite imagery, street-view imagery and land-use embeddings per station. Implementation: PyTorch, Adam (lr 0.01, weight decay 1e-4), batch 256, look-back 96 steps, environmental embedding dim 8, nodes partitioned into 10 landscape groups, 8:1:1 temporal split. Warning metric: Spatio-temporal Top-K Accuracy (STTop-K) — whether the true hottest (location, time) lies in the model's top-k predicted cells.

**(c) Dataset — SeoulTemp (released with paper).** 947 temperature stations, 605 km² of Seoul, hourly, 1 Jan 2021 – 8 Apr 2024; temperature range −19.9 to +43.2 °C; average inter-station distance ≈ 500 m; context assigned on a 500 m × 500 m grid; modalities: SDot hourly temperatures (Seoul SDot project), satellite + street-view imagery, Seoul Land-use Dataset (Korea EGIS). Inter-station differences exceed 10 °C in both winter and summer.

**(d) Baselines.** Statistical: Historical Average (HA), Linear Regression, ARIMA; time-series: DLinear, PatchTST; spatio-temporal: Graph WaveNet (GWN), MTGNN, STID, STAEformer (plus "+Context" augmented variants).

**(e) Exact metrics.** Regional temperature prediction, MAE (°C) by horizon:

| Horizon | DeepUHI MAE | DeepUHI sMAPE |
|---|---|---|
| 12 | 1.433 | 0.241 |
| 24 | 1.811 | 0.303 |
| 48 | 2.367 | 0.375 |
| 96 | 3.231 | 0.464 |

UHI-warning STTop-K precision (best baseline in parentheses):

| Horizon | k=3 | k=9 |
|---|---|---|
| 24 h | **0.653** (STAEformer 0.472) | **0.802** (0.604) |
| 48 h | **0.495** (0.376) | **0.569** (0.423) |

Compute: DeepUHI 20.95 M multi-adds vs STAEformer 236,330 M, GWN 297,160 M, STID 7,560 M, DLinear/LR 1.69 M — i.e., ~10³× cheaper than ST baselines while winning the warning task. Deployment: SeoUHI platform issues day-ahead street-level warnings for >10 million Seoul citizens.

**(f) Limitations.** Single city (Seoul), single sensor network; heat-equation decomposition assumes diffusive dynamics that may not hold under advection (strong wind); landscape grouping fixed at 10 groups (sensitivity 10–25 noted but standardized); MAE advantage over best TS/ST baselines at short horizon is small (1.433 vs ~1.43), while the warning task shows the real gain; satellite/street-view dependence complicates replication.

## A.6 W-WaveNet — "A multi-site water quality prediction model incorporating adaptive graph convolution and CNN-LSTM"
*Yang, Zhong & Chen, PLOS ONE 19(3): e0276155 (2024), DOI 10.1371/journal.pone.0276155.*

**(a) Problem.** Multi-site, multi-step water-quality forecasting that handles **non-aligned spatial correlations** — correlation structures that change across time spans and cannot be captured by a single static adjacency matrix.

**(b) Method.** Adaptive graph convolution (AGCN; learnable adjacency refined per layer) is *interleaved* with CNN-LSTM blocks in a stacked encoder-decoder ("wave" structure): spatial aggregation and temporal convolution alternate so that non-aligned correlations are re-learned at each timescale. Metrics: MAE, MAPE, RMSE, RMSPE, r², Pearson r.

**(c) Dataset.** Two real river sections instrumented with multiple monitoring sites; six commonly used water-quality factors (including pH, TP, TN, NH₃); three forecast steps (t+1..t+3).

**(d) Baselines.** SVR, Random Forest, CNN-LSTM, STGCN; ablations: WaveNet (no AGCN/LSTM), WaveNet-LSTM (no AGCN), WaveNet-MGCN (no LSTM).

**(e) Exact metrics (overall performance, averaged over stations/factors/steps).**

*Section A:*

| Model | MAE | MAPE | RMSE | RMSPE | r² | r |
|---|---|---|---|---|---|---|
| RF | 0.381 | 0.113 | 0.627 | 0.091 | 0.873 | 0.935 |
| SVR | 0.375 | 0.116 | 0.630 | 0.091 | 0.869 | 0.934 |
| CNN-LSTM | 0.460 | 0.158 | 0.709 | 0.116 | 0.824 | 0.917 |
| STGCN | 0.302 | 0.092 | 0.494 | 0.072 | 0.912 | 0.956 |
| **W-WaveNet** | **0.225** | **0.070** | **0.406** | **0.061** | **0.939** | **0.969** |

*Section B:* W-WaveNet MAE 0.287, MAPE 0.083, RMSE 0.504, RMSPE 0.073, r² 0.912, r 0.955 (vs CNN-LSTM 0.511/0.133/0.814/0.102/0.819/0.911).

Headline: average MAE 0.264 across sections — **45.2% lower than CNN-LSTM and 23.8% lower than STGCN**. Ablations: removing AGCN raises MAE 38.0% (0.363); removing LSTM raises it 30.9% (0.326). NH₃ at t+1: MAE SVR 0.274, RF 0.283, CNN-LSTM 0.354, STGCN 0.258, W-WaveNet 0.165 (−41.7% vs RF); stability holds at t+3 (0.187 vs RF 0.382, −51.3%).

**(f) Limitations.** Only two river sections; the paper states data were "generated on" these sections (model-derived/simulated series limit external validity); no cross-river generalization; CNN-LSTM baseline underperforms even RF, suggesting hyperparameter mismatch — i.e., some gains reflect tuning asymmetry; no uncertainty or extreme-pollution-event analysis.

## A.7 FPHFA — "Forecasting of PM2.5 Concentration in Beijing Using Hybrid Deep Learning Framework Based on Attention Mechanism"
*Li, Liu & Zhao, Applied Sciences 2022, 12(21):11155, DOI 10.3390/app122111155.*

**(a) Problem.** Short-term (1–12 h) and longer-term (13–96 h) PM2.5 prediction across 12 Beijing stations from multivariate pollutant + meteorological series.

**(b) Method.** Multi-channel 1-D CNN (trend/spatial features between sites) → Bi-LSTM (bidirectional temporal correlation) → attention layer (weights informative time steps): h'_t = α_t·h_t with α_t = softmax(e_t), e_t = v^T tanh(W_a h_t + b_a).

**(c) Dataset.** UCI Beijing multi-site, 12 stations, 1 Mar 2013 – 28 Feb 2017, hourly (PM2.5, PM10, temperature, pressure, etc.).

**(d) Baselines.** LSTM, GRU, CNN-LSTM, DAQFF (attention-free hybrid).

**(e) Exact metrics (short-term task).**

| Model | RMSE | MAE | R² | IA | MAPE |
|---|---|---|---|---|---|
| LSTM | 34.39 | 23.03 | 0.796 | 95.30% | 0.707 |
| GRU | 32.62 | 22.25 | 0.824 | 95.93% | 0.683 |
| CNN-LSTM | 31.69 | 21.81 | 0.832 | 96.15% | 0.672 |
| DAQFF | 30.12 | 21.02 | 0.849 | 96.47% | 0.669 |
| **FPHFA** | **28.15** | **19.19** | **0.877** | **97.04%** | **0.561** |

Gains vs CNN-LSTM: RMSE −11.2%, MAE −12.0%, R² +0.045. The model "performs well" for 1–12 h and yields "satisfactory results" for 13–96 h (per authors).

**(f) Limitations.** Single city; attention weights are not validated as explanations; gains over the best non-attention hybrid (DAQFF) are moderate (RMSE 28.15 vs 30.12); longer-horizon (13–96 h) numbers are not tabulated at the same granularity; no graph structure despite 12-station data.

**Section A synthesis.** Across seven studies the field converges on hybrid temporal architectures (CNN+LSTM ± attention/graph), with consistent findings: (i) spatial structure (graphs, street-canyon features, station adjacency) adds 1.4–3.8 pp accuracy (Deep-AIR) or 12–30% MAE reduction (W-WaveNet vs non-graph); (ii) physics-informed constraints (heat equation) buy extreme-event warning skill at ~10³× lower compute (DeepUHI); (iii) reported R² near 0.99 (Bekkar) should be audited for interpolation/split leakage; (iv) nearly all studies are single-city — cross-city transfer remains open.

---

# SECTION B — PUBLIC SAFETY & HEALTH (6 papers + 1 note)

## B.1 GLDNet — "Graph deep learning model for network-based predictive hotspot mapping of sparse spatio-temporal events"
*Zhang & Cheng, Computers, Environment and Urban Systems 79 (2020) 101403, DOI 10.1016/j.compenvurbsys.2019.101403.*

**(a) Problem.** Predictive hotspot mapping of *sparse* events (crime) on a street network: generate daily risk maps over street segments. Sparsity in both space and time makes grid/area-based DL models ill-posed; events are represented as graph signals on a **weighted, undirected street graph**. The many zero counts reframe the task as an **imbalanced regression** problem.

**(b) Method.** GLDNet = gated network (temporal propagation) + localized diffusion network (spatial propagation) + weighted regression loss:
- Temporal gate (GRU-style): z_t = σ(W_z x_t + U_z h_{t−1}), r_t = σ(W_r x_t + U_r h_{t−1}), h̃_t = tanh(W x_t + U(r_t ⊙ h_{t−1})), h_t = (1 − z_t) ⊙ h_{t−1} + z_t ⊙ h̃_t.
- Localized Diffusion Network (LDN): stacked layers whose inner connections preserve graph topology and propagate information to 0-, 1st- and 2nd-order neighbors with **localized weight sharing** (parameters shared over local neighborhoods — the model's answer to sparse supervision); two-to-five LDN layers with small hidden widths in reference configurations (2 Gated-ReLU layers/8 units; 5 LDN layers/4 units; loss parameter ρ ≈ 0.03 in independent re-implementation).
- Weighted loss: L = Σ_i w(y_i)·(ŷ_i − y_i)², with larger weights for informative non-zero/rare observations to counter imbalance.

**(c) Dataset.** City of Chicago open data portal, South Chicago side: street network of **5,910 segments**; burglary **3,995**, assault **5,707**, theft **13,033** events; **731 days** from 1 Jan 2016; **100 consecutive test days** (ending 31 Dec 2017).

**(d) Baseline.** Network-Time Kernel Density Estimation (NTKDE; Rosser et al. 2017) — the deployed statistical standard (used by London's Metropolitan Police). Other DL models excluded by the authors because sparsity breaks them (an acknowledged evaluation gap).

**(e) Exact metrics.** Hit rate = proportion of events falling on the top-ranked street segments (up to 20% street-length coverage), averaged over 100 test days:

| Crime | GLDNet vs NTKDE @10% coverage | @20% coverage | GLDNet level (@10% / @20%) |
|---|---|---|---|
| Burglary | +12% or more | ≈ +25% | ≈ 40% / ≈ 60% |
| Assault | +12% or more | ≈ +25% | ≈ 40% / ≈ 60% |
| Theft | +12% or more | ≈ +25% | ≈ 40% / ≈ 60% |

Mean relative daily improvement (5% / 10% / 20% coverage): burglary 0.48/0.60/0.80; assault 0.17/0.40/0.62; theft 0.28/0.46/0.63. Differences significant at the 5% level (Wilcoxon signed-rank test) across most coverage levels; NTKDE's hit rate collapses ≈50% on the sparsest days whereas GLDNet degrades gracefully. GLDNet maps are also more spatially compact/connected (better for patrol routing).

**(f) Limitations.** One city, three crime categories, 2016–2017; single statistical baseline (no DL competitor); hit-rate-only evaluation (no calibration/probability scores); risk maps are daily (no intra-day dynamics); burglary remains noisier due to extreme sparsity.

## B.2 DeepCrime — "Attentive Hierarchical Recurrent Networks for Crime Prediction"
*Huang, Zhang, Zheng & Chawla, CIKM 2018, DOI 10.1145/3269206.3271793.*

**(a) Problem.** Predict whether each crime *category* occurs in each region of a city per time slot — a multi-class classification problem over regions with evolving region–category–time inter-dependencies.

**(b) Method.** (i) Joint embeddings of spatial (region), temporal (slot) and categorical signals; (ii) attentive hierarchical recurrent network: LSTM/GRU layers over time with an attention mechanism assigning β_t = softmax(v^T tanh(W h_t)) to past time slots, so recent/relevant periods are weighted automatically; MLP head (3 hidden layers) for per-category scores. Training: TensorFlow, Adam, lr 0.001, batch 64, grid-searched hyper-parameters.

**(c) Dataset.** New York City Open Data, 1 Jan – 31 Dec 2014; four categories above frequency threshold (Robbery, Burglary, Felony Assault, Grand Larceny); **77 police precincts**; **24,031 POIs** (14 categories); 311 complaints (4 categories: Noise, Blocked Driveway, Illegal Parking, Building Use). Split chronological: 6.5 months train / 0.5 month validation / 1 month test; 30 consecutive test days.

**(d) Baselines.** SVR, ARIMA, Logistic Regression, MLP, TriMine (tensor factorization), Wide&Deep, GRU.

**(e) Exact metrics.** Macro-F1 / Micro-F1, October test month: **DeepCrime 0.6836 / 0.6233** vs GRU 0.6530 / 0.5879 (+4.5% / +6.1% over the best baseline), TriMine 0.6432 / 0.5258, MLP 0.6482 / 0.5436, LR 0.6378 / 0.5304, ARIMA 0.6362 / 0.5514, SVR 0.6383 / 0.5380, Wide&Deep 0.6467 / 0.5419. Per-category F1 (August example): burglary DeepCrime 0.6173 vs GRU 0.5394 (avg +11.0% over GRU, +18.8% over Wide&Deep, +18.7% over TriMine for burglary); robbery 0.6300 vs LR 0.5165 (+21.9%); felony assault 0.6459; grand larceny 0.8734. Consistent best-in-class across Aug–Dec; gains grow as data gets sparser.

**(f) Limitations.** Classification (occurrence) rather than count/regression or hotspot mapping; NYC 2014 only; 77-region granularity set by precincts; gains over GRU ≈ 4–6% absolute Macro-F1; no weather/calendar-exogenous covariates beyond time features; attention interpretability asserted but not quantitatively validated.

## B.3 Google Flood Forecasting — "Flood forecasting with machine learning models in an operational framework"
*Nevo et al., Hydrology and Earth System Sciences 26 (2022) 4013–4034.*

**(a) Problem.** Operational riverine flood warnings at scale: (1) river-stage forecasting at gauges, (2) flood inundation extent/depth mapping, (3) alert delivery — replacing/augmenting hydraulic and conceptual hydrological models.

**(b) Method.** Four subsystems: data validation → stage forecasting → inundation modeling → alert distribution.
- Stage: LSTM with **128 cell states**; inputs = past **168 h** of hourly stage at target + upstream gauges and past **240 h** of mean areal precipitation; predicts hourly stage for all lead times up to each gauge's maximum (8–48 h). A linear model (with/without precipitation) is the operational fallback.
- Inundation: (i) *thresholding model* (extent from stage thresholds) and (ii) *manifold model* (first presentation here) — an ML alternative to hydraulic modeling predicting both extent and depth; alerts rendered at **16 m** resolution.
- Loss/eval: Nash–Sutcliffe Efficiency (NSE) NSE = 1 − Σ(o−f)²/Σ(o−ō)², persistence-NSE, and per-pixel F1 = 2PR/(P+R).

**(c) Scale/coverage.** Operational during the **2021 monsoon season** in India and Bangladesh: stage models at **167 gauges**, inundation models at **126 gauges**; AOI ≈ **287,000 km²** (abstract cites flood-prone river regions totalling close to 470,000 km²) home to **>350 million people**; **≈115 million flood alerts** sent, reaching **≈22 million people**; alerts in local languages.

**(d) Baselines.** Linear stage models (± precipitation), persistence baselines; thresholding vs manifold for inundation; external comparison to US NWS stage models (Zalenski et al. 2017).

**(e) Exact metrics.**

| Stage model | Median NSE (range) | Median persistence-NSE |
|---|---|---|
| Linear, no precip | 0.9839 (0.8368–0.9988) | 0.5851 |
| Linear, + precip | 0.9847 (0.8368–0.9989) | 0.5991 |
| LSTM, no precip | 0.9862 (0.8444–0.9992) | 0.6608 |
| **LSTM, + precip** | **0.9870 (0.8508–0.9992)** | **0.6708** |

Inundation F1: 1-year cross-validation — thresholding **69.01** (41.67–92.49), manifold **69.12** (36.91–91.36); leave-extreme-out — thresholding **76.74** (2.48–96.68), manifold **76.27** (10.36–95.46). Stage RMSE medians 0.1 m (24 h) and 0.2 m (48 h) vs NWS 0.3/0.5 m. Lead times per gauge: commonly 12–48 h (e.g., Bhagyakul & Mawa 48 h; Mirpur 12 h).

**(f) Limitations.** Requires *gauged*, large rivers and upstream telemetry — inapplicable to ungauged/flash-flood regimes; per-pixel F1 ≈ 69% means material false-alarm/miss areas; delivery ≠ comprehension (authors cite the warning-use gap); performance ranges are wide across gauges (F1 as low as 2.48% in leave-extreme-out worst case); extreme events under-represented by training.

## B.4 Rapid Urban Flood Surrogate — "A deep-learning-technique-based data-driven model for accurate and rapid flood predictions in temporal and spatial dimensions"
*Zhou, Teng, Situ, Liao & Feng, Hydrology and Earth System Sciences 27 (2023) 1791–1809.*

**(a) Problem.** Predict urban flood maps (maximum water depth spatial fields) and flood time series for arbitrary hyetograph inputs, in near-real time, as a substitute for slow physics-based hydrodynamic simulation.

**(b) Method.** LSTM network predicting flood maps, with **Bayesian optimization** over network structure (relative error between prediction and ground truth serves as the a-priori objective; BO infers the optimal architecture from historical error) and **transfer learning** from source site A to new site B (pre-train → fine-tune with limited target samples).

**(c) Dataset.** Case studies in northern China (Site A + Site B for transfer); hyetograph inputs paired with ground-truth flood maps from the physically based hydrodynamic model (153.2 s average runtime per map).

**(d) Baselines.** (i) The physically based hydrodynamic model (ground truth/runtime reference); (ii) Artificial Neural Network; (iii) Convolutional Neural Network.

**(e) Exact metrics.** Speed: DL model **0.038 s** vs hydrodynamic **153.2 s** → **19,585× faster on average** (worst case: hydrodynamic >36,600× slower). Accuracy: **mean relative error 9.5%** on water depths; best single prediction differs from ground truth by only **0.76%**; Bhattacharyya distances ≈ 0, histogram-intersection / structural similarity / 2D-CC all ≈ 1 (near-identical spatial patterns). Transfer learning enabled successful deployment at a second site; DL model outperformed ANN and CNN baselines.

**(f) Limitations.** Supervised by hydrodynamic-model output (inherits model bias; not independent ground truth); site-specific training with transfer still requiring local data; single-country, pipe-network-dependent urban settings; extreme-event (rare hyetograph) coverage unquantified; no uncertainty bands.

## B.5 Neural SIR — "A Neural SIR Model for Global Forecasting"
*Nadler, Arcucci & Guo, PMLR v136 (ML4H @ NeurIPS 2020) 254–266.*

**(a) Problem.** Forecast confirmed COVID-19 infections across countries by fusing compartmental epidemiology with deep sequence learning — capturing latent (unreported) infections that SIR alone cannot observe.

**(b) Method.** Discretized SIR inside a **Bayesian recursive updating framework** (data assimilation estimating latent I), coupled to an LSTM:
- SIR ODEs: dS/dt = −β·S·I/N; dI/dt = β·S·I/N − γ·I; dR/dt = γ·I.
- LSTM: 175 neurons, ReLU activation, Adam optimizer, MSE loss, dense layers → 1 output neuron; inputs are the SIR state variables + observed cases.
- Coupled forecast: ŷ = w₁·ŷ_LSTM + w₂·ŷ_SIR, where w₁, w₂ are relative weights set by each model's *previous-period forecasting error* (self-calibrating blend).

**(c) Dataset.** Johns Hopkins University Coronavirus Resource Center daily time series (confirmed/recovered/deceased); six countries: India, Brazil, Turkey, Philippines (developing), US, UK (developed).

**(d) Baselines.** Dynamic SIR alone; univariate LSTM (cases only); multivariate LSTM (coupled inputs without SIR combination).

**(e) Exact metrics (one-step-ahead in-sample).**

| Model | US MSFE | US MAFE | UK MSFE | Brazil MSFE | India MSFE |
|---|---|---|---|---|---|
| **Neural SIR** | **5.64×10⁹** | **5.93×10⁴** | **2.50×10⁸** | **4.47×10⁸** | **1.30×10⁸** |
| Dynamic SIR | 3.20×10¹⁰ | 1.27×10⁵ | 4.27×10⁸ | 2.34×10⁹ | 1.52×10⁸ |
| Univ. LSTM | 1.56×10¹⁰ | 1.24×10⁵ | 7.02×10⁸ | 1.99×10⁹ | 2.43×10⁸ |
| Multiv. LSTM | 8.12×10⁹ | 8.44×10⁴ | 3.18×10⁸ | 3.06×10⁸ | 1.25×10⁸ |

MAPE (Neural SIR): India 4.42×10⁻¹, Brazil 1.53×10⁻¹, Turkey 6.78×10⁻², Philippines 1.19×10⁻¹, US 7.94×10⁻², UK 1.64×10⁻¹ — e.g., US MAPE 0.079 vs univariate LSTM 0.497 (≈6.3× lower). Neural SIR is best on MSFE/MAFE for all six countries.

**(f) Limitations.** In-sample one-step metrics dominate the tables (out-of-sample shown qualitatively); sensitivity to error-covariance initialization (Q, P); depends on reporting/testing quality (Brazil/Philippines show strong upward-trend bias); SIR compartment structure is fixed (no age/vaccination variants); absolute errors still large in high-count regimes (US MAFE ≈ 59,300 cases).

## B.6 SmartFall — "A Smartwatch-Based Fall Detection System Using Deep Learning"
*Mauldin, Canby, Metsis, Ngu & Cubero Rivera, Sensors 18(10):3363 (2018).*

**(a) Problem.** Detect falls from raw wrist-worn accelerometer data, in real time on-device (phone-paired), preserving privacy and avoiding cloud latency — for elderly/clinical monitoring.

**(b) Method.** Commodity smartwatch streams raw tri-axial accelerometer to a paired Android phone; a deep recurrent network trains on **raw** signals (no hand-crafted features), versus SVM/Naive Bayes trained on manually extracted acceleration features. Three-layer open IoT architecture: perception (sensors) → network (BT/phone) → application (inference/dashboard).

**(c) Datasets.** Three public fall datasets: **Smartwatch**, **Notch**, **Farseeing** (Farseeing highly imbalanced: >1,000 ADLs per fall; Notch ≈ 23 ADLs per fall). Online validation: unseen volunteers (5 subjects in real-world test).

**(d) Baselines.** Naive Bayes, SVM (both on engineered features).

**(e) Exact metrics.**

Offline (precision / recall / ADL accuracy / overall accuracy):

| Dataset | NB | SVM | Deep |
|---|---|---|---|
| Smartwatch | 0.60 / 0.92 / 0.38 / 0.65 | 0.68 / 0.86 / 0.60 / 0.73 | **0.77 / 1.00 / 0.70 / 0.85** |
| Notch | 0.58 / 0.89 / 0.97 / 0.97 | 0.53 / 0.80 / 0.97 / 0.96 | **0.79 / 0.89 / 0.99 / 0.99** |
| Farseeing | 0.005 / 0.82 / 0.87 / 0.87 | 0.44 / 0.55 / 0.99 / 0.99 | 0.37 / 1.00 / 0.99 / 0.99 |

Online (unseen volunteers): overall precision/recall/accuracy — NB 0.62/0.66/0.64; SVM 0.62/0.26/0.56; **Deep 0.64/0.86/0.70**. Fall recall by direction (Deep): back 0.84, front 0.80, left 0.96, right 0.84 (SVM: 0.20–0.28). Generalization: SVM fall detection 85.7% → 26% offline→online; NB 92.3% → 66%; Deep 100% → 86%.

**(f) Limitations.** Overall online accuracy only 70% and ADL precision weak (sitting 0.40, walking 0.56 online) → false alarms in daily life; Farseeing precision collapses under >1000:1 imbalance (NB 0.005; Deep 0.37); tiny real-time evaluation cohort (5 subjects); authors note medicine demands near-perfect reliability; single sensor modality (accelerometer only).

**Note on a 7th candidate.** IMEFD-ODCNN (Neuroquantology, 2021) — IoT-based elderly fall detection using an *optimized* deep CNN (SqueezeNet backbone optimized via variational-autoencoder-style search per subject) — is frequently cited in this space, but its reported metrics could not be verified from primary sources within this research session and it is therefore excluded from the quantitative tables.

**Section B synthesis.** Safety/health models split into three families: (i) *graph/sparse-event* forecasting (GLDNet +12–25% hit rate over deployed statistics; DeepCrime +4.5–6.1% Macro-F1 over GRU), (ii) *physics-guided rapid surrogates* (floods: NSE ≈ 0.99 stage skill, F1 ≈ 69% inundation, 19,585× speed-ups), and (iii) *on-device wearable* detection where deep learning buys generalization (86% vs 26% SVM recall) but real-world accuracy (~70%) remains deployment-limiting. Recurring lesson: operational metrics (hit rate, F1, alert recall) matter more than laboratory accuracy, and imbalance handling decides whether a model survives contact with real cities.

---

# SECTION C — URBAN VISION (5 papers)

## C.1 Cross-Scene Crowd Counting via Deep CNN
*Zhang, Li, Wang & Yang, CVPR 2015, pp. 833–841.*

**(a) Problem.** Count people in surveillance scenes *unseen during training* without per-scene manual annotation; classic domain-shift problem for city crowd monitoring.

**(b) Method.** A CNN predicts density maps; counting is integration of the map: Ñ = Σ_x D(x), with ground-truth density built from head annotations D_gt(x) = Σ_i δ(x − x_i)·G_σ(x) (Gaussian kernel per annotated head). Training is **switchable dual-objective**: alternate between density-map loss L_D and global count loss L_C = |Σ_x D(x) − N|, with scale weights **10 (density) and 1 (count)**; convergence in ≈6 switch iterations. Joint multi-task loss is outperformed by this alternating scheme. At test time, a data-driven fine-tuning step adapts the model to the target scene using retrieved similar samples (no new labels).

**(c) Dataset.** New **WorldExpo'10**: 1,132 annotated video sequences from **108 cameras** (Shanghai World Expo), **3,980 frames**, **199,923 head annotations**; train/val = 1,127 sequences from 103 scenes; test = 5 one-hour sequences from 5 unseen scenes (120 frames each, counts 1–220). Also UCSD 2,000-frame set and UCF_CC_50.

**(d) Baselines.** LBP + Ridge Regression; Fiaschi et al.; Ke et al.; Cumulative Attribute Regression; MESA/density+SIFT methods; Kernel Ridge/GPR.

**(e) Exact metrics.**

WorldExpo'10 mean absolute error per scene (average): LBP+RR **31.0**; Crowd CNN **14.1**; **fine-tuned Crowd CNN 12.9**; Fiaschi et al. 26.7; Ke et al. 16.5; Crowd CNN+RR **10.7** (scene-wise: 2.0 / 29.5 / 9.7 / 9.3 / 3.1). UCSD: Crowd CNN **MAE 1.60, MSE 3.31** vs Kernel Ridge 2.16/7.45, Ridge 2.25/7.82, GPR 2.24/7.97, CAR 2.07/6.86. On UCF_CC_50 the method reports the best MAE among compared works (baselines shown: Rodriguez et al. MAE 655.7/MSE 697.8; Lempitsky et al. 493.4/487.1).

**(f) Limitations.** Fine-tuning needs target-scene data (retrieval/labels) — weakening the "no annotation" claim; density-map supervision is annotation-costly; 2015 CNN lacks modern backbones/attention; weak on stationary crowds whose foreground segmentation fails (acknowledged by authors); error on Scene 2 remains 14.1 (scene difficulty variance).

## C.2 SaCNN — "Crowd Counting via Scale-Adaptive Convolutional Neural Network"
*Zhang, Shi & Chen, WACV 2018 (arXiv:1711.04433, Nov 2017), DOI 10.1109/WACV.2018.00127.*

**(a) Problem.** Single-column multi-scale CNNs (MCNN-style) waste capacity on fixed receptive fields; SaCNN counts with a **fixed small receptive field** backbone and adapts multi-layer features to a common output size — suited to scale-varied urban crowds and efficient inference.

**(b) Method.** Feature maps extracted from multiple depths are resized/adapted to the same output resolution and summed into the final density map (3-scale model used in main results); count = integral of density map. Two losses:
- Density loss: L_D = (1/N)Σ‖F(X_i; Θ) − D_i‖²₂
- **Relative count loss**: L_R = (1/N)Σ |(F_Y − Y_i)/Y_i| (relative error), added after density loss converges; absolute count loss (acl) is tested and found harmful (varies drastically across images).
- Metrics: MAE = (1/N)Σ|F_Y − Y_i|; MSE = sqrt((1/N)Σ(F_Y − Y_i)²).

**(c) Datasets.** ShanghaiTech **1,198 images, 330,165 people** (PartA: 482 imgs, 241,677 people, avg 501.4, max 3,139, split 300/182; PartB: 716 imgs, 88,488 people, avg 123.6, split 400/316); WorldExpo'10 (3,980 frames, 199,923 people); UCF_CC_50 (50 imgs, 63,974 people, avg 1,279.5, max 4,543); new **SmartCity** (50 images, 1920×1080, **369 people**, avg 7.4 — sparse scenes).

**(d) Baselines.** Zhang et al. [32] (CVPR 2015 cross-scene CNN), Zhang et al. [33] (MCNN, CVPR 2016), Sam et al. [25] (Switching CNN), YOLO9000 detection-counting.

**(e) Exact metrics.**

| Method | ShanghaiTech A MAE/MSE | Part B MAE/MSE |
|---|---|---|
| Zhang et al. 2015 [32] | 181.8 / 277.7 | 32.0 / 49.8 |
| MCNN [33] | 110.2 / 173.2 | 26.4 / 41.3 |
| Switching CNN [25] | 90.4 / 135.0 | 21.6 / 33.4 |
| **SaCNN** | **86.8 / 139.2** | **16.2 / 25.8** |

Other: WorldExpo'10 average **MAE 8.5**; UCF_CC_50 **MAE 314.9 / MSE 424.8** (best among compared); SmartCity SaCNN 8.6/11.6 (YOLO9000 with cs>0.05 scores 3.5/4.7 there — detection counting competitive in ultra-sparse scenes). Ablation: w/o count loss 87.4/141.7 (A) and 16.6/26.0 (B); absolute count loss *degrades* to 102.7/164.9; relative count loss best at 86.8/139.2. Speed: **293 ms vs 580 ms** per image (2× faster than Switching CNN).

**(f) Limitations.** Benchmark-era results (2016–2017) now superseded; density-map annotation cost; fixed-small-receptive-field prior breaks under extreme scale mixing (authors note combining multi-scale outputs gives limited gains on PartA); YOLO9000 beats it on ultra-sparse SmartCity; no occlusion/drift handling for video streaming.

## C.3 Multistage License Plates — "Efficient Multistage License Plate Detection and Recognition Using YOLOv8 and CNN for Smart Parking Systems"
*Safran, Alajmi & Alfarhood, Journal of Sensors 2024, Article 4917097, DOI 10.1155/2024/4917097.*

**(a) Problem.** Sensor-based smart parking is costly; replace occupancy sensors with existing surveillance cameras + a Saudi-plate-specific vision pipeline (plate formats/fonts differ globally).

**(b) Method.** Three learned stages: (1) **license-plate detection** — YOLOv5x; (2) **character detection** — YOLOv8x producing nine character boxes, ordered by box coordinates inside the plate box; (3) **character recognition** — a new compact CNN (27 classes: 17 letters + 10 Arabic digits) with dropout/regularization, lr 0.01. Evaluation metrics: mAP@0.5 and stricter mAP@0.5:0.95 (IoU 0.5→0.95 step 0.05); end-to-end plate accuracy.

**(c) Dataset.** Self-collected Saudi plates: plate detection **2,528 images** (1,769/506/253 train/val/test); character detection **1,849 images** (1,295/370/184); recognition **27,000 characters** (18,900/5,400/2,700, class-balanced). Deployment test: camera at car-park entrance → local PC (GeForce RTX 2050) → web dashboard via APIs.

**(d) Baselines.** YOLOv7x, YOLOv8x (detection stages); single-stage approach (YOLOv8x used for detection+recognition end-to-end).

**(e) Exact metrics.**

| Stage | Best model | mAP@0.5 | mAP@0.95 |
|---|---|---|---|
| Plate detection | YOLOv5x (vs v8x 0.973/0.844, v7x 0.920/0.730) | **0.994** | **0.892** |
| Character detection | YOLOv8x (vs v5x 0.978/0.819, v7x 0.977/0.711) | **0.981** | **0.827** |

Recognition CNN: accuracy **0.970**, precision 0.985, recall 0.985, F1 0.982. End-to-end on 181 test plates: detection 179/181 (98.8%) for both approaches; **full correct recognition 174/181 = 96.1%** (multistage) vs **152/181 = 83.9%** (single-stage) — **+12.2 pp**. Real-world latency **264.7 ms/frame** (incl. API transmission, redundancy buffer skipping repeated plates).

**(f) Limitations.** Single country/format; small self-collected set; 264.7 ms/frame limits multi-lane throughput; custom CNN (not CRNN/CTC) is brittle to blur/occlusion; no cross-country or night/rain stratification; mAP@0.95 drops ~10–17 pp vs mAP@0.5 (localization precision weaker than headline).

## C.4 Unified ALPR Pipeline — "Unified Deep Learning Pipeline for License Plate Recognition: From Detection to OCR with Faster R-CNN, FCN, and CRNN"
*Ganesamoorthi & Ravikumar, ICICC 2025, DOI 10.1109/ICICC66840.2025.11199678.*

**(a) Problem.** Replace every stage of ALPR (detection, segmentation, OCR) with task-specific deep models to survive blur, low light, and unconventional fonts, while keeping real-time throughput.

**(b) Method.** Faster R-CNN (plate detection) → FCN (character segmentation) → CRNN with Connectionist Temporal Classification loss (sequence recognition without explicit per-char classification): CRNN = CNN feature extractor → BiLSTM → CTC: P(π|x) = Σ_{paths mapping to π} Π_t p_t(k_t|π, x).

**(c) Dataset.** 5,000 mixed-condition roadway images.

**(d) Baselines.** YOLOv5 + Tesseract hybrid.

**(e) Exact metrics.** Detection **mAP 90.5% @ IoU 0.5**; segmentation **IoU 85.6%**; character recognition **95.2%**; **end-to-end plate accuracy 88.7%**; **≈25 FPS on NVIDIA RTX 3080**; **+8.6 pp** overall accuracy vs YOLOv5+Tesseract.

**(f) Limitations.** Single 5,000-image dataset (private, no cross-dataset test); FPS tied to high-end GPU (edge deployment unverified); detection mAP@0.5 of 90.5% is below Safran's 99.4% (different data difficulty, not directly comparable); no night/weather breakdown in reported results.

## C.5 Layout-Independent ALPR — "An Efficient and Layout-Independent Automatic License Plate Recognition System Based on the YOLO Detector"
*de Souza et al., arXiv:1909.01754 (v3, 2021).*

**(a) Problem.** Multi-region (layout/font) plate recognition in uncontrolled road scenes; avoid brittle character segmentation.

**(b) Method.** Three phases: vehicle detection → plate detection **+ layout classification in one stage** → simultaneous recognition of *all* characters on the plate patch (no segmentation), with heuristic rules conditioned on predicted layout class; YOLO-family models optimized per stage for speed/accuracy.

**(c) Dataset/annotation.** Eight public datasets across five regions (incl. ChineseLP, OpenALPR-EU, SSIG-SegPlate, UFPR-ALPR); authors annotate **38,351 bounding boxes on 6,239 images** (publicly released).

**(d) Baselines.** Prior published methods and commercial ALPR systems on the same datasets.

**(e) Exact metrics.** **96.9% average end-to-end recognition** across the eight datasets; outperforms previous works and commercial systems on ChineseLP, OpenALPR-EU, SSIG-SegPlate and UFPR-ALPR; competitive elsewhere; real-time FPS on high-end GPU even with four vehicles in scene.

**(f) Limitations.** Relies on layout-classification heuristics (new plates/layouts need relabeling); GPU-centric speed claims; per-dataset variance hidden by the 96.9% average; no edge-device benchmark.

**Section C synthesis.** Urban vision matured from density-map counting (MAE 86.8 on ShanghaiTech-A) to layout-agnostic, multi-stage deep pipelines (≥96% end-to-end plate accuracy). Cross-cutting findings: (i) task decomposition beats monolithic models (+12.2 pp in Safran's ablation), (ii) sequence models (CRNN+CTC) remove segmentation error propagation, (iii) evaluation discipline (mAP@0.5:0.95, cross-dataset tests, FPS) separates deployable systems from benchmark-only results, and (iv) every paper still struggles with the long tail: sparse scenes, blur, unseen layouts.

---

# SECTION D — LLMs & FOUNDATION MODELS (2024–2026) (8 papers)

## D.1 UrbanLLaVA — "UrbanLLaVA: A Multi-modal Large Language Model for Urban Intelligence"
*Feng, Wang, Liu, Xi & Li, ICCV 2025, pp. 6209–6219; code: github.com/tsinghua-fib-lab/UrbanLLaVA.*

**(a) Problem.** Urban research spans four heterogeneous data types — structured geospatial data, human trajectories, satellite imagery, street-view imagery — but existing MLLMs handle them piecemeal. Goal: one model with unified perception/reasoning across all four, for urban tasks.

**(b) Method.** (i) **UData**: curated urban instruction dataset covering single-modal and cross-modal tasks "from location view to global view"; (ii) **multi-stage training pipeline** (UTrain) that decouples spatial-reasoning enhancement from domain adaptation for stability/compatibility; (iii) **UBench**: 12-task benchmark reorganized/expanded from CityBench (GeoQA, trajectory prediction, navigation) and UrBench (image retrieval, camera localization, scene comparison) plus 6 new tasks (STV-address, STV-landmark, STV-outlier, SAT-address, SAT-landuse, SceneFunc) — new tasks split train/val to prevent leakage. Base: VILA1.5-8B; fine-tuned 8×A100 (lr 1e-5, max seq 2048, batch 8/GPU, 1 epoch); Beijing training on 4×A100 took 10.7 h. Eval: VLMEvalKit, temperature 0, max 1,000 output tokens; also LLaVA-Bench(In-the-Wild), RealWorldQA, MM-Vet.

**(c) Dataset/cities.** Three cities — Beijing, London, New York (spatially partitioned regions); instruction data per city; benchmark tasks per city.

**(d) Baselines.** Qwen2VL-7B/72B, InternVL2-8B/26B, VILA1.5-3B/8B/13B, LLaMA3.2-11B/90B, GPT4o-mini, GPT4o.

**(e) Exact metrics (UBench scores, Beijing — selected).**

| Task @Beijing | Best baseline (model) | UrbanLLaVA | vs best baseline | vs VILA1.5-8B |
|---|---|---|---|---|
| GeoQA | 0.5491 (Qwen2VL-72B) | 0.5682 | +3.48% | +31.47% |
| TrajPredict | 0.1611 (Qwen2VL-72B) | 0.2800 | +72.63% | +375.38% |
| Navigation | 0.24 (several) | 0.46 | +91.67% | +666.67% |
| STV-Address | 0.440 (Qwen2VL-72B) | 0.91 | +106.82% | +237.04% |
| STV-Outlier | 0.5500 (Qwen2VL-72B) | 0.8150 | +48.18% | +120.27% |
| SAT-Address | 0.395 (Qwen2VL-72B) | 0.780 | +97.47% | +246.67% |
| Image retrieval | 0.315 (GPT4o) | 0.785 | +149.21% | +302.56% |
| SceneFunc | 0.390 (GPT4o) | 0.58 | +48.72% | +68.12% |

Overall: gains over best baseline **+3.48% to +132.23%** across Beijing's five task groups; vs base model up to **+375.38%**. London: top in 9 of 12 subtasks (gains 5.17–49.38%); New York: best in 4 of 5 groups; **GeoQA is the exception** (−0.73% vs GPT4o in London, −7.37% in New York). Training data quality and the weaker 8B base explain the GeoQA gaps.

**(f) Limitations.** One training epoch per city (city-specific models, not one universal model); GeoQA still trails GPT4o outside Beijing; new benchmark tasks partly overlap training-distribution splits; no temporal/dynamic urban processes (real-time traffic, events); evaluation scores are accuracy-like but task metrics vary (Table 1 of paper); dependence on Google/proprietary base (VILA) limits full open reproduction.

## D.2 CityGPT — "CityGPT: Empowering Urban Spatial Cognition of Large Language Models"
*Feng et al., KDD 2025; arXiv:2406.13948; code: github.com/tsinghua-fib-lab/CityGPT.*

**(a) Problem.** Open LLMs lack a city-scale "world model": poor urban spatial cognition (city image, urban semantics, spatial reasoning). Inject spatial knowledge *without destroying* general capabilities.

**(b) Method.** (i) **CityInstruction**: diverse instruction-tuning dataset (knowledge QA over city imagery, POI/land-use semantics, spatial-reasoning question families — 20 question types for spatial reasoning alone, with with-context/without-context variants); (ii) **SWFT (self-weighted fine-tuning)**: weighted loss using an exponential weighting f_exp over per-sample losses to balance urban vs general data — mitigating the catastrophic forgetting seen in plain SFT; (iii) **CityEval** benchmark: City Image, Urban Semantics, Spatial Reasoning, Composite Tasks (mobility prediction, trajectory generation, navigation), single/multi-choice accuracy, 1-shot for composites. Base models: ChatGLM3-6B, Qwen2.5-7B, Llama3-8B (also Gemma2-9B baselines). Eval via vllm, temperature 0.

**(c) Cities/data.** Training instruction data from San Francisco; evaluation on **Beijing, London, New York, Paris** (out-of-domain transfer); leakage-checked evaluation sets.

**(d) Baselines.** Small: ChatGLM3-6B, Qwen2.5-7B, Llama3-8B, Gemma2-9B; large: Mistral-Small-24B, Gemma2-27B, Qwen2.5-32B/72B, Llama3.1-70B/405B; commercial: GPT-3.5, GPT-4o-mini; plus general benchmarks MMLU, GSM8K, BBH (opencompass).

**(e) Exact metrics (CityEval accuracy — Beijing).**

| Model | City Image | Urban Semantics | Spatial Reasoning |
|---|---|---|---|
| Qwen2.5-7B (base) | 0.325 | 0.587 | 0.164 |
| Llama3.1-405B (best open) | 0.417 | 0.587 | 0.414 |
| GPT-4o-mini | 0.319 | 0.533 | 0.246 |
| **CityGPT-Qwen2.5-7B** | **0.502** | **0.620** | **0.552** |
| vs base | +54.50% | +5.68% | **+236.59%** |
| vs best baseline | +20.29% | −1.07% | +33.33% |

Across all base models, CityGPT gains **148%–237%** on Spatial Reasoning. General capability (Beijing models): Qwen2.5-7B MMLU 74.15 → 74.72, BBH 66.01 → 70.03, GSM8K 80.21 → 77.18 (≈ preserved); plain SFT on Llama3-8B drops MMLU 68.33 → 56.89 and GSM8K 79.38 → 60.58, while **SWFT recovers +0.8% to +27%** over SFT on CityEval and general benchmarks combined. London/NewYork/Paris replicate the pattern (e.g., Paris CityGPT SR 0.619 vs Llama3.1-405B 0.467).

**(f) Limitations.** Urban Semantics gains are small (−1.07% vs best baseline in Beijing); GSM8K still regresses vs base even with SWFT; composite tasks use 1-shot prompting; absolute scores remain low (best baseline ceiling ≈0.63 — the benchmark is hard/noisy); city imagery/text sources bias coverage; without-context reasoning consistently weaker (memory-limited).

## D.3 PlanGPT — "PlanGPT: Enhancing Urban Planning with a Tailored Agent Framework"
*Zhu, Chen et al., ACL 2025 (Industry Track), anth ID 2025.acl-industry.54.*

**(a) Problem.** General LLMs fail professional planning workflows: text generation (proposals), style transfer across government document formats, information extraction (metrics/requirements), document evaluation, plus retrieval over regulation corpora.

**(b) Method.** **PlanAgent** orchestrates four components: **PlanRAG** (domain-aware retrieval over a custom local database; includes Plan-Emb semantic embeddings), **WebLLM** (real-time regulation search via orienting URL crawlers), **PlanLLM** (knowledge activation via targeted instruction synthesis / Plan-Annotation fine-tuning), **ToolLLM** (function-calling for spatiotemporal analysis, urban simulation, knowledge-graph construction, reverse geocoding, TOD analysis, digital-twin platforms) + custom reward models trained on planner feedback for response ranking. Implementation is China-specific (regulations, document styles).

**(c) Evaluation suites.** (i) Offline: **PlanBench** (Bloom's revised taxonomy, 4 categories / 24 classes / 81 subcategories, Content-Validity-Index confirmed). (ii) Online: 4 professional tasks judged by 4 human planners + PlanEval (LLM judge); knowledge tests: C-Eval urban-planning subset **v1 = 418 questions** + curated **v2 = 3,500** Chinese Registered Urban Planner exam questions.

**(d) Baselines.** ChatGLM3-6B, Yi-6B, Baichuan2-13B-Chat, ChatGPT, GPT-4, Qwen/Llama3/Gemma/DeepSeek-R1 families on PlanBench.

**(e) Exact metrics.**

| Model | Text Gen (Human) | Style Transfer (Human) | Info Extraction (Acc) | Text Evaluation (Acc / F1) |
|---|---|---|---|---|
| ChatGLM3-6B | 41.33 | 67.00 | 50.00 | 25.67 / — |
| ChatGPT | 58.0 | 70.67 | 31.00 | 21.30 / — |
| Baichuan2-13B | 34.00 | 39.33 | 33.00 | 17.42 / — |
| **PlanGPT** | **86.67** (PlanEval 60.33) | **80.00** (PlanEval 66.80) | **65.18** | **41.00 / 35.28** |

Knowledge test: PlanLLM v1 63.0 / v2 51.2 / **avg 57.1**, δ = 0.812 vs GPT-4 (59.3 avg, δ 0.875), ChatGPT 47.1, ChatGLM3 52.7 — ≈5% accuracy gain over base. PlanRAG ablation: direct ChatGLM3-6B 48.8 → raw search 48.6 → +PlanEmb 49.3 → **full PlanRAG 52.2** (+3.6 over raw search); PlanEval shows **79% Spearman correlation** with human scores.

**(f) Limitations.** China-only regulation/document scope; online human evaluation rests on four planners; PlanGPT's text-generation PlanEval (60.33) lags its human score (86.67) — judge–human gap; text evaluation accuracy still only 41%; Yi-6B baseline completion failure (10.8%) skews comparisons; no English/cross-jurisdiction generalization reported.

## D.4 OmniGeo — "OmniGeo: Towards a Multimodal Large Language Model for Geospatial Artificial Intelligence"
*Yuan, Mo, Huang et al., arXiv:2503.16326 (20 Mar 2025; under review, 15 pp.).*

**(a) Problem.** GeoAI spans geospatial semantics, health geography, urban geography, urban perception and remote sensing; existing LLMs/MLLMs handle text and images but not *spatial* reasoning over heterogeneous sources jointly.

**(b) Method.** A geospatial-tailored MLLM processing satellite imagery, geospatial metadata and textual descriptions; instruction-following training designed to strengthen spatial reasoning; evaluated in zero-shot settings against task-specific models and general LLMs. Data sources underlying the GeoAI task suites include crowdsourced text (tweets/web), CDC Wonder polygon statistics, Gaode POIs, WorldView remote-sensing imagery and Google street-view imagery.

**(c) Tasks/scale.** Five domain groups (Geospatial Semantics, Health Geography, Urban Geography, Urban Perception, Remote Sensing); code promised upon publication.

**(d) Baselines.** Task-specific GeoAI models and general-purpose LLMs/MLLMs (per-task comparisons).

**(e) Reported results.** Authors report that OmniGeo **outperforms task-specific models and existing LLMs across diverse geospatial tasks** and achieves **competitive zero-shot** performance (abstract-level claims; fine-grained per-task tables are in the under-review full text — not quoted here to avoid transcription error).

**(f) Limitations.** Under review at time of writing — no peer-reviewed numbers yet; code not released; zero-shot competitiveness ≠ production accuracy; benchmark construction (and possible train/test contamination with public geo corpora) requires scrutiny.

## D.5 ChatGPT for Citizen Feedback — "Deciphering Public Voices in the Digital Era: Benchmarking ChatGPT for Analyzing Citizen Feedback in Hamilton, New Zealand"
*Fu, Sanchez, Li & Reu Junqueira, Journal of the American Planning Association 90(4) (2024) 728–741, DOI 10.1080/01944363.2024.2309259.*

**(a) Problem.** Municipalities receive huge volumes of text public feedback (e.g., Hamilton City Council Plan Change 12, 2022); manual coding of summaries, topics, stances and sentiment is slow. Can zero-shot LLM prompting match planners and standard NLP?

**(b) Method.** Zero-shot prompts for three tasks — summarization (reasons, decisions sought), topic identification, sentiment analysis — benchmarked against (i) human planners, (ii) LDA topic modeling, (iii) lexicon-based sentiment analysis; few-shot variant tested for jargon-heavy tasks. Accuracy = agreement with the true feedback content; convergence = agreement with human planners.

**(c) Dataset.** Online public submissions, Hamilton, NZ, 2022 Plan Change 12 (district-plan housing rules).

**(d) Baselines.** Human planners; LDA; lexicon sentiment.

**(e) Exact metrics.** Zero-shot accuracy: **political stance 81.7%, reasons 87.3%, decisions sought 85.8%, sentiment 94.1%**; few-shot sentiment rises **+3.1 pp to 97.2%**. Convergence with planners: stance 71.2%, reasons 84.6%, decisions 79.2%, topics 56.0%. Versus NLP: ChatGPT sentiment 94.1% vs lexicon **55.8%** (agreement between ChatGPT and lexicon only 49.9%); topic ID ChatGPT **64.2%** vs LDA **42.6%**, with both fully wrong ≈24.6% of submissions. Few-shot gains were marginal except for jargon-heavy topics. (Context: same team's earlier "Can ChatGPT Evaluate Plans?", JAPA 2023 — 10 climate plans, **68% average agreement** with manual content analysis.)

**(f) Limitations.** Single city/one plan change; prompt sensitivity; training-data bias; overgeneralization and omission of nuance; topic identification remains weak (64.2%); human review mandatory per authors' practice recommendation.

## D.6 LLM × Urban Digital Twin — "Bridging Natural Language and Urban Digital Twins: An LLM Assistant for Geospatial Queries"
*Kanna & Kolbe, ISPRS Annals X-G-2025-469-476, DOI 10.5194/isprs-annals-x-g-2025-469-2025 (2025); repo: github.com/tum-gis/ai_assistant_queries.*

**(a) Problem.** Urban Digital Twins (CityGML/3DCityDB + sensor platforms) are queryable only via expert languages; non-expert city staff cannot interrogate the twin.

**(b) Method.** LLM assistant translating **natural language → structured queries**: SQL over 3DCityDB (CityGML semantic 3D city models) and OGC **SensorThings API** requests for live sensor streams; prompt-pipeline handles schema grounding, query generation and result narration; tool orchestration around the twin's APIs.

**(c) Scope.** CityGML/3DCityDB-based twin + SensorThings sensor platform (demonstrator built at TUM); open repository of assistant queries.

**(d)/(e) Baselines & metrics.** Evaluation is demonstrator/task-completion based (qualitative query success and case studies) rather than a standardized numeric benchmark — the paper reports no headline accuracy/F1 table; its contribution is the integration architecture.

**(f) Limitations.** No quantitative LLM benchmark; correctness depends on schema-grounding prompts (hallucinated SQL risk); single-twin configuration; no latency/cost analysis; semantic 3D queries remain constrained to what SQL over CityGML can express.

## D.7 IBM Geospatial Foundation Model — "Detection and Simulation of Urban Heat Islands Using a Fine-Tuned Geospatial Foundation Model for Microclimate Impact Prediction"
*Fleckenstein, Kreismann, Govindasamy, Brunschwiler, Vos & Rigotti, NeurIPS 2025 (workshop); arXiv:2510.18773 / 2509.16617.*

**(a) Problem.** Cities lack dense air-temperature data (esp. underserved areas); conventional ML trained on local data fails to generalize. Can a geospatial foundation model (GFM) detect UHI, forecast under future climate, and simulate mitigation?

**(b) Method.** **Granite-GFM (Land-Surface-Temperature)**: SWIN Transformer built on Prithvi-SWIN-L Earth-Observation FM, producing LST at **30 m spatial, hourly temporal** resolution. V1 fine-tuned on HLS L30 + ERA5-Land (2013–2023, **28 cities**); V2 on extended **52 cities** across hydro-climatic zones. Three experiments: (i) empirical ground truth — park cooling gradients from LULC × LST overlays (summer daytime 2017–2025); (ii) extrapolation — Brașov, Romania (unseen city): fine-tune on coolest 90%, test on hottest 10%, then swap ERA5 → EURO-CORDEX RCP 2.6/4.5/8.5 inputs for 2030/2050/2100 projections; (iii) mitigation — guided **inpainting** of satellite imagery (built-up pixels → green pixels, NDVI adjusted) to simulate cooling.

**(c) Dataset.** Multi-city LULC + HLS/ERA5 (training); Brașov held-out; all-city summer-daytime aggregates 2017–2025.

**(d) Baselines.** Model V1 vs V2; Baseline vs Random-Split vs High-Heat training configurations.

**(e) Exact metrics.** Empirical UHI: **+3.3 °C** average in dense cores; internal park cooling up to **−2.6 °C within 200 m**; spillover cooling up to **−3.5 °C** near parks (≈ −1 °C at 150 m). Cooling-replication accuracy: internal-cooling MAE V1 **0.240 °C** → V2 **0.231 °C**; spillover MAE V1 **0.302 °C** → V2 **0.199 °C** (RMSE 0.339 → 0.243). Extrapolation: Brașov 90th-percentile 23.29 °C, model predicts to **26.91 °C** (**+3.62 °C beyond training range**) at **MAE 1.74 °C**; V2 high-heat MAE 1.74 vs random-split 1.77 and baseline 2.81 (V2 config).

**(f) Limitations.** LST ≠ air temperature (UHI alerts need air T); single held-out extrapolation city; extrapolation limit asserted at the 10% threshold (assumption-driven); inpainting simulation is counterfactual (no causal validation against a real greening intervention); RCP projections inherit EURO-CORDEX biases.

## D.8 Survey — "A Genealogy of Foundation Models in Remote Sensing"
*arXiv:2504.17177v2 (2025).*

**(a) Problem.** Track the design lineage of remote-sensing foundation models that increasingly power urban monitoring (land use, change detection, heat, flood).

**(b) Method/content.** Taxonomy of pretraining strategies — masking objectives (masked image modelling à la SatMAE), seasonal/temporal contrast (SeCo), geospatial/spectral pretraining (NASA-IBM Prithvi) — plus data, scale, and downstream adaptation patterns; framework: self-supervised pretraining on large RS corpora → task fine-tuning.

**(c) Scope.** Literature-level survey across the RS-FM family (SatMAE, SeCo, Prithvi and successors), not an experimental paper.

**(d)/(e) Baselines & metrics.** No original experiments/metrics; its value is comparative architecture/lineage mapping used to choose backbones (e.g., Prithvi → IBM's Granite-GFM in D.7).

**(f) Limitations.** Snapshot of a fast-moving area (cutoff 2025); no standardized benchmark comparison; limited coverage of MLLM-based geo-models (OmniGeo, UrbanLLaVA lines).

**Section D synthesis.** The 2024–2026 wave shows three patterns: (1) *urban specialization of small open models* beats bigger general models on urban tasks — CityGPT-7B's spatial reasoning +236.59% over its base and +33.33% over Llama3.1-405B; UrbanLLaVA-8B beats GPT4o on most cross-modal urban tasks while trailing on pure GeoQA; (2) *agents + retrieval* (PlanGPT) convert LLMs into workflow tools with measurable human-rated gains (86.67 text-gen score), but extraction/evaluation accuracy (65.18%/41.00%) remains the bottleneck; (3) *foundation models move from benchmarks to physics-grounded simulation* (IBM Granite-GFM: 0.199 °C spillover MAE, +3.62 °C extrapolation). Human-in-the-loop caution persists (Fu 2024: 94.1% sentiment but 64.2% topic accuracy).

<!-- SECTION-E-MARKER -->
