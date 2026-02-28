# Use Case: Extract a PDF Document

## Intent

I have an engineering PDF — a drawing, spec sheet, or technical document — and I want structured text, sections, and semantic chunks without manually copying content. Upload the PDF to Istari, run extraction, get structured data automatically.

## Tools Used

| Tool | Role |
|------|------|
| **Istari Platform** | Outer loop — stores the document, runs extraction, hosts artifacts, shares with team |
| **PDF Extractor** (`@istari:extract` via `open_pdf` v1.0.0) | Inner loop — parses PDF structure, extracts text, sections, semantic chunks, and OCR data |

## Inner / Outer Loop

```
+--- Outer Loop: Istari -- store - extract - view - share ------+
|                                                                 |
|   +- PDF Extractor (inner loop) ----------+                    |
|   | Parse PDF -> extract text, sections,  |                    |
|   | chunks, OCR, metadata -> HTML render  |                    |
|   +------------------+-------------------+                     |
|                      |                                          |
|                      v                                          |
|   text.txt - sections JSON - chunks JSON - metadata - HTML      |
+-----------------------------------------------------------------+
```

The **inner loop** (PDF Extractor) does the domain-specific work — parsing the PDF structure, extracting raw text, identifying document sections, creating semantic chunks suitable for search/RAG, running OCR on image-based content, and generating an HTML rendition. The **outer loop** (Istari) handles everything else — storing the document, running the extraction as a tracked job on a Linux agent, hosting the artifacts, and versioning.

## K-Script

| Step | Interaction / Process | Unobservable Actions or Assumptions |
|------|----------------------|-------------------------------------|
| 1 | **Engineer:** Uploads a PDF to Istari | Could be a drawing, spec sheet, report, or patent |
| 2 | **Engineer:** Runs `@istari:extract` on the PDF | Job is matched to an agent running open_pdf v1.0.0 on Ubuntu 22.04 |
| 3 | **System:** Agent parses the PDF structure | Extracts text layers, identifies sections, runs OCR on images |
| 4 | **System:** Agent creates semantic chunks for search | Text split into meaningful segments with structural metadata |
| 5 | **System:** Job completes; 10 artifacts appear | Structured text, sections, chunks, metadata, HTML |
| 6 | **Engineer:** Views sections to understand document structure | Hierarchical breakdown without opening the PDF |
| 7 | **Engineer:** Uses semantic chunks for search or RAG integration | Pre-chunked text ready for vector databases or LLM context |
| 8 | **Engineer:** Snapshots the results for the team | Point-in-time capture of the PDF + all extraction artifacts |

## Expected Results

Running extraction on `BRACKET_v2.2.pdf` (85.2 KB) produces 10 artifacts:

| Artifact | Format | Size | Description |
|----------|--------|------|-------------|
| `text.txt` | TXT | 0.0 KB | Raw extracted text |
| `text_sections.json` | JSON | 1.1 KB | Document sections with hierarchy |
| `json_sections.json` | JSON | 1.1 KB | Sections as structured JSON |
| `smart_chunks.json` | JSON | 1.4 KB | Intelligently chunked text segments |
| `semantic_chunks.json` | JSON | 1.4 KB | Semantic chunks for RAG/search |
| `metadata.json` | JSON | 0.2 KB | Document metadata (author, dates, etc.) |
| `text_with_OCR.json` | JSON | 0.3 KB | OCR-enhanced text extraction |
| `docling_text.json` | JSON | 607.4 KB | Full structured document representation |
| `document.html` | HTML | 1.4 KB | HTML rendition of the document |
| `document.pdf` | PDF | 85.2 KB | Processed PDF copy |

## Version Control

| # | Snapshot Tag | Files | What happened |
|---|-------------|-------|---------------|
| 1 | `initial-upload` / `baseline` | 1 | Raw PDF uploaded |
| 2 | `post-extraction` | 11 | PDF + 10 extraction artifacts |

## Try It

Run the notebook: [`extract_pdf.ipynb`](extract_pdf.ipynb)

See [`example-input/`](example-input/) for the source PDF file and [`example-output/`](example-output/) for pre-computed results.
