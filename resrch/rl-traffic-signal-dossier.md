# Deep Technical Dossier: Reinforcement Learning for Traffic Signal Control & Urban Mobility

**Scope:** Full technical extraction (MDP formulations, architectures, training details, environments, baselines, quantitative results, limitations) for 16+ core RL-TSC papers, plus simulator comparison, survey taxonomy, and urban-mobility RL applications. All numbers are taken from the papers themselves (arXiv/publisher PDFs) as retrieved during research.

---

## SECTION A — PAPER-BY-PAPER DEEP DIVES

---

### A1. IntelliLight (Wei, Zheng, Yao, Li — KDD 2018)

**Citation:** *IntelliLight: A Reinforcement Learning Approach for Intelligent Traffic Light Control*, KDD'18, pp. 2496–2505.

**Problem setting:** Single intersection, 2-phase simplification (one of the earliest deep-RL TSC papers; explicitly motivated by lack of real-world data testing and lack of policy interpretation in prior work).

**(a) MDP formulation (exact):**
- **State (per lane i):** queue length L_i (vehicles with speed < 0.1 m/s count as waiting), number of vehicles V_i, updated waiting time W_i; plus an **image representation M** of vehicle positions on the intersection, the current phase P_c, and the next phase P_n. State vector = explicit features {L, W, P, V} concatenated with CNN-extracted image features.
- **Action:** binary — `a = 1`: switch light to next phase P_n; `a = 0`: keep current phase P_c (cyclic "keep-or-change" scheme).
- **Reward (Eq. 3):** a weighted sum of: (1) total queue length over approaching lanes, L = Σ L_i; (2) total delay D = Σ D_i, where per-lane delay D_i is computed from lane average speed vs. speed limit (Eq. 1); (3) signal-switching penalty; (4) throughput/vehicles passed; (5) total travel time. Formally written as
  `R = w₁·(−ΣL_i) + w₂·(−ΣD_i) + w₃·(−switch penalty) + w₄·(#vehicles passed) + w₅·(−travel time) + w₆·(−waiting time)` — a hand-tuned linear combination whose components are reported in the paper's analysis section; the reward range is (−∞, +∞), with an upper bound when all vehicles move freely.
- **Metrics:** average reward, average queue length, average delay, average duration (travel time on approaching lanes, seconds).

**(b) Network architecture:** Two convolutional layers process the vehicle-position image; their output is concatenated with the four hand-crafted features (L, W, P, V); this feeds fully-connected layers producing a shared traffic representation. The distinctive component is the **Phase Gate**: for each phase, a separate learning path maps the shared representation to Q(s,a). A gate controlled by the current phase P activates the corresponding branch (e.g., P=0 → left branch, P=1 → right branch). This explicitly separates decision processes per phase, prevents action bias, and improves fitting. A "Memory Palace" stores phase-action experiences separately to avoid data imbalance during training.

**(c) Training:** DQN with ε-greedy exploration. Two-stage training: offline phase using a fixed signal schedule to collect data, then online exploration phase where the agent controls lights and refines via ε-greedy.

**(d) Environment/data:** SUMO simulation fed with **real-world traffic from 1,704 surveillance cameras in Jinan, China, 08/01–08/31/2016**; >405 million vehicle records, >11 million unique plates; 935 locations, 43 four-way intersections, 24 intersections with continuous data used for experiments. Synthetic configs 1–4 (simple-changing, equally-steady, unequally-steady, complex) with Poisson arrivals.

**(e) Baselines:** Fixed-Time (FT), Self-Organizing Traffic Lights (SOTL), vanilla DRL (Li et al.).

**(f) Quantitative results (real-world, Table 10; ± = std):**

| Method | Reward ↑ | Queue Length ↓ | Delay ↓ | Duration (s) ↓ |
|---|---|---|---|---|
| FT | −5.727 ± 5.977 | 19.542 ± 22.405 | 3.377 ± 1.057 | 84.513 ± 60.888 |
| SOTL | −35.338 ± 65.108 | 16.603 ± 17.718 | 4.070 ± 0.420 | 64.833 ± 23.136 |
| DRL | −30.577 ± 26.242 | 54.148 ± 43.420 | 4.209 ± 1.023 | 166.861 ± 93.985 |
| **IntelliLight** | **−3.892 ± …** | **7.609 ± 10.238** | **2.730 ± 1.086** | **46.439 ± 50.487** |

Relative improvement over the best baseline: **reward +32%, queue −38%, delay −19%, duration −22%**. On synthetic configs, queue-length reductions of **81.8%–99.9%** vs. traditional methods are reported; aggregate figures cited in later surveys put travel-time reduction at **40.26%** and queue reduction at **47.6%** vs. conventional baselines.

**(g) Limitations:** Single-intersection, 2-phase only (not all-phase); heavy dependence on image input (aerial/camera views hard to obtain in real time at every intersection — a criticism later made by MPLight); hand-tuned multi-term reward with unclear weight sensitivity; no coordination with neighbors; evaluation in SUMO replaying camera-derived flows rather than closed-loop deployment.

---

### A2. PressLight (Wei, Chen, Zheng, Wu, Gayah, Xu, Li — KDD 2019)

**Citation:** *PressLight: Learning Max Pressure Control to Coordinate Traffic Signals in Arterial Network*, KDD'19, pp. 1290–1298.

**Core idea:** Ground RL elements (state & reward) in **max-pressure (MP) control theory** from transportation, which is provably throughput-maximizing.

**(a) MDP formulation (exact):**
- **Pressure (Eq. 2):** For intersection i, pressure aggregates per-movement pressure `w̃(l,m) = x^(l) − x^(m)` (queue on upstream incoming lane segment minus queue on connected downstream lane), summed over movements served by a phase: `θ(Ã, X) = Σ_{(l,m): a(l,m)=1} w̃(l,m)`.
- **State (observation):** current phase p; number of vehicles on each outgoing lane x^(m), m ∈ L_out; number of vehicles on each **segment** of every incoming lane x^(l)_k, l ∈ L_in, k = 1..K with **K = 3** segments per lane (segment 1 nearest the intersection).
- **Action:** choose phase p ∈ A at time t; **4 permissible phases**, one-hot encoded; **acyclic** action space (directly selects which phase greens next).
- **Reward (Eq. 3):** `r_i = −P_i` — negative pressure of intersection i. Minimizing pressure balances vehicle distribution and maximizes throughput.

**Theory:** Definition 5.2 (movement stability in the mean), Definition 5.3 (max-pressure policy), **Theorem 5.4**: without physical queue expansion, both MP policy and the RL policy stabilize the system under admissible demand; **Theorem 5.5** relaxes the no-queue-expansion assumption and still proves stabilization; §5.2.2 connects stabilization → max throughput → min travel time in arterial networks without U-turns.

**(b) Architecture:** Standard DQN over the concise pressure-aligned state (deliberately low-dimensional; paper argues complex image states increase learning time without gain when the reward is pressure).

**(c) Training:** Deep Q-learning; multi-agent (one agent per intersection), decentralized.

**(d) Environment:** **CityFlow**; 6-intersection arterial synthetic configs (LightFlat, LightPeak, HeavyFlat, HeavyPeak — flows synthesized from Jinan/Hangzhou statistics) + real arterials: Qingdao Rd. (Jinan), Beaver Ave. (State College, USA), 8th/9th/10th/11th Ave. (NYC). Metric: average travel time (s).

**(e) Baselines:** FixedTime (15 s/phase, random offset), GreenWave, MaxPressure (greedy), GRL, LIT.

**(f) Quantitative results (Table 4, avg travel time, seconds):**

| Method | LightFlat | LightPeak | HeavyFlat | HeavyPeak | Qingdao Rd | Beaver Ave | 8th Ave | 9th Ave | 10th Ave | 11th Ave |
|---|---|---|---|---|---|---|---|---|---|---|
| FixedTime | 93.29 | 109.50 | 325.48 | 246.25 | 317.40 | 336.29 | 432.60 | 469.54 | 347.05 | 368.84 |
| GreenWave | 98.39 | 124.09 | 263.36 | 286.85 | 370.30 | 332.06 | 451.98 | 502.30 | 317.02 | 314.08 |
| MaxPressure | 74.30 | 82.37 | 262.26 | 225.60 | 567.06 | 222.90 | 412.58 | 370.61 | 392.77 | 224.54 |
| GRL | 123.02 | 115.85 | 525.64 | 757.73 | 238.19 | 455.42 | 704.98 | 669.69 | 676.19 | 548.34 |
| LIT | 65.07 | 66.77 | 233.17 | 258.33 | 58.18 | 338.52 | 471.30 | 726.04 | 309.95 | 340.40 |
| **PressLight** | **59.96** | **61.34** | **160.48** | **184.51** | **54.87** | **92.00** | **223.36** | **149.01** | **161.21** | **140.82** |

Key deltas: HeavyFlat **160.48 vs LIT 233.17 (−31.2%)** and **vs MaxPressure 262.26 (−38.8%)**; Qingdao Rd **54.87 vs MaxPressure 567.06 (≈90% lower)** — MaxPressure's greediness fails under dynamic demand where RL's long-horizon optimization wins.

**(g) Limitations:** Simplified 4-phase arterial model; state limited to queues (no speeds/travel times); assumes downstream queue observability (hard without detectors on downstream approaches); greedy-MP-informed reward may be myopic under spillback; single-direction arterials rather than grids in main experiments.

---

### A3. CoLight (Wei, Xu, Zhang, Zheng, Zang, Chen, Zhang, Zhu, Xu, Li — CIKM 2019)

**Citation:** *CoLight: Learning Network-level Cooperation for Traffic Signal Control*, CIKM'19, pp. 1913–1922.

**(a) MDP formulation:**
- **State:** per-lane vehicle counts + current phase at the target intersection (PressLight-style local state; no neighbor concatenation — neighbor info enters through attention instead).
- **Action:** select next phase (acyclic phase selection).
- **Reward:** based on local queue length (queue-based negative reward), consistent with the LibSignal reproduction (`reward: queue`).
- **Coordination:** not via state concatenation but via **graph attention over neighbors**.

**(b) Architecture — graph attention equations (exact):**
1. **Observation interaction / interaction score:** e_ij computed from target intersection hidden state h_i and neighbor h_j (linear projections W_t, W_s with LeakyReLU attention as in GAT).
2. **Attention distribution (Eq. 4):** `α_ij = softmax(e_ij) = exp(e_ij/τ) / Σ_{j∈N_i} exp(e_ij/τ)`, where τ is a temperature factor and N_i is the neighborhood (top-|N_i| closest intersections by **road distance** or **node distance**; i itself ∈ N_i).
3. **Index-free neighborhood cooperation (Eq. 5):** `h^s_i = σ( W_q · Σ_{j∈N_i} α_ij (h_j W_c) + b_q )`, with W_c ∈ R^{m×c} source-embedding weights. The **weighted sum makes the representation index-free** — no fixed [E,W,N,S] ordering — resolving the conflicting-learning problem under parameter sharing (Fig. 1 example: major vs side-street neighbors).
4. **Multi-head attention:** H heads with separate {W_t, W_s, W_c}, averaged: `h^m_i = (1/H) Σ_h h^s_i`; **H = 5 heads** found best.
5. Two GAT layers expand cooperation scope: layer 1 = adjacent neighbors; layer 2 ≈ 8 intersections (upstream emphasis grows via learned α).
6. **Complexity:** O(m²L) time/space — independent of number of intersections → scalable to hundreds/thousands of signals.

**(c) Training:** DQN with shared parameters across agents; phase-gate-free (relies on attention for context).

**(d) Environment:** **CityFlow**; synthetic Grid3×3, Grid6×6 (uni- and bi-directional, 300 veh/lane/h on E–W, 90 on N–S); real: **D_NewYork 196 intersections** (Upper East Side Manhattan, taxi trips), **D_Hangzhou 16** (Gudang, camera data), **D_Jinan 12** (Dongfeng, camera data). Arrival stats: NY mean 240.79 veh/300s (std 10.08, max 274, min 216); Hangzhou 526.63 ± 86.70; Jinan 250.70 ± 38.21. Turning ratios 10% L / 60% S / 30% R.

**(e) Baselines:** FixedTime, MaxPressure, CGRL, Individual RL (no sharing), OneModel (shared, no neighbors), Neighbor RL (concatenate neighbors), GCN (static adjacency), CoLight-node (hop-distance neighborhood).

**(f) Quantitative results (Table 2, avg travel time, s):**

| Method | Grid6×6-Uni | Grid6×6-Bi | D_NewYork | D_Hangzhou | D_Jinan |
|---|---|---|---|---|---|
| FixedTime | 209.68 | 209.68 | 1950.27 | 728.79 | 869.85 |
| MaxPressure | 186.07 | 194.96 | 1633.41 | 422.15 | 361.33 |
| CGRL | 1532.75 | 2884.23 | 2187.12 | 1582.26 | 1210.70 |
| Individual RL | 314.82 | 261.60 | — | 345.00 | 325.56 |
| OneModel | 181.81 | 242.63 | 1973.11 | 394.56 | 728.63 |
| Neighbor RL | 240.68 | 248.11 | 2280.92 | 1053.45 | 1168.32 |
| GCN | 205.40 | 272.14 | 1876.37 | 768.43 | 625.66 |
| CoLight-node | 178.42 | 176.71 | 1493.37 | 331.50 | 340.70 |
| **CoLight** | **173.79** | **170.11** | **1459.28** | **297.26** | **291.14** |

**Average improvement: 6.98% (synthetic), 11.69% (real-world)** over SOTA (MaxPressure / Individual RL). Individual RL fails to scale to 196 intersections; Neighbor RL/GCN perform poorly because static importance assigned to upstream vs downstream ignores real-time flow direction.

**(g) Limitations:** Neighborhood scope hyperparameter (|N_i|, distance metric); attention assumes observable neighbor states; still queue-count-based state; reward not theoretically grounded like pressure; single-layer parameter sharing may underfit heterogeneous intersection geometries.

---

### A4. FRAP (Zheng, Xiong, Zang, Feng, Wei, Zhang, Li, Xu, Li — CIKM 2019)

**Citation:** *Learning Phase Competition for Traffic Signal Control*, CIKM'19 (arXiv:1905.04722).

**Core idea:** Two principles — **competition** (when two movements conflict, prioritize larger demand) and **invariance** (control should be invariant to flipping/rotation of traffic flow).

**(a) MDP formulation (exact, §3.2):**
- **State:** number of vehicles `f^v_i` on each traffic movement i (i = 1..8 for 4-approach × {L,S,R} with right-turn free) **and** current traffic signal phase as one bit `f^s_i` per movement signal (1 = green, 0 = red).
- **Action:** choose the phase for the next time interval; 8 paired-signal phases (A–H) in the all-phase setting (8-bit phase vector p).
- **Reward:** **average queue length of each traffic movement** (deliberately simple — paper focuses on model design).
- Objective: maximize `G_t = Σ_{m≥0} γ^m R_{t+m+1}` (Eq. 1).

**(b) Architecture (three stages, Eqs. 3–8):**
1. **Phase demand modeling:** per movement, two FC layers: `h^v_i = ReLU(W_v f^v_i + b_v)`, `h^s_i = ReLU(W_s f^s_i + b_s)`; `d_i = ReLU(W_h [h^v_i, h^s_i] + b_h)` (Eq. 3–4); parameters shared across all 8 movements. Phase demand `d(p) = d_i + d_j` for the two non-conflicting signals in p (Eq. 5).
2. **Phase pair embedding:** for each ordered pair (p,q), q≠p: **relation embedding** e(p,q) looked up from the phase competing matrix (partial-competition vs full-competition); **demand embedding** from concatenation [d(p), d(q)]. Volumes E ∈ R^{8×7×l1}, D ∈ R^{8×7×l2}.
3. **Phase pair competition:** K conv layers with **1×1 filters**: `H^r_k = ReLU(W^r_k H^r_{k-1} + b^r_k)`, `H^d_k = ReLU(W^d_k H^d_{k-1} + b^d_k)`; elementwise product `H_c = H^d_K ⊗ H^r_K`; `C = ReLU(W_c · H_c + b_c)` (Eq. 8) — rows = relative priority of phase p over opponents; sum rows → Q-value per phase; argmax = action.

**Sample-efficiency argument:** exploration space reduced from `64 × n^8` (DRL/IntelliLight) to **`16 × n^4`** samples (n = lane capacity).

**(c) Training:** **Ape-X distributed DQN** (parallel actors with diverse exploration + centralized learner); Bellman: `Q(s_t,a_t) = R(s_t,a_t) + γ max Q(s_{t+1}, a_{t+1})`.

**(d) Environment:** **CityFlow**; real datasets Hangzhou 1×1, Atlanta 1×5, Jinan; 8-phase and 4-phase settings; traffic flow flipping experiments (morning vs evening reversal).

**(e) Baselines:** DRL (Li et al.), IntelliLight, plus (in MetaLight reproductions) SOTL.

**(f) Quantitative results:** In the 8-phase setting on Jinan, FRAP achieves **66.40 s average travel time vs. best baseline IntelliLight 88.74 s**; per-intersection improvements of **25.17%–47.69%** across Jinan intersections; **33.20%** over IntelliLight on Hangzhou; **11.54%–21.49%** on Atlanta. 8-phase FRAP (66.40 s) beats its own 4-phase variant (81.97 s) because dynamic green allocation avoids wasted green. Transfer test: model trained on original flow applied to flipped/rotated flows achieves travel time nearly identical to fully re-trained models.

**(g) Limitations:** Single intersection (no explicit neighbor coordination); reward = average queue (not travel time); assumes paired-signal phases only (no single-signal phases — noted as necessary for spillback in multi-intersection settings); architecture tuned to 8-phase conflict structure.

---

### A5. MPLight (Chen, Wei, Xu, Zheng, Yang, Xiong, Xu, Li — AAAI 2020)

**Citation:** *Toward A Thousand Lights: Decentralized Deep Reinforcement Learning for Large-Scale Traffic Signal Control*, AAAI-20, pp. 3414–3421.

**Core idea:** = **PressLight state/reward (pressure)** + **FRAP network (phase competition)** + **global parameter sharing**, enabling city-scale decentralization.

**(a) MDP formulation:**
- **State:** per PressLight — current phase, outgoing-lane vehicle counts, segmented incoming-lane counts (pressure-aligned, "simple features like queue length available in the real world").
- **Reward:** negative average pressure (PressLight's theoretically grounded reward).
- **Action:** acyclic phase selection.
- **Design criteria** the paper demands of deployable RL: (1) scalability, (2) signal coordination, (3) data feasibility (only queue-like features).

**(b) Architecture:** FRAP backbone (phase demand → pair embedding → 1×1-conv competition), **all agents share one network** — justified because FRAP's structure-agnostic design encodes the universal "phase competition" logic regardless of local geometry; naive sharing of non-FRAP models degrades (major vs minor intersection).

**(c) Training:** Decentralized DQN (one shared model), pressure reward; parameter sharing accelerates convergence (fewer episodes).

**(d) Environment:** **CityFlow**. Synthetic 4×4 grid (four 300-m segments, turning 10/60/30, four demand configs: Flat σ=0.3 / Peak σ=0.6 × two arrival rates). **Real: Manhattan, NYC from OpenStreetMap with 2,510 signalized intersections**; flow from NYC TLC taxi trips scaled ×k → **≈25,156 vehicles/hour**; vehicles spawn/vanish at any edge; non-uniform real demand.

**(e) Baselines:** FixedTime, MaxPressure, GCN, NeighborRL, GRL, PressLight, FRAP (no-pressure).

**(f) Quantitative results — Manhattan 2,510 lights (Table 3):**

| Model | Travel Time (s) | Throughput |
|---|---|---|
| FixedTime | 974.23 | 1940 |
| MaxPressure | 497.76 | 2143 |
| GRL | — (cannot scale) | — |
| GCN | 653.45 | 5045 |
| NeighborRL | — (cannot scale) | — |
| PressLight | 600.42 | 3447 |
| FRAP | 512.70 | 6346 |
| **MPLight** | **472.51** | **6932** |

Synthetic 4×4: **up to 19.2% travel-time improvement over PressLight**; **13% over MaxPressure** (RESCO re-implementation later reported a comparable 11%). MPLight vs FRAP on Manhattan: 472.51 vs 512.70 s (−7.8%) with +9.3% throughput.

**(g) Limitations:** Pressure assumes downstream queue observability at city scale; shared model may still underfit extreme geometry heterogeneity; Manhattan demand is scaled taxi data (not calibrated counts); GRL/NeighborRL excluded for scalability (fairness caveat); preliminary real-world deployment only.

---

### A6. AttendLight (Oroojlooy, Nazari, Hajinezhad, Silva — NeurIPS 2020)

**Citation:** *AttendLight: Universal Attention-Based Reinforcement Learning Model for Traffic Signal Control*, NeurIPS 2020 (arXiv:2010.05772).

**Core idea:** One **universal** model for any #roads/lanes/phases via two attention modules — eliminating per-intersection retraining.

**(a) MDP formulation:**
- **State:** per-lane traffic features (queue/vehicle counts per lane; input-channel size 4 in the embedding) — variable-length across intersections.
- **Action:** next phase (variable number of phases; handled by action-attention returning a probability per action).
- **Reward:** tied to average travel time (ATT); policy-gradient objective.

**(b) Architecture (supplement A.2):** five trainable components: (1) **embedding layer** — 1-D conv, input channels 4, kernel size & stride 1, output dim d (affine map of lane characteristics); (2) **State-Attention** — linear transforms for query/keys, output d, produces per-phase representations z_p^t handling variable roads/lanes; (3) **RNN** — single-layer **LSTM**, hidden dim d; (4) **FC + ReLU**; (5) **Action-Attention** — same linear Q/K transforms, outputs action probabilities. d = 128 (single-env), d = 256 (multi-env). No structured hyperparameter tuning performed (authors' note).

**(c) Training:** policy-gradient based method (actor-critic style); two regimes: (i) single-environment train/test; (ii) multi-environment: train on **42 instances**, test on **70 unseen instances**.

**(d) Environment:** CityFlow; **112 intersection instances** from 11 topologies: 3- and 4-approach roads; 1/2/3 lanes per direction; uni-/bi-directional; varying phases; synthetic congestion rates + real traffic from **Atlanta and Hangzhou**.

**(e) Baselines:** FixedTime, MaxPressure, SOTL, DQTSC-M, FRAP.

**(f) Quantitative results (avg ATT improvement):**
- **Single-env:** best on **107/112 cases**; average improvement **46% vs FixedTime, 39% vs MaxPressure, 34% vs SOTL, 16% vs DQTSC-M, 9% vs FRAP**.
- **Multi-env (zero retraining on 70 unseen):** best on 57 cases; **39% / 32% / 26% / 5% / −3%** vs the same baselines (i.e., within 3% of per-intersection-tuned FRAP while being one universal model).

**(g) Limitations:** Single intersection (no network coordination — listed as future work); performance gap to FRAP in multi-env regime (−3%); relies on configurations appearing in training; no structured HPO; policy-gradient less sample-efficient than value-based methods in small discrete action spaces.

---

### A7. PDLight (Zhao, Hu, Wang — arXiv 2009.13711, 2020)

**Citation:** *PDLight: A Deep Reinforcement Learning Traffic Light Control Algorithm with Pressure and Dynamic Light Duration*.

**(a) MDP formulation (exact):**
- **PRCOL (Eq. 1):** `P_i = N_in · (1 − N_out / N_max)` — pressure of movement i where N_in = vehicles on incoming lane, N_out = vehicles on outgoing lane, **N_max = max vehicles fitting on the lane**. Corrects MP's blind spot: when the outgoing lane is full, green is wasted.
- **State:** **12-dimensional vector** = number of vehicles on the 12 incoming lanes (4 approaches × 3 lanes), plus current phase.
- **Action:** 4 phases **plus green duration** (Fixed: 10 s; Dynamic: 10–20 s computed from `N_pass = min(N_in, N_left)`, `N_left = N_max − N_out`, acceleration a = 2 m/s², max speed v = 40 km/h, minimum gap l_g).
- **Reward (Eqs. 2–3):** `r_i = −P_i`, total `R = Σ_i r_i`.
- Coordination via GAT (as in CoLight).

**(b) Architecture:** DQN + graph attention for neighbor communication; phase with minimum PRCOL intersection pressure selected as next green.

**(c) Training (exact hyperparameters):** ε decays **0.8 → 0.2**; **γ = 0.8**; replay capacity **10,000**; learning rate **0.001**; target network updated every **5 steps**; episode length **3,600 s**; yellow **5 s** between phases.

**(d) Environment:** CityFlow; two synthetic + two real datasets (**Hangzhou, New York**).

**(e) Baselines:** PressLight, CoLight (both fixed and dynamic green duration settings).

**(f) Results:** Lower average travel time than PressLight and CoLight under **both fixed and dynamic** duration settings; PRCOL avoids "vehicles cannot completely pass due to limited outgoing capacity" failure mode; throughput increased. (Paper reports qualitative superiority with tables per dataset; exact per-cell numbers not reproduced here as the arXiv v1 tables were partially graphically encoded.)

**(g) Limitations:** N_max is a static capacity estimate (ignores turning conflicts at downstream); 12-dim state ignores neighbor queues directly (relies on GAT); DQN only; dynamic duration formula assumes static queues at decision time.

---

### A8. MetaLight (Zang, Yao, Zheng, Xu, Xu, Li — AAAI 2020)

**Citation:** *MetaLight: Value-based Meta-reinforcement Learning for Traffic Signal Control*, AAAI-20.

**(a) MDP formulation:**
- Task = MDP per intersection `S_i, A_i, R_i, γ_i, H_i`; Q(s,a; f_θ) = E[r_i(t) + γ_i r_i(t+1) + … | s_i(t)=s, a_i(t)=a] (Eq. 1).
- Base model **FRAP++**: state = number of vehicles + signal phase per approaching lane; action = next phase; **reward = average queue length on approaching lanes**.
- FRAP++ changes vs FRAP: (1) phase demand uses **average** (not sum) over lane demands → lane-count agnostic; (2) **per-step mini-batch updates** (FRAP updated only per episode, violating DQN's one-step update).

**(b) Meta-learning equations:**
- **Individual-level adaptation (Eq. 6):** `θ_i ← θ_i − α ∇_θ L(f_θ; D_i)` at each timestep (fast DQN-style adaptation per intersection).
- **Global-level adaptation (Eq. 7):** `θ_0 ← θ_0 − β ∇_θ Σ_i L(f_θ; D_i)` — meta-learner updates shared initialization θ_0 periodically over a batch of tasks.
- Alternation of the two replaces vanilla MAML (which the authors found only marginally better than random init for value-based RL).

**(c) Training hyperparameters:** learner & meta-learner lr = **0.001**; episode = 3600 s; interaction interval 10 s; learner updates after each interaction with **30 samples, 1 epoch**; meta-learner updates every **10 learner updates**. (MAML comparison: 1000 samples, 100 epochs per episode-end update.)

**(d) Environment:** CityFlow; four real datasets — **Hangzhou, Jinan, Atlanta, LA**; training on **26 intersections in Hangzhou**; three meta-test protocols: (1) change #intersections, (2) change #intersections + action schemes, (3) + change city. Action schemes vary phase configurations (e.g., 4a/4b/… settings).

**(e) Baselines:** Random init FRAP++, Pretrained, MAML (on FRAP), SOTL.

**(f) Quantitative results:**
- Task-1 (homogeneous, only #intersections changes): average improvement **5.52%** over best baseline (Pretrained/MAML) — modest because overfitting is mild.
- Task-2 (heterogeneous phase settings, unseen in training): **22.57% average improvement**; MetaLight outperforms in most scenarios; MAML ≈ Random (unstable policy-based meta-update on value-based base model).
- Single-model advantage: one initialization serves all scenarios, whereas Pretrained must select a suitable model each time.

**(g) Limitations:** Value-based meta-RL gains small in homogeneous settings; single-intersection focus (multi-intersection cooperation left as future work); FRAP++ reward still queue-based; meta-training requires diverse task distribution.

---

### A9. π-Light (Gu, Zhang, Liu, Gao, Li, Zhou — AAAI 2024)

**Citation:** *π-Light: Programmatic Interpretable Reinforcement Learning for Resource-Limited Traffic Signal Control*, AAAI-24, pp. 21107–21115.

**Core idea:** Replace black-box DRL with **human-readable programs** searched via MCTS in a DSL — interpretable, deployable on edge hardware, generalizable across cities.

**(a) MDP formulation:**
- **Observation features:** (1) VehicleCount per lane, (2) WaitVehicleCount per lane, (3) number of vehicles within x meters of the intersection (InLane* features).
- **Policy structure (Algorithm 1):** fixed program template `E_base` (MaxPressure-inspired): compute priority value **v** for each lane link, then phase score = Σ_{lane links in phase} v, action = argmax phase. **Learning reduces to finding program E that computes v.**
- **Action:** next phase (shared program across all intersections in a region).
- **Program evaluation reward:** **reciprocal of average vehicle travel time** over one episode.

**(b) Architecture / search method:**
- **DSL:** modules P = sequence of A (instruction), IT (if-then), ITE (if-then-else) — recursive (ITE inside branches), unlike fixed templates of Imitation-learning predecessors. Instructions are atomic: e.g., `v += InLaneWaitVehicleCount`. Deliberately **no feature interactions** (e.g., products) for interpretability.
- **MCTS:** node = program, edge = transformation rule. (1) **Selection** via UCT: `UCT = r(j) + C·sqrt(ln N(k)/N(j))`; (2) **Expansion**: randomly pick entity (A or P), apply random transformation rule → new executable program; (3) **Backpropagation**: `r(k) ← max(r(j), r(k))` (max, not mean — seeking best program); visit counts updated.
- **Constant optimization:** Bayesian optimization for numeric constants (c, x) inside programs.

**(c) Training:** Not gradient-based — program search + BO; no neural weights to train; evaluation = running one environment episode.

**(d) Environment:** Real-world datasets — **Jinan, Hangzhou1, Manhattan** (cross-city generalization runs: train Hangzhou1 → test Manhattan); CityFlow-based.

**(e) Baselines:** DRL methods (DQN-family, CoLight-class) — paper reports outperforming DRL baselines on tested networks.

**(f) Quantitative results:** Consistently outperforms baseline DRL approaches on multiple road networks; **cross-city transfer** (e.g., Hangzhou → Manhattan) retains performance where DRL degrades; memory/CPU footprint analysis shows direct deployment on **extremely limited edge devices** (KB-scale program vs. MB-scale network). On the JN-3 benchmark leaderboard (independent reproduction), π-Light registers ATT 226.37 s vs FixedTime 371.43 s and MPLight 302.58 s.

**(g) Limitations:** DSL expressiveness bounded by predefined operators/templates (later LLM-guided evolution work criticizes this); MCTS reward = 1/ATT is myopic per-episode; constant optimization adds a second loop; program search cost grows with program depth.

---

### A10. MPLight Variants / IPDALight / MNLight (dynamic-duration line)

**IPDALight (Zhao, Ye, Ding, Wang, Wei, Chen — J. Systems Architecture 123:102374, 2021/2022):**
- **Intensity** concept (max-pressure-inspired): ensures reward and state accurately reflect vehicle status; **phase-duration-aware** — fine-tunes green duration with neighbor coordination for GreenWave.
- Algorithm: deep Q-learning (DQN) with intensity-based reward/state + neighbor-informed duration control.
- Results: better ATT and GreenWave than SOTA RL (PressLight/CoLight family) with **much faster convergence** on synthetic and real scenarios.
- **MonitorLight** (CIKM 2022) later beat IPDALight by **2.84% (real) and 5.71% (synthetic) ATT**, with **36.87% fewer episodes to start converging** and **34.58% better jumpstart**, using "mixed pressure" (stationary + moving vehicles) and a phase-duration-aware PDA-TSC formulation.

**MNLight / Memory-Network Light (Kong, Lu, Yang, Zhang — ITSC 2022):** adds **LSTM dual branches** to DQN to condition Q on history states/actions — addresses DQN's memoryless state assumption; shown superior to existing methods.

**PRGLight (Zhao, Hu, Wang — IJCAI RL4ITS workshop 2021):** pressure-based reward + **GNN** with dynamic phase duration from real-time **and predicted** traffic state (GNN-based prediction).

**DynLight (arXiv 2204.03471):** multi-level: **Max-QueueLength (M-QL)** chooses phase; **DQN chooses duration**; DynLight-C swaps M-QL for a cyclical policy for deployability; argues avg travel time/throughput are unfair metrics and addresses cyclical-phase deployment constraints.

---

### A11. HiLight (Xu, Wang, Wang, Jia, Lu — AAAI 2021)

**Citation:** *Hierarchically and Cooperatively Learning Traffic Signal Control*, AAAI-21, pp. 669–677.

**Motivation:** Average travel time (true objective) is a **long-horizon delayed reward**; proxy rewards (queue/wait/delay) can deviate from it across networks. Also: how to cooperate toward the *network* travel-time objective.

**(a) MDP formulation:**
- **Observation (sub-policy):** concatenation of three vectors: current phase (one-hot), next phase (one-hot, determined by cycle), number of vehicles on incoming lanes.
- **Action (all RL baselines in paper):** whether to change to next phase in the cycle; **action interval = 5 s**.
- **Hierarchy:** every **T timesteps**, controller selects a sub-policy; sub-policy rewarded every timestep; controller rewarded every T timesteps.
- **Sub-policies (3):** each optimizes a short-term target — **queue length, waiting time, delay** (pressure optional).
- **Rewards:** controller optimizes **local travel time** and **neighborhood travel time** with **adaptive weighting** via **multi-critic**: local critic V^l and neighborhood critic V^n. Ablations: LocalCritic (local only), NBHDCritic (neighborhood only), StaticWeight (fixed λ).

**(b) Architecture:** controller = PPO over sub-policy selection; sub-policies = value-based (DQN-style) agents. Network: **3 convolutional layers; MLP with 3 layers, units (32,32); learning rate 0.001 for V^l and V^n** (AAAI appendix hyperparameter table).

**(c) Training:** PPO for controller + DQN sub-policies; 3 random seeds averaged after convergence.

**(d) Environment:** **CityFlow**; four real datasets: **Jinan 12 (4×3), Hangzhou 16 (4×4), Manhattan 48 (16×3), Shenzhen 33 (non-grid, weekday D & weekend E, 10,000 s)**; Jinan/Hangzhou/NY flows from camera/taxi data; 3600 s span for the first three.

**(e) Baselines:** FixedTime, SOTL, MaxPressure, PressLight, CoLight, IQLQ/IQLW/IQLD (independent Q on queue/wait/delay) + ablations. (MPLight omitted — "cannot run successfully on latest CityFlow"; MetaLight omitted — single-intersection.)

**(f) Quantitative results (Table 2 — avg travel time s / throughput):**

| Method | Jinan TT | Hangzhou TT | Manhattan TT | Shenzhen-D TT | Shenzhen-E TT | Jinan TP | Hangzhou TP | Manhattan TP | SZ-D TP | SZ-E TP |
|---|---|---|---|---|---|---|---|---|---|---|
| FixedTime | 749 | 762 | 1649 | 3821 | 3886 | 3399 | 1947 | 192 | 32 | 187 |
| SOTL | 1350 | 1413 | 1686 | 3854 | 3972 | 1480 | 2119 | 148 | 20 | 147 |
| MaxPressure | 397 | 352 | 443 | 3838 | 3873 | 5465 | 10428 | 2349 | 26 | 198 |
| PressLight | 382 | 425 | 1369 | 2220 | 1444 | 5517 | 9971 | 587 | 841 | 2246 |
| CoLight | 320 | 359 | 278 | 1574 | 1099 | 5688 | 10394 | 2615 | 1267 | 2999 |
| StaticWeight | 313 | 260 | 262 | 379 | 285 | 5725 | 11011 | 2631 | 2377 | 3968 |
| **HiLight** | **290** | **252** | **251** | **337** | **223** | **5769** | **11063** | **2635** | **2482** | **4088** |

HiLight vs CoLight: Jinan −9.4%, Hangzhou −29.8%, Manhattan −9.7%, Shenzhen-D −78.6%, Shenzhen-E −79.7%; vs FixedTime on Shenzhen-E: 223 vs 3886 s (−94%). PressLight collapses in Manhattan (1369 s) — pressure proxies misalign with travel time there.

**(g) Limitations:** Cycle-constrained action (not fully acyclic); T (controller period) is a hyperparameter; neighborhood definition (fixed radius) hand-set; requires training 3 sub-policies + controller (more compute); Shenzhen flows from cameras with simplification.

---

### A12. IG-RL (Devailly, Larocque, Charlin — IEEE TITS 2021, arXiv:2003.05738)

**Citation:** *IG-RL: Inductive Graph Reinforcement Learning for Massive-Scale Traffic Signal Control*, IEEE T-ITS (2021), DOI 10.1109/TITS.2021.3070835.

**Core idea:** GCN over a **dynamic object-level graph** (vehicles, lanes, signals as nodes) → **inductive** policy with constant parameter count, zero-shot transferable across networks.

**(a) MDP formulation:**
- **Decomposition:** road network decomposed into small local MDPs (one per controller); independent Q-learning (IQL) with a **shared policy** applied decentralized.
- **Graph:** nodes = objects (vehicle with vectorized features e.g. speed; lane; traffic signal controller); edges = physical connections (vehicle↔current lane, lane↔intersection...). Computational graph adapts to road-network state including moving vehicles.
- **Reward:** local queues (Eq. 2 of paper) — coordination limited by design (authors note this as future work).
- **Action-values:** TSC node embeddings → Q-values per action.

**(b) Architecture:** GCN (initial node embeddings from observable features → message passing → TSC node embedding → Q-head); trained end-to-end by backprop of **TD error** (standard DQN loss). Two variants: **G-IG-RL-V** (vehicle-level granularity) and **G-IG-RL-L** (lane-level).

**(c) Training:** DQN/IQL; generalist trained on random synthetic networks; specialist trained on target network.

**(d) Environment:** SUMO; synthetic random road networks for training; evaluation includes **zero-shot transfer to Manhattan with 3,971 traffic signal controllers** — "by far the largest RL-ATSC experiment to date."

**(e) Baselines:** MARL-IQL, dynamic heuristics (greedy/max-pressure-style), fixed-time.

**(f) Quantitative results:** G-IG-RL-L controls **3,971 signals with a single GPU and only 11,076 parameters**; total instantaneous delay shows slower congestion growth and lower steady-state congestion than all scalable baselines; generalist outperforms specialist on unseen regimes; outperforms MARL-IQL and domain heuristics on synthetic networks. (Follow-up MuJAM, arXiv 2208.00659, adds model-based joint-action modeling + coordination with cyclic/acyclic constraints.)

**(g) Limitations:** Local-queue reward limits coordination (explicitly acknowledged); shallow GCN suffices only because reward is local; robustness to sensor failure/unobserved data untested; approximate delay metric used for Manhattan comparison.

---

### A13. SocialLight (Goel, Zhang, Damani, Sartoretti — AAMAS 2023)

**Citation:** *SocialLight: Distributed Cooperation Learning towards Network-Wide Traffic Signal Control*, AAMAS 2023, pp. 1551–1559 (arXiv:2305.16145).

**Core idea:** Distribute COMA's counterfactual credit assignment into **locally-centralized critics** over overlapping neighborhoods — scalable cooperation without a global critic.

**(a) MDP formulation:**
- **Local state per agent:** incoming queue lengths, current local traffic phase, average waiting time of queued vehicles, **pressure** (all measurable via induction-loop detectors).
- **Reward:** **queue lengths** (local neighborhood reward; paper cites Zhang et al. 2022 showing queue superior to other local formulations).
- **Action:** phase selection.
- **Advantage (naive COMA local version):** `A = Q_φ(z^t_{V_i}, a^t_{V_i}) − E_{a^t_i} Q_φ(z^t_{V_i}, a^t_{V_i})` — baseline marginalizes agent i's action over the neighborhood joint action; **modified advantages decouple neighbors' actions** from the computed advantage to reduce gradient variance.

**(b) Architecture:** **A3C** framework; each agent has an actor + local critic with **parameter sharing**; critic conditioned on joint neighborhood observation z^t_{V_i} and one-hot actions of *other* agents a^t_{V_i−i}, outputs a vector of length |A| (COMA-style) so the advantage is a single dot product with actor outputs. Fixed neighborhood size ⇒ O(1) critic input scaling.

**(c) Training:** asynchronous distributed actors; fully decentralized training.

**(d) Environment:** **both SUMO and CityFlow** (first work to show effective performance on both). CityFlow real datasets: Jinan 12 (3×4), Hangzhou 16 (4×4), **New York 196 (28×7)** — 3 Jinan flows, 2 Hangzhou, 2 NY. SUMO: Manhattan grid.

**(e) Baselines:** FixedTime, MaxPressure, CoLight, MPLight, AttentionLight; SUMO: Greedy, IA2C, MA2C, IQL-LR, A3C, A3C(no reward shaping).

**(f) Quantitative results — CityFlow (Table 1, avg travel time s; gain vs best baseline):**

| Method | NY-1 | NY-2 | HZ-1 | HZ-2 | JN-1 | JN-2 | JN-3 |
|---|---|---|---|---|---|---|---|
| FixedTime | 1397.37 | 1660.29 | 432.32 | 359.44 | 364.36 | 289.74 | 316.69 |
| MaxPressure | 1177.75 | 1535.77 | 262.35 | 348.68 | 275.79 | 223.06 | 234.93 |
| CoLight | 1221.77 | 1476.18 | 271.07 | 297.26 | 276.33 | 237.14 | 278.16 |
| MPLight | 1168.49 | 1597.24 | 343.47 | 282.14 | 300.93 | 259.10 | 261.45 |
| AttentionLight | 978.62 | 1571.68 | 259.62 | 284.75 | 268.68 | 212.76 | 216.34 |
| **SocialLight** | **760.94** | **1114.47** | **255.68** | 301.16 | **226.21** | **209.81** | **205.38** |
| **Gain** | **22.23%** | **24.53%** | **1.54%** | — | **15.68%** | **1.41%** | **5.09%** |

**SUMO Manhattan (Table 2, mean (std)):** SocialLight trip time **309.81 (243.95)** vs A3C 395.04, MA2C 597.88, Greedy 885.47; queue **0.74 (0.69)** vs 1.71/2.24/5.00; intersection delay **10.07 (9.02)** vs 38.23/21.96/60.97; cumulative delay 106.51 vs 184.60/325.02/595.78; speed 5.36 m/s vs 4.55/2.31/1.56.

Gains **≥20% over AttentionLight/CoLight on both New York sets** (196 agents); modest gains on small Jinan/Hangzhou attributed to **saturation** (classical MaxPressure already near-optimal there).

**(g) Limitations:** Small-network saturation limits measurable gains; queue-based local reward; neighborhood radius fixed a priori; A3C async training variance; no explicit safety/compliance constraints.

---

### A14. OffLight (Bokade, Jin — arXiv 2411.06601, 2024; IEEE CASE 2025)

**Citation:** *OffLight: An Offline Multi-Agent Reinforcement Learning Framework for Traffic Signal Control*.

**Motivation:** online MARL training is costly/risky for deployment; offline RL faces **heterogeneous behavior policies** in real TSC datasets (mixed rule-based/greedy/learned controllers).

**(a) MDP formulation:**
- Standard offline MARL: dataset of transitions from behavior policy π_b; target policy π_θ to optimize.
- **State:** local observations aggregated across intersections via GAT (spatial) + LSTM (temporal) encoders; parameter sharing among agents.
- **Action:** phase selection.
- **Behavior policy model — GMM-VGAE:** Gaussian Mixture Model Variational Graph Autoencoder; latent space = mixture of Gaussians disentangling distinct control regimes; encoder maps (observations, past actions) → structured latent z; decoder reconstructs policy distributions.

**(b) Key equations:**
- **Importance sampling weight (Eq. 6):** `w^k_IS,t = (1/N) Σ_{n=1}^{N} π^i_θ(a^i_t | h^i_t) / π^i_b(a^i_t | h^i_t, z_t)` — reweights transitions by target/behavior likelihood ratio.
- **Return-Based Prioritized Sampling (RBPS):** prioritizes high-return episodes.
- **Combined weight:** product `w_IS,t · w_RBPS` — only transitions both relevant to π_θ *and* from successful episodes get significant weight.

**(c) Training:** offline actor-critic MARL with IS + RBPS; GAT+LSTM spatio-temporal encoder; GMM mixture components for policy diversity.

**(d) Environment:** real-world urban scenarios: **Jinan (12 intersections), Hangzhou (16), Manhattan (196)**; datasets with mixed-quality/heterogeneous behavior policies.

**(e) Baselines:** existing offline RL methods (CQL-family / behavior-regularized MARL as implemented in paper's comparisons).

**(f) Quantitative results:** **up to 7.8% reduction in average travel time** and **11.2% reduction in queue length** vs state-of-the-art offline RL, especially on mixed-quality datasets; ablations confirm GMM-VGAE, IS, RBPS each contribute; scales to 196 intersections.

**(g) Limitations:** Depends on behavior-policy coverage (no support ⇒ no correction); OPE not formalized as a separate estimator (IS weights used inside training rather than as standalone OPE); offline ceiling below well-trained online RL; GMM component count is a hyperparameter.

---

### A15. Traffic-R1 (Zou, Yang, Chen, Hao, Chen et al. — ACL 2026 / arXiv 2508.02344)

**Citation:** *Traffic-R1: Reinforced LLMs Bring Human-Like Reasoning to Traffic Signal Control Systems*, ACL 2026 (Vol. 1 Long Papers), DOI 10.18653/v1/2026.acl-long.995.

**Core idea:** A **3B-parameter LLM foundation model** for TSC with zero-shot generalization, edge inference, and explainable CoT — trained by two-stage agentic RL (GRPO).

**(a) MDP / RL formulation:**
- **State tokenization:** intersection state rendered into a structured text prompt (template with format instructions); **lane aggregation** — lanes with identical traffic movements merged to reduce state-space complexity; **mandatory pedestrian-crossing phases** injected during peak hours.
- **Action:** signal phase decision generated as part of structured output (reasoning + answer); actions mutually exclusive.
- **Offline rule-based reward:** `R(x,y) ∈ [0,1] = w_acc·R_acc + w_format·R_format`; **R_acc = 1 only when generated action exactly matches expert action**; **R_format = 1 only when y fully adheres to reasoning/answer format** (anti-reward-hacking design: clear, simple, cheap).
- **Online stage:** action rewards derived from simulated traffic feedback (queue/travel-time outcomes).
- **Policy optimization: GRPO** — for prompt x_i with k sampled completions, group-normalized advantages center rewards within the group (reduces variance, no value network): advantage ∝ `r_i^(j) − mean_j(r_i^(j))`.

**(b) Architecture:** Qwen2.5-3B backbone; two-stage agentic RL fine-tuning (offline expert-alignment → online simulation exploration); generates CoT + action jointly; **asynchronous communication network** for multi-intersection message passing (mimicking human traffic agents); multimodal sensing: fine-tuned **Grounding DINO** on 2D roadside cameras + **mmWave radar** for distance.

**(c) Training:** GRPO rollouts with template prompts; self-generated training samples (avoids catastrophic forgetting from synthetic distillation); retains general language skills.

**(d) Deployment (exact):** Chinese Tier-1 city (withheld), **10 interconnected intersections** in a high-volume commercial district; four-way arterials spaced **600–800 m**; **>55,000 vehicles/drivers daily**; peak throughput **>21,000 vehicles per intersection**. Hybrid dispatch: LightGBM (30-day history + spatio-temporal embeddings) forecasts next-day flow → Traffic-R1 generates preliminary timing plan → **human experts approve** before implementation; online pipeline reserved for expert-supervised incident response. Centralized server: **NVIDIA Tesla T40 24G, <2 s average inference latency, 437 output tokens average**; quantization path to low-power edge devices.

**(e) Baselines:** manual human control (production A/B); in-simulation: traditional RL controllers, GPT-4o, other LLM-TSC methods.

**(f) Quantitative results:**
- **Six-week A/B test** (systems alternated weekly; metrics only weekday 16:00–19:30): Manual avg queue **34.5** → Traffic-R1 **31.3 (−9.3%)**; max queue **50.3 → 48.1 (−4.4%)**; working hours **2+ → 0.5+ (~75% reduction)**.
- Abstract-level claims: **>55,000 drivers served daily, average queues shortened >5%, operator workload halved**; zero-shot transfer to new road networks and OOD incidents; matches/exceeds GPT-4o and training-intensive RL controllers on benchmarks (e.g., JN-3 ATT 287.78 s vs MPLight 302.58, PressLight 331.65, FixedTime 371.43 on the independent SOTA2 leaderboard).

**(g) Limitations:** Human-in-the-loop approval required for routine plans (not fully autonomous); only 10 intersections in production; A/B alternation weekly (temporal confounds partially mitigated but not eliminated); token latency (2 s) requires offline/forecast-driven dispatch rather than per-second closed loop; single-city deployment; reward hacking mitigated but format rewards can dominate if weights poorly chosen.

---

### A16. G2P-XLight (Liao, Mei, Zhang, Chen — arXiv 2503.20205, 2025)

**Citation:** *Generalized Phase Pressure Control Enhanced Reinforcement Learning for Traffic Signal Control* (G2P + G2P-XLight template; G2P-MPLight, G2P-CoLight).

**(a) State equations (exact):**
- Queue: `Q(l) = |{C_k | C_k ⊏ l}|`; homogeneous-lane set queue `Q(L) = Σ_{l∈L} Q(l)` (Eq. 1–2).
- **Effective range:** `L^r_max = min(V^c_max, V^r_max) · Δt` (Eq. 3) — max distance vehicles can travel before next signal change (c = free-flow speed, r = speed limit, Δt = actuated phase duration).
- **Truncated queue:** `Q^+(L→) = Σ_{l∈L→} |{C_k | D(C_k, I) ≤ L_max ∧ C_k ⊏ l}|` (Eq. 4).
- **Traffic movement pressure (Eq. 5):** `P{(L→, L)} = min( P(L|L→)·Q(L→), β ) − Q(L)`; with β = truncated-queue turn expectation (Eq. 6) simplifies to (Eq. 7 always holds ⇒ **Eq. 8**):
  `P{(L→, L)} = P^+(L | L→) · Q^+(L→) − Q(L)`
- **Generalized turn movement pressure (Eq. 9) — turn-probability-free:**
  `P{T_j} = Q(L'_j) − Q^−(L'_j) − Σ_{L∈R_out,j} Q(L)`, where residual queue `Q^−(L→) = Σ_l |{C_k | D(C_k,I) > L_max ∧ C_k ⊏ l}|` (Eq. 10). This closed form needs **no knowledge of turn probabilities** — critical for real deployment.
- **Generalized phase pressure (Eq. 11):** `P{s_i} = Σ_{T_j ∈ s_i} P{T_j}` (sum over the two movements of a phase).
- **G2P control:** `s* = argmax_{s_i∈S} P{s_i}` (Algorithm 1); **Theorem 1:** G2P control is **stabilizing** whenever average demand d is feasible (proof via routing/flow conservation Eqs. 12–16, queue-stability in the mean).

**(b) G2P-XLight RL formulation:**
- **State (Eq. 18):** `O_TM = { P{T^↓}, P{T^←}, P{T^↑}, P{T^→}, P{T^↰×4}, P{T^↱×4} }` — 12 turn-movement pressures (dimension = intersection config), combined with current phase (FRAP-style) + advanced traffic state (Zhang et al. 2022 effective-range features) → `O^G2P_t`.
- **Action:** phase s* ∈ S.
- **Rewards:** G2P-MPLight: `−| Σ_{∀L→∈I} Q(L→) − Σ_{∀L∈I} Q(L) |` (pressure-grounded, à la PressLight); G2P-CoLight: `−Σ_{∀L→∈I} Q(L→)` (queue-minimizing).
- Backbones: **MPLight** (stability) and **CoLight** (performance).

**(c) Training:** same as underlying models (DQN variants); CityFlow; **30 independent runs** for learning-based methods; 2-s all-red, yellow intervals; phase timing per dataset.

**(e) Baselines:** Random, FixedTime-like heuristic rows, MaxPressure, Efficient-MP, Advance-MP, G2P control (non-RL), MPLight, Efficient-/Advanced-MPLight & CoLight variants (Wu 2021, Zhang 2022).

**(f) Quantitative results (Table 1, avg travel time s, 30 runs):**

| Method | Jinan-1 | Jinan-2 | Jinan-3 | HZ-1 | HZ-2 | NY-1 | NY-2 |
|---|---|---|---|---|---|---|---|
| Random | 722.17 | 644.05 | 674.31 | 690.83 | 641.21 | 1603.77 | 1504.77 |
| MaxPressure | 374.56 | 328.96 | 332.94 | 365.06 | 446.91 | 1335.79 | 1121.38 |
| Advance-MP | 352.9977 | 282.5613 | 303.2879 | 317.7901 | 428.4886 | 1331.5656 | 1091.0796 |
| G2P control | 353.10 | 279.42 | 295.67 | 311.14 | 415.14 | 1279.59 | 1046.53 |
| MPLight (avg) | 341.16 | 309.37 | 314.94 | 329.87 | 423.17 | 1240.77 | 961.93 |
| Advanced-MPLight (avg) | 284.49 | 268.65 | 266.04 | 306.43 | 380.88 | 1264.58 | 1030.10 |
| CoLight-family (Efficient, avg) | 498.55 | 281.51 | 303.43 | 316.27 | 418.77 | 1280.60 | 980.91 |
| **G2P-MPLight (avg)** | **282.63** | **268.41** | **265.33** | **306.24** | **379.90** | 1247.85 | 1010.60 |

G2P control (non-RL) already beats Advance-MP on most sets; G2P-MPLight best-or-second on Jinan/Hangzhou; on NY-1, Advanced-MPLight (1264.58) edges G2P-MPLight (1247.85 is better actually — G2P-MPLight lower/better on NY-1: 1247.85 < 1264.58). Standard deviations for G2P-MPLight: e.g., Jinan-1 1.29-ish range (paper reports std ~1.29 for Advanced; G2P-MPLight std values listed alongside bests).

**(g) Limitations:** Turn probabilities unknown at test time (mitigated by Eq. 9 but truncated-queue estimation depends on Δt); β/effective-range needs speed parameters; still requires downstream queue sensors Q(L); G2P-CoLight reward not pressure-theoretic; NY-scale results show larger variance (std 40–46 s).

---

### A17. Cross-Paper Results Synthesis (exact numbers)

| Paper | Year | Venue | Simulator | Network scale | Headline quantitative result |
|---|---|---|---|---|---|
| IntelliLight | 2018 | KDD | SUMO | 1×1, 24 Jinan intersections | −22% duration, −38% queue vs best baseline (real camera data) |
| PressLight | 2019 | KDD | CityFlow | 6-int arterial + real arterials | HeavyFlat 160.48 s (−38.8% vs MP); Qingdao Rd 54.87 s |
| CoLight | 2019 | CIKM | CityFlow | up to 196 (NY) | 11.69% avg gain real-world; NY 1459.28 s |
| FRAP | 2019 | CIKM | CityFlow | single int. | Jinan 66.40 s vs IntelliLight 88.74 s (−25.2%) |
| MPLight | 2020 | AAAI | CityFlow | **2,510 lights** | 472.51 s / 6,932 throughput (best); 19.2% vs PressLight synthetic |
| AttendLight | 2020 | NeurIPS | CityFlow | 112 instances | +46/39/34/16/9% vs FT/MP/SOTL/DQTSC-M/FRAP |
| PDLight | 2020 | arXiv | CityFlow | multi-int | beats PressLight & CoLight (fixed & dynamic green) |
| MetaLight | 2020 | AAAI | CityFlow | 4 cities | +5.52% (homo), **+22.57%** (hetero) adaptation |
| π-Light | 2024 | AAAI | CityFlow | Jinan/HZ/Manhattan | beats DRL; cross-city transfer; edge-deployable |
| IPDALight | 2021/22 | JSA | SUMO/CityFlow | multi-int | better ATT + GreenWave, faster convergence |
| HiLight | 2021 | AAAI | CityFlow | 12–48 int + Shenzhen 33 | SZ-E 223 s vs CoLight 1099 s (−79.7%) |
| IG-RL | 2021 | TITS | SUMO | **3,971 signals** | 11,076 params, 1 GPU, zero-shot transfer |
| SocialLight | 2023 | AAMAS | SUMO+CityFlow | 196 (NY) | **+22.23% / +24.53%** NY1/NY2; trip 309.81 s (SUMO) |
| OffLight | 2024 | arXiv/CASE | — | 12/16/196 | −7.8% ATT, −11.2% queue vs offline SOTA |
| Traffic-R1 | 2026 | ACL | sim + production | 10 ints, 55k veh/day | −9.3% avg queue, −75% labor (6-wk A/B) |
| G2P-XLight | 2025 | arXiv | CityFlow | Jinan/HZ/NY | G2P-MPLight 282.63 s (Jinan-1) vs MPLight 341.16 s |

---

## SECTION B — SIMULATOR DEEP COMPARISON

### B1. SUMO (Simulation of Urban MObility)
- **Vehicle/lane model:** continuous-time, continuous-space microscopic simulator; car-following based on **Krauß model**: vehicle drives as fast as possible subject to safety regularization (can stop if leader stops at max deceleration). SUMO uses **Euler position update** (CityFlow deliberately switches to ballistic for better dynamics at 1-s steps). Lane-changing model with sublane logic; Krauß free-flow speed constraints: max acceleration, road speed limit, collision-free following, headway time, intersection-related speed.
- **Road network file:** `.net.xml` (roads, lanes, traffic lights); routes `.rou.xml`; further `.tll.xml`/`.add.xml` for TLS programs and additional structures.
- **TraCI (Traffic Control Interface):** socket-based client-server API allowing query/modify of simulation state **at single time-step resolution** — set phase, insert vehicles, retrieve lane counts/speeds. Overhead: socket round-trips per query are the main speed bottleneck (CityFlow uses pybind11 in-process instead).
- **Community status:** default in transportation research; validated/calibrated by domain experts; RESCO benchmarks built on it; supports dynamic routing (vehicles adapt routes to congestion) — important for realistic network-level evaluation.

### B2. CityFlow (Zhang et al., WWW 2019 Demo, DOI 10.1145/3308558.3314139)
- **File formats:** `roadnet.json` (intersections + roads as graph nodes/edges; each road → multiple lanes; intersection → roadlinks; roadlink → lanelinks = specific lane-to-lane paths; cross points precomputed between lanelinks) and `route.json` (vehicles as (o, t, d) origin-time-destination).
- **Why >20× faster than SUMO:**
  1. **Multithreading** (1/2/4/8 threads) — first open-source city-wide parallel simulator; ~**25× speedup on 30×30 grid with 8 threads = 72 simulation steps/s**;
  2. **Data structures:** each lane = linked list of vehicles (fast insertion/leader search); **segments** (small lane fragments) enable O(1)-ish range queries for lane changes (search ≤3 adjacent segments);
  3. **Intersection logic:** precomputed **cross points** — arrival notification decides pass/yield in **O(N_crosspoints)** instead of brute-force collision scans;
  4. **Ballistic update** allows larger stable time steps;
  5. **pybind11** in-process Python bindings vs SUMO's socket TraCI — much faster state retrieval for RL loops.
- **Effectiveness check:** average vehicle duration matches SUMO within **0.07%–1.06%** across 100–500 veh/h (Table 1 of the CityFlow paper).
- **RL interface:** `set_tl_phase()`, `next_step()`, `get_lane_vehicle_count()`, `get_lane_waiting_vehicle_count()`, `get_vehicles()`, `get_vehicle_speed()`; web GUI (PixiJS/WebGL) for large-scale replay.

### B3. Flow (Wu et al., 2017/2018; UC Berkeley)
- Framework for **deep RL + control experiments in traffic microsimulation**, originally integrating **SUMO + rllab** (now also RLlib), Gym-compatible env API; supports SUMO and Aimsun backends.
- Focus: **mixed-autonomy traffic** (autonomous + human-driven vehicles), not primarily TSC — benchmarks on ring road (Sugiyama instabilities), merge, figure-8, intersection networks; exposes TRPO/GAE-style policy gradient; AWS-scale experiment support.
- Extensions to SUMO for high-frequency simulation; benchmark finding: hand-designed controllers excel in-distribution but fail to generalize; simple NN policies stabilize across densities OOD.

### B4. LibSignal (Mei, Lei, Da, Shi, Wei — NeurIPS 2022 RL4RealLife Workshop)
- **Design:** cross-simulator (SUMO + CityFlow) unified pipeline; PyTorch; OpenAI Gym interface.
- **Atomic files:** roadnet (`.net.xml` ↔ `.json`) and flow (`.rou.xml` ↔ `.json`) with `converter.py` for conversion.
- **World module** exposes unified info functions: `lane_count, lane_waiting_count, lane_waiting_time_count, pressure, phase` + metrics `throughput, average_travel_time, lane_delay, lane_vehicles`; action space typically 8 phases.
- **Models (10):** MaxPressure, IDQN, PressLight, CoLight, FRAP, MPLight, MetaLight, AttendLight, etc.; **9 datasets** covering 65% of the reproduced-model papers (Jinan 1×1/3×4, Hangzhou 1×1/4×4, Manhattan 48/196/2510, Atlanta 1×5, LA 1×4, Cologne...).
- **Metrics (4):** delay, queue, travel time, throughput — with appendix formulas; paper shows **approximated delay ≠ actual delay**, and queue definitions change rankings.
- **Calibration methodology:** reproduce models in both simulators under identical datasets; report best-episode ATT consistency (e.g., PressLight Hangzhou4×4: TF 342.361 vs PT 344.75; CoLight: 344.49 vs 341.41) — TensorFlow/PyTorch implementations consistent; **does not claim identical absolute performance across simulators** — emphasizes *relative* policy ordering (sim-to-real testbed, not parity claim).

### B5. PyTSC (Bokade, Jin — Sensors 25(5):1302, 2025)
- Unified MARL-TSC platform over **SUMO + CityFlow** with consistent API (ConfigParser, Retriever, Simulator, TrafficSignal, TrafficSignalNetwork).
- Motivation vs LibSignal: LibSignal lacks native **CTDE** (QMIX/MAPPO) integration; SUMO-RL is SUMO-only. PyTSC plugs into **EPyMARL / MARLLib**.
- Speed: **batched TraCI queries** (single call for vehicle counts/speeds) minimizes socket overhead.
- Networks: Hangzhou (16), Cologne 8 (irregular, high-traffic); SUMO dynamic routing vs CityFlow static routes — complementary evaluation; customizable phase-select logic (`TLSFreePhaseSelectLogic`, `TLSRoundRobinPhaseSelectLogic`).

### B6. Calibration Methodology & Deployment Pitfalls — "The Real Deal" (Chen, Fang, Sadeh 2022, arXiv:2206.11996)

**Calibration:** convert roadnets/flows across simulators (LibSignal converter); match demand profiles (Poisson vs camera-derived); verify aggregate outputs (duration tables); fix turning ratios (10/60/30 standard); align time steps and yellow/all-red intervals; keep vehicle behavior models fixed during learning (Wei 2021 §4.4) — else non-stationarity confounds policy evaluation.

**Four deployment challenges (first review of RL-TSC→reality):**
1. **Uncertainty in detection:** queue/travel-time rewards need accurate detectors; loop (intrusive, cheap/accurate but maintenance-heavy) vs camera/radar (non-intrusive); agencies configure detectors differently; remedies: ensembles of models, connected-vehicle data at limited penetration.
2. **Reliability of communications:** real systems are **closed-loop hierarchies**: TMC (policy) → FMC (field master, regional coordination, clock sync) → LIC (local intersection controller); **90% of US TSC is closed-loop**; upgrades need Type 2070/ATC controllers (some intersections keep outdated hardware); NTCIP 1202 standard object definitions must be respected; wireless links suffer signal-strength data loss/latency — RL coordination must tolerate failure/latency.
3. **Compliance & interpretability:** MUTCD standards, state-level minimum green/yellow/red-clearance rules ("engineering judgement"); deep-RL opaque states block audits; suggestions: bake safety constraints into action space (as SURTRAC does), use **Accident Modification Factors (AMFs)** for interpretable safety accounting (no RL work does this yet), stakeholder preference learning for arbitrary local rules.
4. **Heterogeneous road users:** simulations assume identical cars; reality has pedestrians (leading pedestrian intervals, lagging phases), cyclists, transit, emergency preemption; agencies disagree on train-vs-pedestrian priority; RL must detect/respond equitably.

Additional pitfalls: trial-and-error learning causes real jams during training (motivates offline RL/meta-RL/imitation); sim-to-real gap (sensor noise, incidents, weather absent from sim); hierarchical existing infrastructures constrain where an RL agent can sit.

---

## SECTION C — SURVEYS DEEP

### C1. Wei, Zheng, Gayah, Li (2021) — *Recent Advances in RL for Traffic Signal Control: A Survey of Models and Evaluation*, ACM SIGKDD Explorations 22(2), 50 pp.

**Taxonomy (three axes):**
1. **Agent formulation:** single-agent vs multi-agent; independent vs shared parameters.
2. **Policy learning approach:** value-based (DQN variants), policy-based, actor-critic; plus imitation/demo-based.
3. **Coordination strategy:** independent RL (no coordination; non-stationarity issues in complex networks), IRL+communication (concatenate neighbor states/actions — requires consistent neighbor indexing), message-passing/graph methods (GCN with fixed adjacency assumes static influence; **GAT learns dynamic interactions** — CoLight, PDLight), and max-plus joint-action learners (reward passing vs state-observation passing duality).

**Evaluation inconsistencies documented (§4):**
- **Metrics:** average travel time, number of stops, queue length, throughput; **queue "waiting" definitions differ across papers** (speed threshold choices change rankings); **approximated delay (speed vs speed limit) does not reflect actual delay** (LibSignal later demonstrated this empirically).
- **Simulators:** GLD, AIM, SUMO, Paramics, Aimsun, CityFlow — different vehicle models ⇒ different absolute results; most work uses small networks vs city-scale thousands of signals (cites 50-signal Aslani, 196-signal district, MPLight's 2,510).
- **Traffic flow:** demand (o,t,d) volume/dynamics, behavior models (lane change, routing) usually held fixed during learning — but heavy/dynamic demand changes difficulty; non-stationarity from neighbor policies breaks convergence without coordination.
- **Benchmarking gap:** lack of public standard benchmarks; RL papers often **fail to compare with transportation baselines** (Webster's formula, MaxPressure).
- **Future directions:** learning efficiency (massive trial-and-error is unacceptable in real traffic → meta-learning, imitation), safety (risk management for RL agents; constraint integration in action selection e.g. pedestrian crossing), sim-to-real transfer (interpretable policies, realistic simulators).

### C2. Rasheed, Yau, Noor, Wu, Low (2020) — *Deep Reinforcement Learning for Traffic Signal Control: A Review*, IEEE Access 8: 208016–208044 (first DRL-TSC review).

**State taxonomy (six representations):**
- **S.1 Queue length:** waiting vehicles per lane/leg (speed = 0); state = max queue among lanes or binary per-cell occupancy.
- **S.2 Red timing:** time since lane turned red (reset on green/yellow).
- **S.3 Green timing:** time since green started.
- **S.4 Current traffic phase:** one-hot over candidate phases, e.g., (1,0,0,0,0,0,0,0).
- **S.5 Vehicle position:** lane segmented into cells (each holds one vehicle); cell s_{i,1} nearest intersection.
- **S.6 Vehicle speed:** per-cell speed normalized to [0,1] (1 = max legal speed e.g. 90 km/h, 0 = stopped).

**Action taxonomy (two):**
- **A.1 Traffic phase type:** select green combination; **in-order (round-robin with splits)** or **out-of-order**; |A| = #phases.
- **A.2 Traffic phase split:** keep current phase (a₁) vs switch (a₂).

**Reward taxonomy (three):**
- **R.1 Relative waiting time:** `r = W_i,t − W_i,t+1` (difference of average total waiting time between phases).
- **R.2 Relative queue length:** `r = n^c_{i,t+1} − n^q_{i,t+1}` (crossings minus queue — green sufficiency indicator).
- **R.3 Phase transition cost:** penalty for switching (delay incurred).

**Performance measures (four):** P.1 lower average delay; P.2 lower average waiting time; P.3 smaller queue length; P.4 higher throughput. Also covers simulation platforms, complexity analysis (curse of dimensionality: exploration cost + Q-table storage), design guidelines, open issues.

### C3. Michailidis, Michailidis, Lazaridis, Kosmatopoulos (2025) — *Traffic Signal Control via Reinforcement Learning: A Review on Applications and Innovations*, Infrastructures 10(5):114

**Methodology:** Scopus/WoS screening of **250+ publications** (2015–2025); inclusion: **≥30 citations** (2023–24 papers: ≥10), peer-reviewed, RL-TSC-focused, documented RL setup, methodological diversity (value/policy/actor-critic).

**Statistical findings:**
- **Value-based methods dominate** the RL-TSC landscape; **DQN is the most prominent algorithm**; QL favored for simple discrete state-action; evolution toward DDQN, dueling DQN, hierarchical multi-agent frameworks.
- **MARL > 60% of studies** (2015–2025) — decentralized per-intersection agents with shared coordination logic (neighborhood masking, graph message passing).
- Within MARL: **MARL-DQN most dominant**; classical MARL-QL still relevant in grid/hierarchical settings; A2C/A3C most frequent actor-critic; DDPG promising for continuous control but limited by reward design and partial-observability instability.
- **Hybrid RL** (fuzzy logic, immune networks, MPC) common; DQN–ANN the most common hybrid, then DQN–FLC; LSTM/GAT ANN hybrids dominate over FLC in later years.
- **Baselines:** QL, DQN, A2C, FRAP most common RL baselines; CoLight/PressLight/MetaLight favored as coordination/graph/pressure SOTA baselines; classical baselines: **FixedTime (dominant static), Actuated Control, MaxPressure (notable — decentralized, queue-aware, competitive with modern RL), RBC, SOTL**.
- **Rewards:** anchored on waiting time, queue length, average delay; recent expansion to **emissions, safety, equity**.
- **Algorithm choice correlates with objective complexity, not scale** — sophisticated methods appear even in single-intersection studies; simple techniques persist in large congestion-only scenarios.
- **SUMO is the dominant simulation platform** (open-source, modular, TraCI Python API); CityFlow second.
- **Simulator ecosystems** (SUMO, CityFlow) explicitly credited with enabling scalable MARL designs.

---

## SECTION D — URBAN MOBILITY RL (BEYOND SIGNALS)

### D1. Bus Bunching — Wang & Sun (2020) *Dynamic holding control to avoid bus bunching: A multi-agent deep reinforcement learning framework*, Transportation Research Part C 116:102661

*(Note: the headway-self-equalization reward + joint-action-tracker formulation the brief attributes to "Chen 2020 TrC" is this paper — Wang & Sun, TRC 2020.)*

**(a) MDP formulation (exact):**
- **State observation per bus b_i:** `X_i,t = [ h_i,t^+, h_i,t^−, z_t / Z ]` — forward headway, backward headway, normalized waiting passengers at stop s_j when b_i arrives (Z = normalizer).
- **Tracker state:** `O_t = [X_1,t, …, X_n,t]` — global observations for the joint-action tracker.
- **Action:** continuous `a_i,t ∈ [0,1]`; holding duration `d_i,t = a_i,t · T` where T = maximum holding time (a=0 ⇒ no hold). Continuous action for near-optimal exploration.
- **Reward (Eq. 3):** `r_i,t = exp(|h_i,t^+ − h_i,t^−|) − w·exp(a_i,t)` — first term **encourages headway self-equalization** (max when forward = backward headway), second **penalizes intervention** (holding increases mean headway and on-board travel time). Objective = coordination with as few interventions as possible (Bartholdi & Eisenstein inspiration).

**(b) Architecture / training:** basic **actor-critic per agent** + **joint action tracker** (a deep net trained by supervised learning to approximate all agents' actions from global observations — avoids training agents under unknown interaction dynamics, unlike Lowe et al.'s per-agent estimators); **PPO**-based scheme (MPPO-T) for stable policy updates; decisions at bus arrivals, reward at next stop.

**(c) Environment:** real-world transit simulator on a bus corridor; extensive numerical experiments vs local-information baselines (no-control NC, static headway FH, etc.).

**(f) Results:** superiority across average waiting time, forward/backward/mean headway stability, occupancy dispersion; long-horizon reward consideration beats local headway policies.

**(g) Limitations:** single route; simulator-based; weight w tuning; continuous holding may conflict with schedule-based operations.

### D2. Bus Bunching — Wang & Sun (2021) *Reducing Bus Bunching with Asynchronous Multi-Agent Reinforcement Learning*, IJCAI-21, pp. 426–433

**Problem:** holding happens **only when a bus arrives at a stop** → agents act **asynchronously**; standard Markov game G=(N,S,A,P,R,γ) is inaccurate.

**(a) Formulation:** modified transitions per agent `P̂_i: S_i × Â ↦ S_i`, Â ⊆ A (state transition of agent i need not depend on all agents' simultaneous actions); policy `π_θi = p(A_i|S_i)`; independent rewards R = {R_1..R_N}.
- **Reward:** `r_i,t = −CV² − w·a_i,t`-style (paper Eq. 2): first term **headway variability CV² = Var[h]/E²[h]** (small CV = consistent headway), second penalizes holding duration; w ∈ [0,1] balances stability vs efficiency.

**(b) Architecture — CAAC (Credit Assignment for Asynchronous Control):** inductive critic = **ego critic** (evaluate own policy) + **event critic** (approximate marginal contribution of *other* agents' actions) with **graph attention neural network** inductive learning; plugs into actor-critic; MADDPG and IAC are special cases (IAC = CAAC without event critic).

**(d) Environment:** four real trunk routes R1–R4 (>15 km, >40 stops each), true passenger demand from **smart-card data**; models trained on R1.

**(f) Results (execution on R2/R3/R4, vs no-control NC):**

| Method | AHT (s) | ΔAWT (s) | ΔAJT (s) | ΔAOD |
|---|---|---|---|---|
| NC baseline | — | 625 / 757 / 723 | 1415 / 1389 / 1109 | 18.4 / 13.1 / 9.9 |
| FH (fixed headway) | 67/67/68 | −87/−70/−36 | +614/+780/+480 | −5.1/−2.4/−2.5 |
| **CAAC** | 42/40/41 | **−166/−161/−127** | **+251/+336/+192** | **−9.9/−5.9/−4.9** |
| IAC | 40/42/42 | −128/−128/−94 | +254/+360/+202 | −7.5/−4.7/−4.0 |
| MADDPG | 37/35/36 | −132/−145/−111 | +202/+223/+130 | −7.7/−5.0/−3.7 |

CAAC achieves smallest AWT/AOD with moderate control; beats FH, IAC, MADDPG; **zero-shot transfer** of R1-trained model to R2/R3/R4 works (GAT inductive generalization).

**(g) Limitations:** independence assumption simplifies but can mis-specify dynamics; requires smart-card passenger data; single-city routes.

### D3. Bike Rebalancing — Pan, Cai, Fang, Tang, Huang (2019) *A Deep Reinforcement Learning Framework for Rebalancing Dockless Bike Sharing Systems*, AAAI-19

**(a) MDP formulation (exact):**
- Area → **n regions** {r_1..r_n}; day → **T timeslots**.
- **State:** supply vector S(t) = (S_i(t)) (bikes available per region), demand D_i(t), arrivals A_i(t), plus spatial/temporal features; region-to-region trip intents d_ij(t).
- **Action:** at each timeslot, for a user who can't find a bike in r_i, pricing algorithm suggests alternate bikes in neighbor regions N(r_i) and sets **price incentive p_ij(t)** (in order of user arrivals); total rebalancing **budget B** (depletes → no more offers).
- **User model:** walking cost `c_k(i,j,x)` (convex in distance x, private/unknown); user accepts offer with max utility `p_ij(t) − c_k(i,j,x) ≥ 0`; else unsatisfied request.
- **Reward:** **number of satisfied user requests** (immediate); objective = maximize long-term **service level**.

**(b) Architecture — HRP (Hierarchical Reinforcement Pricing):** builds on **DDPG** with hierarchical RL (Dietterich framework): **divide-and-conquer** decomposition of the global Q-value into **sub-Q-values of smaller regions** (handles high-dimensional input + temporal dependencies) + **localized module** correcting bias from decomposition and sub-state/sub-action correlations. Reduces input space and training loss; improves convergence.

**(d) Environment:** real **Mobike** dataset (Shanghai); regions 3×3 blocks for optimality tests; 400 independent runs per algorithm for offline-optimal comparison.

**(e) Baselines:** Random, OPT-FIX, DBP-UCB, vanilla DDPG, HRA (hierarchical without localization), offline V-timeslot optimum.

**(f) Quantitative results:**
- Varying budget: **HRP decreases un-service ratio by 43%–63%**, outperforming all others at every budget level; DDPG fails to use budget in large input space; OPT-FIX/DBP-UCB ignore spatial info.
- Varying supply: **47%–60% decrement in un-service ratio** vs others.
- Bike distribution: end-of-day KL divergence **HRP 0.548** (better than Mobike's own 0.554; OPT-FIX worsens distribution).
- Optimality: HRP performance **close to 24-timeslot look-ahead offline optimum** (HRA ≈ 4-timeslot only).
- Generalization: trained on one area, tested on unseen 3×3 areas → **40%–80% un-service decrement on 80% of test areas**.

**(g) Limitations:** assumes convex walking costs and rational utility-maximizing users; budget-constrained (hard budget, not learned); region granularity hand-chosen; no repositioning-van coordination (incentives only).

### D4. Ride-Hailing — JPDR (Zhang, Yang, Yao, Ma, Wang — IEEE TKDE 36(12), 2024, DOI 10.1109/TKDE.2024.3464563)

**Citation:** *Joint Optimization of Pricing, Dispatching and Repositioning in Ride-Hailing With Multiple Models Interplayed Reinforcement Learning*.

**(a) Problem:** three interdependent tasks — **pricing, order dispatching, vehicle repositioning** — never jointly optimized before; multi-stage decisions with complex coordination and no unified model.

**(b) Architecture — two mutually-guided components:**
1. **SAC-based centralized policy** for **dispatching + repositioning** (Soft Actor-Critic: max expected return + entropy bonus → stable exploration in continuous/high-dim spaces; automatic temperature tuning).
2. **Pricing strategy via multi-armed contextual bandit**, learning from feedback of the SAC component.
- Updates are **highly interdependent**: each component's policy evaluation conditions on the other (mutual bootstrapping, in the spirit of InBEDE's contextual-bandit × TD-learning integration).

**(d) Environment:** realistic environment simulator built on **real-world ride-hailing data** (platform-scale, city traces).

**(e) Baselines:** SOTA pricing-only, dispatch-only, and joint methods.

**(f) Quantitative results:** outperforms SOTA baselines in **both gross merchandise volume (GMV) and success rate** (exact percentages reported in the paper's experiment section; consistent gains across demand/supply regimes).

**(g) Limitations:** simulator-based evaluation (deployment would need platform integration); contextual bandit pricing is per-decision myopic relative to full RL for pricing; assumes centralized visibility of dispatch/reposition state; fairness of prices not explicitly constrained (contrast JDRCL's budget-constrained fairness formulation).

---

## CONCLUDING CROSS-CUTTING OBSERVATIONS

1. **Reward theory arc:** heuristic weighted sums (IntelliLight) → theoretically grounded pressure (PressLight/MPLight, with stability theorems) → capacity-aware PRCOL (PDLight) → turn-probability-free generalized pressure with stability proof (G2P) → long-horizon travel-time alignment via hierarchy (HiLight) → counterfactual marginal-contribution credit (SocialLight).
2. **Architecture arc:** CNN+phase-gate → GAT index-free coordination (CoLight) → symmetry-invariant phase-competition convs (FRAP) → dual attention for universality (AttendLight) → inductive GCNs over object graphs (IG-RL) → programmatic policies (π-Light) → LLM+GRPO foundation models (Traffic-R1).
3. **Scale arc:** 1 intersection (2018) → 196 (2019) → 2,510 (MPLight 2020) → 3,971 (IG-RL 2021) → 10 physical intersections / 55k drivers (Traffic-R1 2026 production).
4. **Deployment arc:** online simulation-only → offline RL with behavior-policy modeling (OffLight) → hybrid human-approved dispatch (Traffic-R1) with the four "Real Deal" barriers (detection, comms, compliance, heterogeneous users) still the field's main bottleneck.
5. **Evaluation debt:** Wei 2021 and LibSignal both document metric/simulator inconsistencies; independent leaderboards (SOTA2) now re-benchmark methods under unified settings, often with materially different absolute numbers than the original papers — a caution for any quantitative comparison across papers.
