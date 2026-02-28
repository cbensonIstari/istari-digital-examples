# Use Case: Extract a CATIA V5 Part

## Intent

I have a `.CATPart` file and I want to know what's in it — parameters, mass properties, and what it looks like — without spinning up a CATIA V5 workstation. Upload the file to Istari, run extraction, get structured data and rendered views automatically.

## Tools Used

| Tool | Role |
|------|------|
| **Istari Platform** | Outer loop — stores the model, runs extraction, hosts artifacts, shares with team |
| **CATIA V5** (`@istari:extract` via `dassault_catia_v5` 6R2023) | Inner loop — opens the part in CATIA V5, extracts parameters, mass properties, BOM, and renders views |

## Inner / Outer Loop

```
+--- Outer Loop: Istari -- store - extract - view - share --------+
|                                                                   |
|   +- CATIA V5 (inner loop) -----------------------------------+   |
|   | Open .CATPart -> read params, calc mass, render 7 views   |   |
|   +----------------------------+------------------------------+   |
|                                |                                  |
|                                v                                  |
|   Parameters JSON - Mass JSON - BOM JSON - 7x PNG - OBJ mesh     |
+-------------------------------------------------------------------+
```

The **inner loop** (CATIA V5) does the domain-specific work — opening the native CATPart, reading user-defined parameters, calculating mass properties, generating a bill of materials, rendering 7 standard views, and exporting an OBJ mesh. The **outer loop** (Istari) handles everything else — storing the model, running the extraction as a tracked job on a Windows agent, hosting the artifacts so anyone can view them, and versioning so you can re-extract after changes.

## K-Script

| Step | Interaction / Process | Unobservable Actions or Assumptions |
|------|----------------------|-------------------------------------|
| 1 | **Engineer:** Uploads a `.CATPart` file to Istari | Part was designed in CATIA V5; engineer may not have a CATIA license on their current machine |
| 2 | **Engineer:** Navigates to the system, sees the part tracked in a configuration | File is tracked with LATEST specifier — always shows the newest version |
| 3 | **Engineer:** Runs `@istari:extract` on the part | Job is matched to an agent running CATIA V5 (dassault_catia_v5 6R2023 on Windows Server 2022) |
| 4 | **System:** Agent opens the part in CATIA V5 and extracts data | Reads all user-defined parameters, calculates mass/volume/CoM, generates BOM |
| 5 | **System:** Agent renders 7 standard views (6 orthographic + 1 isometric) | Views use default CATIA rendering settings |
| 6 | **System:** Agent exports an OBJ mesh of the part geometry | Lightweight 3D representation viewable in any mesh viewer |
| 7 | **System:** Job completes; ~10 artifacts appear on the model | Parameters, mass properties, BOM as JSON; 7 PNGs; 1 OBJ |
| 8 | **Engineer:** Views parameters to understand part configuration | No CATIA license needed — just JSON in the browser |
| 9 | **Engineer:** Views mass properties to check weight and center of mass | Useful for quick mass checks during design reviews |
| 10 | **Engineer:** Views rendered images to see the part geometry | 7 views give a complete picture without opening CAD |
| 11 | **Engineer:** Snapshots the results for the team | Point-in-time capture of the part + all extraction artifacts |

## Expected Results

Running extraction on `Bracket.CATPart` (289.5 KB) produces 12 artifacts:

| Artifact | Format | Size | Description |
|----------|--------|------|-------------|
| `iso.png` | PNG | 59.6 KB | Isometric view |
| `front.png`, `back.png` | PNG | 23.3, 21.1 KB | Front and back views |
| `top.png`, `bottom.png` | PNG | 48.4, 46.1 KB | Top and bottom views |
| `left.png`, `right.png` | PNG | 37.8, 38.6 KB | Left and right views |
| `geometry.obj` | OBJ | 42.5 KB | 3D mesh viewable in any mesh viewer |
| `parameters.json` | JSON | 1.1 KB | 8 user-defined parameters |
| `mass_properties.json` | JSON | 0.8 KB | Mass, volume, density, bounding box |
| `bill_of_materials.json` | JSON | 0.2 KB | Single-part BOM |
| `parts.json` | JSON | 0.0 KB | Part list |

### Parameters found

| Parameter | Value | Unit |
|-----------|-------|------|
| HOLE_DIAMETER | 40 | mm |
| KNOTCH_OPENING | 80 | mm |
| FLANGE_THICKNESS | 15 | mm |
| LENGTH_BRACKET | 180 | mm |
| GUSSET_THICKNESS | 25 | mm |
| HOLE_SPACING_WIDTH | 57.5 | mm |
| HOLE_SPACING_LENGTH | 130 | mm |
| BOLT_DIAMETER | 10 | mm |

### Mass properties

| Property | Value | Unit |
|----------|-------|------|
| Mass | 0.894 | kg |
| Volume | 3.309e-4 | m³ |
| Surface Area | 0.067 | m² |
| Density | 2,700 | kg/m³ |
| Bounding Box | 180 x 90 x 90 | mm |

## Version Control

| # | Snapshot Tag | Files | What happened |
|---|-------------|-------|---------------|
| 1 | `initial-upload` / `baseline` | 1 | Raw .CATPart uploaded |
| 2 | `post-extraction` | 13 | CATPart + 12 extraction artifacts (params, mass, views, OBJ) |

## What's Next?

- **Update parameters** — use `@istari:update_parameters` to modify CAD parameters without opening CATIA
- **Extract assemblies** — upload a `.CATProduct` (as .zip with dependencies) to extract BOM and assembly structure
- **Compare revisions** — upload a modified part, re-extract, and compare parameters across versions

## Try It

Run the notebook: [`extract_catia_v5.ipynb`](extract_catia_v5.ipynb)

See [`example-input/`](example-input/) for the source CATPart file and [`example-output/`](example-output/) for pre-computed results.
