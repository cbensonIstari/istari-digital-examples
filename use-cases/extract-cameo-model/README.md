# Use Case: Extract a Cameo Enterprise Architect Model

## Intent

I have a Cameo `.mdzip` file and I want to understand what's in it — blocks, requirements, diagrams, system architecture — without opening Cameo Enterprise Architect and manually navigating the containment tree. Upload the file to Istari, run extraction, get structured SysML/UML data and all diagrams automatically.

## Tools Used

| Tool | Role |
|------|------|
| **Istari Platform** | Outer loop — stores the model, runs extraction, hosts artifacts, shares with team |
| **Cameo Enterprise Architect** (`@istari:extract` via `dassault_cameo` 2024x Refresh2) | Inner loop — opens the .mdzip, parses SysML/UML model, extracts blocks, requirements, and renders all diagrams |

## Inner / Outer Loop

```
+--- Outer Loop: Istari -- store - extract - view - share ----------+
|                                                                     |
|   +- Cameo Enterprise Architect (inner loop) ---+                  |
|   | Open .mdzip -> parse SysML/UML -> extract   |                  |
|   | blocks, reqs -> render all diagrams as PNG   |                  |
|   +---------------------+-----------------------+                  |
|                         |                                           |
|                         v                                           |
|   blocks.json - requirements.json - 46 diagram PNGs                |
+---------------------------------------------------------------------+
```

The **inner loop** (Cameo) does the domain-specific work — opening the native .mdzip model, parsing the SysML/UML containment tree, extracting all block definitions and requirement specifications, and rendering every diagram as a PNG image. The **outer loop** (Istari) handles everything else — storing the model, running the extraction as a tracked job on a Windows agent, hosting the artifacts so anyone can view them, and versioning so you can re-extract after changes.

## K-Script

| Step | Interaction / Process | Unobservable Actions or Assumptions |
|------|----------------------|-------------------------------------|
| 1 | **Engineer:** Uploads a `.mdzip` file to Istari | Model was built in Cameo; engineer may not have a Cameo license |
| 2 | **Engineer:** Navigates to the system, sees the model tracked in a configuration | File is tracked with LATEST specifier |
| 3 | **Engineer:** Runs `@istari:extract` on the model | Job is matched to an agent running Cameo 2024x Refresh2 on Windows Server 2022 |
| 4 | **System:** Agent opens the model in Cameo and parses all elements | Walks the containment tree, extracts Block and Requirement elements |
| 5 | **System:** Agent renders every diagram in the model as PNG | Block diagrams, requirement diagrams, use case diagrams, activity diagrams, etc. |
| 6 | **System:** Job completes; 48 artifacts appear on the model | blocks.json (5.3 MB), requirements.json (24 KB), 46 PNG diagrams |
| 7 | **Engineer:** Opens `requirements.json` to see all system requirements | Structured list with IDs, names, text, and traceability |
| 8 | **Engineer:** Opens `blocks.json` to understand the system architecture | Full block hierarchy with properties, ports, and relationships |
| 9 | **Engineer:** Views diagram PNGs to see the visual architecture | Stakeholder needs, system context, use cases, subsystem breakdowns |
| 10 | **Engineer:** Snapshots the results for the team | Point-in-time capture of the model + all extraction artifacts |

## Expected Results

Running extraction on `Istari_UAVOne.mdzip` (4.6 MB) produces 48 artifacts:

| Artifact | Format | Size | Description |
|----------|--------|------|-------------|
| `blocks.json` | JSON | 5,320.7 KB | Full block hierarchy with properties and relationships |
| `requirements.json` | JSON | 24.2 KB | All requirements with IDs, text, and traceability |
| 46 diagram PNGs | PNG | 1.6 KB - 3,744.7 KB | Every diagram in the model rendered as an image |

### Key diagrams

| Diagram | Size | Shows |
|---------|------|-------|
| Istari One Body Block Diagram | 135.0 KB | Top-level system architecture |
| Stakeholder Needs | 51.3, 176.4 KB | Requirements from stakeholders |
| Conceptual Subsystems | 65.0 KB | Subsystem breakdown |
| System Context | 245.2 KB | System-of-systems context |
| Use Cases | 124.7, 321.6 KB | Operational use cases |
| Measures of Effectiveness | 198.8, 108.7 KB | Performance metrics |
| Architecture Framework | 467.7 KB | UAF architecture mapping |
| Requirement Verification | 94.3 KB | Verification traceability |

## Version Control

| # | Snapshot Tag | Files | What happened |
|---|-------------|-------|---------------|
| 1 | `initial-upload` / `baseline` | 1 | Raw .mdzip uploaded |
| 2 | `post-extraction` | 49 | mdzip + 48 extraction artifacts (blocks, requirements, diagrams) |

## Try It

Run the notebook: [`extract_cameo.ipynb`](extract_cameo.ipynb)

See [`example-input/`](example-input/) for the source mdzip file and [`example-output/`](example-output/) for pre-computed results.
