# GITHUB REPOS FOR SMART CITY RESEARCH — MASTER INDEX
### Consolidated from 5 deep research dossiers (~47,700 words, ~267 repo entries, Nov 2026)

**Full dossiers in this folder:**
1. `github-repos-smart-city-frameworks.md` (11,966 w — 57 repos: platforms, IoT, digital twins, edge, blockchain, city data)
2. `github-repos-quantum.md` (9,996 w — 60 repos: Qiskit/D-Wave/PennyLane, QAOA/UBO toolkits, city QAOA, QML, QKD)
3. `github-repos-aiml-traffic-energy.md` (9,511 w — 54 repos: traffic forecasting, ride-hailing, energy ML, air quality)
4. `github-repos-rl.md` (9,960 w — 64 repos: TSC-RL, driving, building energy RL, networks, MARL/offline/safe RL)
5. `github-repos-vision-llm-datasets.md` (6,287 w — 43 repos: environment/vision/LLM-city/federated/simulators+datasets)

---

## TOP 40 ESSENTIAL REPOS (start here)

### Simulators & Environments (the foundation of city research)
| Repo | ~Stars | What | Dossier |
|---|---|---|---|
| [eclipse-sumo/sumo](https://github.com/eclipse-sumo/sumo) | 4,261 | Microscopic traffic sim (TraCI) — TSC/AV standard | RL |
| [cityflow-project/CityFlow](https://github.com/cityflow-project/CityFlow) | 1,031 | >20× faster city-wide traffic sim (CoLight/MPLight benchmark) | RL |
| [carla-simulator/carla](https://github.com/carla-simulator/carla) | 14,572 | Autonomous driving city simulator | RL |
| [LucasAlegre/sumo-rl](https://github.com/LucasAlegre/sumo-rl) | 1,101 | Gym traffic-signal RL environments | RL |
| [Pi-Star-Lab/RESCO](https://github.com/Pi-Star-Lab/RESCO) | 189 | TSC RL benchmark (40+ intersections) | RL |
| [citylearn-project/CityLearn](https://github.com/citylearn-project/CityLearn) | ~650 | Building energy DR/RL Gym environment (MIT, v3) | AIML/RL |
| [ugr-sail/sinergym](https://github.com/ugr-savel/sinergym) → `ugr-sail/sinergym` | 241 | EnergyPlus Gym wrapper for RL HVAC | RL |
| [NatLabRockies/EnergyPlus](https://github.com/NREL/EnergyPlus) | 1,614 | Building energy simulator (NREL) | RL |
| [metadriverse/metadrive](https://github.com/metadriverse/metadrive) | 1,274 | Fast generalizable driving benchmark | RL |
| [Farama-Foundation/HighwayEnv](https://github.com/Farama-Foundation/HighwayEnv) | 3,341 | Tactical driving RL | RL |
| [mesa/mesa](https://github.com/projectmesa/mesa) | ~3,900 | Agent-based urban simulation | Vision/Datasets |
| [gboeing/osmnx](https://github.com/gboeing/osmnx) | ~5,870 | OSM street-network download/analysis | AIML/Datasets |
| [ns3-gym](https://github.com/tkn-tub/ns3-gym) | 698 | Network sim ↔ RL binding | RL |

### Traffic & Mobility ML
| Repo | ~Stars | What |
|---|---|---|
| [Bigscity/LibCity](https://github.com/Bigscity/LibCity) | ~1,167 | **74 models, 9 tasks, 52 datasets** — the traffic prediction library (pin deps) |
| [benedekrozemberczki/pytorch_geometric_temporal](https://github.com/benedekrozemberczki/pytorch_geometric_temporal) | ~3,000 | 30+ STGNNs (DCRNN→GMAN→MTGNN), best-documented |
| [TorchSpatiotemporal/tsl](https://github.com/TorchSpatiotemporal/tsl) | ~388 | Most current ST library + LargeST loader |
| [liyaguang/DCRNN](https://github.com/liyaguang/DCRNN) | research | Official DCRNN + METR-LA/PeMS-BAY datasets (TF1, stale code) |
| [liuxu77/LargeST](https://github.com/liuxu77/LargeST) | 299 | 8,600-sensor benchmark (⚠ CC BY-NC) |
| [StanfordASL/Trajectron-plus-plus](https://github.com/StanfordASL/Trajectron-plus-plus) | ~833 | Multi-agent trajectory forecasting |

### Energy ML
| Repo | ~Stars | What |
|---|---|---|
| [Nixtla/neuralforecast](https://github.com/Nixtla/neuralforecast) | ~4,174 | 30+ forecasting models (NBEATS/PatchTST/TFT) for load |
| [google-research/timesfm](https://github.com/google-research/timesfm) | ~35,258 | TimesFM foundation model (⚠ v3 weights non-commercial) |
| [OpenSTEF/openstef](https://github.com/OpenSTEF/openstef) | ~180 | Production probabilistic load/gen pipelines (MPL-2, Docker) |
| [buds-lab/building-data-genome-project-2](https://github.com/buds-lab/building-data-genome-project-2) | ~274 | BDG2: 3,053 building meters dataset |
| [IntelligentSystemsLab/ST-EVCDP](https://github.com/IntelligentSystemsLab/ST-EVCDP) | 266 | Shenzhen EV-charging datasets + PAG model (MIT) |

### Quantum
| Repo | ~Stars | What |
|---|---|---|
| [qiskit/qiskit](https://github.com/qiskit/qiskit) | ~8k | De-facto gate-model SDK (+ qiskit-optimization for city QUBO) |
| [qiskit-community/qiskit-machine-learning](https://github.com/qiskit-community/qiskit-machine-learning) | 1.1k | QSVM/VQC/QLSTM reference |
| [quantumlib/Cirq](https://github.com/quantumlib/Cirq) | 5.1k | Google gate-model SDK |
| [PennyLaneAI/pennylane](https://github.com/PennyLaneAI/pennylane) | 3.5k | Hybrid quantum ML default |
| [dwavesystems/dwave-ocean-sdk](https://github.com/dwavesystems/dwave-ocean-sdk) | 545 | Annealing reference (traffic/OPF QUBOs) |
| [mit-han-lab/torchquantum](https://github.com/mit-han-lab/torchquantum) | 1.7k | Quantum in PyTorch pipelines |
| [QNLab-USTC/SimQN](https://github.com/QNLab-USTC/SimQN) | 1k | Default open QKD-network simulator |
| [QOptLib](https://github.com/qiskit-community/optimization-benchmarks) (search "QOptLib") | — | IBM quantum optimization benchmarks (vs Gurobi) |

⚠ **Gap found:** quantum AQI/city-prediction code on GitHub is essentially **non-existent** — a genuine research opportunity.

### IoT / Platforms / Digital Twins
| Repo | ~Stars | What |
|---|---|---|
| [thingsboard/thingsboard](https://github.com/thingsboard/thingsboard) | 22,644 | Most complete open-core city IoT platform |
| [emqx/emqx](https://github.com/emqx/emqx) | 16,856 | MQTT/CoAP/LwM2M broker perf reference (⚠ BSL license) |
| [eclipse-mosquitto/mosquitto](https://github.com/eclipse-mosquitto/mosquitto) | ~11,300 | Lightweight MQTT default for pilots |
| [node-red/node-red](https://github.com/node-red/node-red) | 23,783 | Low-code IoT integration glue |
| [chirpstack/chirpstack](https://github.com/chirpstack/chirpstack) | 1,123 | LoRaWAN network server (city deployments) |
| [CesiumGS/cesium](https://github.com/CesiumGS/cesium) | 15,911 | 3D geospatial viewer — twin rendering |
| [CesiumGS/3d-tiles](https://github.com/CesiumGS/3d-tiles) | 2,629 | 3D content streaming standard |
| [eclipse-ditto/ditto](https://github.com/eclipse-ditto/ditto) | 941 | IoT digital-twin framework |
| [3dcitydb/3dcitydb](https://github.com/3dcitydb/3dcitydb) | 469 | CityGML 3D city database |
| [UDST/urbansim](https://github.com/UDST/urbansim) | 557 | Land-use microsimulation |
| [ckan/ckan](https://github.com/ckan/ckan) | ~5,150 | Reference city open-data portal |
| [smart-data-models/data-models](https://github.com/smart-data-models/data-models) | 143 | NGSI-LD semantic city schemas (interoperability vocabulary) |
| [kubeedge/kubeedge](https://github.com/kubeedge/kubeedge) | 7,612 | CNCF edge orchestration for city testbeds |
| [mkturkcan/valdrada](https://github.com/mkturkcan/valdrada) | ~253 | NYC city-scale digital twin (2026, fast-moving) |
| [openaq/openaq-python](https://github.com/openaq/openaq-python) | — | Air-quality data infrastructure |

### LLM / Foundation Models for Cities
| Repo | ~Stars | What |
|---|---|---|
| [tsinghua-fib-lab/CityGPT](https://github.com/tsinghua-fib-lab/CityGPT) | research | CityGPT + CityEval (KDD'25) |
| [HKUDS/UrbanGPT](https://github.com/HKUDS/UrbanGPT) | 460 | Spatio-temporal LLM for cities |
| [usail-hkust/LLMTSCS](https://github.com/usail-hkust/LLMTSCS) | 295 | LLM for traffic signal control (KDD'25) |
| [ChenDelong1999/RemoteCLIP](https://github.com/ChenDelong1999/RemoteCLIP) | research | Remote-sensing foundation model |
| [opengeos/segment-geospatial](https://github.com/opengeos/segment-geospatial) (SAMgeo) | high | SAM for geospatial/urban segmentation |

### Public Safety / Vision
| Repo | ~Stars | What |
|---|---|---|
| [google-research/flood-forecasting](https://github.com/google-research/flood-forecasting) | research | Google Flood LSTM pipeline (100M alerts) |
| [shaoshengsong/DeepSORT](https://github.com/shaoshengsong/DeepSORT) | 1,008 | Multi-object tracking for city video |
| [szad670401/HyperLPR](https://github.com/szad670401/HyperLPR) | 6,271 | License-plate recognition (CN) |
| [nutonomy/nuscenes-devkit](https://github.com/nutonomy/nuscenes-devkit) | ~2,800 | Autonomous driving dataset toolkit |
| [waymo-research/waymo-open-dataset](https://github.com/waymo-research/waymo-open-dataset) | research | Waymo dataset (research license) |

### Federated / Edge / TinyML
| Repo | ~Stars | What |
|---|---|---|
| [adap/flower](https://github.com/adap/flower) | ~6,922 | Federated learning framework default |
| [FedML-AI/FedML](https://github.com/FedML-AI/FedML) | ~4,100 | Research FL platform |
| [mit-han-lab/mcunet](https://github.com/mit-han-lab/mcunet) | 718 | TinyML on MCU |
| [tensorflow/tflite-micro](https://github.com/tensorflow/tflite-micro) | high | Edge inference runtime |

### RL Core Stack (used by all city RL papers)
| Repo | ~Stars | What |
|---|---|---|
| [ray-project/ray](https://github.com/ray-project/ray) | 44,222 | RLlib distributed training |
| [DLR-RM/stable-baselines3](https://github.com/DLR-RM/stable-baselines3) | 13,974 | Standard RL algorithms |
| [Farama-Foundation/Gymnasium](https://github.com/Farama-Foundation/Gymnasium) | 12,788 | RL environment API |
| [Farama-Foundation/PettingZoo](https://github.com/Farama-Foundation/PettingZoo) | 3,553 | MARL API |
| [takuseno/d3rlpy](https://github.com/takuseno/d3rlpy) | 1,688 | Offline RL (city offline-TSC) |
| [Farama-Foundation/Minari](https://github.com/Farama-Foundation/Minari) | 1,771 | Offline RL datasets |
| [PKU-Alignment/safety-gymnasium](https://github.com/PKU-Alignment/safety-gymnasium) | 600 | Safe RL benchmark (CMDP) |

### Official Paper Code (traffic-signal RL archive)
- **[traffic-signal-control/sample-code](https://github.com/traffic-signal-control/sample-code)** — official MPLight/CoLight/PressLight/FRAP code (authoritative archive)
- **[traffic-signal-control/RL_signals](https://github.com/traffic-signal-control/RL_signals)** — TSC datasets/archive (code stale, data authoritative)

---

## REPO-TO-PAPER MAP (which repo implements which paper)

| Paper | Repo |
|---|---|
| DCRNN (Li 2018) | liyaguang/DCRNN (stale TF1) |
| Graph WaveNet / ASTGCN / GMAN / MTGNN | reimplemented in pytorch_geometric_temporal, LibCity, tsl |
| CoLight/PressLight/MPLight/FRAP | traffic-signal-control/sample-code (archive) |
| IntelliLight | lucifer1004/IntelliLight (verify in RL dossier) |
| CityFlow benchmark (Zhang 2019) | cityflow-project/CityFlow |
| LibCity (Yu 2021) | Bigscity/LibCity |
| CityLearn challenges | citylearn-project/CityLearn |
| Google flood (Nevo 2022) | google-research/flood-forecasting |
| LargeST (Liu 2023) | liuxu77/LargeST |
| BDG2 building data | buds-lab/building-data-genome-project-2 |
| UrbanLLaVA / CityGPT / PlanGPT | see vision-LLM dossier (CityGPT + UrbanGPT confirmed) |

---

## VERDICT STATISTICS (from dossiers)

| Dossier | ESSENTIAL | USEFUL | NICHE | STALE |
|---|---|---|---|---|
| RL (64 repos) | 21 | 27 | 6 | 10 |
| AI/ML traffic-energy (54) | 13+ | many | — | TF1-era flagged |
| Quantum (60) | 7 core SDKs + simulators | many | city-specific mostly niche | few |
| Frameworks (57) | ~20 | many | O-RAN niche | OpenAQ code stale |
| Vision/LLM/Datasets (43) | ~22 | — | — | DeepCrime repo absent |

## KEY FINDINGS & GAPS

1. **Traffic prediction is the best-served domain** — LibCity + pytorch_geometric_temporal + tsl give mature multi-model stacks.
2. **TSC-RL official code is archival** (sample-code repo) — the field now runs on RESCO/sumo-rl/CityFlow instead.
3. **Quantum city code is a desert**: core SDKs are essential, but *application* repos (traffic QUBO, AQI QML) barely exist → **research opportunity**.
4. **License traps:** LargeST (CC BY-NC), TimesFM 3.0 (non-commercial), EMQX (BSL), STAEformer (unlicensed) — check before productization.
5. **Stale-but-authoritative:** DCRNN/GMAN/STGCN originals are TF1-era — use re-implementations in LibCity/tsl/pytorch_geometric_temporal.
6. **LLM-city repos are new and fast-moving** (CityGPT, UrbanGPT, LLMTSCS, Valdrada) — expect rapid change.

*Index compiled Nov 2026 from 5 multi-agent research dossiers. Star counts are snapshots and drift over time.*
