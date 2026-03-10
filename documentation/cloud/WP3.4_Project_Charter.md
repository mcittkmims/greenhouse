# 04 - GMS -WP3.4 Project Charter

> Source: http://confluence.microlab.club/rest/api/content/42634074 | Version: 5

| **Field** | **Detail** |
| --- | --- |
| **Project Name** | Greenhouse Management System (GMS) |
| **Document Version** | 1.0 |
| **Course / Institution** | PBL IoT - Technical University of Moldova (UTM) |
| **Supervisor** | Andrei Bragarenco |
| **Team** | Team 04-GMS (5 members) |
| **Date** | February 26, 2026 |
| **Target Completion** | June 2026 |
| **Status** | Initiation - Awaiting Authorization |
****

### Executive Summary

The Greenhouse Management System (GMS) is an IoT-based automation and monitoring platform for greenhouse operators and farmers in the Republic of Moldova, integrating industrial-grade sensors, a PLC-driven edge controller (Arduino Portenta Machine Control), and a cloud-connected mobile dashboard to regulate soil moisture, air temperature, humidity, CO₂, and light intensity.
Driven by the critical gap between Moldova’s manual greenhouse practices - responsible for excessive resource use, reactive crop management, and an unsustainable 24/7 monitoring burden - and validated by an 18-respondent stakeholder survey (February 2026) confirming 94.4% demand for automated irrigation, the GMS positions itself as a data platform delivering traceability, remote management, and measurable resource efficiency for Moldovan agricultural operators.****

### Problem Statement

Farmers and greenhouse operators often face difficulties in maintaining stable environmental conditions for plant growth. Monitoring and adjusting factors such as temperature and humidity usually requires constant attention and manual effort. Delayed or incorrect adjustments can cause plant stress and reduce crop quality and yield. As a result, resources such as time, water, and energy are often used inefficiently. ****

### Business Justification

- *Improving resource efficiency* through smart management, driving up to 40% reductions in water use  and 25% in energy consumption .
- *Addressing high market demand* validated by 94% of surveyed operators confirming automated irrigation as a top economic priority.
- *Supporting Moldova’s transition* to Agriculture 4.0 and advancing national food sovereignty initiatives.
- *Ensuring scalable deployment* from smallholder operations (12-300 m²) up to industrial farm-level management (1-5+ ha).
- *Reducing import dependency* by automating local greenhouse production to offset the 60%+ reliance on Ukrainian tomato imports .
****

### Project Objectives

| **#** | **Objective** | **Metric** | **Target** | **Date** |
| --- | --- | --- | --- | --- |
| O1 | Deploy real-time sensor network (soil moisture, temp, humidity, CO₂, light) | All 5 parameters at ≤ 60 s intervals | ≥ 60s | Apr 2026 |
| O2 | Automate irrigation via soil moisture thresholds | ≥ 30% water reduction vs. manual baseline | ≥30% | Apr 2026 |
| O3 | Automate climate regulation (ventilation, heating) | Temperature within ±0.5°C of setpoint | ±0.5°C | Apr 2026 |
| O4 | Deploy cloud dashboard with live data, 90-day history, push/SMS alerts | Accessible on mobile over 4G/5G | Mobile | May 2026 |
| O5 | Guarantee edge-cloud hybrid with offline fallback | ≥ 72 h autonomous control; zero data loss on reconnect | 72h | May 2026 |
| O6 | Validate via pilot in ≥ 1 operational greenhouse | ≥ 30% water, ≥ 20% energy savings confirmed | Pilot | Jun 2026 |
****

### Project Scope

****

#### In-Scope:

- *System Development:* Design, develop, and deploy the IoT-enabled Greenhouse Management System for automated climate and irrigation control.
- *Sensor & Actuator Integration:* Install environmental sensors, like temperature, humidity, soil moisture, light, CO₂, and integrate them with greenhouse climate control equipment, like heaters, fans, valves.
- *Edge Computing Logic:* Implement local control algorithms to ensure uninterrupted greenhouse management even during periods of network disconnection.
- *Cloud & Telemetry Dashboard:* Develop a mobile-friendly dashboard for real-time monitoring, historical data analysis, and remote setpoint configuration.
- *Alerts & Notifications:* Create a reliable communication system to alert operators of critical environmental changes via push notifications or SMS.
- *Cybersecurity Measures:* Ensure secure data transmission and role-based access to protect greenhouse operations from unauthorized access.
- *Pilot Testing:* Deploy the fully integrated system in an active tomato greenhouse in Moldova to validate resource savings and operational improvements.
****

#### Out-of-Scope:

- *Advanced AI Forecasting:* Implementation of complex machine learning models or computer vision for plant disease detection, planned for future phases.
- *Multi-Site Rollout:* Deployment to multiple distinct greenhouse locations during this initial pilot phase.
- *Third-Party Farm Integration:* Connecting the system to external ERP or enterprise farm management software.
- *Hardware Manufacturing:* Designing custom electronic boards or mass-producing hardware components.
****

### Deliverables, Milestones & Timeline

| **Work Package** | **Deliverable** | **Status** | **Target** |
| --- | --- | --- | --- |
| **Problem Definition** | Problem Definition Report | 10 complete Complete | Feb 2026 |
| **Technology Research** | Technology Research Report | 11 complete Complete | Feb 2026 |
| **Business Research** | Business Case, Stakeholder Analysis, Survey Report, Project Charter | 12 complete Complete | Feb 2026 |
| **Stakeholder Req.** | Stakeholder Requirements Document | 13 incomplete Complete | Mar 2026 |
| **System Requirements** | SRS, use cases, acceptance criteria | 14 incomplete Complete | Mar 2026 |
| **System Architecture** | Architecture document, data flows, I/O mapping, API & DB design | 15 incomplete Complete | Mar-Apr 2026 |
| **Implementation** | Integrated system prototype (edge + cloud + dashboard MVP) | 16 incomplete Complete | Apr-May 2026 |
| **Edge Computing** | PLC firmware: PID loops, alarm logic, sensor integration, offline autonomy | 17 incomplete Complete | May 2026 |
| **Cloud Computing** | Time-series DB, MQTT broker, analytics pipeline, remote dashboard | 18 incomplete Complete | May 2026 |
****

### Stakeholders

| **Engagement Level** | **Stakeholders & Rationale** |
| --- | --- |
| **Manage Closely** | Farmers, Greenhouse Operators, Dev Team (Embedded + IoT + Frontend), Investors - direct operational/financial dependence; active sprint collaboration and pilot participation. |
| **Keep Satisfied** | Ministry of Agriculture, Agricultural Agencies, HW Suppliers, Cloud Providers - regulatory authority and infrastructure influence; periodic updates and compliance alignment. |
| **Keep Informed** | Technical University of Moldova (TUM) - research validation, no executive authority; academic reporting. |
| **Monitor** | Consumers - indirect beneficiaries; general awareness only. |
****

### Budget Estimate

| **Category** | **Range** |
| --- | --- |
| Hardware (PLC, sensors, actuators, UPS, enclosures) | ~800-2,000 EUR |
| Cloud infrastructure (DB, Server) | ~100-400 EUR |
| Connectivity (4G modem + SIM) | ~50-150 EUR |
| Miscellaneous (installation, tools, contingency) | ~100-500 EUR |
| **TOTAL** | ~1,050-3,050 EUR |
****

### Key Risks & Mitigation Strategies

| **Risk** | **Mitigation** |
| --- | --- |
| Hardware procurement delays | Obtain critical components early and qualify backup suppliers to prevent pipeline blocks. |
| Connectivity instability at pilot site | Implement edge computing solutions for local data buffering and autonomous control during network loss. |
| Pilot site access withdrawn | Establish a clear written agreement with the pilot participant and identify a secondary backup site. |
| Sensor drift / inaccurate data | Integrate redundant sensors for critical measurements and perform strict calibration during deployment. |
| Scope creep from feature requests | Enforce project charter boundaries and log any out-of-scope requests for future development phases. |
| Cybersecurity vulnerability | Implement robust data encryption, secure authenticated access, and conduct regular security reviews. |
| Timeline pressure | Prioritize core system features first and maintain parallel development of hardware and cloud components. |
****

### Assumptions & Constraints

**Assumptions:**
- 4G coverage at pilot site
- Arduino Portenta Machine Control available
- Pilot farmer willing to participate
- TUM advisory role maintained
- Tomato crop present during pilot

**Constraints:**
- Mobile-first UI (4G/5G mandatory)
- Romanian + Russian language support
- GDPR compliant
- Cost-viable for SME farmers
- Single-zone prototype only
- Completed within one growing season
****

### Authorization

By signing, the undersigned formally authorize the GMS project to proceed as defined in this charter.
| **Role** | **Name** | **Signature** | **Date** |
| --- | --- | --- | --- |
| Academic Supervisor | Andrei Bragarenco |  |  |
| Team Lead | Victoria Mutruc |  |  |

*This is a living document - all revisions require Academic Supervisor re-authorization.*****

### References

ref1[1] “How to Reduce Water Consumption in Your Greenhouse - Hydroponic Systems.”* Hydroponic Systems*, 9 Sept. 2024, hydroponicsystems.eu/how-to-reduce-water-consumption-in-your-greenhouse/. Accessed 21 Feb. 2026.
ref2[2] “An Agricultural Country without Its Tomatoes: Moldova Remains Dependent on Imports.” *News-Pravda.com*, 2026, md.news-pravda.com/en/world/2026/02/10/88535.html. Accessed 22 Feb. 2026.
ref3[3] Li, Haixia, et al. “Towards Automated Greenhouse: A State of the Art Review on Greenhouse Monitoring Methods and Technologies Based on Internet of Things.” *Computers and Electronics in Agriculture*, vol. 191, Dec. 2021, p. 106558, https://doi.org/10.1016/j.compag.2021.106558.  Accessed 22 Feb. 2026.
