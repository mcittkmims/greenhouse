# 04 - GMS -WP3.3 Business Case-Survey

> Source: http://confluence.microlab.club/rest/api/content/42634064 | Version: 2

****

# 1. Survey Objective

The primary goal of this survey was to validate the technical requirements and user priorities for the Greenhouse Management System (GMS) by gathering structured feedback from a representative sample of farmers, greenhouse operators, technical researchers, and agricultural enterprise representatives active in Moldova.
The survey targeted four specific areas of inquiry:
- Critical Triggers — Identifying which environmental parameters (soil moisture, air temperature, humidity, light intensity) are the highest priority for real-time monitoring and automated alerts.
- Connectivity Feasibility — Assessing whether existing internet infrastructure at greenhouse locations supports the cloud-based architecture proposed in the WP2.1 Technology Research.
- Cost vs. Value Perception — Possible willingness to invest in a remote-monitoring solution versus simpler local automation, particularly among small-scale farmers with limited budgets.
- UI/UX Preferences — Determining whether stakeholders prefer a detailed data dashboard (mobile application), simplified push/SMS notifications, or local audio/visual alarms.

The survey was created and distributed via Google Forms during February 18–21, 2026, and collected a total of 18 valid responses with valid for review.****

# 2. Target Audience

The survey was deliberately distributed across three stakeholder tiers, reflecting the stakeholder categorization established in the project documentation:
**Tier A — Primary Users (Core Focus)**
- Small-scale Farmers: Individuals in rural Moldova managing greenhouses typically under 300 m², often relying on mobile connectivity and looking for affordable, low-maintenance solutions.
- Large-scale Agricultural Enterprises: Entities managing multiple or larger industrial greenhouses (1+ ha) with more complex data and multi-zone management needs.
- Greenhouse Operators / Technicians: Hands-on personnel who interact directly with sensors and control equipment on a daily basis.

**Tier B — Technical Experts (Validation Group)**
- Technical Researchers and University Staff: Academics from the Technical University of Moldova (TUM) and similar institutions, providing validation of sensor logic, algorithm design, and system architecture.
****

# 3. Survey Design

The survey was structured to collect both quantitative data (multiple-choice, 1–5 Likert rating scales) and qualitative data (open-ended questions), allowing for statistical analysis alongside thematic insight gathering.
Questions covered:
- Respondent classification and greenhouse area managed (profiling questions).
- Rating scales (1 = Not important, 5 = Very important) for four key environmental parameters: soil moisture, air temperature, relative humidity, and light/CO2 levels.
- Most frequent production-impacting incident (open-ended).
- Internet connectivity availability at the greenhouse site (multiple-choice).
- Preferred alert delivery method (multiple-choice).
- Perceived economic value of full irrigation automation (1–5 scale).
- Additional indispensable feature for a modern GMS (open-ended).

All questions were reviewed for neutral phrasing to avoid leading respondents toward a specific answer. The survey was introduced with a brief explanation of its purpose: to help the GMS project team understand real-world needs before finalizing system specifications.

****

# 4. Response Collection & Organization

Responses were collected via Google Forms and exported as a CSV file for analysis. All 18 responses were reviewed: no duplicates, incomplete submissions, or clearly invalid entries were identified. Responses were organized by question type:
- Multiple-choice and rating-scale questions: Processed for frequency counts, percentage distributions, and average scores.
- Open-ended questions: Manually reviewed and categorized into recurring themes.
****

# 5. Quantitative Analysis

****

## 5.1 Respondent Profile

The survey reached a diverse cross-section of the identified stakeholder tiers. The distribution confirms that primary users (farmers and operators) dominated the sample, lending direct relevance to the system's core use-case validation.

*Figure 1 — Distribution of respondents by activity category (18 responses)*

| Parameter / Question | Result |
| --- | --- |
| Small-scale Farmers | 9 respondents (50.0%) |
| Large Agricultural Enterprise Representatives | 3 respondents (16.7%) |
| Greenhouse Operators / Technicians | 2 respondents (11.1%) |
| Technical Experts / Researchers | 4 respondents (22.2%) |

Half of all respondents are small-scale farmers — the most resource-constrained primary user segment. This skew is intentional and valuable: it ensures that system requirements are validated against real-world constraints such as limited budgets, mobile-first access, and minimal technical expertise. The 22.2% share of technical experts provides a useful counterbalance for assessing feasibility.****

## 5.2 Greenhouse Size Distribution

Respondents manage a wide range of greenhouse sizes, from as small as 12 m² to as large as 5 hectares. The majority of small-scale farmers reported areas between 50–250 m², while large enterprise representatives reported 2–5 ha facilities. This heterogeneity confirms the need for a scalable GMS architecture that can serve both micro-scale personal greenhouses and industrial multi-zone environments.****

## 5.3 Environmental Parameter Priority (Rating Scale 1–5)

Respondents rated the criticality of real-time monitoring for four environmental parameters on a scale from 1 (not important) to 5 (very important). The results are presented below, sorted by average score:
| Parameter / Question | Result |
| --- | --- |
| Soil Moisture | Avg. 4.83 / 5.00 |
| Air Temperature | Avg. 4.61 / 5.00 |
| Relative Humidity | Avg. 4.72 / 5.00 |
| Light / CO2 Levels | Avg. 4.22 / 5.00 |

All four parameters received high scores, with soil moisture and humidity rated most critically. Notably, soil moisture scored 5/5 in the majority of farmer responses. Only one respondent (a small-scale farmer with a 250 m² greenhouse citing water pressure issues) rated humidity at 2/5, suggesting a specific situational context rather than a general deprioritization. Light/CO2 monitoring, while still rated highly, is seen as slightly less urgent — possibly because it is less commonly disrupted compared to water and temperature regulation in Moldovan field conditions.
This data directly validates the sensor selection in WP2.1: prioritizing soil moisture sensors (capacitive type), DHT22/SHT31 temperature-humidity sensors, and supporting CO2/light sensors as secondary instrumentation is aligned with user needs.****

## 5.4 Internet Connectivity at Greenhouse Site

Understanding connectivity is critical to validating the GMS cloud architecture. The survey asked whether a stable internet connection exists at the greenhouse location.

*Figure 2 — Internet connectivity type available at greenhouse locations (18 responses)*
| Parameter / Question | Result |
| --- | --- |
| Cable / Wi-Fi (fixed broadband) | 6 respondents (33.3%) |
| Mobile Data (4G/5G) | 10 respondents (55.6%) |
| No stable connection | 2 respondents (11.1%) |

The dominant connectivity scenario is mobile data (4G/5G), accounting for over half of all responses. This is a critical infrastructure finding: the GMS cloud connectivity design must be optimized for mobile network environments rather than assuming fixed broadband. Only 33.3% have cable or Wi-Fi, while a notable 11.1% report no stable connection at all.
Implications for the GMS architecture:
- The system must support lightweight MQTT or HTTPS communication protocols that operate efficiently over 4G/5G links with variable latency.
- Local data buffering (edge caching on the embedded controller) should be implemented to handle connectivity interruptions and ensure no data loss during temporary outages — essential for the 11.1% with unstable connectivity.
- Wi-Fi-only gateway designs should be reconsidered or made optional, with 4G/LTE modem integration as a first-class connectivity option.
****

## 5.5 Preferred Alert Delivery Method

This question directly informs the UI/UX design and notification architecture of the GMS dashboard and alerting subsystem.

*Figure 3 — Preferred method for receiving system alerts (18 responses)*
| Parameter / Question | Result |
| --- | --- |
| Dedicated Mobile Application (Dashboard) | 12 respondents (66.7%) |
| SMS / Push Notification | 5 respondents (27.8%) |
| Local Audio/Visual Alarm | 1 respondent (5.5%) |

A strong majority, 66.7%,  prefer a dedicated mobile dashboard application as their primary alert channel. This is a definitive signal that the GMS interface investment should prioritize a polished, user-friendly mobile application with real-time data visualization. The 27.8% preference for SMS/Push notifications is complementary rather than contradictory: these users likely want alerts on top of a dashboard, not instead of one. The near-zero preference for local alarms (5.5%, a single respondent with no stable internet) is consistent with connectivity data.
This finding validates the development of a cloud-connected mobile dashboard as the primary user interface, with SMS/push notifications as a secondary, configurable alert layer.****

## 5.6 Perceived Economic Value of Full Irrigation Automation

Respondents rated the economic value that full automation of irrigation would bring to their operations on a scale of 1–5.
| Parameter / Question | Result |
| --- | --- |
| Score 5 (Maximum economic value) | 13 respondents (72.2%) |
| Score 4 (High value) | 4 respondents (22.2%) |
| Score 3 (Moderate value) | 1 respondent (5.6%) |
| Score 1–2 (Low value) | 0 respondents (0%) |

The results are unambiguous: 94.4% of respondents rated automated irrigation as either high or maximum economic value. No respondent scored it below 3. The single score-3 respondent was a large enterprise representative managing a 350 m² site who cited pest control as their primary problem — suggesting that for them, irrigation automation is valuable but not their top concern. This does not detract from the overwhelming consensus across the rest of the sample.
This finding provides strong validation for automated irrigation as a core GMS feature and supports stakeholder buy-in arguments for investors and agricultural agencies.****

# 6. Qualitative Analysis

****

## 6.1 Most Frequent Production-Impacting Incidents

Respondents were asked to describe the most frequent incident that currently affects their greenhouse production. Responses were translated and categorized into recurring themes:
| Parameter / Question | Result |
| --- | --- |
| Drought / Soil Moisture Deficit | 7 mentions (~39%) |
| Temperature Extremes (overheating / night cold) | 4 mentions (~22%) |
| Irrigation System Failures | 3 mentions (~17%) |
| Pest / Insect Infestations | 2 mentions (~11%) |
| Inaccurate / Unreliable Sensor Data | 2 mentions (~11%) |

Drought and insufficient soil moisture is clearly the dominant pain point, mentioned by 39% of respondents. This reinforces the rating-scale finding that soil moisture monitoring is the single most critical parameter. Temperature extremes — overheating during summer days and frost risk at night — were the second most mentioned issue, directly validating the need for automated ventilation and heating control.
Two technical experts specifically mentioned inaccurate or approximate sensor data as a primary concern, highlighting a quality-of-measurement requirement: the GMS must not only collect data but ensure its precision and reliability. One expert noted a need for Excel data export and verified sensor integration, pointing toward robust data management and audit-trail capabilities.****

## 6.2 Indispensable Feature Requests

The final open-ended question asked respondents to name one additional feature they would consider indispensable in a modern greenhouse management system. Responses clustered into four primary themes:
**Theme 1 — Automated Irrigation Control (Most Requested)**
Multiple respondents explicitly requested fully automatic irrigation scheduling, including remote activation, time-based scheduling, and soil-moisture-triggered watering. One respondent highlighted the need to operate the system autonomously while away from the country for extended periods (up to 3 months) — a use case that strongly argues for robust offline scheduling logic in addition to cloud control.
**Theme 2 — Historical Data, Reports & Analytics**
Several respondents requested data history, graphical trend visualization, and periodic reports. Requests included Excel export functionality and integration with verified sensor hardware — features that align with long-term performance monitoring and regulatory compliance. This indicates that the GMS should go beyond real-time monitoring to provide meaningful, actionable historical analytics.
**Theme 3 — Automated Microclimate Regulation**
Respondents requested comprehensive automatic regulation of the full microclimate — not just irrigation, but also humidity control, ventilation scheduling, and temperature balancing across zones. One operator specifically mentioned a program for automatic irrigation combined with threshold-based alerts for temperature and humidity.
**Theme 4 — Wireless Sensor Integration & Real-Time Dashboard**
A researcher-level respondent requested wireless sensor integration (temperature, soil humidity, air humidity, light intensity) paired with a real-time monitoring interface. Another respondent asked for sector-based management (multi-zone control) and graph-based reporting — indicating the need for spatial segmentation in larger greenhouses.****

# 8. Conclusions

The stakeholder survey successfully validated the core design assumptions of the Greenhouse Management System outlined in the WP2.1 Technology Research. With 18 responses from a diverse and representative stakeholder cross-section, the data provides high-confidence directional guidance for the upcoming development phases.
Three conclusions stand out as most impactful:
- Soil moisture monitoring and automated irrigation are the highest-value, highest-urgency features across all user segments. Any minimum viable product (MVP) must include these as core functionality.
- 4G/5G is the real-world connectivity standard for greenhouse locations in Moldova. The GMS cannot assume fixed broadband and must be built mobile-first — both in its communication stack and its user interface.
- Stakeholders are not merely interested in automation for its own sake — they want traceability. The consistent demand for historical data, reports, and analytics indicates that the GMS should position itself as a data platform, not just a control system.
