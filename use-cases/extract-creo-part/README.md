# Use Case: Extract a Creo Parametric Part

## Intent

I have a PTC Creo `.prt` file and I want to know what's in it — parameters, mass properties, and what it looks like — without spinning up a Creo Parametric workstation. Upload the file to Istari, run extraction, get structured data and rendered views automatically.

## Tools Used

| Tool | Role |
|------|------|
| **Istari Platform** | Outer loop — stores the model, runs extraction, hosts artifacts, shares with team |
| **PTC Creo Parametric** (`@istari:extract` via `ptc_creo_parametric` v10.0.0.0) | Inner loop — opens the part in Creo, extracts parameters, mass properties, BOM, and renders views |

## Inner / Outer Loop

```
+--- Outer Loop: Istari -- store - extract - view - share ----------+
|                                                                     |
|   +- Creo Parametric (inner loop) -----+                           |
|   | Open .prt -> read params, calc     |                           |
|   | mass, render 7 views, export OBJ   |                           |
|   +----------------+------------------+                            |
|                    |                                                |
|                    v                                                |
|   Parameters JSON - Mass JSON - BOM JSON - 7x PNG - OBJ mesh       |
+---------------------------------------------------------------------+
```

The **inner loop** (Creo Parametric) does the domain-specific work — opening the native .prt file, reading parameters, calculating mass properties, generating a bill of materials, rendering 7 standard views, and exporting an OBJ mesh. The **outer loop** (Istari) handles everything else — storing the model, running the extraction as a tracked job on a Windows agent, hosting the artifacts so anyone can view them, and versioning so you can re-extract after changes.

## K-Script

| Step | Interaction / Process | Unobservable Actions or Assumptions |
|------|----------------------|-------------------------------------|
| 1 | **Engineer:** Uploads a `.prt` file to Istari | Part was designed in PTC Creo; engineer may not have a Creo license on their current machine |
| 2 | **Engineer:** Navigates to the system, sees the part tracked in a configuration | File is tracked with LATEST specifier — always shows the newest version |
| 3 | **Engineer:** Runs `@istari:extract` on the part | Job is matched to an agent running Creo Parametric (ptc_creo_parametric v10.0.0.0 on Windows Server 2022) |
| 4 | **System:** Agent opens the part in Creo and extracts data | Reads parameters, calculates mass/volume/CoM, generates BOM |
| 5 | **System:** Agent renders 7 standard views and exports OBJ mesh | 6 orthographic + 1 isometric view; lightweight 3D mesh |
| 6 | **System:** Job completes; 14 artifacts appear on the model | Parameters, mass properties, BOM, part data as JSON; 7 PNGs; OBJ; regenerated PRT |
| 7 | **Engineer:** Views parameters to understand part configuration | No Creo license needed — just JSON in the browser |
| 8 | **Engineer:** Views rendered images to see the part geometry | 7 views give a complete picture without opening CAD |
| 9 | **Engineer:** Snapshots the results for the team | Point-in-time capture of the part + all extraction artifacts |

## Expected Results

Running extraction on `gearcase.prt` (751.7 KB) produces 14 artifacts:

| Artifact | Format | Size | Description |
|----------|--------|------|-------------|
| `iso.png` | PNG | 619.8 KB | Isometric view |
| `front.png`, `back.png` | PNG | 690.8, 778.0 KB | Front and back views |
| `top.png`, `bottom.png` | PNG | 669.4, 670.4 KB | Top and bottom views |
| `left.png`, `right.png` | PNG | 644.3, 657.1 KB | Left and right views |
| `creo_model.obj` | OBJ | 39.6 KB | 3D mesh viewable in any mesh viewer |
| `creo_model.prt` | PRT | 763.6 KB | Regenerated Creo part |
| `parameters.json` | JSON | 0.5 KB | Part parameters with values |
| `GEARCASE.json` | JSON | 0.5 KB | Part-specific data |
| `mass_properties.json` | JSON | 0.8 KB | Mass, volume, density, bounding box |
| `bill_of_materials.json` | JSON | 0.2 KB | BOM |
| `parts.json` | JSON | 0.0 KB | Part list |

## Version Control

| # | Snapshot Tag | Files | What happened |
|---|-------------|-------|---------------|
| 1 | `initial-upload` / `baseline` | 1 | Raw .prt uploaded |
| 2 | `post-extraction` | 15 | PRT + 14 extraction artifacts |

## Try It

Run the notebook: [`extract_creo.ipynb`](extract_creo.ipynb)

See [`example-input/`](example-input/) for the source PRT file and [`example-output/`](example-output/) for pre-computed results.
