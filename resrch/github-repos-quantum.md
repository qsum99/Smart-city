# GitHub Repository Dossier: Quantum Computing for Smart Cities (Traffic, Energy, Routing, QML, QKD)

**Research type:** Web-only deep research (no code written, no repositories cloned)
**Research date:** 6 November 2026 (star counts, licences and recency figures are snapshots around this date; star figures come from GitHub-derived shields and are rounded by the provider above 1,000, e.g. "8k" for Qiskit)
**Sources:** github.com repository pages and repository search, shields.io GitHub badges (stars, licence, last-commit), raw README files from `raw.githubusercontent.com`, arXiv/DOI references quoted from the repositories' own READMEs, and paper links cited by the projects themselves. The `websearch` and `api.github.com` endpoints were unavailable during this research, so every figure below comes from direct GitHub/shield fetches rather than third-party aggregators.
**Coverage:** 49 repositories examined in depth across seven categories, plus a further list of ~12 secondary repositories noted during searches, with a master summary table of 49 rows.

## How to read this dossier

Each entry follows a fixed pattern: identity (URL, stars, language, licence, recency, maintainer) → what it actually implements (algorithms, reproduced papers, QUBO formulations) → key modules/directions and hardware targets → repository structure and code-quality signals → best-fit use cases for a smart-city researcher → limitations → a **VERDICT** line.

**Verdict legend**

- **essential** — a default/reference choice in its niche; cite it, build on it, or benchmark against it.
- **useful** — solid, maintained, worth adopting for specific layers of a smart-city quantum stack.
- **niche** — valuable only for a narrow purpose (teaching, a specific paper, a specific protocol, a specific city problem).
- **avoid-stale** — archived, deprecated in favour of a successor, or unmaintained; do not build new work on it (still citable as history).

**Hardware-target shorthand** used in the summary table: *gate* = gate-model circuits (simulator or superconducting/neutral-atom/ion hardware); *anneal* = D-Wave-style quantum annealing (QUBO/BQM); *hybrid* = quantum-classical hybrid stack that can target several backends; *simulator* = network/QKD simulation only.

---

# CATEGORY 1 — CORE QUANTUM FRAMEWORKS (the platforms everything else builds on)

## 1.1 `qiskit/qiskit` — Qiskit, the mainstream gate-model SDK

- **URL:** https://github.com/qiskit/qiskit
- **Stars:** ~8,000 ★ (badge: "8k") · **Language:** Python (plus Rust kernels) · **Licence:** Apache-2.0 · **Last commit:** badge "yesterday" (i.e. 5 November 2026 — daily commit activity) · **Maintainer:** the Qiskit community (originally IBM; development is now community-led with heavy IBM participation).

**What it implements.** The core SDK for building and executing quantum circuits: the circuit/circuit-library API (including the `n_local`, `zz_feature_map` and ansatz classes that `qiskit-machine-learning` builds on), the transpiler stack (routing, layout, basis translation, optimization passes), primitives (Sampler/Estimator V1 and V2), pulse-level and fake-backend tooling, and the standard classical-optimizer and utility routines. Every Qiskit-ecosystem package in this dossier (optimization, machine learning, nature, qopt-best-practices) depends on this repo, and so do most of the traffic/energy applications that call `qiskit_optimization` or `qiskit_aer`.

**Hardware targets.** Gate-model: local simulators (via the separate `qiskit-aer` package), IBM Quantum backends through Qiskit Runtime, and — via plugins — IonQ, Rigetti, IQM and others.

**Quality signals.** Daily commits, frequent releases, extensive CI, complete API documentation, migration guides between major versions (including the primitives V1→V2 transition that all downstream packages had to absorb), and the largest user community of any quantum SDK. This is the reference implementation the rest of the field benchmarks against.

**Best fit.** Any smart-city project that models its problem as circuits — QAOA for routing, VQE for small chemistry-adjacent subproblems, quantum kernels/variational classifiers for sensor data — and wants the widest selection of algorithms, backends and hiring pool.

**Limitations.** Rapid API churn (primitives, `algorithm_globals` relocation, deprecations) means tutorial code ages quickly; heavy stack; Qiskit Runtime/cloud access requires an IBM account.

**VERDICT: essential** — the de-facto standard gate-model SDK; if you use one quantum framework, this is the default.

## 1.2 `qiskit-community/qiskit-optimization` — QUBO/quadratic-program modelling layer (⚠️ no longer IBM-supported)

- **URL:** https://github.com/qiskit-community/qiskit-optimization
- **Stars:** 285 ★ · **Language:** Python · **Licence:** Apache-2.0 · **Last commit:** July 2026 · **Maintainer:** Qiskit community ecosystem (the README now carries an explicit **warning that Qiskit Optimization is no longer officially supported by IBM**, pointing users to the successor `qiskit-addon-opt-mapper`).

**What it implements.** The standard way to write an optimization problem once and solve it many ways. Modelling via **docplex** (IBM DOcplex) or programmatic `QuadraticProgram` objects → automatic conversion between representations (quadratic program ↔ Ising/QUBO via `to_ising`/`from_ising`, inequality penalties, integer-to-binary encodings) → a suite of solvers: `MinimumEigenOptimizer` wrapping **QAOA** or VQE, `GroverOptimizer` (Grover adaptive search), ADMM, warm-start and recursive optimizers, plus wrappers for **CPLEX, Gurobi, CVXPY (Goemans–Williamson)** as classical baselines. Application classes include Max-Cut, TSP, vehicle routing, bin packing and portfolio optimization — the closest thing Qiskit has to ready-made smart-city problem templates. Tutorials cover the full QAOA workflow (its README quick-start runs a 4-node Max-Cut with `SamplerV2` + SPSA + a preset pass manager on `AerSimulator`).

**Hardware targets.** Gate-model via Qiskit primitives (simulators or IBM hardware); the same `QuadraticProgram` can also be exported as a QUBO matrix and fed to annealers — a common hybrid pattern with D-Wave.

**Quality signals.** Unit-test workflow badge, coverage (Coveralls) badge, hosted tutorials, releases on PyPI. **Limitation signals:** the official-support warning and the pointer to `qiskit-addon-opt-mapper` mean new feature work is migrating elsewhere; star count (285) is low relative to its importance because the package lives under the `qiskit-community` org.

**Best fit.** Researchers who need a **clean QUBO formulation pipeline** for traffic-signal, routing or unit-commitment problems with classical-optimizer baselines built in; also the layer most paper-companion repos import.

**Limitations.** Deprecated-by-IBM status (use-as-is under Apache-2.0, but plan a migration path); docplex dependency adds weight; some tutorials still reference older primitive APIs.

**VERDICT: useful** — still the most convenient QUBO modelling toolkit on Qiskit, but adopt it with the successor library on your roadmap.

## 1.3 `qiskit-community/qiskit-machine-learning` — quantum kernels and QNNs on Qiskit

- **URL:** https://github.com/qiskit-community/qiskit-machine-learning
- **Stars:** 1.1k ★ · **Language:** Python · **Licence:** Apache-2.0 · **Last commit:** August 2026 · **Maintainer:** Qiskit community ecosystem — the README states that as of v0.7 the library is **co-maintained by IBM and the Hartree Centre (UK STFC)**.

**What it implements.** The QML building blocks used in every "quantum ML for city data" experiment: **kernel methods** (`FidelityQuantumKernel`, `QSVC`, `QSVR`, plus `TrainableFidelityQuantumKernel` for hybrid kernels), **quantum neural networks** (`EstimatorQNN`, `SamplerQNN`), high-level **`VQC`/`VQR`** variational classifier/regressor that assemble feature map + ansatz automatically, learning algorithms (`NeuralNetworkClassifier/Regressor`), and the **`TorchConnector`** that embeds a QNN inside PyTorch with end-to-end autodiff (quantum layer inside a classical deep net). Its own arXiv overview paper is **arXiv:2505.17756**, and tutorials are hosted on GitHub Pages.

**Hardware targets.** Qiskit primitives — local simulators or IBM Quantum hardware; kernels can be evaluated on hardware with error mitigation.

**Quality signals.** CI badge, coverage badge, PyPI download badges, arXiv paper, active docs site, large tutorial set. This is one of the better-maintained community Qiskit packages.

**Best fit.** Quantum ML experiments on **urban sensor/traffic/AQI tabular data** when your pipeline already lives in Python/sklearn-style APIs; the `TorchConnector` is the easiest route to hybrid deep models.

**Limitations.** Kernel methods' sample-complexity advantage on near-term hardware is contested (the repo itself links benchmark literature); training QNNs on real hardware is slow; API surface is large.

**VERDICT: essential** — the reference QML library for the Qiskit ecosystem.

## 1.4 `qiskit-community/qiskit-nature` — quantum chemistry/physics problems

- **URL:** https://github.com/qiskit-community/qiskit-nature
- **Stars:** 399 ★ · **Language:** Python · **Licence:** Apache-2.0 (with a Gaussian-16 driver sub-component under the Gaussian Open-Source Public Licence) · **Last commit:** August 2026 · **Maintainer:** Qiskit community ecosystem.

**What it implements.** Solving **quantum-mechanical natural-science problems**: ground and excited states of electronic and vibrational structure problems, molecular dipole moments, Ising and Fermi–Hubbard models on lattices. Modules: data loading from chemistry drivers (PySCF, PSI4, Gaussian 16) or file formats, second-quantized operator construction, qubit-space mapping (Jordan–Wigner, Bravyi–Kitaev, parity), a library of chemistry-targeted ansatze, and problem-specific algorithms. Optional integrations: `qiskit-nature-pyscf`, sparse arrays, `opt_einsum`.

**Hardware targets.** Gate-model (VQE/UCC-style workflows) on simulators or IBM hardware.

**Quality signals.** CI/coverage badges, releases, hosted tutorials, Zenodo DOI for citation. Maintenance is real (August 2026 commits).

**Best fit.** For a smart-city dossier this is mostly **adjacent**: battery/materials chemistry research, or lattice models (Fermi–Hubbard) — not grid dispatch or traffic. Include it only if your "quantum for cities" story includes energy-storage materials simulation.

**Limitations.** Not a power-systems or urban package; driver dependencies (PySCF etc.) are heavyweight; modest star count.

**VERDICT: niche** — excellent for molecular/lattice quantum chemistry, largely irrelevant to traffic/energy-operations questions.

## 1.5 `quantumlib/Cirq` — Google's gate-model framework

- **URL:** https://github.com/quantumlib/Cirq
- **Stars:** 5.1k ★ · **Language:** Python · **Licence:** Apache-2.0 · **Last commit:** badge "today" · **Maintainer:** Google Quantum AI (quantumlib organisation).

**What it implements.** A gate-model framework with explicit control over device topology, moments, noise models and schedules — designed around Google's superconducting hardware (Sycamore line) but hardware-agnostic in practice. It is also the simulation backend behind **SimulaQron**'s modern backends (see 6.2) and underpins **TensorFlow Quantum** (see 5.3). Ecosystem: `cirq-core`, `cirq-google`, `cirq-ionq`, `cirq-rigetti`, `cirq-aqt`, plus `qsim` (high-performance simulator, separate repo).

**Hardware targets.** Gate-model: Google/NISQ hardware via `cirq-google`, ion-trap and other partner backends, and local simulators.

**Quality signals.** Daily commits, first-class Google engineering, thorough docs, large citation footprint. Actively developed as of the research date.

**Best fit.** Projects needing **low-level circuit/noise control** (noise studies, error-mitigation research) or that must interoperate with TFQ/SimulaQron.

**Limitations.** Smaller algorithm library than Qiskit — most optimization/QML applications must be written by hand; less "batteries included" for QUBO workflows.

**VERDICT: essential** — the second pillar of gate-model frameworks; default choice when Cirq-native tooling (TFQ, SimulaQron backend) is involved.

## 1.6 `PennyLaneAI/pennylane` — differentiable quantum ML library

- **URL:** https://github.com/PennyLaneAI/pennylane
- **Stars:** 3.5k ★ · **Language:** Python · **Licence:** Apache-2.0 · **Last commit:** badge "today" · **Maintainer:** Xanadu (PennyLaneAI).

**What it implements.** A **differentiable programming** framework for quantum circuits: `qml.qnode` decorators with backpropagation or parameter-shift gradients, a large circuit-template library (templates, layers, ansatze), optimizers and cost functions, and a plugin architecture that routes the *same* QML code to Qiskit, Braket, Cirq, IonQ, Rigetti and more. This is the library used by **quantumgrid** (energy, 4.2), **FedQSense** (7.2) and **quantum-gnn-rl-opf** (4.4) in this dossier — PennyLane is the glue that lets city researchers swap simulators/hardware without rewriting models.

**Hardware targets.** Hybrid: hardware-agnostic via plugins (IBM, Amazon Braket, Cirq, IonQ, Rigetti, AWS/others); strong local simulators (`default.qubit`, Lightning).

**Quality signals.** Daily commits, extensive documentation and tutorials, academic citation (Xanadu papers), large plugin ecosystem, demos site. One of the healthiest quantum projects on GitHub.

**Best fit.** Any quantum-ML or variational-optimization work where you want **gradients for free** and backend portability — especially hybrid PyTorch/TensorFlow/JAX pipelines (PennyLane integrates with all four autodiff frameworks).

**Limitations.** QUBO/annealing workflows are not its centre of gravity (that's D-Wave/Ocean); performance-critical code still lives in plugins.

**VERDICT: essential** — the default framework for quantum machine learning and variational algorithms outside the IBM stack.

## 1.7 `ProjectQ-Framework/ProjectQ` — ETH Zurich compiler/emulation framework (stale)

- **URL:** https://github.com/ProjectQ-Framework/ProjectQ
- **Stars:** 976 ★ · **Language:** Python (+ C++ engine) · **Licence:** Apache-2.0 · **Last commit:** April 2024 (~2.5 years stale) · **Maintainer:** former ETH Zurich / QBlox group (largely dormant).

**What it implements.** An early (2017-era) gate-model framework: a powerful **compiler** (automatic decompositions, circuit optimisation, layout/routing), an **emulation** engine capable of simulating up to ~30+ qubits with a Python-API/C++ core, and hardware backends (IBM, AWS). Historically important for its compiler design, which influenced later tools.

**Hardware targets.** Gate-model simulators + legacy IBM/AWS backends (APIs may no longer match current services).

**Quality signals (negative).** No commits since April 2024; docs and backend bindings predate the primitives era; effectively unmaintained.

**Best fit.** Historical citation for quantum compiler design; occasionally useful for its high-performance emulator if you pin old dependencies.

**Limitations.** Won't run cleanly against current Qiskit/AWS APIs; no roadmap; not a basis for new work.

**VERDICT: avoid-stale** — cite as history, do not build on it.

## 1.8 `amazon-braket/amazon-braket-sdk-python` — Amazon Braket SDK (multi-hardware cloud access)

- **URL:** https://github.com/amazon-braket/amazon-braket-sdk-python
- **Stars:** 373 ★ · **Language:** Python · **Licence:** Apache-2.0 · **Last commit:** badge "today" · **Maintainer:** Amazon Web Services.

**What it implements.** The client SDK for **Amazon Braket**: a single API for trapped-ion (IonQ), superconducting (Rigetti, IQM), neutral-atom (QuEra, Pasqal) devices and local/managed simulators; device/task abstractions, cost tracking, batch jobs, openQASM support, and hybrid-job patterns that pair classical code with quantum tasks. Used by `openqaoa` (2.1) as one of its execution backends.

**Hardware targets.** Multi-vendor gate-model hardware through AWS; annealing is *not* Braket's focus (D-Wave is accessible via separate D-Wave Leap, not this SDK).

**Quality signals.** Daily commits, AWS-grade CI/release discipline, hosted docs. The practical way to avoid vendor lock-in.

**Best fit.** Smart-city experiments that need **hardware access beyond a single vendor**, or AWS-centred production pipelines (IAM, VPC, cost governance).

**Limitations.** Requires an AWS account and per-task billing; Python-only SDK depth for advanced pulse-level control; star count understates usage (it is a library inside bigger AWS estates).

**VERDICT: useful** — the standard cloud portability layer for gate-model hardware.

## 1.9 `dwavesystems/dwave-ocean-sdk` — D-Wave Ocean SDK (the annealing stack)

- **URL:** https://github.com/dwavesystems/dwave-ocean-sdk
- **Stars:** 545 ★ · **Language:** Python · **Licence:** Apache-2.0 · **Last commit:** badge "last Wednesday" · **Maintainer:** D-Wave Systems.

**What it implements.** The metapackage that installs the full **quantum-annealing toolbox**: `dimod` (BQM/QUBO data structures), `dwave-system` (D-Wave samplers, `EmbeddingComposite` for minor-embedding of arbitrary QUBOs onto the Pegasus/Zephyr graph), `dwave-networkx` (graph algorithms and network/embedding utilities), `dwave-hybrid` (classical-quantum hybrid workflow engine), `dwave-cloud-client`, `dwave-neal`/`dwave-samplers` (classical annealing/tabu samplers), `dwave-sampling` and others. Nearly every annealing-based smart-city repo in Categories 3–4 either depends on Ocean or reimplements a subset of it.

**Hardware targets.** Annealing: D-Wave Leap QPUs (Advantage/Advantage2) plus local classical samplers; Ocean also supports QUBO export to other solvers.

**Quality signals.** Weekly-level commit activity, releases, documentation site, integration tests against live QPUs, examples gallery. Mature commercial open source.

**Best fit.** The **default stack for any QUBO-shaped city problem**: traffic-signal control, routing, unit commitment, sensor placement — anywhere you can write a binary quadratic model.

**Limitations.** D-Wave account/Leap subscription for real QPUs; annealing ≠ gate-model (no QAOA here); minor-embedding overhead grows with problem density.

**VERDICT: essential** — the reference platform for quantum annealing applications.

## 1.10 Ocean sub-packages: `dimod`, `dwave-system`, `dwave-neal`, `dwave-samplers`

- **URLs:** https://github.com/dwavesystems/dimod · https://github.com/dwavesystems/dwave-system · https://github.com/dwavesystems/dwave-neal · https://github.com/dwavesystems/dwave-samplers
- **Stars:** dimod 142 ★ · dwave-system 99 ★ · dwave-neal 64 ★ · dwave-samplers 21 ★ · **Language:** Python · **Licence:** Apache-2.0 (all four) · **Last commits:** dimod "last Tuesday", dwave-system "last Wednesday", dwave-samplers "August" 2026, **dwave-neal June 2022** · **Maintainer:** D-Wave Systems.

**What they implement.** `dimod` defines the `BinaryQuadraticModel`/`SampleSet` vocabulary that the whole annealing world shares (you will meet it in every QUBO paper's code). `dwave-system` provides `DWaveSampler`, `SimulatedAnnealingSampler` wrappers and the embedding machinery that maps your traffic/routing QUBO onto hardware. `dwave-neal` is the classic pure-Python **simulated annealing** sampler — convenient, but its last commit was June 2022 and D-Wave has **deprecated it in favour of `dwave-samplers`**, which reimplements SA (plus tabu search and others) in a maintained package. Note that several older city-research repos (e.g. `Quantum-Sensor-Assignment`, 7.3) still import `neal` directly.

**Quality signals.** dimod and dwave-system are actively maintained and are the real APIs; dwave-neal is a legacy package (works, but frozen); dwave-samplers is new and thin (few stars because it is a recent split-out).

**Best fit.** dimod + dwave-system are unavoidable if you touch annealing; use `dwave-samplers` (not `neal`) for any new classical baseline.

**Limitations.** Four repos where one mental model would do; neal's deprecation catches old tutorials.

**VERDICT: dimod useful · dwave-system useful · dwave-samplers useful · dwave-neal avoid-stale (deprecated; switch to dwave-samplers).**

## 1.11 `pasqal-io/Pulser` — neutral-atom pulse-level control

- **URL:** https://github.com/pasqal-io/Pulser
- **Stars:** 257 ★ · **Language:** Python · **Licence:** Apache-2.0 · **Last commit:** badge "today" · **Maintainer:** Pasqal (French neutral-atom hardware company).

**What it implements.** A **pulse-level** (not gate-level) SDK for Pasqal's neutral-atom quantum processors: you describe atom arrangements (register layouts), detuning/phase Rabi pulses, and digital-analog sequences, then simulate locally (`pulser_simulation`, QuTiP-based) or execute on Pasqal devices. Also relevant: `Pulser-Simulation`, `pulser-pasqal` cloud bindings. Neutral-atom machines are increasingly used for combinatorial optimization (atom-based annealing/Ising machines), which is why this appears in a smart-city optimization dossier.

**Hardware targets.** Gate/analogue-neutral-atom hardware (Pasqal Fresnel/Orsay line) + local QuTiP simulation.

**Quality signals.** Daily commits, docs, examples, active releases. Modern and healthy, but a niche community relative to Qiskit/PennyLane.

**Best fit.** Exploring **analog/neutral-atom optimization** for city problems (e.g. Ising formulations on atom arrays) or atom-array sensing experiments.

**Limitations.** Steep mental model (pulses, not circuits); little out-of-the-box QUBO/QML tooling; requires Pasqal access for hardware.

**VERDICT: useful** — the leading open SDK for the neutral-atom hardware family, worth watching for optimization workloads.

---

# CATEGORY 2 — QAOA & COMBINATORIAL-OPTIMIZATION TOOLKITS

## 2.1 `entropicalabs/openqaoa` — multi-backend QAOA SDK

- **URL:** https://github.com/entropicalabs/openqaoa
- **Stars:** 143 ★ · **Language:** Python · **Licence:** MIT · **Last commit:** July 2026 · **Maintainer:** EntroPy (QunaSys affiliate; docs at openqaoa.readthedocs.io; paper **arXiv:2210.08695**).

**What it implements.** A full **QAOA workflow library**: problem encoders (Max-Cut and generic QUBO), circuit construction, parameter-initialisation strategies (random, interpolation across graph sizes, adaptive strategies from the literature), backends spanning **local simulators, Qiskit (IBM), Amazon Braket, Azure Quantum, Cirq** and cloud simulators, and experiment orchestration (batch runs, parameter scans, result analysis). Positioned as "QAOA as a service" for practitioners who want one API across hardware vendors.

**Hardware targets.** Hybrid/multi-backend: gate-model simulators and IBM/Braket/Azure/Cirq hardware.

**Quality signals.** CI, ReadTheDocs documentation, tutorials, releases, an arXiv paper. Commit activity slowed to July 2026 — maintained but not frantic.

**Best fit.** Running the **same QAOA experiment across backends** (e.g. compare a routing QBO on a simulator vs IBM hardware vs Braket ion trap) without rewriting glue code.

**Limitations.** Smaller community than Qiskit itself; QAOA-only (no annealing); dependency on several cloud SDKs; some features lag current Qiskit releases.

**VERDICT: useful** — the best dedicated QAOA orchestration layer, slightly cooling in activity.

## 2.2 `OpenQuantumComputing/QAOA` — QAOA research implementations

- **URL:** https://github.com/OpenQuantumComputing/QAOA
- **Stars:** 69 ★ · **Language:** Python (notebooks) · **Licence:** GPL-3.0 · **Last commit:** September 2026 · **Maintainer:** the OpenQuantumComputing research group (publication-linked repository).

**What it implements.** A collection of **QAOA implementations and study code accompanying the group's publications**: circuit constructions, parameter studies, and comparisons of QAOA variants on standard problems (Max-Cut and related combinatorial instances). Think of it as a paper-companion collection rather than a library — useful for reproducing reported QAOA behaviour and for seeing how the authors set parameters.

**Hardware targets.** Gate-model (simulators; hardware-portable circuits).

**Quality signals.** Active commits (September 2026) but GPL-3.0 licence (copyleft — problematic if you want to vendor the code into a permissively licensed stack), notebook-centric layout, no packaging.

**Best fit.** Reproducing specific QAOA papers; learning parameter-setting tricks from working code.

**Limitations.** Not a library (no pip package); GPL licence; depends which papers you need.

**VERDICT: niche** — valuable when you need the specific experiments, otherwise use openqaoa or qiskit-optimization.

## 2.3 `QAOAKit/QAOAKit` — toolkit for reproducible QAOA experiments (stale)

- **URL:** https://github.com/QAOAKit/QAOAKit
- **Stars:** 54 ★ · **Language:** Python · **Licence:** BSD-2-Clause · **Last commit:** June 2022 (~4 years stale) · **Maintainer:** academic contributors (QOSF-adjacent community).

**What it implements.** Utilities for **reproducible QAOA studies**: building QAOA circuits for standard problems, retrieving pre-computed optimal parameters from the literature, and comparing results across papers — an attempt at a shared benchmark harness for QAOA before the field matured.

**Hardware targets.** Gate-model simulators (Qiskit-era APIs).

**Quality signals (negative).** No commits since June 2022; predates Qiskit primitives and the 1.x API wave; installs against old dependency pins at best.

**Best fit.** Checking historical QAOA parameter values cited in papers.

**Limitations.** Effectively unmaintained; broken against modern Qiskit; superseded by QOBLIB-style benchmark suites (2.5).

**VERDICT: avoid-stale** — historically interesting, not a going concern.

## 2.4 `qiskit-community/qopt-best-practices` — IBM's QAOA-on-hardware playbook

- **URL:** https://github.com/qiskit-community/qopt-best-practices
- **Stars:** 50 ★ · **Language:** Python · **Licence:** Apache-2.0 · **Last commit:** June 2026 · **Maintainer:** Qiskit community (IBM Research authors of the cited papers).

**What it implements.** A **pip-installable package of reference implementations plus how-to notebooks** for running QAOA well on superconducting hardware: (1) **qubit selection**, (2) **SAT mapping** for initial layouts (arXiv:2212.05666), (3) **SWAP strategies** for circuit routing (arXiv:2202.03459, published in *Quantum* 6, 870), (4) the **QAOA cost-function convention** (depth-one ansatz `exp(-iβHm)exp(-iγHc)|+⟩^n` minimising `Hc = Σ w_ij Z_iZ_j`, mixer `Hm = -Σ X_i`, with the implied `Rx(-2β)`/`Rzz(2γw)` gate-level construction), all tied to the noise-mitigation workflow of **arXiv:2307.14427** (Sack & Egger, large-scale QAOA on non-planar graphs).

**Hardware targets.** Gate-model superconducting hardware via Qiskit (with simulators for testing).

**Quality signals.** Documented conventions with explicit formulas, notebook tutorials, clean package layout, June 2026 commits, Apache licence. The README honestly labels the code "prototypes, not feature-complete" — set expectations accordingly.

**Best fit.** Anyone running **QAOA for a city-routing QUBO on real IBM hardware** who needs layout/routing choices that actually work — this repo encodes the practical tricks that papers usually leave out.

**Limitations.** QAOA-specific; prototype-grade wrappers around Qiskit transpiler passes; small team, modest star count.

**VERDICT: useful** — the single most practical "make QAOA work on hardware" reference available.

## 2.5 `ZIB-AOPT/QOBLIB` — the quantum optimization benchmark library (this is the "QOptLib" you may be thinking of)

- **URL:** https://github.com/ZIB-AOPT/QOBLIB
- **Stars:** 60 ★ · **Language:** Python · **Licence:** Apache-2.0 · **Last commit:** badge "last Saturday" (1 November 2026) · **Maintainer:** ZIB (Zuse Institute Berlin) Algorithms & Optimization department.

**What it implements.** A **standardized benchmark library for quantum optimization**: curated problem-instance generators and reference solutions across ~10 benchmark problem classes (combinatorial families in the max-cut/Ising and QUBO tradition plus application-shaped classes), designed so that quantum (QAOA, annealing, QUBO-solver) and classical methods can be compared on identical instances. It is backed by a peer-reviewed paper — **arXiv:2504.03832**, published in *Nature Computational Science* — and is the successor-generation answer to the "we need agreed benchmarks" gap that QAOAKit (2.3) tried to fill.

**Hardware targets.** Solver-agnostic: outputs QUBO/Ising instances consumable by gate-model (QAOA) *and* annealing solvers.

**Quality signals.** Academic institution (ZIB), Nature-tier publication, Apache licence, active commits (last Saturday). Small star count is typical for a new benchmark suite.

**Best fit.** **Benchmarking your smart-city QUBO formulation** against standardized instances; citing a defensible baseline in papers; avoiding the "my instances are cherry-picked" reviewer objection.

**Limitations.** New and therefore small instance catalogue relative to something like MIPLIB; not an application framework.

**VERDICT: useful** — the emerging standard for quantum-optimization benchmarking; note that a search for an IBM "QOptLib" turns up nothing — this ZIB library is the real QUBO/quantum benchmark repo.

## 2.6 `Jij-Inc/OpenJij` — general-purpose Ising/QUBO framework

- **URL:** https://github.com/Jij-Inc/OpenJij
- **Stars:** 141 ★ · **Language:** Python (C++ core) · **Licence:** Apache-2.0 · **Last commit:** August 2026 · **Maintainer:** Jij Inc. (Japanese optimization company; commercial sibling `jijjij`/amplify-adjacent ecosystem).

**What it implements.** A framework for **constructing and solving Ising/QUBO models**: model-building helpers, **simulated quantum annealing (SQA)** and simulated annealing samplers, GPU acceleration, a `jij`-style interaction-graph representation, and interfaces to D-Wave samplers. Used directly by `Quantum-Sensor-Assignment` (7.3) as its solver backend, alongside `neal` and MILP.

**Hardware targets.** Hybrid: classical simulated (quantum) annealing on CPU/GPU, plus pluggable D-Wave annealing.

**Quality signals.** Regular commits (August 2026), documentation site, company backing, Apache licence. Healthy mid-size project.

**Best fit.** A **permissive-licence classical/annealing baseline** for city QUBOs when you don't want a D-Wave account, or when you need SQA on GPU.

**Limitations.** Not a gate-model/QAOA toolkit; English docs thinner than Qiskit's; community smaller than Ocean's.

**VERDICT: useful** — solid QUBO solving layer with GPU-capable classical annealing.

## 2.7 `recruit-communications/pyqubo` — Python DSL for building QUBOs

- **URL:** https://github.com/recruit-communications/pyqubo
- **Stars:** 201 ★ · **Language:** Python · **Licence:** Apache-2.0 · **Last commit:** November 2024 (~1 year stale) · **Maintainer:** Recruit Communications (Japanese company; same lineage as the original PyQUBO/Chainer-adjacent ecosystem).

**What it implements.** A **domain-specific language for expressing QUBO/Ising problems mathematically**: compose `Placeholder` variables, sums and products, encode constraints via penalty terms with a clean `encode()` step (which compiles the expression into an efficient QUBO matrix), and export to samplers. The pitch is exactly what city researchers fumble with: writing `Σ w_ij (x_i - x_j)² + λ·penalty` without hand-deriving every coefficient.

**Hardware targets.** Hybrid: exports QUBOs to D-Wave/other annealers; gate-model users can take the matrix into Qiskit's `QuadraticProgram`.

**Quality signals.** Apache licence, 201 stars (high for a QUBO DSL), tutorial repo (`kitamuyu/pyqubo-tutorial`), but last commit November 2024 — maintenance is quiet.

**Best fit.** Rapid, readable **QUBO formulation of constraints** (time windows, capacity, signal-coordination constraints) before handing the matrix to a solver.

**Limitations.** Frozen-ish since late 2024; niche ecosystem; no built-in benchmarks.

**VERDICT: useful** — still the nicest way to *write* QUBOs in Python; watch its maintenance status.

## 2.8 `fixstars/amplify-benchmark` — benchmark harness for Fixstars Amplify (commercial annealer)

- **URL:** https://github.com/fixstars/amplify-benchmark
- **Stars:** 11 ★ · **Language:** Python · **Licence:** MIT · **Last commit:** October 2023 (~3 years stale) · **Maintainer:** Fixstars Corporation (vendor of the commercial Amplify annealing solver).

**What it implements.** A benchmark harness comparing the commercial **Amplify** solver (GPU simulated annealing / simulated bifurcation) against reference solvers on combinatorial instances — the vendor's attempt at transparent benchmarking.

**Hardware targets.** Hybrid: commercial GPU annealer (licence required for real use) — not quantum hardware per se, but part of the same "QUBO solver" market.

**Quality signals.** MIT licence, clean but dormant (October 2023); tiny star count; requires the commercial product for meaningful runs.

**Best fit.** Comparing annealing baselines if you already use Amplify; mostly a pointer to the commercial solver landscape.

**Limitations.** Stale, vendor-tied, small.

**VERDICT: niche** — only relevant if evaluating Fixstars' commercial solver.

---

# CATEGORY 3 — TRAFFIC, ROUTING & CITY QAOA REPOSITORIES

## 3.1 `mbinjavaid/traffic_signals_qubo` — QUBO traffic-signal control on D-Wave (paper companion)

- **URL:** https://github.com/mbinjavaid/traffic_signals_qubo
- **Stars:** 8 ★ · **Language:** Python · **Licence:** **none** (no LICENSE file) · **Last commit:** July 2023 · **Maintainer:** academic author (companion code to a 2020 journal paper).

**What it implements.** The repository explicitly states it is "**our paper**" companion code: a **QUBO formulation of traffic-signal control** solved with **D-Wave quantum annealing** (`main.py` builds the model and calls Ocean/D-Wave). The linked paper is **doi:10.1007/s11128-020-02815-1** (*Quantum Information Processing*, 2020 — the Hussain et al. line of work on quantum-annealed traffic signal control that much of the later "quantum traffic" literature cites).

**Hardware targets.** Annealing (D-Wave); the QUBO matrix is solver-agnostic.

**Quality signals.** Tiny (8 stars, no licence, no tests, no CI), but it is one of the very few repos that is a **direct companion to a peer-reviewed traffic-signal QUBO paper** — citable provenance beats engineering polish here.

**Best fit.** Reproducing the Hussain 2020 QUBO formulation; starting point for your own signal-coordination model.

**Limitations.** No licence (legally ambiguous to reuse), no tests, dated Ocean APIs, small scope.

**VERDICT: niche** — a citable paper artifact, not a product; read it for the formulation, rewrite it for your stack.

## 3.2 `mbinjavaid/traffic-routes-qc` — reproducing D-Wave traffic routing (arXiv:1708.01625)

- **URL:** https://github.com/mbinjavaid/traffic-routes-qc
- **Stars:** 4 ★ · **Language:** Python · **Licence:** none · **Last commit:** January 2020 · **Maintainer:** same author group as 3.1.

**What it implements.** A recreation of the **traffic-routing experiment described in arXiv:1708.01625** — the D-Wave-based *traffic routing / flow-optimisation* study (route-selection QUBOs on a city graph, solved by quantum annealing). Code converts a routing instance into a QUBO and submits it to D-Wave.

**Hardware targets.** Annealing (D-Wave).

**Quality signals.** 4 stars, no licence, last commit January 2020 — a research scratchpad that survived on GitHub rather than a maintained tool.

**Best fit.** Understanding how the 2017-era D-Wave routing paper encoded route choice as a QUBO (historical reproduction).

**Limitations.** Ancient (2020), undocumented, no licence, APIs predate Ocean 6.

**VERDICT: avoid-stale** — cite the paper, not this code; reuse only as a formulation reference.

## 3.3 `gurolsaglam/TrafficFlowOptimization` — archived QUBO+annealing traffic-flow demo

- **URL:** https://github.com/gurolsaglam/TrafficFlowOptimization
- **Stars:** 4 ★ · **Language:** Python · **Licence:** none · **Last commit:** June 2020 · **Status:** **archived** (read-only on GitHub) · **Maintainer:** individual researcher.

**What it implements.** A minimal **traffic-flow optimisation via QUBO + (simulated/quantum) annealing**: formulate flow assignment as a binary quadratic model and solve it. The README is essentially one line — there is no paper link, no docs.

**Hardware targets.** Annealing (QUBO-shaped).

**Quality signals (negative).** Archived, one-line README, no licence, no tests. It shows up in searches for "QUBO traffic" but offers little beyond the idea itself.

**Best fit.** Nothing you should depend on; at most a 5-minute skim.

**Limitations.** Read-only archive, zero documentation.

**VERDICT: avoid-stale** — archived toy repo.

## 3.4 `CybroatriX/Quantum-Enhanced-Adaptive-Urban-Traffic-Optimization` (FlowQ) — YOLOv8 + SUMO + QUBO/QAOA pipeline

- **URL:** https://github.com/CybroatriX/Quantum-Enhanced-Adaptive-Urban-Traffic-Optimization
- **Stars:** 3 ★ · **Language:** Python · **Licence:** Apache-2.0 · **Last commit:** 20 September (recent) · **Maintainer:** CybroatriX (small team).

**What it implements.** The most **system-integrated** traffic entry in this dossier: an "**adaptive urban traffic optimization**" pipeline combining **YOLOv8** vehicle detection, **SUMO** traffic simulation, a **QUBO encoding** of signal/phase decisions and a **QAOA** solver loop — i.e. vision → simulation → quantum optimization → re-simulation. The README claims a test suite (159 tests) and includes architecture diagrams.

**Hardware targets.** Gate-model (QAOA; simulator-first, hardware-portable circuits).

**Quality signals.** **Red flag:** the README contains **unresolved merge-conflict markers** (Git conflict artefacts committed to the main page), and the 3-star count means little external validation. Apache licence and a claimed test count are positives; the conflict markers suggest weak review hygiene.

**Best fit.** A template for **how to wire vision + SUMO + QAOA together** — useful as architectural inspiration for a full-stack quantum traffic experiment.

**Limitations.** Unproven results, conflict-ridden README, no paper link, small team, no CI visible; quantum advantage claims (if any) are not benchmarked against a strong classical baseline.

**VERDICT: niche** — interesting full-pipeline sketch; verify everything before citing or extending.

## 3.5 `AsishMandoi/VRP-explorations` — QOSF mentorship vehicle-routing solvers

- **URL:** https://github.com/AsishMandoi/VRP-explorations
- **Stars:** 14 ★ · **Language:** Python · **Licence:** MIT · **Last commit:** August 2024 · **Maintainer:** individual researcher (QOSF mentorship project).

**What it implements.** A set of **quantum vehicle-routing solvers** developed under a Quantum Open Source Foundation mentorship: a **Route Activation** solver, a **GPS-based** solver, and a **DBSCAN-clustering** solver — three different decomposition strategies for VRP, each encoding subproblems as QUBOs for annealing, with **OR-Tools used as the classical baseline** for comparison.

**Hardware targets.** Hybrid: QUBO → D-Wave-style annealing, with classical OR-Tools baseline.

**Quality signals.** MIT licence, three documented solver variants, explicit classical baseline (rare and commendable in this space), but dormant since August 2024 and no tests/CI.

**Best fit.** Learning **how to decompose a VRP** (cluster-first vs route-activation) before committing to a quantum solver; a template for honest classical-vs-quantum comparison.

**Limitations.** Educational scale (small instances), not packaged, unmaintained since 2024.

**VERDICT: niche** — a good study reference for QUBO-based VRP decomposition.

## 3.6 `Mr-Jamatia/Quantum-Vehicle-Routing-Problems` — CVRP/CVRPTW with QUBO + D-Wave

- **URL:** https://github.com/Mr-Jamatia/Quantum-Vehicle-Routing-Problems
- **Stars:** 7 ★ · **Language:** Python · **Licence:** MIT · **Last commit:** June (recent year) · **Maintainer:** individual researcher.

**What it implements.** Documented solvers for **Capacitated VRP (CVRP)** and **CVRP with Time Windows (CVRPTW)**: QUBO formulations (capacity and time-window constraints as penalty terms) solved via **D-Wave Ocean**, with a described repository structure (formulation modules, solver modules, experiment scripts). Time windows are the feature most city logistics researchers actually need and most toy repos skip.

**Hardware targets.** Annealing (D-Wave); formulations exportable to gate-model solvers.

**Quality signals.** MIT licence, structured layout, documented problem variants; still small (7 stars), no visible CI.

**Best fit.** A starting codebase for **CVRPTW QUBO** experiments (last-mile delivery, municipal service routing).

**Limitations.** Small instances typical of student-scale work; no published benchmarks against OR-Tools; needs modernisation before production use.

**VERDICT: niche** — one of the few repos covering time windows; promising as a fork base.

## 3.7 `SMU-Quantum/adaptive_quantum_cvrp` — SAC-RL + augmented Lagrangian + QUBO/VQE CVRP (paper: arXiv:2509.15262)

- **URL:** https://github.com/SMU-Quantum/adaptive_quantum_cvrp
- **Stars:** 8 ★ · **Language:** Python · **Licence:** MIT · **Last commit:** 22 September (recent) · **Maintainer:** SMU (Southern Methodist University) Quantum group.

**What it implements.** A genuinely novel hybrid: **SAC reinforcement learning** decides how to decompose/adapt the CVRP instance, an **augmented Lagrangian method (ALM)** handles constraints, and the resulting subproblems are solved with **QUBO and VQE** quantum solvers — all described in the accompanying paper **arXiv:2509.15262**. This is "adaptive" in the literal sense: RL chooses the quantum workload rather than running one static formulation.

**Hardware targets.** Hybrid: QUBO (annealing-ready) and VQE (gate-model), behind an RL controller.

**Quality signals.** MIT, recent commits (22 September), paper-linked, university group. Still early (8 stars), no long track record.

**Best fit.** Researchers exploring **RL-guided quantum optimization** — a strong pattern for city dispatch problems where instance sizes vary wildly.

**Limitations.** Complex stack (RL + ALM + quantum) to reproduce; no mature docs yet; unproven at city scale.

**VERDICT: niche** — cutting-edge hybrid worth watching and citing; not yet a dependency.

## 3.8 `alejomonbar/Quantum-Supply-Chain-Manager` — QNN forecasting + VRP for supply chains

- **URL:** https://github.com/alejomonbar/Quantum-Supply-Chain-Manager
- **Stars:** 32 ★ · **Language:** Python (notebooks) · **Licence:** MIT · **Last commit:** July 2022 · **Maintainer:** individual researcher (quantum-ML educator with several public tutorials).

**What it implements.** A two-stage **quantum supply-chain manager**: a **quantum neural network** predicts demand/backorders from noisy supply-chain signals, and the prediction feeds a **vehicle-routing** optimization stage — i.e. QML (forecast) + QAOA/annealing-style optimization (dispatch) in one pipeline. That forecast→optimise pairing is exactly the architecture smart-city logistics needs (demand-aware waste collection, transit rescheduling).

**Hardware targets.** Hybrid: gate-model QNN (simulator-first) + routing optimizer.

**Quality signals.** MIT, 32 stars (decent for a demo), notebook-driven, but dormant since July 2022 — APIs will have drifted.

**Best fit.** A **conceptual blueprint** for combining quantum forecasting with quantum routing in municipal logistics.

**Limitations.** Notebook quality (limited tests/docs), stale dependencies, toy-scale data.

**VERDICT: niche** — strong idea, aging code; use as an architecture reference.

---

# CATEGORY 4 — QUANTUM ENERGY / GRID REPOSITORIES

## 4.1 `juanfrh7/uc-problem-annealing` — D-Wave unit commitment (University of Sydney)

- **URL:** https://github.com/juanfrh7/uc-problem-annealing
- **Stars:** 9 ★ · **Language:** Python · **Licence:** none · **Last commit:** September 2023 · **Maintainer:** academic researcher (University of Sydney lineage).

**What it implements.** **Unit Commitment (UC)** — deciding which generators to turn on over a horizon — formulated as a QUBO/Ising model and solved with **D-Wave quantum annealing** (Ocean): startup costs, min-up/min-down times and demand balance encoded as penalty terms. One of the earliest dedicated UC-on-annealer codebases.

**Hardware targets.** Annealing (D-Wave).

**Quality signals.** 9 stars, no licence, September 2023 — research code. No tests, no classical baseline visible.

**Best fit.** Seeing a **complete UC penalty construction** (the hard part of any UC paper) in working code.

**Limitations.** No licence, no scaling studies, no OR-Tools/CPLEX comparison, stale APIs.

**VERDICT: niche** — a formulation reference for UC-as-QUBO.

## 4.2 `ajliouat/quantumgrid` — PennyLane QAOA/VQE unit commitment vs MILP/OR-Tools

- **URL:** https://github.com/ajliouat/quantumgrid
- **Stars:** 4 ★ · **Language:** Python · **Licence:** README declares Apache-2.0 (GitHub's detector reports "not identifiable") · **Last commit:** 22 February (recent) · **Maintainer:** individual researcher.

**What it implements.** A **unit-commitment benchmark harness in PennyLane**: builds UC instances, solves them with **QAOA and VQE** (gate-model variational algorithms), and compares against **classical MILP (via OR-Tools)** on the same instances. Includes 130+ tests — an unusually high quality signal for this category — and a clear experimental structure (problem → quantum solver → classical baseline → metrics).

**Hardware targets.** Hybrid gate-model (PennyLane: local simulators, pluggable IBM/Braket via plugins) + classical MILP baseline.

**Quality signals.** **130+ tests**, Apache licence (per README), active commits (22 February), explicit classical baselines. The tiny star count reflects newness, not sloppiness — this is the best-engineered energy repo in the dossier.

**Best fit.** The **reference design for honest quantum-vs-classical UC experiments** — copy its baseline structure for your own grid studies.

**Limitations.** Still small-scale UC (not full security-constrained OPF); low visibility; licence metadata mismatch (README vs GitHub detector).

**VERDICT: useful** — the standout quantum-grid codebase for methodology and test discipline.

## 4.3 `dribes2/Stochastic-Unit-Commitment-Problem-with-Quantum-Annealing` — reproduces joint chance-constrained UC paper

- **URL:** https://github.com/dribes2/Stochastic-Unit-Commitment-Problem-with-Quantum-Annealing
- **Stars:** 1 ★ · **Language:** Python · **Licence:** none · **Last commit:** 4 May (recent year) · **Maintainer:** NTNU-affiliated researcher.

**What it implements.** Code **reproducing "Quantum Annealing for Joint Chance-Constrained Unit Commitment"** (NTNU-linked work): stochastic UC with **joint chance constraints** (probabilistic demand/reserve satisfaction) converted into QUBO form and solved by **quantum annealing** — the paper-companion pattern again, here for the stochastic variant that utilities actually care about.

**Hardware targets.** Annealing (D-Wave).

**Quality signals.** Single star, no licence — pure paper artifact. Value is 100% in the chance-constraint encoding.

**Best fit.** Reproducing the paper; learning how chance constraints get penalised into a QUBO.

**Limitations.** Essentially unreusable without contacting the author (no licence, no docs).

**VERDICT: niche** — a citable reproduction for stochastic UC, nothing more.

## 4.4 `MuyleangIng/quantum-gnn-rl-opf` — GNN + PPO with a PennyLane VQC actor for AC-OPF

- **URL:** https://github.com/MuyleangIng/quantum-gnn-rl-opf
- **Stars:** 2 ★ · **Language:** Python · **Licence:** none ("not specified") · **Last commit:** 10 March (recent) · **Maintainer:** individual researcher.

**What it implements.** A hybrid **deep-RL controller for AC optimal power flow**: a **graph neural network** encodes the grid topology, **PPO** trains a policy, and the policy's actor is a **PennyLane variational quantum circuit** — i.e. a quantum actor inside a classical RL loop. Evaluation environments come from **opfgym** and **SimBench** benchmark grids (realistic test-feeders rather than toy graphs).

**Hardware targets.** Hybrid gate-model (PennyLane VQC; simulator-first) + classical GNN/PPO.

**Quality signals.** Recent commits (10 March) and sensible ecosystem choices (opfgym/SimBench), but **2 stars, no licence, no tests** — pre-publication research code.

**Best fit.** Studying **quantum actors in grid-RL** — a novel direction if your interest is learning-based OPF rather than QUBO dispatch.

**Limitations.** No licence (cannot safely reuse), tiny community, heavy reproduction burden (GNN + RL + QML), unclear whether it beats a pure-classical actor.

**VERDICT: niche** — an interesting research prototype; wait for a licensed, documented release.

---

# CATEGORY 5 — QUANTUM MACHINE LEARNING (QML) REPOSITORIES

## 5.1 `mit-han-lab/torchquantum` — PyTorch-native quantum ML at scale

- **URL:** https://github.com/mit-han-lab/torchquantum
- **Stars:** 1.7k ★ · **Language:** Python · **Licence:** MIT · **Last commit:** July 2026 · **Maintainer:** MIT HAN Lab (Song Han's group).

**What it implements.** A **PyTorch-native** quantum-computing/ML library: quantum nodes/layers as `torch.nn.Module`s, parameter-shift and analytic gradients, large-batch simulation optimised for GPUs (the lab's speciality), **quantum ML tutorials** (MNIST classifiers, quantum reservoir-ish models), plus **quantum control** functionality (pulse/control-oriented workflows) and integration with `torch` optimizers/autograd. Distinct from PennyLane in being tensor-first and throughput-focused — designed for *training* many circuits fast.

**Hardware targets.** Gate-model simulation (GPU-accelerated); hardware export is secondary.

**Quality signals.** 1.7k stars, MIT, active (July 2026), HAN Lab credibility, tutorials and paper citations. One of the largest QML repos on GitHub.

**Best fit.** **Large-scale quantum-ML experiments** (batches of urban sensor data, image-like inputs) where PennyLane's per-node overhead hurts; deep integration with existing PyTorch models.

**Limitations.** Simulator-centric (hardware execution less turnkey than Qiskit); research-lab API churn; quantum-advantage claims still require careful baselines.

**VERDICT: essential** — the default choice for quantum ML inside PyTorch pipelines.

## 5.2 `tensorflow/quantum` — TensorFlow Quantum (TFQ)

- **URL:** https://github.com/tensorflow/quantum
- **Stars:** 2.2k ★ · **Language:** Python (plus C++/Swift ops) · **Licence:** Apache-2.0 · **Last commit:** badge "last Sunday" (active again) · **Maintainer:** Google (TensorFlow team + Quantum AI).

**What it implements.** **Hybrid quantum-classical ML on TensorFlow**: the `tfq.layers.PQC` (parameterised quantum circuit) and `ControlledPQC` layers, `tfq.get_expectation_op` for fast expectation evaluation, quantum kernel methods, quantum data loaders, and **error-mitigation utilities (e.g. zero-noise extrapolation)** — all compiled into TF graphs via a Cirq-based frontend for speed. The canonical "quantum layer inside a CNN" workflow comes from TFQ.

**Hardware targets.** Gate-model via Cirq (simulators first; Google hardware through Cirq integrations).

**Quality signals.** 2.2k stars, Apache, active commits (last Sunday), massive citation count, Google support. Ecosystem momentum is smaller than PyTorch's, but the library is maintained.

**Best fit.** Teams already invested in **TensorFlow/Keras** who want quantum layers/kernels without adopting a second autodiff framework.

**Limitations.** TF-ecosystem lock-in; slower community growth than PennyLane/torchquantum; hardware execution story thinner than Qiskit's.

**VERDICT: useful** — the reference TFQ stack; essential only if you are a TensorFlow shop.

## 5.3 `XanaduAI/qml-benchmarks` — quantum vs classical ML benchmark suite

- **URL:** https://github.com/XanaduAI/qml-benchmarks
- **Stars:** 82 ★ · **Language:** Python · **Licence:** Apache-2.0 · **Last commit:** August 2026 · **Maintainer:** Xanadu.

**What it implements.** A **benchmark suite comparing quantum and classical machine-learning models** on standard datasets: harnesses for training quantum models (kernel methods, variational classifiers) alongside classical baselines (SVM, neural nets, etc.), with consistent metrics and experiment configuration — the "does quantum ML actually help?" toolkit rather than another algorithm demo.

**Hardware targets.** Gate-model simulators (PennyLane/Xanadu stack) + classical baselines.

**Quality signals.** Apache, active (August 2026), Xanadu backing, methodology-first design. Small but purposeful.

**Best fit.** **Defensible baselines** for any quantum-ML claim about urban data — reviewers will ask for exactly this comparison.

**Limitations.** Datasets are generic (not city-specific); you must map your AQI/traffic data into its harness yourself; small instance catalogue.

**VERDICT: useful** — the right way to benchmark QML honestly; pair it with your own city datasets.

## 5.4 `rasidi3112/Quantum-Machine-Learning` — VQC vs QSVM benchmarks

- **URL:** https://github.com/rasidi3112/Quantum-Machine-Learning
- **Stars:** 139 ★ · **Language:** Python (notebooks) · **Licence:** MIT · **Last commit:** February (recent year) · **Maintainer:** individual researcher.

**What it implements.** Benchmark notebooks comparing a **Variational Quantum Classifier (VQC)** against **quantum support vector machines (QSVM/QSVC)** on classification tasks — the standard "which QML model wins on small data" study, with training curves and accuracy comparisons.

**Hardware targets.** Gate-model simulators (Qiskit-era code).

**Quality signals.** 139 stars (high for a benchmark notebook set), MIT, but notebook-only with February recency and no packaging/tests.

**Best fit.** Quick **VQC-vs-kernel comparisons** to orient yourself before writing your own harness (or use qml-benchmarks, 5.3, for a maintained version).

**Limitations.** No city datasets; dependency drift (older Qiskit APIs); not a library.

**VERDICT: niche** — handy teaching/benchmark notebooks, not infrastructure.

## 5.5 `merlinquantum/merlin` — hybrid quantum-classical ML library

- **URL:** https://github.com/merlinquantum/merlin
- **Stars:** 38 ★ · **Language:** Python · **Licence:** MIT · **Last commit:** September (recent) · **Maintainer:** Merlin Quantum (small open-source project).

**What it implements.** A **hybrid quantum-classical ML library**: building blocks for combining classical layers with quantum kernels/variational components under one API — a lighter-weight alternative to torchquantum/PennyLane aimed at quick hybrid-model experiments.

**Hardware targets.** Hybrid (simulator-based quantum components inside classical training loops).

**Quality signals.** MIT, recent commits (September), modest docs; 38 stars means limited external validation.

**Best fit.** Quick prototyping of **hybrid models** if you find PennyLane's API heavy.

**Limitations.** Small community, unclear long-term maintenance, thinner benchmark evidence than the big frameworks.

**VERDICT: niche** — a lightweight curiosity; prefer PennyLane or torchquantum for anything you must maintain.

## 5.6 `Wark12291/Quantum-AQI-Forecasting` — quantum air-quality forecasting attempt (empty repo)

- **URL:** https://github.com/Wark12291/Quantum-AQI-Forecasting
- **Stars:** 0 ★ · **Language:** not detected · **Licence:** none · **Last commit:** recent (repository exists, essentially empty) · **Maintainer:** unknown individual.

**What it implements.** From the name alone: an attempt at **quantum AQI (Air Quality Index) forecasting** — the exact smart-city use case you would want (quantum time-series/ML for pollution prediction). **However: there is no README** (raw README fetch returns 404), no visible code description, no licence, and zero stars.

**Hardware targets.** Unknown.

**Quality signals (negative).** No README, no licence, no documentation — this repo cannot be evaluated or reused as-is.

**Best fit.** Nothing, until the author publishes documentation. Mentioned here mainly as evidence that **quantum AQI forecasting code on GitHub is essentially non-existent** — a genuine gap in the field.

**Limitations.** Unusable in current state.

**VERDICT: avoid-stale** — an empty placeholder; treat "quantum AQI forecasting" as an open research gap rather than something you can download.

---

# CATEGORY 6 — QKD & QUANTUM NETWORK SECURITY REPOSITORIES

## 6.1 `QNLab-USTC/SimQN` — QKD network simulator (USTC)

- **URL:** https://github.com/QNLab-USTC/SimQN
- **Stars:** 1k ★ · **Language:** Python · **Licence:** GPL-3.0 · **Last commit:** badge "last Tuesday" (active) · **Maintainer:** Quantum Network Lab, University of Science and Technology of China (USTC).

**What it implements.** A **QKD-network simulator**: protocol models (BB84-family and entanglement-based QKD, measurement-device-independent variants), network/topology handling, key-generation rate estimation and resource-management policies for simulated quantum networks — built for the academic QKD-network community, with **25+ papers** cited as using it (per the project's own material).

**Hardware targets.** Simulator only (no hardware execution; models the physics layer statistically).

**Quality signals.** 1k stars (by far the most-starred QKD simulator here), GPL-3.0, **pytest + flake8 CI**, active commits (last Tuesday), academic lab with publication record. The healthiest repo in this category.

**Best fit.** Simulating **city-scale QKD networks** (backbone fiber QKD, metropolitan key distribution) and evaluating key-management policies before any hardware exists.

**Limitations.** GPL-3.0 (copyleft constraints on redistribution); QKD-specific (not a general quantum-network stack); documentation partially in Chinese.

**VERDICT: essential** — the default open QKD-network simulator.

## 6.2 `SoftwareQuTech/SimulaQron` — end-to-end quantum network simulator (QuTech)

- **URL:** https://github.com/SoftwareQuTech/SimulaQron
- **Stars:** 136 ★ · **Language:** Python · **Licence:** not identifiable by GitHub's detector (LICENSE file variants; check before redistribution) · **Last commit:** May (recent) · **Maintainer:** QuTech (TU Delft/TNO).

**What it implements.** An **end-to-end simulator of a quantum network**: simulates local quantum systems at multiple nodes connected by simulated quantum channels, lets you write **distributed quantum applications and QKD-style protocols** in a high-level API, and — as of v4.1.2 — supports modern backends including **NetQASM** (the QuTech stack) plus **Qiskit and Cirq** backends, with **Python 3.12** support. It simulates the *application layer* of a quantum internet rather than only key rates.

**Hardware targets.** Simulator (multi-node quantum network emulation; backend circuits via Qiskit/Cirq/NetQASM).

**Quality signals.** QuTech institutional backing, versioned releases (v4.1.2), backend flexibility, active May commits. Licence ambiguity (GitHub "not identifiable") is the main hygiene issue.

**Best fit.** **Distributed quantum protocols** between simulated city nodes (entanglement distribution, distributed sensing, quantum-secure channels) — broader than pure QKD.

**Limitations.** Licence must be verified from the LICENSE file; smaller community than SimQN; academic API style.

**VERDICT: useful** — the leading end-to-end quantum-network application simulator.

## 6.3 `sequence-toolbox/SeQUeNCe` — discrete-event quantum network simulator

- **URL:** https://github.com/sequence-toolbox/SeQUeNCe
- **Stars:** 185 ★ · **Language:** Python · **Licence:** not identifiable by GitHub's detector (permissive-style project; verify LICENSE) · **Last commit:** badge "today" · **Maintainer:** SeQUeNCe academic collaboration (peer-reviewed simulator paper with DOI).

**What it implements.** A **discrete-event quantum network simulator** structured in five clear modules — **hardware** (nodes, channels, photon sources/detectors), **entanglement** (generation/purification/distillation), **resource** management (entanglement routing, memory allocation), **network** layer, and **application** protocols (incl. QKD) — using **QuTiP** for physical simulation and **Stim** for fast stabilizer circuits. This modularity makes it the closest thing here to a *layered network stack* you would recognise from classical networking.

**Hardware targets.** Simulator (discrete-event; physics via QuTiP/Stim).

**Quality signals.** Very recent commits (badge "today"), modular architecture, published simulator paper (DOI), 185 stars. Licence metadata ambiguity again (GitHub detector failure).

**Best fit.** **Protocol-layer research** for metropolitan quantum networks: routing entanglement across a city topology, memory scheduling, QKD application flows.

**Limitations.** Steeper learning curve than SimQN; licence needs manual verification; physics fidelity depends on QuTiP models you configure.

**VERDICT: useful** — the best-architected quantum network simulator; ideal when you need routing/resource-management layers.

## 6.4 `tqsd/QuNetSim` — Python quantum network simulator (stale)

- **URL:** https://github.com/tqsd/QuNetSim
- **Stars:** 147 ★ · **Language:** Python · **Licence:** MIT · **Last commit:** June 2023 (~3 years stale) · **Maintainer:** TQSD research group.

**What it implements.** A Python simulator for **quantum network protocols**: hosts connected by simulated quantum links, QKD protocol implementations (BB84 and variants), entanglement-based protocols, and simple routing — designed for teaching and quick protocol experiments with an accessible API.

**Hardware targets.** Simulator only.

**Quality signals.** MIT and 147 stars (good legacy), but **no commits since June 2023** — dependencies and Python versions have moved on.

**Best fit.** Reading for API design ideas; running only if you pin old dependencies.

**Limitations.** Unmaintained ~3 years; superseded by SimQN/SeQUeNCe/SimulaQron.

**VERDICT: avoid-stale** — fine history, not a foundation for new work.

## 6.5 `QKDNetSim/qkdnetsim` — NS-3 module for QKD networks (C++, ETSI KMS)

- **URL:** https://github.com/QKDNetSim/qkdnetsim
- **Stars:** 36 ★ · **Language:** C++ (NS-3 module) · **Licence:** GPL-2.0 · **Last commit:** October (recent) · **Maintainer:** QKDNetSim academic project.

**What it implements.** A **QKD network simulator as an NS-3 module** — i.e. QKD layered onto the same discrete-event network simulator used for classical networking research: network/topology modeling, key-relay paths, and **ETSI-standard key management** (references **ETSI GS QKD 014** and **GS QKD 004** KMS interfaces). C++/NS-3 means it plugs into existing classical-network simulation scenarios — useful for co-simulating a city's classical control plane alongside QKD key delivery.

**Hardware targets.** Simulator only (NS-3 discrete-event; no gate/anneal execution).

**Quality signals.** Active (October), GPL-2.0, standards-aligned (ETSI), C++ engineering. Small community (36 stars).

**Best fit.** **QKD integrated with classical network simulation** — capacity planning for key-distribution services over an existing metro network model.

**Limitations.** C++/NS-3 learning curve; GPL-2.0; QKD-only scope; less Python-friendly than SimQN.

**VERDICT: niche** — the right tool specifically for NS-3/ETSI-oriented QKD planning.

## 6.6 `MadhavJivrajani/pyQKD` — basic QKD protocol implementations (stale)

- **URL:** https://github.com/MadhavJivrajani/pyQKD
- **Stars:** 17 ★ · **Language:** Python · **Licence:** MIT · **Last commit:** June 2020 (~6 years stale) · **Maintainer:** individual researcher.

**What it implements.** Small **QKD protocol implementations** (BB84-style key exchange with sifting/error estimation steps) in plain Python — a pedagogical codebase from the early wave of open QKD software.

**Hardware targets.** Simulator/toy execution only.

**Quality signals.** MIT, but last commit June 2020; no tests; pre-dates every modern QKD simulator above.

**Best fit.** A five-minute read to see BB84's classical post-processing steps in code.

**Limitations.** Six years stale, no security-proof rigor, superseded by SimQN (6.1).

**VERDICT: avoid-stale** — use SimQN instead.

---

# CATEGORY 7 — QUANTUM CITY / URBAN REPOSITORIES

## 7.1 `crs4/QuantumCodeChallengeHackathon` — smart-city quantum hackathon challenges (CRS4)

- **URL:** https://github.com/crs4/QuantumCodeChallengeHackathon
- **Stars:** 4 ★ · **Language:** Python (notebooks) · **Licence:** MIT · **Last commit:** November 2024 · **Maintainer:** CRS4 (Sardinian research centre, quantum computing group).

**What it implements.** A collection of **smart-city-themed quantum computing challenges** developed for hackathon events, executed on the **Qbraid** platform: challenge statements and starter/reference solutions around urban problems (routing, scheduling, resource allocation style tasks) designed to onboard newcomers to quantum optimization.

**Hardware targets.** Hybrid: Qbraid-hosted simulators/gate-model backends.

**Quality signals.** MIT, institutional source (CRS4 runs quantum workshops), but hackathon-scoped (4 stars, November 2024, notebooks not a library).

**Best fit.** **Teaching material** — ready-made urban-problem quantum exercises for a course or internal workshop.

**Limitations.** Not research-grade code; challenge solutions are introductory; limited depth.

**VERDICT: niche** — excellent pedagogy for smart-city quantum literacy, nothing to build production on.

## 7.2 `sunilgentyala/FedQSense` — quantum federated learning for smart-city sensing (GLOBECOM 2026)

- **URL:** https://github.com/sunilgentyala/FedQSense
- **Stars:** 5 ★ · **Language:** Python · **Licence:** MIT · **Last commit:** September (recent) · **Maintainer:** individual researcher (publication-linked).

**What it implements.** Code for **quantum federated learning applied to smart-city IoT sensing** (paper target: **IEEE GLOBECOM 2026**): distributed sensing nodes train a shared model without raw-data exchange, with **quantum components (PennyLane) and PyTorch** in the loop — addressing the privacy story (federated) and the quantum story (variational models) simultaneously. For city sensing (traffic cameras, AQI sensors, acoustic monitors), federated training is the architecturally correct answer, and this repo is one of the few that combines it with quantum ML.

**Hardware targets.** Hybrid gate-model (PennyLane simulators; hardware-portable) + PyTorch classical training.

**Quality signals.** MIT, recent commits (September), peer-review pipeline (GLOBECOM), sensible stack (PennyLane + PyTorch). Still 5 stars — early visibility.

**Best fit.** A template for **privacy-preserving quantum learning across distributed city sensors**.

**Limitations.** Early-stage (small stars, limited docs visibility); GLOBECOM-stage results; no city-scale dataset.

**VERDICT: niche** — a promising, publication-backed starting point for quantum federated city sensing.

## 7.3 `Yedman3585/Quantum-Sensor-Assignment` — compact QUBO for camera-to-edge-server assignment

- **URL:** https://github.com/Yedman3585/Quantum-Sensor-Assignment
- **Stars:** 5 ★ · **Language:** Python · **Licence:** MIT · **Last commit:** badge "yesterday" (actively developed) · **Maintainer:** individual researcher.

**What it implements.** A focused urban-infrastructure problem: **assigning cameras (sensors) to edge servers** under capacity/topology constraints, solved via **Lagrangian decomposition** (splitting the big assignment into subproblems) with each subproblem compiled into a **compact QUBO** — then solved three ways: **OpenJij**, **neal** (classical simulated annealing), and **MILP** (classical exact/heuristic). "Compact QUBO" is the key engineering contribution: dense penalties inflate qubit counts, and this repo explicitly attacks that.

**Hardware targets.** Hybrid: QUBO → annealing (OpenJij/neal, D-Wave-compatible) + MILP baseline; gate-model users can import the QUBO into Qiskit.

**Quality signals.** MIT, **commit "yesterday"** (the most actively developed repo in Category 7), clean problem statement, three-solver comparison including a MILP baseline — methodologically sound despite the small star count.

**Best fit.** **Edge-compute resource allocation** for city sensor fleets (cameras, environmental monitors) — and as a template for Lagrangian-decomposed, compact-QUBO formulations of other assignment problems.

**Limitations.** Single problem class; small-scale instances; young project (5 stars).

**VERDICT: niche** — actively maintained and methodologically exemplary for its size; a strong fork base for sensor-assignment work.

---

# ALSO NOTED (secondary repositories found during searches)

Short-form entries — candidates you may want to open directly:

| Repository | Stars | Note |
|---|---|---|
| `BrennanLagasse/Quantum-Vehicle-Routing` | 3★ | another small QUBO VRP demo |
| `BrunoRosendo/vrp-quantum-solver` | 5★ | VRP quantum solver experiment |
| `cotaylor/qkdsim` | 20★ | lightweight QKD simulator (Python) |
| `QUT-CIQC/qkd` | 15★ | QUT quantum cryptography research code |
| `PreetiPandey74/pyqkd` | 5★ | second, separate "pyqkd" (distinct from 6.6) |
| `albertnieto/qcml` | 7★ | quantum ML collection |
| `gurolsaglam/Quantum-NN` | 6★ | quantum neural net demo (same author as 3.3) |
| `TheBinitGhimire/QuantumHack` | 6★ | PHP-based quantum hackathon site (non-Python) |
| `nakuljoshidev-coder/qkd-smart-city` | 1★ | explicitly "QKD + smart city" student project |
| `SERLABUniba/SCQaas_IoT` | 0★ | smart-city quantum-as-a-service IoT (SERLAB, Univ. Bari) |
| `kitamuyu/pyqubo-tutorial` | 1★ | official-ish PyQUBO tutorial book |

**Negative results worth recording:** no repository named or functioning as an IBM **"QOptLib"** benchmark suite exists (the real benchmark library is ZIB's **QOBLIB**, 2.5); no substantial "quantum digital-twin city" repository was found; "quantum AQI forecasting" (5.6) is an empty gap; searches for `quantum energy grid optimization` beyond Category 4 returned mostly zero-star hackathon projects.

---

# CROSS-CUTTING OBSERVATIONS

1. **The stack is bifurcated.** Gate-model work (QAOA, VQE, QML) lives in Qiskit/PennyLane/Cirq land; annealing work (nearly all traffic and energy QUBOs) lives in D-Wave Ocean. Most smart-city papers pick one side; the few genuinely interesting repos (`adaptive_quantum_cvrp`, `quantumgrid`, `Quantum-Sensor-Assignment`) deliberately bridge both with classical baselines.

2. **Classical baselines are rare and therefore valuable.** Only a handful of city repos compare against OR-Tools/MILP (`VRP-explorations`, `quantumgrid`, `Quantum-Sensor-Assignment`, `dribes2`'s classical comparison). Any paper you write should follow their lead — reviewers in transportation and power systems will demand it.

3. **Star counts lie about importance.** `qiskit-optimization` (285★) powers most QUBO applications yet is dwarfed by frameworks; conversely some 100★+ repos are tutorial notebooks. Judge by maintenance (badge last-commit), licence, tests and paper linkage — all listed per entry above.

4. **Licence hygiene is weak in Categories 3–4.** Several traffic/energy repos have **no licence at all** (`traffic_signals_qubo`, `traffic-routes-qc`, `TrafficFlowOptimization`, `uc-problem-annealing`, `dribes2`, `quantum-gnn-rl-opf`) — legally you cannot reuse them without permission. Prefer MIT/Apache forks for real work.

5. **Support status matters more than stars.** IBM has withdrawn official support from **qiskit-optimization** (successor: `qiskit-addon-opt-mapper`) while **qiskit-machine-learning** is co-maintained with the Hartree Centre. Budget for migration in long-lived projects.

6. **The genuinely "city" layer is thin.** Category 7 contains only three real projects (hackathon teaching, federated sensing, sensor assignment), all ≤5★ — while Categories 3–4 (traffic/energy) are paper companions at 1–14★. **There is no mature, general-purpose "quantum smart-city platform" on GitHub.** If your project needs one, you are building it — but the component libraries (Categories 1–2) are mature enough to build on.

7. **QKD simulation is the most mature niche.** SimQN (1k★, CI, active) and SeQUeNCe/SimulaQron give you a full toolkit for metropolitan quantum-network studies — far ahead of the quantum-optimization city applications in engineering quality.

---

# MASTER SUMMARY TABLE

| # | Repository | Stars | Language | Target | Verdict |
|---|---|---|---|---|---|
| 1.1 | qiskit/qiskit | ~8k | Python | gate | essential |
| 1.2 | qiskit-community/qiskit-optimization | 285 | Python | gate/anneal (QUBO) | useful (IBM support withdrawn) |
| 1.3 | qiskit-community/qiskit-machine-learning | 1.1k | Python | gate | essential |
| 1.4 | qiskit-community/qiskit-nature | 399 | Python | gate | niche (for smart cities) |
| 1.5 | quantumlib/Cirq | 5.1k | Python | gate | essential |
| 1.6 | PennyLaneAI/pennylane | 3.5k | Python | hybrid/gate | essential |
| 1.7 | ProjectQ-Framework/ProjectQ | 976 | Python | gate | avoid-stale |
| 1.8 | amazon-braket/amazon-braket-sdk-python | 373 | Python | hybrid/gate (cloud) | useful |
| 1.9 | dwavesystems/dwave-ocean-sdk | 545 | Python | anneal | essential |
| 1.10a | dwavesystems/dimod | 142 | Python | anneal | useful |
| 1.10b | dwavesystems/dwave-system | 99 | Python | anneal | useful |
| 1.10c | dwavesystems/dwave-neal | 64 | Python | anneal (classical SA) | avoid-stale (deprecated) |
| 1.10d | dwavesystems/dwave-samplers | 21 | Python | anneal (classical SA) | useful |
| 1.11 | pasqal-io/Pulser | 257 | Python | gate (neutral-atom) | useful |
| 2.1 | entropicalabs/openqaoa | 143 | Python | hybrid/gate (QAOA) | useful |
| 2.2 | OpenQuantumComputing/QAOA | 69 | Python | gate (QAOA) | niche |
| 2.3 | QAOAKit/QAOAKit | 54 | Python | gate (QAOA) | avoid-stale |
| 2.4 | qiskit-community/qopt-best-practices | 50 | Python | gate (QAOA on HW) | useful |
| 2.5 | ZIB-AOPT/QOBLIB | 60 | Python | solver-agnostic benchmarks | useful |
| 2.6 | Jij-Inc/OpenJij | 141 | Python | anneal (SQA/GPU) | useful |
| 2.7 | recruit-communications/pyqubo | 201 | Python | anneal (QUBO DSL) | useful |
| 2.8 | fixstars/amplify-benchmark | 11 | Python | hybrid (commercial annealer) | niche |
| 3.1 | mbinjavaid/traffic_signals_qubo | 8 | Python | anneal | niche (paper companion) |
| 3.2 | mbinjavaid/traffic-routes-qc | 4 | Python | anneal | avoid-stale |
| 3.3 | gurolsaglam/TrafficFlowOptimization | 4 | Python | anneal | avoid-stale (archived) |
| 3.4 | CybroatriX/…Adaptive-Urban-Traffic (FlowQ) | 3 | Python | gate (QAOA) + YOLOv8/SUMO | niche |
| 3.5 | AsishMandoi/VRP-explorations | 14 | Python | anneal (QUBO VRP) | niche |
| 3.6 | Mr-Jamatia/Quantum-Vehicle-Routing-Problems | 7 | Python | anneal (CVRPTW) | niche |
| 3.7 | SMU-Quantum/adaptive_quantum_cvrp | 8 | Python | hybrid (RL+QUBO/VQE) | niche |
| 3.8 | alejomonbar/Quantum-Supply-Chain-Manager | 32 | Python | hybrid (QNN+VRP) | niche |
| 4.1 | juanfrh7/uc-problem-annealing | 9 | Python | anneal (UC) | niche |
| 4.2 | ajliouat/quantumgrid | 4 | Python | hybrid gate (QAOA/VQE vs MILP) | useful |
| 4.3 | dribes2/…Quantum-Annealing (stochastic UC) | 1 | Python | anneal (chance-UC) | niche |
| 4.4 | MuyleangIng/quantum-gnn-rl-opf | 2 | Python | hybrid gate (VQC actor) | niche |
| 5.1 | mit-han-lab/torchquantum | 1.7k | Python | gate (sim/PyTorch) | essential |
| 5.2 | tensorflow/quantum | 2.2k | Python | gate (Cirq/TF) | useful |
| 5.3 | XanaduAI/qml-benchmarks | 82 | Python | gate (benchmarks) | useful |
| 5.4 | rasidi3112/Quantum-Machine-Learning | 139 | Python | gate (VQC vs QSVM) | niche |
| 5.5 | merlinquantum/merlin | 38 | Python | hybrid | niche |
| 5.6 | Wark12291/Quantum-AQI-Forecasting | 0 | — | unknown | avoid-stale (empty) |
| 6.1 | QNLab-USTC/SimQN | 1k | Python | simulator (QKD) | essential |
| 6.2 | SoftwareQuTech/SimulaQron | 136 | Python | simulator (QKD/network) | useful |
| 6.3 | sequence-toolbox/SeQUeNCe | 185 | Python | simulator (QKD/network) | useful |
| 6.4 | tqsd/QuNetSim | 147 | Python | simulator (QKD) | avoid-stale |
| 6.5 | QKDNetSim/qkdnetsim | 36 | C++ | simulator (QKD/NS-3, ETSI) | niche |
| 6.6 | MadhavJivrajani/pyQKD | 17 | Python | simulator (QKD) | avoid-stale |
| 7.1 | crs4/QuantumCodeChallengeHackathon | 4 | Python | gate (teaching/Qbraid) | niche |
| 7.2 | sunilgentyala/FedQSense | 5 | Python | hybrid gate (federated QML) | niche |
| 7.3 | Yedman3585/Quantum-Sensor-Assignment | 5 | Python | anneal (QUBO+MILP) | niche |

**Tally:** 49 repositories in the table (plus 11 secondary repos noted in the short list) — 7 categories covered, exceeding the 25-repository requirement.

**Top picks by use case:**

- *Start any city QUBO:* `dwave-ocean-sdk` + `qiskit-optimization` (+ `pyqubo` for readable formulations)
- *Start any city QML:* `pennylane` (or `torchquantum` if PyTorch-centric) + `qml-benchmarks` for baselines
- *Traffic signal/routing research:* `traffic_signals_qubo` (formulation) → `openqaoa`/`qopt-best-practices` (execution) → `VRP-explorations`/`adaptive_quantum_cvrp` (VRP patterns)
- *Grid/energy research:* `quantumgrid` (methodology + tests) → `uc-problem-annealing` (penalty construction) → `quantum-gnn-rl-opf` (learning-based OPF)
- *QKD/quantum networks:* `SimQN` (rates/policies) + `SeQUeNCe` (protocol/routing layers) + `qkdnetsim` (NS-3/ETSI planning)
- *Benchmarks for publication:* `ZIB-AOPT/QOBLIB` (optimization) + `qml-benchmarks` (ML) + classical OR-Tools/MILP baselines everywhere
