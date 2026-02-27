# Use Case: Explore a SysML Model

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

## Try It

Run the notebook: [`explore_sysml_model.ipynb`](explore_sysml_model.ipynb)

Or from the command line using the scripts in [`sysgit/`](../../sysgit/):

```bash
python sysgit/update_and_extract_sysml.py --model-id <MODEL_ID> --extract-only
```
