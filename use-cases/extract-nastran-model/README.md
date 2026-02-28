# Use Case: Extract a NASTRAN FEM Model

## Intent

I have a NASTRAN `.bdf` file and I want to understand what's in it — mesh structure, materials, properties, loads, and constraints — without opening NASTRAN or Patran and manually inspecting thousands of lines of bulk data cards. Upload the file to Istari, run extraction, get structured FEM data automatically.

## Tools Used

| Tool | Role |
|------|------|
| **Istari Platform** | Outer loop — stores the model, runs extraction, hosts artifacts, shares with team |
| **NASTRAN Extractor** (`@istari:extract_input` via `nastran_extract`) | Inner loop — parses NASTRAN bulk data cards and extracts structured FEM data |

## Inner / Outer Loop

```
+--- Outer Loop: Istari -- store - extract - view - share --------+
|                                                                   |
|   +- NASTRAN Extractor (inner loop) --------------------------+   |
|   | Parse .bdf bulk data -> extract mesh, materials, loads    |   |
|   +----------------------------+------------------------------+   |
|                                |                                  |
|                                v                                  |
|   Mesh info - Materials - Properties - Loads - Constraints        |
+-------------------------------------------------------------------+
```

The **inner loop** (NASTRAN Extractor) does the domain-specific work — parsing NASTRAN bulk data card format, extracting grid points, element connectivity, material definitions, property cards, load cases, and boundary conditions. The **outer loop** (Istari) handles everything else — storing the model, running the extraction as a tracked job on a Linux agent, hosting the artifacts so anyone can view them, and versioning so you can re-extract after changes.

## K-Script

| Step | Interaction / Process | Unobservable Actions or Assumptions |
|------|----------------------|-------------------------------------|
| 1 | **Engineer:** Uploads a NASTRAN `.bdf` file to Istari | BDF was created in MSC Patran or similar preprocessor |
| 2 | **Engineer:** Navigates to the system, sees the BDF tracked in a configuration | File is tracked with LATEST specifier — always shows the newest version |
| 3 | **Engineer:** Runs `@istari:extract_input` on the model | Job is matched to an agent running nastran_extract v1.0.0 on Ubuntu 22.04 |
| 4 | **System:** Agent parses the NASTRAN bulk data cards | Reads GRID, CQUAD4, CTRIA3, MAT1, PSHELL, FORCE, SPC cards and more |
| 5 | **System:** Agent extracts structured FEM data as JSON | Mesh info, material properties, element properties, loads, constraints |
| 6 | **System:** Job completes; extraction artifacts appear on the model | Structured JSON files describing the full FEM model |
| 7 | **Engineer:** Views mesh info to understand model size and element types | Grid count, element types and counts, coordinate systems |
| 8 | **Engineer:** Views materials to check material properties | Young's modulus, Poisson's ratio, density for each material card |
| 9 | **Engineer:** Views loads and constraints to verify boundary conditions | Applied forces, moments, SPCs — all extracted without opening Patran |
| 10 | **Engineer:** Snapshots the results for the team | Point-in-time capture of the BDF + all extraction artifacts |

## Expected Results

Running extraction on `Aircraft-One_DEMO.bdf` produces structured FEM data including:

| Data | Description |
|------|-------------|
| Mesh info | Grid points, element types (CQUAD4, CTRIA3, etc.), element counts |
| Materials | MAT1/MAT2 cards — E, G, nu, rho for each material |
| Properties | PSHELL, PCOMP, PBAR cards — thicknesses, layups, cross-sections |
| Loads | FORCE, MOMENT, PLOAD cards — applied loads and load cases |
| Constraints | SPC cards — boundary conditions and enforced displacements |

## Version Control

| # | Snapshot Tag | Files | What happened |
|---|-------------|-------|---------------|
| 1 | `initial-upload` / `baseline` | 1 | Raw .bdf uploaded |
| 2 | `post-extraction` | ~5+ | BDF + extracted FEM data artifacts |

## What's Next?

- **Run simulation** — use the NASTRAN solver integration to run the model and get `.op2` results
- **Extract results** — use Paraview integration to extract data from result files
- **Compare models** — upload a modified BDF, re-extract, and compare across versions

## Try It

Run the notebook: [`extract_nastran_model.ipynb`](extract_nastran_model.ipynb)

See [`example-input/`](example-input/) for the source BDF file and [`example-output/`](example-output/) for pre-computed results.
