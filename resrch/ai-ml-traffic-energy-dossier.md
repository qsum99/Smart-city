# AI/ML Research Dossier: Deep Learning for Smart-City Traffic & Mobility and Energy Systems

**Scope.** A technical research dossier (no code) surveying the most influential and most recent AI/ML papers in two smart-city domains: (A) Traffic & Mobility forecasting, and (B) Energy forecasting, EV-charging management, and building/load analytics. For each paper the dossier records the problem formulation, the architectural design with its governing equations, the datasets and baselines used, the exact reported error metrics (MAE / RMSE / MAPE), and the ablations or limitations reported by the authors. A final section traces the methodological evolution from CNNs to graph networks to adaptive-graph models to transformers to foundation models, and consolidates the traffic results into a single comparison table.

**Metric conventions.** All traffic papers use 5-minute sampling unless noted; horizons are typically 15/30/60 min (12-step input → 12-step output for multi-step protocols). MAE = mean absolute error, RMSE = root mean squared error, MAPE = mean absolute percentage error (reported as a percentage). For grid-based (taxi/bike) datasets, MAPE is computed only on samples above a flow threshold (typically 10, or 5 for CHIBike), following DMVST-Net's protocol.

---

# Section A — Traffic & Mobility (13 papers)

## A.1 ST-GCN: Spatio-Temporal Graph Convolutional Networks (Yu, Yin & Zhu, IJCAI 2018)

**Problem.** Traffic forecasting on a road network modeled as a graph 𝒢 = (𝒱, ℰ, **A**) with N sensors (nodes) and a weighted adjacency **A** (from road-network distance). Given X₁ₜ ∈ ℝᴺˣᶜ for T past frames, the model must predict the next T′ frames. ST-GCN was the first work to cast traffic forecasting as learning on a spatial graph *and* a temporal sequence simultaneously, rather than treating sensor data as a plain image or an independent set of time series.

**Architecture — the ST-Conv "sandwich" block.** The core is a spatio-temporal convolution block consisting of two temporal gated convolution layers sandwiching one spatial graph-convolution layer:

1. **Graph convolution (spatial layer).** ST-GCN adopts the Chebyshev spectral graph convolution of Defferrard et al.: with **L** = **I**ₙ − **D**⁻¹ᐟ²**AD**⁻¹ᐟ² the normalized graph Laplacian, the convolution of a signal X ∈ ℝᴺˣᵀ with filter g_θ is approximated by a K-order polynomial

   g_θ ∗_𝒢 X ≈ Σ_{k=0}^{K−1} θ_k **L**ᵏ X,

   where **L**ᵏ is computed recursively (**L**⁰ = **I**, **L**ᵏ = 2**L·L**^{k−1} − **L**^{k−2} for k ≥ 2), giving complexity O(K|ℰ|) per layer instead of O(N²). The spatial layer stacks multiple such graph-convolution channels with non-linear gating.

2. **Temporal gated convolution.** Temporal dynamics are captured by a 1-D convolution along the time axis with a **gated linear unit** (GLU): for input Z ∈ ℝ^{T×d}, the gate is

   Γ(Z) = σ(Z₁) ⊙ Z₂,

   where Z₁, Z₂ are two stacked convolution outputs and ⊙ denotes element-wise multiplication. This lets the network open/close information flow per feature channel, replacing the recurrence of LSTMs with a parallel, non-autoregressive operator.

3. **Block composition.** A full ST-Conv block is Temporal-GLU → Spatial-GCN → Temporal-GLU with residual connections, followed by batch normalization. Stacking B blocks and appending a fully connected output layer yields the prediction. The receptive field grows linearly with B in time and with K·B hops in space.

**Datasets & baselines.** Four public traffic datasets: PeMSD4, PeMSD8, PeMSD3, PeMSD7 (California PeMS, 5-min flow), plus a speed dataset. Baselines: historical average (HA), ARIMA, VAR, LSTM, GRU, STGCN-without-gate (GLU-STGCN), and GeoMAN.

**Exact results.** On the *average performance over the next hour* reported in the original AAAI'19 companion study of ASTGCN (which re-implemented STGCN under an identical protocol), STGCN obtains **PeMSD4: RMSE 38.29, MAE 25.15** and **PeMSD8: RMSE 27.87, MAE 18.88**, versus HA (54.14/36.76 and 44.03/29.52) and LSTM (45.82/29.45 and 36.96/23.18). Under the MAGCRN (2023) 12-horizon average protocol, STGCN scores **PeMSD4 MAE 22.70 / RMSE 35.55 / MAPE 14.59%** and **PeMSD7 MAE 25.38 / RMSE 38.78 / MAPE 11.08%**. On METR-LA/PeMS-BAY (7:1:2 split), STAEformer's 2023 re-evaluation reports STGCN at **METR-LA 15 min: MAE 2.75, RMSE 5.29, MAPE 7.10%; 30 min: 3.15/6.35/8.62%; 60 min: 3.60/7.43/10.35%** and **PeMS-BAY 15 min: 1.36/2.88/2.86%; 30 min: 1.70/3.84/3.79%; 60 min: 2.02/4.63/4.72%**.

**Limitations.** The adjacency **A** is fixed and hand-built from road distances; the model cannot express time-varying correlations (e.g., morning-peak vs. off-peak dependencies), and the K-hop polynomial limits long-range spatial message passing.

## A.2 DCRNN: Diffusion Convolutional Recurrent Neural Network (Li, Yu, Shahabi & Liu, ICLR 2018)

**Problem.** Data-driven traffic forecasting formulated as a **seq2seq** learning problem: an encoder reads T historical frames of N nodes and a decoder autoregressively emits T′ future frames, with a scheduled-sampling curriculum that reduces train/test mismatch.

**Architecture — diffusion convolution.** The key innovation replaces spectral graph convolution with a **diffusion convolution** operator that explicitly models information propagating forward and backward along the graph. With **A**ₙ the row-normalized adjacency, the forward/backward diffusion are the finite truncations of the random-walk operators:

**W**_f = Σ_{k=0}^{K−1} θ_{k,f} (**A**ₙ)ᵏ,  **W**_b = Σ_{k=0}^{K−1} θ_{k,b} (**Ā**ₙ)ᵏ,

where **Ā**ₙ is the column-normalized adjacency (reverse direction) and θ_{k,f}, θ_{k,b} are learnable parameter vectors. The diffusion convolution of hidden state H with W is X ∗_𝒢 H = **W**_f H **W**^{h}_{f,1} + **W**_b H **W**^{h}_{b,1} (per feature channel). Inside each GRU cell, the recurrent update is replaced by the diffusion-convolutional gated recurrent unit (DCGRU):

r_t = σ(Θ_r ∗_𝒢 [H_{t−1}, X_t] + b_r),
z_t = σ(Θ_z ∗_𝒢 [H_{t−1}, X_t] + b_z),
H̃_t = tanh(Θ_h ∗_𝒢 [r_t ⊙ H_{t−1}, X_t] + b_h),
H_t = (1 − z_t) ⊙ H_{t−1} + z_t ⊙ H̃_t.

**Training.** Seq2seq with scheduled sampling: the decoder's ground-truth input is replaced by its own prediction with probability p that decays exponentially from 1.0 to 0.1 over training.

**Datasets.** METR-LA (207 loop detectors, Los Angeles freeways, 3/2012–6/2012) and PeMS-BAY (325 Bay-Area sensors, 1/2017–5/2017), both 5-min speed data, 7:1:2 splits, 12-step input → 12-step output.

**Exact results (original paper).** METR-LA, MAE / RMSE / MAPE:

| Model | 15 min | 30 min | 60 min |
|---|---|---|---|
| ARIMA | 3.99 / 8.21 / 9.60% | 5.15 / 10.45 / 12.70% | 6.90 / 13.23 / 17.40% |
| FC-LSTM | 3.44 / 6.30 / 9.60% | 3.77 / 7.23 / 10.90% | 4.37 / 8.69 / 13.20% |
| **DCRNN** | **2.77 / 5.38 / 7.30%** | **3.15 / 6.45 / 8.80%** | **3.60 / 7.60 / 10.50%** |

On PeMS-BAY, DCRNN reports **15-min MAE 1.38** (with correspondingly lower RMSE/MAPE than all baselines at every horizon). DCRNN's 60-min MAE of 3.60 on METR-LA was the benchmark to beat for three years.

**Ablations/limitations.** The authors ablate diffusion order K (best at K = 2) and show scheduled sampling contributes materially at long horizons. Limitation: the adjacency is static, and the recurrent decoder is sequential, limiting training throughput.

## A.3 Graph WaveNet for Deep Spatial-Temporal Graph Modeling (Wu, Pan, Long, Jiang & Zhang, IJCAI 2019)

**Problem.** Learn both the spatial structure *and* the temporal dynamics of traffic from data alone, without relying on a pre-defined adjacency matrix, and do so with a fully convolutional (non-recurrent) architecture for efficiency.

**Architecture.** Three ingredients:

1. **Adaptive dependency matrix.** Two learnable node embeddings **E**₁, **E**₂ ∈ ℝ^{N×d} generate an adjacency that is optimized end-to-end:

   **Ã**_adp = SoftMax(ReLU(**E**₁ **E**₂ᵀ)) ∈ ℝ^{N×N}.

   This is the paper's Eq. (5) — a dynamic, dataset-specific graph that is not constrained by road distance.

2. **Graph WaveNet block (gated temporal convolution + diffusion conv).** The spatial operator extends the diffusion convolution with both the pre-defined graph **A** (if available) and the adaptive matrix:

   **Z** = Σ_{k} ( (**A**ₙ + **Ã**ₙ)^k X **W**^{k}_{f,1} + (**Ā**ₙ + **Ã**ₙᵀ)^k X **W**^{k}_{b,1} ) + X **W**^{k}_3,   (Eq. 6)

   where the last term injects the adaptive component **Ã**. The temporal operator is a **gated temporal convolution** with dilated causal convolutions: input X is split into two branches, Γ = σ(C₁ ∗ X) ⊙ φ(C₂ ∗ X), so the gate controls how much of the dilated history passes to the next layer. Residual connections and skip connections feed a final 1×1 convolution that maps to the T′ output steps (direct multi-step prediction).

3. **Depthwise-separable structure** keeps parameters small: each layer mixes channels with 1×1 convolutions before the graph/temporal ops.

**Datasets & baselines.** METR-LA, PeMS-BAY; baselines HA, ARIMA, FC-LSTM, STGCN, DCRNN, STGCN-GRU variants.

**Exact results.** As re-reported under the STAEformer protocol (Table 1), Graph WaveNet achieves **METR-LA: 15 min MAE 2.69 / RMSE 5.15 / MAPE 6.99%; 30 min 3.08/6.20/8.47%; 60 min 3.51/7.28/9.96%** and **PeMS-BAY: 15 min 1.30/2.73/2.71%; 30 min 1.63/3.73/3.73%; 60 min 1.99/4.60/4.71%**. On the 12-horizon-average PeMS benchmark (STAEformer Table 3): **PeMS04 18.53/29.92/12.89%**, **PeMS07 20.47/33.47/8.61%**, **PeMS08 14.40/23.39/9.21%** (MAE/RMSE/MAPE). The original IJCAI paper reports comparable METR-LA 60-min MAE ≈ 3.53 with MAPE ≈ 10.01%.

**Ablations/limitations.** Removing the adaptive matrix degrades accuracy on datasets where the road graph is noisy or incomplete; the block is shallow (typically 4 layers), so very long-range temporal patterns rely on dilation rather than recurrence. Note the adaptive matrix is still *static across time* — learned once, applied at all hours.

## A.4 ASTGCN: Attention Based Spatial-Temporal Graph Convolutional Networks (Guo, Lin, Feng, Song & Wan, AAAI 2019)

**Problem.** Traffic flow exhibits three temporal components — **recent**, **daily-periodic**, and **weekly-periodic** dependencies — and the spatial correlation between detectors changes dynamically. ASTGCN models all three explicitly rather than hoping a single hidden state captures them.

**Architecture — three parallel ST blocks.** The input sequence is split into three components (recent window of P frames, daily window of Q_d frames sampled at the same time-of-day one day earlier, weekly window of Q_w frames one week earlier). Each component is processed by an independent **spatio-temporal block**:

1. **Spatial attention.** At time slice t, the attention over nodes is

   e_{ij}^t = LeakyReLU(**a**^T [**W**_s x_i^t ‖ **W**_s x_j^t]),   α_{ij}^t = softmax_j(e_{ij}^t),

   with learnable attention vector **a**; the attended neighborhood of node i is h_i = Σ_j α_{ij}^t (**W**_s x_j^t). This yields a *different adjacency per time slice*.

2. **Temporal attention.** Analogously across time: e_{ij} over time slices with attention vector **a**′, giving β_{ij} = softmax_j(e_{ij}) and the temporally weighted history.

3. **Spatial-temporal convolution.** A graph convolution (first-order Chebyshev on the *attention-weighted* adjacency) followed by a standard 2-D temporal convolution extracts joint features; a fully-connected layer maps to the component's prediction.

4. **Fusion.** The three components' outputs are combined with learnable weights:

   Ŷ = W_r · Ŷ_recent + W_d · Ŷ_daily + W_w · Ŷ_weekly,

   where W_r, W_d, W_w are learned (component-wise) fusion coefficients. A simpler additive variant (MSTGCN) is also evaluated.

**Datasets & baselines.** PeMSD4, PeMSD8 (AAAI'19 protocol, average over the next hour); baselines HA, ARIMA, VAR, LSTM, GRU, STGCN, GLU-STGCN, GeoMAN.

**Exact results (original paper, Table 1 — average over next hour).**

| Model | PeMSD4 RMSE | PeMSD4 MAE | PeMSD8 RMSE | PeMSD8 MAE |
|---|---|---|---|---|
| HA | 54.14 | 36.76 | 44.03 | 29.52 |
| ARIMA | 68.13 | 32.11 | 43.30 | 24.04 |
| VAR | 51.73 | 33.76 | 31.21 | 21.41 |
| LSTM | 45.82 | 29.45 | 36.96 | 23.18 |
| GRU | 45.11 | 28.65 | 35.95 | 22.20 |
| STGCN | 38.29 | 25.15 | 27.87 | 18.88 |
| GeoMAN | 37.84 | 23.64 | 28.91 | 17.84 |
| MSTGCN | 35.64 | 22.73 | 26.47 | 17.47 |
| **ASTGCN** | **32.82** | **21.80** | **25.27** | **16.63** |

ASTGCN beats STGCN by ~13% MAE on PeMSD4 and ~12% on PeMSD8, and its advantage widens at longer horizons (Fig. 6 of the paper). Under the later MAGCRN 12-horizon-average protocol, ASTGCN(r) scores **PeMSD4 MAE 22.93 / RMSE 35.22 / MAPE 16.56%** and **PeMSD7 24.01/37.87/10.73%** — competitive with, but not better than, adaptive-graph models.

**Ablations/limitations.** The three components and both attention modules are each validated by removal; the weekly component matters most on holiday-adjacent weeks. Limitation: the attention parameters are shared across all hours, and the fusion is a linear weighted sum — the model has no mechanism for event-driven (incident) dynamics.

## A.5 T-GCN: A Temporal Graph Convolutional Network (Zhao, Song, Zhang et al., IEEE T-ITS 2020; arXiv 1811.05320)

**Problem.** Capture both short-term and long-term temporal dependencies *and* spatial correlations in a single, lightweight model — an explicit alternative to stacking CNN and RNN separately.

**Architecture.** A two-layer design: **GCN for spatial** + **GRU for temporal**. At time t the graph convolution

H_t = σ( **Â** X_t **W** )

propagates information over the road graph (Â = D̃⁻¹ᐟ²ÃD̃⁻¹ᐟ², Ã = A + I), and the sequence (H₁,…,H_T) is fed to a GRU whose hidden state h_t = (1 − z_t) ⊙ h_{t−1} + z_t ⊙ h̃_t with gates z_t, r_t computed from [h_{t−1}, H_t]. The final hidden state is projected to the T′-step forecast. Because GCN is applied per frame before recurrence, the spatial structure is reused at every step, giving O(|ℰ|) spatial cost per step.

**Datasets & baselines.** METR-LA, PeMS-BAY, plus a Shenzhen taxi-hailing dataset; baselines ARIMA, SVR, FC-LSTM, STGCN, DCRNN, Graph WaveNet.

**Exact results.** T-GCN reports METR-LA 15/30/60-min MAE of **2.88 / 3.14 / 3.60** and RMSE **5.74 / 6.38 / 7.35**, competitive with DCRNN (3.60/7.60 at 60 min) at a fraction of the parameters, and outperforms FC-LSTM (4.37/8.69) at 60 min by 17.6% MAE. On PeMS-BAY it reports 60-min MAE ≈ 2.19 versus DCRNN's 2.05 — i.e., slightly behind DCRNN but ahead of STGCN. The Shenzhen ride-hailing experiment shows T-GCN generalizing to *demand* (pickup counts) rather than speed.

**Ablations/limitations.** Removing either the GCN (→ plain GRU) or the GRU (→ per-step GCN + linear head) degrades accuracy by 8–14%, confirming both spatial and temporal operators are load-bearing. Limitation: a single GRU hidden state is asked to carry both recent and weekly patterns; the model has no explicit periodicity handling.

## A.6 GMAN: A Graph Multi-Attention Network (Zheng, Fan, Wang & Qi, AAAI 2020)

**Problem.** Long-horizon (up to 60 min) traffic prediction where (i) spatial correlations are dynamic, (ii) temporal dependencies include long-range periodic effects, and (iii) encoder-decoder information needs a *direct* path from history to every future step rather than sequential decoding.

**Architecture.** An **encoder–decoder** of L spatio-temporal attention blocks:

1. **Spatial attention block.** For each time slice, compute Q, K, V from node features and apply self-attention across nodes with a masked softmax restricted to the K nearest neighbors (by road distance), giving dynamic per-slice adjacency:

   A_t^{sp} = softmax( Q_t K_t^T / √d + M ),  Z_t^{sp} = A_t^{sp} V_t,

   where M is a −∞ mask outside the K-hop neighborhood.

2. **Temporal attention block.** For each node, self-attention across the T input slices with a similar local mask, capturing multi-scale periodicity.

3. **Transform attention layer.** The key GMAN-specific module: it *directly* aligns each historical slice to each future slice with a learned attention matrix

   A^{tr} = softmax( Q_f K_h^T / √d ),

   applied between encoder outputs and decoder queries, so information bypasses the sequential bottleneck. Residual connections, layer norms, and position-wise FFNs complete each block.

**Datasets & baselines.** METR-LA, PeMS-BAY; baselines HA, ARIMA, FC-LSTM, STGCN, DCRNN, Graph WaveNet, STSGCN, STGODE.

**Exact results.** Under the STAEformer protocol: **METR-LA 15 min 2.80/5.55/7.41%; 30 min 3.12/6.49/8.73%; 60 min 3.44/7.35/10.07%** (MAE/RMSE/MAPE) — note the 60-min MAE of **3.44** is better than DCRNN's 3.54 in the same table, making GMAN the strongest classic baseline at long horizons. **PeMS-BAY: 15 min 1.35/2.90/2.87%; 30 min 1.65/3.82/3.74%; 60 min 1.92/4.49/4.52%**. On the 12-horizon PeMS averages: **PeMS04 19.14/31.60/13.19%**, **PeMS07 20.97/34.10/9.05%**, **PeMS08 15.31/24.92/10.13%** (PDFormer Table 2). On grid data (PDFormer Table 3), GMAN reports NYCTaxi inflow MAE 14.267, T-Drive inflow 19.244, CHIBike inflow 4.115.

**Ablations/limitations.** Removing the transform-attention layer is the most damaging ablation (≈ +6% MAE at 60 min), since the encoder-decoder bottleneck otherwise forces all information through a single hidden state. Computational cost is high: PDFormer's efficiency study measures GMAN at **501.6 s training / 38.8 s inference per epoch on PeMS04**, versus 133.9/8.1 for PDFormer.

## A.7 AGCRN: Adaptive Graph Convolutional Recurrent Network (Bai, Yao, Li, Wang & Wang, NeurIPS 2020)

**Problem.** The road graph is only *one* of several latent graphs that govern traffic; node-specific dynamics require node-adaptive parameterization rather than shared weights.

**Architecture.** Two coupled innovations:

1. **Node-adaptive parameter learning.** For each node v, a learnable node embedding **e**_v generates *its own* weight matrices:

   W_v = MLP(**e**_v) ∈ ℝ^{d×d'}.

   Because each node gets dedicated convolution/GRU parameters, nodes with different roles (highway vs. arterial vs. ramp) specialize.

2. **Adaptive adjacency learning.** The graph itself is generated from node embeddings:

   **Ã** = SoftMax( ReLU(**E**_a **E**_bᵀ) ),

   with **E**_a, **E**_b ∈ ℝ^{N×d} learned jointly with the model — no road network input is required.

3. **AV-GCRN cell.** The adaptive graph convolution and the GRU are fused: the hidden-state update uses the node-adaptive weights on the adaptive graph, i.e., a per-node GCRU whose transition matrices are functions of **e**_v and whose adjacency is **Ã**.

**Datasets & baselines.** PeMSD4, PeMSD8, PeMSD3, PeMSD7, PeMSD7(M), and METR-LA/PeMS-BAY; baselines HA (PeMSD4 MAE 38.03 / RMSE 59.24 / MAPE 27.88%; PeMSD8 34.86/52.04/24.07%), ARIMA, VAR, STGCN, STSGCN, ASTGCN, DCRNN, Graph WaveNet, MTGNN.

**Exact results.** AGCRN reports **>5% relative improvement over the best baseline on average** across the five PeMS datasets. Under the 12-horizon-average protocol (MAGCRN Table 2): **PeMSD4 MAE 19.83 / RMSE 32.26 / MAPE 12.97%**, **PeMSD7 21.43/35.49/9.03%**, **PeMSD8 15.95/25.22/10.09%** — beating STGCN (22.70/35.55/14.59% on PeMSD4) and ASTGCN (21.96/34.64/15.12%). Under the STAEformer METR-LA protocol: **15 min 2.85/5.53/7.63%; 30 min 3.20/6.52/9.00%; 60 min 3.59/7.45/10.47%**; **PeMS-BAY 15 min 1.35/2.88/2.91%; 30 min 1.67/3.82/3.81%; 60 min 1.94/4.50/4.55%**.

**Ablations/limitations.** Replacing the adaptive adjacency with the road graph, or the node-adaptive weights with shared weights, each costs 3–7% MAE. Limitation: node embeddings are static, so the "adaptive" graph does not vary with time-of-day; the model also cannot ingest external graphs (e.g., metro lines).

## A.8 MTGNN: Connecting the Dots — Multivariate Time Series Forecasting with Graph Neural Networks (Wu, Pan, Long, Jiang, Chang & Zhang, KDD 2020)

**Problem.** Multivariate time series (including traffic) are coupled through *unknown* cross-variable dependencies; the graph must be inferred jointly with forecasting, and the model must handle both temporal and cross-series structure in a single scalable architecture.

**Architecture.**

1. **Graph structure learning via mix-hop propagation.** A learnable adjacency **A**_g is combined with a *mix-hop* diffusion that aggregates multiple orders simultaneously:

   **H**^{(l+1)} = σ( Σ_{k=0}^{K} (**A**_g)^k **H**^{(l)} **W**^{(k)} ),

   where **A**_g = SoftMax(ReLU(**E**₁**E**₂ᵀ)) — the same adaptive-adjacency construction later popularized by Graph WaveNet — and each hop k has its own weight matrix **W**^{(k)}. Dilated causal convolutions in the temporal branch expand the receptive field exponentially (dilations 1, 2, 4, …).

2. **Gated temporal convolutions** (as in Graph WaveNet) and **input/hidden graph convolutions** at every layer; a final 1×1 convolution produces the T′-step forecast directly.

3. The graph is *shared across layers* but the mix-hop weights differ per layer, letting shallow layers model fine-grained local coupling and deep layers model global coupling.

**Datasets & baselines.** Eight multivariate benchmarks including PeMSD3/4/7/8, METR-LA, PeMS-BAY, Traffic (963 sensors), Electricity, Exchange; baselines ARIMA, VAR, LSTNet, STGCN, DCRNN, Graph WaveNet, ASTGCN.

**Exact results.** MTGNN is the best overall GNN on the PeMS benchmarks in PDFormer's re-evaluation: **PeMS04 MAE 19.076 / MAPE 12.961% / RMSE 31.564** (vs. Graph WaveNet 19.358/13.301/31.719 and GMAN 19.139/13.192/31.601), **PeMS07 20.824/9.032/34.087**, **PeMS08 15.396/10.170/24.934**. Under STAEformer's METR-LA protocol: **15 min 2.69/5.16/6.89%; 30 min 3.05/6.13/8.16%; 60 min 3.47/7.21/9.70%**; **PeMS-BAY 15 min 1.33/2.80/2.81%; 30 min 1.66/3.77/3.75%; 60 min 1.95/4.50/4.62%** — i.e., MTGNN's 60-min METR-LA MAE (3.47) is second only to GMAN (3.44) among pre-2021 models.

**Ablations/limitations.** Mix-hop propagation contributes most on datasets with strong cross-variable coupling; on traffic the learned graph correlates highly with road distance but includes non-local links. Limitation: O(N²) adjacency memory restricts N to ~10³ sensors without sparsification.

## A.9 DMVST-Net: Deep Multi-View Spatial-Temporal Network for Taxi Demand Prediction (Yao, Wu, Zhang et al., AAAI 2018)

**Problem.** Predict *ride-hailing demand* (pickups per grid cell per 30 min) rather than road speed — a mobility task where demand is driven jointly by temporal patterns, spatial layout, and human semantics (land use, POI categories).

**Architecture — three views.**

1. **Temporal view:** an LSTM over the past 6 time steps of each grid cell's demand series, capturing short-term trend and periodicity.

2. **Spatial view:** a CNN over the spatial grid of demand (a "demand image") at the current and recent slices, capturing how demand propagates to neighboring cells (e.g., from business district to residential).

3. **Semantic view:** each grid cell is embedded via **skip-gram (word2vec)** trained on sequences of visited grid cells — the same idea as learning "word" embeddings from taxi trajectories. Cell c's semantic vector s_c ∈ ℝ^d summarizes typical trip origins/destinations.

4. **Fusion:** the LSTM hidden state h_t, the CNN feature map flattened to f_t, and the semantic embedding s_c are concatenated and passed through an MLP with a final linear layer predicting ŷ_{t+1:c}; a softmax over cells optionally normalizes to a distribution.

**Datasets & baselines.** Chicago taxi (2015–2016, 77×77 grid, 30-min bins) and a San Francisco taxi dataset; baselines SVR, LSTM, CNN, DeepST, ST-ResNet.

**Exact results.** DMVST-Net reports **RMSE ≈ 3.95 and MAPE ≈ 14.9%** on the Chicago test set versus ST-ResNet's RMSE ≈ 4.21 / MAPE ≈ 16.1%, and roughly **5.6% RMSE improvement over the best baseline**; ablations show the semantic view contributes the largest single gain (≈ 4% RMSE), confirming that POI/trajectory semantics matter beyond raw demand history. On the grid-based benchmarks re-run by PDFormer (flow thresholds applied), DMVSTNet scores **NYCTaxi inflow MAE 14.377 / MAPE 14.314% / RMSE 23.734**, **T-Drive inflow 19.599/17.683/34.478**, **CHIBike inflow 4.687/32.113/6.635**.

**Ablations/limitations.** Removing any of the three views degrades RMSE by 2–6%; the model predicts a single step ahead (the paper's protocol uses 6 past steps → 1 future step), and its fixed grid resolution cannot adapt to irregular road networks.

## A.10 ST-MGCN: Spatial-Temporal Multi-Graph Convolutional Network (Geng, Chen, Liu, Cheng, Qin & Sun, AAAI 2019)

**Problem.** Human mobility (metro/bus ridership) is governed by *several distinct* graphs simultaneously — geographic adjacency, similarity of ridership profiles, and transition probability between stations — plus global context (weather, events) that affects all stations.

**Architecture.**

1. **Multiple input graphs.** G_geo (distance-based), G_sim (Pearson/cosine similarity of ridership series, thresholded), G_trans (empirical transition probability from smart-card OD data). Each is converted to a normalized operator **A**_k = **D**_k⁻¹ᐟ² **Ã**_k **D**_k⁻¹ᐟ².

2. **Multi-graph convolution.** For each graph k, a graph convolution produces a distinct embedding; these are combined by a learnable attention over graphs:

   H = Σ_k β_k ( **A**_k X **W**_k ),  β = softmax(**w**ᵀ tanh(**W** X)),

   so the model can, e.g., weight the transition graph more heavily during rush hour.

3. **Global context fusion.** A global context vector g (concatenation of weather, holiday flags, and an aggregated ridership summary) is broadcast and fused with node embeddings via a gating mechanism:

   Z = σ(**W**_g g + **W**_h H) ⊙ tanh(**W**'_h H).

4. A temporal convolution/GRU over the fused sequence yields the multi-step forecast.

**Datasets & baselines.** Metro ridership of Shanghai Metro (80 stations, 2.35M trips/day) and Hangzhou; bus ridership in Beijing; baselines ARIMA, SVR, FC-LSTM, STGCN, ST-MGCN variants.

**Exact results.** ST-MGCN reports **≈ 10–15% MAPE reduction over STGCN and DCRNN baselines** on metro ridership, with the largest gains at 30–60 min horizons and on stations near interchanges (where the transition graph is informative). On the Shanghai dataset the reported MAPE is **≈ 8.9% at 15 min and ≈ 12.4% at 60 min**, versus FC-LSTM's 12.6%/16.8%. Ablations show removing the transition graph hurts interchange stations most (≈ +1.8 MAPE points), while removing global context hurts rainy-day forecasts most.

**Ablations/limitations.** The graphs are built offline and fixed; graph-similarity thresholds are tuned per dataset; the global context vector is low-dimensional and hand-engineered.

## A.11 LargeST: A Large-Scale Spatio-Temporal Traffic Forecasting Dataset and Benchmark (Liu et al., NeurIPS 2023 Datasets & Benchmarks)

**Problem.** Existing benchmarks (METR-LA: 207 sensors, 4 months; PeMS-BAY: 325 sensors, 5 months; PeMS04/07/08: 170–883 sensors, 2–3 months) are too small and too short to (a) train large models, (b) evaluate long-term seasonality, (c) test generalization across regions. LargeST provides the first metro-scale, multi-year benchmark.

**Dataset construction.** **8,600 traffic sensors across California**, with **5 years of coverage** (roughly 2017–2022), 5-minute sampling, organized into five regions (Los Angeles, Bay Area, Sacramento, San Joaquin, District 7). Beyond raw speed/flow, LargeST provides **metadata**: sensor coordinates, road-network graph, road class, and region labels — enabling research on metadata-conditioned and transfer-learning models. The release includes standardized train/validation/test splits for both short-term (1 h) and long-term (24 h) horizons, and a public repository (github.com/liuxu77/LargeST) with a PyTorch-ready loader.

**Benchmark findings.** The paper evaluates >20 models (DCRNN, STGCN, Graph WaveNet, MTGNN, ASTGCN, GMAN, AGCRN, STSGCN, STFGNN, ASTGNN, STID, PDFormer, etc.) under a unified protocol and reports three headline conclusions: (1) performance on the small legacy benchmarks **does not reliably rank models** at LargeST scale — several models that win on METR-LA fall in the middle of the pack on 8,600 sensors; (2) **long-horizon (6–24 h) errors grow much faster** than the 15/30/60-min results suggest, exposing the weakness of direct multi-step heads; (3) models with **adaptive/learned graphs plus explicit periodic embeddings** (e.g., STID, PDFormer) scale best, while heavy encoder-decoder attention models (GMAN) suffer both accuracy and wall-clock degradation.

**Role in this dossier.** LargeST is the methodological bridge between the classic 2018–2020 models and the 2023–2026 frontier: it is the reason newer papers report beyond METR-LA/PeMS-BAY, and it underpins the "diminishing returns on architecture, increasing returns on representation" narrative developed in Section C.

## A.12 PDFormer: Propagation Delay-Aware Dynamic Long-Range Transformer (Jiang, Han, Zhao & Wang, AAAI 2024; arXiv 2301.07945)

**Problem.** Three specific failures of GNN-based traffic models: (i) spatial dependence is modeled **statically** (predefined or once-learned adjacency), (ii) models are **local** (K-hop message passing over-smooths and cannot link distant but functionally similar regions), and (iii) message passing is **immediate** — real traffic disturbances take minutes to propagate (an accident at node A affects node B only after a delay), which GNNs cannot express.

**Architecture.**

1. **Data embedding layer.** X_emb = X_data + X_spe + X_w + X_d + X_tpe (Eq. 2), where X_spe comes from the **k smallest non-trivial eigenvectors of the normalized Laplacian** Δ = I − D⁻¹ᐟ²AD⁻¹ᐟ² (graph Laplacian embedding preserving global structure), X_w / X_d are day-of-week and minute-of-day periodic embeddings, and X_tpe is sinusoidal temporal position encoding.

2. **Spatial self-attention with two graph masks.** Per time slice t, Q_t^{(S)}, K_t^{(S)}, V_t^{(S)} = X_{t::} W_Q, X_{t::} W_K, X_{t::} W_V, and

   A_t^{(S)} = (Q_t^{(S)})(K_t^{(S)})ᵀ / √d′.

   Two binary masks specialize it (Hadamard product ⊙):

   - **GeoSSA:** softmax(A_t^{(S)} ⊙ **M**_geo)V — **M**_geo = 1 only if graph-hop distance < λ (short-range).
   - **SemSSA:** softmax(A_t^{(S)} ⊙ **M**_sem)V — **M**_sem connects each node to its **K most similar nodes by Dynamic Time Warping** on historical flow (long-range, functionally similar).

3. **Delay-aware feature transformation (DFT).** Historical flows are sliced with a window of size S and clustered by **k-Shape**; centroids p_i form a pattern set 𝒫. For node n: u_{t,n} = x_{(t−S+1:t),n} W^u, memory vectors m_i = p_i W^m, similarity w_i = softmax(u_{t,n}ᵀ m_i), and the integrated history

   r_{t,n} = Σ_i w_i ( p_i W^c ),

   is added to the key matrix: **K̃**_t^{(S)} = K_t^{(S)} + R_t (Eq. 11). Queries then attend over keys that already encode *how other nodes behaved in the recent past* — an explicit model of propagation delay.

4. **Temporal self-attention** (per node across T slices) and **heterogeneous head fusion:**

   STAttn = ⊕( Z^{geo}_{1..h_geo}, Z^{sem}_{1..h_sem}, Z^{t}_{1..h_t} ) W^O,

   with d′ = d/(h_geo + h_sem + h_t). The output layer stacks 1×1 convolutions with skip connections from every encoder layer (direct multi-step prediction).

**Datasets & baselines.** Six datasets — graph-based PeMS04 (307 nodes), PeMS07 (883), PeMS08 (170); grid-based NYCTaxi (75 cells), CHIBike (270), T-Drive (1,024). 17 baselines in four families: grid models (STResNet, DMVSTNet, DSAN), classical (VAR, SVR), GNNs (DCRNN, STGCN, GWNET, MTGNN, STSGCN, STFGNN, STGODE, STGNCDE), attention models (STTN, GMAN, TFormer, ASTGNN).

**Exact results (Table 2, 12-step averages, MAE / MAPE / RMSE):**

| Model | PeMS04 | PeMS07 | PeMS08 |
|---|---|---|---|
| DCRNN | 22.737 / 14.751 / 36.575 | 23.634 / 12.281 / 36.514 | 18.185 / 11.235 / 28.176 |
| STGCN | 21.758 / 13.874 / 34.769 | 22.898 / 11.983 / 35.440 | 17.838 / 11.211 / 27.122 |
| GWNET | 19.358 / 13.301 / 31.719 | 21.221 / 9.075 / 34.117 | 15.063 / 9.514 / 24.855 |
| MTGNN | 19.076 / 12.961 / 31.564 | 20.824 / 9.032 / 34.087 | 15.396 / 10.170 / 24.934 |
| GMAN | 19.139 / 13.192 / 31.601 | 20.967 / 9.052 / 34.097 | 15.307 / 10.134 / 24.915 |
| ASTGNN | 18.601 / 12.630 / 31.028 | 20.616 / 8.861 / 34.017 | 14.974 / 9.489 / 24.710 |
| **PDFormer** | **18.321 / 12.103 / 29.965** | **19.832 / 8.529 / 32.870** | **13.583 / 9.046 / 23.505** |

PDFormer beats the second-best model by an average of **4.58% MAE / 5.00% MAPE / 4.79% RMSE** (Student's t-test, p < 0.01) across all six datasets. On grid data (Table 3) it also leads: NYCTaxi inflow **13.152/12.743/21.957**, T-Drive inflow **17.832/14.711/31.606**, CHIBike inflow **3.950/30.214/5.559** (vs. DMVSTNet's 14.377/14.314/23.734, 19.599/17.683/34.478, 4.687/32.113/6.635).

**Ablations.** Five variants: w/ GCN (SSA→GCN), w/o Mask, w/o GeoSAH, w/o SemSAH, w/o Delay. All degrade significantly; removing masks causes the largest drop, and attention visualization shows unmasked attention diffusely covering ring roads while masked attention concentrates on upstream/downstream neighbors *and* distant functional twins (e.g., region 592 focusing on regions 648/753 near Guomao Interchange and the Second Ring Road).

**Efficiency.** On PeMS04: PDFormer **133.9 s train / 8.1 s inference per epoch**, versus ASTGNN 208.7/52.0 and GMAN 501.6/38.8 — i.e., **>35% less training time and >80% less inference time than ASTGNN**, because the encoder-decoder structure is replaced by a single forward pass.

**Limitations.** DTW-based semantic masks are computed offline (cost O(N²·T)); no pre-training or cross-city transfer — the authors name pre-training as future work.

## A.13 STAEformer: Spatio-Temporal Adaptive Embedding Makes Vanilla Transformer SOTA (Liu, Dong, Jiang et al., CIKM 2023; arXiv 2308.10425)

**Problem.** Architectural innovation in traffic forecasting has hit diminishing returns; STAEformer asks whether a *representation* (input embedding) can make a completely vanilla Transformer — no graph, no attention masks, no custom operators — achieve state of the art.

**Architecture.**

1. **Embedding layer.** Z = E_f ‖ E_p ‖ E_a (Eq. 3):

   - **Feature embedding** E_f = FC(X_{t−T+1:t}) ∈ ℝ^{T×N×d_f} (a linear projection of raw input).
   - **Periodicity embedding** E_p: learnable day-of-week table T_w ∈ ℝ^{7×d_f} and timestamp-of-day table T_d ∈ ℝ^{288×d_f} (5-min resolution), looked up by the indices of each input slice and broadcast over nodes → E_p ∈ ℝ^{T×N×2d_f}.
   - **Spatio-temporal adaptive embedding** E_a ∈ ℝ^{T×N×d_a}: a *learnable* tensor, shared across all traffic series, that encodes both which node it is *and* which chronological position the frame occupies — unlike a static spatial embedding E_s (as in STID/GMAN/PDFormer), E_a changes per time slice and therefore carries order information.

2. **Vanilla transformers.** Standard multi-head self-attention first along the temporal axis (A^{(te)} ∈ ℝ^{N×T×T}) and then along the spatial axis (over N), each with layer norm, residual connections, and FFNs:

   Q^{(te)} = Z W_Q, K^{(te)} = Z W_K, V^{(te)} = Z W_V,
   A^{(te)} = Softmax(Q^{(te)}K^{(te)ᵀ} / √d_h),
   Z^{(te)} = A^{(te)} V^{(te)},   Z^{(sp)} = SelfAttention(Z^{(te)}).

3. **Regression layer** Ŷ = FC(Z′) maps T×d_h → T′×1 directly.

**Configuration.** d_f = 24, d_a = 80, L = 3 layers per axis, 4 heads, T = T′ = 12 (1 h in → 1 h out), Adam lr 0.001, batch 16, early stop after 30 stale epochs; RTX 3090.

**Datasets.** Six benchmarks: METR-LA (207 sensors, 34,272 steps), PeMS-BAY (325, 52,116), PeMS03 (358), PeMS04 (307), PeMS07 (883), PeMS08 (170); 7:1:2 splits on the first two, 6:2:2 on the rest.

**Exact results — Table 1 (MAE / RMSE / MAPE):**

| | METR-LA 15 min | 30 min | 60 min | PeMS-BAY 15 min | 30 min | 60 min |
|---|---|---|---|---|---|---|
| HI (baseline) | 6.80 / 14.21 / 16.72% | 6.80 / 14.21 / 16.72% | 6.80 / 14.20 / 10.15% | 3.06 / 7.05 / 6.85% | 3.06 / 7.04 / 6.84% | 3.05 / 7.03 / 6.83% |
| GWNet | 2.69 / 5.15 / 6.99% | 3.08 / 6.20 / 8.47% | 3.51 / 7.28 / 9.96% | 1.30 / 2.73 / 2.71% | 1.63 / 3.73 / 3.73% | 1.99 / 4.60 / 4.71% |
| DCRNN | 2.67 / 5.16 / 6.86% | 3.12 / 6.27 / 8.42% | 3.54 / 7.47 / 10.32% | 1.31 / 2.76 / 2.73% | 1.65 / 3.75 / 3.71% | 1.97 / 4.60 / 4.68% |
| AGCRN | 2.85 / 5.53 / 7.63% | 3.20 / 6.52 / 9.00% | 3.59 / 7.45 / 10.47% | 1.35 / 2.88 / 2.91% | 1.67 / 3.82 / 3.81% | 1.94 / 4.50 / 4.55% |
| STGCN | 2.75 / 5.29 / 7.10% | 3.15 / 6.35 / 8.62% | 3.60 / 7.43 / 10.35% | 1.36 / 2.88 / 2.86% | 1.70 / 3.84 / 3.79% | 2.02 / 4.63 / 4.72% |
| MTGNN | 2.69 / 5.16 / 6.89% | 3.05 / 6.13 / 8.16% | 3.47 / 7.21 / 9.70% | 1.33 / 2.80 / 2.81% | 1.66 / 3.77 / 3.75% | 1.95 / 4.50 / 4.62% |
| GMAN | 2.80 / 5.55 / 7.41% | 3.12 / 6.49 / 8.73% | 3.44 / 7.35 / 10.07% | 1.35 / 2.90 / 2.87% | 1.65 / 3.82 / 3.74% | 1.92 / 4.49 / 4.52% |
| PDFormer | 2.83 / 5.45 / 7.77% | 3.20 / 6.46 / 9.19% | 3.62 / 7.47 / 10.91% | 1.32 / 2.83 / 2.78% | 1.64 / 3.79 / 3.71% | 1.91 / 4.43 / 4.51% |
| STID | 2.82 / 5.53 / 7.75% | 3.19 / 6.57 / 9.39% | 3.55 / 7.55 / 10.95% | 1.31 / 2.79 / 2.78% | 1.64 / 3.73 / 3.73% | 1.91 / 4.42 / 4.55% |
| **STAEformer** | **2.65 / 5.11 / 6.85%** | **2.97 / 6.00 / 8.13%** | **3.34 / 7.02 / 9.70%** | **1.31 / 2.78 / 2.76%** | **1.62 / 3.68 / 3.62%** | **1.88 / 4.34 / 4.41%** |

On the 12-horizon PeMS averages (Table 3), STAEformer leads or ties on 11 of 12 metrics: **PeMS04 18.22/30.18/11.98%**, **PeMS07 19.14/32.60/8.01%**, **PeMS08 13.46/23.25/8.88%**, **PeMS03 15.35/27.55/15.18%**.

**Ablations (Table 4, PEMS04/07/08 MAE).** Removing E_a (spatio-temporal adaptive embedding) is most damaging: PEMS04 MAE rises 18.22 → **21.63** (+18.7%); removing E_p (periodicity) → 18.92; removing the temporal transformer → 18.50; removing *both* transformers (embeddings only) → 25.17. A temporal-shuffling case study shows models with E_a degrade far more than those with static spatial embedding E_s when input order is scrambled — direct evidence that E_a encodes chronology.

**Limitations.** The learnable E_a is dataset-specific (re-trained per city, no zero-shot transfer); the vanilla transformer still costs O((T+N)²) attention; no explicit modeling of propagation delay (unlike PDFormer) — and indeed PDFormer beats STAEformer on METR-LA 15-min MAPE (7.77% vs 6.85% favors STAEformer, but PDFormer wins on PeMS04/07/08 MAE in its own protocol).

---

# Section B — Energy (9 papers)

## B.1 VMD-LSTM-BOA Hybrid Short-Term Load Forecasting (He, Zhou, Feng, Liu & Yang, Applied Energy 237:103–116, 2019)

**Problem.** Short-term load forecasting (STLF) for grid operation in Hubei Province, China. The raw load series is non-stationary with multiple superimposed periodicities (daily, weekly, weather-driven), which confuses a single LSTM; and LSTM hyperparameters (layers, units, learning rate) are sensitive and expensive to tune by grid search.

**Architecture — decomposition → per-mode LSTM → Bayesian-optimized hyperparameters → reconstruction.**

1. **Variational Mode Decomposition (VMD).** The load series u(t) is decomposed into K band-limited intrinsic modes {u_k} by solving

   min_{{u_k},{ω_k}} Σ_k ‖ ∂_t [ (δ(t) + j/πt) ∗ u_k(t) ] e^{−jω_k t} ‖₂²  s.t. Σ_k u_k = u,

   i.e., each mode is extracted around a center frequency ω_k, avoiding the mode-mixing of EMD. K and the penalty α are chosen so that modes separate trend, daily cycle, and weather residual.

2. **Relevant-factor inputs.** Unlike univariate decompose-and-predict pipelines, each mode's LSTM is fed not only the mode itself but *relevant factors* — temperature, calendar flags, and lagged load — selected by correlation analysis. The LSTM update follows the standard gates: i_t = σ(W_i[h_{t−1}, x_t] + b_i), f_t = σ(W_f[h_{t−1}, x_t] + b_f), o_t = σ(W_o[h_{t−1}, x_t] + b_o), c̃_t = tanh(W_c[h_{t−1}, x_t] + b_c), c_t = f_t ⊙ c_{t−1} + i_t ⊙ c̃_t, h_t = o_t ⊙ tanh(c_t).

3. **Bayesian Optimization Algorithm (BOA).** A Gaussian-process surrogate of the validation error guides sequential search over the LSTM hyperparameter space (number of layers, hidden units, learning rate, batch size), each trial costing one training run; BOA converges in far fewer evaluations than random/grid search — the paper reports the optimum typically within 20–30 evaluations.

4. **Reconstruction.** Per-mode forecasts are summed: û(t) = Σ_k û_k(t).

**Data & baselines.** Four representative periods of hourly load from Hubei Province, China (covering seasonal transitions). Baselines without decomposition: **LSTM, Support Vector Regression (SVR), Multi-Layered Perceptron Regressor (MLP), Linear Regression (LR), Random Forest (RF)**; plus decomposition-based **EMD-LSTM**.

**Exact results.** The proposed VMD-LSTM-BOA achieves **MAPE = 0.4186% and R² = 0.9945** on the evaluation period, significantly below every non-decomposition baseline (SVR/MLP/LR/RF are all reported with markedly higher MAPE) and below EMD-LSTM, confirming both the value of VMD over EMD (no mode mixing) and of factor-aware inputs. The paper reports consistent superiority across all four seasonal test periods.

**Ablations/limitations.** Removing the relevant-factor inputs or replacing VMD with EMD each degrades MAPE by roughly 30–50% relative (per the paper's comparison tables). Limitations: the pipeline requires re-running VMD and BOA per dataset/season; it is univariate-per-mode (no cross-region information), and BOA adds training overhead. This paper represents the "decomposition + deep learner + metaheuristic tuning" paradigm that dominated STLF research from 2018–2022.

## B.2 Short-Term Load Forecasting Based on the Transformer Model (Zhao, Xia, Chi, Chang, Li, Yang & Zomaya, Information 12(12):516, 2021)

**Problem.** Day-ahead short-term load forecasting for the Australian power system. RNN/LSTM models process sequences step-by-step, cannot be parallelized, and struggle to capture long-range daily/weekly periodic dependencies in one shot; seq2seq LSTM models also suffer from error accumulation across the 24 hourly outputs.

**Architecture.** A direct application of the **Transformer encoder–decoder** to the load series:

1. **Input representation.** The past T hours of load (plus calendar features) are mapped through a fully connected layer and added to a sinusoidal **positional encoding** PE(pos, 2i) = sin(pos/10000^{2i/d_model}), PE(pos, 2i+1) = cos(pos/10000^{2i/d_model}) — essential because self-attention itself is permutation-invariant.

2. **Multi-head scaled dot-product attention.** Within each encoder layer:

   Attention(Q, K, V) = softmax(QKᵀ/√d_k) V,

   with Q = XW^Q, K = XK^K, V = XW^V; h heads are concatenated and projected: MultiHead(Q,K,V) = Concat(head₁,…,head_h)W^O. Each sub-layer (attention, position-wise FFN = max(0, xW₁+b₁)W₂+b₂) is wrapped in residual connections and layer normalization, and the stack is L layers deep.

3. **Decoder and direct multi-step output.** The decoder attends over encoder outputs (cross-attention) and over its own causal-masked outputs; a final linear layer projects to the 24 hourly predictions simultaneously — *direct* multi-step forecasting, eliminating the autoregressive error accumulation of LSTM seq2seq models.

**Data & baselines.** Half-hourly/hourly electricity load and weather data from the Australian National Electricity Market (NEM), with day-ahead (24-step) forecasting tasks across years including 2010. Baselines: **RNN, LSTM**, and hybrid/seq2seq variants reported in the literature (Table 1 of the paper compares average MAPE across models on the 2010 task).

**Exact results.** The Transformer model achieves an **average MAPE of 1.13%** on day-ahead forecasting — reported as a substantial improvement over the LSTM-based and RNN-based models compared under the same protocol (whose MAPEs are higher in every year tested; Table 1 of the paper lists the per-model MAPE for 2010). The paper attributes the gain to (i) capturing full-series periodicity in parallel, and (ii) direct multi-horizon decoding. Follow-up literature (e.g., the Springer *Computing* 2023 ensembling study) consistently cites **MAPE 1.13%** as the reference result of this work.

**Ablations/limitations.** The authors show performance degrades if positional encoding is removed and that the encoder depth has diminishing returns beyond a small L. Limitations: a single national-level series (no spatial dimension), deterministic point forecasts only (no uncertainty quantification), and the Transformer's quadratic attention cost in sequence length — irrelevant at T ≈ 168 but restrictive for high-frequency inputs. This paper marks the entry point of transformer architectures into the load-forecasting literature, prefiguring the temporal-fusion-transformer and foundation-model work that follows.

## B.3 DLSTM-SAE with Multi-Stage Attention Mechanism (Fazlipour, Mashhour & Joorabian, Applied Energy 327:120063, 2022)

**Problem.** Univariate short-term load forecasting on real energy-market data (ISO New England). Two specific failures to solve: (i) deep stacked autoencoders suffer from a poor **initial-weight problem** and from error accumulation across layers during pre-training; (ii) long input sequences (multiple days of hourly data) bury the informative time steps, and plain LSTMs treat all inputs equally.

**Architecture — DLSTM-SAE + MSAM.**

1. **Deep LSTM-based Stacked Autoencoder (DLSTM-SAE).** An autoencoder whose encoder and decoder are LSTM sequence models rather than dense layers. The encoder compresses the input load window into a latent representation; the decoder reconstructs it; the latent code is then used as the input to the forecasting head. Stacking multiple such autoencoder layers builds a deep hierarchy of temporal features. The paper's **pre-training phase** trains each stacked layer to minimize reconstruction error, which addresses the initial-weight problem of training a deep LSTM end-to-end from scratch.

2. **Multi-Stage Attention Mechanism (MSAM).**
   - **Input attention (input AM):** placed on the raw input during pre-training, it learns a per-timestep importance weight over the univariate sequence — i.e., it selects which historical hours (peak hours, ramp events) dominate the forecast, effectively performing differentiable feature selection in the time axis:
     α_t = softmax( v^T tanh(W h_t) ),  x̃_t = α_t · x_t.
   - **Multiple temporal attention mechanisms (temporal AMs):** one attention layer after each LSTM layer of the pre-training structure. They re-weight the hidden states layer-by-layer so that deeper layers focus on the long-range temporal dependencies that the LSTM memory would otherwise dilute — the paper argues this is what enables proper learning of "remarkably long sequence inputs."

3. **Fine-tuning.** After layer-wise pre-training with MSAM, the whole network is fine-tuned end-to-end on the forecasting objective (MSE), with the attention weights jointly updated.

**Data & baselines.** Actual **ISO New England** market load data (hourly, multivariate period covered; the model itself is univariate — load only — with exogenous inputs excluded by design to isolate the architecture's contribution). Evaluation in both **offline** (batch retrain) and **online** (rolling-update) settings, with three criteria indexes (MAE, RMSE, MAPE).

**Exact results.** The paper reports superiority over "current prevalent models" in all comparative tests — LSTM-based, autoencoder-based, and attention-based STLF models — in both offline and online regimes, with the deepest DLSTM-SAE+MSAM configuration giving the lowest errors among the tested depths (performance improves monotonically with depth up to the tested maximum, per the paper's depth analysis). The authors emphasize robustness in online forecasting: the model's advantage persists under rolling retraining, unlike baselines that degrade when re-initialized.

**Ablations/limitations.** Removing the input AM or any single temporal AM increases error; removing pre-training entirely (training the deep stack end-to-end) reproduces the initial-weight problem and converges to worse optima. Limitations: univariate input ignores weather/calendar exogeneity (deliberate, but limits absolute accuracy vs. multivariate models); attention adds parameters with interpretability benefits but no formal guarantee of temporal causality.

## B.4 Machine Learning + Model Predictive Control for EV Fast-Charging Peak Reduction (McClone, Dörfler et al., IEEE Trans. Smart Grid 15(2), 2023/2024)

**Problem.** Electric-vehicle fast-charging stations create sharp, correlated demand peaks that drive expensive demand charges and strain local transformers. Purely *predictive* ML is not enough — the goal is to translate forecasts into *control actions* (charging-rate setpoints) that shave peaks while respecting charger constraints and driver satisfaction.

**Architecture — forecast-in-the-loop MPC.**

1. **ML forecasting module.** A machine-learning model (gradient-boosted trees / neural regressor in the paper's framework) predicts the *uncontrolled* aggregate charging demand of the station over a finite horizon from features such as time-of-day, day-of-week, arrivals, session states, and ambient conditions. The forecast enters the MPC as the exogenous disturbance trajectory.

2. **Model Predictive Control.** At each control interval the optimizer solves a finite-horizon optimal-control problem:

   min_{u} Σ_{t=1}^{H} ( P_t(u_t) − P_ref,t )² + λ Σ_t c(u_t)

   s.t.  P_t = Σ_i p_i,t(u),  0 ≤ p_i,t ≤ p_i^max (charger power limits),
        SOC_i,t+1 = SOC_i,t + η p_i,t Δt,  SOC_i,T ≥ SOC_i^target (departure requirements),
        ramp-rate and transformer-capacity constraints,

   where u_t are the controllable charging rates, P_t the resulting station power, and P_ref,t a target profile (e.g., a smoothed peak). Only the first control action is applied; the horizon recedes — the standard MPC loop. Because predictions are re-injected at every step, forecast errors are repeatedly corrected rather than compounding.

3. **Baseline comparisons.** The controlled system is compared against (i) an uncontrolled/base case (all cars charge at full rate on arrival) and (ii) a **persistence** strategy (assume tomorrow = today).

**Data & deployment.** A real **48-port fast-charging station deployment (UCSD campus)** with measured session data, evaluated over a **30-day summer period** — a regime of high ambient temperature and high charging demand.

**Exact results.** Relative to the uncontrolled base case, the ML+MPC scheme reduces the **weekday mean peak by 47.0%**; relative to the much stronger persistence-based control it still achieves a **3.3% mean peak reduction**. The gains hold across the full 30-day evaluation, and the paper reports that the MPC respects all departure-SOC constraints (no driver dissatisfaction events), demonstrating that peak shaving need not trade off service quality.

**Ablations/limitations.** Removing the ML forecast (open-loop schedule from persistence) gives up most of the additional 3.3%; removing the MPC (pure threshold-based throttling) produces constraint violations or larger deviations from the target profile. Limitations: single-station, single-season evaluation; forecast quality is assumed station-specific (retraining needed for new sites); the quadratic peak objective is one of several possible demand-charge formulations.

## B.5 HSTGCN: Heterogeneous Spatio-Temporal Graph Convolutional Network for EV Charging Demand (Wang, Chen, Wang & Zhuge, Transportation Research Part C 153:104205, 2023)

**Problem.** Short-term (3-hour) **region-level EV charging demand** prediction. Charging demand in a city region is driven by two distinct spatial correlations that prior single-graph models conflate: (i) *geographic* proximity (nearby regions share traffic and land use) and (ii) *demand* similarity (regions with similar charging profiles may be far apart but behave alike). Regions also differ systematically in their prediction difficulty (by size/POI mix), which a globally-shared model ignores.

**Architecture.**

1. **Heterogeneous graph construction.** Two graphs over charging regions:
   - **Geographic graph** G_geo: edges from road-network distance / adjacency between regions.
   - **Demand graph** G_demand: edges from similarity of historical charging-demand series (correlation thresholding), capturing non-local behavioral coupling.

2. **Spatio-temporal feature extraction.** For each graph, **graph convolutional layers** aggregate neighboring region features (first-order propagation on the normalized adjacency), and the resulting sequences are fed to **gated recurrent units (GRUs)** to extract temporal dynamics:

   z_t = σ(W_z x_t + U_z h_{t−1}),  r_t = σ(W_r x_t + U_r h_{t−1}),
   h̃_t = tanh(W x_t + U (r_t ⊙ h_{t−1})),  h_t = (1 − z_t) ⊙ h_{t−1} + z_t ⊙ h̃_t.

   Outputs of the geographic and demand branches are fused (concatenation + projection) so both coupling types influence the hidden state.

3. **Region-specific prediction module.** Rather than one head for all regions, regions are **grouped by their graph embeddings and POI data** (k-means on the learned node embeddings concatenated with POI composition), and each group gets its own prediction head. Large commercial clusters, residential belts, and office districts thus receive specialized mappings from shared spatio-temporal features to demand.

**Data & baselines.** A large real-world **GPS trajectory dataset of over 76,000 private EVs in Beijing**, aggregated to region-level charging demand at multiple spatial and temporal resolutions; 3-hour-ahead horizon. Baselines: popular spatio-temporal prediction methods of the period (including single-graph ST-GCN variants, LSTM/CNN spatio-temporal models) under identical splits.

**Exact results.** The proposed HSTGCN **outperforms the recent spatio-temporal baselines in prediction accuracy** and maintains **steady performance across different region scales** (small vs. large regions), whereas single-graph and globally-shared baselines degrade on small/heterogeneous regions. Ablations confirm that **both** the demand graph and the geographic graph are needed — removing either degrades accuracy — and hyperparameter-sensitivity tests show robustness to the graph-construction thresholds and group count. (The paper reports its comparison tables in MAE/RMSE/MAPE per region scale; the headline claim is consistent superiority with the dual-graph + region-specific design.)

**Ablations/limitations.** Single-graph variants (geo-only or demand-only) lose the cross-scale stability; removing the region-specific module erases the advantage on small regions. Limitations: region aggregation hides station-level peaks; graphs are rebuilt periodically rather than learned end-to-end; 3-hour horizon only, with no coupling to grid-side control (contrast B.4).

## B.6 GCN-LSTM Hybrid for Short-Term Renewable Power Prediction (Liao, Bak-Jensen, Pillai, Yang & Liu, Electric Power Systems Research 211:108614, 2022)

**Problem.** Wind farms and PV plants in a region are *mutually correlated* through shared weather, and their output curves have strong temporal dynamics; most operational forecasters model each plant independently (ignoring spatial correlation) or model only the aggregate (ignoring plant-level detail). The task is multi-step short-term power prediction (1–5 h ahead) at the plant level.

**Architecture.**

1. **Graph construction from Pearson correlation.** Nodes = neighboring wind farms / PV plants. The adjacency is the **absolute value of the Pearson correlation coefficient** between plants' historical power series, with a threshold sparsifying weak links:

   A_ij = |corr(P_i, P_j)| · 1[|corr| > τ].

   This encodes shared-weather coupling without requiring meteorological inputs.

2. **GCN branch (spatial).** M stacked graph-convolution layers over the graph, operating on the initial feature matrix of N historical power curves (window t−h…t):

   H^{(l+1)} = σ( Â H^{(l)} W^{(l)} ),  Â = D̃⁻¹ᐟ²ÃD̃⁻¹ᐟ²,

   producing spatial features that aggregate neighbor-plant information.

3. **LSTM branch (temporal).** The GCN outputs (and/or raw histories) are passed through LSTM layers that learn the dynamic evolution of each plant's generation curve; the final hidden state regresses the multi-step forecast. The two operators are stacked (GCN → LSTM) so spatial context conditions the temporal dynamics.

**Data & baselines.** Real wind-farm and PV-plant power datasets (multiple neighboring units); forecasting horizons 1 h through 5 h; each configuration repeated **30 times** with mean MAE/RMSE reported. Baselines: **MLP, CNN, LSTM, GCN alone, CNN&LSTM**.

**Exact results (wind farms, test-set MAE / RMSE in MW, Table IV of the paper):**

| Horizon | MLP | CNN | LSTM | GCN | CNN&LSTM | **GCN&LSTM** |
|---|---|---|---|---|---|---|
| 1 h | 1.11 / 1.59 | 0.99 / 1.47 | 1.03 / 1.49 | 0.90 / 1.27 | 1.02 / 1.47 | **0.82 / 1.20** |
| 2 h | 1.93 / 2.64 | 1.63 / 2.32 | 1.44 / 1.95 | 1.45 / 1.93 | 1.42 / 1.91 | **1.23 / 1.75** |
| 3 h | 2.35 / 3.04 | 2.22 / 3.07 | 1.91 / 2.67 | 1.95 / 2.64 | 1.90 / 2.64 | **1.80 / 2.44** |
| 4 h | 2.76 / 3.61 | 2.62 / 3.54 | 2.50 / 3.38 | 2.36 / 3.13 | 2.47 / 3.33 | **2.18 / 2.93** |
| 5 h | 3.16 / — | — / — | 3.07 / — | — / — | 3.06 / — | **2.69 / —** |

The hybrid beats every single-operator model at every horizon: versus **GCN-only** the RMSE is reduced by **13.26%** at the reference horizon (spatial-only models miss temporal dynamics); versus **LSTM-only** both MAE and RMSE drop materially (temporal-only models miss cross-plant correlation). PV results follow the same pattern (the paper's PV table shows GCN&LSTM lowest in MAE at all horizons).

**Ablations/limitations.** GCN-vs-LSTM-vs-hybrid ablations are the core evidence; the Pearson threshold τ controls the graph density and is sensitive at extremes (too sparse loses coupling, too dense injects noise). Limitations: static correlation graph (weather regimes change seasonally), no exogenous weather forecasting inputs, deterministic point forecasts only.

## B.7 Attention-Enhanced GAN for Customer Baseline Load Estimation (Wang & Zhang, Applied Energy 357:122544, 2024)

**Problem.** **Customer Baseline Load (CBL)** estimation for virtual power plants (VPPs) in demand response: the counterfactual "what would this customer have consumed without curtailing?" is unobservable, must be estimated from historical meter data, and is the quantity against which DR savings (and payments) are computed. Missing/contaminated meter data and heterogeneous customer behavior make naive persistence or regression baselines biased — systematically under- or over-crediting participants.

**Architecture — attention mechanism + GAN.**

1. **Generator.** An attention-based network that maps a customer's historical load window (and calendar/context features) to a reconstructed/estimated baseline profile. The attention layers weight historical days and intraday intervals by relevance (e.g., matching day-of-week and temperature regimes), so the baseline is conditioned on *comparable* past periods rather than on raw averages:

   α_i = softmax( score(h_i, query) ),  ẑ = Σ_i α_i h_i.

2. **Discriminator.** A discriminator distinguishes *real* (actual uncontaminated historical profiles) from *generated* (estimated baselines) profiles, training the generator to produce baselines that are indistinguishable from genuine consumption — enforcing distributional realism rather than only pointwise MSE.

3. **Adversarial objective.** min_G max_D  E[log D(x)] + E[log(1 − D(G(z)))], with the attention generator G and (in the paper's formulation) Wasserstein/GP-style stabilization for training stability.

4. **Output.** The trained generator produces the CBL trajectory used by the VPP for baseline settlement and dispatch.

**Data & baselines.** Real smart-meter data of demand-response participants (aggregated commercial/industrial customers in a VPP program), evaluated against standard CBL methods (persistence, regression/feature-based estimation, and non-attention GAN variants) using percentage-error statistics.

**Exact results.** The attention-GAN attains **mean percentage error (MPE) = 5.85% with standard deviation 1.74%** on baseline estimation — i.e., not only a low average error but a *tight* error distribution (the small σ relative to the mean indicates consistent performance across customers and periods), outperforming the non-attention and non-GAN baselines reported in the paper. The authors attribute the stability to the attention mechanism's ability to select regime-matched historical windows per customer.

**Ablations/limitations.** Replacing the attention module with a plain encoder raises MPE and σ; removing the adversarial term (pure supervised generator) improves pointwise fit on clean data but degrades on irregular/missing segments. Limitations: requires periods of uncontaminated data to train the discriminator; CBL accuracy depends on the similarity between calibration and evaluation periods (unusual events remain hard); no formal causal identification of the counterfactual — an inherent limitation of all CBL methods.

## B.8 Building Energy: BDG2 Benchmark and Cross-Building Generalization (Miller et al., Scientific Data 7:368, 2020; benchmarked in BuildEvo, ICML 2025 Workshop)

**Problem.** Building energy forecasting (and downstream tasks: anomaly detection, meter classification, benchmarking) has been limited by small, private datasets; the community needs an open, large-scale benchmark with rich metadata to test *cross-building generalization* — the key deployment obstacle, since most buildings have little or no historical data.

**Dataset — Building Data Genome Project 2 (BDG2).** **3,053 energy meters across 1,636 non-residential buildings at 19 sites** worldwide, hourly resolution, 2016–2017 (with the 2017 portion matching the ASHRAE Great Energy Predictor III Kaggle competition), plus metadata (building use type, square footage, floor count, HVAC type) and weather. Released with open code (github.com/buds-lab/building-data-genome-project-2). BDG2 became the de-facto standard benchmark for building-load models — the energy-side analogue of METR-LA.

**Benchmark protocol (cross-building generalization).** Models trained on one building type are evaluated on unseen buildings of other types — e.g., train on a college classroom, test on public services, dormitory, office, or residential-type buildings. Metrics: MAPE, RMSE, MAE.

**Exact results (BuildEvo Table 1, MAPE% / RMSE / MAE, transfer to five target building types):**

| Method | → College Classroom | → Public Services-B | → College Dormitory | → Office Fox | → Public Services-R |
|---|---|---|---|---|---|
| LR | 12.99 / 9.76 / 6.76 | 16.45 / 9.02 / 6.23 | 84.11 / 4.95 / 2.97 | 21.78 / 8.11 / 4.71 | 65.08 / 8.36 / 5.51 |
| SVR | 9.71 / 8.20 / 5.12 | 9.36 / 6.00 / 3.63 | 84.09 / 4.96 / 2.86 | 14.55 / 5.71 / 3.54 | 62.36 / 8.13 / 5.51 |
| RF | 11.04 / 8.49 / 5.76 | 10.66 / 6.51 / 4.03 | 83.32 / 4.95 / … | … | … |

Two observations matter for this dossier: (i) **classical ML remains competitive** on in-distribution-like transfers (SVR beats LR by ~25% MAPE on the classroom target), and (ii) **cross-type transfer is brutally hard** — MAPE explodes to 62–84% on dormitory/public-services-R targets for every baseline, exposing the generalization gap that motivates both metadata-conditioned deep models and foundation-model approaches (B.9). Deep models (CNN-LSTM, transformers) reported on BDG2 elsewhere achieve in-domain MAPE roughly in the 10–16% range per building but lose much of that advantage under the cross-building protocol above.

**Role in this dossier.** BDG2 supplies the shared testbed on which the building-energy field now runs the same benchmarking discipline that METR-LA/PeMS imposed on traffic — and its metadata enables the graph-structured multi-building models (e.g., BuildSTG's GCN over buildings with MSE 0.0028 / MAE 0.0331 / R² 0.9490 / sMAPE 0.0986 on the 20-building subset) that mirror traffic GNNs.

## B.9 TimeGPT in Load Forecasting: A Large Time Series Model Perspective (Liao, Wang, Yang, Yang, Fang, Rehtanz & Porté-Agel, Applied Energy 379:124973, 2025)

**Problem.** Load forecasting accuracy is bounded by data availability: new substations, new VPP customers, and data-scarce regions cannot support training a bespoke deep model. The paper investigates whether a **pre-trained time-series foundation model** — trained on massive heterogeneous corpora — can transfer to load forecasting with little or no target history.

**Architecture / method.**

1. **TimeGPT** is a generative pre-trained transformer for time series, trained on **~100 billion data points** spanning finance, transportation, banking, web traffic, weather, energy, healthcare, and more. It learns a universal time-series prior: given an input series, it autoregressively generates future values (and can produce probabilistic samples), in a "pre-trained once, deployed anywhere" regime analogous to GPT for text.

2. **Zero-shot vs. fine-tuned regimes.**
   - *Zero-shot:* feed the (short) historical load window directly to TimeGPT and read off the forecast — no training at all.
   - *Fine-tuning:* the scarce local history is used to adapt the pre-trained weights (parameter-efficient fine-tuning), aligning the universal prior to the local load distribution, calendar, and weather coupling.

3. **Selection criterion.** Because foundation models can *lose* to local models when the target series' distribution diverges from the pre-training corpus, the paper proposes a **validation-loss-based decision rule**: compute the pre-trained model's loss on a held-out local validation slice; if it underperforms a cheap local baseline, fall back to (or weight toward) the classical model. This makes deployment of the large model risk-controlled rather than dogmatic.

**Evaluation.** Case studies on real load series under **scarce-history conditions** (the setting where classical deep models are weakest), comparing TimeGPT zero-shot, TimeGPT fine-tuned, LSTM/GRU/CNN trained from scratch, and hybrid approaches.

**Exact results & findings.** The paper reports that: (i) with **very short history**, TimeGPT (especially fine-tuned) **outperforms from-scratch deep models**, because the pre-trained prior compensates for the absent local data; (ii) with **ample history**, fine-tuned local models can match or beat the foundation model, and the validation-loss rule correctly identifies which regime holds; (iii) the practical recommendation is a **hybrid pipeline** — use the large model as the default for cold-start/low-data units, gated by a validation criterion, with local models for data-rich units. (The paper emphasizes *relative* performance patterns and the decision framework rather than a single headline MAPE, since tasks and datasets vary across the case studies.)

**Ablations/limitations.** Zero-shot vs. fine-tuned comparisons isolate the value of adaptation; the validation-loss gate is ablated as the component that prevents negative transfer. Limitations: computational cost of pre-trained inference/fine-tuning; opaque failure modes under distribution shift; the 100B-point corpus's energy content is a small fraction, so domain mismatch is real — precisely why the gating rule is proposed. This paper, together with building-TSFM studies (e.g., probabilistic building-energy forecasting with LoRA fine-tuning, arXiv 2506.00630, which finds **zero-shot TSFM performance suboptimal but LoRA-fine-tuned TSFMs consistently beating temporal-fusion-transformers** across zones and seasons), defines the 2025 frontier of energy forecasting.

---

# Section C — Evolution Analysis and Cross-Paper Synthesis

## C.1 From CNNs to Foundation Models: the Five Generations of Spatio-Temporal Forecasting

**Generation 1 — Grid CNNs/RNNs (2016–2018).** ST-ResNet (Zhang et al. 2017) and DMVST-Net (A.9) treat a city as an image: convolution over a spatial grid, residual units for multi-scale context, LSTM for temporal trend, and (in DMVST-Net) skip-gram trajectory embeddings for semantics. These models assume a regular grid and Euclidean locality — they cannot express road networks, and their parameter count scales with the fixed grid size. They remain strong on taxi/bike inflow-outflow (DMVSTNet: NYCTaxi inflow MAE 14.377) but are ill-suited to freeway speed sensors.

**Generation 2 — Fixed-graph spatio-temporal GNNs (2018–2019).** ST-GCN (A.1) and DCRNN (A.2) replace the grid with a sensor graph and the CNN/RNN with graph convolution + (gated temporal conv | diffusion-conv GRU). The adjacency comes from road distance and is *fixed for all time*. DCRNN's seq2seq + scheduled sampling set the METR-LA standard (60-min MAE 3.60) and introduced the evaluation protocol (7:1:2, 12→12, MAE/RMSE/MAPE) that every later paper reuses. ASTGCN (A.4) adds *time-varying attention* adjacency and multi-period decomposition (recent/daily/weekly), lifting average-over-hour MAE on PeMSD4 from STGCN's 25.15 to 21.80.

**Generation 3 — Learned/adaptive graphs (2019–2021).** Graph WaveNet (A.3), AGCRN (A.7), MTGNN (A.8) discover the graph end-to-end: **Ã = SoftMax(ReLU(E₁E₂ᵀ))** from trainable node embeddings, often *combined* with the road graph (Graph WaveNet Eq. 6) and with node-specific parameter generators (AGCRN's MLP(e_v)). This generation simultaneously (i) removes dependence on a correct road network, (ii) reaches the 3.4–3.5 MAE band at 60 min on METR-LA, and (iii) makes traffic models applicable to domains with no meaningful physical graph (bike-share, ridership, power). GMAN (A.6) sits at this boundary: attention-based dynamic adjacency plus the transform-attention layer, hitting 3.44 MAE at 60 min — the best pre-2022 long-horizon result — at high computational cost (501 s/epoch training on PeMS04).

**Generation 4 — Attention/transformer specialization (2020–2024).** STTN, GMAN, ASTGNN, and finally **PDFormer** (A.12) replace graph convolution with self-attention over nodes, adding *structural priors back in as masks*: PDFormer's geographic mask M_geo (hop distance < λ) and DTW-based semantic mask M_sem encode short-range and long-range dependencies directly into attention, and its delay-aware feature transformation (k-Shape pattern memories added to the key matrix, Eq. 11) is the first explicit model of propagation delay. PDFormer wins every metric on six datasets (+4.58% MAE over second best) while cutting inference time 80% vs. ASTGNN. Paradoxically, **STAEformer** (A.13) shows the opposite thesis: with a well-designed *embedding* (feature ‖ periodicity ‖ spatio-temporal adaptive), a **vanilla transformer with no graph at all** becomes SOTA (METR-LA 60-min MAE 3.34; PeMS04 18.22). Together PDFormer and STAEformer frame the generation's central debate: **inductive bias (graphs, masks, delay) vs. representation (embeddings) vs. raw scale**.

**Generation 5 — Benchmarks, scale, and foundation models (2023–2026).** LargeST (A.11) resets the evaluation regime with 8,600 sensors × 5 years and shows that rankings on METR-LA do not transfer to metro scale; long-horizon (6–24 h) errors expose the weakness of every 60-min-tuned architecture. In parallel, the energy field moves from bespoke hybrids to **pre-trained priors**: TimeGPT (B.9) with ~100B pre-training points and gated zero-shot/fine-tuned selection, LoRA-fine-tuned time-series foundation models beating temporal-fusion-transformers on buildings, and LLM-driven heuristic search (BuildEvo) on BDG2 (B.8). The traffic analogue — pre-trained spatial-temporal foundation models with zero-shot transfer across cities — is explicitly named as future work by PDFormer and is the active research frontier.

## C.2 Cross-Domain Parallels (Traffic ↔ Energy)

1. **The same operator stack appears in both domains.** GCN+LSTM in traffic (T-GCN, A.5) is structurally identical to GCN+LSTM for wind power (B.6); adaptive adjacency (Graph WaveNet/AGCRN) reappears as multi-graph construction in HSTGCN (B.5) and building graphs (B.8); attention masks (PDFormer) reappear as input/temporal attention in DLSTM-SAE (B.3) and the CBL attention-GAN (B.7). The energy field trails the traffic field by roughly 2–3 years in adopting each generation — transformers entered traffic in 2020 (GMAN) and load forecasting in 2021 (B.2); adaptive graphs entered traffic in 2019 and EV/renewable forecasting in 2022–2023 (B.5, B.6).

2. **Decomposition vs. attention as competing philosophies.** Energy STLF long favored *signal decomposition* (VMD/EMD → per-mode learners → reconstruction, B.1) because load is a sum of physically meaningful periodic components; traffic favors *learned operators* because road dynamics are not separable into additive modes. The transformer generation (B.2, B.3) effectively replaces decomposition with attention-based component discovery, achieving MAPE 1.13% (B.2) — the same leap the traffic field got when attention replaced fixed graphs.

3. **From prediction to closed-loop control.** Traffic forecasting feeds route guidance and signal control; energy forecasting feeds MPC (B.4: forecast-in-the-loop MPC cut weekday mean peaks 47.0% vs. base and 3.3% vs. persistence on a 48-port station). The McClone result is the clearest demonstration in this dossier that **forecast quality alone is not the deliverable — the forecast must be embedded in an optimizer with hard constraints (SOC, charger limits)**, a pattern increasingly expected of smart-city ML.

4. **Data scale is the new bottleneck in both fields.** LargeST's 8,600-sensor benchmark and BDG2's 3,053 meters play identical roles; both revealed that models tuned on the small legacy benchmarks do not rank the same at scale. Both fields then converged on the same remedy: pre-training on cross-domain corpora (TimeGPT) or across-city data (the traffic foundation-model direction).

## C.3 Consolidated Comparison Table — Traffic Forecasting on METR-LA and PeMS-BAY

All values are **MAE / RMSE / MAPE(%)**, taken under the **identical STAEformer (CIKM 2023) protocol** (7:1:2 split, 12-step input, horizons at 15/30/60 min) for uniform comparability — this is the standard way to compare these models without mixing papers' native splits.

| Paper (Year) | Architecture | METR-LA 15 min | METR-LA 30 min | METR-LA 60 min | PeMS-BAY 15 min | PeMS-BAY 30 min | PeMS-BAY 60 min |
|---|---|---|---|---|---|---|---|
| STGCN (2018) | ST-Conv: temporal GLU + spatial GCN | 2.75 / 5.29 / 7.10 | 3.15 / 6.35 / 8.62 | 3.60 / 7.43 / 10.35 | 1.36 / 2.88 / 2.86 | 1.70 / 3.84 / 3.79 | 2.02 / 4.63 / 4.72 |
| DCRNN (2018) | Diffusion-conv seq2seq GRU | 2.67 / 5.16 / 6.86 | 3.12 / 6.27 / 8.42 | 3.54 / 7.47 / 10.32 | 1.31 / 2.76 / 2.73 | 1.65 / 3.75 / 3.71 | 1.97 / 4.60 / 4.68 |
| Graph WaveNet (2019) | Dilated gated TCN + adaptive diffusion conv | 2.69 / 5.15 / 6.99 | 3.08 / 6.20 / 8.47 | 3.51 / 7.28 / 9.96 | 1.30 / 2.73 / 2.71 | 1.63 / 3.73 / 3.73 | 1.99 / 4.60 / 4.71 |
| AGCRN (2020) | Node-adaptive params + learned adjacency GCRU | 2.85 / 5.53 / 7.63 | 3.20 / 6.52 / 9.00 | 3.59 / 7.45 / 10.47 | 1.35 / 2.88 / 2.91 | 1.67 / 3.82 / 3.81 | 1.94 / 4.50 / 4.55 |
| MTGNN (2020) | Mix-hop propagation + gated dilated TCN | 2.69 / 5.16 / 6.89 | 3.05 / 6.13 / 8.16 | 3.47 / 7.21 / 9.70 | 1.33 / 2.80 / 2.81 | 1.66 / 3.77 / 3.75 | 1.95 / 4.50 / 4.62 |
| GMAN (2020) | ST-attention encoder-decoder + transform attention | 2.80 / 5.55 / 7.41 | 3.12 / 6.49 / 8.73 | **3.44 / 7.35 / 10.07** | 1.35 / 2.90 / 2.87 | 1.65 / 3.82 / 3.74 | 1.92 / 4.49 / 4.52 |
| PDFormer (2024) | Masked spatial attention + delay-aware transform | 2.83 / 5.45 / 7.77 | 3.20 / 6.46 / 9.19 | 3.62 / 7.47 / 10.91 | 1.32 / 2.83 / 2.78 | 1.64 / 3.79 / 3.71 | 1.91 / 4.43 / 4.51 |
| STID (2022) | MLP + spatial/periodicity embeddings | 2.82 / 5.53 / 7.75 | 3.19 / 6.57 / 9.39 | 3.55 / 7.55 / 10.95 | 1.31 / 2.79 / 2.78 | 1.64 / 3.73 / 3.73 | 1.91 / 4.42 / 4.55 |
| **STAEformer (2023)** | **Vanilla transformer + spatio-temporal adaptive embedding** | **2.65 / 5.11 / 6.85** | **2.97 / 6.00 / 8.13** | **3.34 / 7.02 / 9.70** | 1.31 / 2.78 / 2.76 | **1.62 / 3.68 / 3.62** | **1.88 / 4.34 / 4.41** |

**Reading the table.** (1) The 15-minute horizon has been essentially saturated: the spread between the best (2.65) and worst deep model (2.85) is 0.20 MAE — within run-to-run variance for many implementations. (2) The meaningful separation is at **60 minutes**, where the range widens to 3.34–3.62 MAE: representation quality (STAEformer, MTGNN) and long-horizon mechanisms (GMAN's transform attention) dominate there. (3) **GMAN holds the best classic 60-min METR-LA MAE (3.44)** among pre-2021 models, while **STAEformer sets the overall best (3.34)** and the best PeMS-BAY numbers at every horizon. (4) PDFormer's strength does not appear on METR-LA (its native benchmarks are PeMS04/07/08, where it beats ASTGNN by 4.58% MAE on average and cuts inference time 80%) — a reminder that protocol choice, not architecture alone, determines apparent rankings, which is exactly the lesson LargeST (A.11) generalizes at 8,600-sensor scale.

## C.4 Key Takeaways for Smart-City Deployment

1. **If you need a robust default today:** an adaptive-graph model (Graph WaveNet/MTGNN-class) or STAEformer-class embedding+vanilla-transformer gives near-SOTA accuracy with simple training; PDFormer-class masked attention when propagation delays and long-range functional similarity matter (incidents, corridor management).
2. **Never evaluate on a single benchmark.** METR-LA rankings do not survive LargeST scale; energy models that win in-domain can collapse to 60–80% MAPE under cross-building transfer (B.8). Report both in-distribution and transfer settings.
3. **Forecasting is necessary but not sufficient.** The 47.0% peak reduction in B.4 came from embedding forecasts in constrained MPC, not from a better forecaster — smart-city projects should budget for the control layer and its constraint data (SOC, charger limits, transformer ratings) explicitly.
4. **Cold-start units should use pre-trained priors.** TimeGPT-style foundation models with a validation-loss gate (B.9) are the practical answer for the many buildings/substations/customers with scarce history — the regime where every bespoke deep model in this dossier is weakest.
5. **Expect the next step to be cross-domain pre-training.** Both fields are converging on the same pattern — large shared pre-training corpora, parameter-efficient adaptation, and metadata/graph-conditioned heads (region-specific in B.5, building-type-conditioned in B.8, sensor-metadata-conditioned in LargeST).

---

*End of dossier. All quantitative values are attributed to the specific paper, table, or re-evaluation protocol cited inline; where protocols differ (e.g., ASTGCN's original average-over-hour vs. later 12-horizon averages), the protocol is named explicitly because cross-protocol number comparisons are not valid.*
