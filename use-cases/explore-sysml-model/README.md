# Use Case: Understand My Requirements & Architecture — Without Being a SysML Expert

## Intent

I have a `.sysml` file sitting in Istari and I just want to understand what's in it — what requirements exist, what parts are defined, how they relate. I don't want to install a SysML editor or learn the syntax. I want structured, readable output.

## Tools Used

| Tool | Role |
|------|------|
| **Istari Platform** | Outer loop — stores the model, runs extraction, hosts artifacts, shares with team |
| **SysGit** (`@istari:extract_sysmlv2`) | Inner loop — parses SysML v2 text, extracts structured data + visual diagrams |

## Inner / Outer Loop

```
┌─── Outer Loop: Istari ── store · extract · view · share ───┐
│                                                              │
│   ┌─ SysGit (inner loop) ────────────────────────────────┐   │
│   │ Parse SysML v2 → extract reqs & parts → gen diagrams │   │
│   └──────────────────────────┬────────────────────────────┘   │
│                              │                                │
│                              ↓                                │
│   Requirements JSON · Parts JSON · Hierarchy PNG · Parts PNG  │
└───────────────────────────────────────────────────────────────┘
```

The **inner loop** (SysGit) does the domain-specific parsing — understanding SysML v2 syntax, resolving requirement hierarchies, extracting part attributes, and rendering diagrams. The **outer loop** (Istari) handles everything else — storing the model, running the extraction as a tracked job, hosting the artifacts so anyone on the team can view them, and versioning so you can re-extract after changes.

## K-Script

| Step | Interaction / Process | Unobservable Actions or Assumptions |
|------|----------------------|-------------------------------------|
| 1 | **Engineer:** Opens Istari in browser, navigates to "Group3 UAS" system | Engineer received a .sysml file from a systems architect and uploaded it earlier |
| 2 | **Engineer:** Sees the .sysml file listed under the configuration | File is tracked with LATEST specifier — always shows the newest version |
| 3 | **Engineer:** Clicks on the .sysml file to preview it | Istari renders SysML v2 text with syntax highlighting in the browser |
| 4 | **Engineer:** Reads the raw text but finds it hard to quickly parse — "what requirements are actually in here?" | SysML v2 is verbose — requirement definitions, part definitions, constraints, and satisfy statements are all interleaved |
| 5 | **Engineer:** Wants a structured view → clicks "Run Function" and selects `extract_sysmlv2` | Available functions are determined by the file extension (.sysml) |
| 6 | **System:** Queues the extraction job and assigns it to an available agent | Job is matched to an agent running sysgit v0.1.8 on Ubuntu 22.04 |
| 7 | **System:** Agent parses the SysML model, extracts all RequirementUsage and PartUsage elements | SysGit preprocesses the file — strips unsupported constructs like `satisfy` statements before parsing |
| 8 | **System:** Generates structured JSON for requirements and parts, plus two PNG diagrams | Graphviz renders the hierarchy; JSON captures IDs, descriptions, target values, parent-child relationships |
| 9 | **System:** Job completes; 4 artifacts appear on the model | `output_requirements.json`, `output_parts.json`, `requirements_hierarchy.png`, `parts_diagram.png` |
| 10 | **Engineer:** Clicks on `requirements_hierarchy.png` to see the visual tree | Diagram shows color-coded depth — system-level requirements at top, sub-requirements nested below |
| 11 | **Engineer:** Opens `output_requirements.json` to read individual details | Each requirement has: ID, name, "shall" description, target value, unit, priority, parent reference |
| 12 | **Engineer:** Finds the range requirement — "1500 nm" — and checks it against the current wing design | This is the connection point: requirements (SysGit) inform geometry parameters (nTop) |
| 13 | **Engineer:** Opens `parts_diagram.png` to understand the physical system structure | Shows Propulsion, Power, Flight Control, Communications, Payload, Airframe with key attributes |
| 14 | **Engineer:** Shares the system with a teammate so they can review the extracted data | Sharing requires access on both the system and its files |
| 15 | **Engineer:** Done — knows what's in the model and can reference specific requirements by ID in design reviews | Extracted artifacts persist alongside the model; no re-extraction needed unless the .sysml changes |

## Expected Results

Running extraction on the Group3 UAS model (`group3_uas_requirements.sysml`, 596 lines, 22.7 KB) produces:

| Artifact | Size | Contents |
|----------|------|----------|
| `output_requirements.json` | 5.5 KB | 11 requirements with target values, units, and parent references |
| `output_parts.json` | 34.6 KB | 39 parts across 6 subsystems with typed attributes |
| `requirements_hierarchy.png` | 253 KB | Visual tree: TopLevelRequirements → 10 child requirements |
| `parts_diagram.png` | 828 KB | Block diagram: Drone → Propulsion, Power, Flight Control, Comms, Payload, Airframe |

### Requirements found

| Requirement | Shall Statement | Target |
|-------------|----------------|--------|
| RangeReq | The drone shall achieve a range of at least 1000 nm | 1000.0 nm |
| MaxStructureWeight | The drone structure weight shall not exceed 275 lb | 275.0 lb |
| CruiseSpeed | The drone shall achieve a cruise speed of at least 100 knots | 100.0 knots |
| PayloadCapacity | The drone shall carry a payload of at least 125 lb | 125.0 lb |
| OperatingTemperature | The drone shall operate in temperatures from -10°C to 45°C | -10.0 to 45.0 °C |
| FailSafeReq | The drone shall return to home on signal loss | Critical |
| BatteryMonitoring | The system shall monitor battery voltage and initiate landing at 15% capacity | Critical |
| PositionAccuracy | The drone shall maintain position accuracy within 2.5m | 2.5 m |
| VideoTransmissionRange | Video transmission shall work up to 1000m range | 1000.0 m |
| ControlRange | Control signals shall work up to 1500m range | 1500.0 m |

### Parts found (39 total, 6 subsystems)

| Subsystem | Parts | Example Attributes |
|-----------|-------|--------------------|
| Propulsion System | engine, propeller, fuelSystem, starter | displacement: 215cc, maxPower: 23hp, fuelType: JP-8 |
| Power System | alternator, avionicsBattery, powerDistributionBoard, regulators | outputPower: 500W, capacity: 8000mAh, 6S LiPo |
| Flight Control System | flightController, gyroscope, accelerometer, magnetometer, barometer, gps, airspeedSensor | Pixhawk 6X, ICM-42688, UBLOX F9P RTK |
| Communication System | radioReceiver, telemetryModule, satelliteComm, videoTransmitter | RFD900x 433MHz, Iridium 9603, 60km range |
| Payload System | eoirCamera, thermalCamera, gimbal, gimbalController, lidarSensor, additionalPayloadBay | 30x zoom, 640x512 LWIR, Velodyne Puck Lite |
| Airframe | centerBody, wing, elevons, winglets, landingGear, avionicsBay | 6061-T6 aluminum, 4.5m wingspan, reflexed airfoil |

See [`example-input/`](example-input/) for the source SysML file and [`example-output/`](example-output/) for the full JSON and PNG files.

## Try It

Run the notebook: [`explore_sysml_model.ipynb`](explore_sysml_model.ipynb)

Or from the command line using the scripts in [`sysgit/`](../../sysgit/):

```bash
python sysgit/update_and_extract_sysml.py --model-id <MODEL_ID> --extract-only
```
