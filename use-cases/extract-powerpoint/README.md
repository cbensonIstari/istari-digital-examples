# Use Case: Extract a PowerPoint Presentation

## Intent

I have a PowerPoint `.pptx` file and I want individual slides, slide text, and the full deck as PDF — without opening PowerPoint. Upload the file to Istari, run extraction, get individual slides in multiple formats automatically.

## Tools Used

| Tool | Role |
|------|------|
| **Istari Platform** | Outer loop — stores the presentation, runs extraction, hosts artifacts, shares with team |
| **Microsoft PowerPoint** (`@istari:extract` via `microsoft_office_powerpoint` 2021) | Inner loop — opens the .pptx, splits into individual slides, exports as PDF/PNG, extracts text per slide |

## Inner / Outer Loop

```
+--- Outer Loop: Istari -- store - extract - view - share ------+
|                                                                 |
|   +- Microsoft PowerPoint (inner loop) ---+                   |
|   | Open .pptx -> split into slides ->    |                    |
|   | export each as PPTX/PDF/PNG ->        |                    |
|   | extract text per slide -> full PDF    |                    |
|   +------------------+-------------------+                     |
|                      |                                          |
|                      v                                          |
|   slide_N.pptx/pdf/png - slide_N_text.json - whole_deck.pdf    |
+-----------------------------------------------------------------+
```

The **inner loop** (PowerPoint) does the domain-specific work — opening the native .pptx, splitting the deck into individual slides, exporting each slide as PPTX (editable), PDF (printable), and PNG (viewable), extracting text content per slide as JSON, and generating a full-deck PDF and ODP. The **outer loop** (Istari) handles everything else — storing the presentation, running the extraction as a tracked job on a Windows agent, hosting the artifacts, and versioning.

## K-Script

| Step | Interaction / Process | Unobservable Actions or Assumptions |
|------|----------------------|-------------------------------------|
| 1 | **Engineer:** Uploads a `.pptx` file to Istari | Presentation with multiple slides |
| 2 | **Engineer:** Runs `@istari:extract` on the presentation | Job is matched to an agent running PowerPoint 2021 on Windows Server 2022 |
| 3 | **System:** Agent opens the presentation in PowerPoint | Reads all slides, text, embedded objects |
| 4 | **System:** Agent splits into individual slides | Each slide exported as separate PPTX, PDF, and PNG |
| 5 | **System:** Agent extracts text per slide and full-deck formats | Text as JSON; full deck as PDF and ODP |
| 6 | **System:** Job completes; 35 artifacts appear | Per-slide PPTX/PDF/PNG + text JSON, full deck PDF/ODP |
| 7 | **Engineer:** Views slide PNGs for a quick visual overview | See every slide without opening PowerPoint |
| 8 | **Engineer:** Uses slide text JSON for search or content analysis | Structured text per slide |
| 9 | **Engineer:** Downloads full-deck PDF for sharing | Universal format anyone can open |
| 10 | **Engineer:** Snapshots the results for the team | Point-in-time capture of the deck + all extraction artifacts |

## Expected Results

Running extraction on `PPT_500KB_PPTX.pptx` (500.2 KB, 8 slides) produces 35 artifacts:

| Artifact | Format | Size | Description |
|----------|--------|------|-------------|
| `whole_deck.pptx` | PPTX | 500.2 KB | Original deck copy |
| `whole_deck.pdf` | PDF | 152.3 KB | Full deck as PDF |
| `whole_deck.odp` | ODP | 588.1 KB | Full deck as ODP (LibreOffice) |
| `slide_1.pptx` through `slide_8.pptx` | PPTX | 74-482 KB | Individual slides (editable) |
| `slide_1.pdf` through `slide_8.pdf` | PDF | 21-76 KB | Individual slides (printable) |
| `slide_1.png` through `slide_8.png` | PNG | 23-300 KB | Individual slides (viewable) |
| `slide_1_text.json` through `slide_8_text.json` | JSON | 0.1-0.9 KB | Text content per slide |

## Version Control

| # | Snapshot Tag | Files | What happened |
|---|-------------|-------|---------------|
| 1 | `initial-upload` / `baseline` | 1 | Raw .pptx uploaded |
| 2 | `post-extraction` | 36 | PPTX + 35 extraction artifacts (per-slide exports, text, PDF, ODP) |

## Try It

Run the notebook: [`extract_powerpoint.ipynb`](extract_powerpoint.ipynb)

See [`example-input/`](example-input/) for the source PPTX file and [`example-output/`](example-output/) for pre-computed results.
