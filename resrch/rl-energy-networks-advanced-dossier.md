# Deep Technical Dossier: Reinforcement Learning for Smart City Systems

## Building Energy, Microgrid/EV/DR, Networks/IoT, Water/Waste, and Advanced RL Paradigms

---

# 1. Introduction

Smart cities concentrate heterogeneous cyber-physical subsystems—buildings, distribution grids, electric vehicle (EV) fleets, radio access networks, water distribution, and waste logistics—each of which must be operated sequentially under uncertainty, partial observability, and hard constraints. Reinforcement learning (RL) and deep reinforcement learning (DRL) have emerged as a unifying decision-making formalism for these problems because they (i) require no differentiable or explicitly calibrated plant model, (ii) optimize long-horizon discounted or average return rather than myopic cost, and (iii) can express safety, comfort, fairness, and equity through reward shaping or constrained Markov decision processes (CMDPs).

This dossier synthesizes technical results across five domains:

- **Section A — Building Energy RL:** HVAC setpoint control, multi-zone coordination, radiant systems, data-center cooling, and sensor-driven comfort optimization.
- **Section B — Microgrid, EV, and Demand Response RL:** economic dispatch, battery degradation-aware control, V2G, and constrained safe RL.
- **Section C — Networks and IoT RL:** RAN slicing, edge offloading, multi-UAV data harvesting, and fairness-aware scheduling.
- **Section D — Water, Waste, and Other Urban Systems:** pump scheduling, pressure control, waste routing, and elevator dispatch.
- **Section E — Advanced Paradigms:** multi-agent RL (MARL), safe RL, offline RL, LLM+RL, and sim-to-real transfer.

For each representative paper we report: **(a)** the MDP formulation, **(b)** the algorithm or architecture, **(c)** the environment or simulator and scale, **(d)** baselines, **(e)** quantitative results with exact numbers where available, and **(f)** limitations. Common notations used throughout:

| Symbol | Meaning |
|---|---|
| $s_t \in \mathcal{S}$ | state at time $t$ |
| $a_t \in \mathcal{A}$ | action |
| $r_t \in \mathbb{R}$ | scalar reward |
| $P(s'|s,a)$ | transition kernel |
| $\gamma \in [0,1)$ | discount factor |
| $\pi(a|s)$ | stochastic policy |
| $\mu(s)$ | deterministic policy |
| $Q^\pi(s,a)$ | action-value function |
| $V^\pi(s)$ | state-value function |
| $J(\pi) = \mathbb{E}_\pi[\sum_t \gamma^t r_t]$ | expected discounted return |

Standard Bellman optimality equation:

$$
Q^*(s,a) = r(s,a) + \gamma \sum_{s'} P(s'|s,a) \max_{a'} Q^*(s',a').
$$

---

# Section A: Building Energy Reinforcement Learning

Buildings account for roughly 40% of global energy use, and HVAC constitutes 40–50% of commercial building electricity. The control problem is high-dimensional, partially observed (occupancy, weather, prices), multi-objective (cost vs. comfort), and often continuous-action. The following papers span deep deterministic policy gradients (DDPG), soft actor-critic (SAC), multi-agent formulations, and Bayesian/generative hybrids.

## A.1 Wei et al., DAC 2017 — Deep RL for Joint HVAC Load Control in Mixed-Use Buildings

**Citation:** T. Wei, Y. Wang, Q. Zhu, "Deep Reinforcement Learning for Building HVAC Control," *ACM Design Automation Conference (DAC)*, 2017, doi:10.1145/3061639.3062224.

**(a) MDP formulation.** The building is modeled as a discrete-time dynamical system with thermal state $x_t$ (zone temperatures), ambient disturbance $w_t$ (outdoor temperature, solar, occupancy heat), and price signal $c_t$. The agent selects HVAC power/setpoint commands $a_t$. The state is $s_t = [x_t; w_t; c_t]$ (and optionally history for partial observability). Reward balances energy cost and comfort deviation:

$$
r_t = -\,c_t^\top a_t \;-\; \lambda \sum_{i} \big[ (T_{i,t}-T_i^{\mathrm{set}})^2 \big],
$$

or a constrained form with comfort band $\underline{T}_i \le T_{i,t} \le \overline{T}_i$.

**(b) Algorithm/architecture.** Deep deterministic policy gradient (DDPG) with actor-critic networks: actor $\mu(s|\theta^\mu)$ maps continuous thermal/price states to HVAC power; critic $Q(s,a|\theta^Q)$ estimates cost-to-go. Target networks with soft updates $\theta' \leftarrow \tau\theta + (1-\tau)\theta'$ stabilize training. Experience replay stores $(s,a,r,s')$ transitions.

**(c) Environment/simulator.** Custom building thermal model (RC-network / equivalent) coupled with EnergyPlus-like load traces; multi-zone mixed-use building (office + residential). Scale: tens of zones, hourly or 5-minute control steps.

**(d) Baselines.** Rule-based thermostat control, MPC with calibrated model, PID, and (in related follow-ups) DQN.

**(e) Quantitative results.** Reported energy cost reductions on the order of **~20% versus rule-based control** while maintaining comfort, with reduced peak demand under time-of-use pricing. (Exact percentages vary by building configuration and price signal; the DAC paper established the DDPG-for-HVAC template later cited by Applied Energy and IoT-J work.)

**(f) Limitations.** Single-building simulation; comfort penalty weight $\lambda$ requires tuning; no formal safety guarantee on temperature violations during exploration; transfer to other buildings not demonstrated in the original paper.

## A.2 Zhang, Energy and Buildings 2019 — BEM-DRL Hybrid for Radiant Heating

**Citation:** Z. Zhang, A. Chong, Y. Pan, C. Song, K.P. Lam, "Whole building energy model for HVAC optimal control: A practical framework based on deep reinforcement learning," *Energy and Buildings*, vol. 199, pp. 1–16, 2019 (and related BEM-DRL radiant-heating work, doi:10.1016/j.enbuild.2018.09.x / S0378778818330858).

**(a) MDP formulation.** State includes zone air temperature, radiant surface temperature, supply water temperature, outdoor weather, occupancy, and price. Actions are heating water temperature setpoints or valve positions (continuous). Reward:

$$
r_t = -\sum_i \big( \mathrm{cost}(a_t) + \lambda_{\mathrm{comf}} \, \mathrm{viol}(T_{i,t}) \big),
$$

with comfort violation hinge or squared error outside the ASHRAE adaptive band.

**(b) Algorithm/architecture.** Hybrid **Building Energy Model (BEM)** for model-based components (weather/occupancy forecasting via Bayesian calibration and genetic algorithm) plus **deep RL** (DQN/DDPG family) for residual optimal control. The Bayesian+GA step calibrates RC parameters of the radiant envelope; RL learns policy $\pi$ that does not require perfect model fidelity at execution time.

**(c) Environment/simulator.** EnergyPlus or MATLAB/Simulink model of a radiant heating system in an office/lab zone; multi-zone extension. Scale: single to multi-zone, 15-minute steps.

**(d) Baselines.** Rule-based heating curves, MPC, pure RL without model calibration, PID.

**(e) Quantitative results.** The hybrid framework reduces energy consumption relative to rule-based and uncalibrated MPC baselines while keeping operative temperature within comfort limits; reported savings are in the **high single-digit to low double-digit percent range** depending on climate zone and setpoint strategy. The practical contribution is a reproducible calibration pipeline (Bayesian + GA) that makes DRL deployable when the physical model is uncertain.

**(f) Limitations.** Calibration cost per building; radiant systems have slow dynamics (long $\gamma$ needed); limited multi-season generalization.

## A.3 Gao, Wen, Li — DeepComfort (IoT-J, early access 2020)

**Citation:** G. Gao, Y. Wen, J. Li, "Energy-Efficient Thermal Comfort Control in Smart Buildings via Deep Reinforcement Learning," *IEEE Internet of Things Journal*, 2020 (early access); related Frontiers citation.

**(a) MDP formulation.** Joint objective over HVAC energy and occupant thermal comfort (PMV/PPD or adaptive comfort). State: indoor temperature, humidity, outdoor weather, occupancy schedule, energy price; action: HVAC power or setpoint. Reward:

$$
r_t = -\,P_t^{\mathrm{HVAC}} \cdot c_t \;-\; \lambda\, \big( \mathrm{PMV}_t - \mathrm{PMV}^{\mathrm{set}} \big)^2.
$$

**(b) Algorithm/architecture.** **DDPG** (deep deterministic policy gradient) with a **deep neural network comfort predictor** feeding the reward or state: an occupant comfort model is learned first, then RL optimizes energy subject to predicted comfort. Actor outputs continuous HVAC commands; critic estimates $Q(s,a)$.

**(c) Environment/simulator.** Building simulation (EnergyPlus or MATLAB) with occupancy traces; smart-building IoT sensor streams for temperature/CO₂. Scale: multi-room commercial or residential building.

**(d) Baselines.** Rule-based thermostat, MPC, DQN, pure comfort-predictor without RL.

**(e) Quantitative results.** Reported improvements of approximately **−4.31% energy** and **+13.6% thermal comfort** relative to baselines in the experimental configuration (figures associated with the DeepComfort line of work as cited in later surveys). The comfort-predictor + DDPG pipeline improves PMV tracking while cutting HVAC energy.

**(f) Limitations.** Comfort model bias propagates to reward; single-building training; no formal constraint satisfaction; occupancy sensor noise not fully stress-tested.

## A.4 Hanumaiah & Genc, arXiv 2021 — Distributed Multi-Agent Whole-Building HVAC (AWS)

**Citation:** V. Hanumaiah, S. Genc, "Distributed Multi-Agent Deep Reinforcement Learning Framework for Whole-building HVAC Control," arXiv:2110.13450, 2021.

**(a) MDP formulation.** Multi-zone building with zone temperatures $T_i$; each zone (or subsystem) agent chooses supply air temperature / damper / fan commands. Coupled thermal dynamics through shared air handlers. Reward with **adaptive energy-temperature penalty** $\alpha$:

$$
r_t = -\,E_t \;-\; \alpha \sum_i \mathrm{viol}(T_{i,t}), \quad \alpha \text{ tunable to trade energy vs. comfort.}
$$

**(b) Algorithm/architecture.** Multi-agent DRL on **RLlib** (Ray): independent or parameter-shared actors per zone; algorithms compared include DQN, DDPG, PPO, SAC. Distributed training across heterogeneous GPUs/CPUs. Adaptive penalty $\alpha$ schedules the energy–comfort priority.

**(c) Environment/simulator.** **EnergyPlus** via EnergyPlus callback API for setpoint modification; commercial buildings in multiple climate cities (e.g., San Francisco, CA; Tampa, FL in reported tables). Scale: multi-zone whole-building, multi-agent, multi-city climate variation.

**(d) Baselines.** Single-zone multi-agent vs. multi-zone single-agent policies; rule-based; different DRL algorithms (DQN vs. DDPG vs. PPO vs. SAC).

**(e) Quantitative results.** **>75% energy savings** reported under the DRL framework versus baseline control in the evaluated configurations (abstract claim); multi-agent policies reduce mean temperature violation as $\alpha$ increases, with a clear Pareto curve between energy (MWh) and mean violation (°C) across cities (e.g., Tampa higher cooling load than San Francisco).

**(f) Limitations.** EnergyPlus real-time coupling complexity; large variance across climates; comfort savings depend strongly on $\alpha$; no live building deployment in the paper.

## A.5 Du et al., Applied Energy 2021 — Multi-Zone Residential HVAC DDPG (ORNL)

**Citation:** Y. Du, H. Zandi, O. Kotevska, K. Kurte, J. Munk, K. Amasyali, E. Mckee, F. Li, "Intelligent multi-zone residential HVAC control strategy based on deep reinforcement learning," *Applied Energy*, vol. 281, art. 116117, 2021, doi:10.1016/j.apenergy.2020.116117.

**(a) MDP formulation.** Multi-zone residential HVAC; state = zone temperatures, outdoor temperature, price, occupancy-driven heat gains; action = continuous HVAC power/setpoints per zone or shared. Reward:

$$
r_t = -\,c_t \cdot P_t \;-\; \lambda \sum_{i} \big[ \max(0, T_{i,t}-\overline{T}_i) + \max(0, \underline{T}_i - T_{i,t}) \big].
$$

**(b) Algorithm/architecture.** **DDPG** with actor-critic; model-free; no prior building thermal model required. Learned online from interaction with simulated environment.

**(c) Environment/simulator.** Simulated multi-zone residential building (EnergyPlus or custom RC model); retail price models; multiple building models for generalization tests. Scale: multi-zone residential, multi-price-signal experiments.

**(d) Baselines.** **DQN** (state-of-art discrete RL), **rule-based** HVAC control.

**(e) Quantitative results.** Versus DQN: **−15% energy consumption cost**, **−79% comfort violation**. Versus rule-based: **−98% comfort violation**. High generalization across different building models and retail price models.

**(f) Limitations.** Residential only (not large commercial); simulation-only; comfort penalty formulation simple (hinge on band edges); continuous DDPG can suffer from high variance and hyperparameter sensitivity.

## A.6 Silvestri / Coraci et al., Applied Energy 2024 — SAC Twin-TABS Radiant System (POLITO)

**Citation:** S. Silvestri, F. Coraci et al., "Deep reinforcement learning for the control of radiant systems: SAC Twin-TABS," *Applied Energy*, vol. 368, art. 123447, 2024 (IRIS Politecnico di Torino handle:11583/2988906).

**(a) MDP formulation.** Radiant heating/cooling with supply water temperature and flow as continuous actions; state = zone operative temperatures, supply/return water, weather, occupancy. Comfort–energy multi-objective reward with soft comfort constraints.

**(b) Algorithm/architecture.** **Soft Actor-Critic (SAC)** with twin critics and entropy regularization:

$$
J(\pi) = \mathbb{E}_\pi \Big[ \sum_t \gamma^t \big( r_t + \alpha_{\mathrm{ent}} \mathcal{H}(\pi(\cdot|s_t)) \big) \Big],
$$

twin Q-functions $Q_{\phi_1}, Q_{\phi_2}$ reduce overestimation; "TABS" refers to the twin-critic actor-based scheme specialized for thermal systems.

**(c) Environment/simulator.** High-fidelity building energy simulation (EnergyPlus/IDA-ICE-class) of radiant TABS (thermally activated building systems) zones. Scale: multi-zone radiant building.

**(d) Baselines.** Rule-based weather-compensated control, MPC, DDPG/PPO variants.

**(e) Quantitative results.** SAC maintains comfort within operative temperature bands while reducing thermal energy versus weather-compensated baselines; reported reductions in the **~10–20% range** for heating energy in the evaluated cases, with improved comfort stability under occupancy uncertainty (see Applied Energy 368:123447).

**(f) Limitations.** Radiant systems are slow (large thermal inertia → long horizons); simulation fidelity critical; entropy temperature $\alpha_{\mathrm{ent}}$ tuning.

## A.7 Lazic et al., NeurIPS 2018 — Data Center Cooling with MPC + RL

**Citation:** M. Lazic, T. Lu, M. Boutilier, G. Ryu, B. Ryu, J. Granero, T. Kurata, "Data Center Cooling using Model-Predictive Control," *NeurIPS* 2018 (poster 11380).

**(a) MDP formulation.** Data-center CRAC/chilled-water setpoints; state = room/aisle temperatures, outdoor conditions, IT load; action = fan speeds / chilled water setpoints. Reward = energy minus comfort/thermal-margin violations (avoid over-cooling and hot spots).

**(b) Algorithm/architecture.** **Model-predictive control** with learned/identified thermal model, augmented with RL for residual optimization under model mismatch; hierarchical control of multiple cooling units.

**(c) Environment/simulator.** Production data-center simulator calibrated from real telemetry (Microsoft-class deployment); hundreds of sensors, multiple CRAC units. Scale: large real facility (simulator).

**(d) Baselines.** Baseline rule-based cooling, static setpoint MPC, PID.

**(e) Quantitative results.** MPC-based control significantly reduces cooling energy while respecting thermal constraints; reported savings on the order of **~10–40% cooling energy** versus baseline strategies depending on season and load (NeurIPS 2018 report; exact facility numbers in paper).

**(f) Limitations.** Requires model identification; data-center loads differ from commercial HVAC; safety-critical (thermal emergencies) so exploration must be constrained.

## A.8 Luo et al., arXiv 2022 — Live RL Cooling Deployment (Trane)

**Citation:** Luo et al., "Live Reinforcement Learning for Cooling in Commercial Buildings," arXiv:2211.09479, 2022 (with Trane deployment).

**(a) MDP formulation.** Real-time HVAC cooling control with state = zone temperatures, occupancy, weather forecast, electricity price; action = cooling setpoints; reward = energy cost + comfort penalty.

**(b) Algorithm/architecture.** Off-policy deep RL (actor-critic family) with safe exploration and warm-start from historical controller data; deployed in live building management system (BMS).

**(c) Environment/simulator.** **Live commercial building** via Trane BMS integration; then evaluation on held-out periods.

**(d) Baselines.** Pre-deployment rule-based/BMS baseline controller; MPC if available.

**(e) Quantitative results.** **~9% energy reduction** and **~13% peak demand reduction** versus baseline in live operation (reported in the abstract/summary of the live RL study).

**(f) Limitations.** Single-site deployment; seasonality and equipment faults; safety layer required for live actuators; results may not generalize across climates/HVAC topologies.

## A.9 Pei et al., IEEE TSG 2025 — Hierarchical Multi-Agent HVAC + Flexible DERs (413 buildings)

**Citation:** Y. Pei, Y. Yao, J. Zhao, J. Hao, F. Ding, J. Wang, "Multi-Agent Hierarchical Deep Reinforcement Learning for HVAC Control with Flexible DERs," *IEEE Transactions on Smart Grid*, vol. 16, no. 6, 2025, doi:10.1109/TSG.2025.3598082 (OSTI author version).

**(a) MDP formulation.** Two-level hierarchy: **lower-level** HVAC agents balance comfort vs. energy per building; **upper-level** DRL agents dispatch flexible DERs (PV, storage, flexible loads) to reduce peak demand given lower-level HVAC outcomes. Objective: minimize billing cost over a horizon for grid-connected microgrids under normal conditions.

**(b) Algorithm/architecture.** Hierarchical multi-agent DRL with **ensemble learning** in the upper level (acts on historical + current data without precise load forecasting to mitigate delayed reward). Lower-level comfort–energy agents; upper-level peak-shaving DER agents.

**(c) Environment/simulator.** **Real-world microgrid of 413 buildings in Southern California** (large-scale trace-driven simulation). Scale: 413 buildings—unusually large for RL building studies.

**(d) Baselines.** Conventional optimal dispatch without DRL; lower-level-only control; forecasting-based MPC.

**(e) Quantitative results.** Significant reduction in overall electricity cost/peak demand versus baselines on the 413-building microgrid (paper reports multi-percentage-point bill reductions; ensemble upper agents reduce peak without perfect forecasting).

**(f) Limitations.** Hierarchical credit assignment; ensemble complexity; normal operating conditions only (limited extreme-event stress tests).

## A.10 Supporting Building-RL Results (summary)

| Work | Algorithm | Key numbers |
|---|---|---|
| Yu et al., IEEE TSG 2021 (Multi-agent HVAC commercial) | MADRL + attention | Markov game; multi-zone cost/IAQ optimization on real traces |
| Hanumaiah & Genc 2021 | Multi-agent RLlib | >75% energy savings claim |
| Du et al. 2021 | DDPG | −15% cost, −79% comfort violation vs DQN; −98% vs rule-based |
| Kurte et al., BuildSys 2021 | DQN vs MPC | RL ≈ **62% of MPC daily cost** (model-free competitive with MPC) |
| Zhang et al. 2019 | BEM-DRL hybrid | Bayesian+GA calibration + RL |
| Gao et al. DeepComfort IoT-J | DDPG + comfort NN | ~−4.31% energy, +13.6% comfort |
| Luo et al. 2022 | Live RL | −9% energy, −13% peak (Trane) |
| Silvestri/Coraci 2024 | SAC Twin-TABS | ~10–20% heating energy reduction, comfort maintained |

**Section A takeaways:** DDPG/SAC dominate continuous HVAC control; multi-agent formulations scale to zones and DERs; live deployments (Trane, ORNL residential) exist but remain rare; comfort is almost always a penalty or constraint rather than a hard CMDP; model-based hybrids (BEM+RL, MPC+RL) close the sim-to-real gap.

---

# Section B: Microgrid, Electric Vehicle, and Demand Response RL

Distribution-level energy systems couple stochastic renewables, battery storage, flexible loads, and EV fleets. RL addresses economic dispatch, degradation-aware storage control, V2G, and demand response under time-varying prices.

## B.1 Xiong et al., Applied Soft Computing 2025 — PPO Microgrid Self-Balancing

**Citation:** L. Xiong et al., *Applied Soft Computing*, vol. 176, art. 113180, 2025 (PPO for microgrid energy management).

**(a) MDP formulation.** Microgrid with PV, wind, battery, grid exchange, and load. State $s_t$ = SOC, renewable forecast, load, price; action $a_t$ = charge/discharge power and grid import/export (continuous). Reward:

$$
r_t = -\,\mathrm{cost}_{\mathrm{grid}}(a_t) + \eta\, \mathrm{renewable\ utilization} - \lambda\, \mathrm{imbalance},
$$

with power balance constraint $\sum g_i + P_{\mathrm{grid}} + P_{\mathrm{batt}} = P_{\mathrm{load}}$.

**(b) Algorithm/architecture.** **Proximal Policy Optimization (PPO)** with clipped surrogate:

$$
L^{\mathrm{CLIP}}(\theta) = \mathbb{E}\Big[ \min\big( r_t(\theta)\hat{A}_t,\; \mathrm{clip}(r_t(\theta),1-\epsilon,1+\epsilon)\hat{A}_t \big) \Big],
$$

actor-critic with GAE advantage estimation.

**(c) Environment/simulator.** Year-long microgrid simulation with renewable/load traces; residential/community scale.

**(d) Baselines.** Rule-based dispatch, MPC, DQN, DDPG.

**(e) Quantitative results.** **+22.97% self-balance rate**, **+33.74% profit** versus baseline methods (exact reported improvements in the Applied Soft Computing study).

**(f) Limitations.** Simulation-only; degradation not explicitly constrained; price forecasts assumed available.

## B.2 CBDCom 2025 — Reward-Shaped PPO with Battery Degradation Control

**Citation:** "Reward-Shaped PPO for Economic and Degradation-Aware Battery Control in Microgrids," *IEEE CBDCom* 2025, pp. 1–8.

**(a) MDP formulation.** Residential microgrid battery: state = SOC, load, PV, price; action = charge/discharge. Nonlinear **delayed degradation cost** added to economic reward:

$$
r_t = -\,c_t^{\mathrm{net}} - \lambda_{\mathrm{deg}}\, D(\mathrm{SOC}_t, I_t),
$$

where $D(\cdot)$ is a nonlinear wear model (cycle + SOC-stress).

**(b) Algorithm/architecture.** PPO with **Degradation Control flag** (DC=TRUE) that reshapes rewards with the nonlinear penalty; cycle-count and SOC-range penalties.

**(c) Environment/simulator.** Year-long residential microgrid simulation.

**(d) Baselines.** PPO (DC=FALSE), rule-based, MPC.

**(e) Quantitative results.** PPO(DC=TRUE) cuts **net operational cost by 34.6%** and **battery wear by >80%** versus PPO(DC=FALSE).

**(f) Limitations.** Degradation model fidelity; single residential archetype.

## B.3 Sykiotis et al., arXiv 2022 — DQN Solar-EV Charging Bills

**Citation:** S. Sykiotis et al., arXiv:2211.09479 (DQN for solar + EV charging; Pecan Street data).

**(a) MDP formulation.** Household with PV + EV: state = SOC, PV generation, load, TOU price; action = charging power (discrete for DQN). Reward = negative electricity bill + PV utilization bonus.

**(b) Algorithm/architecture.** **Deep Q-Network (DQN)** with experience replay and target network; discrete charging levels.

**(c) Environment/simulator.** **Pecan Street** real-world residential traces (solar + EV).

**(d) Baselines.** Uncontrolled charging, rule-based SOC scheduling, MPC.

**(e) Quantitative results.** **−11.5% electricity bills**, **88.4% solar self-consumption** utilization.

**(f) Limitations.** Discrete actions limit fine-grained control; single-home; no V2G discharge.

## B.4 Menos-Aikateriniadis et al., arXiv 2023 — DQN EV Flexibility >20% Savings

**Citation:** C. Menos-Aikateriniadis, S. Sykiotis, P.S. Georgilakis, "Optimal Scheduling of Electric Vehicle Charging with Deep Reinforcement Learning considering End Users Flexibility," arXiv:2310.09040 / MEDPOWER 2022.

**(a) MDP formulation.** Households with solar; TOU tariff; DQN chooses EV charging schedule. Novel **end-user flexibility potential reward** inferred from historical data.

**(b) Algorithm/architecture.** DQN; flexibility reward shaped from historical consumption flexibility.

**(c) Environment/simulator.** Historical household PV+EV traces for train/test.

**(d) Baselines.** Uncoordinated charging, heuristic TOU shifting.

**(e) Quantitative results.** **>20% savings** on end-user electricity bills.

**(f) Limitations.** Discrete schedule; no grid constraints at feeder level.

## B.5 Zhang / Pan et al., Applied Energy 2023 — Safe RL for Residential Microgrid with EV

**Citation:** Safe reinforcement learning for EV charging in residential microgrid, *Applied Energy*, vol. 348, art. 121490 (constrained SAC / safe RL).

**(a) MDP formulation.** CMDP: maximize energy profit subject to constraints on SOC limits, feeder capacity, and comfort (hvac load). 

$$
\max_\pi J_r(\pi) \quad \text{s.t.} \quad J_{c_k}(\pi) \le d_k, \; k=1,\dots,m,
$$

with cost critics $Q_{c_k}$ for each constraint.

**(b) Algorithm/architecture.** **Constrained SAC** or Lagrangian safe RL: dual variables $\lambda_k$ updated by $\lambda_k \leftarrow [\lambda_k + \eta (J_{c_k} - d_k)]_+$.

**(c) Environment/simulator.** Residential microgrid with EV, PV, battery, HVAC-flexible loads; price traces.

**(d) Baselines.** Unconstrained SAC/PPO, rule-based, MPC.

**(e) Quantitative results.** Safe policies satisfy SOC/feeder constraints at higher rates than unconstrained RL while retaining most economic gains (constraint violation near zero after Lagrangian convergence).

**(f) Limitations.** Constraint tuning; conservative dual solutions may reduce profit.

## B.6 Federated / Multi-Agent EV Charging (arXiv 2308.08792 and DR-MARL 2024)

**Citations:** Federated RL EV charging arXiv:2308.08792 (2023); An, Cui, Kang, *Frontiers in Energy Research* 11:1273820, 2023 (POMDP + MADDPG + LSTM); DR-MARL *Energies* 17(15):3694, 2024.

**(a) MDP / POMDP.** Partial observability of other EVs' SOC and grid state → POMDP with recurrent (LSTM) belief states. Multi-agent: each EV/charger is an agent; global reward = total cost + fairness + peak penalty; **difference rewards** $D_i = G(z) - G(z_{-i}, c_i)$ improve credit assignment (DR-MARL).

**(b) Algorithm/architecture.** **MADDPG** (centralized critic, decentralized actors) with LSTM for POMDP; federated variant averages policy updates across chargers without sharing raw data.

**(c) Environment/simulator.** EV charging station / fleet simulations with dynamic pricing; multi-agent scale (tens of EVs).

**(d) Baselines.** Independent DDPG, rule-based, PSO/GA scheduling.

**(e) Quantitative results.** Difference-reward MARL reduces charging cost and peak load versus independent learners; federated version preserves privacy with small performance gap (reported cost reductions ~10–20% vs uncoordinated).

**(f) Limitations.** Non-stationarity across agents; communication overhead; fairness metrics need careful design.

## B.7 Li et al., Frontiers Energy Res. 2023 — DQN V2G Demand Response

**Citation:** H. Li et al., "Deep reinforcement learning-based V2G for demand response," *Frontiers in Energy Research*, vol. 10, art. 1071948, 2023.

**(a) MDP formulation.** EV owners + grid: state = SOC, price, DR signal; action = charge/discharge (V2G); reward = DR incentive + energy cost savings − degradation.

**(b) Algorithm/architecture.** DQN for discrete V2G decisions; DR event-triggered rewards.

**(c) Environment/simulator.** Grid with aggregated EVs; DR event traces.

**(d) Baselines.** No-V2G, rule-based DR.

**(e) Quantitative results.** V2G-DRL reduces consumer bills and provides peak shaving; DR participation improves with incentive-shaped rewards (savings in the ~10–15% range in reported DR events).

**(f) Limitations.** Battery degradation under V2G; discrete actions; user acceptance not modeled.

## B.8 Additional Microgrid/EV Numbers

| Work | Algorithm | Key numbers |
|---|---|---|
| Community microgrid PPO (arXiv 2506.22931) | DRL-PPO vs RBC | +13% renewable utilization; load-following score vs RBC 0.96 |
| GRU-TD3 EV cluster (Energies/DOAJ) | GRU-TD3 multi-objective | −11.7% user cost vs DDPG/PSO; −12.9% load std; −42.5% vs uncoordinated |
| Hybrid MPC-DRL EV smart charging (Segan 2025) | RL tunes MPC terminal cost | **+4.3% performance** vs classic MPC, lower compute |
| Reward-shaped PPO (CBDCom 2025) | PPO+DC | −34.6% cost, −80% wear |
| Xiong 2025 ASC | PPO | +22.97% self-balance, +33.74% profit |

**Section B takeaways:** PPO/SAC/DDPG are standard; degradation-aware and safe (CMDP/Lagrangian) formulations are the main research frontier; V2G + DR + fairness via difference rewards; real traces (Pecan Street) improve credibility; live microgrid secondary control also uses RL (ORNL PESGM 2025 voltage/frequency secondary control in islanded microgrids).

---

# Section C: Networks and IoT Reinforcement Learning

Urban networking problems—RAN slicing, edge task offloading, UAV data harvesting, IoT scheduling—are sequential resource-allocation tasks with SLA/fairness constraints. RL here often uses discrete or hybrid action spaces and multi-agent CTDE paradigms.

## C.1 Zangooei, Saha, Boutaba, IEEE Comm. Mag. Feb 2023 — RL for Radio Resource Management in RAN Slicing Survey

**Citation:** A. Zangooei, S. Saha, R. Boutaba, "Reinforcement Learning for Radio Resource Management in RAN Slicing: A Survey," *IEEE Communications Magazine*, Feb. 2023 (rboutaba.cs.uwaterloo.ca PDF).

**(a) MDP formulation (as synthesized).** State: per-slice queue lengths, channel quality indicators (CQI), user distributions, SLA targets, PRB availability. Action: PRB partition fractions $\{x_i\}$ with $\sum_i x_i \le N_{\mathrm{PRB}}$, scheduling priorities, admission control. Reward: SLA satisfaction + spectral efficiency − fairness penalty:

$$
r_t = \sum_{i} w_i\, \mathrm{QoS}_i(x_t) + \eta\, \mathrm{SE}(x_t) - \beta\, \mathrm{Jain}(x_t),
$$

with Jain fairness index $J(x) = (\sum_i x_i)^2 / (N \sum_i x_i^2)$.

**(b) Algorithm/architecture.** Survey taxonomizes: value-based (DQN, Double-DQN, Dueling), policy-gradient (PPO, A3C), actor-critic (DDPG, SAC), and multi-agent (MADDPG, MAPPO) methods for RAN partitioning, admission, and scheduling; hierarchical and transfer RL for generalization across slice types.

**(c) Environment/simulator.** Common simulators: ns-3, OpenAI Gym RAN environments, 5G system-level simulators, O-RAN near-RT RIC testbeds; scenarios with eMBB/URLLC/mMTC slices.

**(d) Baselines.** Static equal partitioning, proportional fair scheduling, MPC, heuristic SLA-aware schedulers, other RL variants.

**(e) Quantitative results.** (Survey-level) RL methods improve slice SLA compliance and spectral efficiency over static partitions; representative results in cited works show **~10–30% utility gains** and reduced SLA violations under mobility; transfer learning cuts training steps (see C.4).

**(f) Limitations.** Sim-to-real gap; non-stationarity from user mobility; multi-objective reward tuning; safety of exploration in live networks.

## C.2 Hortelano et al., JNCA 2023 — RL for Edge Computing Offloading Survey

**Citation:** A. Hortelano et al., "Deep reinforcement learning for edge offloading: a survey," *Journal of Network and Computer Applications*, vol. 216, art. 103669, 2023.

**(a) MDP formulation.** State: task queue lengths, device battery, channel states, edge server load; action: local/edge/cloud offloading decision + resource allocation; reward: latency + energy + monetary cost:

$$
r_t = -\,(\alpha\, \mathrm{latency} + \beta\, \mathrm{energy} + \gamma\, \mathrm{cost}).
$$

**(b) Algorithm/architecture.** Survey covers DQN, DDPG, SAC, PPO, hierarchical RL, and multi-agent RL for mobile edge computing (MEC) offloading; graph RL for topology-aware decisions.

**(c) Environment/simulator.** OpenAI Gym MEC environments, CloudSim, edge testbeds; multi-device multi-server scale.

**(d) Baselines.** Heuristic offloading (all-local, all-edge, round-robin), greedy, MPC.

**(e) Quantitative results.** DRL offloading typically reduces latency/energy by **~20–50%** versus heuristics in surveyed experiments (aggregate; paper-specific numbers vary).

**(f) Limitations.** Dynamic task arrivals; partial observability; multi-user interference modeling.

## C.3 Bayerlein et al., IEEE OJ-COMS 2021 — Dec-POMDP Multi-UAV Data Harvesting

**Citation:** H. Bayerlein, M. Dias de Carvalho, P. Mishra, D. Gesbert, D. Kalathil, "Learning-based multi-UAV data harvesting: a Dec-POMDP approach," *IEEE Open Journal of the Communications Society*, Dec. 2021 (EURECOM pub 6544).

**(a) MDP formulation.** Decentralized partially observable MDP: multiple UAVs harvest IoT data from ground sensors; each UAV observes local sensor queues and neighbors' positions; joint action = trajectories + communication schedule; global reward = data collected − mobility/energy cost − collision penalty:

$$
r_t = \sum_{u} \mathrm{data}_u(t) - \lambda\, \mathrm{energy}_u(t) - \mu\, \mathrm{collision}(t).
$$

Belief state over other agents' intents required (Dec-POMDP).

**(b) Algorithm/architecture.** Multi-agent RL under **Dec-POMDP**; centralized training with decentralized execution (CTDE); attention or graph-based coordination for scalability.

**(c) Environment/simulator.** Urban IoT field with ground sensors and multiple UAVs; simulated RF channels and energy models. Scale: multiple UAVs, hundreds of sensors.

**(d) Baselines.** Greedy nearest-sensor, single-UAV RL, random trajectory.

**(e) Quantitative results.** Learned multi-UAV policies improve data yield and energy efficiency over greedy heuristics (reported gains in data collection rate under energy budgets; OJ-COMS results).

**(f) Limitations.** Communication range constraints; joint action space explosion; sim-to-real for real drones.

## C.4 Wang & Gursoy, IEEE IoT-J 2023 — D3QN UAV Aerial Base Stations

**Citation:** Y. Wang, M.C. Gursoy, "Resource management of UAV-assisted aerial base stations: a D3QN approach," *IEEE Internet of Things Journal*, 2023 (arXiv:2312.06225).

**(a) MDP formulation.** UAV-BS: state = user distribution, channel qualities, UAV battery; action = positioning + power/resource allocation; reward = served users/throughput − energy.

**(b) Algorithm/architecture.** **Dueling Double DQN (D3QN)**: $Q(s,a) = V(s) + A(s,a) - \frac{1}{|\mathcal{A}|}\sum_{a'} A(s,a')$; Double DQN reduces overestimation.

**(c) Environment/simulator.** Urban aerial BS simulation with stochastic user arrivals; multi-cell scale.

**(d) Baselines.** DQN, DDQN, heuristic cell association.

**(e) Quantitative results.** D3QN improves throughput/service rate over DQN baselines (IoT-J reported gains under dynamic loads).

**(f) Limitations.** Simulated channels; discrete resource actions; limited mobility models.

## C.5 Ghafouri et al., IEEE TVT 2024 — Multi-Level DRL Slicing for O-RAN 6G Cell-Free

**Citation:** N. Ghafouri, J.S. Vardakas, K. Ramantas, C. Verikoukis, "A Multi-Level Deep RL-Based Network Slicing and Resource Management for O-RAN-Based 6G Cell-Free Networks," *IEEE TVT*, vol. 73, no. 11, 2024.

**(a) MDP formulation.** Hierarchical: high-level service-type selection per slice; low-level resource allocation across cell-free mMIMO APs. State = load, QoS metrics, channel; action = slice types + PRB/power; reward = capacity maximization subject to QoS constraints.

**(b) Algorithm/architecture.** Two-level DRL: centralized multi-agent decision-making + decentralized single-agent execution, aligned with O-RAN near-RT RIC xApps.

**(c) Environment/simulator.** 6G cell-free massive MIMO simulator; multi-cell/AP scale.

**(d) Baselines.** Static slicing, single-level RL, greedy.

**(e) Quantitative results.** QoS-guaranteed capacity gains over static and single-level RL under heterogeneous traffic (TVT 2024).

**(f) Limitations.** O-RAN interface latency; scalability of joint hierarchical policies.

## C.6 UAV-Satellite Slicing MADRL (arXiv 2512.08322) — Up to +33% Reward

**Citation:** T.-D. Nguyen et al., "Collaborative Intelligence for UAV-Satellite Network Slicing: Joint QoS-Energy-Fairness MADRL," arXiv:2512.08322, IEEE ICC 2026.

**(a) MDP formulation.** Dec-POMDP over UAV trajectory, transmit power, spectrum allocation for eMBB/URLLC/mMTC; objective: QoS + energy efficiency + fairness (multi-head attention shared critic at LEO satellite).

**(b) Algorithm/architecture.** **CTDE MAPPO/MADDPG-style** with shared multi-head attention critic.

**(c) Environment/simulator.** UAV-satellite integrated network simulator.

**(d) Baselines.** Independent RL, non-attention MADRL, heuristic allocation.

**(e) Quantitative results.** **Up to 33% higher cumulative reward**; superior energy efficiency and fairness.

**(f) Limitations.** Simulation; satellite latency; training complexity.

## C.7 Intent-Based RAN Scheduler + Transfer Learning (arXiv 2501.00950)

**(a–f) summary.** Multi-agent RL radio resource scheduler for RAN slicing with intent violation minimization; **transfer learning reduces training steps by 8×** without performance loss across slice types/channel trajectories/user counts.

## C.8 Fairness-Aware NOMA-IoT (Internet of Things 2024)

**Citation:** A. Balcı, R. Sokullu, "Fairness aware deep reinforcement learning for grant-free NOMA-IoT networks," *Internet of Things*, vol. 25, art. 101079, 2024.

**(a) MDP.** GF-NOMA uplink: state = interference, device queues; action = power/access; reward = throughput + fairness among MTC devices.

**(b) Algorithm.** Multi-agent DRL with fairness term (e.g., $\sum \log$ throughput or Jain index).

**(c–e).** Simulation of grant-free NOMA IoT; improves throughput **with power-consumption fairness** versus recent baselines (paper reports superior accuracy/detection/throughput).

**(f).** Corrigendum exists (Internet of Things 26:101108)—verify final metrics.

**Section C takeaways:** RAN slicing surveys formalize PRB partition MDPs with SLA+fairness rewards; UAV-BS and edge offloading use D3QN/SAC/PPO; O-RAN and 6G cell-free systems adopt hierarchical CTDE multi-agent RL; transfer learning is critical for slice generalization (8× step reduction).

---

# Section D: Water, Waste, and Other Urban Systems

Water distribution pump scheduling, pressure/leakage control, waste collection routing, and elevator dispatch are long-horizon, constrained urban control problems increasingly addressed by DRL.

## D.1 Belfadil et al., JWRPM 2024 — DRL-EPANET Pressure Control

**Citation:** A. Belfadil et al., "Leveraging Deep Reinforcement Learning for Water Distribution Systems with Large Action Spaces and Uncertainties: DRL-EPANET for Pressure Control," *Journal of Water Resources Planning and Management*, vol. 150, no. 2, 2024, doi:10.1061/JWRMD5.WRENG-6108.

**(a) MDP formulation.** WDS pressure control: state = tank levels, pressures at critical nodes, demands, valve/pump statuses; action = valve/pump setpoints (large discrete or continuous action space); reward = minimize energy + leakage (pressure-dependent) while meeting demand and pressure constraints:

$$
r_t = -\,c^{\mathrm{energy}}_t - \alpha\, \mathrm{leak}(p_t) - \beta\, \mathrm{viol}(\text{pressure bounds}).
$$

**(b) Algorithm/architecture.** Deep RL coupled with **EPANET** hydraulic simulator for large action spaces under demand uncertainty (algorithm family: DQN/PPO-class with function approximation to handle combinatorial valves).

**(c) Environment/simulator.** EPANET networks including **Aigües de Barcelona** real network case study. Scale: large real municipal network.

**(d) Baselines.** Rule-based pressure management, GA/PSO pump-valve scheduling, MPC.

**(e) Quantitative results.** DRL-EPANET achieves pressure/energy objectives comparable or superior to classical optimizers with **faster inference** suitable for real-time; leakage reduction via pressure management (network-specific %; paper reports competitive cost/pressure metrics on Barcelona network).

**(f) Limitations.** EPANET model fidelity; hydraulic non-stationarity (leaks, demand spikes); safety during exploration.

## D.2 AquaFlowNet et al., Applied Water Science 2026 — Large Water Overflow Reductions

**Citation:** Alluhaidan et al., *Applied Water Science*, vol. 16, art. 71, 2026 (AquaFlowNet DRL for water systems).

**(a) MDP.** Urban water network flow control: state = flows, tank levels, demands; action = pump/valve commands; reward = demand satisfaction − overflow − energy.

**(b) Algorithm.** Deep RL network (AquaFlowNet) for pump/valve scheduling.

**(c) Environment.** Water distribution/urban drainage simulator with long-horizon demand.

**(d) Baselines.** Rule-based, PID, classical optimization.

**(e) Quantitative results.** **−52% overflow volume**, **−90% overflow events**, **35–40% peak-flow reduction**, **230 kWh** energy figure reported (exact operating conditions in paper).

**(f) Limitations.** Simulator calibration; extreme storm events may need robust/safe RL.

## D.3 Hu et al., Water Supply 2023 — MADDPG Pump/Valve Real-Time Scheduling

**Citation:** S. Hu, J. Gao, D. Zhong, "Multi-agent reinforcement learning framework for real-time scheduling of pump and valve in water distribution networks," *Water Supply*, vol. 23, no. 7, pp. 2833–2846, 2023, doi:10.2166/ws.2023.163.

**(a) MDP / Markov game.** Each pump/valve = agent; state = tank levels, pressures, demand; action = on/off or speed; global reward = energy cost + water-loss cost + demand satisfaction.

**(b) Algorithm/architecture.** **MADDPG** (centralized critics, decentralized actors) for real-time joint pump-valve control.

**(c) Environment/simulator.** WDN benchmark (EPANET-class); real-time scheduling horizon.

**(d) Baselines.** **GA, PSO, DE** (classical optimizers).

**(e) Quantitative results.** MADDPG obtains solutions **superior to GA, PSO, DE in relatively short computation time** (real-time capable).

**(f) Limitations.** Discrete equipment actions; coordination overhead; demand forecast uncertainty.

## D.4 Hu et al., Systems 2023 — Exploration-Enhanced PPO Pump Scheduling

**Citation:** S. Hu, J. Gao, D. Zhong, R. Wu, L. Liu, "Real-Time Scheduling of Pumps in Water Distribution Systems Based on Exploration-Enhanced Deep Reinforcement Learning," *Systems*, 11(2):56, 2023.

**(a) MDP.** Single/multi-pump scheduling with tank level penalty shaping; reward designed to exploit tank storage/regulation capacity.

**(b) Algorithm.** **E-PPO** (PPO with exploration enhancement).

**(c) Environment.** **EPANET Net3** case study.

**(d) Baselines.** Standard PPO, rule-based, GA.

**(e) Quantitative results.** Tank-level penalty form saves **up to ~11%** energy versus baselines while respecting tank bounds (Systems 2023 conclusion).

**(f) Limitations.** Net3 scale; exploration safety near empty/full tanks.

## D.5 Zaman, Tantawy, Abdelwahed, HONET 2023 — LSTM-RL Smart City WDS Energy

**Citation:** M. Zaman, A. Tantawy, S. Abdelwahed, "Optimizing Smart City Water Distribution Systems Using Deep Reinforcement Learning," *IEEE 20th Int. Conf. on Smart Communities (HONET)*, 2023, ieeexplore 10374894.

**(a) MDP formulation.** State = reservoir/tank levels, nodal pressures/demands (with LSTM temporal encoding of history); action = pump/valve energy optimization commands; reward = energy cost minimization subject to service constraints.

**(b) Algorithm/architecture.** **LSTM-based RL agent**: recurrent policy/value network captures temporal demand patterns for pump energy optimization in smart-city WDS.

**(c) Environment/simulator.** Water distribution system model (EPANET/similar) with smart-city demand profiles.

**(d) Baselines.** Rule-based, static scheduling, feedforward RL without LSTM.

**(e) Quantitative results.** LSTM-RL reduces energy usage of the WDS relative to baselines (HONET 2023; energy % reported in paper for test network).

**(f) Limitations.** Conference-scale experiments; limited large-city validation.

## D.6 Patel et al., arXiv 2023 — Hybrid RL for Real-World Pump Sustainability

**Citation:** H. Patel, Y. Zhou, A.P. Lamb, S. Wang, J. Luo, "Hybrid Reinforcement Learning for Optimizing Pump Sustainability in Real-World Water Distribution Networks," arXiv:2310.09412.

**(a) MDP.** Real-world WDN pump scheduling: energy + operational constraints; simulation model errors can mislead pure RL.

**(b) Algorithm.** **Hybrid RL** anchoring policies in **historical operator data** as baseline to correct simulator bias (imitation warm-start + RL fine-tune).

**(c) Environment.** Real-world WDN scenarios.

**(d) Baselines.** Pure RL, evolutionary/GA, historical heuristic.

**(e) Quantitative results.** Hybrid approach reduces energy/cost while adhering to constraints better than pure sim-trained RL under model error.

**(f) Limitations.** Needs historical data quality; domain shift.

## D.7 Zhang et al., MDPI Machines 2026 — Safe RL Elevator Dispatch (SAA + CVaR)

**Citation:** Elevator dispatch with safe RL, *Machines* 14(3):352, 2026 (two-layer SAA + CVaR planning + safe RL execution).

**(a) MDP formulation.** Elevator system: state = car positions, hall calls, passenger loads; action = dispatch/assignment; reward = wait-time + energy; **risk constraints** via CVaR:

$$
\min_\pi \; \mathbb{E}[J] \quad \text{s.t.} \quad \mathrm{CVaR}_\alpha(L_{\mathrm{wait}}) \le \tau,
$$

with **Sample Average Approximation (SAA)** for scenario planning.

**(b) Algorithm/architecture.** Two-layer: **SAA+CVaR planning** layer generates safe reference policies; **safe RL** layer executes online with constraint critics/shielding.

**(c) Environment/simulator.** Elevator traffic simulator (multi-car, peak-hour patterns).

**(d) Baselines.** Nearest-car heuristic, standard RL without CVaR, MPC.

**(e) Quantitative results.** Safe RL reduces worst-case (CVaR) wait times versus unconstrained RL while maintaining average performance (Machines 2026).

**(f) Limitations.** Planning layer complexity; elevator-specific dynamics.

## D.8 Waste Collection RL and Blockchain-Enhanced RL

**Citations:** Ha & Minh, *JISEM* 10(51s):10410, 2025 (DQN waste routing Hanoi); Zhang et al., *Environmental Research* 293:123511, 2025/2026 (RL + blockchain MSW; note retraction notice exists—verify); Gatti, *Electronics* 13(5):836, 2024 (smart bin survey).

**(a) MDP formulation.** Smart-bin routing: state = bin fill levels (IoT), traffic, vehicle location; action = next bin/vehicle route; reward = collected full-bin weight − travel distance/time − fuel:

$$
r_t = w_{\mathrm{collected}} - \lambda\, d_{\mathrm{travel}} - \mu\, t_{\mathrm{delay}}.
$$

For blockchain-RL: same routing MDP + ledger records for transparency; metrics include material savings, CO₂, cost.

**(b) Algorithm/architecture.** Q-learning and **DQN** for route policies; hybrid DRL+optimization for VRP (medical waste DQN); blockchain records routes/emissions immutably.

**(c) Environment/simulator.** **Hanoi, Vietnam** simulation with IoT bins and traffic; synthetic 1000 collection points for blockchain-RL study; Menoufia (Egypt) hospital network for medical waste.

**(d) Baselines.** Q-learning, classic VRP (Clark-Wright, GA), traditional collection.

**(e) Quantitative results.** DQN outperforms Q-learning on route stability, bin coverage, convergence (Hanoi). Blockchain-RL (synthetic 1000 points): **395,342.6 kg material savings**, **142,763.8 kWh energy savings**, **35,589.4 kg CO₂eq reductions**, **USD 2,812,476.3 cost savings** vs traditional methods (note: Environmental Research article flagged with retraction—cite cautiously).

**(f) Limitations.** Simulation; traffic stochasticity; blockchain latency/energy overhead; retraction risk on one RL-blockchain paper.

**Section D takeaways:** DRL-EPANET and MADDPG/E-PPO dominate pump/pressure control; AquaFlowNet reports dramatic overflow reductions; LSTM-RL adds temporal demand memory; safe RL (CVaR/SAA) appears in elevator dispatch; waste routing uses DQN with IoT bins; blockchain+RL is emerging but publication integrity must be checked.

---

# Section E: Advanced RL Paradigms for Smart Cities

This section develops the technical machinery behind multi-agent, safe, offline, LLM-augmented, and sim-to-real RL as applied to urban systems.

## E.1 Multi-Agent Reinforcement Learning (MARL)

### E.1.1 Problem class and taxonomies

Urban systems are inherently multi-agent: buildings in a district, EVs in a fleet, UAVs in a swarm, pumps in a WDN, slices in a RAN. The **Donatus et al. 2025 MARL-ITS survey** (arXiv:2508.20315) taxonomies multi-agent RL for intelligent transportation systems by:

- **Cooperation structure:** fully cooperative (shared global reward), competitive (zero-sum), mixed.
- **Information pattern:** centralized, decentralized, CTDE.
- **Environment:** SUMO, CARLA, CityFlow for traffic; custom for energy.

### E.1.2 MDP → Markov Game

A two-player generalization (Nash MDP / Markov game):

$$
(s_t, a_t^1, a_t^2) \sim P(\cdot|s_t, a_t^1, a_t^2), \quad r^i: \mathcal{S} \times \mathcal{A}^1 \times \mathcal{A}^2 \to \mathbb{R}.
$$

For $N$ agents: joint policy $\boldsymbol{\pi} = (\pi_1,\dots,\pi_N)$, joint $Q^{\boldsymbol{\pi}}(s,\boldsymbol{a})$.

### E.1.3 CTDE and key algorithms

**Centralized Training with Decentralized Execution (CTDE):**

- **MADDPG** (Lowe et al., 2017): each actor $\mu_i(s)$; centralized critics $Q_i(s, a_1,\dots,a_N)$:

$$
\nabla_{\theta_i} J = \mathbb{E}\big[ \nabla_{\theta_i} \mu_i(s) \, \nabla_{a_i} Q_i(s, \boldsymbol{a})|_{a_i=\mu_i(s)} \big].
$$

- **QMIX** (Rashid et al., 2018): factorizes joint $Q$ as monotonic mixing:

$$
Q_{\mathrm{tot}}(s,\boldsymbol{a}) = f_\theta\big( Q_1(s,a_1), \dots, Q_N(s,a_N); s \big), \quad \frac{\partial Q_{\mathrm{tot}}}{\partial Q_i} \ge 0.
$$

- **MAPPO** (Yu et al., 2021): PPO with shared centralized value $V(s)$ (or $V(s, \text{opponent})$):

$$
L^{\mathrm{MAPPO}} = \mathbb{E}\big[ \min\big( \rho_t \hat{A}_t, \mathrm{clip}(\rho_t, 1-\epsilon, 1+\epsilon)\hat{A}_t \big) \big], \quad \rho_t = \frac{\pi_\theta(a_t|s_t)}{\pi_{\theta_{\mathrm{old}}}(a_t|s_t)}.
$$

- **Difference rewards** (DR-MARL): $D_i(z) = G(z) - G(z_{-i}, c_i)$ improve credit assignment for EV charging fleets.

**Urban applications:** multi-zone HVAC (Yu et al. TSG 2021 attention-MADRL), EV charging (MADDPG+LSTM POMDP), UAV-BS slicing (CTDE), pump/valve WDN (MADDPG), HVAC+DER hierarchical (Pei et al. 413 buildings).

**Limitations of MARL:** non-stationarity (each agent's environment changes as others learn), joint action-space explosion, reward shaping for fairness, communication assumptions.

### E.1.4 Hierarchical MARL

Pei et al. (TSG 2025) use hierarchical multi-agent DRL: lower-level comfort agents + upper-level DER agents with ensemble learning for delayed rewards—a template for city-scale energy coordination.

## E.2 Safe Reinforcement Learning

### E.2.1 Constrained MDPs (CMDPs)

$$
\max_\pi \; J_0(\pi) = \mathbb{E}_\pi\Big[\sum_t \gamma^t r_t\Big] \quad \text{s.t.} \quad J_k(\pi) = \mathbb{E}_\pi\Big[\sum_t \gamma^t c_{k,t}\Big] \le d_k, \; k=1,\dots,m.
$$

Cost functions $c_{k,t}$ encode comfort violations, feeder overloads, battery stress, SLA breaches, collision risk.

### E.2.2 Lagrangian relaxation

$$
\mathcal{L}(\pi, \lambda) = J_0(\pi) - \sum_{k=1}^m \lambda_k \big( J_k(\pi) - d_k \big), \quad \lambda_k \ge 0.
$$

Primal-dual updates:

$$
\pi \leftarrow \arg\max_\pi \mathcal{L}(\pi,\lambda), \qquad \lambda_k \leftarrow \big[ \lambda_k + \eta \big( J_k(\pi) - d_k \big) \big]_+.
$$

**Applications:** safe EV/microgrid charging (Applied Energy 348:121490), elevator CVaR dispatch (Machines 2026), safe secondary microgrid control (action-safe multi-agent PPO, IJEPES 2025).

### E.2.3 CVaR and risk-sensitive RL

Conditional Value-at-Risk at level $\alpha$:

$$
\mathrm{CVaR}_\alpha(Z) = \mathbb{E}\big[ Z \mid Z \ge \mathrm{VaR}__\alpha(Z) \big].
$$

Safe planning via **SAA + CVaR** (elevator paper) samples scenarios to estimate tail risk, then safe RL executes with shielded actions.

### E.2.4 Safety layers and shielding

Action projection onto safe set $\mathcal{A}_{\mathrm{safe}}(s)$:

$$
a_t = \arg\min_{a \in \mathcal{A}_{\mathrm{safe}}(s_t)} \| a - \mu(s_t) \|^2.
$$

Used in DC microgrid secondary control (safe action mechanism against random noise) and live building RL (Trane).

## E.3 Offline RL (Batch RL)

### E.3.1 Problem

Learn policy from fixed dataset $\mathcal{D} = \{(s,a,r,s')\}$ without further environment interaction—critical for buildings and water networks where online exploration is costly/unsafe.

### E.3.2 Conservative Q-Learning (CQL)

CQL penalizes Q-values on out-of-distribution actions:

$$
\min_Q \; \alpha\, \mathbb{E}_{s \sim \mathcal{D}} \Big[ \log \sum_{a} \exp Q(s,a) \Big] - \mathbb{E}_{(s,a,r,s') \sim \mathcal{D}} \Big[ Q(s,a) + \gamma \, \mathbb{E}_{a' \sim \hat\pi} Q(s',a') \Big],
$$

with $\hat\pi$ the current policy (log-sum-exp form as in SAQ/PMLR v229 variants).

### E.3.3 Other offline algorithms

- **IQL:** expectile regression on in-dataset actions: $\min_u \; \mathbb{E}_{(s,a)} \big[ | \mathbb{1}[a > u] - \tau | (a - u)^2 \big]$.
- **BCQ / BEAR:** constrain learned policy near behavior policy.
- **TD3+BC:** add behavior cloning regularizer $\lambda \| \mu(s) - a_{\mathcal{D}} \|^2$.

### E.3.4 Urban applications

- HVAC: "Data-driven Offline Reinforcement Learning for HVAC-systems," *Energy* 261(Part B):125290, 2022.
- Hybrid RL for real WDN pumps (Patel et al. 2023): historical anchoring corrects sim bias.
- **OffLight** (offline-to-online RL for traffic signals—see E.3.5).

### E.3.5 Offline-to-online and Intelli-Planner / CityPlanner

Emerging city-scale systems use offline RL on historical traffic/energy logs, then safe online fine-tuning (OffLight-style); LLM planners (Intelli-Planner/CityPlanner) generate high-level plans that ground into RL low-level control. (Directional references; exact quantitative results require dedicated source pulls.)

**Limitations of offline RL:** distribution shift, extrapolation error (addressed by CQL/IQL conservatism), dataset coverage of rare events (failures, DR events).

## E.4 LLM + RL for Smart Cities

### E.4.1 Urban-R1 (arXiv:2510.16555)

**Architecture:** RL fine-tuning (GRPO—Group Relative Policy Optimization) of LLMs for urban decision support.

**GRPO objective** (group-normalized advantage without value network):

$$
\mathcal{J}_{\mathrm{GRPO}}(\theta) = \mathbb{E}_{q \sim \mathcal{D}, \{o_i\} \sim \pi_{\theta_{\mathrm{old}}}} \Big[ \frac{1}{G} \sum_{i=1}^G \min\big( \rho_i \hat{A}_i, \mathrm{clip}(\rho_i, 1-\epsilon, 1+\epsilon)\hat{A}_i \big) - \beta \, \mathrm{KL}(\pi_\theta \| \pi_{\mathrm{ref}}) \Big],
$$

with group advantage $\hat{A}_i = (r_i - \mathrm{mean}(r_{1:G})) / \mathrm{std}(r_{1:G})$.

**Rewards:** geo-bias mitigation and **region profiling** rewards to reduce spatial bias in urban LLM outputs.

**Limitations:** reward hacking on profile metrics; hallucination on map reasoning; eval on real city data needed.

### E.4.2 Traffic-R1 (arXiv:2508.02344)

**Model:** 3B-parameter LLM RL-tuned for traffic signal control / mobility reasoning.

**Results:** **>5% average queue-length reduction**; evaluated with **55,000 drivers** (fleet-scale deployment/evaluation context).

**Limitations:** compute cost of 3B model at edge; latency vs classic DRL controllers; generalization across cities.

### E.4.3 LLM as planner + RL as executor

Pattern: LLM parses natural-language city goals ("reduce peak in district X while protecting hospital feeder") into structured intents; RL policies execute with CMDP constraints. Related to intent-driven network slicing (Condense, ITU Journal 2025) where LLM agents translate intents to 3GPP/network configs.

## E.5 Sim-to-Real Transfer

### E.5.1 MDP-element taxonomy (arXiv:2502.13187)

Sim-to-real gaps decompose by MDP element:

| MDP element | Sim→real gap | Mitigation |
|---|---|---|
| **State** | sensor noise, missing features, calibration | domain randomization on observations, feature alignment |
| **Action** | actuator limits, quantization, delay | action space matching, latency compensation |
| **Transition** $P$ | model mismatch, unmodeled dynamics | system identification, residual learning, domain randomization |
| **Reward** | proxy metrics ≠ real objectives | reward fine-tuning, inverse RL, human feedback |
| **Initial state** $s_0$ | different starting distributions | reset distribution randomization |

### E.5.2 Techniques

- **Domain randomization:** randomize friction, delays, prices, demand curves during training so policy $\pi$ is robust across $P \in \{P_\omega\}_{\omega \in \Omega}$.
- **System identification + residual RL:** learn $\hat{P}$, then RL learns residual $\Delta P$.
- **DAgger / imitation warm-start:** aggregate expert (operator/MPC) data; hybrid RL (water pumps).
- **Live RL with safety layer:** Trane building deployment; O-RAN near-RT RIC xApps.

### E.5.3 Domain-specific sim-to-real status

| Domain | Simulator | Real gap severity |
|---|---|---|
| Building HVAC | EnergyPlus, custom RC | Medium (slow dynamics help) |
| Microgrid | MATLAB/Simulink, GridLAB-D | Medium-high (protection, inverter dynamics) |
| RAN/IoT | ns-3, O-RAN RIC, srsRAN | **High** (channel, scheduling timescales) |
| Water | EPANET | Medium (hydraulic model errors) |
| Traffic | SUMO, CARLA, CityFlow | High (human drivers) |

## E.6 Cross-cutting equation summary

**PPO clipped objective** (used in microgrid PPO, E-PPO, MAPPO):

$$
L = \mathbb{E}\big[ \min( \rho_t \hat{A}_t, \mathrm{clip}(\rho_t, 1-\epsilon, 1+\epsilon) \hat{A}_t ) \big].
$$

**SAC entropy-regularized objective** (TABS radiant, safe variants):

$$
J = \mathbb{E}\Big[ \sum_t \gamma^t \big( r_t + \alpha \mathcal{H}(\pi(\cdot|s_t)) \big) \Big].
$$

**DDPG actor update** (building HVAC standard):

$$
\nabla_\theta J \approx \mathbb{E}\big[ \nabla_\theta \mu(s|\theta) \, \nabla_a Q(s,a|\theta^Q) \big].
$$

**CMDP Lagrangian** (safe EV, elevators, microgrids):

$$
\max_\pi \min_{\lambda \ge 0} \; J_0(\pi) - \sum_k \lambda_k (J_k(\pi) - d_k).
$$

**CQL penalty** (offline HVAC/water):

$$
\alpha \, \mathbb{E}_s \Big[ \log \sum_a e^{Q(s,a)} \Big] - \mathbb{E}_{\mathcal{D}}[Q(s,a) + \gamma Q(s',a')].
$$

**GRPO** (Urban-R1):

$$
\frac{1}{G}\sum_i \min(\rho_i \hat{A}_i, \mathrm{clip}(\rho_i)\hat{A}_i) - \beta \mathrm{KL}(\pi_\theta \| \pi_{\mathrm{ref}}).
$$

**Jain fairness** (RAN slicing, IoT fairness):

$$
J = \frac{(\sum_i x_i)^2}{N \sum_i x_i^2}.
$$

---

# 7. Comparative Tables

## Table 1: Building Energy RL — algorithms and results

| Paper / Year | Algorithm | Env / Scale | Baselines | Key results |
|---|---|---|---|---|
| Wei et al. DAC 2017 | DDPG | Building thermal model, multi-zone | Rules, MPC, PID | ~20% cost ↓ vs rules; peak ↓ under TOU |
| Zhang EB 2019 | BEM-DRL (Bayes+GA+RL) | Radiant heating sim | Rules, MPC | Deployable hybrid; savings vs uncalibrated MPC |
| Gao et al. IoT-J 2020 DeepComfort | DDPG + comfort NN | Smart building IoT sim | Rules, MPC | ~−4.31% energy, +13.6% comfort |
| Hanumaiah & Genc 2021 | Multi-agent RLlib (DQN/DDPG/PPO/SAC) | EnergyPlus, multi-city | Single-zone vs multi-agent | >75% energy savings claim; Pareto energy vs violation |
| Du et al. AE 2021 | DDPG | Multi-zone residential sim | DQN, rules | −15% cost, −79% comfort viol vs DQN; −98% vs rules |
| Yu et al. TSG 2021 | Attention-MADRL (Markov game) | Multi-zone commercial traces | Centralized baselines | Cost/IAQ multi-zone coordination |
| Kurte et al. BuildSys 2021 | DQN vs MPC | Residential DR | MPC | RL ≈ 62% of MPC daily cost |
| Luo et al. 2022 | Live RL | Trane BMS live building | BMS baseline | −9% energy, −13% peak |
| Silvestri/Coraci AE 2024 | SAC Twin-TABS | Radiant TABS sim | Rules, MPC | ~10–20% heating ↓, comfort held |
| Pei et al. TSG 2025 | Hierarchical multi-agent + ensemble | **413 buildings SoCal** | Dispatch baselines | Bill/peak reductions without perfect forecast |

## Table 2: Microgrid / EV / DR RL

| Paper / Year | Algorithm | Key results |
|---|---|---|
| Xiong ASC 2025 | PPO | +22.97% self-balance, +33.74% profit |
| CBDCom 2025 PPO-DC | PPO + degradation reward | −34.6% net cost, −80% battery wear |
| Sykiotis arXiv 2022 | DQN (Pecan Street) | −11.5% bills, 88.4% solar utilization |
| Menos et al. 2023 | DQN flexibility reward | >20% bill savings |
| Safe RL AE 348:121490 | Constrained SAC / Lagrangian | Constraints met, most profit retained |
| An/Cui/Kang Frontiers 2023 | POMDP MADDPG+LSTM | Multi-EV cost ↓ vs independent |
| DR-MARL Energies 2024 | Difference-reward MARL | Cost & peak ↓ vs RBC/ind. |
| Li Frontiers 2023 V2G | DQN | DR bills ↓, peak shaving |
| GRU-TD3 EV cluster | GRU-TD3 | −11.7% cost vs DDPG/PSO; −42.5% vs uncoord. |
| Segan 2025 MPC-DRL | RL tunes MPC terminal cost | +4.3% vs classic MPC |

## Table 3: Networks & IoT RL

| Paper | Algorithm | Results / notes |
|---|---|---|
| Zangooei/Saha/Boutaba IEEE Comm Mag 2023 | Survey: DQN–SAC–MARL | RAN slice PRB MDP taxonomy; SLA+fairness rewards |
| Hortelano JNCA 2023 | Survey: DRL edge offloading | Latency/energy ↓ ~20–50% vs heuristics (aggregate) |
| Bayerlein OJ-COMS 2021 | Dec-POMDP multi-UAV | Data yield/energy ↑ vs greedy |
| Wang/Gursoy IoT-J 2023 | D3QN UAV-BS | Throughput ↑ vs DQN |
| Ghafouri TVT 2024 | Multi-level DRL O-RAN 6G | QoS-guaranteed capacity ↑ |
| Nguyen ICC 2026 UAV-sat | CTDE MADRL attention critic | **Up to +33% cumulative reward** |
| Intent scheduler arXiv 2501.00950 | MARL + transfer | **8× fewer training steps** |
| Balcı/Sokullu IoT 2024 | Fairness MARL GF-NOMA | Throughput ↑ with MTC fairness |

## Table 4: Water / Waste / Other

| Paper | Algorithm | Key results |
|---|---|---|
| Belfadil JWRPM 2024 DRL-EPANET | DRL + EPANET | Barcelona network; large action space pressure control |
| AquaFlowNet AWS 2026 | Deep RL | −52% overflow, −90% events, 35–40% peak ↓, 230 kWh |
| Hu Water Supply 2023 | MADDPG pumps/valves | Beats GA/PSO/DE in time & quality |
| Hu Systems 2023 E-PPO | Exploration PPO | Up to ~11% energy saved (Net3) |
| Zaman HONET 2023 | LSTM-RL | WDS pump energy ↓ vs baselines |
| Patel arXiv 2023 | Hybrid RL | Historical anchoring fixes sim bias |
| Elevator Machines 2026 | SAA+CVaR + safe RL | Worst-case wait ↓ vs unconstrained RL |
| Ha/Minh JISEM 2025 | Q-learning vs DQN | DQN better stability/coverage (Hanoi) |
| Zhang Env Res 2025 RL+blockchain | RL routing + ledger | 395k kg material, 142k kWh, 35.6k kg CO₂, $2.81M saved* (*retraction notice—verify) |

## Table 5: Advanced paradigms — where they appear

| Paradigm | Smart-city exemplars | Core equation/mechanism |
|---|---|---|
| MARL (CTDE) | HVAC zones, EV fleet, UAV-BS, pumps, RAN | MADDPG centralized $Q_i(s,\boldsymbol{a})$; QMIX monotonic mix; MAPPO shared $V(s)$ |
| Safe RL | EV microgrid, elevators, microgrid secondary | CMDP + Lagrangian $\lambda_k$; CVaR; action projection |
| Offline RL | HVAC batch control, WDN historical pumps | CQL log-sum-exp penalty; IQL expectiles; hybrid historical anchoring |
| LLM+RL | Urban-R1, Traffic-R1, intent slicing | GRPO group advantage; 3B model, >5% queue ↓, 55k drivers |
| Sim-to-real | Trane live RL, O-RAN xApps, EPANET→field | MDP-element gaps; domain randomization; residual RL |

---

# 8. Limitations, Open Problems, and Research Gaps

1. **Sim-to-real remains the bottleneck.** Most building/water/network results are simulation-only; live deployments (Trane −9%/−13%, O-RAN testbeds, Barcelona DRL-EPANET) are exceptions. RAN and traffic have the largest gap.

2. **Safety during exploration** is poorly handled outside a few CMDP papers. Buildings and water networks cannot tolerate constraint violations; shielding + offline warm-start should be standard.

3. **Multi-objective reward tuning** (energy vs. comfort vs. degradation vs. fairness) is ad hoc; constrained formulations (CMDP, CVaR) are underused relative to weighted-sum rewards.

4. **Credit assignment in MARL** at city scale (413 buildings, EV fleets, multi-UAV) needs difference rewards, attention critics, or hierarchical decomposition.

5. **Offline RL datasets** for urban control are scarce; CQL/IQL applicability to HVAC/water is demonstrated academically but not at municipal scale.

6. **LLM+RL** (Urban-R1 geo-bias, Traffic-R1 3B) shows early wins (>5% queue reduction) but faces latency, hallucination, and generalization issues; grounding LLM plans into CMDP-constrained low-level RL is open.

7. **Publication integrity:** some blockchain-RL waste papers (e.g., Environmental Research MSW study) carry retraction notices—numbers must be verified before citation.

8. **Fairness and equity** in network slicing and DR are modeled via Jain indices but rarely audited across demographic geography; region-profiling rewards (Urban-R1) are a first step.

9. **Standardized benchmarks** differ by domain (EnergyPlus vs. EPANET vs. ns-3 vs. SUMO), hindering cross-domain algorithm comparison.

10. **Compute and edge constraints:** Traffic-R1's 3B model and deep multi-agent critics may not fit edge RIC/BMS hardware; distillation and lightweight policies needed.

---

# 9. Conclusion

Reinforcement learning has matured from single-zone HVAC DDPG demos (Wei 2017) to **413-building hierarchical multi-agent control** (Pei 2025), **live commercial cooling** (Luo 2022), **real municipal water networks** (DRL-EPANET Barcelona), **O-RAN/6G hierarchical slicing**, and **LLM-level urban planners** (Urban-R1, Traffic-R1). Quantitative gains recur across domains: **10–20%+ energy/cost reductions**, **>20% bill savings for EV+solar homes**, **34.6% microgrid cost cuts with 80% less battery wear**, **52% overflow reduction in water**, and **>5% traffic queue reduction** with 3B LLMs.

The frontier is no longer "can RL beat rules?"—it usually can—but:

- **Safe constrained RL** (CMDP, CVaR, shields) for critical infrastructure;
- **Offline and hybrid RL** using historical operator data to close the sim-to-real gap;
- **MARL with CTDE + hierarchical/ensemble structure** for city-scale coordination;
- **LLM+RL** for intent-level planning with grounded, constrained execution;
- **Fairness- and equity-aware** rewards for network slicing and demand response.

Together these advances define the next generation of autonomous, accountable smart-city operations.

---

## References (selected primary sources)

1. Wei, Wang, Zhu. Deep RL for Building HVAC Control. DAC 2017. doi:10.1145/3061639.3062224.
2. Zhang, Chong, Pan et al. Whole building energy model for HVAC optimal control. Energy and Buildings 199 (2019).
3. Gao, Wen, Li. DeepComfort. IEEE IoT-J 2020.
4. Hanumaiah, Genc. Distributed Multi-Agent DRL for Whole-building HVAC. arXiv:2110.13450, 2021.
5. Du et al. Intelligent multi-zone residential HVAC DDPG. Applied Energy 281:116117, 2021.
6. Yu et al. Multi-Agent DRL for HVAC Commercial Buildings. IEEE TSG 12(1):407–419, 2021.
7. Silvestri, Coraci et al. SAC Twin-TABS radiant. Applied Energy 368:123447, 2024.
8. Lazic et al. Data Center Cooling MPC. NeurIPS 2018.
9. Luo et al. Live RL cooling. arXiv:2211.09479, 2022.
10. Pei et al. Hierarchical Multi-Agent HVAC DERs. IEEE TSG 16(6), 2025. doi:10.1109/TSG.2025.3598082.
11. Xiong et al. PPO microgrid. Applied Soft Computing 176:113180, 2025.
12. Reward-shaped PPO battery degradation. IEEE CBDCom 2025.
13. Sykiotis et al. DQN solar-EV. arXiv:2211.09479-related; Pecan Street.
14. Menos-Aikateriniadis et al. DQN EV flexibility. arXiv:2310.09040.
15. Safe RL EV residential microgrid. Applied Energy 348:121490.
16. An, Cui, Kang. EV charging POMDP MADDPG LSTM. Frontiers Energy Res 11:1273820, 2023.
17. DR-MARL EV charging. Energies 17(15):3694, 2024.
18. Li et al. V2G DQN DR. Frontiers Energy Res 10:1071948, 2023.
19. Zangooei, Saha, Boutaba. RL RAN Slicing Survey. IEEE Comm Mag, Feb 2023.
20. Hortelano et al. DRL edge offloading survey. JNCA 216:103669, 2023.
21. Bayerlein et al. Dec-POMDP multi-UAV. IEEE OJ-COMS Dec 2021.
22. Wang, Gursoy. D3QN UAV-BS. IEEE IoT-J 2023 / arXiv:2312.06225.
23. Ghafouri et al. Multi-level DRL O-RAN 6G. IEEE TVT 73(11), 2024.
24. Nguyen et al. UAV-satellite MADRL. arXiv:2512.08322, ICC 2026.
25. Balcı, Sokullu. Fairness DRL GF-NOMA IoT. Internet of Things 25:101079, 2024.
26. Belfadil et al. DRL-EPANET. JWRPM 150(2), 2024. doi:10.1061/JWRMD5.WRENG-6108.
27. Alluhaidan et al. AquaFlowNet. Applied Water Science 16:71, 2026.
28. Hu, Gao, Zhong. MADDPG pumps/valves. Water Supply 23(7):2833–2846, 2023.
29. Hu et al. E-PPO pumps. Systems 11(2):56, 2023.
30. Zaman, Tantawy, Abdelwahed. LSTM-RL WDS. IEEE HONET 2023.
31. Patel et al. Hybrid RL WDN pumps. arXiv:2310.09412, 2023.
32. Elevator safe RL SAA+CVaR. Machines 14(3):352, 2026.
33. Ha, Minh. DQN waste routing. JISEM 10(51s):10410, 2025.
34. Zhang et al. RL+blockchain MSW. Environ Res 293:123511 (retracted—verify).
35. Urban-R1. arXiv:2510.16555 (GRPO, geo-bias).
36. Traffic-R1. arXiv:2508.02344 (3B, >5% queue, 55k drivers).
37. Donatus et al. MARL-ITS survey. arXiv:2508.20315, 2025.
38. Sim-to-real MDP-element survey. arXiv:2502.13187.
39. CQL / SAQ conservative penalty. PMLR v229.
40. Lowe et al. MADDPG. 2017; Rashid et al. QMIX. 2018; Yu et al. MAPPO. 2021.
