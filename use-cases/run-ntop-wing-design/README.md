# Use Case: Run an nTop Wing Design

## Intent

I have a parametric wing model in nTopology and I want to run it with specific design parameters — sweep angles, span, length — then see the resulting geometry, aerodynamic metrics, and rendered views. I want to do this without opening nTop locally, and I want the outputs versioned in Istari so I can compare across runs.

## Tools Used

| Tool | Role |
|------|------|
| **Istari Platform** | Outer loop — stores the model, submits jobs, hosts artifacts, tracks versions across runs |
| **nTopology** (`@ntop:run_model` via `ntopcl`) | Inner loop — parametric geometry engine that generates wing geometry, mesh, and aerodeck metrics |

## Inner / Outer Loop

```
┌─── Outer Loop: Istari ── store · run · version · compare ──┐
│                                                              │
│   ┌─ nTopology (inner loop) ─────────────────────────────┐   │
│   │ Load wing model → apply parameters → generate geom   │   │
│   │ → export mesh → compute aerodeck metrics              │   │
│   └──────────────────────────┬────────────────────────────┘   │
│                              │                                │
│                              ↓                                │
│   .ntop model · .obj mesh · aerodeck metrics · 7 view PNGs   │
└───────────────────────────────────────────────────────────────┘
```

The **inner loop** (nTopology) does the domain-specific geometry work — interpreting sweep angles, generating the wing surface, meshing for export, and computing aerodynamic performance. The **outer loop** (Istari) handles storage, job orchestration, and versioning — so you can run three different parameter sets and compare them all from one place.

## K-Script

| Step | Interaction / Process | Unobservable Actions or Assumptions |
|------|----------------------|-------------------------------------|
| 1 | **Engineer:** Opens Istari, navigates to the "AI_Native_CAD_with_nTop" system | System contains the Group3-UAS-Wing-v8 parametric nTop model |
| 2 | **Engineer:** Selects the .ntop model file and clicks "Run Function" → `run_model` | Function is registered for .ntop files; ntopcl v5.30 is the configured tool |
| 3 | **Engineer:** Enters wing parameters — LOA: 99.9", Span: 144", LE Sweep: 46°/46°, TE Sweep: -46°/15°, Panel Break: 0.30 | Parameters are passed as JSON; the nTop model has named inputs matching these fields |
| 4 | **System:** Queues the job and assigns it to an agent running ntopcl on RHEL 8 | The agent has nTopology command-line tools installed; job includes the input JSON as a parameter |
| 5 | **System:** nTop loads the parametric model, applies the parameter values, regenerates geometry | The wing surface, internal structure, and mesh are all recomputed from the parameter set |
| 6 | **System:** nTop exports artifacts — updated .ntop model, .obj mesh, aerodeck metrics JSON, interactive HTML report, output summary, and 7 rendered PNG views | Views: top, front, back, left, right, bottom, isometric. Aerodeck metrics include structure weight, range, cruise speed |
| 7 | **System:** Job completes; 14 artifacts appear on the model | Each run adds a new set of artifacts; previous run artifacts are preserved |
| 8 | **Engineer:** Clicks on the isometric view PNG to see the wing shape | Rendered view shows the 3D wing geometry from the iso camera angle |
| 9 | **Engineer:** Opens `aerodeck_metrics.json` to check performance | Contains structure weight (composite + metal), range in nm, cruise speed in knots, and other metrics |
| 10 | **Engineer:** Compares weight against the 275 lb requirement — "Am I under budget?" | This connects nTop geometry outputs back to the SysML requirements |
| 11 | **Engineer:** Wants to try a longer-span wing → modifies parameters: Span: 168", LE Sweep: 30°/20°, Panel Break: 0.55 | Different parameter sets explore the design space; each run is tracked separately |
| 12 | **Engineer:** Runs again with new parameters | Second set of 14 artifacts is added; both runs' outputs coexist on the model |
| 13 | **Engineer:** Compares aerodeck metrics between Run 1 and Run 2 side by side | Istari preserves all artifacts with their source job references |
| 14 | **Engineer:** Likes Run 2 → promotes its output .ntop as a new formal revision of the model | `client.update_model()` creates a new revision on the same file_id — enables diff view in Istari UI |
| 15 | **Engineer:** Shares the system with a teammate to review the design | Teammate can see all runs, all artifacts, and the version history |

## Expected Results

Running the default parameters (LOA 99.9", Span 144", LE Sweep 46°/46°, TE Sweep -46°/15°, Panel Break 0.30) produces 14 artifacts:

| Artifact | Size | Description |
|----------|------|-------------|
| `Group3-UAS-Wing-v8(2).ntop` | ~31 MB | Updated nTop model with computed geometry |
| `grp3-uas_v6.obj` | ~5.6 MB | 3D mesh export for visualization/analysis |
| `grp3-uas_v6_aerodeck_metrics.json` | 4.3 KB | Aerodynamic performance metrics |
| `grp3-uas_v6_aerodeck.html` | 122 KB | Interactive aerodeck report |
| `output.json` | ~350 B | Run output summary |
| `grp3-uas_v6_output.json` | ~150 B | Additional output data |
| `grp3-uas_v6_aerodeck.json` | ~9 KB | Full aerodeck data |
| 7 view PNGs | 30-130 KB each | top, front, back, left, right, bottom, iso |

### Aerodeck Metrics (example)

| Metric | Value |
|--------|-------|
| MTOW | 479.0 lb |
| Empty weight | 321.8 lb |
| Fuel weight | 157.2 lb (32.8% fuel fraction) |
| Wing area | 49.6 ft² |
| Wingspan | 12.0 ft |
| Aspect ratio | 2.90 |
| Wing loading | 9.66 lb/ft² |
| L/D max | 23.64 at 2.0° AoA |
| Range | 2,312 nm at 175 kts cruise |
| Cruise time | 13.2 hr |
| Loiter time | 12.0 hr |
| Total endurance | 25.5 hr |
| Static margin | 2.08% |
| Overall stability | ✅ All axes stable and damped |

See [`example-output/`](example-output/) for the full JSON files, rendered views, and aerodeck HTML report.

### Parameters Reference

| Parameter | Units | Default | Description |
|-----------|-------|---------|-------------|
| LOA In | inches | 99.9 | Overall length of aircraft |
| Span | inches | 144 | Wingspan |
| LE Sweep P1 | degrees | 46 | Leading edge sweep, inboard panel |
| LE Sweep P2 | degrees | 46 | Leading edge sweep, outboard panel |
| TE Sweep P1 | degrees | -46 | Trailing edge sweep, inboard panel |
| TE Sweep P2 | degrees | 15 | Trailing edge sweep, outboard panel |
| Panel Break Span % | — | 0.30 | Spanwise location of panel break |

## Try It

Run the notebook: [`run_ntop_wing_design.ipynb`](run_ntop_wing_design.ipynb)

Or from the command line:

```bash
python ntop/run_ntop_model.py --model-id 063a1593-6fad-4dd9-b963-f0c8bf4119a1
```
