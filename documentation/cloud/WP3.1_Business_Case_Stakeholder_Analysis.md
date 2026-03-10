# 04 - GMS -WP3.1 Business Case/Stakeholder Analysis

> Source: http://confluence.microlab.club/rest/api/content/42634061 | Version: 6

****

# Business Case Analysis

**

## Business Domain Analysis

The domain of AgriTech (Agricultural Technology) focuses on integrating modern technologies into agricultural practices to improve productivity, sustainability, and operational efficiency. As climate variability increases and Global food demand will increase by 50-60 percent from 2019 to 2050, as the world’s population grows by 1.5 billion, agriculture is progressively adopting automation, sensor-based monitoring, and data-driven decision-making systems . Within this domain, greenhouse cultivation plays a significant role, as it enables controlled plant production independent of seasonal and environmental constraints. By regulating temperature, humidity, soil moisture, and ventilation, greenhouses create stable growing environments that enhance crop quality and yield consistency.
Despite these advantages, many greenhouse operations still rely heavily on manual supervision and reactive management. Farmers must constantly monitor environmental parameters and manually adjust irrigation, heating, and ventilation systems. This traditional approach causes several challenges.
One major issue is **uncontrolled resource consumption**. Agriculture is responsible for approximately 70% of freshwater use, posing serious challenges in regions affected by climate change and water scarcity. Manual greenhouse management often results not only in excessive use of water, but also of energy and fertilizers due to inaccurate estimation of plant requirements. Over-irrigation and inefficient climate control increase operational costs and contribute to environmental waste.
Another challenge is the **reactive rather than preventive nature of management**. In the absence of real-time monitoring, farmers typically detect problems and plant stress only after it is visible or disease symptoms appear, because plant stress is most often non-visible, at cellular level. By that stage, crop damage may already have occurred, leading to reduced yield and financial loss.
The need for** 24/7 monitoring further intensifies operational pressure**. Greenhouse environments can change rapidly, especially during extreme weather events such as heatwaves or cold snaps. Manual supervision is labor-intensive and unsustainable, often resulting in worker fatigue and delayed responses during off-hours.
The complexity increases when **addressing multi-site management**. Farmers operating multiple greenhouses cannot physically supervise all facilities simultaneously, leading to uneven monitoring and inconsistent environmental conditions across locations.
Additionally, **agricultural production remains highly vulnerable to extreme weather conditions**. Sudden temperature spikes, storms, or unexpected cold periods can overwhelm manual response capabilities, causing crop losses due to delayed intervention. In Moldova, the poor harvests of recent years are more than 50% caused by drought, especially in the Southern Zone, where severe and extremely severe droughts prevail. 
Finally, there is a **limitation in predictive capability**. Without structured collection and analysis of historical environmental data linked to crop outcomes, farmers cannot identify optimal growth patterns or accurately forecast yield. This lack of predictive insight makes long-term planning uncertain and restricts strategic optimization.
Here is where the **problem definition **comes in: Farmers and greenhouse operators often face difficulties in maintaining stable environmental conditions for plant growth. Monitoring and adjusting factors such as temperature and humidity usually requires constant attention and manual effort. Delayed or incorrect adjustments can cause plant stress and reduce crop quality and yield. As a result, resources such as time, water, and energy are often used inefficiently.**

## Solution Proposal

To address the identified challenges within the AgriTech greenhouse domain, the project proposes the development of an intelligent greenhouse automation and monitoring system based on industrial control principles and cloud-integrated data management. The system relies on an industrial PLC platform(Arduino Portenta Machine Control) to ensure stable, reliable, and continuous environmental control within greenhouse facilities.
Environmental sensors measure key growth parameters such as temperature, humidity, and soil moisture. Based on real-time data, the control unit automatically regulates irrigation, ventilation, and climate conditions to maintain optimal plant environments. This reduces manual intervention, improves response time to environmental changes, and enhances overall resource efficiency. Need-based irrigation programs can reduce water consumption up to 40%, by optimizing the use of water resources based on the real crop conditions.
Cloud integration enables remote monitoring and centralized supervision of greenhouse conditions. Operators can access real-time data, adjust environmental settings, and receive alerts when parameters exceed acceptable limits. At the same time, the system maintains local control to ensure continuous functionality.
While the system is designed to support multiple crop types, this implementation focuses on tomato cultivation as a representative greenhouse crop due to its sensitivity to environmental fluctuations. Tomatoes were selected for three main reasons. First, they are highly sensitive to variations in temperature, humidity, and irrigation. After the summer of 2022, which was marked by hot, dry conditions, the French production of tomatoes for the fresh market fell 3% against 2021 results, despite a 7% increase in cultivated area. This makes them suitable for demonstrating the benefits of precise environmental control. Second, tomatoes are economically significant and widely cultivated, which makes the system practically relevant for commercial greenhouse operators. Third, tomato yield and quality are strongly influenced by environmental stability, allowing measurable evaluation of system performance.
Additionally, although tomatoes are one of Moldova’s main vegetable crops, the country does not fully meet its domestic demand for fresh tomatoes and relies partially on imports, especially outside peak growing seasons. As of 2025, Moldova remains the main consumer of Ukrainian tomatoes - 61.5% of Ukrainian exports of this vegetable are to Moldova. Improving greenhouse efficiency and yield stability through automation can contribute to increased local production and reduced dependency on external suppliers.
Overall, the proposed solution supports more consistent crop performance, optimized resource usage, and improved sustainability, while remaining adaptable to various greenhouse cultivation scenarios.**

## Use Cases and Technological Benefits

### Use Case 1: Cloud-Based Environmental Monitoring and Remote Management

Application: Remote monitoring of greenhouse conditions (temperature, humidity, soil moisture) via a cloud platform.
Implementation: Environmental sensors send real-time data through the PLC to a cloud dashboard. Operators can view current and historical conditions, set alerts for threshold breaches, and access the system from any internet-connected device.

#### Benefits

- Continuous remote access: Cloud-connected monitoring allows greenhouse conditions to be checked from anywhere, reducing the need for physical presence and minimizing labor intensity. 
- Data-driven decision support: Historical and real-time data enable better planning and environmental adjustments compared to manual observation alone. Research highlights that it is easier to predict impending weather patterns by measuring variables such as the temperature and humidity of the soil. Moreover, agriculture that is supported by IoT makes it easier to make better judgments on agricultural productivity. 
- Improved resource efficiency: Collecting and analyzing environmental data in the cloud provides insights that support more precise water and climate management, contributing to reduced waste and improved sustainability over traditional practice. 

### Use Case 2: Automated Climate Control for Enhanced Yield and Decreased Resource Use

Application: Automated regulation of greenhouse temperature and humidity to maintain stable conditions for tomato crops.
Implementation: Sensor data is evaluated in real time, and the PLC triggers ventilation, irrigation, shading, or heating when environmental parameters deviate from target ranges. The system maintains close control without constant human intervention.

#### Benefits

- Better resource utilization: Studies indicate that smart greenhouse environmental control systems can reduce resource consumption, such as water use up to 40% due to Need-based irrigation. Moreover, energy use can be reduced by around 25 %. 
- Yield and quality stability: Automated monitoring and control help maintain favorable growth conditions, reducing stress and environmental fluctuation impacts on plants. 
- Reduced manual workload: By automating climate adjustments, growers no longer need to continuously check and adjust environmental systems manually, freeing labor for other agriculture related activities.
**

## Existing Business Cases

****

### Microcontroller-Based Systems (Arduino-Driven Smart Greenhouse)

**Technology:** Arduino Mega 2560 microcontroller combined with an ESP8266 Wi-Fi module and ThingSpeak cloud platform for environmental monitoring and relay-based actuator control.
**Outcomes:** The system achieved approximately **4750 kWh energy savings per cultivation cycle** by optimizing heating and ventilation using real-time sensor data .
This solution represents a low-cost IoT greenhouse control system. It uses environmental sensors (temperature, humidity, CO₂, light intensity, soil moisture) connected to an Arduino board that controls irrigation pumps and ventilation fans through relay modules. Data is sent to the cloud for visualization and monitoring. While the system improves energy efficiency and reduces manual work, it relies on consumer-grade hardware with limited memory and processing power. It does not provide deterministic real-time control or industrial communication standards, which limits its suitability for large-scale commercial greenhouses.****

### Industrial Automation Systems (PLC/SCADA Architectures in Commercial Agriculture)

**Technology:** Industrial PLC and SCADA-based greenhouse control systems implementing advanced control strategies such as Model Predictive Control (MPC), Artificial Neural Networks (ANN), fuzzy logic, and PID control within Industry 4.0 architectures .
**Outcomes:** The use of Model Predictive Control demonstrated approximately **30% electrical energy savings** compared to traditional relay-based control in greenhouse environments, while maintaining stable temperature conditions .
Industrial automation systems use PLCs and SCADA platforms that are widely applied in manufacturing and process industries. These systems provide structured monitoring and advanced control algorithms to maintain stable environmental conditions. By calculating optimal control actions under defined constraints, MPC-based approaches improve energy efficiency and climate stability. This makes PLC/SCADA architectures reliable and suitable for professional greenhouse management within an Industry 4.0 framework .****

# Stakeholder Management

The effective implementation of a smart greenhouse automation and control system, that is focused on environmental monitoring, automated irrigation, and data-driven crop management, depends on structured and active stakeholder engagement. Clearly identifying the stakeholders involved, understanding their level of interest and decision-making power, and ensuring their objectives are aligned with the project’s goals are essential for overcoming technical, operational, financial, and regulatory constraints.
Strong coordination among stakeholders supports system reliability, secure cloud connectivity, and sustainable resource management while ensuring compliance with agricultural standards. Involving end users such as farmers and greenhouse operators ensures the solution addresses practical field requirements, whereas collaboration with technical experts, institutional authorities, and research partners such as the Technical University of Moldova enhances system validation, innovation capacity, and long-term scalability.**

## Stakeholder Identification and Categorization

**

### Primary Users

**Farmers (Small and Large-scale)** - They are the main users because their crop yield and income depend directly on proper irrigation and climate control and stress monitoring.
**Greenhouse Operators** - They use the system to monitor temperature, humidity, and soil moisture and ensure healthy plant growth.**

### Technical Team

**Automation and Embedded Engineers** - They are responsible for designing and programming the control logic, integrating sensors and actuators, and ensuring reliable real-time operation of the greenhouse system. They maintain system stability and guarantee proper execution of irrigation, ventilation, and climate control processes.
**Software and IoT Engineers** - They develop the cloud connectivity, data dashboards, remote monitoring features, and user interfaces. They ensure secure data transmission, system configuration, and efficient interaction between the greenhouse and cloud platforms.**

### Government and Institutions

**Ministry of Agriculture** - Supports agricultural modernization and may influence large-scale adoption.
**Agricultural Agencies** - Ensure compliance with farming and environmental regulations.
**Technical University of Moldova** - Contributes through research, testing, and validation of the system.**

### Business and Comercial Partners

**Hardware and Sensor Suppliers** - Provide PLCs, sensors, and control equipment.
**Cloud Service Providers** - They offer data storage and remote monitoring infrastructure.
**Investors**  - Support funding and system expansion.**

### Society

**Consumers** - They benefit from improved food safety, consistent product quality, and environmentally responsible production methods.

**

## Stakeholder Map

A stakeholder map is a visual tool used to categorize and prioritize stakeholders based on their level of power and interest in a project. It helps project teams understand which stakeholders require close collaboration and which require minimal engagement. Stakeholder mapping is part of the stakeholder analysis process. And of course, stakeholder analysis is often part of the stakeholder planning, stakeholder assessment, stakeholder engagement, and stakeholder management processes [1]. By structuring stakeholders into clear categories, organizations can allocate communication efforts efficiently and reduce project risks.
The **Manage Closely** quadrant includes stakeholders with high power and high interest. These actors directly influence project decisions and are strongly affected by project outcomes. In this project, farmers, greenhouse operators, technical engineers and investors fall into this category because they either depend on the system’s performance or have decision-making authority over its development and funding. Continuous communication and active involvement are essential for this group.
The **Keep Satisfied** quadrant contains stakeholders with high power but lower day-to-day interest. These stakeholders can significantly influence regulatory approval, infrastructure access, or long-term scalability, but they are not directly involved in system operation. For this project, the Ministry of Agriculture, agricultural agencies, cloud providers, and hardware suppliers are placed in this quadrant. They require regular updates and strategic alignment to ensure ongoing support.
The **Keep Informed** quadrant includes stakeholders with high interest but limited power. These actors care about the project’s outcomes but do not control major decisions. The Technical University of Moldova is positioned here due to its role in research validation and academic support. Maintaining transparent communication with this group ensures knowledge exchange and institutional collaboration.
The **Monitor** quadrant represents stakeholders with low power and low direct interest in the project’s technical implementation. Consumers are included in this category because, although they benefit indirectly from improved food quality and sustainability, they do not influence operational or strategic decisions. Periodic observation of their expectations is sufficient, without intensive engagement.
****

## Stakeholder Description

The stakeholder table provides a structured overview of all relevant actors involved in or affected by the greenhouse automation system, clearly defining their roles, reasons for inclusion, and levels of interest and influence. Primary users and the technical team demonstrate both high interest and high influence, as system reliability directly impacts agricultural productivity and operational performance. Government and institutions hold significant influence due to their regulatory authority and ability to support large-scale adoption through policy and funding mechanisms. Business and commercial partners contribute essential infrastructure, financial resources, and technological components necessary for implementation and scalability. Consumers are identified as indirect stakeholders with low influence, benefiting from improved food quality and sustainability outcomes without directly affecting project decisions.
| StakeholderGroup | Stakeholder | Role in Project | Reason for Inclusion | Level of Interest | Level of Influence |
| --- | --- | --- | --- | --- | --- |
| Primary Users | Farmers (Small & Large-scale) | Use the system for irrigation, climate control, and crop stress monitoring | Their productivity and income depend directly on system performance | High | High |
| Primary Users | Greenhouse Operators | Monitor environmental parameters and manage daily operations | They are responsible for daily system operation and crop management | High | High |
| Technical Team | Automation & Embedded Engineers | Design control logic, integrate sensors/actuators, ensure real-time reliability | They develop and maintain the core control functionality of the system | High | High |
| Technical Team | Software & IoT Engineers | Develop cloud connectivity, dashboards, and remote monitoring | They enable data transmission, visualization, and system configuration | High | High |
| Government and Institutions | Ministry of Agriculture | Supports agricultural modernization and funding initiatives | Influences policy, funding programs, and large-scale adoption | Medium | High |
| Government and Institutions | Agricultural Agencies | Ensure compliance with farming and environmental regulations | Regulate agricultural practices and environmental standards | Medium | High |
| Government and Institutions | Technical University of Moldova | Provides research validation, testing, and technical expertise | Contributes scientific validation and technical support | High | Medium |
| Business and Comercial Partners | Hardware & Sensor Suppliers | Provide PLCs, sensors, and control equipment | Supply essential hardware infrastructure | Medium | Medium |
| Business and Comercial Partners | Cloud Service Providers | Provide data storage and remote monitoring infrastructure | Enable scalable data management and remote access | Medium | Medium |
| Business and Comercial Partners | Investors | Provide capital for development and system scaling | Determine financial sustainability and expansion potential | High | High |
| Society | Consumers | Benefit from improved food quality and sustainable production | Indirect beneficiaries of safer and more efficient agriculture | Low | Low |
**

## Stakeholder Mapping Reasoning

The stakeholder mapping rationale clarifies why each actor is positioned within a specific quadrant of the Power-Interest matrix. Primary users and the technical team are placed in the “Manage Closely” category because system performance directly impacts their operations and responsibilities. Government and Institutional bodies and key suppliers are classified under “Keep Satisfied” due to their regulatory authority and infrastructure influence, even though they are not involved in daily activities. Research institutions are kept informed to support validation and innovation, while consumers are monitored as indirect beneficiaries with limited decision-making power.

| Stakeholder | Mapping Position | Justification for Interest | Justification for Influence |
| --- | --- | --- | --- |
| Farmers (Small & Large-scale) | Manage Closely | The system directly affects crop performance, resource efficiency, and overall farm profitability. | Their decision to adopt the technology determines market acceptance and long-term expansion. |
| Greenhouse Operators | Manage Closely | They rely on the system for day-to-day environmental supervision and operational control. | They shape configuration settings and influence how the system is practically implemented. |
| Automation & Embedded Engineers | Manage Closely | They are deeply engaged in system design, hardware integration, and control stability. | Technical decisions made by them define system robustness and reliability. |
| Software & IoT Engineers | Manage Closely | Responsible for digital infrastructure, data visualization, and remote access functionality. | Their work determines scalability, cybersecurity, and system usability. |
| Investors | Manage Closely | Focused on financial performance, growth potential, and long-term sustainability. | Provide capital resources necessary for development and deployment continuity. |
| Ministry of Agriculture | Keep Satisfied | Interested in technological advancement and modernization of the agricultural sector. | Holds authority over national policies, funding schemes, and strategic support. |
| Agricultural Agencies | Keep Satisfied | Concerned with adherence to environmental and agricultural standards. | Possess regulatory power that can impact approval and operational compliance. |
| Hardware & Sensor Suppliers | Keep Satisfied | Involved in providing physical components required for system operation. | Influence project timelines and costs through equipment availability. |
| Cloud Service Providers | Keep Satisfied | Enable secure storage, analytics, and remote accessibility of collected data. | Moderate leverage due to infrastructure dependency and service agreements. |
| Technical University of Moldova | Keep Informed | Engaged through research collaboration and technical validation activities. | Strengthens academic credibility but does not participate in executive decisions. |
| Consumers | Monitor | Benefit indirectly from improved production quality and environmental efficiency. | Minimal direct authority unless public perception significantly affects adoption. |

**Disclaimer:**
This report is based on publicly available research and technical sources. AI tools were used to help organize and summarize the information. The conclusions presented are drawn from these sources and should be viewed in the context of ongoing developments in agricultural automation.
**Bibliography**
ref1 [1]“Our Current Path: Where We’re Headed in the Absence of Deliberate Transformation,” *Foodsecurityleadership.org*, 2025. https://www.foodsecurityleadership.org/analysis-post/our-current-path-where-were-headed-in-the-absence-of-deliberate-transformation Accessed 21 Feb. 2026.
ref2[2]“How to Reduce Water Consumption in Your Greenhouse - Hydroponic Systems.” *Hydroponic Systems*, 9 Sept. 2024, hydroponicsystems.eu/how-to-reduce-water-consumption-in-your-greenhouse/. Accessed 21 Feb. 2026.
ref3[3]Cooper, Julian, et al. “Current Methods and Future Needs for Visible and Non-Visible Detection of Plant Stress Responses.” *Frontiers in Plant Science*, vol. 16, 29 Sept. 2025, https://doi.org/10.3389/fpls.2025.1585413. Accessed 22 Feb. 2026.
ref4[4]Vasile, Botnari, and Cotenco Eugenia. “Seceta-Factor de Risc Sporit Pentru Agricultura Convențională.” *Idsi.md*, vol. Ediția 8, 2024, pp. 496–502, ibn.idsi.md/vizualizare_articol/213539. Accessed 22 Feb. 2026.
ref5[5]“Climate change: tomatoes on the brink of an unprecedented migration,” *Tomato News*, 2024. https://tomatonews.com/climate-change-tomatoes-on-the-brink-of-an-unprecedented-migration/  Accessed 22 Feb. 2026.
ref6[6] “Moldova - Agriculture.” *Www.trade.gov*, 8 Mar. 2024, www.trade.gov/country-commercial-guides/moldova-agriculture.  Accessed 22 Feb. 2026.
ref7[7]“An Agricultural Country without Its Tomatoes: Moldova Remains Dependent on Imports.” *News-Pravda.com*, 2026, md.news-pravda.com/en/world/2026/02/10/88535.html. Accessed 22 Feb. 2026.
ref8[8] Simo, Attila, et al. “Smart Agriculture: IoT-Based Greenhouse Monitoring System.” *INTERNATIONAL JOURNAL of COMPUTERS COMMUNICATIONS & CONTROL*, vol. 17, no. 6, 14 Dec. 2022, https://doi.org/10.15837/ijccc.2022.6.5039.  Accessed 22 Feb. 2026.
ref9[9] Li, Haixia, et al. “Towards Automated Greenhouse: A State of the Art Review on Greenhouse Monitoring Methods and Technologies Based on Internet of Things.” *Computers and Electronics in Agriculture*, vol. 191, Dec. 2021, p. 106558, https://doi.org/10.1016/j.compag.2021.106558.  Accessed 22 Feb. 2026. 
ref10[10] Sagheer, Alaa, et al. “A Cloud-Based IoT Platform for Precision Control of Soilless Greenhouse Cultivation.” *Sensors*, vol. 21, no. 1, 31 Dec. 2020, p. 223, https://doi.org/10.3390/s21010223.
ref11[11] Bersani, Chiara, et al. “Internet of Things Approaches for Monitoring and Control of Smart Greenhouses in Industry 4.0.” *Energies*, vol. 15, no. 10, 23 May 2022, p. 3834, https://doi.org/10.3390/en15103834.
