# 04 - GMS -WP4.3 Import Stakeholder requirements in Jira

> Source: http://confluence.microlab.club/rest/api/content/42634112 | Version: 60

| Category | Stakeholder Requirements | Type | Classification | Rationale | Jira Link |
| --- | --- | --- | --- | --- | --- |
| Environmental Monitoring and Control | As a farmer, I want the system to monitor soil moisture continuously so that my crops receive water only when needed. | US | Must Have | Highest survey score (4.83/5) and cited by 39% of respondents as their most frequent production-impacting incident; soil moisture is the foundational trigger for all irrigation automation. |  |
| Environmental Monitoring and Control | When soil moisture drops below a set threshold, I want the system to automatically activate irrigation so I can avoid crop stress without being on-site. | JS | Must Have | Highest survey score (4.83/5) and cited by 39% of respondents as their most frequent production-impacting incident; soil moisture is the foundational trigger for all irrigation automation. |  |
| Environmental Monitoring and Control | As a greenhouse operator, I want real-time temperature monitoring so that I can prevent crop damage from overheating or frost. | US | Must Have | Second highest survey score (4.61/5) with 22% citing temperature extremes as a recurring incident; Moldova's −15°C to +35°C climate range makes automated thermal regulation non-negotiable. |  |
| Environmental Monitoring and Control | When temperature falls below 10°C or exceeds 35°C, I want the system to activate heating or ventilation automatically so I can protect my crops without manual intervention. | JS | Must Have | Second highest survey score (4.61/5) with 22% citing temperature extremes as a recurring incident; Moldova's −15°C to +35°C climate range makes automated thermal regulation non-negotiable. |  |
| Environmental Monitoring and Control | As an operator, I want humidity levels tracked automatically so that I can prevent fungal diseases caused by excessive moisture. | US | Must Have | Third highest survey score (4.72/5); excess humidity directly triggers fungal pathogen growth and is tightly coupled with temperature and ventilation control. |  |
| Environmental Monitoring and Control | When humidity exceeds safe levels, I want the system to trigger ventilation so I can reduce disease risk without constant manual checks. | JS | Must Have | Third highest survey score (4.72/5); excess humidity directly triggers fungal pathogen growth and is tightly coupled with temperature and ventilation control. |  |
| Environmental Monitoring and Control | As a greenhouse operator, I want CO₂ levels tracked so that I can optimise growing conditions and increase yield. | US | Should Have | Lowest environmental rating (4.22/5) with no respondents citing CO₂ as a production incident, yet controlled enrichment (800–1200 ppm) is documented to increase crop yield by 20–30%. |  |
| Environmental Monitoring and Control | When CO₂ drops below optimal levels, I want the system to alert me so I can adjust enrichment and improve crop productivity. | JS | Should Have | Lowest environmental rating (4.22/5) with no respondents citing CO₂ as a production incident, yet controlled enrichment (800–1200 ppm) is documented to increase crop yield by 20–30%. |  |
| Environmental Monitoring and Control | As a greenhouse operator, I want up-to-date readings on my screen so that I can catch problems as soon as they happen. | US | Must Have | 66.7% of respondents selected the dashboard as their primary monitoring channel; automatic refresh is essential for detecting fast-changing conditions without manual page reloads. |  |
| Environmental Monitoring and Control | When conditions change rapidly, I want the dashboard to refresh automatically so I can respond before crop damage occurs. | JS | Must Have | 66.7% of respondents selected the dashboard as their primary monitoring channel; automatic refresh is essential for detecting fast-changing conditions without manual page reloads. |  |
| Environmental Monitoring and Control | As a farmer, I want to receive a warning when conditions become dangerous so that I can act before my crops are damaged. | US | Must Have | Survey respondents explicitly requested threshold-based alerts across all monitored parameters; without in-system alerting, real-time monitoring cannot prevent crop loss during unattended periods. |  |
| Environmental Monitoring and Control | When a parameter exceeds a safe range, I want an immediate alert so I can intervene before plants are stressed. | JS | Must Have | Survey respondents explicitly requested threshold-based alerts across all monitored parameters; without in-system alerting, real-time monitoring cannot prevent crop loss during unattended periods. |  |
| Automated Irrigation | As a farmer, I want irrigation to follow a timed schedule so that my greenhouse can run for months without anyone on-site. | US | Must Have | One survey respondent required fully autonomous operation for up to 3 months while abroad; schedule-based irrigation ensures continuity when connectivity or sensor feedback is unavailable. |  |
| Automated Irrigation | When I am abroad for extended periods, I want a timed irrigation schedule to run autonomously so I can keep the greenhouse operational without being on-site. | JS | Must Have | One survey respondent required fully autonomous operation for up to 3 months while abroad; schedule-based irrigation ensures continuity when connectivity or sensor feedback is unavailable. |  |
| Climate Control | As a farmer, I want to define my own comfort zones for the greenhouse so that the system reacts according to my specific crop needs. | US | Must Have | Stakeholders growing different crop types noted the need to adjust setpoints per species; fixed thresholds would make automation inapplicable across varied growing scenarios. |  |
| Climate Control | When I switch to a different crop, I want to reconfigure temperature and humidity ranges so I can adapt the system to new plant requirements. | JS | Must Have | Stakeholders growing different crop types noted the need to adjust setpoints per species; fixed thresholds would make automation inapplicable across varied growing scenarios. |  |
| Web Dashboard | As a greenhouse owner, I want to check my greenhouse from a browser on any device so that I am not tied to a specific phone or application. | US | Must Have | 66.7% of respondents selected a browser dashboard as their preferred monitoring channel; zero-install browser access eliminates device lock-in and lowers adoption barriers. |  |
| Web Dashboard | When I am travelling, I want to access the dashboard from any browser so I can monitor my greenhouse without carrying specific hardware. | JS | Must Have | 66.7% of respondents selected a browser dashboard as their preferred monitoring channel; zero-install browser access eliminates device lock-in and lowers adoption barriers. |  |
| Web Dashboard | As an operator, I want a simple overview page so that I can understand the state of my greenhouse at a glance. | US | Must Have | Stakeholders described needing to assess all parameters in one view; a consolidated, simple layout is critical for non-technical users to make timely operational decisions. |  |
| Web Dashboard | When checking greenhouse status quickly, I want a clear single-page overview so I can assess all critical conditions at a glance. | JS | Must Have | Stakeholders described needing to assess all parameters in one view; a consolidated, simple layout is critical for non-technical users to make timely operational decisions. |  |
| Alerts and Notifications | As a farmer, I want to be notified on my phone when something goes wrong so that I can react even when I am away from the computer. | US | Should Have | 27.8% of respondents preferred SMS/push as their primary alert channel; off-screen notifications extend responsiveness beyond the dashboard but in-dashboard alerts cover the baseline need. |  |
| Alerts and Notifications | When a critical threshold is exceeded, I want a push notification on my phone so I can react immediately even when away from the site. | JS | Should Have | 27.8% of respondents preferred SMS/push as their primary alert channel; off-screen notifications extend responsiveness beyond the dashboard but in-dashboard alerts cover the baseline need. |  |
| Historical Data and Reports | As a greenhouse operator, I want to see how conditions have changed over the past weeks and months so that I can make better planting and management decisions. | US | Should Have | Multiple respondents and technical experts requested historical trends; real-time control and alerting address immediate crop safety while trend visualisation improves longer-term decisions. |  |
| Historical Data and Reports | When planning the next growing season, I want to review environmental trends from previous months so I can optimize conditions for better yield. | JS | Should Have | Multiple respondents and technical experts requested historical trends; real-time control and alerting address immediate crop safety while trend visualisation improves longer-term decisions. |  |
| Historical Data and Reports | As a business owner, I want to download reports from the system so that I can share them with investors or agronomists. | US | Should Have | Technical experts flagged audit-trail needs and survey respondents requested shareable reports; export capability positions the system beyond real-time control but is not critical for pilot operation. |  |
| Historical Data and Reports | When meeting with investors or agronomists, I want to export a formatted data report so I can present evidence of system performance. | JS | Should Have | Technical experts flagged audit-trail needs and survey respondents requested shareable reports; export capability positions the system beyond real-time control but is not critical for pilot operation. |  |
| Affordability | As a small farmer, I want a solution I can actually afford so that I do not need to take on significant financial risk to automate my greenhouse. | US | Must Have | 50% of survey respondents are small-scale farmers; affordability is a prerequisite for adoption among the primary user segment and a core project objective. |  |
| Affordability | When deciding to invest in automation, I want transparent pricing and a cost estimate so I can assess whether the system fits my budget. | JS | Must Have | 50% of survey respondents are small-scale farmers; affordability is a prerequisite for adoption among the primary user segment and a core project objective. |  |
| Affordability | As an investor, I want to see proven reductions in operational costs so that I can evaluate the return on investment before committing funds. | US | Should Have | Research shows smart greenhouse systems achieve up to 40% water and 25% energy savings; demonstrating this validates ROI for investors but requires pilot operational data to measure. |  |
| Affordability | When reviewing operational results, I want measurable data on water and energy savings so I can calculate the return on investment. | JS | Should Have | Research shows smart greenhouse systems achieve up to 40% water and 25% energy savings; demonstrating this validates ROI for investors but requires pilot operational data to measure. |  |
| Multi-Site / Multi-Zone Management | As a large agricultural enterprise manager, I want a unified dashboard for all my greenhouse sites so that I can manage operations without visiting each location. | US | Won't Have | Majority of surveyed operators manage a single greenhouse; multi-site architecture would add significant complexity and is not required for the initial pilot deployment. |  |
| Multi-Site / Multi-Zone Management | When managing multiple zones, I want to compare environmental data across sites so I can identify underperformance and allocate resources efficiently. | JS | Won't Have | Majority of surveyed operators manage a single greenhouse; multi-site architecture would add significant complexity and is not required for the initial pilot deployment. |  |
| Cybersecurity | As a system administrator, I want all data transmissions encrypted so that unauthorised parties cannot access or manipulate greenhouse controls. | US | Should Have | Remote control of physical actuators over public networks is an identified risk; TLS and authenticated MQTT are standard IoT security provisions and must be addressed before production rollout. |  |
| Cybersecurity | When connecting the greenhouse controller to the cloud, I want secure authentication so I can prevent unauthorised access to critical actuator controls. | JS | Should Have | Remote control of physical actuators over public networks is an identified risk; TLS and authenticated MQTT are standard IoT security provisions and must be addressed before production rollout. |  |
| Survey Extracted Stakeholder Requirements: |  |  |  |  |  |
| Soil and Water Management | As a farmer, I want soil moisture to be the first thing shown on my dashboard so that I always know if my crops need water. | US | Must Have | Highest survey score (4.83/5) and most frequently cited production incident (39%); soil moisture must be the primary indicator on the dashboard interface. |  |
| Soil and Water Management | When opening the dashboard, I want soil moisture to appear prominently so I can immediately see if irrigation is needed. | JS | Must Have | Highest survey score (4.83/5) and most frequently cited production incident (39%); soil moisture must be the primary indicator on the dashboard interface. |  |
| Soil and Water Management | As a greenhouse owner abroad, I want to start watering from my browser so that I can react to unexpected dry spells even when I am not in the country. | US | Must Have | Survey respondents explicitly requested remote irrigation control; one respondent described needing to trigger watering while abroad for extended periods. |  |
| Soil and Water Management | When I am outside the country for weeks, I want to remotely activate irrigation from my browser so I can respond to unexpected dry spells. | JS | Must Have | Survey respondents explicitly requested remote irrigation control; one respondent described needing to trigger watering while abroad for extended periods. |  |
| Soil and Water Management | As a farmer, I want irrigation to stop automatically when the soil is wet enough so that I do not waste water or damage the roots. | US | Must Have | 17% of respondents cited irrigation failures as a production problem; automatic cutoff prevents sensor-triggered over-activation and the resulting root damage. |  |
| Soil and Water Management | When soil reaches the target moisture level, I want irrigation to stop automatically so I can prevent overwatering and root damage. | JS | Must Have | 17% of respondents cited irrigation failures as a production problem; automatic cutoff prevents sensor-triggered over-activation and the resulting root damage. |  |
| Temperature and Humidity | As a farmer, I want different alerts for heat and cold so that I know exactly what kind of problem I am dealing with. | US | Could Have | Survey respondents described needing to distinguish heat and cold events; the distinction improves response accuracy but a single threshold alert already covers both scenarios at the baseline. |  |
| Temperature and Humidity | When nighttime temperatures drop unexpectedly, I want a frost-specific alert separate from heat warnings so I can take the right corrective action. | JS | Could Have | Survey respondents described needing to distinguish heat and cold events; the distinction improves response accuracy but a single threshold alert already covers both scenarios at the baseline. |  |
| Connectivity | As a rural farmer, I want the system to work well over mobile internet so that I can use it without needing to install a wired connection at my greenhouse. | US | Must Have | 55.6% of respondents rely on mobile data as their primary connection and only 33.3% have fixed broadband; without 4G/5G support the majority of target users cannot access cloud features. |  |
| Connectivity | When located in a rural area with only mobile internet, I want the system to connect reliably over 4G/5G so I can use all features without a fixed broadband line. | JS | Must Have | 55.6% of respondents rely on mobile data as their primary connection and only 33.3% have fixed broadband; without 4G/5G support the majority of target users cannot access cloud features. |  |
| Connectivity | As a small-scale farmer using a mobile data plan, I want the website to be lightweight so that it does not consume too much data or load too slowly. | US | Should Have | Respondents on mobile data plans expressed concern over data consumption; a lightweight interface is important for usability on limited plans but does not block core functionality. |  |
| Connectivity | When accessing the dashboard on a limited mobile data plan, I want pages to load quickly and consume minimal bandwidth so I can use the system cost-effectively. | JS | Should Have | Respondents on mobile data plans expressed concern over data consumption; a lightweight interface is important for usability on limited plans but does not block core functionality. |  |
| Web Dashboard | As a small-scale farmer, I want the website to look and work well on my phone so that I do not need a computer to use the system. | US | Must Have | 55.6% of sites rely exclusively on mobile data and smartphones are the primary device among surveyed operators; mobile-responsive design is essential for field usability. |  |
| Web Dashboard | When checking the greenhouse on-the-go, I want the interface to be fully functional on my smartphone so I can manage everything without needing a computer. | JS | Must Have | 55.6% of sites rely exclusively on mobile data and smartphones are the primary device among surveyed operators; mobile-responsive design is essential for field usability. |  |
| Historical Data and Reports | As a business owner, I want to export sensor data to a spreadsheet so that I can share it with my agronomist or include it in business reports. | US | Should Have | Multiple survey respondents and technical experts explicitly requested Excel/CSV export for sharing with agronomists, investors, and regulatory authorities. |  |
| Historical Data and Reports | When preparing records for compliance or advisory meetings, I want to export sensor data to Excel or CSV so I can share it with agronomists or authorities. | JS | Should Have | Multiple survey respondents and technical experts explicitly requested Excel/CSV export for sharing with agronomists, investors, and regulatory authorities. |  |
****

## Classes

****

### Environmental Monitoring and Control false Microlab Jira 5b8ef41d-7a73-399f-9666-c949acb53653 GMS-1

Stakeholder Requirement: The system should continuously monitor, control and display all key greenhouse parameters in real time.

#### User Stories:

- As a farmer, I want the system to monitor soil moisture continuously so that my crops receive water only when needed.falseMicrolab Jira5b8ef41d-7a73-399f-9666-c949acb53653GMS-10
- As a greenhouse operator, I want real-time temperature monitoring so that I can prevent crop damage from overheating or frost.falseMicrolab Jira5b8ef41d-7a73-399f-9666-c949acb53653GMS-11
- As an operator, I want humidity levels tracked automatically so that I can prevent fungal diseases caused by excessive moisture.falseMicrolab Jira5b8ef41d-7a73-399f-9666-c949acb53653GMS-12
- As a greenhouse operator, I want CO₂ levels tracked so that I can optimize growing conditions and increase yield.falseMicrolab Jira5b8ef41d-7a73-399f-9666-c949acb53653GMS-13
- As a greenhouse operator, I want up-to-date readings on my screen so that I can catch problems as soon as they happen.falseMicrolab Jira5b8ef41d-7a73-399f-9666-c949acb53653GMS-14
- As a farmer, I want to receive a warning when conditions become dangerous so that I can act before my crops are damaged.falseMicrolab Jira5b8ef41d-7a73-399f-9666-c949acb53653GMS-15

#### Job Stories:

- When soil moisture drops below a set threshold, I want the system to automatically activate irrigation so I can avoid crop stress without being on-site.falseMicrolab Jira5b8ef41d-7a73-399f-9666-c949acb53653GMS-16
- When temperature falls below 10°C or exceeds 35°C, I want the system to activate heating or ventilation automatically so I can protect my crops without manual intervention.falseMicrolab Jira5b8ef41d-7a73-399f-9666-c949acb53653GMS-17
- When humidity exceeds safe levels, I want the system to trigger ventilation so I can reduce disease risk without constant manual checks.falseMicrolab Jira5b8ef41d-7a73-399f-9666-c949acb53653GMS-18
- When CO₂ drops below optimal levels, I want the system to alert me so I can adjust enrichment and improve crop productivity.falseMicrolab Jira5b8ef41d-7a73-399f-9666-c949acb53653GMS-19
- When conditions change rapidly, I want the dashboard to refresh automatically so I can respond before crop damage occurs.falseMicrolab Jira5b8ef41d-7a73-399f-9666-c949acb53653GMS-20
- When a parameter exceeds a safe range, I want an immediate alert so I can intervene before plants are stressed.falseMicrolab Jira5b8ef41d-7a73-399f-9666-c949acb53653GMS-21
****

### Automated Irrigation and Climate Control false Microlab Jira 5b8ef41d-7a73-399f-9666-c949acb53653 GMS-2

Stakeholder Requirement: The system should allow users to configure and schedule irrigation and climate parameters remotely, enabling fully autonomous greenhouse operation without requiring on-site presence.

#### User Stories:

- As a farmer, I want irrigation to follow a timed schedule so that my greenhouse can run for months without anyone on-site.falseMicrolab Jira5b8ef41d-7a73-399f-9666-c949acb53653GMS-22
- As a farmer, I want to define my own comfort zones for the greenhouse so that the system reacts according to my specific crop needs.falseMicrolab Jira5b8ef41d-7a73-399f-9666-c949acb53653GMS-23
- As a farmer, I want soil moisture to be the first thing shown on my dashboard so that I always know if my crops need water.falseMicrolab Jira5b8ef41d-7a73-399f-9666-c949acb53653GMS-24
- As a greenhouse owner abroad, I want to start watering from my browser so that I can react to unexpected dry spells even when I am not in the country.falseMicrolab Jira5b8ef41d-7a73-399f-9666-c949acb53653GMS-25
- As a farmer, I want irrigation to stop automatically when the soil is wet enough so that I do not waste water or damage the roots.falseMicrolab Jira5b8ef41d-7a73-399f-9666-c949acb53653GMS-26
- As a farmer, I want different alerts for heat and cold so that I know exactly what kind of problem I am dealing with.falseMicrolab Jira5b8ef41d-7a73-399f-9666-c949acb53653GMS-27 

#### Job Stories:

- When I am abroad for extended periods, I want a timed irrigation schedule to run autonomously so I can keep the greenhouse operational without being on-site.falseMicrolab Jira5b8ef41d-7a73-399f-9666-c949acb53653GMS-28
- When I switch to a different crop, I want to reconfigure temperature and humidity ranges so I can adapt the system to new plant requirements.falseMicrolab Jira5b8ef41d-7a73-399f-9666-c949acb53653GMS-29
- When opening the dashboard, I want soil moisture to appear prominently so I can immediately see if irrigation is needed.falseMicrolab Jira5b8ef41d-7a73-399f-9666-c949acb53653GMS-30
- When I am outside the country for weeks, I want to remotely activate irrigation from my browser so I can respond to unexpected dry spells.falseMicrolab Jira5b8ef41d-7a73-399f-9666-c949acb53653GMS-31
- When soil reaches the target moisture level, I want irrigation to stop automatically so I can prevent over-watering and root damage.falseMicrolab Jira5b8ef41d-7a73-399f-9666-c949acb53653GMS-32
- When nighttime temperatures drop unexpectedly, I want a frost-specific alert separate from heat warnings so I can take the right corrective action.falseMicrolab Jira5b8ef41d-7a73-399f-9666-c949acb53653GMS-33
****

### Web Dashboard & Mobile Accessibility false Microlab Jira 5b8ef41d-7a73-399f-9666-c949acb53653 GMS-3

Stakeholder Requirement: The system should provide a browser-accessible, mobile-friendly dashboard with a clear and lightweight interface.

#### User Stories:

- As a greenhouse owner, I want to check my greenhouse from a browser on any device so that I am not tied to a specific phone or application.falseMicrolab Jira5b8ef41d-7a73-399f-9666-c949acb53653GMS-34
- As an operator, I want a simple overview page so that I can understand the state of my greenhouse at a glance.falseMicrolab Jira5b8ef41d-7a73-399f-9666-c949acb53653GMS-35
- As a small-scale farmer, I want the website to look and work well on my phone so that I do not need a computer to use the system.falseMicrolab Jira5b8ef41d-7a73-399f-9666-c949acb53653GMS-36

#### Job Stories:

- When I am traveling, I want to access the dashboard from any browser so I can monitor my greenhouse without carrying specific hardware.falseMicrolab Jira5b8ef41d-7a73-399f-9666-c949acb53653GMS-37
- When checking greenhouse status quickly, I want a clear single-page overview so I can assess all critical conditions at a glance.falseMicrolab Jira5b8ef41d-7a73-399f-9666-c949acb53653GMS-38
- When checking the greenhouse on-the-go, I want the interface to be fully functional on my smartphone so I can manage everything without needing a computer.falseMicrolab Jira5b8ef41d-7a73-399f-9666-c949acb53653GMS-39
****

### Alerts & Notifications false Microlab Jira 5b8ef41d-7a73-399f-9666-c949acb53653 GMS-4

Stakeholder Requirement: The system should deliver timely alerts through SMS, push notifications, or on-screen warnings when thresholds are exceeded.

#### User Stories:

- As a farmer, I want to be notified on my phone when something goes wrong so that I can react even when I am away from the computer.falseMicrolab Jira5b8ef41d-7a73-399f-9666-c949acb53653GMS-40

#### Job Stories:

- When a critical threshold is exceeded, I want a push notification on my phone so I can react immediately even when away from the site.falseMicrolab Jira5b8ef41d-7a73-399f-9666-c949acb53653GMS-41
****

### Historical Data, Reports & Analytics false Microlab Jira 5b8ef41d-7a73-399f-9666-c949acb53653 GMS-5

Stakeholder Requirement: The system should store environmental history, visualize trends, and support data export for reporting and compliance.

#### User Stories:

- As a greenhouse operator, I want to see how conditions have changed over the past weeks and months so that I can make better planting and management decisions.falseMicrolab Jira5b8ef41d-7a73-399f-9666-c949acb53653GMS-42
- As a business owner, I want to download reports from the system so that I can share them with investors or agronomists.falseMicrolab Jira5b8ef41d-7a73-399f-9666-c949acb53653GMS-43
- As a business owner, I want to export sensor data to a spreadsheet so that I can share it with my agronomist or include it in business reports.falseMicrolab Jiraissuekey,summary,issuetype,created,updated,duedate,assignee,reporter,priority,status,resolutionkey,summary,type,created,updated,due,assignee,reporter,priority,status,resolution5b8ef41d-7a73-399f-9666-c949acb53653GMS-44

#### Job Stories:

- When planning the next growing season, I want to review environmental trends from previous months so I can optimize conditions for better yield.falseMicrolab Jira5b8ef41d-7a73-399f-9666-c949acb53653GMS-49
- When meeting with investors or agronomists, I want to export a formatted data report so I can present evidence of system performance.falseMicrolab Jira5b8ef41d-7a73-399f-9666-c949acb53653GMS-50
- When preparing records for compliance or advisory meetings, I want to export sensor data to Excel or CSV so I can share it with agronomists or authorities.falseMicrolab Jira5b8ef41d-7a73-399f-9666-c949acb53653GMS-51
****

### Connectivity & Network Reliability false Microlab Jira 5b8ef41d-7a73-399f-9666-c949acb53653 GMS-6

Stakeholder Requirement: The system must operate reliably over 4G/5G mobile networks and function on low-bandwidth connections.

#### User Stories:

- As a rural farmer, I want the system to work well over mobile internet so that I can use it without needing to install a wired connection at my greenhouse.falseMicrolab Jira5b8ef41d-7a73-399f-9666-c949acb53653GMS-52
- As a small-scale farmer using a mobile data plan, I want the website to be lightweight so that it does not consume too much data or load too slowly.

#### Job Stories:

- When located in a rural area with only mobile internet, I want the system to connect reliably over 4G/5G so I can use all features without a fixed broadband line.
- When accessing the dashboard on a limited mobile data plan, I want pages to load quickly and consume minimal bandwidth so I can use the system cost-effectively.
****

### Affordability & Cost Optimization false Microlab Jira 5b8ef41d-7a73-399f-9666-c949acb53653 GMS-7

Stakeholder Requirement: The system should be affordable for small-scale farmers and demonstrate measurable savings in water and energy costs.

#### User Stories:

- As a small farmer, I want a solution I can actually afford so that I do not need to take on significant financial risk to automate my greenhouse.
- As an investor, I want to see proven reductions in operational costs so that I can evaluate the return on investment before committing funds.

#### Job Stories:

- When deciding to invest in automation, I want transparent pricing and a cost estimate so I can assess whether the system fits my budget.
- When reviewing operational results, I want measurable data on water and energy savings so I can calculate the return on investment.
****

### Multi-Site/ Multi-Zone Management false Microlab Jira 5b8ef41d-7a73-399f-9666-c949acb53653 GMS-8

Stakeholder Requirement: The system should enable centralized monitoring and management of multiple greenhouse sites or zones, allowing users to compare performance data and allocate resources without visiting each location.

#### User Stories:

- As a large agricultural enterprise manager, I want a unified dashboard for all my greenhouse sites so that I can manage operations without visiting each location.falseMicrolab Jiraissuekey,summary,issuetype,created,updated,duedate,assignee,reporter,priority,status,resolutionkey,summary,type,created,updated,due,assignee,reporter,priority,status,resolution5b8ef41d-7a73-399f-9666-c949acb53653GMS-45

#### Job Stories:

- When managing multiple zones, I want to compare environmental data across sites so I can identify under-performance and allocate resources efficiently.falseMicrolab Jira5b8ef41d-7a73-399f-9666-c949acb53653GMS-46
****

### Cybersecurity false Microlab Jira 5b8ef41d-7a73-399f-9666-c949acb53653 GMS-9

Stakeholder Requirement: The system should ensure all cloud communications and actuator controls are protected through encryption and authentication mechanisms, preventing unauthorized access or manipulation by external parties.

#### User Stories:

- As a system administrator, I want all data transmissions encrypted so that unauthorized parties cannot access or manipulate greenhouse controls.falseMicrolab Jira5b8ef41d-7a73-399f-9666-c949acb53653GMS-47

#### Job Stories:

- When connecting the greenhouse controller to the cloud, I want secure authentication so I can prevent unauthorized access to critical actuator controls.falseMicrolab Jira5b8ef41d-7a73-399f-9666-c949acb53653GMS-48
