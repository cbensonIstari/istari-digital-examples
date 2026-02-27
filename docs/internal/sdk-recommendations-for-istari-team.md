# SDK Recommendations for the Istari Engineering Team

Hey team! After building out these example notebooks and getting-started scripts using `istari-digital-client` v10.7.0, I ran into a few things that tripped me up. Nothing major — the SDK works well overall — but these are spots where a small change could save the next person (or AI assistant) a lot of head-scratching.

Each item below includes the specific friction, a code example showing what happened, and a suggestion.

---

## 1. `list_system_configurations()` vs the expected `list_configurations()`

**What happened:** I instinctively called `client.list_configurations(system_id)` — which doesn't exist. The actual method is `client.list_system_configurations(system_id)`.

```python
# What I tried (fails with AttributeError):
configs = client.list_configurations(system_id, page=1, size=50)

# What works:
configs = client.list_system_configurations(system_id, page=1, size=50)
```

**Suggestion:** Either add `list_configurations` as an alias, or at minimum document the full method name prominently. Every other resource uses the pattern `list_{resource}()` — `list_models()`, `list_snapshots()`, `list_tags()` — so `list_system_configurations` breaks the convention.

---

## 2. `system.name` vs `model.display_name` — different attribute for the same concept

**What happened:** System uses `.name` for its human-readable label. Model uses `.display_name`. I kept reaching for `system.display_name` (which doesn't exist) and `model.name` (which also doesn't exist).

```python
# System:
print(system.name)           # works
print(system.display_name)   # AttributeError

# Model:
print(model.display_name)    # works
print(model.name)            # AttributeError
```

**Suggestion:** Unify on one attribute name across all resource types, or at least add the other as an alias. Having both `.name` and `.display_name` on all objects (even if one is computed) would eliminate this confusion entirely.

---

## 3. `SnapshotItem.file_revision_id` exists but `.file_revision` does not

**What happened:** When iterating snapshot items, I expected to access the file revision object directly. Instead, `SnapshotItem` only has `file_revision_id` — a bare UUID. To get the actual file name and size, I had to discover `list_snapshot_revisions()` as a separate call.

```python
# What I expected to work:
items = client.list_snapshot_items(snapshot_id)
for item in items.items:
    print(item.file_revision.name)  # AttributeError — no .file_revision

# What actually works:
revs = client.list_snapshot_revisions(snapshot_id, page=1, size=50)
for rev in revs.items:
    print(rev.name, rev.size)  # These are FileRevision objects
```

**Suggestion:** Either eagerly load the `file_revision` object on `SnapshotItem`, or make `list_snapshot_revisions()` the clearly documented primary way to get file details for a snapshot. Right now it feels hidden.

---

## 4. `ResponseCreateSnapshot` — polymorphic return type is confusing

**What happened:** `client.create_snapshot()` returns a `ResponseCreateSnapshot`, which wraps either a `Snapshot`, a `DryRunSnapshot`, or a `NoOpResponse`. You have to call `.actual_instance` and then check what type you got back.

```python
response = client.create_snapshot(config_id, NewSnapshot())
snapshot = response.actual_instance

# Is this a Snapshot or a NoOpResponse? Only one way to find out:
if hasattr(snapshot, "id"):
    # It's a real Snapshot
    snapshot_id = snapshot.id
else:
    # It's a NoOpResponse — no new snapshot was created
    # Now you have to go find the existing one
    snaps = client.list_snapshots(configuration_id=config_id, page=1, size=1)
    snapshot_id = snaps.items[0].id
```

**Suggestion:** Consider returning the snapshot directly in the NoOp case too (the existing unchanged snapshot), or at least include its ID in the `NoOpResponse`. Having to handle three possible types from one method is unusual for a CRUD API. At minimum, document what triggers each return type.

---

## 5. `NoOpResponse` when creating snapshots — undocumented behavior

**What happened:** When I created a configuration with tracked files, Istari automatically created a snapshot behind the scenes. When I then called `create_snapshot()` myself, I got a `NoOpResponse` instead of a `Snapshot` — because nothing had changed since the auto-created snapshot.

This isn't documented anywhere. I only figured it out by inspecting the response type.

**Suggestion:** Add a note in the `create_snapshot()` docs: "Returns `NoOpResponse` if no tracked files have changed since the last snapshot." Even better: include the existing snapshot's ID in the NoOp so the caller can find it without a separate query.

---

## 6. Pagination starts at page 1 — fails silently at page 0

**What happened:** Most APIs I've used are 0-indexed. I started with `page=0` and got back empty results with no error. Took a while to realize `page` starts at 1.

```python
# Returns empty results (no error, just... nothing):
client.list_systems(page=0, size=20)  # .items is []

# What works:
client.list_systems(page=1, size=20)  # .items has data
```

**Suggestion:** Either raise a `ValueError` for `page=0`, or accept 0-indexed pages. Silently returning empty results for an invalid page number is a subtle bug factory.

---

## 7. `list_snapshot_revisions()` isn't in the API documentation

**What happened:** This method is critical for getting file names and sizes from a snapshot. But I couldn't find it in the docs — I only discovered it by running `dir(client)` and guessing. It's the complement to `list_snapshot_items()` but much more useful.

**Suggestion:** Add `list_snapshot_revisions()` to the official API documentation, ideally right next to `list_snapshots()` and `list_snapshot_items()`. It's arguably the most useful of the three for displaying snapshot contents.

---

## 8. `archive_status` uses lowercase strings instead of an enum

**What happened:** The archive status values are lowercase strings (`'active'`, `'archived'`, `'all'`). This isn't obvious, and I initially tried `'Active'` and `'ACTIVE'` before finding the right format.

```python
# These fail (no error, just wrong results):
client.list_systems(archive_status='Active')
client.list_systems(archive_status='ACTIVE')

# What works:
client.list_systems(archive_status='active')
```

**Suggestion:** Use an enum like `ArchiveStatus.ACTIVE` for type safety and discoverability. The SDK already uses enums for other things (`TrackedFileSpecifierType`, `JobStatusName`, `AccessRelation`) — this one was just missed.

---

## 9. `NewSnapshot` only accepts `dry_run` — no way to add a description

**What happened:** When creating snapshots, I wanted to add a description ("post-extraction snapshot") or a name. But `NewSnapshot` only has a single optional field: `dry_run`.

```python
# The only field available:
NewSnapshot(dry_run=False)

# What I wished I could do:
NewSnapshot(description="Captured after SysGit extraction", name="v1.0")
```

**Suggestion:** Add `description` and/or `name` fields to `NewSnapshot`. Snapshots are meant to be milestones — being able to describe them when created (not just via tags after the fact) would make the version history much more readable.

---

## 10. No snapshot comparison API

**What happened:** After creating two snapshots (pre-extraction and post-extraction), I wanted to show what changed between them. There's no `compare_snapshots()` or `diff_snapshots()` method, so I had to manually list files in both and diff them.

```python
# What I had to do:
revs_before = client.list_snapshot_revisions(snap1_id, page=1, size=50)
revs_after = client.list_snapshot_revisions(snap2_id, page=1, size=50)
before_names = {r.name for r in revs_before.items}
after_names = {r.name for r in revs_after.items}
added = after_names - before_names
print(f"New files: {added}")
```

**Suggestion:** Add a `compare_snapshots(snapshot_id_1, snapshot_id_2)` method that returns added, removed, and modified files. This is one of the most valuable features of version control — "what changed?" — and it should be a first-class API.

---

## 11. Tag uniqueness isn't enforced — duplicate tags are silently created

**What happened:** I accidentally created the same tag twice on a snapshot. No error was raised — it just created a duplicate.

```python
client.create_tag(snapshot_id, NewSnapshotTag(tag="v1.0"))
client.create_tag(snapshot_id, NewSnapshotTag(tag="v1.0"))  # No error!

tags = client.list_tags(snapshot_id=snapshot_id)
# Now there are 2 tags both named "v1.0"
```

**Suggestion:** Either enforce uniqueness (return the existing tag or raise an error) or document that tags are not unique. If tags can appear on multiple snapshots, that's fine — but duplicates on the *same* snapshot seems like it should be prevented.

---

## 12. No `get_configuration()` by ID

**What happened:** I had a configuration ID but couldn't fetch it directly. The only way to get a configuration object is to list all configurations for a system and filter.

```python
# What I expected:
config = client.get_configuration(config_id)  # doesn't exist

# What I had to do:
configs = client.list_system_configurations(system_id, page=1, size=50)
config = next(c for c in configs.items if c.id == config_id)
```

**Suggestion:** Add `get_configuration(config_id)` or `get_system_configuration(config_id)` for direct lookup. Most resources have a `get_*()` method — configurations are an exception.

---

## 13. `add_job()` parameter naming varies by tool

**What happened:** The `parameters` dict for `add_job()` uses different top-level keys depending on which tool you're calling. For SysGit it's just `{}`, but for nTop it's `{"ntop_input_json": input_data}`. There's no documentation on what key each tool expects.

```python
# SysGit — no parameters needed:
client.add_job(model_id, "@istari:extract_sysmlv2", "sysgit", "0.1.8", "Ubuntu 22.04", parameters={})

# nTop — requires specific key "ntop_input_json":
client.add_job(model_id, "@ntop:run_model", "ntopcl", "5.30", "RHEL 8",
               parameters={"ntop_input_json": input_data})
```

**Suggestion:** Document the expected `parameters` schema for each function/tool combination. Even a simple table in the docs would help: "For `@ntop:run_model`, pass `{'ntop_input_json': {...}}`."

---

## 14. `model.artifacts` returns all artifacts — no way to filter by job or run

**What happened:** After running nTop twice, the model accumulated 28 artifacts (14 per run). There's no way to tell which artifacts came from which job run, so I had to use filename matching and reverse iteration to find the "most recent" set.

```python
# Returns ALL artifacts, ever:
model = client.get_model(model_id)
all_artifacts = model.artifacts  # 28 artifacts from 2 runs

# What I wished I could do:
recent_artifacts = client.list_artifacts(model_id, job_id=job.id)
```

**Suggestion:** Add a way to query artifacts by job ID, or include the source job ID on each artifact. This would make it easy to display "results from this specific run" instead of "all results ever."

---

## 15. No webhook or callback for job completion — forced to poll

**What happened:** Job execution takes 1-8 minutes depending on the tool. The only way to know when it's done is to poll `client.get_job(job_id)` in a loop.

```python
# The polling pattern used in every notebook:
while True:
    sleep(10)
    job = client.get_job(job.id)
    if job.status.name in {JobStatusName.COMPLETED, JobStatusName.FAILED}:
        break
```

This works fine for notebooks, but it's not great for production integrations.

**Suggestion:** Add webhook support (POST to a URL on completion) or a streaming/long-poll endpoint. Even an async `await client.wait_for_job(job_id, timeout=600)` helper in the SDK would be a nice quality-of-life improvement.

---

## Overall

The SDK does its job well — these are refinements, not blockers. The version control model (system → configuration → snapshot → tag) is genuinely powerful once you understand it. These suggestions would just make it easier for the next person to reach that understanding faster.

Thanks for building this!
