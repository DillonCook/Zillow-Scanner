# padsplit_deal_scanner

`padsplit_deal_scanner` currently runs a focused ingestion step for Hillsborough County Property Appraiser (HCPA) parcel data.

## Current behavior

When you run the daily script, it will:

1. Install required Python dependencies from `requirements.txt`
2. Fetch the HCPA downloads page (`https://downloads.hcpafl.org/`)
3. Find the latest file matching `parcel_MM_DD_YYYY.zip`
4. Download it to `data/hcpa/`
5. Extract the zip and locate the `.dbf` table
6. Print:
   - `HCPA fields detected:` and the first 50 DBF field names
   - `Sample record:` and one record as a dictionary

This step is for schema discovery only so we can map columns correctly before adding scoring logic.

## Run

From the project directory:

```bash
cd padsplit_deal_scanner
python scanner/run_daily.py
```

## Files

- `scanner/sources/hillsborough_hcpa.py` – HCPA page parsing, zip download, extraction, DBF read
- `scanner/run_daily.py` – dependency install + ingestion execution + field/sample output
- `requirements.txt` – runtime dependencies (`requests`, `dbfread`)
