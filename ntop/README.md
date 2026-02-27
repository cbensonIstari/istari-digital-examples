# nTopology Integration

Run parametric CAD models via the [nTopology](https://www.ntop.com/) engine through Istari.

## What It Does

The `run_ntop_model.py` script submits a `@ntop:run_model` job with wing design parameters, polls until completion, and lists the resulting artifacts (updated `.ntop` file, `.obj` mesh, aerodeck metrics, view PNGs).

## Parameters

The wing is controlled by these inputs (see `v4_input.json`):

| Parameter | Units | Default | Description |
|-----------|-------|---------|-------------|
| LOA In | inches | 99.9 | Overall length of aircraft |
| Span | inches | 144 | Wingspan |
| LE Sweep P1 | degrees | 46 | Leading edge sweep, inboard panel |
| LE Sweep P2 | degrees | 46 | Leading edge sweep, outboard panel |
| TE Sweep P1 | degrees | -46 | Trailing edge sweep, inboard panel |
| TE Sweep P2 | degrees | 15 | Trailing edge sweep, outboard panel |
| Panel Break Span % | — | 0.30 | Spanwise location of panel break |

## Usage

```bash
# Run with default parameters
python ntop/run_ntop_model.py --model-id <YOUR_MODEL_ID>

# Run with a custom input file
python ntop/run_ntop_model.py --model-id <YOUR_MODEL_ID> --input my_params.json
```

## Example: Three Parameter Sweeps

| Run | LOA | Span | LE Sweep | TE Sweep | Panel Break |
|-----|-----|------|----------|----------|-------------|
| 1 — Original | 99.9" | 144" | 46°/46° | -46°/15° | 0.30 |
| 2 — Modified | 78" | 150" | 55°/35° | -30°/25° | 0.45 |
| 3 — High Endurance | 115" | 168" | 30°/20° | -20°/5° | 0.55 |

Each run produces ~14 artifacts: updated nTop model, OBJ mesh, aerodeck metrics JSON, interactive HTML report, output summary, and 7 rendered view PNGs.

## Versioning

After a run, you can promote its output as a formal new revision:

```bash
# Download the output .ntop, then re-upload as a new version
python getting-started/02_version_model.py \
    --model-id <MODEL_ID> \
    --file Group3-UAS-Wing-v8-run3.ntop \
    --name "v2 — High Endurance"
```

This creates a side-by-side diff view in the Istari UI between the original and updated geometry.

## Job Config

| Setting | Value |
|---------|-------|
| Function | `@ntop:run_model` |
| Tool | `ntopcl` |
| Version | `5.30` |
| OS | `RHEL 8` |
