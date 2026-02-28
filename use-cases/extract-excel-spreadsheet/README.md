# Use Case: Extract an Excel Spreadsheet

## Intent

I have an Excel `.xlsx` file — a specifications list, trade study, or data sheet — and I want the data as CSV, the rendered layout as PDF, and structured worksheet metadata without opening Excel. Upload the file to Istari, run extraction, get everything automatically.

## Tools Used

| Tool | Role |
|------|------|
| **Istari Platform** | Outer loop — stores the spreadsheet, runs extraction, hosts artifacts, shares with team |
| **Microsoft Excel** (`@istari:extract` via `microsoft_office_excel` 2021) | Inner loop — opens the workbook, exports sheets as CSV, renders as PDF/HTML, extracts chart and named cell data |

## Inner / Outer Loop

```
+--- Outer Loop: Istari -- store - extract - view - share ------+
|                                                                 |
|   +- Microsoft Excel (inner loop) --------+                   |
|   | Open .xlsx -> export CSV per sheet,   |                    |
|   | render PDF, extract charts & named    |                    |
|   | cells, generate HTML workbook         |                    |
|   +------------------+-------------------+                     |
|                      |                                          |
|                      v                                          |
|   CSVs - worksheet JSON - chart JSON - PDF - HTML workbook      |
+-----------------------------------------------------------------+
```

The **inner loop** (Excel) does the domain-specific work — opening the native .xlsx workbook, exporting each sheet as CSV, rendering the formatted workbook as PDF and HTML, extracting chart data, and reading named cell references. The **outer loop** (Istari) handles everything else — storing the spreadsheet, running the extraction as a tracked job on a Windows agent, hosting the artifacts, and versioning.

## K-Script

| Step | Interaction / Process | Unobservable Actions or Assumptions |
|------|----------------------|-------------------------------------|
| 1 | **Engineer:** Uploads an `.xlsx` file to Istari | Spreadsheet contains specs, trade data, or analysis results |
| 2 | **Engineer:** Runs `@istari:extract` on the spreadsheet | Job is matched to an agent running Excel 2021 on Windows Server 2022 |
| 3 | **System:** Agent opens the workbook in Excel | Reads all sheets, charts, named ranges |
| 4 | **System:** Agent exports each sheet as CSV | Raw tabular data accessible without Excel |
| 5 | **System:** Agent renders the workbook as PDF and HTML | Formatted view preserving layout, fonts, colors |
| 6 | **System:** Job completes; 8 artifacts appear | CSVs, worksheet data JSON, chart JSON, named cells, PDF, HTML |
| 7 | **Engineer:** Views CSV data for programmatic access | Import into Python, MATLAB, or any analysis tool |
| 8 | **Engineer:** Views PDF for formatted layout | See the spreadsheet as the author intended |
| 9 | **Engineer:** Snapshots the results for the team | Point-in-time capture of the spreadsheet + all extraction artifacts |

## Expected Results

Running extraction on `IstariOne UAV Specifications List.xlsx` (14.4 KB) produces 8 artifacts:

| Artifact | Format | Size | Description |
|----------|--------|------|-------------|
| `Sheet1.csv` | CSV | 7.0 KB | Sheet 1 data as CSV |
| `Copy of Sheet1.csv` | CSV | 6.4 KB | Additional sheet export |
| `worksheet_data.json` | JSON | 0.2 KB | Worksheet metadata and structure |
| `chart_data.json` | JSON | 0.0 KB | Chart definitions (if any) |
| `named_cells.json` | JSON | 0.0 KB | Named cell references |
| `workbook.pdf` | PDF | 24.6 KB | Formatted render of the workbook |
| `workbook.xlsx` | XLSX | 17.9 KB | Processed workbook copy |
| `html_workbook.zip` | ZIP | 8.5 KB | Interactive HTML version |

## Version Control

| # | Snapshot Tag | Files | What happened |
|---|-------------|-------|---------------|
| 1 | `initial-upload` / `baseline` | 1 | Raw .xlsx uploaded |
| 2 | `post-extraction` | 9 | XLSX + 8 extraction artifacts (CSVs, JSON, PDF, HTML) |

## Try It

Run the notebook: [`extract_excel.ipynb`](extract_excel.ipynb)

See [`example-input/`](example-input/) for the source XLSX file and [`example-output/`](example-output/) for pre-computed results.
