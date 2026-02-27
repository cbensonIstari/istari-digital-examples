# Use Case: Does My Design Meet Requirements?

## Intent

Three engineers are working on the same aircraft — one on requirements, one on the system architecture, one on the CAD model. They each use their own tools. The question is: **does it all line up?** Do the requirements match the architecture? Does the CAD model actually meet the requirements? And when something changes, how fast can we re-check?

## The Old Way

```
 Requirements           Architecture            CAD Model
 Engineer               Engineer                Engineer
     |                      |                       |
     v                      |                       |
 Write requirements         |                       |
     |                      |                       |
     +--- handoff --------->|                       |
     |                      v                       |
     |               Write architecture             |
     |                      |                       |
     |<-- weeks of -------->|                       |
     |    meetings          |                       |
     |                      |                       |
     v                      v                       |
 Reqs + Arch aligned        |                       |
     |                      |                       |
     +-------- handoff -----+---------------------->|
     |                      |                       v
     |                      |                Build CAD model
     |                      |                       |
     |<----- more weeks of meetings --------------->|
     |        three-way alignment                   |
     v                      v                       v
               Final alignment (hopefully)
```

**Problems:** Serial handoffs. Weeks of meetings. No automated checks. Copy-paste engineering. Everyone has their own version of the truth. By the time the CAD engineer hears about a requirement change, he's already three revisions deep.

## The New Way (with Istari)

```
+--- Outer Loop: Istari -- version - check - compare -------------+
|                                                                  |
|  +- SysGit ----------+  +- SysGit ----------+  +- nTop -------+ |
|  | Requirements      |  | Architecture      |  | CAD Model    | |
|  | (Engineer A)      |  | (Engineer B)      |  | (Engineer C) | |
|  +--------+----------+  +--------+----------+  +------+-------+ |
|           |                      |                     |         |
|           v                      v                     v         |
+------------------------------------------------------------------+
|  Automated checks: requirements <-> architecture <-> CAD         |
|  --> Compliance report: PASS / FAIL per check                    |
+------------------------------------------------------------------+
```

Everyone works in parallel in their preferred tool. Istari stores everything in one system. **Checks run automatically** — no meetings required to answer "does it line up?"

## Tools Used

| Tool | Role |
|------|------|
| **Istari Platform** | Outer loop — stores all three models, runs extractions, hosts artifacts, connects everything |
| **SysGit** (`@istari:extract_sysmlv2`) | Inner loops 1 & 2 — parses SysML v2 to extract requirements and architecture as structured JSON |
| **nTopology** (`@ntop:run_model` via `ntopcl`) | Inner loop 3 — runs parametric wing model, produces aerodeck metrics and rendered views |
| **Compliance checks** (Python, in this repo) | Automated scripts that compare requirements ↔ architecture ↔ CAD and produce a pass/fail report |

## Milestones

### Milestone 1: Everything in one system

Get requirements, architecture, and CAD model all into one Istari system. Extract the SysML to get structured JSON. Load the latest nTop results. **"I can see it all in one place."**

### Milestone 2: Automated compliance checks

Run the check scripts against the extracted data:
- **Requirements ↔ Architecture**: Does each requirement trace to a subsystem? Does the mass roll-up from components match the weight budget?
- **Requirements ↔ CAD**: Does the actual range meet the range requirement? Does the actual weight meet the weight requirement?

Produce a compliance report. **Weight check FAILS** — the wing weighs 321.8 lb but the requirement says 275 lb.

### Milestone 3: Negotiate and update

The 275 lb budget can't be met with this wing design. The team agrees to relax the requirement to 325 lb. Update the SysML, re-extract, re-run checks. **All green.**

### Milestone 4: Final compliance report

Present a clean compliance report — all checks pass. This is what you'd bring to a design review. Old way: weeks of meetings. New way: 10 minutes in a notebook.

## K-Script

| Step | Interaction / Process | Unobservable Actions or Assumptions |
|------|----------------------|-------------------------------------|
| 1 | **Engineer A:** Writes requirements in SysML v2 — range, weight, speed, payload targets | Uses a SysML editor or text editor; requirements have quantitative targets with units |
| 2 | **Engineer B:** Defines the system architecture in SysML v2 — subsystems, parts, component specs | Works independently; architecture includes mass estimates for each component |
| 3 | **Engineer C:** Builds a parametric wing model in nTopology with configurable sweep, span, panel break | Works independently in the nTop GUI; model accepts parameter JSON as input |
| 4 | **All three:** Upload their files to the same Istari system | Each engineer connects their tool output to Istari; all files land in one system |
| 5 | **System:** SysGit extracts requirements and architecture from the .sysml file → structured JSON | Extraction produces `output_requirements.json` (11 requirements) and `output_parts.json` (39 parts) |
| 6 | **System:** nTop runs the wing model with baseline parameters → aerodeck metrics + views | Run produces 14 artifacts including `aerodeck_metrics.json` with weight, range, speed |
| 7 | **Engineer A:** "Okay, everything's uploaded. Can we check if it all lines up?" | This is the moment — instead of scheduling a meeting, they run automated checks |
| 8 | **System:** Compliance check — requirements vs architecture | Checks traceability (does each requirement map to a subsystem?) and mass roll-up (do component masses fit the budget?) |
| 9 | **System:** Compliance check — requirements vs CAD | Compares aerodeck actuals against requirement targets: range, weight, speed |
| 10 | **System:** Report generated — Range ✅, Speed ✅, Weight ❌ (321.8 lb vs 275 lb) | The report shows exactly where the gap is — no ambiguity |
| 11 | **Engineer C:** "I can't get the wing below 320 lb without losing range. Can we adjust the weight budget?" | This is the design tension — the CAD results inform a requirement negotiation |
| 12 | **Engineer A:** Agrees to relax MaxStructureWeight from 275 lb to 325 lb | Team decision based on data, not guesswork |
| 13 | **Engineer A:** Updates the .sysml file — changes `maxValue` from 275.0 to 325.0, updates the description | Single line change in the SysML text |
| 14 | **System:** Re-uploads updated .sysml as a new revision in Istari | Istari tracks the change — old revision is preserved, new revision is active |
| 15 | **System:** Re-extracts requirements → updated JSON shows 325 lb target | Extraction confirms the change propagated correctly |
| 16 | **System:** Re-runs compliance checks with updated requirements | Same check scripts, updated input data |
| 17 | **System:** Report generated — Range ✅, Speed ✅, Weight ✅ | All checks pass |
| 18 | **All three:** Review the compliance report in the design review — everything lines up, with full traceability | Old way: weeks of meetings. New way: update, re-check, done |

## Expected Results

### Initial compliance check (before update)

| Check | Requirement | Target | Actual | Status |
|-------|-------------|--------|--------|--------|
| Range | RangeReq | ≥ 1,500 nm | 2,312 nm | ✅ PASS |
| Cruise Speed | CruiseSpeed | ≥ 100 kts | 175 kts | ✅ PASS |
| Structure Weight | MaxStructureWeight | ≤ 275 lb | 321.8 lb | ❌ FAIL |
| Architecture Mass Roll-up | MaxStructureWeight | ≤ 275 lb | 155.7 lb (components) | ✅ PASS |

### After updating requirement (275 → 325 lb)

| Check | Requirement | Target | Actual | Status |
|-------|-------------|--------|--------|--------|
| Range | RangeReq | ≥ 1,500 nm | 2,312 nm | ✅ PASS |
| Cruise Speed | CruiseSpeed | ≥ 100 kts | 175 kts | ✅ PASS |
| Structure Weight | MaxStructureWeight | ≤ 325 lb | 321.8 lb | ✅ PASS |
| Architecture Mass Roll-up | MaxStructureWeight | ≤ 325 lb | 155.7 lb | ✅ PASS |

## Check Script

The compliance checks live in [`compliance_checks.py`](compliance_checks.py) and can be imported from the notebook:

```python
from compliance_checks import run_all_checks, format_report

results = run_all_checks(reqs_data, parts_data, metrics_data)
print(format_report(results))

# Output:
#   Range                          PASS  (2312.0 nm >= 1500.0 nm, margin: +54.1%)
#   Structure Weight               FAIL  (321.75 lb <= 275.0 lb, margin: -17.0%)
#   Cruise Speed                   PASS  (175 kts >= 100.0 kts, margin: +75.0%)
#   Architecture Mass Roll-up      PASS  (155.7 lb <= 275.0 lb, margin: +43.4%)
```

## Example Files

### [`example-input/`](example-input/) — what goes in

| File | Milestone | Description |
|------|-----------|-------------|
| `group3_uas_requirements.sysml` | 1 | The original SysML source file (requirements + architecture) |
| `v4_input.json` | 1 | nTop wing parameters (sweep, span, panel break) |

### [`example-output/`](example-output/) — what comes out

| File | Milestone | Description |
|------|-----------|-------------|
| `output_requirements.json` | 1 | Extracted requirements (11 total, with target values) |
| `output_parts.json` | 1 | Extracted architecture (39 parts across 6 subsystems) |
| `grp3-uas_v6_aerodeck_metrics.json` | 1 | nTop aerodeck results (weight, range, speed, stability) |
| `compliance_report_initial.md` | 2 | First compliance check — **weight fails** (321.8 lb vs 275 lb) |
| `group3_uas_requirements_updated.sysml` | 3 | Updated SysML with relaxed weight budget (275 → 325 lb) |
| `output_requirements_updated.json` | 3 | Re-extracted requirements showing the 325 lb target |
| `compliance_report_final.md` | 4 | Final compliance check — **all green** |

## Try It

Run the notebook: [`check_design.ipynb`](check_design.ipynb)
