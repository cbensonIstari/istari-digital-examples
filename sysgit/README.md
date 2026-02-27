# SysGit Integration (SysML v2)

Manage SysML v2 requirements models via Istari's SysGit extraction engine.

## What It Does

The `update_and_extract_sysml.py` script demonstrates the full requirements workflow:

1. **Download** a SysML model from Istari
2. **Edit** a requirement value (e.g. update range from 1000nm to 1500nm)
3. **Re-upload** as a new revision (tracked with full history)
4. **Extract** via `@istari:extract_sysmlv2` to regenerate diagrams and structured data

## Usage

```bash
# Update a requirement and re-extract
python sysgit/update_and_extract_sysml.py \
    --model-id <MODEL_ID> \
    --find "1000" --replace "1500"

# Just run extraction on the current model (no edits)
python sysgit/update_and_extract_sysml.py \
    --model-id <MODEL_ID> \
    --extract-only
```

## Example: Group3 UAS Requirements

The included `group3_uas_requirements.sysml` defines a Group 3 expendable tailless flying wing UAV with:

- **Performance requirements**: range (1500nm), cruise speed (100kt), payload (125lb), structure weight (275lb max)
- **Safety requirements**: fail-safe return-to-home, battery monitoring
- **Part definitions**: heavy fuel engine, propulsion, power system, flight control, communications, payload, airframe
- **Requirement satisfaction**: parts traced to the requirements they satisfy

## Extraction Artifacts

After extraction, the model produces:

| Artifact | Description |
|----------|-------------|
| `output_requirements.json` | Structured requirements data |
| `requirements_hierarchy.png` | Visual requirements hierarchy |
| `output_parts.json` | Structured parts data |
| `parts_diagram.png` | Visual parts diagram |

## Job Config

| Setting | Value |
|---------|-------|
| Function | `@istari:extract_sysmlv2` |
| Tool | `sysgit` |
| Version | `0.1.8` |
| OS | `Ubuntu 22.04` |
