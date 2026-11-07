# Quantum Computing Algorithms for Smart City Problems: A Technical Dossier

**Document type:** Research dossier (literature synthesis, no code artifacts)
**Scope:** Ten topic areas spanning quantum optimization, quantum machine learning, quantum communication, hardware comparisons, benchmarking, and fault tolerance, with emphasis on quantitative results reported in primary sources (journal articles, arXiv preprints, vendor technical reports).

---

## 0. Scope, Method, and Reading Guide

Modern cities generate computational problems that are combinatorial by nature: traffic signal phase selection across thousands of intersections, vehicle routing for fleets of thousands of vehicles, power dispatch with discrete switching decisions, and the protection of the communication infrastructure that ties these systems together. Nearly all of these problems reduce, formally, to quadratic unconstrained binary optimization (QUBO), to constrained optimization that can be mapped into QUBO form, or to supervised learning over high-dimensional spatio-temporal data. This dossier examines how quantum computing algorithms — chiefly the quantum approximate optimization algorithm (QAOA) and quantum annealing, together with hybrid quantum machine learning (QML) circuits and quantum key distribution (QKD) — have been applied to these smart-city problems, and it reports honestly on where the numbers stand against classical solvers.

Every quantitative claim below is attributed to a named source. Where sources disagree, or where a claim is a vendor benchmark rather than a peer-reviewed measurement, that status is stated explicitly. Equations are given in plain-text/LaTeX notation so that they can be transcribed into any editor.

---

## 1. Foundations: Problem Formulation, QUBO/Ising Models, and the QAOA Circuit

### 1.1 From urban decisions to binary variables

Almost every smart-city optimization task begins with a decision vector. A traffic controller chooses, for each intersection i and cycle t, a binary variable x_it ∈ {0,1} meaning "north–south green" (1) or "east–west green" (0). A distribution network planner chooses binary variables for the open/closed state of each tie-switch, for each candidate placement of a photovoltaic (PV) unit, and for each time block of an electric-vehicle (EV) charging schedule. A logistics planner chooses binary assignment variables y_vr ∈ {0,1} indicating whether vehicle v traverses route r. Once all decisions are binary, the objective — total travel time, network losses, congestion cost, energy not served — is expressed as a polynomial in the x_i, and all constraints are folded into penalty terms squared so that infeasible solutions become energetically expensive rather than forbidden.

### 1.2 The QUBO and Ising forms, and the standard penalty constructions

A QUBO problem is written

H_P(x) = Σ_{i<j} Q_ij x_i x_j + Σ_i Q_ii x_i ,  x_i ∈ {0,1} ,

where the upper-triangular matrix Q encodes both the objective and the penalties. Quantum annealers natively minimize an Ising Hamiltonian

H_Ising(s) = Σ_{i<j} J_ij s_i s_j + Σ_i h_i s_i ,  s_i ∈ {−1,+1} ,

and the two forms are exactly related by the affine substitution x_i = (1 − s_i)/2, which pushes the linear field h_i and couplings J_ij into the Q-matrix and vice versa. Because the map is exact and linear, any QUBO can be compiled to an Ising model without approximation; only the physical embedding onto the processor's qubit graph introduces loss (see Section 1.4).

The penalty constructions used in the smart-city literature are highly stereotyped:

- **One-hot / selection constraints.** "Exactly one route per vehicle" or "exactly one phase per cycle": P_onehot · (Σ_r y_r − 1)^2. Rusnáková et al. (arXiv:2510.06053) derive their penalty coefficient analytically so that any one-hot violation costs more than the best achievable objective decrease, guaranteeing that the ground state is feasible on their Traffic Flow Optimization (TFO) instances.
- **Flow conservation.** For vehicle routing, Azfar et al. (arXiv:2505.01614) place Σ_{e ∈ in(v)} x_e − Σ_{e ∈ out(v)} x_e = 0 for every node v directly into the cost Hamiltonian, together with subtour-elimination penalties of the form P · (Σ_{e ∈ δ(S)} x_e − 2)^2 for node subsets S, which is the standard Miller–Tucker–Zemlin construction squared into a diagonal penalty.
- **Capacity and coupling constraints.** Σ_{e} w_e x_e ≤ C becomes P · (Σ_e w_e x_e − C + slack)^2 with slack variables or, when the slack can be shown to saturate, without them. In Hussain et al. (Quantum Inf. Process. 19:312, 2020) the traffic-signal QUBO includes an "average deviation" term penalizing deviation of each phase's green split from its ideal share of the measured queue lengths, plus hard-constraint terms preventing two orthogonal approaches from being green simultaneously.
- **Objective terms.** Travel-time or congestion objectives enter as quadratic coefficients linking pairs of decisions whose costs interact (e.g., two adjacent intersections both flushing into a saturated downstream link), exactly the structure that makes QUBO the natural form.

A recurring engineering issue is penalty scaling. If P is too small, the optimizer returns infeasible solutions; if P is too large, the dynamic range of the Q-matrix exceeds the analog control precision of the annealer and precision of the couplers degrades. Azfar et al. devote an explicit section to penalty scaling and coefficient normalization for their link-based VRP Hamiltonian, and Marchesin et al. (IEEE Trans. Quantum Eng. 4:1–13, 2023) study the joint impact of D-Wave's two reference parameters — chain strength and annealing time — at a fixed 100 reads, which is precisely the operational face of the penalty-scaling problem: chain strength is the penalty that keeps a logical qubit's minor-embedding chain of physical qubits acting as one variable.

### 1.3 The QAOA circuit and its variants

The quantum approximate optimization algorithm (Farhi, Goldstone, Gutmann, 2014) prepares, on n qubits,

|β,γ⟩ = Π_{k=1}^{p} e^{−i β_k B} e^{−i γ_k C} |+⟩^{⊗n} ,

where C = H_P is the problem (cost) Hamiltonian diagonal in the computational basis, B = Σ_i X_i is the mixer, γ_k, β_k are 2p classical parameters optimized by an outer loop, and p is the circuit depth. Measurement of |β,γ⟩ in the computational basis yields a bitstring whose expected cost ⟨C⟩ approximates the optimum; the approximation ratio is r = (⟨C⟩ − C_max)/(C_min − C_max) for minimization conventions adjusted per paper. As p → ∞ the algorithm converges to the adiabatic solution of Section 1.4; at p = 1–3 it is a NISQ-feasible heuristic whose performance is dominated by the quality of the classical outer optimizer.

Because raw ⟨C⟩ is dominated by the far tail of the cost distribution — most bitstrings are bad, and averaging washes out the good ones — four practically important variants appear in the smart-city context:

1. **CVaR-QAOA (Barkoutsos et al., Quantum 4:256, 2020).** Instead of the mean, the objective is the conditional value at risk CVaR_α(C) = E[C | C ≤ q_α], the average cost of the best α-quantile of samples. With α ≈ 0.01–0.25 the optimizer directly targets the low-energy tail, stabilizing training at shallow depth.
2. **Warm-start QAOA (Egger, Mareček, Woerner, Quantum 5:479, 2021).** The initial state is a classical Gibbs-like state exp(−η H_C)|b⟩ prepared from a cheap classical approximation |b⟩, with η an additional tunable parameter. The key theoretical property used in the smart-city literature is that warm-starting preserves the Goemans–Williamson approximation ratio for MAX-CUT at any depth p (whenever the classical preprocessing itself achieves it), decoupling solution-quality guarantees from circuit depth. Its practical performance is noted to be COBYLA-optimizer-dependent.
3. **Quantum alternating operator ansatz / QAOA+ (Eq. constraint-preserving mixers).** Constraints are enforced structurally by choosing a mixer that never leaves the feasible subspace (e.g., partial mixers acting only on violated constraints) and by initializing from a feasible bitstring. This eliminates the penalty-scaling problem entirely for problems with easy feasible states.
4. **Multi-angle QAOA (ma-QAOA; Herrman et al.; Wilkie, Ostrowski, Herrman, arXiv:2404.10743).** Each gate gets its own angle rather than one angle per layer, and initialization on multiples of π/8 followed by BFGS yields approximation ratios of 0.900 (p=1), 0.982 (p=2), and 0.997 (p=3) on the benchmark set studied — the strongest depth-performance figures available for gate-model combinatorial optimization at small size.

For constrained problems, the outer-loop optimizer choice is as consequential as the circuit. Fitzek et al. (Sci. Rep. 14:25415, 2024) systematically compare four optimizers — Nelder–Mead, Powell, differential evolution, and basinhopping (with BFGS as the local minimizer) — on their HVRP circuits: basinhopping and differential evolution perform significantly better than Nelder–Mead and Powell, but at roughly one order of magnitude greater wall-clock cost because of the many circuit evaluations their global-search mechanisms require (differential evolution capped at 1,000 iterations, basinhopping at 50). They also quantify a fundamental NISQ obstacle: the probability of sampling a valid (feasile) bitstring reaches only about 25% at p = 5 for an 11-qubit instance and does not exceed 10% for the 19- and 21-qubit instances, which is why feasibility repair (e.g., local bit-flip post-processing, as used by Dash et al.) is standard in routing demonstrations.

### 1.4 Quantum annealing and the adiabatic pathway

Quantum annealing implements the same optimization by physically evolving a Hamiltonian

H(t) = (1 − t/T) H_0 + (t/T) H_P ,  t ∈ [0, T] ,

starting in the ground state of H_0 = −Σ_i X_i (all qubits in superposition) and ending in H_P. The adiabatic theorem guarantees that the system remains in the instantaneous ground state if T ≫ 1/Δ_min², where Δ_min is the minimum spectral gap along the path; in practice T is 1–1000 μs on D-Wave hardware and the evolution is not adiabatic, so performance is empirical. Two classical-adjacent features matter for smart-city work: **reverse annealing** (start from a classical bitstring and anneal backward/forward to locally refine it, enabling hybrid schemes) and **minor embedding** (a logical problem graph of maximum degree d is mapped onto the hardware graph by replacing logical qubits with chains of physical qubits coupled by chain-strength penalties).

Hardware generations cited in this dossier: D-Wave 2000Q (Chimera topology, ~2000 physical qubits), Advantage (Pegasus topology, 5,760 physical qubits), Advantage2 (Zephyr topology, >4,400 qubits with reduced noise), gate-model systems from IBM (Eagle/Heron processors, up to 1,000+ qubits, heavy-hex connectivity), IonQ (trapped ions, all-to-all connectivity), and Fujitsu's classical Digital Annealer (DA, up to 100,000 binary decision variables — a "quantum-inspired" ASIC, not a quantum device).

### 1.5 Classical baselines and how results must be read

The baselines used in the papers below are, in order of strength: greedy/random initialization; D-Wave's `neal` simulated annealer (SA) and simulated tabu search; Google OR-Tools metaheuristics for routing; interior-point/active-set exact solvers (Gurobi, CPLEX, CBC) for MILP formulations; Newton–Raphson (NR) iteration for power flow; and for QML, classical CNN/LSTM/MLP baselines retrained on the same data. The most common quantum result shapes to interpret are: (a) "matches classical within ε%" — a non-negative result only if ε is within the quantum solver's own sampling noise; (b) "X% better than baseline" — meaningful only if the classical solver was tuned comparably; and (c) "faster" — must state whether QPU anneal time only, or full end-to-end time including embedding and queueing, is counted. Section 7 returns to this.

---

## 2. Traffic Signal Control

Traffic signal control was the earliest and most persistent smart-city target for quantum optimization, because a city-scale signal plan is a large binary problem that changes every few tens of seconds.

### 2.1 Hussain et al. (2020): time-dependent phase selection as QUBO

Hussain, Javaid, Khan, Aslam, Arai (Quantum Information Processing 19(9):312, 2020; arXiv:1912.07134) formulate the selection of traffic-signal phases for a grid of intersections, with time-dependent queue measurements, as a QUBO whose variables encode which phase (and, for multi-phase signals, which phase sequence position) is active in each control interval. The Hamiltonian combines the system cost (minimizing queue imbalance and delay proxy) with penalty terms for constraints such as mutual exclusion of conflicting movements and the "average deviation" of green allocation from the ideal split. Because a full city exceeds what a QPU can embed, they adopt the hybrid workflow QBSolv/LEAP: a classical outer loop decomposes the problem, fixes a subset of variables, and repeatedly submits small QUBOs to D-Wave's quantum-classical hybrid solver (LEAP), reassembling a globally improved plan. This "large problem, small QUBOs" pattern is the dominant real-world deployment mode for annealing-based city optimization to this day.

### 2.2 Inoue et al. (2021): global lattice control on a 50×50 city

Inoue, Okada, Matsumori, Aihara, Yoshida (Sci. Rep. 11:3303, 2021; arXiv:2003.07527; the Toyota Central R&D Labs/D-Wave collaboration) consider L×L square-lattice roads with periodic boundary conditions, two lanes per road, and one signal per node taking σ_i = +1 (north–south green) or −1 (east–west green). They define a global objective minimizing the imbalance of flows in the two orthogonal directions; the resulting quadratic form in the σ_i is an Ising Hamiltonian compatible with the annealer. Three controllers are compared over wide ranges of α, the probability that a car goes straight rather than turning:

1. conventional **local control** (each signal reacts only to its own queue),
2. **global simulated annealing** (the `neal` library, minimizing the full Ising energy each step),
3. **global quantum annealing** on the D-Wave 2000Q — which, because the problem size (up to L = 50, i.e., 2,500 signals, 2,500 logical qubits) exceeds a single QPU, is executed with graph-partitioning subdivision of the lattice.

Reported outcomes: both global controllers suppress traffic imbalance over the whole parameter range far better than local control; and the quantum-annealing solutions are better than those obtained with simulated annealing, with the quantum advantage most visible at large α (cars mostly going straight). The paper additionally proves analytically that local and global control converge in the limit α → equiprobable turning/straight, verified numerically. A candid limitation the authors state themselves: since the 50×50 problem had to be partitioned to fit the 2000Q, the full unpartitioned quantum advantage should improve further once larger annealers exist — an expectation later tested by the Advantage generation.

### 2.3 Marchesin et al. (2023): a versatile QUBO for realistic urban networks

Marchesin, Montrucchio, Graziano, Boella, Mondo (IEEE Trans. Quantum Eng. 4:1–13, 2023, DOI 10.1109/TQE.2023.3312284) move away from the idealized lattice: their algorithm collects traffic information over a wide urban road network and defines signal activation patterns that "holistically reduce congestion," formulated as a QUBO solved on D-Wave machines. Operationally, each network intersection is analyzed separately; signals controlling roads with traffic density above a threshold σ are given priority, and the priority value establishes which signal is enabled in the next activation cycle (random tie-breaking under a uniform distribution when several are eligible; a signal already activated cannot be immediately re-selected in subsequent optimizations). A key reported evaluation metric is the distribution, at the end of each optimization cycle (each cycle = 100 subsequent optimization processes), of the percentage of streets experiencing congestion relative to their maximum capacity. Their parameter study jointly varies D-Wave's chain strength and annealing time at fixed 100 reads, and robustness tests span different traffic scenarios. The comparative claim is qualitative but strong: the proposed model outperforms traditional control techniques in several traffic conditions, "effectively containing critical congestion situations, reducing their presence, and preventing their formation," and the paper closes by characterizing what these machines can and cannot do today. (Full-text access to the article's numeric figures is restricted by the publisher repository; the statements here are those confirmed from the open abstract, indexed full-text excerpts, and the IEEE TQE article page.)

### 2.4 Rusnáková et al. (2025): city-scale traffic flow with 25,000 vehicles

Rusnáková, Chovanec, Gazda (arXiv:2510.06053, v5 2026) provide the largest quantitative annealing-vs-classical traffic result available. Their TFO model samples vehicle trajectories at fixed intervals from simulated mobility data, identifies leader–follower interactions on shared road segments, and builds a time-resolved congestion objective plus route-duration penalties, with an analytically derived penalty enforcing one-hot route selection. To tame combinatorial growth they apply **Leiden clustering** to partition vehicles into dense communities optimized independently; each cluster subproblem is solved by (i) D-Wave's hybrid quantum-classical annealer, (ii) exact MILP via Gurobi, (iii) SA and tabu search, (iv) CBC, on multiple city maps with up to 25,000 vehicles. Results: across large scenarios the hybrid quantum annealer produces feasible solutions within ≈1% of Gurobi's objective, with stable runtimes; both beat the shortest-route baseline with congestion-cost reductions of **up to 24.4% (hybrid quantum) and 29.4% (Gurobi)** for n ≥ 10,000 vehicles. The honest headline is therefore "near-classical-exact quality at scale, not superiority" — and the authors note the map topology itself drives embedding efficiency and interaction density.

Related evidence: Shikanai, Ohzeki, Tanaka (2023 preprint) integrated QUBO signal control with SUMO simulation on real geographic maps including T-junctions and multi-forked roads, and found D-Wave could not reach the ground state found by Gurobi and was slower — a useful negative result showing that real-map structure (not just size) determines whether annealing wins. Salloum et al. (Sci. Rep. 15:—, 2025, s41598-025-04568-2) decompose 100–500-car routing on the Almaty map into iterative sub-QUBOs solved purely on the D-Wave Advantage QPU (Pegasus topology), reporting improved median congestion reduction versus prior Volkswagen-style weighted baselines.

---

## 3. Vehicle Routing and Logistics

The vehicle routing problem (VRP), its capacitated (CVRP), time-window (VRPTW), and heterogeneous (HVRP) variants, is the backbone of urban logistics. Its binary formulation — assignment of customers to routes with capacity and subtour constraints — maps naturally onto QUBO, but its qubit count has been the field's central obstacle.

### 3.1 Fitzek et al. (2024): HVRP on gate-model QAOA, with an honest resource audit

Fitzek, Bös, Lang, Lobe, Prölß (Sci. Rep. 14:25415, 2024; open access, PMC11512041) solve the heterogeneous VRP by mapping it to an Ising model and running QAOA. Two structural findings dominate their paper:

- **Qubit scaling is quadratic in the number of customers** for their edge/assignment-based encoding (qubits scale as ~N_c²), which motivates every subsequent decomposition scheme.
- On simulated hardware they sample feasible solutions with probability up to ≈25% (p = 5, 11 qubits) and ≤10% (19 and 21 qubits), so they apply feasibility post-processing; and their optimizer comparison (Section 1.3) shows basinhopping/differential evolution give the best energies at ~10× the wall-clock of Nelder–Mead/Powell.

Their conclusion about scale is the one usually quoted: classical optimizers already handle instances with more than 1,000 customers, whereas the corresponding quantum formulation "would need millions of qubits" — i.e., direct end-to-end QAOA for industrial VRP requires fault-tolerant hardware (Section 9). The value of the paper is precisely that it performs this audit rather than hiding it.

### 3.2 Dash et al. (2025): hierarchical QAOA with clustered decomposition

Dash et al. (arXiv:2511.00506) attack the qubit explosion by hierarchical decomposition: cluster customers, solve an intra-cluster open-traveling-salesperson (OTSP) subproblem and an inter-cluster reduced VRP with QAOA, then patch. Their concrete demonstration: 100 random instances of a 13-node, 2-vehicle problem; p = 3; both standard and multi-angle QAOA; a local 1- or 2-bit-flip feasibility repair after sampling. The resource claim is the headline: **12 logical qubits per subproblem versus 156 for the direct edge-based encoding** — an order-of-magnitude reduction. Reported approximation ratios are in the 1.2–1.5 range against Gurobi on their normalized cost convention (i.e., quantum solutions are within a bounded factor of the exact optimum, not better than it). This paper is the clearest current template for making QAOA-VRP fit NISQ devices: decompose, keep each sub-QUBO small, repair feasibility classically.

### 3.3 Azfar et al. (2025): link-based QAOA on real IBM hardware

Azfar, Wong, Al-Taha, Alsebaan, ... (arXiv:2505.01614v2) present a link-based VRP formulation in which flow-conservation and subtour-elimination constraints are embedded directly in the cost Hamiltonian, executed with QAOA on an IBM Quantum System One. Their contribution is engineering-grade: explicit circuit-complexity analysis and a section on penalty scaling/coefficient normalization ensuring analog control ranges are respected — the two failure modes (too many qubits, ill-conditioned coefficients) that sink most hardware VRP demonstrations. The paper is a reference for how the QUBO compilation should be documented if results are to be reproducible.

### 3.4 Industrial context: what was actually deployed

Volkswagen's Quantum Shuttle (Web Summit, Lisbon, 2019) is the canonical production-adjacent deployment: 418 cars requiring 1,254 qubits in the original QUBO were routed through a hybrid classical-quantum loop on D-Wave (publicized results include up to ≈40% reductions in selected travel-time metrics in pilot-scale tests, per D-Wave case-study communications rather than peer review). Salloum et al. (2024/2025) explicitly rebuild on that foundation, moving from hybrid to pure-QPU iterative sub-QUBOs. The pattern across all VRP work is invariant: **no paper solves city-scale VRP on a QPU alone; every deployed result is a hybrid loop with classical decomposition and repair.**

---

## 4. Power Systems: Optimal Power Flow, Network Reconfiguration, and Power Flow Solvers

Urban grids are the second classical application domain: discrete switching, EV charging schedules, and DER placement are binary decisions coupled through nonlinear AC power-flow physics.

### 4.1 Morstyn (2023): combinatorial OPF on the 5,760-qubit Advantage

Morstyn (IEEE Trans. Smart Grid 14(2):1093–1102, 2023, DOI 10.1109/TSG.2022.3200590) shows how an optimal power flow problem incorporating (i) linear multiphase network modeling, (ii) discrete sources of energy flexibility, (iii) renewable generation placement/sizing, and (iv) network upgrades can be written as a QUBO for annealing-based quantum computing. Two formulations worth transcribing:

- **Binary expansion of controllable DER output:** for controllable asset c with output p_ct in block δ_c,
  p_ct = δ_c Σ_{m=0}^{N_c − 1} 2^m x_ctm ,  x_ctm ∈ {0,1},
  converting continuous set-points into N_c binary variables per asset per period (a direct way to make smart charging combinatorial).
- **Network model:** linear multiphase (LinDistFlow-style) constraints — voltage drops linear in power flows — enter the QUBO as squared residuals, turning the AC feasibility check into penalty terms.

Case studies place controllable on/off EV charging, PV placement/sizing, and network upgrades on the **IEEE European Low Voltage Test Feeder (55 loads, 30 EVs)** and solve the QUBO with D-Wave's **5,760-qubit Advantage QPU and hybrid quantum-classical solver**, each QUBO solved 30 times to characterize the output distribution (median, interquartile range, whiskers reported). Concrete planning finding: with network upgrades (50% impedance reduction) the co-optimized solution builds **100 kWp of PV**, versus only **50 kWp without upgrades** — the quantum solve identifies where reinforcement unlocks DER headroom. The paper is explicit that definitive advantage over classical computing in the noisy case is unclear, positioning the work as applicability proof for power systems rather than speedup evidence.

### 4.2 Silva et al. (2023): minimum-loss network reconfiguration

Silva et al. (Sci. Rep. 13:10777, 2023; PMC10319827) formulate distribution-network reconfiguration — choosing which tie-switches to open so as to minimize active losses while radiality and load-supply constraints hold — as a QUBO. Tests use the standard 33-node network with substation at node 0. The interesting structural point: radiality (no loops) can be encoded via spanning-tree-style penalties on switch variables, after which the loss objective (computed from the linearized branch flows) supplies quadratic terms linking adjacent switch decisions. This is one of the cleanest examples of a "pure QUBO" grid problem with no continuous relaxation inside it.

### 4.3 Kaseb et al. (2024): adiabatic quantum power flow (AQPF)

Kaseb, Möller, Vergara, Palensky (Sci. Rep. 14:23216, 2024, DOI 10.1038/s41598-024-73512-7) introduce the first adiabatic quantum power flow. Voltage magnitudes μ_i and angles ω_i are discretized with steps Δμ = 1×10⁻², Δω = 1×10⁻³ around an initial point (μ = 1, ω = 0), so each bus variable becomes a small set of binary digits (e.g., 3 bits per variable for their range). Substituting the digit expansions into the nodal power-injection equations

p_i = Σ_j μ_i (g_ij (μ_j cos θ_ij + ...) − b_ij (...)),  q_i = ... (standard AC form)

and squaring the residual between scheduled and computed injections yields the QUBO/HUBO Hamiltonian that an annealer minimizes; the AQPF algorithm iterates: compute injections → build Hamiltonian → solve on annealer → update μ, ω until the residual threshold ε = 1×10⁻³ (or better) is met. Their Algorithm 1/2 pair (combinatorial PF and its adiabatic variant) is fully specified in the paper and supplement.

Quantitative findings:
- Test systems: 4-bus (both QUBO and Ising formulations) and 14-bus (partitioned). Solvers: D-Wave Advantage QA, D-Wave hybrid (HA), Fujitsu Digital Annealer V3, D-Wave `neal` SA, and a second classical SA.
- Accuracy: partitioned AQPF on the 14-bus case reproduces Newton–Raphson to mean differences of ≈4.57×10⁻² W (active) and 1.67×10⁻³ var (reactive, sd 1.42×10⁻² var) — precision set by the discretization step, refinable by smaller thresholds.
- Speed profile: NR needs fewer iterations than DA, but DA's clock time per iteration is lower by orders of magnitude; AQPF additionally **mitigates the divergence problem** that classical solvers face on ill-conditioned cases, and tolerates incomplete load information.
- Scale limits: QA is confined to the 14-bus system (QUBO) and 4-bus (Ising) by hardware-graph connectivity, whereas Fujitsu's DA handles up to 100,000 decision variables — which is why the authors position AQPF for NISQ and future fault-tolerant hardware while using quantum-inspired classical annealers for today's larger grids. Their companion QCE24 study concludes QA and DA both outperform classical simulated annealers for this application, with DA handling larger systems.

### 4.4 Gate-model power-flow ML (context)

Kaseb et al. (Electr. Power Syst. Res. 235:110677, 2024) also benchmark hybrid quantum–classical neural networks for power flow: parameterized quantum circuits (1,024 shots per training step) replace part of a classical network; their hybrid model outperforms both pure-quantum and pure-classical networks on distribution load-flow prediction. Earlier lineage: Feng, Zhou, Zhang's "Quantum power flow" (IEEE TPWRS 36:3810, 2021), noise-resilient QPF (iEnergy 6:63, 2023), Jing et al.'s data-driven QAOA for power systems (Commun. Eng. 2:12, 2023), and Pareek et al.'s "Demystifying quantum power flow" (Electr. Power Syst. Res. 235:110677-adjacent literature), which argues limits on practical quantum advantage for PF — a counterweight worth citing alongside the optimistic results.

---

## 5. Quantum Machine Learning for Urban Prediction

Hybrid QML replaces selected classical layers (convolutions, recurrent cells, attention branches) with parameterized quantum circuits (PQCs) trained by gradient-based classical optimizers. For smart cities the relevant tasks are air-quality (AQI/PM2.5) nowcasting, weather and wind forecasting, flood prediction/detection, and energy time-series — all regression or binary-classification problems where reported quantum gains must be read against retrained classical baselines on identical data.

### 5.1 Dong et al. (2024): QRELU-HQCNN-LSTM for air-quality prediction

Dong, Li, Zhu, Yan (Front. Phys. 12:1412664, 2024) propose a hybrid architecture in which an HQCNN (hybrid quantum convolutional neural network) acts as encoder — quantum convolution layers with a quantum activation function, **QRELU**, modeled on the classical ReLU but implemented by the PQC's measured expectation values — feeding an LSTM (Tanh activation) decoder; the daily multivariate series (PM2.5, PM10, SO₂, CO, NO₂, O₃, plus meteorology) is processed end to end. Their algorithmic flow: (1) input the air-quality time series; (2) set batch size, epochs, learning rate and the quantum-circuit hyperparameters; (3) train the QRELU-HQCNN encoder jointly with the LSTM; (4) compare against CNN-LSTM, QRELU-CNN-LSTM, and HQCNN-LSTM baselines.

Reported error metrics (lower is better; the three columns are RMSE / MAPE / MAE) for Shanghai and two other cities show the monotone benefit of combining both innovations:

| Model | RMSE | MAPE | MAE |
|---|---|---|---|
| QRELU-CNN-LSTM | 12.3632 | 0.2161 | 9.6196 |
| HQCNN-LSTM | 12.2231 | 0.2127 | 9.3862 |
| **QRELU-HQCNN-LSTM** | **11.4827** | **0.2011** | **8.8771** |

in one evaluated city configuration (e.g., 55.5842 / 0.4601 / 40.9113 for the best model in a second city, versus 56.5811 / 0.5074 / 42.2921 for QRELU-CNN-LSTM; and 21.7895 / 0.2581 / 13.8983 versus 22.3154 / 0.2630 / 14.2872 in a third). The consistent ordering — full hybrid best, quantum-activation-only and HQCNN-only intermediate, classical CNN-LSTM worst — is the paper's central claim, on simulated quantum circuits rather than QPU hardware.

### 5.2 Pires et al. (2026): 172-qubit annealing-based QNN for PM2.5 nowcasting

Pires, Saimon, Herrmann, Kumar, Moret (arXiv:2610.13882, 2026) build a scalable hybrid framework coupling variational quantum circuits with quantum annealing on a neuromorphic quantum computing platform, applied to high-density UK urban PM2.5 data. Pipeline: discrete wavelet transform (DWT) decomposition of the polluted input series → quantum feature space → variational QNN → classical head. Their largest architecture is a **172-logical-qubit QNN** (lookback 2; the circuit designed for 172 qubits in quantum feature space, with the actual QUBO optimization variables sized to the platform): base state of 172 variables, **4 variational layers × 172 single-qubit rotations = 688 rotation gates**; smaller variants use 86 qubits (lookback 1). Performance is reported as NMSE/Pearson R pairs (e.g., 0.506/0.748 and 0.644/0.688 for depth-1 configurations across dataset variants, with the 172-qubit depth-4 wavelet model achieving the best fidelity). Headline claims: QNNs show intrinsic resilience to input volatility, "significantly outperforming classical baselines (MLP and LSTM) on raw, high-entropy environmental data," and wavelet coupling produces synergistic fidelity gains. Code is public (github.com/OttoMP/quantum-air-pollution-nowcasting). This is currently the largest qubit-count QML result tied to an urban environmental monitoring task.

### 5.3 Marchisio et al. (2026): QLIF-CAST weather forecasting with hardware verification

Marchisio, Ebrahim, Innan, Kashif, Shafique (arXiv:2605.18333v3; IEEE QAI 2026) adapt the Quantum Leaky-Integrate-and-Fire spiking neuron to time-series regression: neuron excitation states are single-qubit superpositions driven by R_x rotation gates and T1 relaxation decay, embedded in a hybrid quantum-classical recurrent architecture. Results are unusually concrete:

- **vs parameter-matched classical LIF baseline** on a multivariate weather dataset: **15.4% lower MSE and 4.4% lower MAE** — a controlled isolation of quantum neuronal dynamics.
- **vs published QLSTM/QNN models** on air-quality and wind-speed benchmarks: converges in **up to 94% less training time**, occupying a distinct point in the speed-error trade-off space.
- **Real hardware:** the core gate sequence |0⟩ → R_x(φ) → R_x(θ) → Measure executed on **IBM Marrakesh (156-qubit QPU)** with 1,000 shots per test case showed **only 1.2% average deviation from simulation** — one of the cleanest NISQ-era hardware-verifications of an urban-forecasting circuit.

### 5.4 Lin, Liu, Chen (2024): Quantum-Train LSTM for flood prediction

Lin, Liu, Chen (arXiv:2407.08617; IEEE QCE 2024) apply the Quantum-Train (QT) technique — winner of the Deloitte Quantum Climate Challenge 2024 — to an LSTM forecasting water levels for flood prediction. QT maps classical NN weights to a Hilbert space: a QNN's measurement probabilities are reparameterized into the classical network's parameters, so the trainable parameter count drops from M to **O(polylog(M))**. Concrete numbers: the QT-LSTM trains the same classical LSTM with **18,830 trainable parameters versus 40,451** for the classical model (a >50% reduction), with only slight accuracy degradation; classical training data conditioning is illustrated by a baseline with MSE 475.91 / MAE 17.44. Two practical properties matter for cities: the model processes classical data without quantum embedding at inference, and — because the trained artifact is classical — **post-training operation requires no quantum hardware** (the 11-hour training figure reported is quantum simulation on a classical computer, not QPU time). Follow-on QT results include QT-CNN with up to 70% parameter reduction at unchanged accuracy and QT reinforcement learning (QTRL).

### 5.5 Maity & Ghanbarian (2026): quantum-enhanced vision transformer for flood detection

Maity, Ghanbarian (arXiv:2603.13689; IEEE DCAS 2026) fuse a ViT backbone with a **4-qubit parameterized quantum circuit** branch on the SEN12-FLOOD remote-sensing dataset (~36,000 Sentinel-1/Sentinel-2 GeoTIFFs, 337 sites). The quantum branch produces compact nonlinear feature descriptors (a 64-dimensional vector concatenated with the ViT's 1024-dimensional stream → 1088 combined). Results: overall accuracy **84.48% → 94.47%**, F1 **0.841 → 0.944**, with the largest gain in non-flooded recall (**68.24% → 87.65%, +19.41 points**), cutting dangerous false positives; flooded-class F1 rises 0.889 → 0.960. Both models were trained from scratch, so the gain is attributable to the quantum structural contribution. This is a compact example of the "few qubits, real data, big delta" pattern that dominates credible QML-for-cities results.

Adjacent context: Kaseb et al.'s hybrid QNN power-flow model (Section 4.4) reports the hybrid beating both pure-classical and pure-quantum networks; wind-speed QNN forecasting with weather covariates up to a 6-hour horizon appears in Energy and AI (Pires & Nascimento et al., 2025); and EGU26 work by Ahmed, Qazi, Magri reports quantum-inspired reservoir computing producing 45-day forecasts with **10–50× less compute** than leading classical AI weather models — quantum-inspired rather than quantum, but a relevant efficiency baseline. Cross-cutting caveats from the field: barren plateaus limit trainable width, the lack of standardized benchmarks makes cross-paper NMSE comparisons unsafe, and nearly all results above are simulator-based except where hardware deviation is explicitly reported (QLIF-CAST; the annealing-based QNN platform).

---

## 6. Quantum Key Distribution for Urban Communication Security

QKD is the one quantum technology already deployed at metropolitan scale, and unlike optimization it has mature, quantitatively specified results. It secures the control/telemetry links (traffic controllers, grid SCADA, IoT gateways) that smart-city operations depend on.

### 6.1 Protocol mathematics: BB84 with decoy states

In BB84, Alice sends single photons prepared in one of four polarization states spanning two conjugate bases; after basis reconciliation over an authenticated classical channel they share a sifted key, from which they extract a secret key by error correction (efficiency f) and privacy amplification. Photon-number-splitting (PNS) attacks exploit the multi-photon pulses of real lasers; the **decoy-state method** (Lo, Ma, Chen, PRL 94:230504, 2005) defeats this with the same hardware by randomly interleaving signal, weak-decoy, and vacuum pulses and comparing yields. The standard security formula used in the Chinese network papers is:

r = −f Q_μ H(E_μ) + Y_1 μ e^{−μ} [1 − H(e_1^p)] ,

where μ is the mean photon number of the signal state, Q_μ and E_μ are the overall gain and error rate, Y_1 is the single-photon yield, e_1^p the single-photon error rate, and H the binary Shannon entropy; the first term is the cost of error correction, the second the privacy-amplified single-photon contribution. Finite-size analysis extends this to real integration windows. Typical implementation parameters (Hefei network): signal/decoy mean photon numbers **0.6 and 0.2**, in a **6:1:1** signal:decoy:vacuum ratio.

### 6.2 The Beijing–Shanghai backbone and the Hefei metropolitan network

The **Beijing–Shanghai backbone (BSBN)**, inaugurated 30 August 2017, is the flagship: **over 2,000 km of fiber with 32 trusted relay stations** connecting Beijing, Jinan, Hefei, and Shanghai, interlinking four metropolitan networks each with >10 nodes. Reported performance includes **250 kbps key rate over a 43 km span**, a maximum inter-node link of **89.3 km (Hefei–Wuwei)**, and the design property that every node XORs and forwards keys without ever reading the end-to-end key material (trusted physically, not computationally). Because fiber QKD is distance-limited (~100 km practical reach), the backbone multiplexes the quantum channel with classical telecom traffic via WDM and is trialed for bank/securities/insurance traffic.

The **46-node Hefei metropolitan QKD network** (Chen et al., npj Quantum Inf. 7:124, 2021) is the most detailed urban deployment study: three subnetworks (USTC, QuantumCTek, City Library) ~15 km apart; polarization-encoded BB84 with vacuum+weak decoy states; a 16-port optical switch serving 16 users for **120 possible key-pairing schemes**, with switching-time qualification and optical-switch losses <1.2 dB (isolation 50 dB); device-to-network connection within 2 minutes of power-on; standard decoy-state BB84 security analysis with finite-size corrections. Applications carried: real-time voice telephony, instant messaging, and digital files under one-time-pad encryption, with **total encryption-path delay <50 μs**.

### 6.3 Satellite QKD and carrier-grade national networks

The Micius satellite extended the model: decoy-state BB84 from orbit shared **~300 kbit of key in a 273-second pass** near Beijing; **100 kilobytes** of secure keys supported a 75-minute Beijing–Vienna videoconference with 128-bit keys refreshed every second; entanglement distribution spanned **1,200 km** between Delingha and Lijiang; and ground-to-ground entanglement-based QKD over **1,120 km** yielded (in that first demonstration) 6 secure bits per pass — illustrating the distance/rate frontier. By 2021, a space-to-ground integrated network covered **4,600 km**.

Most recently (npj Quantum Inf. 2025, "Implementation of carrier-grade quantum communication networks over 10,000 km"), backbone + metropolitan QKD infrastructure spans **10,000+ km across 20 cities**, with four high-speed backbone QKD systems (three polarization-encoded at **625 MHz repetition rate**, one phase-encoded), low-speed metro decoy-BB84 plus two Gaussian-modulated **continuous-variable QKD** device types for lossy/short metro spans, time-division multiplexing to up to 24 user nodes per optical switch, ITU-T Y.3802-conformant functional architecture (quantum layer / key-management layer with one-time-pad key relaying / application layer), satellite ground stations in Beijing, Shanghai, Guangzhou, Chongqing, Hainan, Xinjiang, and Jinan-1 microsatellite key relay interconnecting satellite-ground and fiber segments.

### 6.4 Honest limits

Trusted relays are the acknowledged weak point: users must trust every relay's physical security; device imperfections motivate MDI-QKD and measurement-device-independent variants (already network-integrated in Chinese trials); and the ultimate fix — quantum repeaters with memory — remains beyond current hardware. European milestones for context: SECOQC (Vienna, 2007) at 3.1 kbps/33 km; Tokyo (2009) at 304 kbps/45 km; DARPA's earlier network. The comparison to note for smart-city planners: QKD's value proposition is forward secrecy against future quantum adversaries (Shor breaking RSA/ECC), which is why deployment continues even while rate/distance economics favor classical symmetric crypto with PQC alternatives for most traffic.

---

## 7. Quantum Annealing versus Gate-Model Computing: What the Benchmarks Say

A smart-city engineering team must choose between annealing (D-Wave, Fujitsu-style DA) and gate-model QAOA on IBM/IonQ hardware. The evidence:

### 7.1 Annealing-favorable measurements

- **Kim et al. (npj Quantum Inf. 11:77, 2025; arXiv:2504.06201):** benchmarked D-Wave **Advantage 4.1** (1,000 reads, 20 μs total anneal time) against classical solvers on >50 large dense-Hamiltonian instances. The state-of-the-art quantum (hybrid) solver reached **~0.013% higher accuracy and ~6,561× faster problem-solving time than the best classical solver** — the strongest peer-reviewed QA-favorable headline, though it depends on the hybrid configuration and instance family.
- **D-Wave application-oriented benchmarking (corporate technical deck, 2025, citing Lubinski et al. 2024 application-benchmark methodology):** on MAX-CUT, D-Wave annealing achieves **~98% of optimal at problem size 320**, whereas IBM gate-model QAOA achieves **~75% of optimal at size 6** and IonQ ~80% at size 10; claimed time-to-solution ratios of ~100× (vs IBM) and ~10,000× (vs IonQ). Treat as vendor-reported, but it aligns with the structural argument: gate-model QAOA at p ≤ 3 on ≤10 qubits is not competitive with thousands of annealing qubits on native Ising graphs.
- **Application lineage:** every large-scale city optimization in Sections 2–4 that actually ran on hardware (Inoue 2,500 signals partitioned; Rusnáková 25,000 vehicles via hybrid; Morstyn 5,760-qubit OPF; Kaseb AQPF up to 14-bus on QA) used annealing — no gate-model equivalent has run at that scale.

### 7.2 Measurements favoring classical or gate-model

- **Zeng et al. (Commun. Phys. 7:249, 2024):** quantum-annealing-inspired classical algorithms (bSB) achieve nearly **50-fold time-to-solution reduction versus the D-Wave machine** on Chimera-structured MAX-CUT up to 20,000 nodes — a reminder that "quantum-inspired" classical codes are the immediate practical competitor.
- **Pelofske et al. (Quantum Sci. Technol. 10:025025, 2025):** across three D-Wave generations (four devices), newer hardware improves optimal-solution sampling on minor-embedded max-clique/max-cut, but embedding overhead and small gaps still bound performance — the gains are incremental, not categorical.
- **Shikanai et al. (2023):** on real SUMO-mapped traffic maps, D-Wave failed to reach Gurobi's ground state and lost on runtime — negative but informative.
- **Structural gate-model advantages** cited in the literature: all-to-all connectivity on trapped ions (no minor-embedding chains), programmable mixers enabling constraint-preserving QAOA (Section 1.3), and error mitigation yielding "100× accuracy improvement" claims on IBM HPC-stacked workflows (IBM, 2025).

### 7.3 Synthesis

For unconstrained, large, dense Ising objectives at NISQ scale, annealing currently wins on scale and wall-clock; for constrained problems where feasible-by-construction mixers matter, and for algorithmic evolution toward error-corrected machines, gate-model QAOA is the strategic path. Hybrid loops dominate all real deployments, and Fujitsu-style digital annealers sometimes outperform quantum annealers simply because they accept larger QUBOs (Section 4.3) — the correct engineering question is not "quantum or not" but "which sampler sits inside the classical loop."

---

## 8. Benchmarks, Bibliometrics, and the State of the Field

### 8.1 Application-level benchmark suites

The field lacks a single canonical smart-city benchmark; instead, papers reuse (i) MAX-CUT/Ising families for algorithm comparison (Lubinski et al. 2024 "application-oriented benchmarking" framework, referenced by D-Wave and academic studies), (ii) standard electrical test systems (IEEE 14-bus, European LV Test Feeder, 33-node), (iii) standard routing instances (CVRP-style random 13-node sets in Dash et al.; 100-instance-per-size sweeps in Rusnáková et al.), and (iv) public environmental datasets (UK urban PM2.5, SEN12-FLOOD, weather station series). A dossier reader should treat any single-number quantum claim as instance-conditional unless reproduced across families.

### 8.2 Bibliometric landscape

- **Yigitcanlar, Hossain, Shaamala, Li (2026 preprint, DOI 10.20944/preprints202610.2727.v1; SSRN 6571118):** bibliometric mapping of **358 Scopus-indexed records** on quantum urbanism finds four dominant clusters — quantum optimization, quantum machine learning, quantum-secure smart-city systems, quantum communication — with the field concentrated in computer science (28.4%) and engineering (21.7%) while social sciences account for only 7.0%, confirming a governance/planning gap. Crucially for expectations management, the review characterizes headline gains such as **10–15% reductions in vehicle delay as proof-of-concept demonstrations on NISQ hardware and simulations**, concluding that quantum computing is a complementary capability — augmented by hybrid quantum–classical workflows as the realistic near-term pathway.
- **Conde-Torres et al. (EPJ Quantum Technol., 2026):** large-scale bibliometrics over **31,662 quantum-computing records (1980–2025)** documents explosive growth and thematic convergence — the macro backdrop for the smart-city subfield.
- **Earlier reviews:** Bashirpour Bonab et al.'s two 2023 reviews — a systematic review of urban quantum technologies (Technol. Forecast. Soc. Change 194:122642) and "Urban quantum leap" (Cities 140:104459), the latter combining 80 quantum articles with a taxonomy from 567 smart-city abstracts — establish that quantum communication (security) and quantum computing (transportation, AI, big-data, blockchain) are the two most promising urban technology classes; Yigitcanlar et al.'s "Quantum AI Urbanism" (J. Urban Technol. 32(3):213–226, 2025) supplies the layered conceptual framework; and the Cities special issue "Quantum Computing and the City" (submission deadline 31 Oct 2026, guest-edited by Yigitcanlar, Lai, Taeihagh, Quan, Fu) signals institutionalization of the field.

### 8.3 What a fair benchmark protocol looks like

Synthesizing the best practices implicit in Kim et al., Rusnáková et al., and Fitzek et al.: (1) publish the QUBO matrix or generator; (2) report instance counts per size (≈100/size is achievable); (3) give the classical solver equal wall-clock or equal-evaluation budgets and include exact solvers where tractable; (4) separate QPU time from end-to-end time (embedding, queueing, post-processing); (5) report feasibility rate before repair and quality after repair; (6) state optimizer (outer loop) and anneal parameters (reads, chain strength, schedule); (7) for QML, report both simulator and hardware results with deviation (as QLIF-CAST's 1.2% does).

---

## 9. Fault Tolerance and the Roadmap That Changes the Conclusions

Every limitation flagged above — millions of qubits for HVRP (Fitzek), 14-bus embedding ceilings (Kaseb), p-depth approximation-ratio ceilings (ma-QAOA) — is contingent on the fault-tolerant roadmap now in motion.

### 9.1 The qLDPC step-change

IBM's quantum low-density parity-check (qLDPC) codes (Nature cover, 2024) cut the physical-qubit overhead of error correction by **approximately 90% relative to surface codes**, the previously assumed gold standard, because non-local "bicycle"-architecture couplers (on-chip c-couplers linking distant qubits through low-loss routing layers) allow high-rate codes. Concrete resource points reported in IBM's 2025 technical papers: **144 physical qubits hosting 12 logical qubits** (with measurement qubits), or **288 physical qubits for the same 12 logical qubits at code distance 18** for higher error suppression. Real-time decoding — the classical bottleneck — was demonstrated at **<480 nanoseconds** latency on FPGAs with a **10× speedup** over the prior leading approach, delivered a year ahead of schedule (announced 12 Nov 2025 alongside IBM Quantum Loon, the processor exercising all fault-tolerant hardware elements, including qubit reset and long-range couplers).

### 9.2 The IBM roadmap: Loon (2025) → Kookaburra (2026) → Starling (2029) → Blue Jay (2033)

- **IBM Quantum Loon (2025):** validates qLDPC components (c-couplers, reset, low-loss routing) on hardware; supports ~30% more circuit complexity than its predecessor at comparable error rates.
- **IBM Quantum Kookaburra (2026):** first modular processor combining quantum memory with logic qubits — the building block for extending error correction beyond one chip.
- **IBM Quantum Starling (2029, Poughkeepsie data center):** **200 logical qubits executing 100 million quantum operations**, projected ~20,000× more work than today's machines; IBM states its state space (10^48+ memory) exceeds what today's best supercomputers could store — the "beyond-classical simulation" criterion.
- **IBM Quantum Blue Jay (2033):** **2,000 logical qubits executing 1 billion operations.**
- Supporting moves: 300 mm wafer fabrication (10× physical complexity per wafer for the correction roadmap), and a stated goal of quantum advantage by end of 2026 with fault tolerance by 2029.

### 9.3 What changes for smart cities at those milestones

Work backwards from the resource counts: (a) HVRP at ~10³ customers needs ~10⁶ physical-equivalent qubits today under edge encodings — Starling's 200 logical qubits with qLDPC efficiency plausibly enable **decomposed** versions (Dash-style hierarchies at depth, plus Grover-style quadratic gains on subproblems), not monolithic solves; (b) AQPF-class problems embedding 10⁵ variables (Fujitsu DA territory) become addressable on gate-model machines with error-corrected arithmetic (HHL/variational linear solvers plus QAOA refinement); (c) QML's barren-plateau and shot-noise limits relax as logical error rates fall, making the Section 5 gains reproducible on hardware rather than simulators; (d) QKD remains complementary — it is already deployable — but repeater-based entanglement swapping would eventually remove the trusted-relay caveat of Section 6. Conversely, gate-model fault tolerance does nothing for annealing-specific limitations (analog control precision, freeze-out), and annealing's advantage on dense Ising instances (Section 7.1) may persist into the early FTQ era, since annealers are not waiting for error correction to scale.

---

## 10. Limitations, Failure Modes, and an Honest Scorecard

1. **No demonstrated end-to-end quantum advantage on a smart-city problem.** The strongest results are: within-1% of Gurobi at 25,000 vehicles (annealing hybrid, Rusnáková), 6,561×/0.013% on selected dense instances (Kim et al., hybrid configuration), and near-matches on power flow (Kaseb). Where quantum is "faster," hybrid scaffolding usually carries the load.
2. **Embedding, not qubit count, binds annealers.** 5,760 physical qubits ≠ 5,760 variables; chains and Pegasus/Zephyr connectivity reduced AQPF to 14 buses and forced Inoue's 2,500 signals into partitions.
3. **QAOA depth is capped by noise; feasibility probabilities are low.** ≤10% valid-bitstring sampling at 19–21 qubits (Fitzek) means classical repair is mandatory and must be reported.
4. **Outer-loop optimizers dominate cost.** COBYLA/SPSA/Powell/basinhopping comparisons show order-of-magnitude runtime swings at fixed p; CVaR, warm starts, and multi-angle parameterizations are not optional refinements but load-bearing components.
5. **QML gains are dataset- and simulation-conditional.** Single-digit-to-ten-point accuracy jumps (Dong, Maity) come from simulator runs on modest qubit counts; only QLIF-CAST (1.2% hardware deviation) and the annealing-based QNN platform close the hardware loop at scale.
6. **Vendor benchmarks ≠ independent benchmarks.** D-Wave's 98%-at-320 figure and IBM's mitigation claims should be read alongside Zeng's 50× classical-inside-D-Wave result and Shikanai's negative finding.
7. **Penalty scaling and coefficient normalization are first-class problems.** Ill-conditioned QUBOs silently destroy analog precision; the better papers (Azfar, Rusnáková, Marchesin) treat this explicitly.
8. **Socio-technical gap.** Yigitcanlar's 358-record bibliometric shows only 7.0% social-science participation — governance, equity, and procurement questions for quantum-enabled cities are underdeveloped relative to the engineering.

**Scorecard by domain:** traffic signals — mature prototypes, hybrid deployment demonstrated, 10–24% objective gains reported but mostly proof-of-concept; routing — decomposition templates exist (12 vs 156 qubits), industrial scale still classical; power systems — clearest formulation work (Morstyn, Kaseb, Silva), embedding-limited on QA, actively benchmarked against NR/Gurobi; QML — promising deltas, hardware validation nascent; QKD — deployment-proven at 10,000-km/national scale; hardware platforms — annealing ahead for dense Ising at NISQ scale, gate-model ahead for constraints and the error-corrected future; fault tolerance — qLDPC + <480 ns decoding make 2029 Starling credible on paper.

---

## 11. Comparison Table

| Algorithm / method | City problem | Qubits (as reported) | Result vs classical baseline | Hardware |
|---|---|---|---|---|
| Hussain et al. 2020 QUBO + QBSolv/LEAP | Time-dependent traffic-signal phase selection (grid) | Sub-QUBOs per decomposition; hybrid loop | Outperforms naive selection; hybrid workflow handles city-scale (qualitative vs tuned classical control) | D-Wave LEAP hybrid solver |
| Inoue et al. 2021 Ising global control | Citywide signal timing, 50×50 lattice (2,500 signals) | 2,500 logical (partitioned to fit QPU) | Global QA better than simulated annealing; both far better than local control; analytic convergence at equal turn/straight probability | D-Wave 2000Q + graph partitioning |
| Marchesin et al. 2023 QUBO | Traffic-light activation patterns, urban road network | Not fixed (per-cycle optimization; chain strength/annealing-time study, 100 reads) | Outperforms traditional control in several conditions; reduces/contains congestion (qualitative; publisher PDF restricted) | D-Wave quantum annealer |
| Rusnáková et al. 2025 TFO QUBO + Leiden clustering | Citywide traffic-flow assignment, up to 25,000 vehicles | Cluster sub-QUBOs (embeddable) | Within ≈1% of Gurobi; 24.4% congestion-cost reduction (hybrid QA) vs 29.4% (Gurobi) vs shortest-route | D-Wave hybrid annealer + Gurobi/SA/tabu/CBC |
| Fitzek et al. 2024 QAOA | Heterogeneous vehicle routing (HVRP→Ising) | ~N_c² (quadratic in customers); 11–21 qubit instances run | Best energies with basinhopping/DE at ~10× runtime; ≤10–25% feasible sampling; classical handles >1,000 customers (quantum needs ~millions qubits end-to-end) | Simulated QAOA (NISQ-scale instances) |
| Dash et al. 2025 hierarchical QAOA (p=3, ma-QAOA + repair) | Multi-vehicle routing, 13-node/2-vehicle × 100 instances | 12 logical qubits/subproblem vs 156 direct edge encoding | Approximation ratio 1.2–1.5 vs Gurobi exact | Simulated (NISQ-oriented) |
| Azfar et al. 2025 link-based QAOA | VRP with flow conservation + subtour penalties | Link-based encoding; penalty scaling/normalization studied | Hardware-executed QAOA baseline (circuit complexity + coefficient conditioning focus) | IBM Quantum System One |
| Morstyn 2023 combinatorial OPF QUBO | EV smart charging + PV placement/sizing + network upgrades | Problem QUBO on 5,760-qubit device (hybrid solver; 30 solves/QUBO) | Finds feasible plans; upgrades enable 100 kWp PV vs 50 kWp without; advantage vs classical unclear (stated) | D-Wave Advantage 5,760-qubit QPU + hybrid |
| Kaseb et al. 2024 AQPF (QUBO/Ising digits) | AC power flow, 4-bus & 14-bus | QA: 14-bus QUBO / 4-bus Ising; DA up to 100,000 variables | Matches NR to ~4.57×10⁻² W / 1.67×10⁻³ var; fewer-than-NR iterations × orders-of-magnitude-faster clock; no divergence on ill-conditioned cases | D-Wave Advantage, hybrid, Fujitsu DA V3, 2× SA |
| Silva et al. 2023 QUBO reconfiguration | 33-node distribution network min-loss switching | QUBO over switch variables (33-node test) | Near-optimal reconfiguration vs conventional heuristics (simulated annealing-class baselines) | Simulated/annealing-based QUBO |
| Dong et al. 2024 QRELU-HQCNN-LSTM | Air-quality (AQI) time-series prediction | Simulated hybrid circuits (small PQC) | RMSE 11.48 vs 12.23 (HQCNN-LSTM) vs 12.36 (QRELU-CNN-LSTM) in Shanghai test; best across all three metrics | Simulator |
| Pires et al. 2026 wavelet + QNN nowcasting | PM2.5 nowcasting (UK urban data) | 172 logical qubits (also 86); 688 rotation gates at depth 4 | Best fidelity with 172-qubit depth-4 + wavelets; beats MLP/LSTM on raw high-entropy data (NMSE/Pearson reported) | Neuromorphic annealing platform (hybrid VQC + annealing) |
| Marchisio et al. 2026 QLIF-CAST | Multivariate weather forecasting | Core circuit on 156-qubit QPU | 15.4% lower MSE, 4.4% lower MAE vs classical LIF; up to 94% less training time vs QLSTM/QNN; 1.2% hardware-vs-simulation deviation | IBM Marrakesh (156 qubits), 1,000 shots |
| Lin et al. 2024 Quantum-Train LSTM | Flood/water-level prediction | O(polylog M) QNN params; classical LSTM inference | 18,830 vs 40,451 trainable params (>50% reduction) at slight accuracy cost; no quantum HW needed post-training | QNN simulated in training; classical inference |
| Maity & Ghanbarian 2026 Quantum-ViT | Flood detection (SEN12-FLOOD satellite imagery) | 4-qubit PQC branch | Accuracy 84.48% → 94.47%; F1 0.841 → 0.944; non-flooded recall +19.41 pts | Simulator |
| Decoy-state BB84 (Hefei 46-node; BSBN) | Municipal/enterprise secure communications | Single-photon qubits; 46 nodes (Hefei), 32 relays / 2,000+ km (Beijing–Shanghai) | 250 kbps over 43 km span; 120 key-pairings via 16-port switch; <50 μs OTP encryption delay; carrier-grade 10,000-km/20-city network (2025) | Fiber QKD + Micius satellite (trusted relay) |
| QA vs gate benchmark (Kim et al. 2025) | Generic combinatorial optimization (proxy for city QUBOs) | >5,000-qubit annealer | ~0.013% better accuracy, ~6,561× faster than best classical solver (hybrid); D-Wave deck: 98%-of-optimal at size 320 vs 75% at size 6 (gate) | D-Wave Advantage 4.1 vs classical/Gurobi-class |

---

## 12. Source Register (primary)

1. Hussain et al., *Quantum Inf. Process.* 19(9):312 (2020), arXiv:1912.07134.
2. Inoue et al., *Sci. Rep.* 11:3303 (2021), arXiv:2003.07527; D-Wave/Toyota case study.
3. Marchesin et al., *IEEE Trans. Quantum Eng.* 4:1–13 (2023), DOI 10.1109/TQE.2023.3312284.
4. Rusnáková, Chovanec, Gazda, arXiv:2510.06053 (v5, 2026).
5. Shikanai, Ohzeki, Tanaka, preprint DOI 10.21203/rs.3.rs-3302709/v1 (2023); Salloum et al., *Sci. Rep.* (2025), DOI 10.1038/s41598-025-04568-2.
6. Fitzek et al., *Sci. Rep.* 14:25415 (2024).
7. Dash et al., arXiv:2511.00506 (2025).
8. Azfar et al., arXiv:2505.01614v2 (2025).
9. Morstyn, *IEEE Trans. Smart Grid* 14(2):1093–1102 (2023), DOI 10.1109/TSG.2022.3200590.
10. Silva et al., *Sci. Rep.* 13:10777 (2023).
11. Kaseb et al., *Sci. Rep.* 14:23216 (2024), DOI 10.1038/s41598-024-73512-7 (+ supplement; QCE24 DOI 10.1109/QCE60285.2024.10396); Kaseb et al., *Electr. Power Syst. Res.* 235:110677 (2024).
12. Dong, Li, Zhu, Yan, *Front. Phys.* 12:1412664 (2024).
13. Pires et al., arXiv:2610.13882 (2026); Pires et al., *Energy and AI* (2025), DOI 10.1016/j.egyai.2025.100588-class (wind-speed QNN).
14. Marchisio et al., arXiv:2605.18333v3 (2026), IEEE QAI 2026.
15. Lin, Liu, Chen, arXiv:2407.08617 / IEEE QCE 2024; Liu et al., arXiv:2405.11304 (Quantum-Train).
16. Maity & Ghanbarian, arXiv:2603.13689 (2026), IEEE DCAS 2026.
17. Lo, Ma, Chen, *Phys. Rev. Lett.* 94:230504 (2005); Chen et al., *npj Quantum Inf.* (Hefei 46-node, 2021); USTC BSBN releases (2017); Liao et al. Micius results (*Nature* 549:43, 2017; *PRL* 120:030501, 2018; *Nature* 582:501, 2020); *npj Quantum Inf.* carrier-grade 10,000-km networks (2025).
18. Kim et al., *npj Quantum Inf.* 11:77 (2025), arXiv:2504.06201; Zeng et al., *Commun. Phys.* 7:249 (2024); Pelofske, *Quantum Sci. Technol.* 10:025025 (2025); D-Wave corporate benchmark deck (2025, citing Lubinski et al. 2024).
19. Yigitcanlar et al., preprint DOI 10.20944/preprints202610.2727.v1 / SSRN 6571118 (2026); Yigitcanlar et al., *J. Urban Technol.* 32(3):213–226 (2025); Bashirpour Bonab et al., *Cities* 140:104459 (2023) and *TFSC* 194:122642 (2023); Conde-Torres et al., *EPJ Quantum Technol.* (2026).
20. IBM newsroom/technical papers: qLDPC *Nature* (2024); Starling/Blue Jay roadmap (10 Jun 2025); Loon + <480 ns decoding (12 Nov 2025); IEEE Spectrum coverage (2025).
21. Barkoutsos et al., *Quantum* 4:256 (2020); Egger, Mareček, Woerner, *Quantum* 5:479 (2021); Farhi et al. (2014); Wilkie, Ostrowski, Herrman, arXiv:2404.10743 (ma-QAOA).

---

*End of dossier.*
