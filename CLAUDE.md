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
| Explore SysML Model | Example: Explore SysML Model | `16ea4a85-cb3f-433a-8278-26eca07765a5` |
| nTop Wing Design | Example: nTop Wing Design | `91cde24e-8343-44ba-8b8f-67dc6e9e5334` |
| Check Design Meets Requirements | Example: Check Design Meets Requirements | `294568b3-e626-4293-8e2c-307370ec9e95` |

## Model IDs

| Model | ID | Used By |
|-------|----|---------|
| Group3 UAS Requirements (Explore) | `cdef0a6f-9457-4500-9a2a-62c6b1bf4039` | Use Case 1 |
| Group3-UAS-Wing-v8 (nTop) | `263b7332-03f4-4ded-9686-7f11df478058` | Use Case 2, Use Case 3 |
| Group3 UAS Requirements (Compliance) | `c4280a27-b2e4-4376-81f7-474062bcdf4d` | Use Case 3 |

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
