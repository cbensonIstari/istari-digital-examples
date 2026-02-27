# Istari Digital SDK — Examples

Real-world examples of the [Istari Digital](https://www.istaridigital.com/) Python SDK, built from an actual engineering session on a Group 3 UAS wing design. Covers parametric CAD with nTopology, SysML v2 requirements with SysGit, model versioning, lineage tracking, and sharing.

## Inner Loop / Outer Loop

Engineering tools each have their own **inner loop** — the domain-specific work of designing geometry, writing requirements, or running simulations. Istari provides the **outer loop**: versioning model outputs, tracking lineage across tools, sharing with teammates, and connecting everything back to one system of record.

```
┌─── Outer Loop: Istari ── version · lineage · share · compare ────┐
│                                                                   │
│  ┌─ nTop ──────────┐  ┌─ SysGit ────────┐  ┌─ Luminary ──────┐  │
│  │ Design geometry  │  │ Write reqs      │  │ Set up mesh     │  │
│  │ Run parameters   │  │ Extract models  │  │ Run CFD         │  │
│  │ Export artifacts │  │ View hierarchy  │  │ Post-process    │  │
│  └────────┬─────────┘  └───────┬─────────┘  └───────┬─────────┘  │
│           │                    │                     │            │
│           ↓                    ↓                     ↓            │
├───────────────────────────────────────────────────────────────────┤
│            Versioned outputs tracked in one system                │
└───────────────────────────────────────────────────────────────────┘
```

Each integration in this repo is one folder. As new tools come online, they just add a folder.

## Quick Start

```bash
pip install istari-digital-client python-dotenv

# Copy and fill in your credentials
cp .env.example .env

# Verify your connection
python istari_client.py
# → Connected as: Your Name (you@example.com)
```

## Integrations

| Folder | Model Type | Tool | What It Does |
|--------|-----------|------|--------------|
| [`ntop/`](ntop/) | Geometry / CAD | nTopology | Run parametric wing designs, compare outputs across parameter sweeps |
| [`sysgit/`](sysgit/) | Requirements / MBSE | SysGit (SysML v2) | Download, edit, re-upload, and extract requirements models |
| *More coming* | CFD, FEA, ... | Luminary, ... | Same pattern — new folder, new inner loop |

## Common Workflows

The [`getting-started/`](getting-started/) folder covers SDK patterns that work across all tools:

| Script | What It Does |
|--------|-------------|
| [`01_explore_systems.py`](getting-started/01_explore_systems.py) | Browse systems, configurations, snapshots, and files |
| [`02_version_model.py`](getting-started/02_version_model.py) | Upload a job output as a new formal revision |
| [`03_share_resources.py`](getting-started/03_share_resources.py) | Share a system and its files with a teammate by email |

## Use Cases

End-to-end walkthroughs showing how engineers use Istari day-to-day. Each includes a [K-script](https://medium.com/@bladekotelly/k-scripts-the-fastest-and-most-flexible-way-to-articulate-a-user-experience-97264d9c4786) describing the user experience and a working notebook.

| Use Case | Question It Answers |
|----------|-------------------|
| [Understand My Requirements & Architecture](use-cases/explore-sysml-model/) | See what's inside a systems model — without being a SysML expert |
| [Test a New Wing Shape](use-cases/run-ntop-wing-design/) | Change wing parameters and see how it performs — without spinning up the nTop GUI |
| [Does My Design Meet Requirements?](use-cases/check-design-meets-requirements/) | Automatically check that requirements, architecture, and CAD all line up |

## Model Lineage

Three nTop runs with different wing parameters, tracked back to a single model with formal versioning:

![nTop Model Lineage](assets/ntop_lineage_chart.png)

See [`docs/model_lineage.md`](docs/model_lineage.md) for the full interactive Mermaid version.

## SDK Tips

| Gotcha | Details |
|--------|---------|
| Pagination starts at **1** | `page=1`, not `page=0` |
| Use `.items` | Not `.content` — `page.items` returns the list |
| Archive status is lowercase | `'active'`, `'archived'`, or `'all'` |
| Systems and files share separately | `create_access_by_email()` on the system, then on each file |
| `update_model()` creates a new revision | Same file_id, new revision — enables diff in the Istari UI |

## Links

- [Istari SDK Docs](https://docs.istaridigital.com/developers/SDK/setup)
- [Open Orchestra Mod-Sim DIDs](https://github.com/cbensonIstari/Open_Orchestra_Mod-Sim_DIDS) — the organizational philosophy behind this structure
