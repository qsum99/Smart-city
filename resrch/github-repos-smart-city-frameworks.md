# GitHub Repository Dossier: Smart City Frameworks, IoT Platforms, Digital Twins & City Data Platforms

**Research type:** Web-only deep research (no code written, no repositories cloned)
**Research date:** 6 November 2026 (star counts, licences and recency figures are snapshots around this date)
**Sources:** github.com repository pages and organisation pages, GitHub-derived statistics aggregators (RepositoryStats, buildradar, DiscoverGit, Snyk, LFX Insights, appsgit), official project websites, Eclipse Foundation project metrics, Wikipedia, university/project documentation, and publisher/journal pages for paper-linked code.
**Coverage:** 50+ repositories across six categories, with a master summary table of 45+ rows.

## How to read this dossier

Each entry follows a fixed pattern: identity (URL, stars, language, licence, recency, maintainer) → what it actually implements (architecture, protocols, standards, papers) → repository structure and code-quality signals → installation/dependencies → best-fit use cases for a smart-city researcher → limitations → a **VERDICT** line.

**Verdict legend**

- **essential** — a default/reference choice in its niche; cite it, build on it, or benchmark against it.
- **useful** — solid, maintained, worth adopting for specific layers of a smart-city stack.
- **niche** — valuable only for a narrow purpose (teaching, a specific standard, a specific city, a specific paper).
- **avoid-stale** — archived, relicensed into source-available limbo, or unmaintained; do not build new work on it (still citable as history).

---

# CATEGORY 1 — SMART CITY / URBAN PLATFORMS

## 1.1 `3dcitydb/3dcitydb` — 3D City Database (the open-source CityGML database)

- **URL:** https://github.com/3dcitydb/3dcitydb
- **Stars/forks:** 469 ★ / 84 forks · **Language:** SQL (PostgreSQL/PostGIS) + Java tooling · **Licence:** Apache-2.0 (releases before 3.3.0 were LGPL-3.0) · **Created:** November 2013, still maintained (V5 line active) · **Maintainer:** international 3DCityDB consortium (originally TU Munich / cc gateway GmbH, now a broad academic-industrial group; homepage 3dcitydb.org).

**What it implements.** A free, semantically rich 3D geo-database on top of a standard spatial relational database. V5 maps the OGC City Geography Markup Language Conceptual Model (**CityGML 3.0**) onto a PostgreSQL/PostGIS schema with pgSQL utility functions, and supports **CityGML 3.0, 2.0 and 1.0**, Application Domain Extensions (ADEs), four/five Levels of Detail, textures/appearances, TIN terrain models, recursive aggregation, flexible 3D geometries (Solid, MultiSurface, TIN, CompositeCurve, etc.), deletion-with-historisation (termination timestamps as a versioning mechanism), and a `citydb-tool` for import/export in **GML and CityJSON** encodings with on-the-fly upgrade/downgrade between CityGML versions. The README explicitly positions CityGML as "a key role in Urban Digital Twins" and BIM-GIS integration, and indexes open 3D city datasets: **21 countries, 65 regions/cities, >210 million semantic 3D building models** available for free download.

**Structure & quality signals.** Dual SQL/Java codebase; documented schema; homepage + dataset index; releases on GitHub; Apache licence since 3.3.0 (older LGPL). This is infrastructure software, not a demo: the value is the schema design itself, which is effectively a reference implementation of how to store a city model with semantics, LODs, history and ADEs.

**Install/deps.** PostgreSQL + PostGIS; `citydb-tool` (Java) for bulk import/export; Docker images published by the project.

**Best fit.** Any researcher modelling **storage of semantic 3D city models**, CityGML/CityJSON round-tripping, city-scale BIM-GIS integration, or building the persistence layer of an urban digital twin.

**Limitations.** Not a viewer or a platform — no API gateway, no IoT layer; requires DBA-level setup; documentation is spread across the homepage/wiki; a single project with a modest GitHub community (469 stars) despite its importance.

**VERDICT: essential** — the de-facto open database layer for CityGML-based urban digital twins.

## 1.2 `UDST/urbansim` — UrbanSim (land-use/transport microsimulation)

- **URL:** https://github.com/UDST/urbansim
- **Stars/forks:** 557 ★ / 145 forks · **Language:** Python (plus HTML/R docs) · **Licence:** BSD-3-Clause · **Created:** August 2013 (project lineage from 1998) · **Maintainer:** UDST (Urban Data Science Toolkit) organisation, Berkeley CA / urbansim.com; founder Paul Waddell (UC Berkeley, later UT Austin).

**What it implements.** A platform for building statistical models of cities and regions — forecasting long-range patterns in real estate development, demographics and related outcomes under policy scenarios. The `urbansim` library contains statistical estimation and simulation utilities; domain models for housing markets, household relocation, location choice, transition and development; real-estate feasibility methods; and frameworks for assembling a full model. In pseudocode: estimate a set of models, then simulate them in sequence. Version **3.3 was released 16 September 2026** and the README declares status "Active" with a portable, CPU-based architecture.

**Papers it maps to (this is a genuinely paper-linked repo).** Waddell, P. (2002) *UrbanSim: Modeling Urban Development for Land Use, Transportation and Environmental Planning*, JAPA 68(3); Waddell (2011) *Integrated Land Use and Transportation Planning and Modeling*, Transport Reviews; Noth, Borning & Waddell (2003) *An Extensible, Modular Architecture for Simulating Urban Development, Transportation, and Environmental Impacts*, CEUS 27(2); Waddell et al. (2007) *Incorporating Land Use in Metropolitan Transportation Planning*, TRPart A; Sevcikova, Raftery & Waddell (2007) *Assessing Uncertainty in Urban Simulations Using Bayesian Melding*, TRPart B; plus 25+ more on the urbansim.com academic page.

**Structure & quality signals.** GitHub Actions CI (`test.yml` badge), Sphinx docs hosted on GitHub Pages (v3.3 docs), PyPI + conda-forge distribution, 18 open issues, sibling repos in the UDST org: **vizicities** (2,717 ★, 3D geospatial browser framework — largely dormant), **pandana** (422 ★, pandas network analysis/accessibility), **urbanaccess** (263 ★, GTFS+OSM accessibility), **synthpop** (114 ★), **choicemodels** (85 ★).

**Install/deps.** `pip install urbansim` or conda-forge; pure Python, no compilation; heavier model runs need pandas/scikit-learn-era stacks plus your own parcel/household/employment datasets.

**Best fit.** Land-use/transport interaction studies, scenario analysis for urban planning, synthetic population and accessibility pipelines (via pandana/urbanaccess), and any paper that needs a credible, decades-cited microsimulation baseline.

**Limitations.** Data-hungry (you must assemble municipal parcel, household and employment data); interface is library-level, not a city platform; the org's other repos (vizicities) are much less active than `urbansim` itself.

**VERDICT: essential** — the canonical open land-use microsimulation codebase for urban research.

## 1.3 `GetDKAN/dkan` — DKAN open data portal (Drupal)

- **URL:** https://github.com/getdkan/dkan
- **Stars/forks:** 387 ★ / 171 forks · **Language:** PHP (96.8%, plus JS/Twig) · **Licence:** GPL-2.0-or-later · **Recency:** active — updated within days of this research; DKAN 4.1.5 released 7 October 2026 on Drupal.org · **Maintainer:** GetDKAN / CivicActions (US); registered **Digital Public Good** (DPGA evaluated 08.12.2024).

**What it implements.** An open data catalog module for Drupal 10/11: JSON-based metadata catalog with user-defined schemas, **DCAT-US** out of the box, harvesting from external `data.json` catalogs, REST APIs for remote dataset management, a decoupled React front end, and a datastore that loads CSVs into the database for queryable APIs. It is a city-portal building block: the DPG registry explicitly ties DKAN to SDGs 8, 9, 11, 16.6 and 16.10 (public access to information, accountable institutions).

**Structure & quality signals.** ReadTheDocs documentation, code coverage/maintainability badges, security advisory policy on Drupal.org, 161 open issues (migrating to Drupal.org — GitHub issues/PRs moved in October 2026; releases now cut on Drupal.org as `drupal/dkan`, mirrored `4.x` branch on GitHub).

**Install/deps.** `composer require drupal/dkan` (v4) or historically `composer require getdkan/dkan`; requires a Drupal site; React front end optional.

**Best fit.** Researchers/engineers deploying a **municipal open-data portal** who need DCAT harvesting, datastores and APIs without building a catalog from scratch; also SDG-reporting data hubs.

**Limitations.** Drupal-heavy stack (PHP expertise required); 161 open issues; dual-homing (GitHub → Drupal.org) creates some confusion about where to file/work; star count modest relative to CKAN.

**VERDICT: useful** — a credible, standards-focused city open-data portal, second choice after CKAN unless you are already a Drupal shop.

## 1.4 `ckan/ckan` — CKAN, the world's leading open data portal software

- **URL:** https://github.com/ckan/ckan
- **Stars/forks:** ~5,150 ★ / ~2,122 forks · **Language:** Python (plus JS) · **Licence:** AGPL-3.0 · **Recency:** last commit 30 October 2026; release **ckan-2.12.1** (28 October 2026); ~881 commits in the last 12 months; 28,665 total commits · **Maintainer:** Open Knowledge / CKAN global community (311 contributors).

**What it implements.** A full data management system for cataloging, storing, accessing and publishing datasets: rich front end, dual APIs (data + catalog), the DataStore (queryable tabular store), DataPusher, user/org/permission model, harvesting, and an extension ecosystem (`ckanext-*`). It powers **catalog.data.gov, open.canada.ca/data and data.humdata.org**, plus hundreds of city portals worldwide — this is the default engine behind municipal open-data programs.

**Structure & quality signals.** Monorepo layout with `ckan/` core package, `ckanext/` extension points, `doc/` Sphinx docs, `.github/` Actions workflows, `test-infrastructure/`, Cypress E2E tests, `.snyk` security config, `SECURITY.md`, `AGENTS.md` (AI-assisted contributor guidance added 2026), Transifex i18n, 864 open issues, 22 releases.

**Install/deps.** Source install (pip/requirements + PostgreSQL+SOLR+Redis), official Docker images, or package installs; Python 3.x, PostgreSQL, SOLR/ElasticSearch for search.

**Best fit.** Any city/regional **open data platform**, sensor-data publishing front ends (via DataStore APIs), DCAT/CKAN-API interoperability studies, and extension development (there are city-specific extensions for geospatial data, etc.).

**Limitations.** AGPL imposes obligations on hosted derivatives; a large legacy codebase with a big issue backlog; SOLR/Postgres ops overhead; UI is functional rather than modern.

**VERDICT: essential** — the reference city open-data platform; benchmark DKAN and others against it.

## 1.5 `citygml4j/citygml-tools` + `citygml4j/citygml4j` — CityGML/CityJSON processing toolkit

- **URLs:** https://github.com/citygml4j/citygml-tools (163 ★) and https://github.com/citygml4j/citygml4j (138 ★)
- **Language:** Java · **Licence:** Apache-2.0 both · **Maintainer:** Claus Nagel and the citygml4j organisation (8 public repos; homepage citygml4j.org) · **Recency:** `citygml-tools` changelog through 2026 (2.4.1 on 1 February 2026; releases 2.4.x/2.5 line; Java 17 minimum as of 2.3.0); `citygml4j` latest release 3.5.1.

**What it implements.** `citygml4j` is the open-source **Java API for OGC CityGML**: a `citygml4j-core` module implementing the CityGML 3.0 conceptual model, an ADE extension API, plus serialization modules `citygml4j-xml` (GML/XML for CityGML 3.0/2.0/1.0) and `citygml4j-cityjson` (CityJSON 2.0/1.1/1.0). `citygml-tools` is the CLI built on it with commands: `stats`, `validate`, `apply-xslt`, `change-height`, `remove-apps`, `clip-textures`, `merge`, `subset`, `filter-lods`, `reproject`, `from-cityjson`, `to-cityjson`, `upgrade` (to CityGML 3.0). Companion repos: `citygson` (10 ★), `energy-ade-citygml4j` (9 ★, Energy ADE), `iur-ade-citygml4j` (6 ★, i-Urban Revitalization ADE), `ade-xjc` (4 ★).

**Quality signals.** Changelog-driven releases, GitHub Releases binaries, Dockerfile present, integration with the official CityJSON site's tutorials (the CityJSON docs recommend `citygml-tools` for conversions), zero open issues on both repos at snapshot time.

**Install/deps.** Java 17+, download ZIP or build from source; Gradle coordinates `org.citygml4j:citygml4j-xml` / `citygml4j-cityjson`.

**Best fit.** Converting municipal CityGML datasets to CityJSON (and to viewer-ready formats), validating city models, LOD filtering for web delivery, Energy ADE workflows in urban-twin projects.

**Limitations.** Library/CLI only — no database, no server, no viewer; small maintainer team; niche star counts reflect a specialised audience rather than weak health.

**VERDICT: useful (citygml-tools) / essential-adjacent for anyone handling CityGML** — the practical Swiss-army knife for 3D city files.

## 1.6 `smart-data-models/data-models` + `smart-data-models/SmartCities` — Smart Data Models initiative

- **URLs:** https://github.com/smart-data-models/data-models (143 ★) and https://github.com/smart-data-models/SmartCities (115 ★)
- **Language:** JSON Schema / Python tooling · **Licence:** open, royalty-free model licence (schemas CC-BY-class "Smart Data Models" terms; code MIT where applicable) · **Maintainer:** smart-data-models org — a programme led by **FIWARE, IUDX, TM Forum, OASC** and others (106 public repos, 310 followers) · **Recency:** continuously updated; new API/demo tooling (`sdm_as_a_service`) present in the umbrella repo.

**What it implements.** The de-facto standard **information models for smart city (and 11 other) domains**: JSON Schemas plus written specifications, attribute URIs, and NGSIv2/NGSI-LD payload examples with `@context` files. The SmartCities subject repository alone lists: `dataModel.Building`, `GBFS` (bike sharing), `OSLO`, `Parking`, `ParksAndGardens`, `PointOfInterest`, `Ports`, `S4BLDG`, `Streetlighting`, `Transportation`, `UrbanMobility`, `WasteManagement`, `Weather`, `WifiNetwork`, `ZEB` (zero-energy buildings). Models move through lifecycle states: Incubated → Harmonization → Official. This is the semantic layer of the FIWARE/ETSI NGSI smart-city stack, aligned to the **ETSI NGSI API** and TM Forum Open APIs.

**Related archived repo.** `FIWARE/data-models` (88 ★, MIT, **ARCHIVED**) is the predecessor — "subsequent works carried out in Smart data models repositories" — worth citing historically (it aligned with the GSMA IoT Big Data project).

**Best fit.** Anyone publishing or consuming **interoperable city data** (parking, street lighting, waste, mobility, weather) across a data space; schema reuse for NGSI-LD context brokers; harmonisation research.

**Limitations.** Not code you "run" — it is schemas and docs; no consumer runtime; large org with many small repos means discoverability requires the umbrella list (`official_list_data_models.json`).

**VERDICT: essential** — if your paper touches smart-city interoperability, these schemas are your vocabulary.

## 1.7 `FIWARE/tutorials.Step-by-Step` (+ `FIWARE/tutorials.NGSI-LD`) — FIWARE smart-system tutorials

- **URL:** https://github.com/FIWARE/tutorials.Step-by-Step (81 ★, 73 forks) and https://github.com/FIWARE/tutorials.NGSI-LD (34 ★)
- **Language:** Python/shell (umbrella), mixed (CSS/Dockerfile/JS/TS in NGSI-LD repo) · **Licence:** MIT · **Maintainer:** FIWARE Foundation · **Recency:** actively maintained; hosted on fiware.github.io and Read the Docs; supports GitHub Codespaces.

**What it implements.** The canonical learning path for building **context-based smart systems**: NGSI-v2 "Smart Supermarket" and NGSI-LD "Smart Farm" tutorial series covering `@context`, CRUD, concise payloads, entity relationships, subscriptions, registrations, temporal operations, IoT Agents (Ultralight/JSON), time-series (QuantumLeap/CrateDB), big-data analysis with Flink and Spark, identity management/verifiable credentials, cloud-edge computing (507) and federative data spaces (601). Each tutorial is a self-contained repo/submodule with `./services` scripts that spin up Docker Compose stacks (Orion/Orion-LD, Scorpio, Stellio brokers selectable).

**Quality signals.** RTD documentation, Postman collections, CI badges, Docker images, submodule structure for ~40 tutorials; the architecture advice in the READMEs (when to use NGSI-v2 vs NGSI-LD) is itself citable guidance for city platform design.

**Best fit.** Standing up a **FIWARE-based city context broker stack** for a pilot; teaching; reproducing published NGSI-LD experiments; understanding federation/data-space patterns increasingly used in EU smart-city projects.

**Limitations.** Tutorial-grade (toy entities: farms, supermarkets), not production city code; star counts are low because each tutorial lives in its own repo; requires Docker and some DevOps familiarity.

**VERDICT: useful** — the on-ramp to the entire FIWARE smart-city ecosystem.

## 1.8 `lutece-platform/lutece-core` — Lutece, the city digital-services platform (Paris)

- **URL:** https://github.com/lutece-platform/lutece-core
- **Stars/forks:** 80 ★ / 67 forks · **Language:** Java · **Licence:** BSD-3-Clause · **Created:** November 2014 · **Maintainer:** City of Paris / Lutece consortium (homepage lutece.paris.fr; over 400 off-the-shelf modules in the plugin repositories).

**What it implements.** An open modular platform enabling city governments to share, re-use and adapt digital services created by other cities — a municipal web-portal/cms framework with a large module marketplace (authentication, forms, geolocation, etc.), Docker images on Docker Hub, a wiki, a MOOC, and an online demo site resetting every 3 hours.

**Best fit.** Municipal e-services research, cross-city service re-use studies, French/EU city-government IT modernisation case studies.

**Limitations.** Portal software, not an IoT/urban-data platform; small international mindshare; activity concentrated in French public-sector adopters.

**VERDICT: niche** — relevant if your smart-city scope includes citizen-facing municipal services rather than sensors/twins.

## 1.9 `egovernments/egov-smartcity-suite` — eGov SmartCity suite (India) — ARCHIVED

- **URL:** https://github.com/egovernments/egov-smartcity-suite
- **Stars/forks:** 76 ★ / 69 forks · **Language:** Java (eGovernments stack) · **Licence:** GPL-3.0 · **Status: ARCHIVED** (snapshot) · **Maintainer:** eGovernments Foundation (Bangalore); homepage egovernments.org.

**What it implements.** An eGovernance suite for municipal governments aimed at internal efficiency, transparency, accountability and service delivery for urban local bodies (ULBs) in India — serving 325+ ULBs historically, with a Codacy quality badge in the README. This is one of the few openly published **India smart-cities-related** codebases: ULB-level billing/property/treasury workflows rather than sensors.

**Best fit.** Indian smart-city/municipal-governance research, e-governance comparisons, reuse of property-tax and grievance workflow logic.

**Limitations.** **Archived** — no upstream fixes; old stack; docs and issues frozen; successor products from eGovernments are commercial/elsewhere.

**VERDICT: avoid-stale** — valuable as historical evidence of India's municipal open-source stack, not as a build dependency.

## 1.10 `enryteam/smart-city` — Chinese smart-city standards & solution library

- **URL:** https://github.com/enryteam/smart-city
- **Stars/forks:** 341 ★ / 158 forks · **Language:** Markdown documentation · **Licence:** MIT · **Created:** March 2022 · **Maintainer:** single author (transportation/traffic domain practitioner).

**What it implements.** Not code: a curated collection of smart-city construction schemes, Chinese national standards (GB/T), regulations, solutions and reference materials — with emphasis on intelligent transportation, smart highways, vehicle-road collaboration (车路协同) and cloud-control platforms. Recommended to be read with Typora's file-tree view.

**Best fit.** Getting oriented in **Chinese smart-city standards and solution templates** — useful for comparative policy/standards research or for finding standard numbers to cite.

**Limitations.** Documentation only; no runnable system; Chinese-language; provenance of collected internet material varies.

**VERDICT: niche** — a standards/reading list, not a framework.

## 1.11 Recent NGSI-LD "city platform" wave (small but noteworthy)

**`minhe51805/UrbanReflex`** — 133 ★ / 9 forks, GPL-3.0, created November 2025, homepage docs. An open-source smart-city intelligence platform that turns road segments into linked-data nodes: real-time air-quality monitoring (NGSI-LD/ETSI-aligned), citizen infrastructure reports with photos and geolocation, AI-powered classification/prioritisation (RAG system), open data exports (GeoJSON, NDJSON, CSV), role-based access, one-command setup via **Just + UV**. Well-organised README with live stat badges (contributors, commit activity, issues). **VERDICT: useful** — a modern, standards-aligned reference implementation of a citizen+environment city platform; young (2025), GPL-3.0 obligations.

**`Haui-HIT-H2K/SmartCity-Platform`** — 83 ★ / 6 forks, Apache-2.0, created 30 October 2025. Vietnamese university competition entry (PMNM 2025) implementing a **smart urban data platform with tiered (HOT/WARM/COLD) storage and edge architecture**: RabbitMQ 3 as edge storage layer, Redis (hot), MongoDB 7 (warm/cold), Docker Compose orchestration, Python 3.10 + Faker data generator, NGSI-LD standards. **VERDICT: niche** — hackathon-grade, but a clean illustration of tiered IoT data routing for teaching.

**`UIP-Urban-Intelligence-Platform/UIP-Urban_Intelligence_Platform`** — 25 ★ / 5 forks, MIT, created November 2025. Production-oriented multi-agent smart-traffic system for Ho Chi Minh City: computer vision (YOLOX + DETR) feeding **Linked Open Data** (NGSI-LD, RDF, W3C SOSA/SSN), Neo4j knowledge graph, Python backend + React/TypeScript frontend, Docker Compose with 12 services, 100% YAML configuration, Docusaurus docs. **VERDICT: niche** — a good end-to-end example of vision→semantic-web pipelines, but young and single-city.

**`CTU-SematX/LegoCity`** — 19 ★ / 1 fork, MIT (+CC-BY-4.0 open data), created October 2025. Lightweight FIWARE/NGSI-LD smart-city template for teaching and rapid experimentation: demo/weather servers (Elysia + Bun) with Swagger UI and health checks, Orion broker with nginx, dashboard, and an `opendata/` seed set (traffic flow, flood sensors/zones, emergency incidents/vehicles, medical facilities, weather stations, air-quality monitors); Docker Compose quickstart; OpenSSF scorecard badges. Related: **`CTU-SematX/Lego-Dashboard`**, a PayloadCMS/Next.js 16 low-code alternative to FIWARE WireCloud with Vitest+Playwright tests. **VERDICT: niche** — excellent teaching scaffold for NGSI-LD city dashboards.

**`Prayag-X/Smart-City-Dashboard`** — 22 ★ / 6 forks, MIT, GSoC'23. Android/Dart app visualising open data from 8+ cities (NYC, Charlotte, Seattle, Austin, Boulder, Chicago, Toronto, Monterrey) with Liquid Galaxy/KML export. **VERDICT: avoid-stale** — a finished GSoC artefact; nice UI demos, no ongoing life.

**`tpt-solutions/tpt-smartcity`** — 0 ★, MIT, created May 2026. Claims an "enterprise-grade" modular city platform: traffic, energy, water, safety, environment services, 3D digital twin engine, cross-domain AI orchestrator, Docker/K8s/Helm/Terraform deployment, Sentry/Grafana/Prometheus. **VERDICT: avoid-stale (too early)** — zero community traction; watch rather than adopt.

**`smartcitiescommunity/Civikmind`** — 42 ★ / 15 forks, GPL-2.0, created 2021. Spanish/EN/FR/ZH/AR/HI multi-language platform for citizen participation, oversight and smart-asset management framed around the SDGs (born from "Hacking Cívico"). **VERDICT: niche** — SDG-aligned civic participation reference.

**`meirim-org/meirim`** — 66 ★ / 29 forks, MIT (+CC-BY content), created 2017, 165 open issues. Open-source smart-city application for transparency in urban planning (Portugal): backend + frontend + crawler for municipal planning procedures, topics tagged citizen-participation/democracy/smart-cities/urban-planning. **VERDICT: niche** — a real civic-tech deployment with a heavy open-issue backlog.

---

# CATEGORY 2 — IoT FRAMEWORKS & PROTOCOLS (the connectivity/ingestion layer actually used in city deployments)

## 2.1 `thingsboard/thingsboard` — the all-in-one IoT platform

- **URL:** https://github.com/thingsboard/thingsboard
- **Stars/forks:** **22,644 ★ / 6,552 forks** (99th percentile on GitHub; ~#1,981 overall) · **Language:** Java (primary), plus JS/TS, SQL, Dockerfile · **Licence:** **BUSL-1.1 since v4.4** (older versions Apache-2.0; each release becomes Apache-2.0 four years after publication) · **Recency:** last commit ~3 days before 5 Nov 2026; **release 4.4.0.2 on 30 Oct 2026**; 29,245 commits; 6,347 PRs merged; 96 public repos in the org · **Maintainer:** ThingsBoard, Inc.

**What it implements.** An all-in-one IoT platform covering device management, data collection, processing and visualisation: **MQTT, CoAP, HTTP, LwM2M, SNMP** device connectivity; microservices architecture; rule chains for stream processing; dashboards/widgets; alarms; multi-tenancy; edge computing module; and (as of 4.4) the former Professional-Edition features — integrations, scheduler, reporting, advanced security — merged into the single public repo. The org adds **thingsboard-gateway** (2,150 ★ — Modbus, CAN bus, BACnet, BLE, OPC-UA, MQTT, ODBC, REST for legacy/industrial gear), **tbmq** (736 ★ — distributed MQTT broker on Kafka claiming 100M+ connections), **thingsboard-edge** (167 ★), Flutter mobile app (301 ★) and client SDKs (202 ★).

**City relevance.** ThingsBoard ships an official **"Air quality monitoring" Solution Template** explicitly marketed as "your accelerator for Smart City environmental initiatives": a simulated Los Angeles deployment with district-level AQI sensors, calculated fields converting PM2.5/NO2/O3 to AQI per EPA breakpoints, a public citizens dashboard (no login), an admin command centre with battery/connectivity alarms, and ThingsBoard Edge support for remote districts.

**Structure & quality signals.** Large monorepo with Java/TS/SQL/Dockerfile, 247 open PRs, 8,109 closed issues, extensive docs (thingsboard.io), Docker images, deb/rpm packages, CI, 96 releases. Ranked #84 among 35,154 Java repos by watchers.

**Install/deps.** Docker (single/all-in-one or microservice compose), deb/rpm, or binaries; Cassandra/PostgreSQL (CE: embedded or Postgres/HSQL), Kafka (PE/tbmq), Redis for some components.

**Best fit.** A city **sensor ingestion + dashboard + alarm backbone** for air quality, street lighting, water, parking pilots; industrial/legacy protocol conversion via the gateway; edge/fog deployments for districts.

**Limitations.** **Licence nuance matters for research/commercialisation:** BUSL-1.1 free tier = non-commercial up to 1,000 devices across servers with branding intact; commercial up to 100 devices on one server with branding; beyond that (or removing branding) you need a paid licence (releases open up to Apache-2.0 after four years). Large issue backlog (393 open issues).

**VERDICT: essential** — the most complete open-core city IoT platform; just model the BUSL constraints in any tech-transfer plan.

## 2.2 `emqx/emqx` — EMQX, the scalable MQTT broker

- **URL:** https://github.com/emqx/emqx
- **Stars/forks:** **16,856 ★ / 2,569 forks** (ranked #1 among Erlang repos on GitHub) · **Language:** Erlang/OTP (with the project's own OTP fork `emqx/otp` required for builds), C, Python bits · **Licence:** **BSL-1.1 since v5.9.0** (previously Apache-2.0; clustering with v5.9.0+ requires a license file) · **Recency:** last commit ~3 days before 5 Nov 2026; 37,704 commits; latest releases **6.3.1 (18 Sep 2026)** and Enterprise LTS 6.3.2 (16 Oct 2026); 12,511 PRs merged · **Maintainer:** EMQ Technologies (Germany/China).

**What it implements.** A high-performance IoT messaging platform: **MQTT 5.0/3.1.1/3.1, MQTT-SN, CoAP, LwM2M gateways, and MQTT over QUIC**; SQL-based rule engine for in-flight filtering/transformation; 50+ data bridges (Kafka, RabbitMQ, Pulsar, PostgreSQL, ClickHouse, InfluxDB, AWS/GCP/Azure, webhooks); Flow Designer (drag-and-drop pipeline orchestration); durable message queue with TTL/last-value semantics; masterless clustering with Cluster Linking. Claimed scale: 100M+ concurrent MQTT clients per cluster, millions of msgs/sec at sub-millisecond latency — the numbers usually cited for **city-scale (and vehicle-scale) telemetry backbones**; its own README lists "smart cities" as a target domain.

**Structure & quality signals.** Topics include lorawan, lwm2m, coap, iiot; massive release cadence (402 releases); repo health monitors record commits within a day; docs/emqx.com; Docker images, Helm charts, Terraform modules.

**Install/deps.** Docker/Kubernetes/Helm; building from source requires the EMQX Erlang fork (`.tool-versions`, e.g. erlang 27.3.4.2-9) — upstream Erlang builds are unsupported.

**Best fit.** City-scale MQTT/CoAP/LwM2M ingest where Mosquitto is too small; protocol gateway unification; data-plane integration with lakehouses for urban analytics.

**Limitations.** **BSL-1.1 is not OSI open source** — review LICENSE before redistribution or multi-node production use; build toolchain is fork-specific; license change (Apr 2025 initial, reaffirmed Sep 2026) may affect grant-funded reproducibility claims.

**VERDICT: essential** (with a licence footnote) — the performance reference for large IoT message backbones.

## 2.3 `node-red/node-red` — low-code flow programming for IoT

- **URL:** https://github.com/node-red/node-red
- **Stars/forks:** **23,783 ★ / 3,936 forks** (23,816 by 4 Nov 2026 snapshot) · **Language:** JavaScript/Node.js · **Licence:** Apache-2.0 (OpenJS Foundation; originally IBM Emerging Technology) · **Recency:** v5.0.9 released 21 Oct 2026; last push ~1 week before this research; 240 contributors; ~96k weekly npm downloads · **Maintainers:** Nick O'Leary, Dave Conway-Jones and community.

**What it implements.** A visual, event-driven flow runtime for wiring hardware devices, APIs and services — the classic "glue" layer of IoT: MQTT in/out nodes, HTTP endpoints, function nodes, dashboard nodes, social/E-mail connectors, and a palette manager with thousands of community nodes. Monorepo of the main Node-RED modules; flows are JSON, versionable and importable.

**Structure & quality signals.** 5.0 release line (June 2026 onward), Contribution Covenant, funding/sponsorship, Snyk health score 84/100 ("Popular, Healthy, Active"), docs at nodered.org, Docker image, `npm install -g node-red` install.

**Best fit.** Rapid prototyping of **city sensor pipelines** (LoRaWAN MQTT → enrich → database), hackathons, teaching, small municipal deployments (weather/AQ stations, smart bins), and bridging legacy HTTP APIs into a unified event bus.

**Limitations.** Flow-based programming scales poorly for very large teams/complex logic (that is where ThingsBoard rule chains or Kafka come in); core repo is Apache-2.0 but many high-value nodes are vendor-licensed; performance is single-process Node.

**VERDICT: essential** — the default prototyping/integration layer in nearly every city IoT pilot.

## 2.4 `eclipse-mosquitto/mosquitto` — the default lightweight MQTT broker

- **URL:** https://github.com/eclipse-mosquitto/mosquitto
- **Stars/forks:** **~11,300 ★ / ~2,660 forks** · **Language:** C/C++ · **Licence:** **EPL-2.0 OR BSD-3-Clause** (dual; GitHub shows "Other") · **Maintainer:** Eclipse Foundation (iot.eclipse.org project), development driven by **Cedalo**; org page shows the main repo updated May 2026 · **Recency:** active maintenance; ~900 open issues (long tail).

**What it implements.** An open-source server for **MQTT 5.0, 3.1.1 and 3.1** plus a C/C++ client library and the ubiquitous `mosquitto_pub`, `mosquitto_sub`, `mosquitto_rr`, `mosquitto_ctrl`, `mosquitto_passwd` tools. Lightweight enough for single-board computers — the near-universal choice for gateways, Raspberry-Pi-class city sensor nodes and lab testbeds. Companion `mosquitto.rsmb` (95 ★) implements a really small message broker for embedded use. Mosquitto is explicitly named as a device-connectivity layer in Eclipse Ditto's architecture (see 3.3).

**Best fit.** Edge/gateway brokers in city sensor networks; teaching MQTT; local brokers for digital-twin device emulation; anywhere an OSI/Eclipse licence is required (unlike EMQX/ThingsBoard's BSL).

**Limitations.** Single-node by default (HA/clustering and enterprise integrations are Cedalo Pro features); ~900 open issues indicate slower triage; no built-in rules engine or dashboard.

**VERDICT: essential** — the safe-permissive MQTT default for city pilots and research artefacts.

## 2.5 `chirpstack/chirpstack` — open-source LoRaWAN network server

- **URL:** https://github.com/chirpstack/chirpstack
- **Stars/forks:** 1,123 ★ / 294 forks (org: 21 repos, 269 followers) · **Language:** Rust · **Licence:** MIT · **Recency:** last commit ~17 hours before 5 Nov 2026; **v4.20.0 released 21 Oct 2026**; 52 releases; 222 PRs merged · **Maintainer:** Orne Brocaar / ChirpStack project (sponsor-supported).

**What it implements.** A complete **LoRaWAN Network Server**: gateway/device/tenant management web UI, de-duplication of uplinks, downlink scheduling, class A/B/C handling, multi-tenancy, and data integrations to major clouds, databases and services (MQTT, AWS IoT Core, Azure, PostgreSQL/TimescaleDB, InfluxDB…), plus a **gRPC API** for integration/extension. The v4 monorepo supersedes the archived `brocaar/chirpstack-network-server` (1,512 ★, **ARCHIVED** — migration guide provided). Ecosystem repos: `chirpstack-gateway-bridge` (447 ★, abstracts packet-forwarder protocols to Protobuf/JSON over MQTT), `chirpstack-docker` (372 ★), `chirpstack-gateway-os` (160 ★, OpenWrt gateway images), `chirpstack-concentratord` (103 ★, HAL daemon), ansible playbook (89 ★).

**Best fit.** Building a **city-wide LoRaWAN network** for environmental/parking/waste/traffic sensors; academic testbeds needing a standards-compliant NS; multi-tenant municipal networks (one NS, many tenants/departments).

**Limitations.** LoRaWAN only (no cellular/NB-IoT); MIT-licensed core but operations (gateways, spectrum, backhaul) remain your problem; 45 open issues; mid-size community — bus-factor risk on a single lead maintainer (sponsorship model acknowledged in README).

**VERDICT: essential** — the open default for city LoRaWAN deployments (vs. proprietary TTN-enterprise or vendor NS).

## 2.6 `RIOT-OS/RIOT` and `contiki-ng/contiki-ng` — sensor-node operating systems

**RIOT-OS/RIOT** — https://github.com/RIOT-OS/RIOT · **5,831 ★ / 2,113 forks** · C/C++ (plus Makefile, Rust/Lua bits) · **LGPL-2.1** · created Dec 2012 · quarterly releases (**RIOT-2026.07**) · ~298 contributors, 78 boards, 289 commits per release cycle · homepage riot-os.org.
Implements a multi-threaded, energy-efficient RTOS for 8/16/32-bit microcontrollers with soft real-time support, small footprint, uniform APIs (partial POSIX), and open-standard networking (6LoWPAN, CoAP, MQTT-SN-class stacks) independent of vendor. Independent, community-governed ("the Linux of the IoT"), with a stated preference for free components (some ESP WiFi blobs excepted). Install: `git clone` + `make` with the board toolchain; releases as tarballs. **Use case:** firmware for city-deployed sensor nodes where you need a general-purpose OS, many MCU families and active development. **Limitation:** LGPL obligations for proprietary linking (mostly fine, but read it), large open-issue backlog (908). **VERDICT: useful.**

**contiki-ng/contiki-ng** — https://github.com/contiki-ng/contiki-ng · **1,540 ★ / 788 forks** · C · **BSD-3-Clause** · created May 2017 (fork of Contiki OS) · `develop` branch · 281 open issues.
Implements "the OS for Next Generation IoT devices" focused on **dependable low-power communication and standard protocols: IPv6/6LoWPAN, 6TiSCH, RPL, CoAP**, with extensive documentation/tutorials and — its unique research asset — the **Cooja network simulator** tightly integrated. The official RIOT website's comparison states it directly: Contiki-NG has a smaller community and codebase, is **research-steered by computer-science researchers**, supports fewer boards but has a sophisticated network stack and a polished simulator; RIOT has broader hardware support. **Use case:** reproducing wireless-sensor-network/6TiSCH papers, simulated city WSN experiments, permissive-licence firmware. **Limitation:** fewer boards, research-driven roadmap. **VERDICT: useful** (choose RIOT for hardware breadth, Contiki-NG for simulation/protocol research).

## 2.7 `eclipse-hono/hono` — device connectivity abstraction (Eclipse IoT)

- **URL:** https://github.com/eclipse-hono/hono · **500 ★ / 147 forks** · Java · **EPL-2.0** · created Feb 2016 · **Last release 2.4.1: 17 November 2023** (project status: "Mature" at projects.eclipse.org).

**What it implements.** Uniform remote service interfaces for connecting **large numbers of IoT devices to a cloud backend**, independent of the device protocol: telemetry ingestion and command & control messaging, device identity/provisioning and access-control management, protocol adapters for **CoAP, HTTP, MQTT, Kafka-facing northbound APIs**, and tenant-based federation of cloud services. Hono is the "device connectivity" half of the Eclipse IoT architecture paired with Ditto (digital twins).

**Best fit.** Architecture research on multi-protocol device gateways; FIWARE/Eclipse-adjacent smart-city stacks needing protocol-agnostic ingestion with per-tenant isolation.

**Limitations.** **Release activity stopped in late 2023**; modest star count; Java/Kubernetes complexity for what a broker+gateway can often do; Eclipse "Mature" status can precede archival. **VERDICT: niche** — architecturally instructive, but verify community momentum before adopting.

## 2.8 `eclipse-californium/californium` — CoAP/DTLS for Java

- **URL:** https://github.com/eclipse-californium/californium · **779 ★ / 378 forks** · Java · **EPL-2.0 OR BSD-3-Clause** (shown as "Other") · created Sep 2015 · Eclipse metrics: 24 commits by 2 people in the last 12 months; release cadence 3.x (3.14.0, March 2025) with 4.0.0 milestones (M6, Aug 2025) · top contributors: boaks, sbernard31, jvermillard.

**What it implements.** A Java implementation of **RFC 7252 CoAP** for IoT cloud services (scalability/usability focus rather than embedded resource-efficiency), including the **Scandium DTLS** implementation (DTLS 1.2, experimental 1.3), OMA LwM2M/oneM2M integration hooks, an Actinium app-server, demo/test apps, and a public **interop server** at `coap://californium.eclipseprojects.io:5683`. Artifacts on Maven Central.

**Best fit.** Building CoAP/DTLS endpoints for constrained city devices behind a Java gateway; interoperability testing; LwM2M-based device management research.

**Limitations.** Low commit volume (24 commits/12 months across the project) — maintenance mode rather than rapid development; cloud-oriented rather than embedded; small contributor base.

**VERDICT: useful** — the standard Java CoAP stack, with a "check the release calendar" caveat.

## 2.9 `home-assistant/core` and `openhab/openhab-core` — building/campus-level automation in a city context

**home-assistant/core** — https://github.com/home-assistant/core · **~92,000 ★ / ~39,211 forks** · Python · **Apache-2.0** · 5,406 contributors, 122,681 commits, last commit 6 Nov 2026, release 2026.10.4 / 2026.11.0 line · integration-heavy monorepo (`homeassistant/`, `tests/`, `script/`, `machine/` for images, strict-typing lists, pre-commit, codecov).
Implements local-first home/building automation with thousands of integrations, dashboards, automations and companion apps. **City relevance:** the largest community sensor/actuator aggregation platform — routinely used to aggregate air-quality, energy, noise and occupancy feeds in living labs, campus buildings and retrofit pilots; its MQTT/HTTP integrations plug directly into Mosquitto/EMQX city backbones. **Limitations:** designed for single-household/single-site scale, not multi-tenant city operations; Python release cadence (monthly) creates upgrade churn. **VERDICT: useful.**

**openhab/openhab-core** — https://github.com/openhab/openhab-core · **1,157 ★ / 473 forks** · Java/OSGi (Xtend/Groovy) · **EPL-2.0** · last commit 4 Nov 2026 · 385 open issues.
The core runtime of openHAB (project first released 2010): vendor-neutral bindings, text-file "things/items/rules" configuration, Rules DSL/JS/Blockly, add-ons distribution. **City relevance:** the JVM alternative for building/campus pilots where text-based config and long-term stability are valued; same MQTT/HTTP bridging story as Home Assistant. **Limitations:** smaller community (~1/80th the stars), steeper learning curve. **VERDICT: niche-to-useful** — choose if your lab is Java-centric.

*(Related, covered under ThingsBoard: `thingsboard/thingsboard-gateway` 2,150 ★ for Modbus/BACnet/OPC-UA/BLE protocol conversion — often the piece that makes city deployments "work" with existing municipal infrastructure.)*

# CATEGORY 3 — DIGITAL TWINS (urban/city twins and DT frameworks)

## 3.1 `CesiumGS/cesium` — CesiumJS, the 3D geospatial web runtime

- **URL:** https://github.com/CesiumGS/cesium
- **Stars/forks:** **15,911 ★ / 3,894 forks** (daily snapshots Aug–Nov 2026 climbed 15,567 → 15,890+) · **Language:** TypeScript/JavaScript (plus GLSL, CSS) · **Licence:** Apache-2.0 · **Created:** March 2012 · **Recency:** last push ~2 days before this research; ~1,758 open issues (high but typical for a large client library) · **Maintainer:** CesiumGS (AGL — 67 public repos, 1,817 followers, Philadelphia).

**What it implements.** A JavaScript library for creating **3D globes and 2D maps in the browser without plugins**, WebGL-accelerated, WGS84-precision, built on open formats: **3D Tiles, glTF, CZML** (time-dynamic), KML/GeoJSON. It is the rendering backbone of most open web-based city digital twins: terrain/imagery/3D Tiles streaming, dynamic sensor/entity visualisation, picking, and analysis. Open-core: the runtime is Apache-2.0 while tiling/hosting is sold via Cesium ion (bring-your-own data is supported). Ecosystem: **cesium-unreal** (1,207 ★) for game-engine twins, **cesium-native** (606 ★) C++ core, gltf-pipeline (2,121 ★), obj2gltf (1,846 ★).

**Structure & quality signals.** npm package with release cadence, extensive documentation site, Sandcastle examples, community forum, CI. Ranked as one of the largest JS geospatial repos.

**Install/deps.** `npm install cesium`; needs a bundler (Vite/webpack) for modern builds; data served as 3D Tiles/glTF/CZML from any static host or ion.

**Best fit.** Any **city 3D web viewer**, digital-twin front end, sensor-over-3D dashboards, and visualisation of CityGML-derived tiles (e.g., via 3DCityDB exporters → 3D Tiles).

**Limitations.** Rendering framework, not a twin (no state model, no IoT sync); ion is a paid service (mitigated by BYO data); large issue backlog; Apache-2.0 but trademarked name.

**VERDICT: essential** — the default web renderer for urban digital twins.

## 3.2 `CesiumGS/3d-tiles` — the 3D Tiles specification

- **URL:** https://github.com/CesiumGS/3d-tiles · **2,629 ★ / 501 forks** · Language: specification (JSON/Markdown) · Licence: Apache-2.0 (spec repo) · created June 2015 · active (spec versions 1.0 → 1.1).

**What it implements.** The open specification for **streaming massive heterogeneous 3D geospatial datasets**: tilesets, bounding volumes, geometric/screen-space error, and tile formats combining photogrammetry/massive models, BIM/CAD, 3D buildings, instanced features and point clouds (glTF-based `b3dm`-successor payloads, `pnts`, `i3dm`, `cmpt`, plus implicit tiling). Endorsed as an OGC Community Standard; it is how city models (CityGML/CityJSON/BIM) become web-streamable, and how twins push incremental updates.

**Best fit.** Citing the standard; designing tile pipelines for city models; evaluating level-of-detail/streaming performance in twins research.

**Limitations.** A **specification repo, not software** — you need CesiumJS/native or another runtime to implement it; open issues track spec discussion rather than bugs.

**VERDICT: essential** — the interoperability contract for 3D city content delivery.

## 3.3 `eclipse-ditto/ditto` — Eclipse Ditto, the IoT digital-twin framework

- **URL:** https://github.com/eclipse-ditto/ditto
- **Stars/forks:** **941 ★ / 293 forks** · **Language:** Java (plus Scala/JS/TS for things like the UI and JSON templates) · **Licence:** EPL-2.0 · **Created:** April 2017 · **Recency:** last push 13 hours before snapshot (health monitors: updated 6 days prior, 736 commits in last 12 months, 100 releases, 61 contributors, health index 96/100) · **Maintainer:** Eclipse IoT (Bosch-affiliated origin, broad adopter list).

**What it implements.** The reference **"digital twin" middleware pattern for IoT**: virtual representations of real-world things (sensors, smart heating, connected cars, **smart grids, EV charging stations**) with:
- desired / reported / current **state management** and synchronisation;
- **WoT (W3C Web of Things)** integration and JSON-LD context handling;
- fine-grained, resource-based **access control** on twin sub-paths;
- **connections** to foreign systems over AMQP 0.9.1/1.0, Kafka, HTTP webhooks, MQTT 3.1.1/5 with payload mapping;
- twin search, events (SSE/WebSocket), batch APIs, and managed dual-write to devices via a connectivity layer (Eclipse Hono or MQTT brokers like Mosquitto).

Domain-agnostic by design — "industrial, residential, agricultural and other IoT domains" — which makes it the device/asset-level twin layer beneath a city-scale twin (the city twin holds entities; Ditto holds live device twins).

**Structure & quality signals.** Maven multi-module (`org.eclipse.ditto` artifacts on Maven Central, current line v3.7.6, 108 total versions), docker-compose local start, CONTRIBUTING + Code of Conduct (issue/PR templates absent), documentation site (eclipse.dev/ditto), 110 open issues.

**Install/deps.** JDK ≥ 25, Maven ≥ 3.9, running Docker daemon (services: MongoDB, connectivity, gateway, things, policies).

**Best fit.** Building the **device-twin layer of a smart-city platform** (streetlights, chargers, meters): state sync, command routing, per-tenant policies; research on twin synchronisation semantics; integration patterns between twins and Kafka/MQTT city backbones.

**Limitations.** Heavy JVM/K8s-style deployment for small pilots; not a 3D/geo twin (no map/CityGML); learning curve around policies/connections; star count modest vs. platform mindshare (Eclipse projects often under-star).

**VERDICT: essential** — the canonical open digital-twin framework; pair with Cesium (visual) and a context broker (semantic city layer).

## 3.4 `Azure/opendigitaltwins-dtdl` — Digital Twins Definition Language (DTDL)

- **URL:** https://github.com/Azure/opendigitaltwins-dtdl · **578 ★ / 180 forks** · Language: spec (Markdown/JSON-LD) · **Licence: CC-BY-4.0** · created April 2019 · **Maintainer:** Microsoft (community contributions welcome) · 34 open issues.

**What it implements.** The **DTDL modelling language** for IoT digital twins: a JSON-LD/RDF-based vocabulary of metamodel classes — Interface, Telemetry, Property, Command, Relationship, Component — plus schema primitives and (v3+) geospatial schemas and interface schemas. Versions: v1 (out of support), **v2** (Azure Digital Twins, IoT Central, IoT Plug and Play), **v3** (ADT + PnP; context `dtmi:dtdl:context;3`), **v4** (Azure IoT Operations). Semantic annotations allow analytics/ML to reason about units and meaning (e.g., "temperature" vs `double`). Tooling: **DTDLParser for .NET (NuGet)**, VS Code extension, Azure IoT Explorer; SDKs for data-plane operations live in `Azure/azure-sdk-for-*` (`azure-digitaltwins-core` in .NET/Java/JS/Python).

**Best fit.** Modelling **asset/space twins** (buildings, floors, rooms, devices) in a vendor-neutral JSON-LD way; comparing DTDL vs CityGML vs NGSI-LD for semantic coverage; academic work on twin modelling languages (the language itself is open even if the platform is not).

**Limitations.** Spec + parser, not a twin runtime; deep coupling with Azure services in practice; CC-BY licence means attribution obligations for derivative specs; multi-tenant city deployments require the (commercial) Azure Digital Twins service unless you self-host equivalents.

**VERDICT: useful** — the most widely deployed twin modelling language; cite it in any DT-modelling survey, but don't confuse the open spec with the cloud service.

## 3.5 `Urban-Model-Platform/urban-model-platform` — OGC API - Processes for urban-twin models

- **URL:** https://github.com/Urban-Model-Platform/urban-model-platform · **28 ★ / 6 forks** · **Python** · **GPL-3.0** · created June 2023 · homepage docs site · 11 open issues.

**What it implements.** An open **Urban Model Platform** implementing the **OGC API - Processes** standard to distribute and access simulation models in an **urban digital twin**: a Python "system of systems" that federates multiple model providers/model servers instead of executing jobs locally — ranging from simple regression models to advanced simulation and AI models. Developed by the **City Science Lab at HafenCity University Hamburg** together with the **Agency for Geoinformation and Surveying (LGV) Hamburg** in the context of the EU/regional **Connected Urban Twins (CUT)** project.

**Paper/project linkage.** Directly tied to the Connected Urban Twins programme and OGC API - Processes standardisation — a citable implementation of "model federation as a service" in urban twins.

**Best fit.** Researchers integrating **what-if simulation models** (mobility, energy, noise, microclimate) behind a standards-based API in a twin; European smart-city project replication.

**Limitations.** 28 stars / ~6 forks — a small academic user base; GPL-3.0; provider-side deployment complexity; docs-heavy rather than batteries-included.

**VERDICT: useful** — a standards-clean way to wire simulation models into a twin; cite even if you roll your own orchestration.

## 3.6 `mkturkcan/valdrada` — a real-time city-scale digital twin of New York City

- **URL:** https://github.com/mkturkcan/valdrada
- **Stars/forks:** **~253–261 ★ / 37 forks** (261 ★ by 5 Nov 2026 snapshot; author's CV cites 258★ in six weeks) · **Language:** Python (server/API) + TypeScript/WebGL2 (client) + Unreal Engine 5 module · **Licence:** code MIT; compiled city ODbL (OSM-derived); docs/figures CC-BY-4.0; vehicle/ped models CC-BY-4.0 (CARLA), some MIT (Rocketbox); textures CC0 · **Created:** 24 September 2026 · **Recency:** extremely active — ~39+ commits, last commit ~12 hours before snapshot; releases through 0.6.x · **Maintainer:** Mehmet Kerem Turkcan (Associate Research Scientist, Columbia University; urban perception/physical AI).

**What it implements.** A city-scale twin **compiled from public municipal records**: all five NYC boroughs, **1,085,937 buildings** (NYC Building Footprints joined to PLUTO use/class/floors/year and facade-inspection filings), street centerline (CSCL) turned into a routable **lane graph** with widths/lane counts/speed limits, street furniture from records (trees, hydrants, kiosks, subway entrances), detailed districts (125th Street, Central Park with 16,951 trees, Midtown towers, Statue of Liberty). Technical core: real-time **WebGL2 renderer** with binary tile streaming; **lane-level traffic simulation** (IDM car-following, signal phases, pedestrians on sidewalk graphs, NYC fleet/MTA metro); **pixel-exact perception ground truth** (RGB, semantic segmentation Cityscapes-compatible, instance/amodal 3D boxes, metric depth); a **CARLA-modelled client–server API** (TCP + Python client with synchronous stepping, sensors, map queries); export of recorded takes to **OpenUSD** rendered in Blender Cycles/UE5; a packaged UE5 renderer; browser client. Intended for synthetic data generation, closed-loop scenario simulation and streetscape studies.

**Paper linkage.** Companion/derivative of the author's **"Boundless: Generating Photorealistic Synthetic Data for Object Detection in Urban Streetscapes" (arXiv:2409.03022, 2024)** and urban-perception works (e.g., *A Vision-Based Analysis of Congestion Pricing in New York City*, arXiv:2602.03015; edge video analytics, ACM/IEEE SEC 2025 Best Paper), developed alongside NYC testbed deployments (COSMOS PAWR, DataCity, FAU MobIntel).

**Structure & quality signals.** `server/`, `client/`, `core/`, `src/`, `ue_client/`, `PythonAPI/`, `tools/`, `space/`, `docs/` (MkDocs), `BUILDING.md`, `LICENSING.md` (careful licence split), GitHub Actions workflows, recent tags/releases — a rare example of clear multi-licence documentation for a city-scale asset.

**Best fit.** **Urban perception & sim-to-real research**: training/validating detectors and trackers with ground truth; synthetic-data generation for autonomous mobility; scenario replay of city streetscapes; a reference for "how to compile a city from open records."

**Limitations.** One month old at research time — API still moving (0.6.x); heavy data/asset pipeline (UE5 + compiled tiles) to reproduce; NYC-specific; not a live IoT twin (public-record-compiled, with simulation rather than sensor sync); GPU needed for rendering paths.

**VERDICT: essential (for urban AI/perception research)** — the most ambitious open city-scale twin to appear in 2026; treat as fast-moving.

## 3.7 Other urban-twin repos (smaller, project-tied)

**`destination-earth/DestinE_ESA_CityNexus`** — 6 ★ / 3 forks, **Apache-2.0**, created Nov 2023 (ESA/Destination Earth ecosystem). **CITYNEXUS**: an urban digital-twin application assessing environmental/social/economic impacts of changes to road networks, mobility and urban-space design — baseline indicators (air quality, population distribution, public health, accessibility) plus live **what-if scenario** simulation, KPI dashboards for policymakers. Demo cities: **Copenhagen, Bologna, Seville, Aarhus**; explicitly positioned for the **EU Mission 100 Climate-Neutral & Smart Cities by 2030**. **VERDICT: niche** — program-linked (DestinE), low repo activity; valuable for Mission-cities scenario-methodology comparisons.

**`paramountric/digitaltwincityviewer`** — 17 ★ / 7 forks, **MIT**, created Feb 2022. **Digital Twin City Viewer** from the **Digital Twin Cities Centre (DTCC) at Chalmers University of Technology** (DTCC Platform): an open toolkit for collaborative right-time city data on the web using shared data layers and open geospatial exchange standards; developed 2022–2024, README notes follow-up projects "eventually end up here" — i.e., **development has paused**. **VERDICT: niche (archival research output)** — good for studying DTCC's standards-based approach; don't expect new releases.

**`phungdo/BoMoDT`** — 0 ★ (fork), **AGPL-3.0**, created January 2026. **Bologna Mobility Digital Twin**: model-driven architecture (with an automated model-to-model transformation tool, **MoDT-M2M-MTT**) combining **FIWARE** generic enablers (Smart Data Models, semantic interoperability) with **Eclipse SUMO** traffic simulation; provides digital representation + state simulation, **bidirectional synchronisation** (physical sensors → twin → traffic-light feedback), and monitoring via Django + Grafana. Inputs: Bologna open data + OpenStreetMap (road network, induction loops, traffic lights). **VERDICT: niche** — a well-documented academic mobility-twin artefact; check upstream maintenance before depending on it.

**`FARI-brussels/Fari-Brussels-Digital-Twin-Unity`** — 1 ★, created May 2025, no licence file reported in snapshot. Unity + **Cesium for Unity** digital twin of Brussels (TrafficTwin): real-time visualisation/simulation of mobility scenarios with live open-API data. **VERDICT: avoid-stale (prototype)** — interesting institutionally (FARI — AI for the Common Good, Brussels), but repository-grade is prototype-level.

**`c-toolbox/Digital-Twin-City-Platform-UE-Public`** — 0 ★, created Feb 2026, Linköping University. Public releases of an **Unreal Engine 5.6** Digital Twin City Platform for Norrköping (C++/Blueprint, WebSocket-controlled pawn, JSON request protocol in the Wiki, SWEREF99TM extents documented). Windows/VS2022-only. **VERDICT: niche (too early)** — watch for the private-repo feature set to mature.

**`atenearesearchgroup/public-transport-system-dt`** — 0 ★, created May 2023, University of Málaga. Urban Digital Twin of a public-transport system over the **Cloud-to-Thing Continuum**: metamodel + object model, bus-line simulation with 60-second ticks. **VERDICT: niche** — model/method artefact for UDT-over-C2T papers; code presence minimal.

---

# CATEGORY 4 — EDGE / 6G / CITY ARCHITECTURE

## 4.1 `kubeedge/kubeedge` — Kubernetes-native edge (CNCF graduated)

- **URL:** https://github.com/kubeedge/kubeedge
- **Stars/forks:** **7,612 ★ / 2,034 forks** · **Language:** Go (plus Python/Shell) · **Licence:** Apache-2.0 · **Created:** September 2018 · **Recency:** active; CNCF **graduated** project (top tier) · **Maintainer:** CNCF (originally Huawei; broad community) · **1,341 open issues** (notable backlog).

**What it implements.** Extends Kubernetes orchestration to edge hosts with a **cloud part (CloudCore) and edge part (EdgeCore)**: networking, application deployment and metadata synchronisation between cloud and edge; **MQTT** device access through edge nodes; **DeviceMapper/Device CRD** framework for IoT devices; edge autonomy (local metadata persistence so nodes recover fast without list-watch when the link is down); memory footprint down to ~70 MB; support for x86/ARMv7/ARMv8; offline-tolerant operation — exactly the requirements of city infrastructure (cameras, meters, gateways on unreliable links).

**Structure & quality signals.** Go Report Card, CII Best Practices badge, releases via GitHub, docs site kubeedge.io, Chinese/English docs, `keadm` installer.

**Install/deps.** `keadm` CLI or Helm; needs a Kubernetes control plane (K3s/K8s) + edge nodes; MQTT broker (Mosquitto etc.) for device paths.

**Best fit.** **Edge-cloud architecture for city services**: running vision/analytics models next to intersections, caching twin state offline, district-level autonomy; baseline for papers comparing edge orchestration frameworks.

**Limitations.** Large open-issue backlog (1,341); operational complexity; device-management model is its own CRD (vs OpenYurt's EdgeX bridge).

**VERDICT: essential** — the CNCF-graduated default for Kubernetes-at-the-edge in city testbeds.

## 4.2 `openyurtio/openyurt` — vanilla-K8s edge (CNCF incubating)

- **URL:** https://github.com/openyurtio/openyurt · **1,968 ★ / 428 forks** · Go · **Apache-2.0** · created May 2020 · **latest release v1.7.0 (6 May 2026)** · CNCF **Incubating** · maintainer: CNCF (originally Alibaba).

**What it implements.** A cloud-edge orchestration layer that **preserves intact upstream Kubernetes API compatibility** and is vendor-agnostic: **YurtHub** (node-side kubelet/kubeproxy request proxy with local cache for edge autonomy), **Yurt-Manager** (controllers/webhooks for edge), **Raven-Agent** (L3 pod connectivity across regions/edge sites), **YurtIoTDock** (bridges **EdgeX Foundry** devices into K8s CRDs), plus **NodePool**/region-aware deployment and unified management across "pools" of edge sites. Positioned as SIMPLE relative to KubeEdge.

**Best fit.** City edge clusters where you already operate vanilla K8s and want region-aware (district-level) deployment with autonomy; integration points with EdgeX device services.

**Limitations.** Fewer stars/community than KubeEdge; device story depends on EdgeX integration; 23 open issues (healthy triage).

**VERDICT: useful** — the "keep vanilla K8s" alternative; evaluate side-by-side with KubeEdge for city edge pilots.

## 4.3 `edgexfoundry/edgex-go` — EdgeX Foundry device/edge middleware (Linux Foundation)

- **URL:** https://github.com/edgexfoundry/edgex-go · **1,548 ★ / 521 forks** · Go (monorepo; container-heavy build) · **Apache-2.0** · created January 2018 · **Recency:** active; `main` branch is explicitly WIP toward the next release (stable code at Releases); LFX Insights: org-wide **3,077 GitHub stars, 3,288 forks, 32 quarterly active contributors, active 330/365 days, avg issue resolution 14 days, healthy score** · **Maintainer:** The Linux Foundation / EdgeX Foundry.

**What it implements.** A **vendor-neutral, hardware- and OS-agnostic IoT edge interoperability framework**: core services (metadata, data, command/config), **device services** (protocol plugs: Modbus, BACnet, MQTT, BLE, OPC-UA…), application services for northbound filtering/export (to MQTT, Kafka, cloud, DBs), message bus (Redis/MQTT/NATS-era history), REST APIs, and Docker Compose packaging (`edgex-compose`, 114 ★) with per-release branches. It is the standard "southbound" layer connecting municipal OT (BACnet building systems, Modbus meters) to modern apps.

**Best fit.** City edge gateways needing **protocol-agnostic device abstraction**; research on edge data pipelines; the device half of an OpenYurt/EdgeX stack.

**Limitations.** The `main` branch is unstable by policy (use release branches/tags); Go monorepo with many microservices = deployment weight; star count split across many repos in the org.

**VERDICT: useful** — the reference edge device-framework; standard in Linux-Foundation-aligned city pilots.

## 4.4 `UCY-LINC-LAB/fogify` (+ `5G-Slicer`) — paper-linked fog/5G emulation for city scenarios

**fogify** — https://github.com/UCY-LINC-LAB/fogify · **32 ★ / 9 forks** · Python · **Apache-2.0** · created May 2019 · maintainer: Laboratory for Internet Computing (LInC), University of Cyprus.
Implements an **emulation framework for fog/edge testbeds**: model complex fog topologies (heterogeneous resources, network QoS), deploy them via containerised infrastructure-as-code (extended Docker Compose "fogified" model) to cloud or local environments, then experiment with **fault injection, runtime scaling, workload/network adaptation and data-movement restrictions** for what-if analysis. **Paper linkage & awards:** Fogify received the **Best Demo Award at IEEE/ACM Symposium on Edge Computing 2020**; its **5G-Slicer extension (16 ★)** — an emulator for mobile IoT over 5G network slices with radio units, trajectories and runtime signal-strength QoS, including a **ready-to-use city-scale transportation template** — won **Best Paper at IEEE/ACM IoTDi 2022**; featured on the European Commission Innovation Radar. A companion `fogify-demo` (9 ★) shows Jupyter-integrated geo-distributed fog experiments.

**Best fit.** Reproducing edge/fog/5G-slice experiments when you lack a real city testbed; benchmarking latency/availability of city services under emulated conditions; teaching edge computing.

**Limitations.** Small community (32 ★), academic "as-is" maintenance disclaimer; emulation ≠ real radio; 5G-Slicer is separate and even smaller.

**VERDICT: niche/useful** — one of the few *reproducible, paper-linked* edge/5G city-experiment toolkits on GitHub; cite and use where a physical testbed is out of reach.

## 4.5 O-RAN / 5G city stacks on GitHub

**`o-ran-sc` (O-RAN Software Community org)** — https://github.com/o-ran-sc · **151 public repos, 281 followers**; **Apache-2.0**; languages C++, Go, Python.
Implements the **near-RT RIC platform and O-RAN components**: xApp framework, **E2 (southbound to O-DUs/gNBs), A1, O1/O2** interfaces, non-RT RIC (`nonrtric` 18 ★), O-DU L2 (`o-du-l2` 30 ★), O-DU PHY (`o-du-phy` 24 ★), deployment (`ric-plt-ric-dep` 8 ★) with Helm/Kubernetes install guides. **Important nuance:** canonical development happens on **Linux Foundation Gerrit** (`gerrit.o-ran-sc.org`); GitHub repos are **mirrors** — hence star counts of 5–30 are meaningless as health signals (commits updated March 2026, 20 contributors per repo typical). CII best-practices status: met for near-RT RIC.

**Best fit.** Research on **open RAN for city/neutral-host networks**, private 5G for municipalities, xApp-based radio optimisation.

**Limitations.** Steep telecom-domain learning curve; Kubernetes+Helm heavy; mirror-repo confusion; GitHub stars not representative. **VERDICT: niche** (essential only if RAN/spectrum is your research domain).

**`edwardkeith-io/ORAN-Project`** — 2 ★, created May 2024, capstone project **replicating arXiv:2205.13178**: an open-source 5G small-cell base station using **srsRAN (SRSeNB/SRSEPC/SRSUE) + Ettus B205-mini SDR** in Docker on Ubuntu 22.04, with replication documentation (ping/SSH/web-server validation over the air). README explicitly lists **smart-city infrastructure** (traffic management, grid optimisation, public safety) among government applications. **VERDICT: niche** — a replication/teaching artefact, not a framework; useful precisely because it documents the messy setup steps academia usually omits.

**Context (non-GitHub but relevant):** city 5G/6G testbeds referenced in research — DAI-Labor Future Communication Testbed (Berlin MEC along a 3.5 km road stretch), 6G-PATH Aveiro Tech City Living Lab (OpenAirInterface/srsRAN + O-RAN SC RIC/FlexRIC on USRPs, LoRaWAN, ITS-G5/C-V2X, edge UPF), 5G Berlin testbed — typically expose only fragments on GitHub; treat the O-RAN SC org plus srsRAN/OpenAirInterface projects as the buildable open pieces.

# CATEGORY 5 — BLOCKCHAIN CITY (identity, energy trading, certificates)

## 5.1 `energywebfoundation/origin` (+ the EW paper repo) — Energy Web Origin, renewable-certificate infrastructure

- **URL:** https://github.com/energywebfoundation/origin · **110 ★ / 60 forks** · **Language:** TypeScript/JavaScript (NestJS backend, React UI, Solidity contracts) + Python utilities · **Licence:** MIT for the meta-repo/many packages (components have had GPLv3 lineage — verify per npm package) · **Created:** August 2019 · **Recency:** org has 237 public repos and ongoing contributions (top contributors include renovate-bot with 1,749 contributions, indicating continuous dependency maintenance) · **Maintainer:** Energy Web Foundation (non-profit, Germany; co-founded by Rocky Mountain Institute + Grid Singularity).

**What it implements.** A system for **issuance and management of Energy Attribute Certificates (EACs)** — Guarantee of Origin (EU), Renewable Energy Certificate (North America), I-REC (international) — as an open, decentralised reference application: device registry APIs, smart-meter energy APIs, an **Issuer** module (NestJS), an order-book **Exchange** (ERC-1888 deposit/withdrawal processing), organisation registries for I-REC, and React UI packages (`origin-ui-*`). Sibling repos: **`energywebfoundation/paper`** (32 ★, GPL-3.0) — the **Energy Web Chain whitepaper, "The Energy Web Chain: Accelerating the Energy Transition with an Open-Source, Decentralized Blockchain Platform" (Version 1.0, October 2018)**, which also defines the EW frameworks **EW Origin** (certificates), **EW Link** (device-to-chain connectivity) and **EW D3A** (localised electricity market simulation) — a directly citable paper-linked repo; `ewc-system-contracts` (24 ★, GPLv3, genesis/chain-spec contracts); `ew-did-registry` (36 ★, decentralised identifiers); `authority-node` (15 ★).

**Best fit.** City **clean-energy programmes**: municipal renewable procurement, district-level certificate tracking, prosumer/P2P pilots needing auditable green-attribute accounting; DID research (ew-did-registry) for citizen/device identity.

**Limitations.** Individual repos have modest stars; some historical components are archived (**`ew-origin` 1★ — ARCHIVED/deprecated in favour of `origin`**; **`ew-link-origin` 13★, Python hardware link, last push Dec 2022**); the Energy Web Chain itself is now a Parity-derived PoA/EWA chain whose node software and tooling live elsewhere — check current node repos before building; heavy multi-package monorepo sprawl (many `@energyweb/*` npm packages).

**VERDICT: useful** — the most credible open energy-certificate stack; treat sibling repos as a minefield of archived predecessors.

## 5.2 Hyperledger city/energy examples

**`IBM/decentralized-energy-fabric-on-IBP20`** — 41 ★ / 34 forks, **Apache-2.0**, JS/TS, created Jan 2019, last push 17 Sep 2025 (dependabot-era maintenance). A Hyperledger Fabric code pattern for **neighbourhood energy trading**: residents with solar generation sell surplus energy to neighbours; pre-paid coin accounts; banks for fiat, utility company actors; Node.js server + Fabric SDK; chaincode packaged via the IBM Blockchain VS Code extension. Architecture flow fully documented. **Limitations:** built for **Fabric 1.4 and IBM Blockchain Platform SaaS (retired product)** — the pattern is now legacy; needs modernising to Fabric 2.5+/Hyperledger Fabric samples. **VERDICT: niche** — useful as a documented reference topology, dated as deployment instructions.

**`raphabenoi/thesis` (hypenergy)** — 16 ★ / 6 forks, **AGPL-3.0**, JS/Shell/TS, created April 2019. **Paper-linked:** the full implementation accompanying a **Master's thesis** — a decentralised **peer-to-peer marketplace for community-based local electricity markets on Hyperledger Fabric**: chaincode (`packages/energymarket-cc`), unit tests, three-layer local-electricity-market model, auction/gross-market logic (`createMarket`, grid buy/sell prices), Docker-compose dev network, ledger explorer on :5084. Requirements pinned to **Node 8.15 / Docker 18.09 / Fabric-era tooling**. **VERDICT: niche** — a reproducible thesis artefact; expect dependency rot (Node 8).

**`alexsicart/Energy-Trading`** — 13 ★ / 6 forks, MIT, 2017. Energy trading for neighbour communities on **Hyperledger Composer** (deprecated/archived platform) + React client. **VERDICT: avoid-stale** — Composer is dead; historical interest only.

**`zdpleon/energy_blockchain`** — 47 ★, multi-language (Go/Python/Vue), 2017. Chinese-language **Fabric 1.0** energy-trading platform: chaincode → CouchDB, Flask backend, Vue frontend, node 6.9.5/Fabric-from-source install instructions. **VERDICT: avoid-stale** — instructive as a full-stack layout, unusable without a rewrite.

*(Not found in a dedicated, well-maintained form: a "PowerLedger-like" fully open city P2P-trading product — the credible open options remain Energy Web Origin for certificates, Fabric-based thesis/reference apps for P2P trading, and newer EVM L2 experiments not covered here. IOTA covers the feeless-DLT angle below.)*

## 5.3 IOTA repositories — largely archived; track the successor

**`iotaledger/hornet`** — 303 ★ / 149 forks, Go, Apache-2.0, created Dec 2019, **Status: ARCHIVED**. The IOTA fullnode software (Stardust era, "INX" gRPC extension framework, Docker-compose with Traefik/Prometheus/Grafana/INX modules: Indexer, MQTT, Participation, Spammer, Dashboard). Last significant release **v2.0.2 (2023)**. Successor: the node implementation in the consolidated `iotaledger/iota` repository. **VERDICT: avoid-stale.**

**`iotaledger-archive/iota.rs`** — 221 ★, Rust, Apache-2.0, **ARCHIVED** — deprecated in favour of `iotaledger/iota-sdk`, which itself (60 ★, Rust 76.8% + TS/Python bindings, 80 contributors, 93 releases) was **archived after "IOTA Rebased" went live on mainnet (2025)**, with current SDK code living in `iotaledger/iota` (`crates/iota-sdk`). **VERDICT: avoid-stale** — both SDK entry points are tombstoned; cite history, build on `iotaledger/iota`.

**City relevance assessment.** IOTA's pitch (feeless DAG ledger, machine-to-machine micropayments, DID/identity) appears in smart-city literature for mobility micropayments (EV charging, parking) and device identity, but the GitHub surface a researcher can build on today is in **flux after the protocol rebased onto a MoveVM/Stardust successor architecture**; its identity work also spun out (`iota.rs`-era identity libs → IOTA Identity successors). Practical advice: for a 2026 paper, cite IOTA ecosystem work via the consolidated `iotaledger/iota` repo and official docs rather than hornet/iota.rs/iota-sdk, all of which are archived.

**Overall blockchain-city verdict:** the category is dominated by **archived or demo-grade artefacts**; the durable open pieces are **Energy Web Origin (certificates)** and the **Hyperledger Fabric reference patterns**, with licence/paper clarity strongest in `energywebfoundation/paper`.

---

# CATEGORY 6 — SENSOR / WEATHER / ENVIRONMENT CITY DATA PIPELINES

## 6.1 OpenAQ — global air-quality data platform (ingest → S3 → DB → API)

- **Organisation:** https://github.com/openaq (verified org, 53 repos, 258 followers)
- **Key repos:**
  - `openaq/openaq-api` — **68 ★ / 14 forks**, **MIT**, created Jan 2021, homepage api.openaq.org — the publicly accessible REST API source for real-time and historical measurements.
  - `openaq/openaq-fetch` — **93 ★ / 40 forks**, MIT (JS/TS/Shell), created Oct 2015, **maintenance-only status** (explicit warning: being migrated to a new fetching process, will be archived when complete; 121 open issues).
  - `openaq/openaq-python` — 22 ★, **Apache-2.0**, official Python SDK (`pip install openaq`), PyPI + docs + **DOI badge** (research-friendly), Codecov/Ruff CI.
  - `openaq/openaq.org` (35 ★), `awesome-air-quality` (70 ★ — curated air-quality resource list), `openaq-api-old` (152 ★, retired).
- **Language:** JavaScript/TypeScript (pipeline), Python (SDK) · **Recency:** platform actively re-architected (API v2 generation, SDK 2023+); fetch in migration.

**What it implements.** The architecture is a classic city-data pipeline: **`openaq-fetch` / `openaq-fetch-lcs` collect data from government/official sources every 10 minutes → S3 → `openaq-ingestor` Lambda functions → `openaq-db` → `openaq-api`**. Data criteria (citable methodology): PM10, PM2.5, SO2, CO, NO2, O3, black carbon; **official-level outdoor sources** (not low-cost/indoor); raw physical concentrations (not AQI indices); station-level with coordinates; averages 10 min–24 h; openly licensed origins. Data licence varies by source (CC/open-gov/custom) and the API exposes per-location licence metadata; terms of use require attribution and prohibit building a competing product on the **hosted** API (self-hosting the MIT code is fine).

**Best fit.** Ground-truth **air-quality data for city studies** (epidemiology, exposure equity, model validation), reference data to compare citizen-sensor networks against, and a template architecture (fetch→object-store→warehouse→API) for municipal data platforms.

**Limitations.** Government stations only (no citizen sensors — that is where SmartCitizen/AirCasting come in); `openaq-fetch` in maintenance-only mode; hosted-API rate limits and licence checks are real constraints; the org is lean (don't expect enterprise support).

**VERDICT: essential** — the standard open air-quality data source for smart-city/environment research.

## 6.2 `fablabbcn/smartcitizen-api` — Smart Citizen platform (citizen sensor network)

- **URL:** https://github.com/fablabbcn/smartcitizen-api · **12 ★ / 5 forks** · **Ruby on Rails** (Dockerfile/docker-compose, JS/SCSS front-end assets) · **Licence: AGPL-3.0** · **Created:** January 2015 · **Recency:** live development — issues opened as recently as **4 June 2026** (battery notifications, healthchecks, role reviews) · **Maintainer:** Fab Lab Barcelona / I2CAT-style citizen-science community (org also maintains `smartcitizen-web`, `smartcitizen-onboarding-app`, `smartcitizen-data` (Python), `smartcitizen-R-data`, `smartcitizen-connector`, `smartcitizen-flows`, `smartcitizen-docs` 29 ★ with pushes in March 2026).

**What it implements.** "The Smart Citizen Engine": a data platform for environmental sensor devices (Smart Citizen Kit/Stations) with **dual ingestion protocols — MQTT (devices, token-authenticated) and HTTP (apps, SD-card backfills, external platforms)**, both TLS-encrypted; **PostgreSQL** for user/device metadata and a **masterless-replicating time-series cluster** for readings; a documented **REST API** (devices, measurements, sensors, users, experiments) with OAuth2 and vocabularies linked to unit definitions; archiving/export for research (Python/R client libraries).

**Best fit.** **Citizen-science air-quality/noise/comfort datasets** for urban studies; interoperability experiments (MQTT→city broker bridges); papers on participatory sensing governance (roles, researcher access — an open issue theme in 2026).

**Limitations.** Very low star count (Rails+AGPL niche); API docs "hard for beginners" per their own forum; instance-centric (smartcitizen.me) rather than turnkey SaaS; AGPL obligations for derivatives.

**VERDICT: useful** — a long-running, genuinely operational citizen-sensor platform; star count understates its research value (many published datasets derive from it).

## 6.3 `HabitatMap/AirCasting` — AirCasting platform (AirBeam data)

- **URL:** https://github.com/HabitatMap/AirCasting · **64 ★ / 31 forks** · **Ruby** (Rails API + web app) · **Licence: AGPL-3.0** · **Created:** January 2012 · **Recency:** commits within days of this research (recent activity flagged by aggregators) · **Maintainer:** HabitatMap (NYC non-profit), homepage aircasting.org.

**What it implements.** Backend + web application for **gathering, visualising and sharing environmental/health data**: streams measurements from HabitatMap's **AirBeam** monitors (PM1/PM2.5/PM10, temperature, humidity; mobile personal-exposure mode and fixed outdoor mode) and other devices into a map-based platform described as "the world's largest open-source, open-access database of community-collected air-quality measurements" — billions of data points used by community organisations, educators, researchers, regulators and city managers. Data openly licensed (Creative Commons) with associated Android/iOS clients and AirBeam hardware designs living in sibling repos.

**Best fit.** **Hyperlocal/community air-quality datasets** (mobile monitoring routes, personal exposure), equity analyses of pollution hotspots, and a reference end-to-end open citizen-science pipeline (hardware → phone → API → map).

**Limitations.** AGPL server code; hardware (AirBeam) is a separate procurement/design chain; platform is Ruby/Rails-specific to extend; calibration is user-managed (community collocation studies exist but data quality varies).

**VERDICT: useful** — pair with OpenAQ (regulatory ground truth) for a complete urban air-quality research stack.

## 6.4 `teusH/MySense` — Dutch citizen-sensor framework (documentation-rich, partly stale)

- **URL:** https://github.com/teusH/MySense · **71 ★ / 18 forks** · **Python 3** (MicroPython for kits) · **Licence:** "Other" (custom open terms — read the LICENSE) · **Created:** February 2017 · **Recency: README last updated 2 February 2020** — effectively dormant, 0 open issues · **Maintainer:** individual/community ("Behoud de Parel" citizen initiative, Netherlands).

**What it implements.** A software infrastructure/framework for **managing environmental sensors and data acquisition**: input plugins for DHT11/22, BME280/680, GPS, Dylos/Nova SDS011/Plantower PMS/Sensirion SPS30 dust sensors, SPEC O3/NO2/CO, AlphaSense NH3; output channels to CSV, MySQL, **Mosquitto (MQTT)**, HTTP-Post, **InfluxDB**, email, OLED display, Google Sheets (deprecated); transport via LAN/WiFi/GPRS/**LoRaWAN (TTN MQTT)**; calibration workflows collocated with the Dutch RIVM monitoring station (Vredepeik, 2017 Fireworks Project), and forwarding to **Luftdaten.info/RIVM portals**. Extensive build/calibration/experience documentation; deployed in Dutch agricultural air-quality citizen initiatives (Horst aan de Maas, Land van Cuijk).

**Best fit.** **Calibration methodology and low-cost sensor plumbing patterns**; historical/case material on citizen-science governance in the Netherlands; a checklist of outputs a city sensor gateway should support.

**Limitations.** **README declares "WORK IN PROGRESS" but has not been updated since Feb 2020** — treat as documentation-first, code-second; custom licence; alpha-tested modules; no CI visible.

**VERDICT: niche (documentation-rich, avoid-stale code)** — mine it for method, not for dependencies.

*(Also relevant within this category: ThingsBoard's official **Air Quality Monitoring solution template** (see 2.1) for a simulated city AQ deployment; `openaq/awesome-air-quality` (70 ★) as the curated reading list; and the Luftdaten.info/open-sense-maps ecosystems whose codebases live across many small repos.)*

---

# PAPER- AND STANDARD-LINKED REPOSITORY INDEX

| Repository | Paper / standard it implements |
|---|---|
| `UDST/urbansim` | Waddell (2002) JAPA "UrbanSim: Modeling Urban Development…"; Waddell (2011) Transport Reviews; Noth/Borning/Waddell (2003) CEUS; Sevcikova/Raftery/Waddell (2007) Bayesian melding (full list on urbansim.com) |
| `energywebfoundation/paper` | The Energy Web Chain whitepaper v1.0 (Oct 2018), incl. EW Origin / EW Link / EW D3A frameworks |
| `UCY-LINC-LAB/fogify` + `5G-Slicer` | Fogify (IEEE/ACM SEC 2020 Best Demo); 5G-Slicer (IEEE/ACM IoTDi 2022 Best Paper); EC Innovation Radar entry |
| `mkturkcan/valdrada` | Boundless, arXiv:2409.03022 (synthetic urban data); congestion-pricing vision arXiv:2602.03015; edge urban video analytics (ACM/IEEE SEC 2025 Best Paper) |
| `raphabenoi/thesis` | Master's thesis "hypenergy": P2P local electricity market on Hyperledger Fabric (chaincode + tests in repo) |
| `edwardkeith-io/ORAN-Project` | Replication of arXiv:2205.13178 (open 5G small cell with SDR) |
| `3dcitydb/3dcitydb` | OGC CityGML 3.0/2.0/1.0 Conceptual Model; CityJSON specs; ADE mechanism |
| `citygml4j/*` | OGC CityGML + CityJSON 1.0/1.1/2.0; CityGML 3.0 upgrade path |
| `CesiumGS/3d-tiles` | 3D Tiles specification (OGC Community Standard) |
| `eclipse-ditto/ditto` | Digital-twin pattern; W3C Web of Things integration; ETSI/OMA-adjacent device management ecosystem |
| `Azure/opendigitaltwins-dtdl` | DTDL v1–v4 specification (JSON-LD/RDF) for Azure Digital Twins & IoT Plug and Play |
| `Urban-Model-Platform/urban-model-platform` | OGC API - Processes; Connected Urban Twins (HafenCity University Hamburg / LGV Hamburg) |
| `smart-data-models/*` | ETSI NGSI API (NGSIv2/NGSI-LD) data models; TM Forum Open APIs; GSMA IoT Big Data lineage (archived `FIWARE/data-models`) |
| `chirpstack/chirpstack` | LoRaWAN specification (regional params, MAC layer handling) |
| `contiki-ng/contiki-ng`, `RIOT-OS/RIOT` | IPv6/6LoWPAN, 6TiSCH, RPL, CoAP (IETF RFC series); Contiki-NG Cooja simulation line of WSN research |
| `eclipse-californium/californium` | RFC 7252 CoAP (+ DTLS, OMA LwM2M/oneM2M integration points) |
| `destination-earth/DestinE_ESA_CityNexus` | Destination Earth use-case; EU Mission 100 Climate-Neutral & Smart Cities KPI methodology |
| `IBM/decentralized-energy-fabric-on-IBP20` | Hyperledger Fabric 1.4 chaincode pattern (documented IBM Developer code pattern) |

---

# MASTER SUMMARY TABLE

| # | Repo | ★ (Nov 2026) | Language | Category | Verdict |
|---|---|---|---|---|---|
| 1 | 3dcitydb/3dcitydb | 469 | SQL/Java | Smart city (3D city DB) | essential |
| 2 | UDST/urbansim | 557 | Python | Urban platforms (simulation) | essential |
| 3 | ckan/ckan | ~5,150 | Python | City data portal | essential |
| 4 | GetDKAN/dkan | 387 | PHP | City data portal | useful |
| 5 | citygml4j/citygml-tools | 163 | Java | CityGML/CityJSON tools | useful |
| 6 | citygml4j/citygml4j | 138 | Java | CityGML/CityJSON tools | useful |
| 7 | smart-data-models/data-models | 143 | JSON/Python | Semantic city models | essential |
| 8 | smart-data-models/SmartCities | 115 | JSON | Semantic city models | essential |
| 9 | FIWARE/tutorials.Step-by-Step | 81 | Python/Shell | FIWARE city stack on-ramp | useful |
| 10 | lutece-platform/lutece-core | 80 | Java | Municipal services platform | niche |
| 11 | egovernments/egov-smartcity-suite | 76 | Java | India municipal (archived) | avoid-stale |
| 12 | enryteam/smart-city | 341 | Markdown | China standards library | niche |
| 13 | minhe51805/UrbanReflex | 133 | Python-stack | NGSI-LD city platform | useful |
| 14 | Haui-HIT-H2K/SmartCity-Platform | 83 | Python | Tiered-storage city IoT demo | niche |
| 15 | UIP-Urban-Intelligence-Platform | 25 | Python/TS | Vision→LOD traffic pipeline | niche |
| 16 | CTU-SematX/LegoCity | 19 | TS/Shell | FIWARE teaching template | niche |
| 17 | smartcitiescommunity/Civikmind | 42 | — | SDG civic platform | niche |
| 18 | meirim-org/meirim | 66 | JS | Planning transparency | niche |
| 19 | Prayag-X/Smart-City-Dashboard | 22 | Dart/Kotlin | City data app (GSoC) | avoid-stale |
| 20 | thingsboard/thingsboard | 22,644 | Java | IoT platform | essential |
| 21 | thingsboard/thingsboard-gateway | 2,150 | Python | Protocol gateway | useful |
| 22 | emqx/emqx | 16,856 | Erlang | MQTT/CoAP/LwM2M broker | essential (BSL) |
| 23 | node-red/node-red | 23,783 | JavaScript | Low-code IoT glue | essential |
| 24 | eclipse-mosquitto/mosquitto | ~11,300 | C | Lightweight MQTT broker | essential |
| 25 | chirpstack/chirpstack | 1,123 | Rust | LoRaWAN network server | essential |
| 26 | RIOT-OS/RIOT | 5,831 | C/C++ | Sensor-node OS | useful |
| 27 | contiki-ng/contiki-ng | 1,540 | C | Sensor-node OS (research) | useful |
| 28 | eclipse-hono/hono | 500 | Java | Device connectivity | niche (last release 2023) |
| 29 | eclipse-californium/californium | 779 | Java | CoAP/DTLS stack | useful |
| 30 | home-assistant/core | ~92,000 | Python | Building/campus automation | useful |
| 31 | openhab/openhab-core | 1,157 | Java | Building/campus automation | niche→useful |
| 32 | CesiumGS/cesium | 15,911 | TypeScript | 3D geospatial viewer | essential |
| 33 | CesiumGS/3d-tiles | 2,629 | Spec (JSON) | 3D streaming standard | essential |
| 34 | eclipse-ditto/ditto | 941 | Java | IoT digital-twin framework | essential |
| 35 | Azure/opendigitaltwins-dtdl | 578 | Spec (JSON-LD) | Twin modelling language | useful |
| 36 | Urban-Model-Platform/urban-model-platform | 28 | Python | Urban-twin model federation | useful |
| 37 | mkturkcan/valdrada | ~253 | Python/TS/UE5 | City-scale DT (NYC) | essential* |
| 38 | destination-earth/DestinE_ESA_CityNexus | 6 | — | Urban DT scenarios | niche |
| 39 | paramountric/digitaltwincityviewer | 17 | JS | DT city viewer (DTCC) | niche (paused) |
| 40 | phungdo/BoMoDT | 0 | Python | Mobility DT (FIWARE+SUMO) | niche |
| 41 | FARI-brussels/Fari-Brussels-Digital-Twin-Unity | 1 | C# (Unity) | City DT prototype | avoid-stale |
| 42 | kubeedge/kubeedge | 7,612 | Go | Edge orchestration (CNCF) | essential |
| 43 | openyurtio/openyurt | 1,968 | Go | Edge orchestration (CNCF) | useful |
| 44 | edgexfoundry/edgex-go | 1,548 | Go | Edge device framework | useful |
| 45 | UCY-LINC-LAB/fogify (+5G-Slicer) | 32 (16) | Python | Fog/5G emulation (paper-linked) | niche→useful |
| 46 | o-ran-sc (near-RT RIC mirrors) | 5–30/repo | C++/Go/Python | O-RAN/5G city networks | niche |
| 47 | energywebfoundation/origin | 110 | TypeScript | Energy certificates (blockchain) | useful |
| 48 | energywebfoundation/paper | 32 | LaTeX/MD | Energy Web Chain whitepaper | useful (citation) |
| 49 | IBM/decentralized-energy-fabric-on-IBP20 | 41 | JS/TS | P2P energy trading (Fabric) | niche |
| 50 | raphabenoi/thesis (hypenergy) | 16 | JS/TS | P2P market (Fabric, thesis) | niche |
| 51 | iotaledger/hornet | 303 | Go | IOTA fullnode (archived) | avoid-stale |
| 52 | iotaledger-archive/iota.rs (+iota-sdk) | 221 (60) | Rust | IOTA SDKs (archived) | avoid-stale |
| 53 | openaq/openaq-api | 68 | JS/TS | Air-quality data API | essential |
| 54 | openaq/openaq-fetch | 93 | JS/TS | Air-quality ingest (maintenance-only) | essential (data) / stale (code) |
| 55 | fablabbcn/smartcitizen-api | 12 | Ruby | Citizen sensor platform | useful |
| 56 | HabitatMap/AirCasting | 64 | Ruby | Community air-quality platform | useful |
| 57 | teusH/MySense | 71 | Python | Citizen sensor framework | niche (stale code) |

\* Valdrada: essential for urban-AI/perception researchers; treat as fast-moving (repo ~6 weeks old at snapshot).

---

# CROSS-CUTTING OBSERVATIONS

1. **Star count ≠ smart-city relevance.** The city-specific platforms (UrbanReflex 133★, urban-model-platform 28★, CityNexus 6★) are dwarfed by horizontal infrastructure (Home Assistant ~92k, Node-RED ~23.8k, ThingsBoard 22.6k, EMQX 16.9k, Cesium 15.9k). A defensible smart-city stack is **assembled from horizontal layers** — broker → ingestion/platform → semantic models/context broker → twin state → 3D rendering — rather than adopted as a single "smart city framework".
2. **The FIWARE/NGSI-LD orbit is the most distinctive open smart-city architecture.** Context broker (Orion-LD/Scorpio/Stellio) + Smart Data Models + IoT Agents + QuantumLeap time-series + tutorials appears in the majority of *recent* (2025–2026) city-platform repos (UrbanReflex, LegoCity, UIP, BoMoDT, Haui platform). It maps directly to ETSI NGSI standards and EU data-space policy, which is a strong citation/interoperability argument.
3. **Licensing shifted under our feet (2024–2026).** ThingsBoard moved CE+PE to **BUSL-1.1** (v4.4, Oct 2026); EMQX moved to **BSL-1.1** (v5.9.0, Apr 2025, cluster licensing); both promise Apache-2.0 after four years. For grant-funded reproducibility, prefer **Apache-2.0/EPL/MIT/BSD** pillars (Mosquitto, Node-RED, ChirpStack, Cesium, KubeEdge, EdgeX, OpenYurt, Ditto, CKAN-AGPL) and document BUSL exposure explicitly.
4. **Archived traps are concentrated in IOTA and old blockchain demos** (hornet, iota.rs, iota-sdk, Hyperledger Composer apps, Fabric 1.0 demos) plus India's archived eGov suite and the paused DTCC viewer. Always check the GitHub "ARCHIVED" banner and the last-release date (not just last commit — Eclipse projects like Hono sit in "Mature" limbo).
5. **Digital twins are splitting into three open layers:** (a) *semantic/state* — Ditto, DTDL, NGSI-LD context brokers; (b) *geometric/visual* — CityGML/3DCityDB + Cesium/3D Tiles; (c) *simulation/what-if* — SUMO/UrbanSim + OGC API-Processes model federation (urban-model-platform, CityNexus). Papers increasingly cite all three; repos rarely implement all three (Valdrada and BoMoDT come closest).
6. **Edge/6G openness is real but star-poor.** KubeEdge/OpenYurt/EdgeX are healthy CNCF/Linux-Foundation projects; O-RAN SC GitHub repos are mirrors of Gerrit (stars meaningless); reproducible 5G city experiments live in small paper-linked repos (Fogify/5G-Slicer, the ORAN-Project capstone) rather than in big platforms.

# RECOMMENDATION MATRIX (by researcher profile)

- **City data platform / open-data researcher:** CKAN (essential) + DKAN (compare) + Smart Data Models + OpenAQ API.
- **IoT/communications researcher:** Mosquitto or EMQX (broker) + ChirpStack (LoRaWAN) + Node-RED (glue) + ThingsBoard (platform baseline) + RIOT/Contiki-NG (firmware) + Californium (CoAP).
- **Digital-twin researcher:** 3DCityDB + citygml-tools (geometry/semantics) + Eclipse Ditto (live twin state) + Cesium/3D Tiles (visual) + urban-model-platform or SUMO/UrbanSim (simulation) + DTDL (modelling comparison); Valdrada for perception/sim-to-real.
- **Edge/5G researcher:** KubeEdge or OpenYurt + EdgeX Foundry + Fogify/5G-Slicer for emulation + O-RAN SC (with Gerrit awareness).
- **Urban energy/blockchain researcher:** Energy Web Origin + EW paper (certificates) + Fabric P2P patterns (trading) — and cite, don't build, on IOTA's archived repos.
- **Environmental-justice / citizen-science researcher:** OpenAQ (regulatory) + AirCasting + SmartCitizen + MySense (calibration methods) + ThingsBoard AQ template for dashboards.

*End of dossier. All figures are snapshots as of 6 November 2026; re-verify stars, licences and archive status before citing in a publication.*


