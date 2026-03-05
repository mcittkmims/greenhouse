# 04 - GMS -WP4.1 Develop Stakeholder Requirements

> Source: http://confluence.microlab.club/rest/api/content/42634110 | Version: 7

****

## Requirements

| Category | Stakeholder Requirements | US(User Stories) | JS(Job Stories) |
| --- | --- | --- | --- |
| Environmental Monitoring and Control | The system should monitor soil moisture in real time and trigger automated irrigation based on configurable thresholds. | As a farmer, I want the system to monitor soil moisture continuously so that my crops receive water only when needed. | When soil moisture drops below a set threshold, I want the system to automatically activate irrigation so I can avoid crop stress without being on-site. |
| Environmental Monitoring and Control | The system must continuously monitor air temperature and trigger heating or ventilation actuators when thresholds are exceeded. | As a greenhouse operator, I want real-time temperature monitoring so that I can prevent crop damage from overheating or frost. | When temperature falls below 10°C or exceeds 35°C, I want the system to activate heating or ventilation automatically so I can protect my crops without manual intervention. |
| Environmental Monitoring and Control | The system must monitor relative humidity at canopy level and activate humidification or ventilation actuators accordingly. | As an operator, I want humidity levels tracked automatically so that I can prevent fungal diseases caused by excessive moisture. | When humidity exceeds safe levels, I want the system to trigger ventilation so I can reduce disease risk without constant manual checks. |
| Environmental Monitoring and Control | The system should monitor CO₂ concentration and support controlled enrichment to optimize photosynthesis. | As a greenhouse operator, I want CO₂ levels tracked so that I can optimize growing conditions and increase yield. | When CO₂ drops below optimal levels, I want the system to alert me so I can adjust enrichment and improve crop productivity. |
| Environmental Monitoring and Control | The system should display live readings that refresh automatically without needing to reload the page. | As a greenhouse operator, I want up-to-date readings on my screen so that I can catch problems as soon as they happen. | When conditions change rapidly, I want the dashboard to refresh automatically so I can respond before crop damage occurs. |
| Environmental Monitoring and Control | The system should alert user when any reading goes outside the acceptable range. | As a farmer, I want to receive a warning when conditions become dangerous so that I can act before my crops are damaged. | When a parameter exceeds a safe range, I want an immediate alert so I can intervene before plants are stressed. |
| Automated Irrigation | The system should allow operators to set irrigation schedules as a backup to sensor-based control. | As a farmer, I want irrigation to follow a timed schedule so that my greenhouse can run for months without anyone on-site. | When I am abroad for extended periods, I want a timed irrigation schedule to run autonomously so I can keep the greenhouse operational without being on-site. |
| Climate Control | The system should allow operators to set acceptable ranges for temperature and humidity. | As a farmer, I want to define my own comfort zones for the greenhouse so that the system reacts according to my specific crop needs. | When I switch to a different crop, I want to reconfigure temperature and humidity ranges so I can adapt the system to new plant requirements. |
| Web Dashboard | The system should have a web-based dashboard accessible from any browser without installing an app. | As a greenhouse owner, I want to check my greenhouse from a browser on any device so that I am not tied to a specific phone or application. | When I am traveling, I want to access the dashboard from any browser so I can monitor my greenhouse without carrying specific hardware. |
| Web Dashboard | The dashboard should show live sensor data, active alerts, and actuator status in a clear and simple layout. | As an operator, I want a simple overview page so that I can understand the state of my greenhouse at a glance. | When checking greenhouse status quickly, I want a clear single-page overview so I can assess all critical conditions at a glance. |
| Alerts and Notifications | The system should send SMS or push notifications when critical thresholds are exceeded. | As a farmer, I want to be notified on my phone when something goes wrong so that I can react even when I am away from the computer. | When a critical threshold is exceeded, I want a push notification on my phone so I can react immediately even when away from the site. |
| Historical Data and Reports | The system should store sensor data history and allow operators to view trends over time. | As a greenhouse operator, I want to see how conditions have changed over the past weeks and months so that I can make better planting and management decisions. | When planning the next growing season, I want to review environmental trends from previous months so I can optimize conditions for better yield. |
| Historical Data and Reports | Operators should be able to export data reports for record-keeping and compliance. | As a business owner, I want to download reports from the system so that I can share them with investors or agronomists. | When meeting with investors or agronomists, I want to export a formatted data report so I can present evidence of system performance. |
| Affordability | The system should be affordable enough for small-scale farmers with limited budgets. | As a small farmer, I want a solution I can actually afford so that I do not need to take on significant financial risk to automate my greenhouse. | When deciding to invest in automation, I want transparent pricing and a cost estimate so I can assess whether the system fits my budget. |
| Affordability | The system should demonstrate clear cost savings through reduced water and energy use. | As an investor, I want to see proven reductions in operational costs so that I can evaluate the return on investment before committing funds. | When reviewing operational results, I want measurable data on water and energy savings so I can calculate the return on investment. |
| Multi-Site / Multi-Zone Management | The system should support monitoring and control of multiple greenhouse zones or sites from a single dashboard. | As a large agricultural enterprise manager, I want a unified dashboard for all my greenhouse sites so that I can manage operations without visiting each location. | When managing multiple zones, I want to compare environmental data across sites so I can identify under-performance and allocate resources efficiently. |
| Cybersecurity | The system should implement TLS encryption, X.509 certificate authentication, and role-based access control for all cloud communications. | As a system administrator, I want all data transmissions encrypted so that unauthorized parties cannot access or manipulate greenhouse controls. | When connecting the greenhouse controller to the cloud, I want secure authentication so I can prevent unauthorized access to critical actuator controls. |
| Survey Extracted Stakeholder Requirements: |  |  |  |
| Soil and Water Management | Soil moisture monitoring should be treated as the top priority across all greenhouse operations. | As a farmer, I want soil moisture to be the first thing shown on my dashboard so that I always know if my crops need water. | When opening the dashboard, I want soil moisture to appear prominently so I can immediately see if irrigation is needed. |
| Soil and Water Management | The system should support remote activation of irrigation from the website. | As a greenhouse owner abroad, I want to start watering from my browser so that I can react to unexpected dry spells even when I am not in the country. | When I am outside the country for weeks, I want to remotely activate irrigation from my browser so I can respond to unexpected dry spells. |
| Soil and Water Management | The system should prevent over-watering by stopping irrigation once the moisture level reaches the target. | As a farmer, I want irrigation to stop automatically when the soil is wet enough so that I do not waste water or damage the roots. | When soil reaches the target moisture level, I want irrigation to stop automatically so I can prevent over-watering and root damage. |
| Temperature and Humidity | The system should alert the operator separately for overheating during the day and frost risk at night. | As a farmer, I want different alerts for heat and cold so that I know exactly what kind of problem I am dealing with. | When nighttime temperatures drop unexpectedly, I want a frost-specific alert separate from heat warnings so I can take the right corrective action. |
| Connectivity | The system must work reliably over 4G/5G mobile data, since many greenhouse locations rely on mobile internet rather than fixed broadband. | As a rural farmer, I want the system to work well over mobile internet so that I can use it without needing to install a wired connection at my greenhouse. | When located in a rural area with only mobile internet, I want the system to connect reliably over 4G/5G so I can use all features without a fixed broadband line. |
| Connectivity | The website should load quickly and function on low-bandwidth connections. | As a small-scale farmer using a mobile data plan, I want the website to be lightweight so that it does not consume too much data or load too slowly. | When accessing the dashboard on a limited mobile data plan, I want pages to load quickly and consume minimal bandwidth so I can use the system cost-effectively. |
| Web Dashboard | The website should work well on mobile screens since most farmers rely on smartphones rather than desktop computers. | As a small-scale farmer, I want the website to look and work well on my phone so that I do not need a computer to use the system. | When checking the greenhouse on-the-go, I want the interface to be fully functional on my smartphone so I can manage everything without needing a computer. |
| Historical Data and Reports | Data export to Excel or CSV should be supported for farmers and agronomists who need records for external use. | As a business owner, I want to export sensor data to a spreadsheet so that I can share it with my agronomist or include it in business reports | When preparing records for compliance or advisory meetings, I want to export sensor data to Excel or CSV so I can share it with agronomists or authorities. |
****

## Classes

****

### Environmental Monitoring and Control

Stakeholder Requirement: The system should continuously monitor, control and display all key greenhouse parameters in real time.

#### User Stories:

- As a farmer, I want the system to monitor soil moisture continuously so that my crops receive water only when needed.
- As a greenhouse operator, I want real-time temperature monitoring so that I can prevent crop damage from overheating or frost.
- As an operator, I want humidity levels tracked automatically so that I can prevent fungal diseases caused by excessive moisture.
- As a greenhouse operator, I want CO₂ levels tracked so that I can optimize growing conditions and increase yield.
- As a greenhouse operator, I want up-to-date readings on my screen so that I can catch problems as soon as they happen.
- As a farmer, I want to receive a warning when conditions become dangerous so that I can act before my crops are damaged.

#### Job Stories:

- When soil moisture drops below a set threshold, I want the system to automatically activate irrigation so I can avoid crop stress without being on-site.
- When temperature falls below 10°C or exceeds 35°C, I want the system to activate heating or ventilation automatically so I can protect my crops without manual intervention.
- When humidity exceeds safe levels, I want the system to trigger ventilation so I can reduce disease risk without constant manual checks.
- When CO₂ drops below optimal levels, I want the system to alert me so I can adjust enrichment and improve crop productivity.
- When conditions change rapidly, I want the dashboard to refresh automatically so I can respond before crop damage occurs.
- When a parameter exceeds a safe range, I want an immediate alert so I can intervene before plants are stressed.
****

### Automated Irrigation and Climate Control

Stakeholder Requirement: The system should allow users to configure and schedule irrigation and climate parameters remotely, enabling fully autonomous greenhouse operation without requiring on-site presence.

#### User Stories:

- As a farmer, I want irrigation to follow a timed schedule so that my greenhouse can run for months without anyone on-site.
- As a farmer, I want to define my own comfort zones for the greenhouse so that the system reacts according to my specific crop needs.
- As a farmer, I want soil moisture to be the first thing shown on my dashboard so that I always know if my crops need water.
- As a greenhouse owner abroad, I want to start watering from my browser so that I can react to unexpected dry spells even when I am not in the country.
- As a farmer, I want irrigation to stop automatically when the soil is wet enough so that I do not waste water or damage the roots.
-  As a farmer, I want different alerts for heat and cold so that I know exactly what kind of problem I am dealing with. 

#### Job Stories:

- When I am abroad for extended periods, I want a timed irrigation schedule to run autonomously so I can keep the greenhouse operational without being on-site.
- When I switch to a different crop, I want to reconfigure temperature and humidity ranges so I can adapt the system to new plant requirements.
- When opening the dashboard, I want soil moisture to appear prominently so I can immediately see if irrigation is needed.
- When I am outside the country for weeks, I want to remotely activate irrigation from my browser so I can respond to unexpected dry spells.
- When soil reaches the target moisture level, I want irrigation to stop automatically so I can prevent over-watering and root damage.
- When nighttime temperatures drop unexpectedly, I want a frost-specific alert separate from heat warnings so I can take the right corrective action.
****

### Web Dashboard & Mobile Accessibility

Stakeholder Requirement: The system should provide a browser-accessible, mobile-friendly dashboard with a clear and lightweight interface.

#### User Stories:

- As a greenhouse owner, I want to check my greenhouse from a browser on any device so that I am not tied to a specific phone or application.
- As an operator, I want a simple overview page so that I can understand the state of my greenhouse at a glance.
- As a small-scale farmer, I want the website to look and work well on my phone so that I do not need a computer to use the system.   
- As a small-scale farmer using a mobile data plan, I want the website to be lightweight so that it does not consume too much data or load too slowly.

#### Job Stories:

- When I am traveling, I want to access the dashboard from any browser so I can monitor my greenhouse without carrying specific hardware.
- When checking greenhouse status quickly, I want a clear single-page overview so I can assess all critical conditions at a glance.
- When checking the greenhouse on-the-go, I want the interface to be fully functional on my smartphone so I can manage everything without needing a computer.
- When accessing the dashboard on a limited mobile data plan, I want pages to load quickly and consume minimal bandwidth so I can use the system cost-effectively.
****

### Alerts & Notifications

Stakeholder Requirement: The system should deliver timely alerts through SMS, push notifications, or on-screen warnings when thresholds are exceeded.

#### User Stories:

- As a farmer, I want to be notified on my phone when something goes wrong so that I can react even when I am away from the computer.

#### Job Stories:

- When a critical threshold is exceeded, I want a push notification on my phone so I can react immediately even when away from the site.
****

### Historical Data, Reports & Analytics

Stakeholder Requirement: The system should store environmental history, visualize trends, and support data export for reporting and compliance.

#### User Stories:

- As a greenhouse operator, I want to see how conditions have changed over the past weeks and months so that I can make better planting and management decisions.
- As a business owner, I want to download reports from the system so that I can share them with investors or agronomists.
- As a business owner, I want to export sensor data to a spreadsheet so that I can share it with my agronomist or include it in business reports.

#### Job Stories:

- When planning the next growing season, I want to review environmental trends from previous months so I can optimize conditions for better yield.
- When meeting with investors or agronomists, I want to export a formatted data report so I can present evidence of system performance.
- When preparing records for compliance or advisory meetings, I want to export sensor data to Excel or CSV so I can share it with agronomists or authorities.
****

### Connectivity & Network Reliability

Stakeholder Requirement: The system must operate reliably over 4G/5G mobile networks and function on low-bandwidth connections.

#### User Stories:

- As a rural farmer, I want the system to work well over mobile internet so that I can use it without needing to install a wired connection at my greenhouse.
- As a small-scale farmer using a mobile data plan, I want the website to be lightweight so that it does not consume too much data or load too slowly.

#### Job Stories:

- When located in a rural area with only mobile internet, I want the system to connect reliably over 4G/5G so I can use all features without a fixed broadband line.
- When accessing the dashboard on a limited mobile data plan, I want pages to load quickly and consume minimal bandwidth so I can use the system cost-effectively.
****

### Affordability & Cost Optimization

Stakeholder Requirement: The system should be affordable for small-scale farmers and demonstrate measurable savings in water and energy costs.

#### User Stories:

- As a small farmer, I want a solution I can actually afford so that I do not need to take on significant financial risk to automate my greenhouse.
- As an investor, I want to see proven reductions in operational costs so that I can evaluate the return on investment before committing funds.
- As a business owner, I want the system to be cost-effective so that I can minimize operational expenses.

#### Job Stories:

- When deciding to invest in automation, I want transparent pricing and a cost estimate so I can assess whether the system fits my budget.
- When reviewing operational results, I want measurable data on water and energy savings so I can calculate the return on investment.
- When evaluating automation solutions, I want to ensure the system is affordable so I can justify the investment.
****

### Multi-Site/ Multi-Zone Management

Stakeholder Requirement: The system should enable centralized monitoring and management of multiple greenhouse sites or zones, allowing users to compare performance data and allocate resources without visiting each location.

#### User Stories:

- As a large agricultural enterprise manager, I want a unified dashboard for all my greenhouse sites so that I can manage operations without visiting each location.

#### Job Stories:

- When managing multiple zones, I want to compare environmental data across sites so I can identify under-performance and allocate resources efficiently.
****

### Cybersecurity

Stakeholder Requirement: The system should ensure all cloud communications and actuator controls are protected through encryption and authentication mechanisms, preventing unauthorized access or manipulation by external parties.

#### User Stories:

- As a system administrator, I want all data transmissions encrypted so that unauthorized parties cannot access or manipulate greenhouse controls.

#### Job Stories:

- When connecting the greenhouse controller to the cloud, I want secure authentication so I can prevent unauthorized access to critical actuator controls.
