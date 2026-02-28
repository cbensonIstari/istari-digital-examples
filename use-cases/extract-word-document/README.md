# Use Case: Extract a Word Document

## Intent

I have a Word `.docx` file — a report, specification, or technical document — and I want the text, embedded images, and tables extracted as separate files without opening Word. Upload the file to Istari, run extraction, get structured content automatically.

## Tools Used

| Tool | Role |
|------|------|
| **Istari Platform** | Outer loop — stores the document, runs extraction, hosts artifacts, shares with team |
| **Microsoft Word** (`@istari:extract` via `microsoft_office_word` 2021) | Inner loop — opens the .docx, extracts full text, individual paragraphs, embedded images, and table snapshots |

## Inner / Outer Loop

```
+--- Outer Loop: Istari -- store - extract - view - share ------+
|                                                                 |
|   +- Microsoft Word (inner loop) ---------+                   |
|   | Open .docx -> extract full text,      |                    |
|   | split paragraphs, export images,      |                    |
|   | capture tables as JPEG                |                    |
|   +------------------+-------------------+                     |
|                      |                                          |
|                      v                                          |
|   all_text.txt - paragraphs - images - table snapshots          |
+-----------------------------------------------------------------+
```

The **inner loop** (Word) does the domain-specific work — opening the native .docx, extracting the full document text, splitting into individual paragraphs, exporting embedded images at full resolution, and capturing tables as JPEG snapshots. The **outer loop** (Istari) handles everything else — storing the document, running the extraction as a tracked job on a Windows agent, hosting the artifacts, and versioning.

## K-Script

| Step | Interaction / Process | Unobservable Actions or Assumptions |
|------|----------------------|-------------------------------------|
| 1 | **Engineer:** Uploads a `.docx` file to Istari | Document contains text, images, and/or tables |
| 2 | **Engineer:** Runs `@istari:extract` on the document | Job is matched to an agent running Word 2021 on Windows Server 2022 |
| 3 | **System:** Agent opens the document in Word | Reads all paragraphs, embedded objects, tables |
| 4 | **System:** Agent extracts full text and individual paragraphs | Each paragraph saved as a separate .txt file |
| 5 | **System:** Agent exports embedded images and table snapshots | Images at original resolution; tables as JPEG captures |
| 6 | **System:** Job completes; 26 artifacts appear | Full text, paragraph files, images, table snapshots |
| 7 | **Engineer:** Views `all_text.txt` for the complete document text | Searchable plain text without Word formatting |
| 8 | **Engineer:** Views extracted images and tables separately | Individual artifacts for each embedded object |
| 9 | **Engineer:** Snapshots the results for the team | Point-in-time capture of the document + all extraction artifacts |

## Expected Results

Running extraction on `100KB_DOCX.docx` (101.2 KB) produces 26 artifacts:

| Artifact | Format | Size | Description |
|----------|--------|------|-------------|
| `all_text.txt` | TXT | 5.6 KB | Complete document text |
| `document.docx` | DOCX | 97.9 KB | Processed document copy |
| 20 `Par-*.txt` files | TXT | 0.0 - 0.7 KB each | Individual paragraphs |
| `image1.jpeg` | JPEG | 80.3 KB | Embedded image |
| `Table-1.jpeg` | JPEG | 14.2 KB | Table 1 snapshot |
| `Table-2.jpeg` | JPEG | 14.2 KB | Table 2 snapshot |

## Version Control

| # | Snapshot Tag | Files | What happened |
|---|-------------|-------|---------------|
| 1 | `initial-upload` / `baseline` | 1 | Raw .docx uploaded |
| 2 | `post-extraction` | 27 | DOCX + 26 extraction artifacts (text, paragraphs, images, tables) |

## Try It

Run the notebook: [`extract_word.ipynb`](extract_word.ipynb)

See [`example-input/`](example-input/) for the source DOCX file and [`example-output/`](example-output/) for pre-computed results.
