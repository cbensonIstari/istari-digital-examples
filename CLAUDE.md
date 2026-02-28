# Helpful Hints for AI

Context for AI assistants (Claude, Copilot, etc.) working with this repo.

## Istari Platform

| Resource | URL |
|----------|-----|
| SDK Documentation | https://docs.istaridigital.com/developers/SDK/setup |
| Integration Basics | https://docs.istaridigital.com/integrations/integration_basics |
| Registry API | https://fileservice-v2.demo.istari.app |
| Web UI | https://demo.istari.app |
| Public Repos | https://github.com/cbensonIstari/ |

## URL Structure

Istari UI URLs follow this pattern:

```
https://demo.istari.app/systems/{system_id}                    ← System overview
https://demo.istari.app/systems/{system_id}/config/{config_id} ← Configuration view
https://demo.istari.app/files/{model_id}                       ← Model/file detail
https://demo.istari.app/files/{model_id}/artifact/{artifact_id}/{revision_id} ← Artifact deep link
https://demo.istari.app/jobs/                                  ← Job list
```

## Systems in This Repo

Each use case has its own Istari system:

| Use Case | System Name | System ID |
|----------|-------------|-----------|
| Explore SysML Model | Example: Explore SysML Model | `c61e33e7-e14d-458e-8c82-7c8148c1a643` |
| nTop Wing Design | Example: nTop Wing Design | `91cde24e-8343-44ba-8b8f-67dc6e9e5334` |
| Check Design Meets Requirements | Example: Check Design Meets Requirements | `294568b3-e626-4293-8e2c-307370ec9e95` |
| Extract CATIA V5 Part | Example: Extract CATIA V5 Part | `55726539-5956-447b-8d46-da67aca7ccbe` |
| Extract NASTRAN Model | Example: Extract NASTRAN Model | `41455388-982a-4078-ab6a-2e020a44bb98` |
| Extract Creo Part | Example: Extract Creo Part | `ba171228-1c49-46c8-b502-cbcedbac77bc` |
| Extract Cameo Model | Example: Extract Cameo Model | `b3450e9e-d350-4940-a557-495f7efc9242` |
| Extract PDF | Example: Extract PDF | `94a23774-633b-46ed-9c55-1431649ac898` |
| Extract Excel Spreadsheet | Example: Extract Excel Spreadsheet | `1c72d423-918c-4231-afd8-d1a5825026f2` |
| Extract Word Document | Example: Extract Word Document | `df00ca2e-8295-401a-9e6c-ee46241d15c8` |
| Extract PowerPoint | Example: Extract PowerPoint | `ff748bc2-7a66-4102-93f9-d5a554da6c1a` |

## Model IDs

| Model | ID | Used By |
|-------|----|---------|
| Group3 UAS Requirements (Explore) | `85b78395-9c09-4047-ad2a-7e2aa444b389` | Use Case 1 |
| Group3-UAS-Wing-v8 (nTop) | `263b7332-03f4-4ded-9686-7f11df478058` | Use Case 2, Use Case 3 |
| Group3 UAS Requirements (Compliance) | `c4280a27-b2e4-4376-81f7-474062bcdf4d` | Use Case 3 |
| Bracket.CATPart (CATIA V5) | `0e035383-3a51-48fa-8682-29213dda65ab` | Use Case 4 |
| Aircraft-One_DEMO.bdf (NASTRAN) | `77445b89-a9f2-4e8c-86ac-14962d5f36b3` | Use Case 5 |
| gearcase.prt (Creo) | `2f337779-e564-430c-bb89-37b1b6528410` | Use Case 6 |
| Istari_UAVOne.mdzip (Cameo) | `1fbd8f81-c4f7-4e4f-9140-e5004cf0fcf8` | Use Case 7 |
| BRACKET_v2.2.pdf (PDF) | `f6804715-ec11-4ba2-847b-93be0f72e03f` | Use Case 8 |
| IstariOne UAV Specs.xlsx (Excel) | `2dee52b0-ec79-4c23-a8a5-af5823dbbdc4` | Use Case 9 |
| 100KB_DOCX.docx (Word) | `42623b64-26eb-47b6-b562-53a1cd62189c` | Use Case 10 |
| PPT_500KB_PPTX.pptx (PowerPoint) | `82d6a6e9-7922-4226-a846-087200eb4a5d` | Use Case 11 |

## SDK Quick Reference

```python
from istari_client import get_client

client = get_client()  # uses .env credentials

# Core operations
client.list_systems()                    # → PageSystem (.items, .total)
client.get_system(system_id)             # → System
client.create_system(NewSystem(...))     # → System
client.get_model(model_id)              # → Model
client.add_model(path=file_path)        # → Model (upload new)
client.update_model(model_id, path)     # → Model (new revision)
model.read_text()                       # → str (file content)
model.read_bytes()                      # → bytes
model.read_json()                       # → dict
model.artifacts                         # → list[Artifact]

# Jobs
client.add_job(model_id, function, tool_name, tool_version, operating_system, parameters)
client.get_job(job_id)                  # → Job (poll status)
# JobStatusName: PENDING, VALIDATING, RUNNING, UPLOADING, COMPLETED, FAILED

# Pagination starts at page=1, use .items not .content

# Attribute naming
# System: .name (NOT .display_name)
# Model:  .display_name (computed from file)
# Config: .name
# User:   .display_name, .email
```

## Version Control — Istari's Core Value

Istari is a **version control system for engineering models**. Every file, every revision, every milestone is tracked.

### System Hierarchy

```
System                              ← Top-level project container
└── Configuration                   ← Logical grouping (e.g. "Baseline", "High Endurance")
    ├── TrackedFile                  ← File being tracked (LATEST or LOCKED)
    └── Snapshot                    ← Immutable point-in-time capture
        ├── SnapshotItem → FileRevision  ← Exact file contents at that moment
        └── Tag                     ← Human-readable name ("v1.0", "post-extraction")
```

### Core Concepts

| Concept | What It Does | Analogy |
|---------|-------------|---------|
| **File Revision** | Each `update_model()` creates a new revision on the same file | Like a git commit |
| **Configuration** | Groups tracked files into a logical variant | Like a git branch |
| **Tracked File (LATEST)** | Auto-follows newest revision — changes propagate | Like `HEAD` |
| **Tracked File (LOCKED)** | Pinned to a specific revision — reproducible | Like a pinned dependency |
| **Snapshot** | Immutable capture of all tracked files at a point in time | Like a git tag |
| **Tag** | Human-readable name for a snapshot | The tag label itself |

### Version Control SDK Methods

```python
from istari_digital_client import (
    NewSystem, NewSystemConfiguration, NewTrackedFile,
    TrackedFileSpecifierType, NewSnapshot, NewSnapshotTag,
)

# Create and organize
client.create_system(NewSystem(name=..., description=...))
client.create_configuration(system_id, NewSystemConfiguration(
    name="Baseline",
    tracked_files=[NewTrackedFile(
        specifier_type=TrackedFileSpecifierType.LATEST,  # or LOCKED
        file_id=model.file.id,
        # pinned_file_revision_id=rev.id,  # only for LOCKED
    )]
))

# Snapshot and tag
snap = client.create_snapshot(config_id, NewSnapshot())
# Returns ResponseCreateSnapshot — use .actual_instance to get Snapshot or NoOpResponse
snapshot = snap.actual_instance
client.create_tag(snapshot.id, NewSnapshotTag(tag="v1.0"))

# Navigate the hierarchy
client.list_system_configurations(system_id, page=1, size=50)   # → PageSystemConfiguration
client.list_tracked_files(config_id, page=1, size=50)    # → PageTrackedFile
client.list_snapshots(configuration_id=config_id)         # → PageSnapshot
client.list_snapshot_revisions(snapshot_id)               # → files in snapshot
client.list_tags(snapshot_id=snapshot_id)                 # → tags on snapshot

# Version a file (creates new revision)
client.update_model(model_id, path, version_name="v2", description="Updated range to 1500nm")
```

### Typical Workflow

```
Upload model ──→ Track in config ──→ Run job ──→ Snapshot ──→ Tag
     │                                                          │
     │         Update model (new revision) ──→ Snapshot again   │
     │                                              │           │
     └──────── Compare snapshots to see what changed ──────────┘
```

## Inner Loop / Outer Loop Pattern

- **Inner loop** = domain-specific tool (nTop for CAD, SysGit for SysML, Luminary for CFD)
- **Outer loop** = Istari (version, track, compare, share across tools)
- Each use case connects 1-3 inner loops through Istari's outer loop

## Key Integration Functions

| Function | Tool | OS | Purpose |
|----------|------|----|---------|
| `@istari:extract_sysmlv2` | `sysgit` v0.1.8 | Ubuntu 22.04 | Parse SysML → JSON + diagrams |
| `@ntop:run_model` | `ntopcl` v5.30 | RHEL 8 | Run parametric CAD → metrics + views |
| `@istari:extract` | `dassault_catia_v5` 6R2023 | Windows Server 2022 | Extract CATIA V5 part data → params, mass, views, OBJ |
| `@istari:extract_input` | `nastran_extract` v1.0.0 | Ubuntu 22.04 | Parse NASTRAN BDF → mesh, materials, loads |
| `@istari:extract` | `ptc_creo_parametric` v10.0.0.0 | Windows Server 2022 | Extract Creo part data → params, mass, views, OBJ |
| `@istari:extract` | `dassault_cameo` 2024x Refresh2 | Windows Server 2022 | Extract Cameo model → blocks, requirements, diagrams |
| `@istari:extract` | `open_pdf` v1.0.0 | Ubuntu 22.04 | Extract PDF → text, sections, chunks, metadata |
| `@istari:extract` | `microsoft_office_excel` 2021 | Windows Server 2022 | Extract Excel → CSV, charts, PDF render |
| `@istari:extract` | `microsoft_office_word` 2021 | Windows Server 2022 | Extract Word → text, paragraphs, images, tables |
| `@istari:extract` | `microsoft_office_powerpoint` 2021 | Windows Server 2022 | Extract PowerPoint → slides, text, PDF |
