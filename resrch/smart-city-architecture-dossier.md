# Smart City Core Architecture — Deep Technical Research Dossier

**Scope:** 15 deep-dive entries (12 canonical papers/areas + 3 recent 2024–2026 architectural papers), each extracted for (a) problem formulation, (b) system architecture/layers, (c) algorithms/protocols/equations, (d) datasets/testbeds/deployments, (e) quantitative results, (f) limitations.
**Compiled:** November 2026. Research-only dossier; no code.

---

## Table of Contents
1. Zanella et al. 2014 — IoT for Smart Cities (IEEE IoT-J)
2. Gubbi et al. 2013 — IoT Vision & Architectural Elements
3. Al-Fuqaha et al. 2015 — IoT Protocol Survey (MQTT/CoAP/XMPP/AMQP/DDS)
4. Akyildiz et al. 2002 — Wireless Sensor Networks Survey
5. Shi et al. 2016 — Edge Computing: Vision and Challenges
6. Lee 2008 — Cyber-Physical Systems: Design Challenges
7. Kitchin 2014 — The Real-Time City? Big Data and Smart Urbanism
8. Blockchain for Smart Cities — Xie et al. 2019 + IOTA/Ethereum/Hyperledger
9. Digital Twins — Peldon et al. 2024 & Weil et al. 2023
10. 5G/6G for Smart Cities — Murroni et al. 2023 (+ IMT-2020/2030 KPIs, RIS/THz)
11. Interoperability Stack — oneM2M / SAREF / CityGML / OGC SensorThings
12. City Deployments — Virtual Singapore / Seoul S-DoT / Songdo
13. Recent Paper A — 6G Architectural Approaches Survey (2025)
14. Recent Paper B — Big Data & IoT for Smart Cities (Internet of Things journal, 2025)
15. Recent Paper C — Data Mesh / IoT-Edge-Cloud Continuum Architectures (2024–2026)

---

# 1. Zanella, Bui, Castellani, Vangelista, Zorzi (2014) — "Internet of Things for Smart Cities," IEEE Internet of Things Journal 1(1):22–32, DOI 10.1109/JIOT.2014.2306328

## (a) Problem formulation
The IoT must "transparently and seamlessly incorporate a large number of different and heterogeneous end systems, while providing open access to selected subsets of data for the development of a plethora of digital services." Building a *general* IoT architecture is "a very complex task, mainly because of the extremely large variety of devices, link layer technologies, and services." The paper narrows the scope to **urban IoTs** — IoTs designed specifically to support the Smart City vision for city administration and citizens. The core problem is thus *heterogeneity management at urban scale*: unifying constrained and unconstrained protocol stacks, multiple radio technologies, and multiple service classes under one architecture without forcing a single technology choice.

## (b) System architecture / layers
**Conceptual urban IoT architecture (three-tier "things–backbone–services"):**
1. **Perception/thing layer** — heterogeneous end systems: sensors, actuators, displays, vehicles, RFID tags, smartphones.
2. **Network/backbone layer** — connects sensor clouds to the Internet: 6LoWPAN/IEEE 802.15.4 islands, LoRa/3G/4G/GPRS, fixed broadband (optical fiber, Ethernet), PLC (power-line), TV white spaces. Gateway nodes translate constrained ↔ unconstrained stacks.
3. **Application/service layer** — smart services: air quality, noise monitoring, traffic congestion, city energy consumption, structural health of buildings, smart parking, public-building automation/salubrity, smart lighting, waste management.

**Dual protocol stack (Fig. 2 of the paper):**
- **Unconstrained (Internet host) stack:** HTML/XML → HTTP/TCP → IPv4/IPv6.
- **Constrained (IoT node) stack:** EXI (Efficient XML Interchange, W3C) → CoAP/UDP → IPv6/6LoWPAN → IEEE 802.15.4.
- EXI mirrors HTML/XML, CoAP mirrors HTTP, 6LoWPAN mirrors IPv6 — a deliberate 1:1 "constrained counterpart" mapping so that constrained nodes remain addressable from anywhere on the Internet via IPv6.

## (c) Algorithms / protocol details
- **6LoWPAN (RFC 6282):** header compression of the 128-bit IPv6 address field (which otherwise "provides a 128-bit address field" too large for 802.15.4 MTU of 127 bytes) using context-based prefix compression and stateless address autoconfiguration; fragmentation of IPv6 datagrams into 802.15.4 frames.
- **RPL (RFC 6550):** the IPv6 Routing Protocol for Low-Power and Lossy Networks; builds a Destination-Oriented Directed Acyclic Graph (DODAG) rooted at the gateway. The gateway is simultaneously **6LoWPAN border router and RPL root node**.
- **CoAP (Constrained Application Protocol, IETF CoRE):** RESTful request/response over UDP with 4-byte base header; options for URI-Path, Observe (server push), block-wise transfer. In Padova the nodes did *not* run CoAP; the gateway acted as sink and terminated CoAP toward the backend.
- **EXI (Efficient XML Interchange):** binary encoding of XML with schema knowledge; dramatically reduces payload vs. text XML for constrained links.
- **Proxy pattern:** an HTTP–CoAP proxy instance sits in front of backend servers, enabling "control of multiple gateways by using a single proxy instance."
- **Service specification table (Table I):** each candidate service is specified by *network type(s), traffic rate, tolerable delay, energy source, feasibility*. Example: structural health monitoring — 802.15.4/WiFi/Ethernet, 1 packet every 10 min per device, tolerable delay 30 min for data / **10 seconds for alarms**, battery or energy harvester. This delay-bounded service taxonomy is a distinctive architectural contribution.

## (d) Dataset / testbed / deployment — Padova Smart City (PSC)
- **Location:** Padova (Padua), Italy; proof-of-concept "IoT island" with the city municipality; project timeframe Feb 2014 + 15 months (HIT/University of Padova + Comune di Padova).
- **Scale:** **8 battery-powered sensor nodes (S01–S08) + 1 mains/DC-powered benzene node + 1 WSN gateway** (gateway located inside the switchboard box controlling monitored streetlights; low-voltage DC socket available there). Comparative table in later literature lists PSC as "1 EN, 8 EP."
- **Sensors per node:** photometer (lamp light intensity), temperature, humidity; the special node adds benzene (C6H6) air-quality sensing.
- **Node casing:** transparent plastic shield protecting electronics while permitting air and light circulation.
- **Sampling/reporting scheme (from Zanella's own seminar deck):** each node reads sensors every **5 minutes**; average of 3 readings buffered; one average value every **15 minutes**; a packet carries **7 averaged values × 4 sensors**; one full packet transmitted every **7 × 15 = 105 minutes** to the gateway. This aggressive duty-cycling is the key energy strategy for battery nodes.
- **Backend:** optical-fiber connection to central backend servers; database server co-located in the WSN gateway (plug-and-play module).
- **Data examples published:** temperature, humidity, light, benzene time series with diurnal patterns (benzene decreases at night due to lighter traffic; light saturates in daytime).
- **Related scale reference cited in the paper:** the authors' experimental WSN testbed with **more than 300 nodes**.

## (e) Quantitative results
- PSC is deliberately small (9 sensor nodes) — the paper's quantitative content is architectural rather than benchmark-style:
  - Service delay budgets: **30 min for data, 10 s for alarms** (structural health).
  - Traffic rates: **1 pkt / 10 min / device** for several services.
  - Reporting interval: full packet every **105 minutes** (energy savings).
  - The paper reports **top-100 most-downloaded IEEE Xplore papers May–Dec 2014** and ~5,800+ citations (now ~6,400 on OpenAlex), indicating field-shaping impact.
- Data figures demonstrate successful end-to-end collection: temperature/humidity/light/benzene traces over multiple days from the deployed nodes.

## (f) Limitations
1. **Very small deployment** (8+1 nodes) — not a city-scale demonstration; coverage limited to one streetlight cluster.
2. **Single gateway** — no redundancy; gateway failure partitions the entire island.
3. Nodes did not run CoAP — the constrained stack was not fully exercised end-to-end (gateway acted as sink), so the promised EXI/CoAP/6LoWPAN vertical was only partially validated.
4. **No formal security analysis** — authentication, encryption, and key management for the urban IoT are not treated in depth.
5. **Static architecture** — no support for node mobility, edge analytics, or digital-twin feedback loops (predates those paradigms).
6. Latency budgets (30 min) reflect 2014-era expectations; modern autonomous/vehicular services need sub-second guarantees the architecture cannot provide.
7. Interoperability is handled by protocol translation at gateways, not by semantic standards (no ontology/SAREF layer).

---

# 2. Gubbi, Buyya, Marusic, Palaniswami (2013) — "Internet of Things (IoT): A vision, architectural elements, and future directions," Future Generation Computer Systems 29(7):1645–1660, DOI 10.1016/j.future.2013.01.010

## (a) Problem formulation
Three components must converge for IoT: (1) sensing devices, (2) software architectures and pervasive communication networks to convey contextual information where relevant, (3) application development frameworks. The paper asks how to realize a *worldwide*, cloud-centric IoT that is user-centric rather than thrust upon users, supporting data ownership, security, privacy and sharing. Explicit tension: **Internet-centric vs. Thing-centric** architectures — "The Internet centric architecture will involve internet services being the main focus while data is contributed by the objects. In the object centric architecture the smart objects take the center stage. In our work, we develop an Internet centric approach."

## (b) System architecture / layers
**Conceptual IoT framework with Cloud Computing at the center (Fig. 4):**
1. **Smart things / enabling technologies layer** — RFID (EPCglobal), smart sensors, communication technologies (WSN, mobile networks, Internet protocols), smart environments.
2. **Network/communication layer** — ubiquitous communication networks conveying contextual information.
3. **Cloud-centric middleware layer** — data storage, management, analytics; public/private cloud interaction.
4. **Application layer** — personalized, context-aware applications across domains.

**Application domains redefined by scale (Fig. 1):** Personal & Home IoT (individual/home scale) → Community IoT → Industrial IoT → Urban/City IoT → Global IoT — a *scale-based* taxonomy rather than the traditional sector-based one.

**Cloud platform components (Table 3, Microsoft Azure as reference):** compute, storage, data management, messaging/service bus. **Aneka** (University of Melbourne PaaS) sits on Azure providing: multiple programming models (**Task, Thread, MapReduce**), runtime execution services, workload management, resource provisioning. Aneka "can launch any number of instances on the Azure cloud to run their applications… essentially, it provides the provisioning infrastructure."

**Schematic (Fig. 7):** SaaS data-analytics application = IoT data → Aneka/Azure → analytics → results back to user.

## (c) Algorithms / protocol details
- No novel protocol; the contribution is an **architectural pattern**: Internet-centric + Cloud-centric + user-centric.
- **Aneka/Azure interaction:** application code written against Aneka's Task/Thread/MapReduce abstractions is deployed as worker roles on Azure; data-analytics pipeline (system context diagram, Fig. 8) ingests sensor streams, runs distributed analytics, returns results.
- Convergence thesis: WSN + Internet + distributed computing must converge; the cloud is the rendezvous point.
- Emphasis on **data-on-demand using sophisticated intuitive queries** as workloads scale.

## (d) Dataset / testbed / deployment
- **Case study:** IoT sensor-data analytics SaaS built on **Aneka + Microsoft Azure** — a cloud testbed rather than a physical city deployment. No city, no node counts are reported; the evaluation is architectural/illustrative.
- The paper is conceptual-visionary; domains listed include smart homes, healthcare, environmental monitoring, logistics, but no instrumented pilots are described in this paper.

## (e) Quantitative results
- Essentially **no quantitative benchmarks** (this is a vision paper). Quantitative content is limited to market projections (e.g., RFID/IoT market-share projections referenced from industry reports) and structural counts of architectural components (3 core components; 4 Azure components; 3 Aneka programming models).
- Citation impact: ~10,600+ citations — one of the most-cited IoT vision papers.

## (f) Limitations
1. **No empirical validation** — cloud case study is illustrative, with no latency/throughput/accuracy numbers.
2. **Internet-centric bias** — explicitly subordinates "thing" intelligence; criticized later for underplaying edge/fog computing (a gap Shi et al. 2016 later fills).
3. **Security/privacy left as open challenge** — no concrete mechanisms (no TLS profiles, no identity architecture).
4. **Interoperability unspecified** — no semantic layer, no standards mapping (MQTT/CoAP not compared).
5. **Single-vendor lock-in risk** — Azure/Aneka-centric illustration; the "open architecture" claim is not backed by multi-cloud evidence.
6. Predictive analytics, real-time constraints, and latency budgets for control loops are absent.

---

# 3. Al-Fuqaha, Guizani, Mohammadi, Aledhari, Ayyash (2015) — "Internet of Things: A Survey on Enabling Technologies, Protocols, and Applications," IEEE Communications Surveys & Tutorials 17(4):2347–2376, DOI 10.1109/COMST.2015.2444095

## (a) Problem formulation
IoT enables "billions or trillions of heterogeneous objects" interconnected through the Internet. The basic premise: smart sensors collaborate directly without human involvement. The survey's stated objective (vs. prior surveys): "provide a more thorough summary of the most relevant protocols and application issues to enable researchers and application developers to get up to speed quickly on how the different protocols fit together… without having to go through RFCs." Core problem: **protocol fragmentation** — no single protocol covers M2M, M2S, S2S communications with the needed QoS.

## (b) System architecture / layers
**IoT architecture stack (Fig. 3 of the paper), bottom-up:**
- **Physical/Device Layer:** IEEE 802.15.4, Z-Wave, EPCglobal (RFID), LTE-A.
- **Network Layer:** IPv4/IPv6, **6LoWPAN** (adaptation), **RPL** (routing).
- **Application Layer:** HTTP/REST, CoAP, MQTT, MQTT-SN, AMQP, XMPP, DDS.
- **Service Discovery:** mDNS, DNS-SD.
- **Infrastructure/Influential protocols:** IEEE 1888.3, IPSec, IEEE 1905.1.
- **IoT Gateway** as the vertical integration point between constrained devices and Internet services.

Protocol taxonomy into **four categories:** (1) application protocols, (2) service discovery protocols, (3) infrastructure protocols, (4) routing/network protocols.

**Standardization bodies (Table III):** W3C, IETF (CoRE, 6LoWPAN, roll), EPCglobal, IEEE, ETSI.

## (c) Algorithms / protocol details — the MQTT vs CoAP vs XMPP vs AMQP vs DDS comparison
| Protocol | Model | Transport | QoS | Security | Min header | Notes |
|---|---|---|---|---|---|---|
| **CoAP** | Request/Response (+Observe pub-sub) | **UDP** | 2 levels: Confirmable / Non-confirmable (plus piggy-backed ACK, RST) | **DTLS** | **4 bytes** | IETF CoRE; designed for constrained nodes; block-wise transfer; RFC 7252 (2014) |
| **MQTT** | Publish/Subscribe via broker | **TCP** | **3 levels:** QoS0 at-most-once, QoS1 at-least-once, QoS2 exactly-once | TLS/SSL | **2 bytes** fixed header | OASIS standard 2013; DUP flag for duplicates; topic-based routing; keep-alive |
| **AMQP** | Publish/Subscribe, message queue | **TCP** | 3 levels (0/1/2) | TLS/SSL | **8 bytes** | 2003 (JPMorgan); durable queues, transactions, acknowledgment; heavier |
| **XMPP** | Client/Server XML streams + pub-sub XEPs | **TCP** | **None** (no QoS guarantees) | TLS/SASL | Undefined/variable (XML overhead) | IETF RFC 6120/6121 (2004); XML stanzas; presence; high overhead, unsuited to M2M |
| **DDS** | **Broker-less** publish/subscribe, multicast | Reliability over UDP/TCP | **23 QoS policies** (reliability, durability, liveliness, deadline, latency budget, ownership, redundancy, filtering…) | varies | implementation-dependent | OMG; excellent real-time QoS; multicasting; suits industrial M2M |
| HTTP/REST | Request/Response | TCP | none (app-level) | TLS | ~700–800 bytes typical request header | Not IoT-native |

**Key technical findings reported:**
- CoAP vs MQTT under packet loss: **when packet-loss rate is high, CoAP outperforms MQTT**; for small messages and loss **< 25%**, CoAP generates less extra traffic.
- CoAP vs MQTT on smartphones: CoAP has **smaller bandwidth usage and round-trip time**.
- CoAP vs HTTP: condensed header → lower transmission time and energy.
- **Service discovery:** mDNS + DNS-SD for self-configuration of resource registration/discovery.
- **IoT gateway** role: protocol translation, edge filtering, security enforcement.

**Standardized header sizes (Table IV, last column = minimum header):** MQTT 2 B, CoAP 4 B, AMQP 8 B, HTTP large, XMPP unbounded XML.

## (d) Dataset / testbed / deployment
Survey paper — no own deployment. It synthesizes literature evaluations (e.g., smartphone testbeds comparing CoAP/MQTT, ns-2/3 simulations) and presents **service use-cases** showing protocol stacking (e.g., a smart-home use-case combining CoAP on constrained links, MQTT to broker, AMQP to enterprise backend).

## (e) Quantitative results
- Header sizes: MQTT 2 B, CoAP 4 B, AMQP 8 B (vs HTTP ~700–800 B typical).
- Loss threshold: CoAP advantageous below **25% packet loss** for small messages.
- QoS levels: MQTT/AMQP = 3; CoAP = 2; DDS = 23 policies; XMPP = 0.
- Projected IoT market shares for dominant applications by 2025 (Fig. 2) — industry-sourced.
- The paper has **~7,300+ IEEE citations / ~10,400 total** — canonical protocol taxonomy reference.

## (f) Limitations
1. **No unified benchmark** — performance claims are cited from heterogeneous studies (different hardware, loss models), not re-measured.
2. **XMPP's lack of QoS** and DDS's broker-less design make the comparison axis (QoS) uneven.
3. **Security comparison is shallow** — DTLS vs TLS listed but no cipher suites, no key-management procedures, no PQC considerations.
4. **No latency/throughput numbers** in the survey itself (only qualitative "smaller bandwidth/RTT").
5. Horizontal integration across protocols is identified as a problem but the proposed fix (intelligent gateway) does not resolve root-cause QoS fragmentation (acknowledged in their follow-up 2015 IEEE ComMag paper).
6. Predates MQTT 5.0, CoAP OSCORE/Observe-draft finalization, HTTP/3/QUIC, and LwM2M deep coverage.

---

# 4. Akyildiz, Su, Sankarasubramaniam, Cayirci (2002) — "Wireless sensor networks: a survey," Computer Networks 38(4):393–422, DOI 10.1016/S1389-1286(01)00302-4 (plus companion IEEE ComMag "A Survey on Sensor Networks," 2002)

## (a) Problem formulation
Convergence of MEMS, wireless communications and digital electronics made low-cost sensor networks viable. The survey addresses: sensing tasks/applications, **factors influencing design**, the **communication architecture**, and per-layer algorithms/protocols. The distinguishing problem vs. MANETs: sensor nodes are power-constrained, densely deployed, application-aware, and often immobile; "power efficiency directly influences network lifetime… and hence is of prime importance"; "none of the existing Bluetooth or MANET MAC protocols can be directly used."

## (b) System architecture / layers
**Communication architecture:** sensor nodes scattered in a **sensor field**; each node collects data and routes it back to a **sink (base station)**, which connects to the Internet/task manager via satellite/internet for the end user. Node components: sensing unit (sensor + ADC), processing unit (CPU + memory), transceiver unit (radio), power unit (battery, **< 0.5 Ah, 1.2 V**), and optionally application-specific (location-finding, power generator).

**Five-layer protocol stack surveyed:**
1. **Physical layer** — modulation, spreading, channel coding; design factors: energy consumption vs. bit error rate, shared vs. dedicated channels.
2. **Data link layer (MAC)** — duty-cycling, framing, error control; fixed-allocation vs. random access.
3. **Network layer (routing)** — data-centric, hierarchical, location-based, QoS-based.
4. **Transport layer** — congestion control, reliability (especially for sink-source links).
5. **Application layer** — task management, query/discovery, localization.

**Eight design factors (Section 3):** fault tolerance, scalability, production costs, operating environment, sensor network topology, hardware constraints, transmission media, **power consumption**.

## (c) Algorithms / protocol details — routing taxonomy + lifetime models
**Network-layer taxonomy (Table 2 of the survey):**
- **Flat/network protocols:** SPIN (Sensor Protocols for Information via Negotiation) — three message types **ADV, REQ, DATA**; meta-data negotiation avoids redundant transmission; rumor routing; EAR (Energy-Aware Routing); MCFA.
- **Hierarchical:** **LEACH** (Low-Energy Adaptive Clustering Hierarchy) — forms clusters with rotating cluster-heads to minimize energy dissipation; steady phase → setup phase rounds of cluster-head selection. PEGASIS, TEEN/APTEEN (threshold-sensitive).
- **Location-based:** GAF (Geographical Adaptive Fidelity), GEAR, TBF, MSR.
- **QoS-based / data-centric:** **Directed Diffusion**, SAR (Sequential Assignment Routing), SMECN, ReInForM.

**Directed diffusion mechanics (the survey's flagship example):**
1. Sink broadcasts an **interest** (task description: attribute, duration, timestamp, interval).
2. Nodes set up **gradients** (one per neighbor, with data rate/duration fields) pointing back toward the sink during interest propagation.
3. Data flows along gradients toward the sink; **in-network aggregation, caching and processing** on the way; sink reinforces a path when multiple data arrive.
- Fully **data-centric**: "all communication is for named data"; nodes are application-aware.
- Illustrative route metric (Fig. 4): Route 1 Sink-A-B-T total P_A=4, α=3; Route 2 Sink-A-B-C-T P_A=6, α=6; Route 3 Sink-D-T P_A=3, α=4 — energy vs. delay trade-off (α = delay/hops, P_A = path energy).

**Network lifetime formalism:**
- Node lifetime depends on battery (**<0.5 Ah, 1.2 V**), replenishment often impossible.
- Lifetime metrics used in the literature (surveyed): *time to first node death*, *time to 50% node death*, *connected coverage duration*, *total data delivered to sink*, *average energy per delivered bit*.
- Related quantitative results from the surveyed literature (worth carrying forward):
  - **LEACH reduces energy dissipation by a factor of ~7 vs. direct communication, and 4–8× vs. minimum-transmission-energy routing** (Heinzelman et al., cited).
  - **EAR-type single-path random selection: 21.5% energy saving and 44% network lifetime increase vs. Directed Diffusion** (Shah & Rabaey, cited).
  - MSDD (modified diffusion) achieves **up to 2× network lifetime** vs. Directed Diffusion by reducing routing overhead.
  - REER-1 improves energy consumption **7%–39%** vs. Directed Diffusion.
  - GAF increases lifetime while matching ad-hoc routing latency/packet loss.

**MAC techniques:** duty-cycling (nodes enter reduced-activity periods), contention-based (B-MAC-style preamble sampling implied), fixed allocation impractical without central control → network-wide synchronization difficult.

## (d) Dataset / testbed / deployment
Survey paper — no own deployment. It consolidates schemes from the literature (SPIN, LEACH, Directed diffusion, SAR, SMECN, GAF) evaluated mostly in **ns-2 simulations** and small indoor testbeds of the era. Applications enumerated: temperature, humidity, vehicular movement, lightning, pressure, soil makeup, noise, object presence, mechanical stress, speed/direction; military target tracking, environmental/habitat monitoring, health, home automation.

## (e) Quantitative results
- Battery: **<0.5 Ah @ 1.2 V** typical node power source.
- LEACH: **7× energy reduction vs direct TX; 4–8× vs min-energy routing**.
- EAR vs Directed Diffusion: **21.5% energy saving, 44% lifetime increase**.
- MSDD: **up to 2× lifetime**; REER-1: **7–39% energy improvement**.
- Protocol comparison table (SPIN vs LEACH vs Directed Diffusion): Optimal route: No/No/**Yes**; Network lifetime: Good/**Very good**/Good; Resource awareness: Yes/Yes/Yes; Meta-data use: Yes/No/**Yes**.
- Battery lifetime constraint drives the entire design space (no numeric lifetime formula is given *in this survey*; lifetime models are referenced from Bhardwaj/Chandrakasan upper-bound work).

## (f) Limitations
1. **Pre-dates IPv6/6LoWPAN, BLE, LoRa, energy harvesting** — the stack is 802.15.4-era.
2. **No explicit closed-form lifetime equation** — lifetime is treated qualitatively; formal bounds (e.g., T = E_total / P_node, max-flow min-cut bounds) are deferred to references.
3. **Security not covered** — no crypto, no Sybil/DoS analysis for sensor nets (later became a huge topic).
4. **Mobility largely excluded** (assumes static nodes; MANET comparison only).
5. **Scalability claims untested** at 2002-era scale (tens–hundreds of nodes in sims); no city-scale evidence.
6. Transport-layer section acknowledges congestion/reliability as open issues without strong solutions.
7. Directed Diffusion is query-driven — poor fit for continuous streaming/alarms (acknowledged).

---

# 5. Shi, Cao, Zhang, Li, Xu (2016) — "Edge Computing: Vision and Challenges," IEEE Internet of Things Journal 3(5):637–646, DOI 10.1109/JIOT.2016.2579198

## (a) Problem formulation
IoT proliferation + rich cloud services pushed a new paradigm: **process data at the edge of the network**. Edge computing addresses four concerns: **(1) response-time/latency, (2) battery-life constraints of devices, (3) bandwidth cost, (4) data safety and privacy.** Formalized motivation: data volume grows (citing Domo "Data Never Sleeps": ~2.5 quintillion bytes/day era); sending everything to the cloud is infeasible for latency-sensitive, bandwidth-heavy, privacy-sensitive workloads.

## (b) System architecture / layers
**Edge computing definition (paraphrased):** bring computation, storage, and services from the core cloud to the edge of the network, close to data sources.

**Smart-city-relevant layered topology (from case studies):**
1. **Things/end devices** — sensors, phones, cameras, vehicles.
2. **Edge devices / gateways (home server, building server)** — local processing, filtering, preprocessing (e.g., photo preprocessing before upload).
3. **City data center layer** — city-scale edge; heavier workloads with energy constraints; latency higher than building server but lower than remote cloud.
4. **Cloud layer** — global aggregation, long-term storage, heavy analytics.

**Cross-layer modules (challenge section):** Programming models, Naming (cross-layer), Data abstraction, Service management, Privacy & Security, Optimization metrics (latency, bandwidth, energy, cost).

**Collaborative edge:** edge nodes connect end users and cloud both physically and logically; "workload should be finished in the nearest layer which has enough computation capability."

## (c) Algorithms / protocol details
No single algorithm; the paper defines **decision criteria**:
- **Offloading decision:** prefer edge only if *transmission overhead < local computing overhead*. Influencing factors: workload's computation intensity, local resource footprint, **network signal strength**, data size, available bandwidth.
- **Energy trade-off:** balance computation energy vs. transmission energy (E_compute vs E_transmit).
- **Data-reduction strategy:** pre-process photos at edge to shrink payload → saves user data plans and global bandwidth usable by other edges.
- **Collaborative-edge example (connected healthcare / flu outbreak):** patients flow to hospitals; EMR updated at edge; hospital aggregates average cost, symptoms, population; federation across hospitals without raw-data egress — privacy-preserving collaboration.
- References **OpenFog Architecture** (2016) as the emerging reference architecture.

## (d) Dataset / testbed / deployment
Vision/case-study paper — **no own testbed**. Cases: (A) cloud offloading, (B) smart home (edgeOS aggregating all household things), (C) smart city (city data center layer), (D) collaborative edge (connected healthcare flu-outbreak scenario). Quantitative claims are derived from cited industry data (Domo data-growth stats, Intel IoT Gateway whitepaper, AT&T IoT whitepaper).

## (e) Quantitative results
- **Smart city data volume:** "A city populated by 1 million people will produce..." (the paper's famous figure: ~**1 million people → large data quantity** motivating edge; often cited as "1M people city produces huge daily data" — the exact Domo-scaled figure referenced).
- Latency rationale: edge reduces latency because data "does not have to traverse over a network to a data center"; **millisecond latencies untenable** for financial services/manufacturing if sent to cloud (no precise ms benchmark table in this paper — it is qualitative here).
- Layered latency ordering implied: **edge/gateway < city data center < remote cloud** (energy limitation at city DC "inevitably affects the latency").
- Citation impact: ~7,800+ IEEE citations — foundational edge-computing vision paper.

## (f) Limitations
1. **No experimental evaluation** — no measured latency/throughput/energy numbers; the four benefits are argued, not benchmarked.
2. **No formal offloading model** — the E_transmit < E_compute inequality is stated but not parameterized (no equations with concrete radio models).
3. **Security/privacy named but not solved** — no threat model, no confidential-compute mechanism.
4. **Naming/data abstraction left as open challenges.**
5. Pre-dates MEC/ETSI standardization, serverless edge, and Kubernetes-at-edge — no operational stack detail.
6. Collaborative-edge healthcare example lacks quantitative privacy/accuracy analysis.

---

# 6. Lee (2008) — "Cyber-Physical Systems: Design Challenges," UC Berkeley UCB/EECS-2008-8 / ISORC 2008 invited paper, DOI 10.1109/ISORC.2008.25

## (a) Problem formulation
CPS = "integrations of computation with physical processes. Embedded computers and networks monitor and control the physical processes, usually with **feedback loops** where physical processes affect computations and vice versa." The paper asks whether **today's computing and networking technologies provide an adequate foundation for CPS**, and concludes: improving design processes, raising abstraction levels, or verifying designs built on today's abstractions **will not be sufficient** — "we will have to rebuild computing and networking abstractions. These abstractions will have to embrace physical dynamics and computation in a unified way." Physical components introduce **safety and reliability requirements qualitatively different** from general-purpose computing.

## (b) System architecture / abstractions & timing/feedback formalism
**CPS structural formalism:**
- **Feedback loop:** physical process → sensors → computation → actuators → physical process. Physical dynamics and computation are coupled; "physical processes affect computations and vice versa."
- **Multi-scale, heterogeneous** systems mixing wide ranges of technologies.
- **Concurrency is intrinsic:** "Physical processes are intrinsically concurrent, and their coupling with computing requires, at a minimum, concurrent composition."
- **Time is inexorable:** "In the physical world, the passage of time is inexorable… Neither of these properties [time, concurrency] is present in today's computing and networking abstractions."

**Critique of prevailing abstractions:**
- Core abstraction of computing = "a terminating sequence of state transformations" (method calls, threads). "This core abstraction underlies the design of nearly all computers, programming languages, and operating systems in use today. But unfortunately, this core abstraction may not fit CPS very well."
- "Standard abstractions based on method calls and threads do not work."
- Software artifacts (locks, priority inversion, interrupts) "break the formalisms, forcing designers to rely on **bench testing, which rarely identifies subtle timing bugs**."
- Networking introduces "a great deal of timing variability and stochastic" behavior; timing must be a **semantic property**, not a QoS after-thought (extended argument in his 2009 Time-Critical Networking abstract).

**Key quotable formal commitments:**
- "No cyber-physical system that depends on timeliness can be deployed without timing assurances. **If Turing completeness interferes with this, then Turing completeness must be sacrificed.**"
- Correct execution in C/Java/Haskell "has nothing to do with how long it takes to do anything"; program timing is non-repeatable except at coarse granularity; programmers must step outside abstractions to specify timing.
- Repeatable temporal dynamics: electronics deliver highly precise timing (e.g., **20.000 MHz ± 100 ppm**) but overlaying software abstractions discard it.
- Proposed direction: **architectures with repeatable timing** (PRET), time-triggered architecture (Kopetz & Bauer cited), Ptolemy II-style heterogeneous concurrent models of computation (MoCs) unifying discrete events, continuous time, dataflow.

## (c) Algorithms / protocol details
Not an algorithmic paper. Technical content = **abstraction-level requirements**:
- Unified modeling of dynamics (ODEs/DAEs/PDEs), time, and concurrency.
- Timing assurances at every abstraction layer ("Timing cannot be effectively introduced at 'higher levels of abstraction' if it is entirely absent from the lower levels").
- Network semantics where time is part of the message contract (later embodied in TSN/IEEE 1588/time-sensitive networking and 5G URLLC).
- Safety/reliability requirements derived from physics (not just software fault models).

## (d) Dataset / testbed / deployment
None — position/design-challenges paper (ISORC 2008 invited; NSF CNS-0647591 and CNS-0720841 funded). Illustrative systems referenced (KUKA robotics, distributed micro-power generation into the power grid, networked control systems) but not instrumented in this paper.

## (e) Quantitative results
- Quantitative content is illustrative: **20 MHz ± 100 ppm** clock example; contrast with software timing non-determinism.
- No latency/accuracy benchmarks. Impact metric: foundational CPS citation (thousands of citations) defining the "CPS design challenges" agenda.

## (f) Limitations
1. **No constructive solution** — diagnoses that abstractions must be rebuilt but offers no complete replacement semantics (Ptolemy/PRET are directions, not delivered artifacts here).
2. **No quantitative timing model** (no jitter/deadline equations in this paper).
3. Security, privacy, and human-in-the-loop aspects absent.
4. Networked-control stability analysis (Lyapunov, small-gain) is referenced only tangentially — control theory side under-developed relative to software-abstraction side.
5. Written pre-ISO 26262/IEC 61508 updates and pre-5G URLLC — regulatory and standards mapping missing.

---

# 7. Kitchin (2014) — "The real-time city? Big data and smart urbanism," GeoJournal 79(1):1–14, DOI 10.1007/s10708-013-9516-8

## (a) Problem formulation
"Smart cities" describes cities increasingly composed of and monitored by pervasive/ubiquitous computing, whose economy/governance is driven by innovation. This paper focuses on the **instrumentation** side: cities are being instrumented with digital devices and infrastructure producing "big data," which advocates claim enables **real-time analysis of city life**, new modes of urban governance, and material for "efficient, sustainable, competitive, productive, open and transparent cities." Kitchin's problem: these claims rest on "weak, selective evidence and political ideology"; the paper provides a **critical reflection** with five concerns.

## (b) System architecture (conceptual, not technical)
The paper's implicit architecture of the real-time city:
1. **Instrumentation layer** — pervasive sensors, cameras, RFID, smart meters, transactional data, social media, open data portals, city dashboards (e.g., CASA's **London City Dashboard**, citydashboard.org/london).
2. **Data layer** — "big urban data": exhaustive, diverse, inter-linked datasets; data "always already cooked" (Gitelman & Jackson: "raw data is an oxymoron").
3. **Analytics/algorithms layer** — algorithmic processing producing evidence for governance.
4. **Governance/actuation layer** — real-time regulation, planning, service delivery, evidence-based policy.

## (c) The five concerns (the paper's core "algorithm")
1. **The politics of big urban data** — data portrayed as benign, neutral, pre-analytic; but data are products of choices/constraints shaped by systems of thought, technical know-how, public/political opinion, ethics, regulation. "Data are always already cooked and never entirely raw." Sensors/cameras do have politics.
2. **Technocratic governance and city development** — algorithmic, evidence-based approaches appear rational/impartial and give managers a defense: **"It's not me, it's the data!"** (Haque 2012). But technocratic governance is "highly narrow in scope and reductionist and functionalist," based on a limited set of metrics; provides "weak, selective evidence and political ideology."
3. **Corporatisation of city governance and technological lock-ins** — vendor platforms embed corporate interests; risks of **technological lock-in**, vendor dependence, market-driven urbanism; partnerships between analytics firms and city authorities.
4. **Buggy, brittle and hackable cities** — system vulnerabilities, failure modes; interconnected datasets + automation produce brittleness; cybersecurity, data quality, fidelity, security, validity of analytics using **data-dredging** techniques; "how data are interpreted and acted upon."
5. **The panoptic city** — surveillance, **dataveillance**, and control; "a world in which all aspects of a citizen's life are captured and potentially never forgotten" (Dodge & Kitchin 2007b, referencing superpanopticon/synopticon); ethical issues with constant monitoring.

## (d) Dataset / examples used
Illustrative city dashboards and big-data urbanism projects: **CASA London City Dashboard**; various real-time city projects surveyed; EU 20-20-20 framing; no original dataset. Method: critical synthesis of examples.

## (e) Quantitative results
No technical metrics (this is a social-science critique). Quantitative content: five named concerns; journal metrics (~2,500+ citations, 58k accesses). The "five concerns" list itself is the deliverable used by later smart-city governance literature.

## (f) Limitations
1. **Not a technical architecture paper** — no latency, throughput, or system design content; must be paired with engineering sources for full stack view.
2. **Examples are Western/EU-centric** (London focus); limited treatment of Global South instrumentation.
3. Written pre-generative-AI and pre-LLM-driven urban analytics — "data dredging" critique has intensified but the paper's framework must be extended to foundation-model governance.
4. Offers no constructive governance architecture (no PETs, no data-trust mechanisms specified).
5. Five concerns overlap (lock-in vs. corporatisation vs. panopticon are entangled), which weakens falsifiability.

---

# 8. Blockchain for Smart Cities — Xie et al. (2019) + IOTA / Ethereum / Hyperledger

## 8.1 Xie, Tang, Huang, Yu, Xie, Liu, Liu (2019) — "A Survey of Blockchain Technology Applied to Smart Cities: Research Issues and Challenges," IEEE Communications Surveys & Tutorials 21(3):2794–2830, DOI 10.1109/COMST.2019.2899617

### (a) Problem formulation
Rapid urbanization causes economic/social/environmental problems. Smart cities aim to use public resources optimally and provide high-quality services. **Blockchain features** — trust-free (trustless), transparency, pseudonymity, democracy, automation, decentralization, security — are claimed to improve smart-city services. Problem: survey how blockchain is applied across smart-city domains and what challenges remain.

### (b) Architecture / coverage structure
Survey organizes blockchain-in-smart-city by domain:
1. **Smart citizen** (identity, e-voting, public records)
2. **Smart healthcare** (EMR sharing, consent, audit)
3. **Smart grid** (P2P energy trading, DER integration, demand response)
4. **Smart transportation** (vehicle identity, tolling, MaaS payments, platooning data)
5. **Supply chain management**
6. **Others** (public safety, governance, education)

Background section covers blockchain fundamentals: distributed ledger, blocks, **consensus mechanisms (PoW, PoS, PBFT-family, DPoS)**, smart contracts, cryptographic hash chains, Merkle trees.

### (c) Consensus / protocol details (as covered in survey + platform specifics)
- **PoW (Bitcoin/Ethereum legacy):** energy-intensive, ~10s block time, low throughput (~7–15 tx/s), public.
- **PoS:** lower energy; finality/fork concerns noted in related literature.
- **PBFT / RAFT / IBFT:** permissioned, finality, suitable for enterprise consortia.
- **Ethereum:** general-purpose smart contracts (Solidity), public or private (Quorum); used for P2P energy trading pilots.
- **Hyperledger Fabric:** permissioned, **execute-order-validate** architecture, channels for privacy, pluggable consensus (Kafka/Raft), chaincode; preferred for enterprise smart-city transport/healthcare (v2.5 cited in later work for scalability + privacy).
- **IOTA Tangle (DAG):** see 8.2.

### (d) Datasets / pilots referenced
The survey synthesizes literature pilots (no own testbed). Concrete platform pilots outside the survey (for city energy/transport):
- **PowerLedger** (Solana, Australia) — local energy trading.
- **IOTA + TronderEnegi/Enexis** — smart energy PoC (Trondheim); IOTA Foundation >100 staff, 25+ countries (July 2019).
- **+CityxChange** EU project: 7 European cities (Trondheim, Limerick, Alba Iulia, Písek, Sestao, Smolyan, Võru) — IOTA-enabled decentralized energy marketplace + e-mobility-as-a-service; positive energy districts.
- **Taipei City Government × IOTA MOU (2018)** — blockchain sightseeing application.
- **Seoul** — blockchain in public transportation; **Dubai** — blockchain ambitions for smart transport.
- **Hyperledger Fabric v2.5** selected for MaaS platforms (2025 study) for privacy/scalability vs Ethereum/R3 Corda.

### (e) Quantitative results
- Survey scale: IEEE COMST 37 pages (2794–2830); **~668–765 IEEE citations** (OpenAlex 765).
- Platform survey of blockchain-for-energy papers (2021–2023 review): **Custom consensus 73, Ethereum 38, Hyperledger 29, Cosmos 4, IOTA Tangle 2, Avalanche 2, Energy Web Chain 2, Quorum 2** — showing custom/Ethereum/Hyperledger dominance.
- Bitcoin/Ethereum PoW throughput ceiling ~7–15 tx/s (vs Fabric/Hyperledger hundreds–thousands tx/s in permissioned mode — cited in comparisons).
- +CityxChange: 7 cities, 9 SMEs, 3 NPOs, 2 universities, budget group + ARUP + Statkraft.

### (f) Limitations (Xie et al.)
1. **Scalability** of public chains insufficient for city-scale IoT message rates.
2. **Latency/finality** of PoW unsuitable for real-time control.
3. **Energy consumption** of PoW conflicts with smart-city sustainability goals.
4. **Privacy vs transparency** tension — pseudonymity insufficient for GDPR (right to be forgotten vs immutability).
5. **Interoperability** across heterogeneous city chains/ledgers unsolved.
6. **Governance/legal** — smart-contract enforceability, liability, standards immature.
7. Survey is literature-based: few deployments have published rigorous KPIs.

## 8.2 IOTA Tangle — technical mechanics (city energy/transport relevance)
- **Data structure:** DAG (directed acyclic graph), not linear chain; each new transaction **approves two previous unapproved tips**.
- **Consensus:** nodes add transactions autonomously; confirmation = reachability: "If a transaction is reachable from all tips, it's considered confirmed. If there are 100 open tips and a transaction is reachable only from 80 of them, it's considered 80% confirmed."
- **No miners, no transaction fees** (vs Bitcoin/Ethereum) — designed for M2M micropayments and data sharing at IoT scale.
- **PoW** retained lightly (spam protection), not mining-based consensus.
- **IOTA Smart Contract Protocol (ISCP):** layered above Tangle for conditional payments in P2P energy trading; evaluated vs traditional blockchain: **"only a fraction of the cost"** of conventional DLT for P2P energy trading (arXiv 2210.06427) with speed and energy-efficiency benefits.
- **Proposed smart-city network architecture (3 layers):** outer layer = small client devices; middle layer = gateways/aggregators; inner layer = core network + Tangle nodes.
- **City pilots:** Taipei sightseeing; +CityxChange energy districts across 7 EU cities; TronderEnegi/Enexis energy PoC.

## 8.3 Ethereum vs Hyperledger for cities (technical selection criteria)
| Criterion | Ethereum (public/private, Quorum) | Hyperledger Fabric | IOTA Tangle |
|---|---|---|---|
| Permissioning | Public / semi-private | Permissioned (channel isolation) | Public, optional private Tangle |
| Consensus | PoW→PoS (post-Merge) / IBFT in Quorum | Pluggable: Raft, Kafka, BFT | Tip-selection + light PoW (DAG) |
| Smart contracts | Solidity/EVM | Chaincode (Go/Java/Node) | ISCP (smart contracts on Tangle) |
| Throughput | ~15–30 tx/s (public legacy) | Hundreds–thousands tx/s | High (parallel DAG approvals) |
| Fees | Gas fees | None (org-borne) | No fees |
| City fit | P2P energy trading, open records | Transport MaaS, healthcare, supply chain | IoT micropayments, sensor data markets |

**Limitations of the platform layer overall:** energy consumption (PoW era), fork/finality risk (PoS), key management for citizens, oracle problem for real-world data, quantum vulnerability of ECDSA/hash functions, and lack of cross-ledger interoperability for multi-vendor cities.

---

# 9. Digital Twins — Peldon et al. (2024) & Weil et al. (2023)

## 9.1 Peldon, Banihashemi, LeNguyen, Derrible (2024) — "Navigating urban complexity: The transformative role of digital twins in smart city development," Sustainable Cities and Society 111:105583, DOI 10.1016/j.scs.2024.105583

### (a) Problem formulation
Systematically explore DTs within smart cities: develop **DT integration mechanisms**, integrate the urban DT **network and model** with urban planning/design, and identify **technical, policy and application gaps**. Definitions synthesized: "A smart city digital twin is defined here as a cyber component that mirrors the physical urban system through **real-time monitoring and synchronization** of urban activities" (Mylonas et al. 2021, p.3).

### (b) Architecture — urban DT layers
**Multi-layered framework "starting from the physical reality and extending into the cyber domain through various layers of data handling, modelling, integration, and service delivery" (Fig. 4).** Layer counts vary across literature — the paper tabulates (Table 3):
- **Lv et al. (2022):** Physical layer (tangible elements) + Data layer (collection/storage) + … (more layers).
- **White et al. (2021) six-layer model (Fig. 5):** (1) **Terrain**, (2) **Buildings**, (3) **Infrastructure**, (4) **Mobility**, (5) **Digital layer / Smart City** — "central hub for integrating IoT sensors throughout the urban landscape"; collects data for simulation, (6) **Virtual layer / Digital Twin** — advanced simulations, visualization, experimentation, collaborative urban management.
- **Aheleroff et al. (2021) three-layer:** physical, digital, cyber.
- Buildings layer uses **BIM, 3D laser scanning, 3D data**.

**Synchronization taxonomy (Table contrasting representations):**
| Feature | 3D model | BIM | Digital Shadow | Digital Twin |
|---|---|---|---|---|
| Representation | Static | Static + physical info | Static w/ dynamic updates | Dynamic digital-physical |
| Sync direction | None | Manual | Physical → digital only (no reverse) | **Automatic, integrated, both directions** |

### (c) Synchronization methods & tools
- Bidirectional synchronization (physical ↔ virtual), automatic vs manual.
- Tools/products tabulated (Table 4): GIS/BIM platforms, game engines (Unreal/Unity), Cesium, ESRI, FIWARE-based UDT models, CityGML/CityJSON, 3D Tiles.
- Case-study DT uses (Table 6): urban planning simulations, mobility, energy, disaster.

### (d) Datasets / case studies
Systematic review + case examples (Dublin, Helsinki Kalasatama, Rotterdam covered in related literature; Peldon synthesizes DT tools/products tables). No own sensor deployment.

### (e) Quantitative results
- Six-layer White et al. model; three-layer Aheleroff; five-layer Peldon proposal (per 2025 citations: "Peldon et al. (2024) proposed a five-layer architecture").
- Table counts: 3 urban DT layers sources, 4 tool categories, 5 application aspects, 6 case studies.
- Citation: article in SCS 111 (2024) with corrigendum in 132 (2025).

### (f) Limitations
- Layer taxonomies inconsistent across literature (number/function of layers "common consensus… layered" but counts differ).
- Focus on planning/design integration; **real-time control-loop DTs under-treated**.
- Technical gaps: latency of synchronization, fidelity metrics, scalability of city-scale 3D + IoT fusion not quantified.

## 9.2 Weil, Bibri, Longchamp, Alahi, Golay (2023) — "Urban Digital Twin Challenges: A Systematic Review and Perspectives for Sustainable Smart Cities," Sustainable Cities and Society, DOI 10.1016/j.scs.2023.104730 (S2210670723004730)

### (a) Problem formulation
Governance aspects of **city-scale digital twins (CDTs)** understudied; identify challenges hindering design/implementation including social/legal issues often overlooked.

### (b) Architecture / layers & eight challenges
**Eight challenges identified (as summarized in later literature):**
1. **Interoperability** (disparate semantic standards)
2. **Infrastructure requirements**
3. **Data acquisition**
4. **Data quality**
5. **Modelling and decision support**
6. **Data visualization**
7. **Human and capital resources**
8. **Governance issues**

**Lei et al. 2023 companion finding (Automation in Construction 147:104716):** systematic review + Delphi expert survey → **14 technical + 9 non-technical challenges** mapped to DT life-cycle phases; most severe = **interoperability (disparate semantic standards)** and **practical value (lack of business models)**. Technical challenges include semantic standards, scalability; non-technical include business models, legal/social.

### (c) Tools / formats / synchronization methods (from Weil et al.)
- **Exchange formats:** IFC (building), IndoorGML, CityGML/CityJSON (3D city), GeoSPARQL, GeoJson-LD.
- **Streaming/web formats:** **OGC 3D Tiles**, **I3S** (Indexed 3D Scene Layer), 3D GeoVolumes API, KML/COLLADA/glTF tiles.
- **Game engines:** Unreal Engine, Unity + Cesium/ESRI plugins.
- **Semantic/standards:** CityGML 3.0 (2023, OGC 21-006r2) with **Dynamizer Application Domain Extension (ADA)** for dynamic sensor data.
- **Synchronization:** bidirectional model transformations (Visconti et al. 2021: formal bx theory guaranteeing coherent CityGML ↔ analyzable model sync); NGSI-LD context brokers for data plane; manual bindings common.

### (d) Datasets / cases
Systematic review of initiatives; case examples across cities (Dublin open data portal; Helsinki Kalasatama — CityGML over **five levels of detail (LOD)**; Rotterdam). Corpus scale in related reviews: **92 papers** initial corpus (Ketzler-type review), refined set for DT-for-cities classification into **9 categories** by data-integration method.

### (e) Quantitative results
- 8 challenges (Weil); 14 technical + 9 non-technical (Lei Delphi); 5 LODs in Helsinki CityGML; 9 classification categories for DT implementations; 3 directions of information flow in advanced DT designs (human-machine + two digital layers).
- Format-conversion failure metric: CityGML → web streaming conversion causes **semantic data loss** (Padsala et al. 2023 cited).

### (f) Failure modes / limitations (specific)
1. **Semantic data loss** on CityGML → 3D Tiles/I3S conversion — dynamic fields dropped; tiled formats "hold only the digital representation information, ignoring the fields that would support dynamic updates."
2. **Update/synchronization issues:** simulation outputs must be re-processed into tiled formats; batch vs streaming pipelines diverge (Kafka/Spark/Flume/NiFi for streaming IoT vs batch).
3. **Dynamizer ADA under-used:** "most projects sidestep the Dynamizer ADA by managing sensor data in parallel and then fusing it with the city model at the application level" (arXiv 2509.11810) — geometry and data remain **loosely coupled**, "joined only by manual bindings… unsuitable for city-scale simulations."
4. **No coordination across projects** (Helsinki interview): "currently, there is no coordination yet… 3D-models may or may not be a part of the data used."
5. **Governance/legal gaps** — data ownership, liability for twin-driven decisions, GDPR vs immutable logs.
6. **Business model absence** — practical value questioned by Delphi panellists (who are end-users, what demands?).
7. Interoperability across GIS/BIM/CIM still requires schema-based transformations (IFC→CityGML), a manual, lossy art.

---

# 10. 5G/6G for Smart Cities — Murroni et al. (2023) + IMT KPIs, RIS, THz, Network AI

## 10.1 Murroni, Anedda, Fadda, Ruiu, Popescu, Zaharia, Giusto (2023) — "6G—Enabling the New Smart City: A Survey," Sensors 23(17):7528, DOI 10.3390/s23177528

### (a) Problem formulation
Smart cities and 6G can transform work/life, but require "a critical reassessment of the entire wireless communication sector for smart cities," including IoT infrastructure, economic factors, and operational strategies. 5G's "multifaceted role and inherent limitations" within smart cities serve as the foundational standpoint; the survey then maps the 6G standard's application potential to SC arenas.

### (b) Architecture / usage scenarios mapped to city apps
**5G triangle (Table 1 features/benefits):**
| Scenario | Target | City application mapping |
|---|---|---|
| **eMBB** (enhanced Mobile BroadBand) | High data rates (up to **10 Gbps** class; 5G peak **20 Gb/s**, user-experienced **100 Mb/s**, area traffic **10 Mb/s/m²**) | HD/4K/8K video surveillance, AR/VR city services, digital signage, telemedicine imaging |
| **URLLC** (Ultra-Reliable Low-Latency) | **≤1 ms** latency, 99.999% reliability | Autonomous vehicles/V2X, traffic signal control, remote surgery, industrial automation, emergency response |
| **mMTC** (massive Machine-Type Communications) | **10⁶ devices/km²** connectivity, low energy | Environmental sensor grids, smart metering, smart lighting, waste bins, structural health |

**6G vision additions:** higher frequency bands (**THz**), deeper **AI integration** (intelligent network management), **quantum computing** for secure comms/advanced sensing, integration with **satellite networks** (telecom + GPS) to reach connection speeds **up to 11 Gbps**, **nano-antennas** for IoT.

**Driving trends of 6G (ref [79]):**
- Convergence of communications, computing, control, localization and sensing (**3CLS**).
- **Smart reflective surfaces and environments** — RIS on walls/roads/doors/buildings to maintain line-of-sight and quality signal with minimal loss.
- **Massive availability of small data** — shift from centralized big data to massive distributed small data.

### (c) Enabling technologies — RIS, THz, network AI
- **RIS (Reconfigurable Intelligent Surfaces):** programmable metasurfaces controlling phase/amplitude of reflected waves; smart radio environments; enables coverage enhancement in mmWave/THz NLoS.
- **THz frequencies (>100 GHz):** multi-Gbps/Tbps potential; WRC-19 decided bands **above 6 GHz** needed for multi-Gbps.
- **Network AI:** deep learning replacing "existing algorithms for modeling channel information"; AI for network management (AI-for-network) and network-for-AI.
- **Quantum computing:** secure communications (QKD-class) and advanced sensing.
- **ISAC (Integrated Sensing and Communication)**, non-terrestrial networks (NTN), network slicing as SSC key technologies.

**Quantitative RIS/THz results (supporting literature, Scientific Reports 2026):** at **300 GHz** carrier with RIS: NLoS SNR **−20 dB → +45 dB**; packet delay **16.5 ms → ~2 ms**; throughput **~1 Gbps → ~20 Gbps**; BER **~2.8×10¹ → <5.5×10⁻¹⁰**; SNR advantage **+12 dB** vs recent works; reliability approaching **99.999%**.

**6G KPI table (from comprehensive 6G surveys):**
| KPI | 5G-class | 6G target |
|---|---|---|
| Jitter | — | **1 μs** |
| Latency | 1 ms | **0.1 ms (C-plane ≤1 ms, U-plane ≤0.1 ms)** |
| Energy/bit | — | **1 pJ/bit** |
| Reliability | 10⁻⁵ | **FER 10⁻⁹** |
| DL peak rate | 20 Gbps | **1 Tbps** |
| Traffic capacity | 10 Mbps/m² | **10 Gbps/m³** |
| Localization | 10 cm 2D / 1 m 3D | **1 cm 3D** |
| Mobility target | 500 km/h | **1000 km/h** |

### (d) Dataset / testbed / deployment
Survey paper — no own testbed. Synthesis of literature + market studies; comparison table 5G vs 6G (Table 2) across technological and application dimensions.

### (e) Quantitative results
- 6G connection speeds up to **11 Gbps** (satellite-integrated claim in Table 2 discussion).
- 5G KPIs: 20 Gb/s peak, 100 Mb/s user-experienced, 10 Mb/s/m² area traffic; URLLC ≤1 ms; mMTC 10⁶/km² (limited-deployment variant 10⁷/km² in EPRI table).
- RIS-THz: SNR +65 dB swing (−20→45), latency 16.5→2 ms, throughput 1→20 Gbps, BER 10 orders of magnitude improvement.
- 6G HRLLC PoC objective: **round-trip latency < 100 μs**, 7–9 nines reliability (vs 5G's tightest wireless motion control **0.5 ms**).
- Survey article: Sensors 23(17):7528, 35 pages.

### (f) Limitations
1. **6G is pre-standard** (IMT-2030 framework only) — THz/RIS/AI claims are speculative; "prototypes and demonstrations" exist in specific setups only.
2. **Coverage vs THz range** tension — THz needs dense small cells + RIS beam alignment.
3. **Energy consumption** of AI-native networks and RIS control planes not fully quantified.
4. **Security/privacy** in softwarized, decentralized 6G architecture flagged but not solved (blockchain suggested as trust layer).
5. **Economic/business-model** feasibility of city-wide 6G upgrades under-studied.
6. Survey lacks measured city pilot KPIs (few real 6G-smart-city testbeds as of 2023–2026).

---

# 11. Interoperability Stack — oneM2M / SAREF / CityGML / OGC SensorThings

## (a) Problem formulation
Smart-city systems are siloed ("verticals"). Interoperability must work at four levels: **syntactic** (message formats), **semantic** (shared ontologies), **behavioral** (API/procedure), and **geospatial/3D** (city models). Standards address: (i) a horizontal middleware service layer (oneM2M), (ii) a shared IoT ontology (SAREF), (iii) 3D city exchange (CityGML), (iv) sensor data APIs (OGC SensorThings).

## (b) Architecture / components

### 11.1 oneM2M — functional architecture (TS-0001, TS-0004)
**Three-layer horizontal model:** Applications → Middleware (service layer) → Networks.
**Entities:**
- **AE (Application Entity):** implements application service logic (fleet tracking, glucose monitoring, power metering, pump control).
- **CSE (Common Service Entity):** the oneM2M service layer; resides in gateways, servers, capable devices; provides **Common Service Functions (CSFs)**.
- **NSE (Network Service Entity):** connectivity services (outside oneM2M normative scope but architecturally required).
- **IPE (Interworking Proxy Entity):** interface to non-oneM2M technologies (LwM2M, Modbus, OGC SensorThings, OSGi…).

**Reference points:**
- **Mca:** CSE ↔ AE
- **Mcn:** CSE ↔ NSE
- **Mcc:** CSE ↔ CSE (intra-domain)
- **Mcc′:** CSE ↔ CSE across service providers

**Key CSFs:** Registration (single registrar CSE establishing authorization/authentication between AEs and CSEs), Discovery (incl. semantic discovery), Data management (store/retrieve), Communication management, Semantics, Security, Transactions (commit/abort/rollback), Group management, Location, Device management, Service charging, Notification.

**Resource model:** resources discovered/retrieved/updated via **CRUDN** (Create, Retrieve, Update, Delete, Notify) over **REST APIs**; bindings: **CoAP, HTTP, MQTT, WebSocket** (TS-0004, TS-0013 interop tests cover CoAP/HTTP/MQTT bindings).

**Interworking with OGC SensorThings (TS-0041 v5.3.0, 2025):**
- **IPE** sits between OGC/STA server and oneM2M CSE.
- Communication flow over **HTTP and MQTT** (MQTT enables pub-sub on OGC side per STA MQTT extension).
- Data-model mapping: oneM2M resource instances representing non-oneM2M proximal IoT functions (per TS-0033); STA **Datastream** created then **Observation** sent as **HTTP POST**.

### 11.2 SAREF (ETSI TS 103 264, oneM2M TR-0073, TS-0012 Base Ontology)
- **SAREF** = Smart Applications REFerence ontology: "explicitly specifies the recurring core concepts in the Smart Applications domain, the main relationships between these concepts, and axioms to constrain the usage."
- **Core classes:** Device, Service, Function, Command, **ProcedureExecution**, **Observation**, **Measurement** (deprecated in v3.2.1 → replaced by Observation + hasResult indirection), **Actuation**, **Operation** ("machine-interpretable exposure of a human-understandable command to a network"), FeatureOfInterest, PropertyValue.
- **Design principles:** modular (recombination of parts), extensible, maintainable; **explicitly aligned with oneM2M Base Ontology** and reuses: **W3C SKOS, OGC/W3C SOSA/SSN, OGC/W3C Time, OGC GeoSPARQL**; no direct DUL/SUMO upper ontology (indirect via SOSA/SSN).
- **Semantic interop procedure:** external ontologies mapped (sub-classing/equivalence) onto **oneM2M Base Ontology** (minimal ontology, TS-0012); OWL files configure **ontology-based IPEs** (TS-0030); semantic queries = discovery queries + interoperability queries (TR-0073 §8).
- Normative docs: ETSI TS 103 264 (V4.1.1), EN 303 760 (guidelines), ETSI TS 118 112 = oneM2M TS-0012.

### 11.3 OGC SensorThings API (Part 1, 2016; updated 2021; Part 2 sensing profile)
- **Client/server** architecture: sensor pushes data to STA server via **HTTP**; server may support **MQTT** for pub-sub (subscribers notified of new sensor events).
- **Sensing Entities data model:** things, locations, observations, datastreams, sensors, observed properties, features of interest — events/sensor data are **Observation entities**.
- Interworked to oneM2M via IPE (TS-0041): mapping procedure = create Datastream → POST Observation.

### 11.4 CityGML (OGC) + 3D Tiles
- **CityGML** = open XML data model for storage/exchange of virtual 3D city models; **LOD 0–4+** (Helsinki uses 5 LODs); thematic modules: buildings, bridges, vegetation, water, transport (roads/rails), city furniture, land use, tunnels, etc.
- **CityGML 3.0 (OGC 21-006r2, July 2023):** introduced **Dynamizer ADA** for dynamic attribute time-series (sensor feeds) — but under-used in practice.
- **CityJSON** = compact JSON encoding of CityGML.
- **3D Tiles (OGC Community Standard 18-053r2):** tiled streaming of 3D content (glTF-based) for web; **I3S** = Esri's equivalent; conversions CityGML↔3D Tiles cause **semantic data loss**.
- Database backends: **3DCityDB** (relational), Measur3D, CJDB, NoSQL hybrids (Kasprzyk et al. 2024 multi-database CityGML environment for UDT big-geodata).

## (c) Algorithms / procedures (how interop actually works)
1. **Registration:** AE registers at registrar CSE (authn/authz relationships).
2. **CRUDN resource operations** over REST (CoAP/HTTP/MQTT/WebSocket bindings).
3. **Discovery** with attribute filters + optional **semantic queries** (SPARQL-like over OWL annotations).
4. **IPE translation:** resource mapping (TS-0033), data-model mapping (STA entities ↔ oneM2M resources), communication flow (HTTP POST/GET, MQTT publish/subscribe).
5. **Ontology mapping:** external OWL → oneM2M Base Ontology via sub-class/sub-property (example: SAREF ↔ Base Ontology on oneM2M GitLab).
6. **Geospatial alignment:** SAREF uses GeoSPARQL; CityGML uses GML/CRS; SOSA/SSN links Observation ↔ FeatureOfInterest ↔ location.

## (d) Dataset / testbed / deployment
Standistics-driven: oneM2M has certification/interoperability test procedures (TS-0013), recipes and example deployments (dashboards, IPE to third-party analytics). No single city testbed in the standards docs; interop is validated via **conformance test suites** rather than city pilots.

## (e) Quantitative results
- oneM2M spec suite: TS-0001, TS-0002, TS-0004, TS-0013 (CoAP/HTTP/MQTT bindings tested), TS-0014 (LwM2M interworking), TS-0020 (WebSocket), TS-0034 (semantics), TS-0041 (SensorThings interworking v5.3.0, 2025-04-04).
- SAREF: ETSI TS 103 264 V4.1.1; 4 reused ontologies (SKOS, SOSA/SSN, Time, GeoSPARQL); Measurement deprecated in v3.2.1.
- STA: Part 1 published 2016, updated 2021; 2 parts.
- CityGML: LOD 0–4(+); 3.0 released 2023-07-28; 3D Tiles 1.0 (2018 community standard).

## (f) Limitations
1. **Standards fragmentation persists** — oneM2M ↔ STA ↔ FIWARE NGSI-LD ↔ LoRaWAN all need IPEs; each IPE is custom engineering.
2. **Semantic mapping lossiness** — SAREF↔Base Ontology sub-classing doesn't capture all vendor semantics; "least number of conventions" base ontology may be too minimal.
3. **CityGML Dynamizer under-used** — dynamic data managed in parallel, fused manually at application layer.
4. **Format-conversion semantic loss** (CityGML→3D Tiles) and update-pipeline mismatch (batch vs streaming).
5. **No unified city-scale conformance benchmark** — interop test suites don't measure end-to-end city KPIs.
6. **Performance overhead** of REST/CoAP translation at IPEs for high-frequency sensor streams unquantified in the specs.
7. **Security profiles** (OSCORE, ACE) exist but deployment guidance for city systems is thin.

---

# 12. City Deployments — Virtual Singapore / Seoul S-DoT / Songdo

## 12.1 Virtual Singapore (Singapore)

### (a) Problem
Build an authoritative, dynamic **3D city model + collaborative data platform** for planning (emergency evacuation, urban living), test-bedding services, and research — under the Smart Nation initiative. Challenge: Singapore's aerial survey difficulties (frequent cloud cover, dense urban canyons, lush vegetation, busy airspace, strict data security, tight borders).

### (b) Architecture / stack
- **Lead:** National Research Foundation (NRF) + Singapore Land Authority (SLA); platform by **Dassault Systèmes 3D EXPERIENCity® on the 3DEXPERIENCE platform**.
- **Data layers:** terrain model, high-resolution orthophotos, oblique imagery, photo-realistic building models; transport network + city furniture (bus stops, street lights, traffic lights, overhead bridges) in phase 2.
- **Standard:** **CityGML schema** adopted for both national-3D-map and Virtual Singapore projects "allowing the data to be seamlessly combined, analysed and shared across various departments."
- Static + real-time data; scenarios: renewable energy, waste management, neighbourhood walkability, disease-propagation prediction, public transport route analysis.
- "Living laboratory" for smart-city initiatives.

### (c) Algorithms/techniques
Aerial LiDAR + photogrammetry; oblique photography; secure processing in government premises; CityGLOD/LOD management; simulation modules on the Dassault platform.

### (d) Scale (numbers)
- Announced **2014** by Prime Minister's Office; target platform ready **2018**.
- **200,000 textured buildings** to be modeled (Woolpert scope).
- **Dense LiDAR terrain: >5 points/m², better than 10 cm RMS accuracy.**
- **First-ever 10 cm resolution color orthophoto** for all authorized government users.
- Two survey aircraft mobilized for nationwide capture.

### (e) Quantitative results
- 200,000 buildings; ≥5 pts/m² LiDAR; <10 cm RMS; 10 cm orthophoto; CityGML-based multi-department integration.

### (f) Limitations
- Aerial-survey constraints (clouds, canyons, security) forced complex acquisition.
- Real-time sensor integration maturity unclear from public technical docs (static model emphasized).
- Vendor platform (Dassault) lock-in risk; cost; privacy of citizen mobility data in a national twin.

## 12.2 Seoul — S-DoT, S-Map (Virtual Seoul), Smart Seoul Platform (6S)

### (a) Problem
Instrument the entire city for real-time environmental monitoring, 3D planning, and AI-driven citizen services; integrate heterogeneous spatial + IoT data.

### (b) Architecture — Smart Seoul Platform (6S)
1. **S-DoT (Citywide data sensors):** citywide IoT sensor network for air quality, temperature, humidity.
2. **S-Data:** big-data integration hub (collection, integration, analysis).
3. **S-Map:** 3D digital twin of Seoul (**Virtual Seoul**).
4. **S-Brain:** AI chatbot + analytics.
5. **S-Security:** safety/disaster management system.
6. **S-Net:** hyper-connected network (public Wi-Fi, 5G, IoT networks).

**S-Map technical stack:** browser-based (smap.seoul.go.kr); 3D library (buildings, vegetation, facilities); BIM integration; wind-path simulation at altitudes **10 m, 50 m, 100 m, 1 km, 3 km**; street-view of alleys; drone-based 3D modeling (since 2018 demo in 2016); LiDAR aerial photography.

### (c) Techniques
LiDAR + **25,000 aerial photos** auto-analyzed with AI for 3D reconstruction; drone photogrammetry (orthophoto, oblique, 3D modeling); digital map platform for admin-data sharing; COSMOS-derived traffic signal control (also used in Songdo).

### (d) Scale (numbers)
- **S-Map covers entire Seoul: 605.23 km²** in 3D.
- **~600,000 buildings** in the model; underground utilities (water, drainage, gas, electricity, communications, heating); geological maps + contours.
- **S-DoT: >1,000 sensors** for air-quality visualization (Seoul spatial-data page: "more than 1000 sensors"); GovTech page says "over 300 IoT sensors" for S-Dot citywide network — **discrepancy between sources (300 vs 1000+)** reflecting different counting (nodes vs sensing points/phases).
- Drone datasets since 2018; citizen opinion map with **~1.24 million cases** (Jan-onward) as spatial big data.
- Project initiated **2018**, developed in three stages (physical replication → spatial info collection/visualization → simulation/experimentation).

### (e) Quantitative results
- 605.23 km², 600k buildings, 25k aerial photos, 1,000+ air sensors, 5 altitude bands for wind simulation, 1.24M citizen cases.

### (f) Limitations
- Sensor-count inconsistency across official sources (300 vs 1000+).
- Real-time synchronization depth (how often S-Map updates from S-DoT) not published with KPIs.
- Integration across 6S pillars ("no coordination yet" critique echoes broader UDT governance gaps).
- Privacy/security of CCTV+IoT fusion; cyber risk in S-Security layer.

## 12.3 Songdo (Incheon Free Economic Zone, Republic of Korea)

### (a) Problem
Build a master-planned U-City from scratch (program **2003–2030**) embedding AI/IoT/smart infrastructure across transport, buildings, energy, water, waste, public safety, planning.

### (b) Architecture / stack
- **Foundations:** city-wide **fibre networks**, LEED-certified buildings, **district heating and cooling**, autonomous buses, EV infrastructure, **pneumatic waste collection**, AI-assisted resource management.
- **U-City center:** originally separate centers for 3 districts (Songdo, Yeongjong, Cheongna — total **132.92 km²**); integrated into a **single IFEZ U-City integrated operation center** via data-processing-room integration, platform-level system integration, and equipment virtualization (image-saving server virtualization; real-time DB access monitoring S/W).
- **Traffic:** upgraded **COSMOS** (Cycle Offset Split Model of Seoul) signal control; Time Based Control (TBC) at peak; illegal-parking enforcement via camera → crime-prevention CCTV reuse at night.
- **IoT sensors** in houses/buildings for real-time user information; U-City infrastructure network connecting on-site sensors to center for control/monitoring/data collection.

### (c) Techniques
System integration platform; server virtualization; DB access-control & trend analysis software; predictive information dissemination to citizens; IoT-enabled building/home telemetry; district energy optimization.

### (d) Scale (numbers)
- Investment: **KRW 45,269 billion** across 3 IFEZ districts (**132.92 km²**) for new-city infrastructure (IADB case study).
- Integration cost saving: consolidated U-City center cost reduced from **KRW 20.6 billion → KRW 14.6 billion** (≈29% savings).
- Program timeline: **2003 → 2030** phased.

### (e) Quantitative results (ITU U4SSC case study, 2026)
- **30–40% lower building energy use**
- **~40% lower per-capita CO₂ emissions**
- **10–20% less congestion**
- **>70% waste recycling**
- **40–50% less water leakage**
- **30–40% faster emergency response**

### (f) Limitations
- **Cost, interoperability, cybersecurity, privacy, public trust, technological obsolescence** explicitly listed as challenges (ITU U4SSC).
- Greenfield-only: not replicable in retrofit cities; lesson = open standards + resilient networks + PPP + community engagement + modular phased design.
- Centralized operation center = single point of failure/attack.
- Reported gains are project-reported, limited independent verification methodology disclosed.

---

# 13. Recent Paper A (2025) — "A Survey on Architectural Approaches for 6G Networks: Implementation Challenges, Current Trends, and Future Directions," MDPI (Eng. Proc. / preprint 2025, DOI via preprints.org 1d47cbf…)

## (a) Problem
Categorize 6G architectural approaches (AI/ML, DTs, open air interfaces, network slicing, cloud/fog) and their applicability to smart cities; identify open issues.

## (b) Architecture
- Application layer supports autonomous vehicles, **smart cities**, AR/VR.
- Approaches reviewed: **organic 6G** (architectural protocols as web services); **DT-based 6G network architecture** modeled mathematically by **intra-domain and inter-domain hypergraphs** capturing changing rules of network elements; flexible layered architecture; **ML-enabled slicing** (RL, deep learning, federated learning) to eliminate vendor lock-in.
- **Smart sustainable city (SSC) 4-layer model:** sensing layer → transmission layer → data layer → application layer; key techs: AI/ML, non-terrestrial networks, ISAC.
- Nested city approach: macroscopic cells + 6G cells fiber-linked; **mMIMO per AP** inside 6G cells; **bee-hive distributed cloud** (fog-like) architecture.

## (c) Algorithms
Hypergraph modeling of network domains; RL/DL/FL for slicing orchestration; DT-based model/evaluate/optimize loop.

## (d) Datasets
Survey of related works (2024 CRAN, M2M in 6G, ISAC, AI/ML enablers, AI-enabled 6G).

## (e) Quantitative
Table 2 categorizes ~18 surveyed architectures by KET presence (AI/ML, DT, OAI, slicing, CF); e.g., [55] 6G multi-layer vision, [57] DT-based 6G, [67–69] 6G-for-smart-cities.

## (f) Limitations
- Pre-standard IMT-2030; few measured pilots; DT-6G hypergraph model evaluation depth varies by cited work.

---

# 14. Recent Paper B (2025) — "Big data and Internet of Things applications in smart cities: Recent advances, challenges, and critical issues," Internet of Things (Elsevier), DOI 10.1016/j.iot.2025.101770 (Nov 2025)

## (a) Problem
Literature fragmented: many surveys address individual technologies (IoT, big data, edge, DT, blockchain) in isolation; few examine **interdependencies and combined impact** on smart-city capabilities. Provide comparative assessment of reference architectures + key performance metrics with correlations to design choices and urban application demands.

## (b) Architecture
- Covers **edge–cloud architectures**, digital twins, blockchain complementing traditional **IoT–Big Data pipelines**.
- Emerging trends: **6G-enabled IoT, federated learning (FL), quantum computing, swarm intelligence**.
- Domain coverage: transportation, energy management, healthcare, public safety.
- Challenges linked explicitly to architectural, infrastructural, and policy dimensions: scalability, interoperability, security, data governance.

## (c) Algorithms/pipeline
IoT data pipeline → edge preprocessing → cloud/edge analytics → DT simulation → blockchain-secured exchange; FL for privacy-preserving analytics; swarm intelligence for optimization.

## (d) Datasets
Comparative assessment across representative smart-city deployments (synthesized).

## (e) Quantitative
Highlights claim comparative architecture/metric tables with "clear correlations between design choices, system performance, and application-specific demands" (details in full text).

## (f) Limitations
- Still a survey (no new testbed); fragmentation critique applies reflexively to breadth-over-depth; quantum/swarm items remain prospective.

---

# 15. Recent Paper C (2024–2026) — Data Mesh & IoT–Edge–Cloud Continuum Architectures

## 15.1 Rossini, Bicocchi, Pietri et al. — "A Data Mesh Architecture for IoT–Edge–Cloud Continuum Smart City Systems," IEEE PerCom Workshops 2026, DOI 10.1109/PerComWorkshops68308.2026.11585408 (plus precursor SEC 2024 "Towards a Distributed Data Mesh Model for the IoT-Edge-Cloud Continuum in Smart Cities")

### (a) Problem
Traditional centralized data platforms suffer **single-point load, monolithic design**, and struggle with **interoperability, domain-specific data ownership, and real-time requirements** in CPS/smart-city contexts (IECC smart-city context).

### (b) Architecture
Applies **Data Mesh** principles (domain-oriented data ownership, data-as-a-product, federated computational governance, self-serve platform) to CPS across **IoT–edge–cloud continuum**: prototype integrates IoT endpoints, edge nodes, cloud components as federated domain data products rather than a central warehouse.

### (c) Algorithms
Data-product contracts, federated governance policies; comparison vs microservices-based architecture on latency/memory.

### (d) Testbed
Prototype deployment in IECC smart-city context; performance compared against microservices baseline.

### (e) Quantitative
Results: **slightly higher latency and memory usage** from service replication and domain ownership overhead — but gains in interoperability/ownership (qualitative trade-off quantified in paper).

### (f) Limitations
- Data Mesh overhead (replication) raises latency — problematic for URLLC-class services.
- Early workshop paper (6 pages); limited scale.

## 15.2 Companion: Flexible Multi-Domain IoT Architecture for Smart Cities — Applied Sciences 16(3):1534 (MDPI, Feb 2026), DOI 10.3390/app16031534

### (a)
Cross-domain orchestration, interoperability, distributed systems, **edge-to-cloud integration**, multi-site platforms; validate in **real-world Smart Waste Management pilot**.

### (b)
Flexible open collaborative platform architecture addressing differences in data models, control interfaces, orchestration semantics, administrative governance; comparative analysis vs multi-domain orchestration frameworks, federated IoT testbeds, fog/MEC architectures.

### (c–e)
Empirical deployment testing within a smart-city cluster; demonstrates flexible workflows, cross-platform collaboration, real-time decision-making, vendor-lock avoidance. Validation = real waste-management pilot (numbers in full text).

### (f)
Alignment across diverse hardware/software/connectivity still "remains elusive"; governance semantics hardest.

## 15.3 Additional recent architectural sources (2024–2026)
- **"The Role of 6G Technologies in Advancing Smart City Applications" (Sustainability 16:7039, 2024)** — PRISMA review; 4-layer smart city architecture (sensing → transmission → data management → application); IoT/CPS 3-layer (sensors/middleware/networked world); ISAC, FiWi, MEC V2X use cases; blockchain+6G for trust.
- **"Network Slicing in 6G: A Strategic Framework for IoT in Smart Cities" (PMC11243923, 2024)** — slicing architecture = Access Network + Core Network + Edge Cloud + Transport Network + Service Plane; mathematical resource-allocation model; achieved **resource utilization 80%**, low RTT, minimal packet loss, high availability, remarkable throughput.
- **DIN SPEC 91357 Open Urban Platform** reference architecture (used in 2025 smart-city campus playground paper) — abstract OUP layers: data sources → ingestion → data platform → quality monitoring/configuration → dashboards (e.g., City of Bad Hersfeld Urban Cockpit).
- **arXiv 2509.11810 (2025)** — Dynamic Urban Scene Synthesis DT architecture: decoupled data/representation planes, **NGSI-LD** + 3D representation; surveys six platforms; criticizes "data first, scene second, joined only by manual bindings"; CityGML 3.0 Dynamizer ADA vs open-USD/Omniverse as the two "true" DT ecosystems.

---

# Cross-cutting synthesis (for quick reference)

| Paper | Killer architectural idea | Key number | Biggest gap |
|---|---|---|---|
| Zanella 2014 | Constrained↔unconstrained mirrored stack + service delay taxonomy | 8+1 nodes, 105-min packets, 10 s alarm delay | Tiny deployment, no semantics |
| Gubbi 2013 | Cloud-centric Internet-centric IoT + scale-based domains | 3 core components; Aneka/3 models | No benchmarks |
| Al-Fuqaha 2015 | 4-category protocol taxonomy | MQTT 2B / CoAP 4B / AMQP 8B headers; CoAP wins <25% loss | No unified benchmark |
| Akyildiz 2002 | 8 design factors + data-centric routing taxonomy | LEACH 7×; EAR +44% lifetime vs DD | No lifetime equation, no security |
| Shi 2016 | Edge = latency/battery/bandwidth/privacy fix | Millisecond cloud latency untenable | No measured numbers |
| Lee 2008 | Rebuild abstractions for time+concurrency | 20 MHz ±100 ppm discarded by SW | No constructive model |
| Kitchin 2014 | Five critiques of real-time city | 5 concerns | Non-technical only |
| Xie 2019 | Blockchain-for-SC domain map | Fabric/Ethereum/custom dominance (29/38/73) | No city KPIs |
| Peldon 2024 | 6-layer UDT + sync taxonomy | 6 layers (White) | Inconsistent layer counts |
| Weil 2023 | 8 UDT challenges + format failure modes | 14 tech + 9 non-tech (Lei) | Semantic loss in 3D Tiles |
| Murroni 2023 | 5G triangle → 6G (THz/AI/RIS/quantum) | URLLC 1 ms; 6G 0.1 ms, 1 Tbps, 10⁻⁹ FER | Pre-standard |
| oneM2M/SAREF/STA | Horizontal CSE + ontology mapping + IPE | CRUDN; 4 reused ontologies | Custom IPE engineering |
| Virtual Singapore | CityGML national twin | 200k buildings, 10 cm ortho | Static-model emphasis |
| Seoul 6S/S-DoT/S-Map | 6-pillar platform | 605.23 km², 600k buildings, 1k+ sensors | Sensor-count inconsistency |
| Songdo | Greenfield U-City integration | −30–40% energy, −40% CO₂, −10–20% congestion | Centralized, cost/obsolescence |
| 2025–2026 arch. papers | Data mesh, 6G hypergraph DT, slicing, OUP | 80% slicing utilization; mesh +latency | Early-stage, small scale |

---

*End of dossier.*
