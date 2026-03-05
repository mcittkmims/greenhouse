# 04 - GMS -WP2.1 Technology Research

> Source: http://confluence.microlab.club/rest/api/content/42634000 | Version: 26

****

## 1.General Research

Agriculture represents one of the fundamental pillars of the global economy, being directly linked to food security, employment, and rural development. Global food systems face increasing pressure from population growth, climate change, and competition for natural resources, requiring sustainable intensification and improved resource efficiency . As food demand rises, agriculture must increase productivity while preserving environmental sustainability and resilience.
In the Republic of Moldova, agriculture holds strategic economic importance. The sector contributes significantly to GDP, employment, and export performance, while remaining highly vulnerable to climate variability and extreme weather conditions . Temperature fluctuations and irregular precipitation patterns directly affect crop yields and economic stability, making modernization and technological integration essential for national development.
The evolution of agriculture reflects a progressive transition from labor-intensive practices to technologically driven ecosystems. Agriculture 1.0 represents the traditional agricultural era, characterized by dependence on human labor, basic tools, and natural resources, which limited productivity and efficiency. With the advancement of digital technologies, agriculture has evolved into Agriculture 4.0, integrating innovations such as the Internet of Things (IoT), Big Data, Artificial Intelligence, Cloud Computing, and Remote Sensing . This transformation significantly enhances operational efficiency, resource management, and production optimization. The development of smart farming ecosystems can be traced through distinct phases: precision agriculture and GPS-guided machinery in the early 2000s; the integration of IoT and mobile technologies during the 2010s; the emergence of integrated farm management systems between 2016 and 2020; and recent advancements in robotics, drone technologies, and edge computing. Agriculture 4.0 promotes sustainable and environmentally friendly practices by minimizing water, fertilizer, and pesticide usage while increasing productivity. 
Despite technological progress in industrial sectors, traditional greenhouse management remains largely manual and reactive. Conventional greenhouses operate in partially uncontrolled environments where temperature, humidity, and irrigation are adjusted manually, often leading to inconsistent climate regulation. Such conditions contribute to plant diseases, inefficient water use, soil degradation, and reduced crop production .
Manual supervision requires continuous labor presence and does not allow preventive management. Without continuous environmental monitoring, greenhouse operators react only after visible plant stress occurs. This reactive approach results in excessive water and energy consumption and inefficient fertilizer application. Furthermore, the absence of systematic historical data collection prevents farmers from identifying optimal growth patterns or anticipating environmental deviations, limiting scalability and long-term sustainability .
The integration of Internet of Things (IoT) technologies enables distributed sensor networks capable of continuously collecting environmental data such as temperature, humidity, soil moisture, and CO₂ concentration . A layered sensor component stack supports modular interaction between hardware and software layers, enabling scalable and maintainable IoT systems for applications such as greenhouse monitoring . These systems generate real-time monitoring infrastructures that detect environmental deviations immediately. Instead of relying on periodic inspections, smart agriculture introduces continuous data streams, transforming greenhouses into intelligent ecosystems. Data-driven agriculture represents a paradigm shift in which decisions are based on measured variables rather than estimation. IoT platforms enable predictive control strategies, allowing proactive responses to stress factors and optimized resource allocation [, ].
Programmable Logic Controllers (PLCs) are widely recognized for their industrial reliability and deterministic real-time control capabilities. Within Industry 4.0 environments, PLCs function as robust edge devices capable of executing automation logic with minimal latency and high operational stability . Unlike microcontrollers used in small-scale prototypes, PLC systems are designed for continuous 24/7 operation in industrial conditions.
PLCs provide deterministic processing, ensuring that environmental control actions, such as activating ventilation or irrigation systems are executed within predictable time intervals. This capability is essential in greenhouse environments, where delayed responses to temperature or humidity fluctuations can lead to plant stress and yield reduction. Their durability, fault tolerance, and compatibility with industrial communication protocols make them particularly suitable for greenhouse automation systems .
Modern greenhouse management systems extend beyond local automation by integrating sensor-to-cloud architectures. Environmental data collected by sensors and processed locally can be transmitted to cloud platforms for storage, visualization, and advanced analytics . By integrating IoT communication technologies with cloud infrastructure, greenhouse systems enable continuous monitoring, alarm notifications, and data-driven decision-making. 
Smart greenhouse systems significantly improve resource optimization by aligning environmental control precisely with crop requirements. Automated irrigation reduces water waste, while controlled ventilation and heating systems minimize energy consumption . These improvements lead to increased yield consistency and enhanced crop quality.
Continuous monitoring of stress factors enables predictive management strategies that prevent plant damage before it occurs. The adoption of automated, data-driven greenhouse management strengthens sustainability, increases competitiveness, and supports agricultural resilience in climate-sensitive regions ****

## 2. Disciplines Research on Proposed Technology

### 2.1 IoT Device Domain and Edge Computing

****

#### Sensors

The distributed sensor network continuously monitors environmental parameters critical to crop development, interfacing with the *PLC* through standardized communication protocols following established layered *IoT* architectures .
**Figure 2.1**: Greenhouse climate control system ******

##### Temperature Monitoring

In terms of temperature monitoring, using the *DS18B20 Digital Temperature Probes* is the right choice, due to its advantageous properties.
**Figure 2.2**: DS18B20 Digital Temperature Probe
Some of its properties are:
- *Range:* -55°C to +125°C with ±0.5°C accuracy, in case of temperature from -10°C to +85°C
- *Interface:* 1-Wire protocol enabling multi-drop bus configuration
- *Construction:* Waterproof stainless steel housing
- *Deployment: *Ambient air temperature at canopy level, soil substrate temperature, multi-zone profiling
- *Relevance:* Moldova’s continental climate exhibits temperature extremes from -15°C, during winter, up to +35°C, during summer time 
******

##### Soil Moisture and Temperature

As for the soil, the *SHT-10 Soil Moisture and Temperature Sensor *is another great sensor that should be put to use.

**Figure 2.3**: SHT-10 Soil Moisture and Temperature Sensor
SHT-10 Soil Moisture and Temperature Sensor characteristics:
- *Temperature: *-40°C to +123.8°C, of ±0.4°C accuracy
- *Moisture: *0-100% RH, around ±3% accuracy
- *Interface:* Digital *I²C* communication
- *Housing: *Sintered metal mesh with anti-corrosion coating
- *Application:* Root zone monitoring for precision irrigation control
******

##### Atmospheric Humidity Sensors

Digital capacitive sensors, such as *DHT22*, measure air moisture at canopy level - critical for disease prevention in Moldova's variable humidity conditions, providing 0-100% RH measurement through *I²C *interfaces.******

##### CO₂ Concentration Monitoring

The monitoring of the concentration of carbon dioxide enables photosynthesis optimization, particularly valuable given that controlled CO₂ enrichment, of around 800-1200 ppm, can increase yields by 20-30% compared to ambient atmospheric levels, which sit at around ~420 ppm . Non-dispersive infrared, known as *NDIR*, sensors such as the *MH-Z19B* or *Senseair K-series* measure CO₂ through infrared absorption, offering serial *UART* or *Modbus RTU* output compatible with the *PLC* architecture.******

##### Light Intensity Sensing

Addressing Moldova's pronounced seasonal photoperiod variation, approximately 16 hours daylight in June versus 8 hours in December . *Photosynthetically Active Radiation,* known as *PAR*, sensors or digital lux meters, like *BH1750,* enable both supplemental lighting control during winter months and shade deployment during summer peak radiation periods. As an example, the C-Fenix greenhouse system architecture,* Figure 2.1*, illustrates comprehensive sensor integration including solar radiation, temperature/humidity, and rain detection sensors feeding into centralized control systems .************

#### Actuator S ystems

Generally speaking, actuators transform *PLC* control signals into physical environmental modifications, in our case, executing autonomous climate management decisions. 
**Figure 2.4**: Layered architecture within a Greenhouse Management System 
The actuator infrastructure addresses the four primary greenhouse control domains: *thermal regulation, humidity management, ventilation, and irrigation*.**

##### Ventilation Systems

Exhaust fans and circulation fans maintain optimal atmospheric conditions through forced air exchange and internal mixing. Axial flow exhaust fans , of 0.5-1.5 HP, and powered via 230V AC, create negative pressure drawing outdoor air through intake vents, providing primary cooling during Moldova's summer periods where greenhouse internal temperatures can exceed 40°C without active ventilation . Relay interfaces controlled by *PLC's* digital outputs enable on/off or variable-speed operation through Variable Frequency Drives, known as *VFDs.* Horizontal circulation fans prevent thermal stratification and humidity pockets that promote fungal diseases, operating continuously or in response to detected gradients.**

##### Heating Systems

Electric resistance heating, such as tubular heaters, forced-air units, maintains minimum temperatures during Moldova's November-March cold season. *PLC-*controlled relays or Solid State Relays, known as *SSRs*, implement Proportional Integral Derivative, known as *PID*, algorithms maintaining stable temperatures, of ±0.5°C, while minimizing energy expenditure. Larger installations may employ hot water systems with gas or biomass boilers, where the *PLC* controls motorized mixing valves and circulation pumps.**

##### Irrigation Actuators

Solenoid valves enable zone-based water delivery controlled by soil moisture thresholds. The *Portenta Machine Control'*s 24V outputs directly drive low-power solenoid coils, while relay modules interface with higher-power valves. Electric pumps, of 0.5-1.5 HP centrifugal or diaphragm types, generate system pressure, controlled through contactors or motor starters with *PLC* interlocks preventing dry-running conditions.**

##### Humidity and Light Modulation

Ultrasonic humidifiers inject fine mist during Moldova's dry summer periods, when relative humidity is often <40%, while exhaust ventilation provides dehumidification. Motorized shade screens, made out of polyethylene or aluminized fabrics blocking 30-70% solar radiation, deploy via tubular motors with limit-switch feedback. Supplemental LED grow lights extend the photoperiod during winter, controlled through relay switching or 0-10V dimming protocols.****

#### Hardware Architecture

**

##### Arduino Portenta Machine Control

The *Arduino Portenta Machine Control *serves as the system's industrial *PLC*, providing robust I/O interfacing and deterministic control execution. 

**Figure 2.5**: Arduino Portenta Machine Control
Built on the dual-core *STM32H747* microcontroller, with a Cortex-M7 @ 480 MHz and with a Cortex-M4 @ 240 MHz, the platform executes real-time control loops on one core while managing communication and logging on the other . This parallel processing architecture ensures actuator response latencies under 100 milliseconds - critical in greenhouse environments where rapid temperature or humidity changes threaten crop health .
Therefore, some of its key I/O capabilities that are necessary for the scenario of a Greenhouse Management System include:
- 12 isolated digital inputs/outputs, of 24V DC, with 2A per output
- 8 analog inputs, range of 0-10V/4-20mA, which is configurable
- 8 analog outputs for proportional control
- 3 power relays, of 250V AC @ 3A, for direct AC load switching
- 8 RTD/thermocouple inputs, such as Pt100, Type K
- Communication done through: *Ethernet*, via Modbus TCP, OPC-UA, *RS-485,* via Modbus RTU, or *CAN bus*

The 24V DC operating voltage aligns with industrial automation standards, balancing electrical safety with current-carrying capacity for distributed sensor networks.**

##### Power Distribution and Protection

The *DIN-rail* mounted 24V DC switching power supply, 5-10A, converts Moldova's 230V AC grid voltage. Moreover, the IP65-rated enclosures provide environmental protection. Uninterruptible Power Supply, known as *UPS*, backup, of 500-1000VA, maintains operation during grid instabilities.**

##### Human-Machine Interface

In terms of *HMI*, options include industrial touchscreen panels, such as a 7-10", IP65 front panel communicating via *Modbus TCP*, or embedded Raspberry Pi systems with custom web-based dashboards. The *HMI* displays real-time sensor values, actuator states, alarm conditions, and historical trends while providing touchscreen controls for setpoint adjustments and manual overrides. The architecture diagram, *Figure 2.4*,  shows this HMI placement at the Application Layer, interfacing with the Controller Layer through internet/local network connections .****

#### Edge Computing Architecture

The *edge computing* transforms the system from reactive monitoring to proactive environmental management by processing sensor data and executing control decisions locally within the PLC rather than depending solely on cloud connectivity .**

##### Real-Time Control Implementation

The *Portenta Machine Control*'s dual-core architecture executes multiple parallel control loops: the Cortex-M7 core, which runs time-critical *PID* temperature control at 10 Hz update rates, while the Cortex-M4 manages data logging, cloud communication, and *HMI* updates. Temperature control implements three-term *PID* algorithms – proportional response to current deviation, integral correction for sustained offsets, derivative anticipation of trends-maintaining setpoint stability within ±0.5°C . Humidity and CO₂ control employ hysteresis-based switching where actuators activate at upper thresholds and deactivate at lower bands, preventing rapid cycling that increases electrical consumption and mechanical wear. The *irrigation control* monitors soil moisture sensors against crop-specific thresholds, typically 40-60% volumetric water content, triggering valve activation with maximum duration and minimum interval safeguards preventing overwatering from sensor failures. **

##### Local Data Storage and Alarm Generation

The *Portenta*'s 16 MB Flash memory implements circular buffer storage for 7-30 days of sensor history, depending on sampling frequency, ensuring operational continuity during internet outages. Data logging captures timestamp, sensor readings, actuator states, and alarm conditions in compressed time-series format optimized for storage efficiency.
Autonomous alarm generation executes locally without cloud dependency. Therefore, the sensor validation algorithms detect out-of-range measurements, stale data, and implausible rate-of-change conditions indicating failures. Critical threshold alarms trigger when temperatures fall below 10°C or exceed 35°C, the typical crop tolerance limits, activating maximum heating/cooling while alerting operators through local audible buzzers, LED indicators, or SMS notifications.**

##### Redundancy and Graceful Degradation

Sensor redundancy, such as dual temperature sensors with median value selection, maintains reliable measurements during individual sensor failures. When cloud connectivity is lost, the edge device continues indefinite autonomous operation using last-known setpoints, storing data locally and maintaining full local *HMI* functionality. Physical emergency switches on the electrical enclosure enable manual actuator control bypassing all automation – essential operator fallback during complete system failures .
The edge-cloud hybrid model periodically uploads aggregated statistical summaries, 5-15 minute intervals with min/max/average values, to cloud platforms for long-term trend analysis and multi-season optimization while maintaining local autonomy for real-time control – balancing operational reliability with data-driven improvement .

### 2.2 IoT Communication Technologies

Communication protocols form the nervous system connecting sensors, actuators, the *PLC*, *HMI* displays, and cloud platforms into an integrated automation infrastructure. The system makes use of multiple protocols optimized for different communication requirements, from deterministic real-time *Fieldbus* for sensor networks, to industrial *Ethernet* for *HMI* connectivity, and *Internet* protocols for cloud integration .****

#### Industrial Communication Protocols

**

##### Modbus RTU - Serial Communication

The *Modbus RTU* operates over *RS-485* physical layer, providing multi-drop serial communication suitable for distributed sensor networks across greenhouse zones. The protocol employs* master-slave *architecture where the* Portenta Machine Control, *the* master *in this case, polls up to 247 sensor devices, the *slaves*, on a single bus, requesting data or issuing commands through standardized function codes. Consequently, the *RS-485's* differential signaling provides noise immunity, which is critical in agricultural environments with long cable runs, which can reach up to 1,200 meters, and electromagnetic interference from various motor loads .**

###### PLC ↔ Sensors Communication

Given that the CO₂ sensors, weather stations, and remote I/O modules commonly implement *Modbus RTU* at 9600-115200 baud rates. Subsequently, the *PLC* polls each device sequentially, reading register values containing sensor measurements or status information. Based on this, the *RS-485's* half-duplex operation requires careful timing management – the *PLC* must wait for slave response completion before initiating subsequent transactions, with typical polling cycles achieving 10-50 Hz update rates depending on slave count and baud rate.**

##### Modbus TCP/IP - Industrial Ethernet

Next, the *Modbus TCP* encapsulates the *Modbus* protocol within standard *TCP/IP* packets, enabling communication over *Ethernet* networks. Therefore, this approach leverages existing network infrastructure while maintaining the *Modbus* command compatibility. Unlike *RTU's master-slave* polling, the *Modbus TCP* supports multiple simultaneous connections through *TCP's* session management, such as multiple *HMI* panels or even the cloud gateways can read *PLC* data concurrently without polling conflicts .**

###### PLC ↔ HMI Communication

As an example, the *Portenta Machine Control's* *Ethernet* interface serves *Modbus TCP* requests from local touchscreen *HMIs* or even from embedded Raspberry Pi dashboards. The *HMI* establishes a *TCP* connection, which is typically on port 502, and issues *Modbus* read requests for sensor values, actuator states, and alarm registers at 1-2 Hz refresh rates. Meanwhile, write operations enable setpoint modifications and manual overrides, with the *PLC* validating requests against configured limits before execution. This *Ethernet-based* approach appears in the architecture diagram,* Figure 2.4*, showing bidirectional communication between the *Controller Layer, *the* PLC,* and the *Application Layer, *composed of the control panel, web/mobile applications .******

##### OPC Unified Architecture

In continuity, the *OPC-UA* provides platform-independent industrial communication with advanced features including data modeling, security, and historical data access – positioning it as the emerging standard for the *Industry 4.0* implementations. Unlike *Modbus's* simple register-based model, *OPC-UA* exposes hierarchical information models representing complex device structures with typed variables, methods, and events .**

###### PLC ↔ Cloud Communication

For instance, the *OPC-UA* servers embedded in the *Portenta Machine Control,* through compatible software stacks, publish the greenhouse data models accessible to cloud platforms, Supervisory Control and Data Acquisition, known as *SCADA*, systems, or even analytics applications. As an advantage, the protocol supports both polling, *client-requested reads,* and subscription mechanisms, such as *server-pushed updates* on data changes, resulting in the optimization of bandwidth for cloud connectivity. Moreover, the built-in security features including *X.509* certificates, encryption, and user authentication align with the defined cybersecurity requirements for internet-connected agricultural systems.**

##### MQTT - Message Queuing Telemetry Transport

Last but not least, the *MQTT* implements lightweight publish-subscribe messaging optimized for constrained devices and unreliable networks – characteristics matching the rural Moldova's internet infrastructure. The protocol employs a *broker architecture* where the *PLC, *the client, publishes sensor data to topics, like *greenhouse/zone1/temperature*, while cloud applications subscribe to receive updates. Therefore, via *MQTT's* quality-of-service levels, QoS 0: at-most-once, QoS 1: at-least-once, QoS 2: exactly-once, we enable resilience against packet loss and connection interruptions .**

###### PLC ↔ Cloud Communication

As a scenario, the *Portenta Machine Control* connects to *MQTT* brokers, such as AWS IoT Core, Azure IoT Hub, or even to local Mosquitto instances, over *TLS-encrypted TCP* connections, usually on port 8883. Then, the sensor readings are published at configured intervals, of around 1-60 seconds, with the broker forwarding messages to subscribed cloud analytics platforms, mobile applications, and multi-site dashboards. During connectivity loss, the *PLC* buffers messages locally, republishing accumulated data when connection resumes – maintaining data continuity despite the potential network interruptions.****

#### Physical Layer Communication

**

##### Ethernet Communication

*Gigabit Ethernet* provides the physical backbone for local network communication, connecting the *PLC* to *HMI* panels, local computers, and internet gateways. As the standard *Cat5e/Cat6* cabling supports 100-meter segments without repeaters, this is adequate for typical greenhouse dimensions, of around 50-200 meter lengths. Meanwhile, the *managed Ethernet switches* enable *VLAN* segmentation isolating greenhouse automation traffic from general facility networks – improving security and quality-of-service for time-sensitive control messages .
**Figure 2.6**: A layered IoT architecture for greenhouse monitoring and remote control 
The layered architecture diagram,* Figure 2.6*, depicts this *Ethernet* connectivity through the *Internet Gateway* and *Access Point *components bridging local microcontrollers to cloud-based backend services.******

##### Wi-Fi Gateway Integration

Wi-Fi access points extend network coverage to mobile devices, smartphones, tablets, used by operators for remote monitoring within greenhouse premises. Industrial-grade *Wi-Fi*, *IEEE 802.11ac/ax* with external antennas, penetrates greenhouse structures - metal framing and moisture can attenuate signals requiring strategic AP placement for complete coverage . However, critical control paths, such as *PLC-to-sensors *or *PLC-to-actuators*, utilize wired connections avoiding wireless reliability concerns.

#### Communication Security

**

##### Data Encryption

Communication between greenhouse controllers and cloud platforms implements *Transport Layer Security,* such as *TLS 1.2* or higher, encrypting all transmitted data. *MQTT* over *TLS*, *HTTPS* *REST* *APIs*, and* OPC-UA *security modes provide end-to-end encryption preventing eavesdropping on sensor data or command injection attacks. Research on *IoT* agricultural security identifies unencrypted communication as the primary vulnerability enabling unauthorized greenhouse access .**

##### Authentication Mechanisms

The *X.509* certificate-based authentication validates device identity, ensuring only authorized *PLCs* connect to cloud services. Certificate pinning prevents man-in-the-middle attacks by verifying server certificates against known signatures. Local *HMI* access implements role-based authentication - administrative users configure setpoints and system parameters while operator accounts access monitoring and manual overrides only. This multi-level access control follows best practices documented in *IoT* security frameworks for agricultural applications.

### 2.3 Database, Data Analysis and Cloud Computing (Back End)

The cloud backend transforms raw sensor streams into actionable agricultural intelligence, providing long-term storage, historical analysis, multi-site aggregation, and predictive modeling capabilities beyond the computational scope of edge devices .****

#### Database Architecture

**

##### Cloud-Based Storage

Usage of time-series databases optimized for *IoT* telemetry, like InfluxDB, TimescaleDB, AWS Timestream, which store greenhouse environmental data. These specialized databases index measurements by timestamp, enabling efficient queries across temporal ranges, for instance "*retrieve all temperature readings from Zone 2 during July 2025*", while compressing repetitive data reducing storage costs. Unlike traditional relational databases, time-series systems handle millions of measurements per day with minimal write latency and optimized aggregation queries .**

##### Environmental Logs and Historical Data

The continuous logging captures:
- *Sensor measurements: *Temperature, humidity, soil moisture, CO₂, light intensity at 10-60 second intervals
- *Actuator states:* Fan speeds, valve positions, heating/cooling duty cycles
- *Alarm events: *Threshold violations, sensor failures, communication errors with timestamps
- *Control actions: *Setpoint changes, manual overrides, automated responses

Data retention policies balance storage costs against analytical value – high-resolution data, 10-second samples, retained for 30-90 days for detailed incident analysis, can be downsampled to 5-15 minute averages for long-term storage, multi-year retention, which enables seasonal trend comparison.**

##### Crop Correlation Data

Advanced implementations link environmental logs with crop management records, like planting dates, variety information, harvest yields, quality metrics, enabling correlation analysis between growing conditions and outcomes.

#### Data Analysis Capabilities

**

##### Trend Detection and Threshold Analysis

Cloud analytics platforms process historical data identifying long-term trends invisible in real-time monitoring. Statistical algorithms detect gradual sensor drift, for example temperature sensor losing calibration over months, seasonal patterns, like heating energy consumption correlating with outside temperature, and cultivation cycle progression, as transpiration rates increase during vegetative growth phases.
Threshold violation analysis tracks alarm frequency and duration, highlighting chronic control issues - for example, discovering that a zone consistently exceeds upper humidity limits during morning hours suggests insufficient circulation or ventilation capacity requiring actuator upgrades or control parameter adjustments.**

##### Crop-Environment Correlation

Machine learning models trained on multi-season datasets identify non-obvious relationships between environmental parameters and crop outcomes. Regression analysis might reveal that subtle light intensity variations during flowering stages significantly impact fruit set percentages, or that overnight temperature fluctuations correlate with disease incidence - insights guiding refined control strategies . ******

##### Predictive Modeling

Time-series forecasting algorithms predict future conditions enabling proactive management. Examples include:
- *Heating demand prediction: *Machine learning models trained on historical heating system runtime, outside temperature, wind speed, and solar radiation forecast next-day heating requirements, enabling optimized boiler scheduling and energy procurement
- *Disease risk assessment: *Environmental condition patterns, sustained high humidity, specific temperature ranges, preceding historical disease outbreaks train models that predict infection probability, triggering preventive ventilation or treatment protocols
- *Yield forecasting: *Cumulative environmental exposure during critical growth stages, fruit set, ripening, correlates with final yield, enabling harvest planning and market scheduling 
****

#### Cloud Computing Infrastructure

**

##### Remote Dashboards and Visualization

Web-based dashboards aggregate real-time sensor data, actuator states, and alarm conditions into unified operator interfaces accessible from desktop computers, tablets, or smartphones. Visualization libraries, like Grafana, or even custom React dashboards, render:
- *Real-time gauges:* Current temperature, humidity, CO₂ with color-coded status, such as green: optimal, yellow: marginal, red: critical
- *Time-series charts:* 24-hour or 7-day sensor trends identifying patterns and anomalies
- *Actuator runtime logs: *Bar charts showing daily fan operation hours, irrigation volumes, heating energy consumption
- *Alarm timelines:* Historical alarm occurrence frequency enabling maintenance prioritization
**

##### Multi-Site Monitoring and Benchmarking

The agricultural enterprises operating multiple greenhouse facilities benefit from centralized dashboards aggregating data across locations. Therefore, this comparative visualization enables:
- *Performance benchmarking:* Identifying which facilities achieve highest yields per energy unit, motivating efficiency improvements at underperforming sites
- *Resource allocation:* Directing maintenance resources to greenhouses showing highest actuator failure rates or control instability
- *Best practice dissemination:* Propagating successful control strategies from optimal sites to other facilities
******

##### Scalability and Geographic Distribution

Cloud platforms inherently scale computing and storage resources matching data volume growth – adding greenhouse zones, increasing sampling rates, or expanding multi-site deployments requires no infrastructure changes beyond edge device installation. Geographic distribution through content delivery networks, known as* CDNs*, ensures responsive dashboard access from remote locations, while regional data center deployment complies with data sovereignty requirements if sensitive agricultural data must remain within Moldova's borders .
The cloud backend's computational elasticity enables sophisticated analytics, like complex machine learning model training, multi-year dataset processing, which is impractical on resource-constrained edge devices, while edge-cloud hybrid architecture maintains operational autonomy ensuring greenhouse control continuity independent of internet connectivity – balancing advanced intelligence with critical system reliability .

### 2.4 User Experience / User Interaction Domain (Front End)

The User Experience / User Interaction domain of the proposed IoT-based greenhouse management system ensures that environmental data, control commands, and safety functions are presented in an intuitive and reliable way to both local operators and remote users. A clear separation between sensing, communication, control, and visualization is aligned with layered *IoT* architectures, in which application and user‑interaction components are built on top of generic acquisition and communication stacks rather than dealing with raw signals directly .
In the greenhouse scenario, this concept is applied so that the UI consumes preprocessed and diagnosed environmental data from the service layer, supporting modular evolution of the front end while preserving well‑defined reactions at the embedded controller level .****

#### HMI Interface

**

##### Real-time environmental display

The local *Human-Machine Interface* provides real-time visualization of key environmental parameters such as temperature, humidity, light intensity, soil moisture, and CO₂ concentration, together with the current status of actuators, such as ventilation, irrigation, heating, lighting. In an advanced greenhouse automation project implemented with an *IoT* home‑automation platform, a touchscreen panel is used on-site to display current sensor values and system state for each greenhouse sector, allowing the operator to supervise the installation even in offline mode . By mapping the UI to data exposed by the service layer of the sensor software component stack, the *HMI* can present conditioned and validated measurements, while hiding low-level hardware details .**

##### Setpoint configuration

Moreover, the *HMI* allows operators to configure and adjust setpoints for process variables such as temperature, relative humidity, soil moisture thresholds, and lighting periods in the proposed greenhouse management system. In an advanced, greenhouse automation project implemented on top of an *IoT* home‑automation platform, local touchscreen *HMIs* are used to define operating scenarios and target values that are then executed autonomously by the underlying automation logic, enabling thermostat‑like behaviors and timed irrigation or lighting cycles. In related* IoT-based *greenhouse monitoring work, multiple wireless sensor nodes transmit temperature and humidity measurements to a gateway, which forwards the data to a web dashboard and mobile applications that allow users to access real-time and historical environmental data for each device, illustrating how user interfaces can be built on top of a monitoring layer that aggregates and validates sensor data rather than exposing raw signals directly .**

##### Alarm notifications

Diagnostic and alarm information is presented in dedicated *HMI* views to ensure that operators can quickly identify abnormal conditions. The layered sensor stack architecture defines threshold, range, plausibility, and* “stall-in-range”* symptoms, together with diagnosis qualification and reaction mechanisms, such as* blocking, derating*, which can be exposed at UI level as categorized alarms with associated severity and status. Alarms such as over‑temperature, communication loss or sensor failure are displayed on the local touchscreen in the above-mentioned greenhouse application, where the operator can see the active faults and check the affected sector before taking action .**

##### Manual override controls

Last but not least, the *HMI* provides manual override functions for critical actuators, like fans, pumps, valves, heaters, shading, with explicit indication of the current operating mode, either automatic or manual, and actuator state. In the same implementation, the local touchscreen allows the greenhouse owner and staff to manually trigger scenarios or directly control devices when needed, while the main control logic still enforces predefined constraints . *IoT* greenhouse prototypes reported in the literature expose similar manual controls via mobile or local interfaces, enabling farmers to directly turn irrigation or ventilation on/off in response to real-time sensor readings [, ]****

#### Web / Mobile Interface

**

##### Remote access

The web and mobile interfaces extend the local *HMI* functionality by enabling remote monitoring and control via cloud connectivity. In the *Agri Smart Greenhouse* monitoring system, measurement nodes send temperature and humidity data to the Internet, where greenhouse managers can observe environmental parameters remotely through a web-based interface and a dedicated mobile dashboard . An advanced greenhouse solution built on top of a commercial *IoT* platform integrates the local automation hardware with a cloud service, allowing the owner to manage the greenhouse via smartphone and monitor plant growth from remote locations, including international business trips .**

##### Data graphs

Historical data visualization is a core feature of the web/mobile UI, supporting analysis of greenhouse performance and optimization of control strategies. In the commercial greenhouse project, *Grafana* is integrated as a monitoring add‑on to present time series charts of sensor values and actuator behavior for all sectors, enabling the operator to study trends and detect deviations in temperature, humidity, and other parameters . The *Agri Smart Greenhouse* system similarly provides real-time mobile dashboards and offers the option to download historical measurement data for further analysis, combining numerical values with visual representations in the app .**
****

##### Multi-site overview

For installations that include several greenhouses or multiple climate sectors, the web interface provides a hierarchical overview of all sites, with the possibility to drill down into each sector. In the commercial solution mentioned above, all greenhouse sectors are visualized through a unified platform where the operator can see the status of each area, including sensor values and door controllers integrated via cloud services . Comparable *IoT* platforms for agriculture support centralized dashboards where multiple locations and devices are monitored and controlled through a single web/mobile application, using standard *IoT* communication protocols and intuitive sector-level visualization .**

##### Alert notifications

The web and mobile interfaces implement alert mechanisms that notify users when critical thresholds are exceeded or when system faults are detected. In the *Agri Smart Greenhouse *system, the use of *Internet* connectivity allows remote monitoring and prediction, and alerts can be generated when environmental parameters deviate from expected ranges, enabling timely corrective actions . The cloud-based mobile application in the commercial greenhouse solution provides real-time notifications based on sensor readings from the greenhouse, so the owner can react immediately to abnormal situations, such as unexpected temperature drops or communication issues, even when away from the site .****

#### Safety Features

**

##### Emergency stop

Safety-related interactions are explicitly supported in the front end to rapidly bring the greenhouse into a safe state in case of malfunction or hazardous conditions. The diagnosis and reaction mechanisms defined in sensor and actuator software component stacks include *“blocking” *and *“derating” *behaviors that can be triggered by severe internal or external diagnoses, such as sensor failures or over‑temperature events [, ]. At UI level, an emergency stop command is exposed on the *HMI* and, optionally, in the remote interface, sending a high‑priority request to the controller to execute the configured safe state, while a physical emergency button remains available as a hardware redundancy, as recommended in embedded and industrial *IoT* controller design .**

##### Alarm acknowledgment

Alarm acknowledgment workflows are used to ensure that operators consciously respond to critical events and that system recovery is controlled. The diagnostic process in layered architectures introduces qualification stages and anti‑bounce counters, distinguishing between transient and confirmed faults; this information is propagated to the rest of the system, including the *HMI* . The user interface therefore allows authorized personnel to acknowledge alarms, record the time and user identity, and reset certain reactions only after the underlying condition has been resolved, following best practices from configuration‑based embedded system development and model‑driven code generation for safety‑relevant applications .**

##### Access control

Access control mechanisms are integrated into the front end to restrict sensitive operations, like setpoint changes, manual overrides, emergency reset, or configuration updates, to authenticated and authorized users. Some *IoT* greenhouse platforms distinguish between administrative and client panels, where administrators have access to system configuration, while regular users are limited to monitoring and high-level scenario control . From a broader *IoT* and embedded systems perspective, secure access and configuration management are supported by structured configuration models, for example,* JSON-based* *metamodels*, and by enforcing role-based permissions at the application layer, reducing the risk of unauthorized manipulation of embedded devices and field actuators .

### 3.5 Cybersecurity

Cybersecurity is a critical cross-cutting concern for *IoT-based* greenhouse systems, as compromised devices or platforms can lead not only to data breaches but also to direct manipulation of environmental conditions. Security must therefore be addressed end‑to‑end, from edge devices and communication protocols to cloud services and user access mechanisms, using layered protection measures that combine encryption, strong authentication, and secure data management in the cloud .****

#### Encrypted communication

Communication between greenhouse nodes, gateways, and cloud platforms should use cryptographic protocols that ensure confidentiality and integrity of sensor and control data.* IoT-based *greenhouse monitoring systems using *MQTT* demonstrate the use of* TLS/SSL* between the gateway and *MQTT* broker to prevent eavesdropping and tampering on public networks . Secure *IoT-cloud* architectures further emphasize standardized transport encryption such as *HTTPS* and *SSL/TLS* as a baseline requirement for data transmission in agricultural *IoT* deployments .****

#### Authentication

Robust authentication mechanisms are required to ensure that only authorized users and devices can access greenhouse resources and issue control commands. A user authentication scheme designed specifically for greenhouse remote monitoring systems shows how tailored protocols for wireless sensor networks and *IoT* can prevent unauthorized access to greenhouse parameters . At a more general level, secure *IoT-cloud* authentication protocols propose lightweight public‑key or *ECC‑based* mechanisms to establish session keys while respecting constrained device capabilities .****

#### Secure cloud storage

Environmental data and configuration parameters stored in cloud platforms must be protected against unauthorized access, modification, and loss. Cloud-based *IoT* platforms for agriculture and smart farming highlight secure data handling practices, including access control and privacy-preserving mechanisms for long-term storage of sensor data and control logs . Best-practice guidelines for securing *IoT* in agriculture recommend combining secure storage with continuous monitoring and proper identity and access management, so that only permitted users and services can retrieve or modify greenhouse data in the cloud .

### 3.6 Sustainability

Sustainability is a core design objective of the proposed* IoT-based* greenhouse system, aiming to use water and energy more efficiently while lowering overall environmental impact. Smart control strategies based on real-time sensing and data-driven optimization enable resource-efficient crop production and contribute to more sustainable agricultural practices .​****

#### Water optimization

*IoT-based *smart greenhouses can significantly reduce water consumption by using automated irrigation controlled from soil moisture and environmental sensors. Experimental smart greenhouse implementations show that sensor-driven irrigation and precise scheduling maintain crop growth while minimizing unnecessary watering, improving water-use efficiency compared to manual or time-based irrigation .​****

#### Energy efficiency

Integrating monitoring and automatic control of heating, ventilation, and lighting allows the greenhouse to maintain plant comfort with reduced energy input. Studies on smart greenhouse construction and control report that adaptive algorithms, using feedback from temperature and climate sensors, optimize the operation of fans, pumps, and heating elements, leading to lower energy consumption and more efficient climate management .​****

#### Reduced carbon footprint

Improved water and energy efficiency directly contribute to a reduced carbon footprint, as less energy is required for pumping, heating, and cooling, and fewer resources are wasted. In broader *IoT* and green-technology research, *IoT-based* sensing and control are identified as enablers for reducing greenhouse gas emissions by optimizing resource use and enabling low-power, event-driven operation of embedded systems .****

## 4. Comparative Analysis

### 4.1 Overview of Existing Agricultural Automation Solutions

The development of greenhouse automation systems has followed diverse technological trajectories, ranging from low-cost microcontroller prototypes to industrial-grade control platforms and cloud-based smart farming ecosystems. This section examines representative solutions from three principal categories, analyzing their architectures, capabilities, and limitations in the context of modern precision agriculture requirements.******

#### Example 1: Microcontroller-Based Systems - Arduino-Driven Smart Greenhouse for Soilless Cultivation

*Sagheer et al. (2020) *developed a cloud-based *IoT* platform for precision control of soilless greenhouse cultivation using an *Arduino Mega 2560* microcontroller as the central processing unit . The system was deployed in a commercial greenhouse of 2520 m² in Jordan for cucumber cultivation and integrated sensors for air temperature, relative humidity, CO₂ concentration, light intensity, pH, and soil moisture. Sensor data was transmitted via an *ESP8266 Wi-Fi* module to the *ThingSpeak* cloud platform, where environmental measurements were stored, visualized, and compared against predefined thresholds. Actuators including ventilation fans, heating systems, and irrigation pumps were controlled through relay modules connected to the *Arduino* board.
The system demonstrated measurable improvements, including energy savings of approximately 4750 kWh over a cultivation cycle by optimizing ventilation and heating schedules based on real-time sensor feedback . However, the *Arduino Mega 2560* architecture exhibits fundamental limitations for industrial deployment. The *8-bit ATmega2560* microcontroller operates at 16 MHz with 8 KB of *SRAM*, constraining concurrent task management and complex control algorithm execution. The system lacks deterministic real-time processing guarantees, hardware watchdog redundancy, and industrial-grade fault tolerance mechanisms. Multi-site coordination was not addressed, and the platform was designed as a standalone installation without provisions for centralized fleet management.
Similarly, *Huynh et al. (2023) *implemented a smart greenhouse construction and irrigation control system for optimal *Brassica Juncea* development using an *Arduino Uno R3* paired with an *ESP8266 NodeMCU* module . The system employed *SHT10* sensors for soil moisture and temperature monitoring, with data transmitted to a *Laravel-based* web server and an *Android* mobile application for remote visualization. The irrigation control logic utilized threshold-based switching with soil moisture setpoints configured through the mobile interface. While the system achieved improved crop development metrics compared to manual cultivation, the *Arduino Uno R3's* limited computational resources, composed of 32 KB flash memory and 2 KB *SRAM*, restrict scalability beyond single-greenhouse deployments. The absence of industrial communication protocols such as *Modbus* or *OPC-UA* further limits integration with existing agricultural infrastructure.******

#### Example 2: Industrial Automation Systems - PLC and SCADA Architectures in Commercial Agriculture

Industrial automation approaches to greenhouse management leverage *PLCs,* and* Supervisory Control and Data Acquisition*, known as *SCADA,* systems that have proven reliability in manufacturing and process control environments. *Bersani et al. (2022)* conducted a comprehensive review of *IoT* approaches for monitoring and control of smart greenhouses in the context of *Industry 4.0*, documenting the evolution from basic sensor networks toward integrated cyber-physical systems incorporating *Model Predictive Control, known as MPC,* *Artificial Neural Networks, *shortened to* ANN*, fuzzy logic controllers, and *PID* control strategies . The review identified that industrial control techniques such as *MPC* provide approximately 30% electrical energy savings compared to traditional relay control in greenhouse environments, while ensuring consistent temperature profiles through optimal control signal computation under system constraints .
Industrial *PLC* platforms, as discussed by *Sehr et al. (2021)* in the context of *Industry 4.0,* offer deterministic real-time processing, continuous 24/7 operation, and native support for industrial communication protocols including *Modbus RTU/TCP, PROFINET,* and *OPC-UA *. Commercial greenhouse automation platforms based on *Siemens S7-series* or *Allen-Bradley CompactLogix PLCs *implement hierarchical control architectures where field-level *PLCs* manage local actuator loops while *SCADA* systems provide supervisory monitoring and coordination across multiple greenhouse zones. These systems support redundant I/O configurations, hot-swappable modules, and certified safety functions that meet I*EC 61131-3* programming standards. However, traditional industrial automation systems have historically operated as isolated islands of automation with limited cloud connectivity, proprietary communication protocols, and high capital investment requirements that restrict adoption by small and medium agricultural enterprises.
The work of *A. Bragarenco* *and Marusic (2020)* at the *Technical University of Moldova* addressed layered *IoT* architectures for industrial systems, proposing a structured approach to integrating sensor acquisition layers with processing and communication layers through standardized interfaces . Their research on embedded systems development using *JSON metamodels* for code generation further contributes to the methodology of creating maintainable and scalable automation software for agricultural applications . These contributions from the Moldovan academic context are particularly relevant to greenhouse automation efforts in the region, as they address the specific challenges of implementing industrial-grade *IoT* systems in the local technological landscape.******

#### Example 3: Cloud-Based Smart Farming Platforms - IoT Monitoring with Multi-Layer Architectures

*Méndez-Guzmán et al. (2022) *designed an *IoT-based *monitoring system applied to an aeroponics greenhouse, implementing a four-layer architecture comprising the *perception layer*, the sensors, *network layer*, the communication, *fog layer*, the local processing, and *cloud layer*, the remote storage and analytics . The *perception layer* employed *NodeMCU ESP8266 *devices interfaced with *DHT22 *temperature/humidity sensors, soil moisture sensors, and light intensity sensors. The *fog layer* utilized a *Raspberry Pi 4 *for local data aggregation and preprocessing, reducing cloud communication overhead and enabling edge-based alarm generation. Cloud integration was achieved through dual platforms: *ThingSpeak* for time-series data visualization and *Firebase* for real-time database synchronization with mobile applications.
This multi-layer approach demonstrates the advantages of distributed processing architectures for greenhouse monitoring, providing local autonomy through fog computing while maintaining cloud-based analytics for long-term trend analysis and remote access . However, the system relies on consumer-grade hardware, like *NodeMCU*, *Raspberry Pi*, that lacks industrial certifications for electromagnetic compatibility, operating temperature ranges, and vibration resistance. The *fog layer's* single *Raspberry Pi* represents a single point of failure without hardware redundancy. Furthermore, the system focuses primarily on monitoring rather than closed-loop control, with limited actuation capabilities and no implementation of advanced control algorithms such as *MPC* or adaptive *PID* strategies.
Cloud-based smart farming platforms such as AWS *IoT* Core, Microsoft Azure *IoT* Hub, and specialized agricultural platforms like Arable and *CropX* provide scalable infrastructure for multi-site data aggregation, machine learning-based predictive analytics, and mobile-accessible dashboards [, ]. These platforms offer virtually unlimited storage capacity, distributed computing resources, and pre-built analytics services that reduce development complexity. However, pure cloud-dependent architectures introduce latency in control loops, require reliable internet connectivity, and raise data sovereignty concerns for agricultural operations in regions with limited digital infrastructure.

### 4.2 Comparative Analysis Table

The following comparative matrix evaluates the three categories of existing solutions across seven critical performance dimensions relevant to modern greenhouse automation.
| Criterion | Microcontroller-Based Systems (Arduino/ESP) | Industrial Automation (PLC/SCADA) | Cloud-Based Smart Farming Platforms |
| --- | --- | --- | --- |
| Real-Time Monitoring | Basic sensor polling; limited concurrent channels; data sent to cloud for visualization | Deterministic scan cycles (1-10 ms); high-speed I/O acquisition; local HMI displays | Cloud-dependent visualization (network latency); fog computing reduces delay but adds complexity |
| PLC Usage | No PLC ; relies on microcontrollers ( Arduino Mega, NodeMCU ) with limited resources | Native PLC architecture ( IEC 61131-3 ); modular I/O expansion; industrial-grade processors | No PLC ; cloud computing handles data; edge devices only forward data |
| Cloud Integration | ThingSpeak, Blynk, or Firebase via ESP8266 ; limited data retention/analytics | Traditionally limited; modern systems use OPC-UA gateways (requires add'l hardware) | Native cloud architecture; extensive APIs , ML services, and scalable storage |
| Predictive Capability | Minimal; threshold-based alerts only | Advanced; MPC , ANN , fuzzy logic used (up to 30% energy savings) | Strong via cloud ML services ( SageMaker , Azure ML ); requires config/training data |
| Industrial Reliability | Low; consumer-grade; no certifications; susceptible to EMI | High; ruggedized hardware; extended temperature range; certified EMC ; MTBF > 100,000 hours | Variable; depends on edge hardware quality; high cloud SLA (99.9%+) |
| Scalability | Limited; constrained by microcontroller I/O/processing; hardware mods needed to add sensors | High; modular I/O expansion; distributed PLC networks; PROFINET/EtherCAT | Very high; cloud infrastructure scales automatically; minimal hardware provisioning for new sites |
| Multi-Site Management | Not supported; standalone installations | Supported via SCADA but needs dedicated comms & significant config | Natively supported; cloud dashboards aggregate distributed data; hierarchical navigation |

### 4.3 Key Findings and Identified Gaps

The comparative analysis demonstrates that each existing solution category addresses a subset of requirements for modern greenhouse automation while exhibiting significant limitations in the remaining dimensions. Microcontroller-based systems offer low-cost entry points and rapid prototyping capabilities, but their consumer-grade hardware, limited computational resources, and absence of industrial communication protocols make them unsuitable for reliable commercial-scale greenhouse operations [, ]. Industrial *PLC/SCADA* platforms provide the deterministic control, fault tolerance, and continuous operation required for commercial deployment, yet they have traditionally lacked cloud connectivity, remote accessibility, and advanced data analytics functionality . Cloud-based smart farming platforms deliver powerful multi-site aggregation, scalable storage, and machine learning capabilities, but their dependence on network connectivity and consumer-grade edge hardware introduces reliability concerns for mission-critical greenhouse control [, ].
These findings reveal a clear gap in the current landscape: no single existing solution category fully satisfies all seven evaluation criteria simultaneously. An ideal greenhouse automation system would need to combine the industrial reliability and deterministic processing of *PLC* architectures with the cloud connectivity and predictive analytics of smart farming platforms, while maintaining the cost accessibility that enables adoption by small and medium agricultural enterprises. Bridging this gap between industrial-grade control and modern cloud integration represents a key direction for the next generation of greenhouse automation technologies, particularly for climate-sensitive agricultural regions such as the Republic of Moldova where resource efficiency and operational reliability are paramount [, ].****

## 5. Conclusions

The agricultural sector in the Republic of Moldova, while strategically vital to the national economy, faces persistent challenges rooted in climate variability, resource inefficiency, and dependence on manual greenhouse management practices. Traditional greenhouse operations, characterized by reactive environmental control, high labor dependency, and absence of systematic data collection, result in suboptimal crop yields, excessive water and energy consumption, and limited capacity for informed decision-making. These constraints are particularly consequential in Moldova's continental climate, where temperature extremes ranging from -15°C in winter to +35°C in summer demand precise and continuous environmental regulation to sustain protected cultivation.
The integration of Internet of Things technologies and industrial automation fundamentally transforms greenhouse management from a labor-intensive, reactive process into a data-driven, predictive system capable of maintaining optimal growing conditions with minimal human intervention. The proliferation of distributed sensor networks, cloud computing platforms, and advanced control strategies documented in contemporary scientific literature confirms that smart agriculture represents not merely a technological trend but an essential paradigm shift for agricultural sustainability and competitiveness [, ]. Real-time monitoring of temperature, humidity, CO₂ concentration, soil moisture, and light intensity enables continuous environmental awareness, while automated actuation systems translate sensor data into immediate corrective actions that prevent crop stress and resource waste.
The comparative analysis of existing greenhouse automation solutions reveals that microcontroller-based systems, while accessible and cost-effective for educational prototyping, lack the industrial reliability, deterministic processing, and scalability required for commercial deployment. Cloud-based smart farming platforms provide powerful analytics and multi-site aggregation capabilities but remain dependent on network connectivity and consumer-grade edge hardware that does not meet industrial operational requirements. Traditional *PLC/SCADA *systems offer proven reliability and real-time control performance, yet frequently operate as isolated automation systems with limited cloud integration and data analytics functionality. These findings suggest that future greenhouse automation solutions must bridge the gap between industrial-grade control and modern cloud connectivity to fully realize the potential of smart agriculture.
For Moldovan agriculture specifically, the adoption of smart greenhouse technologies presents a viable pathway toward modernizing protected cultivation, reducing dependency on manual labor, and improving resource efficiency. Multi-site monitoring capabilities enabled by cloud platforms support the scaling of precision agriculture practices across distributed agricultural enterprises, enabling centralized management and comparative optimization that were previously inaccessible to regional operators. Cloud-based data storage and analytics provide the historical datasets necessary for evidence-based agricultural planning, seasonal strategy adaptation, and long-term yield improvement.
Looking forward, the continued evolution of greenhouse automation will be shaped by emerging technological advancements including enhanced machine learning models for crop growth prediction, integration of computer vision for automated disease detection, digital twin implementations for greenhouse simulation and optimization, and blockchain-based traceability for agricultural supply chain transparency . Standards-based communication protocols and modular hardware architectures will enable greenhouse systems to evolve with these technologies without requiring complete redesigns, ensuring long-term adaptability and return on investment.
In conclusion, the convergence of industrial automation, *IoT* sensor networks, and cloud computing technologies provides a comprehensive foundation for addressing the challenges facing greenhouse agriculture in Moldova and similar climate-sensitive regions. By establishing intelligent, data-driven greenhouse ecosystems, the smart agriculture paradigm contributes to food security, agricultural competitiveness, and sustainable resource management, transforming protected agriculture from a traditional practice into a modern, technologically empowered industry aligned with the principles of *Industry 4.0*.
**Disclaimer:**
This report is based on publicly available research and technical sources. AI tools were used to help organize and summarize the information. The conclusions presented are drawn from these sources and should be viewed in the context of ongoing developments in agricultural automation.

**6. Bibliography**
ref1[1] FAO, “The future of food and agriculture,” 2017.Accessed: Feb. 10, 2026. [Online] Available: https://openknowledge.fao.org/server/api/core/bitstreams/2e90c833-8e84-46f2-a675-ea2d7afa4e24/content
ref2[2] C. Guzun, “IMPACTUL SCHIMBĂRILOR CLIMATICE ASUPRA AGRICULTURII DIN REPUBLICA MOLDOVA,” 2025. Accessed: Feb. 13, 2026. [Online]. Available: https://repository.utm.md/bitstream/handle/5014/34356/Conf-TehStiint-UTM-StudMastDoct-2025-V3-p634-638.pdf
ref3[3] M. Raj and M. Prahadeeswaran, “Revolutionizing agriculture: a review of smart farming technologies for a sustainable future,” Aug. 2025. Accessed: Feb. 13, 2026. [Online]. Available: https://link.springer.com/article/10.1007/s42452-025-07561-6
ref4[4] H. A. Méndez‑Guzmán et al., “IoT‑based monitoring system applied to aeroponics greenhouse,” Sensors, vol. 22, no. 15, p. 5646, 2022. [Online]. Available: https://www.mdpi.com/1424-8220/22/15/5646. Accessed: Feb. 12, 2026.
ref5[5] S. Dirac, G. E. Badea, and D. Mean, “Smart Agriculture: IoT-based Greenhouse Monitoring System,” International Journal of Computers, Communications & Control (IJCCC), Dec. 2022.Accessed: Feb. 10, 2026. [Online]. Available:https://www.researchgate.net/publication/366277451_Smart_Agriculture_IoT-based_Greenhouse_Monitoring_System
ref6[6] A. Bragarenco, G. Marusic, “INTERNET OF THINGS SYSTEM FOR ENVIRONMENTAL MAP ACQUISITION,” Journal of Engineering Science, 2019, Accessed: Feb. 12, 2026. [Online]. Available: https://jes.utm.md/wp-content/uploads/sites/20/2020/01/JES-2019-4_88-102.pdf
ref7[7] M. A. Sehr et al., "Programmable Logic Controllers in the Context of Industry 4.0," in IEEE Transactions on Industrial Informatics, vol. 17, no. 5, pp. 3523-3533, May 2021, doi: 10.1109/TII.2020.3007764.
ref8[8] A. Bragarenco, G. Marusic, and C. Ciufudean, “Layered architecture approach of the sensor software component stack for the Internet of Things applications,” WSEAS Transactions on Computer Research, vol. 7, pp. 124–135, 2019. [Online]. Available: https://wseas.com/journals/cr/2019/a305118-090.pdf. Accessed: Feb. 15, 2026.
ref9[9] SPAGNOL, Technical Catalogue. [Online]. Available: https://www.scribd.com/document/715492385/SPAGNOL-Technical-Catalogue. Accessed: Feb. 13, 2026.
ref10[10] Serviciul Hidrometeorologic de Stat, *Ghid climatic al Republicii Moldova: Ediție științifico-aplicativă (Date pe termen lung)*, Chișinău, Republica Moldova: Bons Offices SRL, 2024.
ref11[11] L. M. Mortensen, “Review: CO2 enrichment in greenhouses. Crop responses,” *Scientia Horticulturae*, vol. 33, no. 1–2, pp. 1–25, Aug. 1987, doi: https://doi.org/10.1016/0304-4238(87)90028-8.
ref12[12] A. Bhujel *et al.*, “Sensor Systems for Greenhouse Microclimate Monitoring and Control: a Review,” *Journal of Biosystems Engineering*, vol. 45, no. 4, pp. 341–361, Dec. 2020, doi: https://doi.org/10.1007/s42853-020-00075-6.
ref13[13] M. Soussi, T. Chaibi, M. Buchholz, and Z. Saghrouni, “Comprehensive review on climate control and cooling systems in greenhouses under hot and arid conditions,” *Agronomy*, vol. 12, p. 626, 2022, doi: 10.3390/agronomy12030626.
ref14[14] Arduino, Portenta Machine Control Hardware Overview. [Online]. Available: https://docs.arduino.cc/hardware/portenta-machine-control/. Accessed: Feb. 13, 2026.
ref15[15] H. X. Huynh, L. N. Tran, and N. Duong-Trung, “Smart greenhouse construction and irrigation control system for optimal Brassica juncea development,” PLoS ONE, vol. 18, no. 10, e0292971, Oct. 2023, doi: 10.1371/journal.pone.0292971.
ref16[16] W. Shi, J. Cao, Q. Zhang, Y. Li, and L. Xu, “Edge computing: Vision and challenges,” IEEE Internet of Things Journal, vol. 3, pp. 1–1, 2016, doi: 10.1109/JIOT.2016.2579198.
ref17[17] K. J. Åström and T. Hägglund, PID Controllers: Theory, Design, and Tuning, Research Triangle Park, NC, USA: Instrument Society of America, 1995.
ref18[18] R. Isermann, *Fault-Diagnosis Systems: An Introduction from Fault Detection to Fault Tolerance*, Berlin, Germany; New York, NY, USA: Springer, 2006.
ref19[19] S. Wolfert, L. Ge, C. Verdouw, and M.-J. Bogaardt, “Big data in smart farming – a review,” Agricultural Systems, vol. 153, pp. 69–80, 2017, doi: 10.1016/j.agsy.2017.01.023.
ref20[20] Modbus Organization, Modbus Application Protocol Specification v1.1b3, Modbus_Application_Protocol_V1_1b3.pdf, 2012. [Online]. Available: https://www.modbus.org/docs/Modbus_Application_Protocol_V1_1b3.pdf. Accessed: Feb. 13, 2026.
ref21[21] T. Kugelstadt, The RS‑485 Design Guide, Application Report SLLA272C, Texas Instruments, 2010. [Online]. Available: https://www.ti.com/lit/an/slla272c/slla272c.pdf. Accessed: Feb. 15, 2026.
ref22[22] B. Drury and Institution Of Electrical Engineers, The control techniques drives and controls handbook. Stevenage, UK: Institution Of Engineering And Technology, 2009.
ref23[23] OPC Foundation, OPC Unified Architecture Specification Part 1: Overview and Concepts, Release 1.04, 2017. [Online]. Available: https://reference.opcfoundation.org/Core/Part1/v104/docs/. Accessed: Feb. 16, 2026.
ref24[24] OASIS MQTT Technical Committee, MQTT Version 5.0, OASIS Standard, 2019. [Online]. Available: https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html. Accessed: Feb. 16, 2026.
ref25[25] IEEE Standards Association, IEEE 802.3™‑2022: IEEE Standard for Ethernet, 2022. [Online]. Available: https://standards.ieee.org/standard/802_3-2022.html. Accessed: Feb. 15, 2026.
ref26[26] H. Ibrahim, N. Mostafa, H. Halawa et al., “A layered IoT architecture for greenhouse monitoring and remote control,” SN Applied Sciences, vol. 1, p. 223, 2019, doi: 10.1007/s42452‑019‑0227‑8.
ref27[27] IEEE Standards Association, IEEE 802.11ax™‑2021: High Efficiency WLAN, 2021. [Online]. Available: https://standards.ieee.org/standard/802_11ax-2021.html. Accessed: Feb. 15, 2026.
ref28[28] A. Luz and G. Olaoye, “Security and privacy challenges in IoT-based greenhouse control systems,” EasyChair Preprint 13225, 2024. [Online]. Available: https://easychair.org/publications/preprint/W3pc. Accessed: Feb. 15, 2026.
ref29[29] T. Pelkonen, S. Franklin, J. Teller, P. Cavallaro, Q. Huang, J. Meza, and K. Veeraraghavan, “Gorilla: A Fast, Scalable, In-Memory Time Series Database.” Proceedings of the VLDB Endowment, vol. 8, pp. 1816–1827, 2015, doi: 10.14778/2824032.2824078.
ref30[30] G. van Straten, G. van Willigenburg, E. J. van Henten, and R. J. C. Ooteghem, Optimal Control of Greenhouse Cultivation, CRC Press, 2010, doi: 10.1201/b10321.
ref31[31] M. Rahaman, C.-Y. Lin, P. Pappachan, B. Gupta, and C.-H. Hsu, “Privacy‑centric AI and IoT solutions for smart rural farm monitoring and control,” *Sensors*, vol. 24, p. 4157, 2024, doi: 10.3390/s24134157.
ref32[32] K. Oliynyk, “Advanced greenhouse automation by 2Smart,” 2023. [Online]. Available: https://2smart.com/docs-resources/success-stories/advanced-smart-greenhouse-based-on-home-automation-system. Accessed: Feb. 15, 2026.
ref33[33] L. Hartawan, G. Rakhmat, N. Nugraha, N. D. Anggraeni, K. Maulana, M. Ridjali, M. Iqbal, M. Mahardhika, B. Alam, J. Fani, L. Fahlevi, M. Alfadhlih, M. Sbastio, and A. Purba, “Design of IoT‑based greenhouse temperature and humidity monitoring system,” ELKOMIKA: Jurnal Teknik Energi Elektrik, Teknik Telekomunikasi, & Teknik Elektronika, vol. 12, p. 1051, 2024, doi: 10.26760/elkomika.v12i4.1051.
ref34[34] S. Tammineedu and Y. N. V. Nikhil, “IoT based green house controlling and monitoring system,” B.E. ECE Project Report, Sathyabama Institute of Science and Technology, 2023. [Online]. Available: https://sist.sathyabama.ac.in/sist_naac/aqar_2022_2023/documents/1.3.4/b.e-ece-19-23-batchno-5.pdf. Accessed: Feb. 15, 2026.
ref35[35] A‑Bots, “Custom IoT solutions for greenhouses and vertical farms,” 2025. [Online]. Available: https://a‑bots.com/blog/IoT‑Solutions‑for‑Greenhouses. Accessed: Feb. 15, 2026.
ref36[36] A. Bragarenco, “Method for embedded systems development by configurations and code generation based on JSON metamodels,” AKADEMOS, vol. 3, no. 58, pp. 19–27, 2020, doi: 10.5281/zenodo.4269373.
ref37[37] G. S. Teja and P. Sathish, “MQTT protocol based smart greenhouse environment monitoring system,” International Journal of Innovative Technology and Exploring Engineering (IJITEE), vol. 9, no. 9, 2020. [Online]. Available: https://www.ijitee.org/wp-content/uploads/papers/v9i9/I7149079920.pdf. Accessed: Feb. 15, 2026.
ref38[38] N. Singh, R. Buyya, and H. Kim, “IoT in the cloud: Exploring security challenges and directions,” arXiv, Feb. 2024. [Online]. Available: https://arxiv.org/html/2402.00356v2. Accessed: Feb. 15, 2026.
ref39[39] M. Akhtar, M. Hussain, J. Arshad, M. Ahmad et al., “User authentication scheme for greenhouse remote monitoring system using WSNs/IoT,” in Proc. 2019 3rd International Conference on Future Networks and Distributed Systems, 2019. [Online]. Available: https://dl.acm.org/doi/abs/10.1145/3341325.3342039. Accessed: Feb. 15, 2026
ref40[40] A. Tandon, S. Gupta, A. R. Yadav, and R. Neware, “A novel secure authentication protocol for IoT and cloud servers,” Security and Communication Networks, vol. 2022, Article ID 7707543, 2022. [Online]. Available: https://onlinelibrary.wiley.com/doi/10.1155/2022/7707543. Accessed: Feb. 15, 2026.
ref41[41] J. F. Miceli Jr., “IAM: Securing IoT devices in precision agriculture,” 2024. [Online]. Available: https://www.identityfusion.com/blog/iam-securing-iot-devices-in-precision-agriculture. Accessed: Feb. 15, 2026.
ref42[42] C. D. Fay, B. Corcoran, D. Diamond et al., “Green IoT event detection for carbon‑emission monitoring in smart cities,” Sensors, vol. 24, no. 1, 2024. [Online]. Available: https://pmc.ncbi.nlm.nih.gov/articles/PMC10781252/. Accessed: Feb. 15, 2026.
ref43[43] A. Sagheer, M. Mohammed, K. Riad, and M. Alhajhoj, “A cloud‑based IoT platform for precision control of soilless greenhouse cultivation,” Sensors, vol. 21, no. 1, p. 223, 2021. [Online]. Available: https://pmc.ncbi.nlm.nih.gov/articles/PMC7796151/. Accessed: Feb. 15, 2026.
ref44[44] C. Bersani, C. Ruggiero, R. Sacile, A. Soussi, and E. Zero, “Internet of Things approaches for monitoring and control of smart greenhouses in Industry 4.0,” Energies, vol. 15, no. 10, p. 3834, 2022. [Online]. Available: https://www.mdpi.com/1996-1073/15/10/3834. Accessed: Feb. 15, 2026.
ref45[45] A. Bragarenco and G. Marusic, “Layered architecture for IoT‑based industrial automation systems,” in Proc. IEEE Int. Conf. System Theory, Control and Computing (ICSTCC), 2020, pp. 540–545. [Online]. Available: https://repository.utm.md/bitstream/handle/5014/25654/Conf-IEEE-ICSTCC‑2020‑p540‑545.pdf. Accessed: Feb. 15, 2026.
ref46[46] R. Rayhana, G. Xiao, and Z. Liu, “Internet of Things empowered smart greenhouse farming,” *IEEE Journal of Radio Frequency Identification*, vol. 4, no. 4, pp. 195–211, 2020, doi: 10.1109/JRFID.2020.2984391.

‌
