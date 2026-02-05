# E0469 Payer Coverage Analysis

Dashboard and analysis tool for tracking US insurance payer coverage policies for HCPCS code E0469 (Lung expansion airway clearance, continuous high frequency oscillation, and nebulization device).

## Project Goal

Build a comprehensive dashboard that:
1. Sweeps the internet to find payer policies mentioning E0469
2. Tracks coverage details, prior auth requirements, and policy language
3. Maintains accurate classification of coverage status

## HCPCS Code E0469

- **Description**: Lung expansion airway clearance, continuous high frequency oscillation, and nebulization device
- **Effective Date**: October 1, 2024 (NEW code)
- **Related Code**: A7021 (monthly disposables)
- **Devices**: Volara, BiWaze Clear, MetaNeb (OLE therapy devices)
- **Medicare Status**: No LCD/NCD exists - claims reviewed case-by-case

## Technology Stack

- **Database**: PostgreSQL 16 (via Postgres.app on macOS)
- **Backend**: Python 3.9+, Flask, psycopg2, openpyxl
- **Frontend**: HTML, CSS, JavaScript (no frameworks)

## Project Structure

```
E0469_Payer_Analysis/
├── CLAUDE.md                           # This file
├── SESSION_HANDOVER.md                 # Detailed session history and findings
├── schema.sql                          # PostgreSQL database schema
├── dashboard.py                        # Flask web app (port 5002)
├── load_data.py                        # Load payer data into database
├── templates/
│   └── dashboard.html                  # Main dashboard UI
├── E0469_Payer_Coverage_Analysis.py    # Original analysis script
├── E0469_Payer_Coverage_Analysis.xlsx  # Original spreadsheet output
├── E0469_Explicit_Payer_Policies.py    # Data source (64 payers)
├── E0469_Explicit_Payer_Policies.xlsx  # Spreadsheet output
└── mcp_pdf_server/                     # PDF extraction tool
    ├── pdf_extractor.py                # Extracts text from PDF URLs
    └── requirements.txt                # PyMuPDF dependency
```

## Database Tables

- `payers` - Master payer records (name, type)
- `payer_policies` - Coverage details (status, prior auth, source URL)
- `searched_payers` - Payers searched but no E0469 policy found
- `coverage_categories` - Reference table for coverage status colors

## Quick Start

### 1. Start PostgreSQL
Open **Postgres.app** (blue elephant). Ensure server running on port 5432.

### 2. Setup Database (first time only)
```bash
cd /Users/leahnoaeill/Downloads/E0469_Payer_Analysis

# Create database
/Applications/Postgres.app/Contents/Versions/latest/bin/psql -U postgres -c "CREATE DATABASE e0469_analysis;"

# Run schema
/Applications/Postgres.app/Contents/Versions/latest/bin/psql -U postgres -d e0469_analysis -f schema.sql

# Load data
python3 load_data.py
```

### 3. Start Dashboard
```bash
python3 dashboard.py
```
Dashboard: **http://localhost:5002**

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main dashboard |
| `/api/payers` | GET | Search payers (params: name, payer_type, coverage_status, page) |
| `/api/payers/<id>` | GET | Single payer details |
| `/api/payers/<id>` | PUT | Update payer info |
| `/api/coverage-statuses` | GET | Available coverage statuses |
| `/api/payer-types` | GET | Available payer types |
| `/api/aggregates` | GET | Summary statistics |
| `/api/searched-payers` | GET | Payers searched (no E0469 found) |
| `/api/export` | GET | Export to Excel |

## Database Connection

```python
DB_CONFIG = {
    "dbname": "e0469_analysis",
    "user": "postgres",
    "host": "localhost",
    "port": 5432
}
```

## Coverage Classification (CRITICAL)

Use exact policy language. These terms have different meanings:

| Term | Meaning | Appeal Potential |
|------|---------|------------------|
| **NOT COVERED** | Categorical exclusion from benefits | Low |
| **Investigational/Experimental** | Insufficient evidence | Medium |
| **Not Medically Necessary** | Does not meet criteria | Higher |
| **Case Review - Prior Auth Needed** | Individual case determination | Higher |

**Only use "NOT COVERED" when the policy explicitly says it.** Do not interpret "Investigational" as "NOT COVERED".

## Payer Data Structure

```python
{
    "name": "Payer Name",
    "type": "Commercial/BCBS/Medicaid/Medicare MAC/etc",
    "coverage": "Covered/Not Covered/Investigational/Partial/Case-by-Case",
    "prior_auth": "Yes/No/N/A",
    "investigational": "Yes/No/Not Specified",
    "not_med_necessary": "Yes/No/Not Specified",
    "date": "Policy effective date",
    "policy_num": "Policy number/ID",
    "notes": "Details about E0469 coverage",
    "source": "URL to policy document"
}
```

## Spreadsheet Color Coding

- **Green**: Covered with criteria
- **Yellow**: Partial coverage or investigational status noted
- **Red**: Not covered or investigational/experimental
- **Blue**: Case-by-case review (no LCD)

## Commands

```bash
# Start dashboard
python3 dashboard.py

# Reload data into database
python3 load_data.py

# Database stats
/Applications/Postgres.app/Contents/Versions/latest/bin/psql -U postgres -d e0469_analysis \
  -c "SELECT coverage_status, COUNT(*) FROM payer_policies GROUP BY coverage_status ORDER BY COUNT(*) DESC;"

# Regenerate spreadsheet (standalone)
python3 E0469_Explicit_Payer_Policies.py

# Extract text from a PDF policy
python3 mcp_pdf_server/pdf_extractor.py search "<PDF_URL>" "E0469"

# Kill dashboard
lsof -ti:5002 | xargs kill -9
```

## Search Strategies

```
"E0469" [payer name] policy
"E0469" "A7021" [payer name]
"E0469" Medicaid [state] policy
"E0469" "oscillation lung expansion" policy
"E0469" "investigational" OR "not covered" payer
```

## Current Statistics (as of Feb 4, 2026)

- **Total Payers with Explicit E0469 Policies**: 64
- **Searched Payers (No E0469 Found)**: 104
- **Covered**: 16
- **Not Covered**: 4
- **Investigational**: 10
- **Partial**: 20
- **Case-by-Case/Prior Auth**: 12

## Key Findings

1. **No Medicare LCD/NCD**: CMS has no specific coverage determination
2. **Most Consider OLE Investigational**: Volara, BiWaze Clear devices largely experimental
3. **New Code Challenge**: E0469 effective 10/1/2024 - many payers haven't published policies
4. **HFCWO vs OLE**: Many payers cover HFCWO (E0483) but NOT OLE devices (E0469)

## Reference

See `SESSION_HANDOVER.md` for complete session history, all payers searched, and detailed findings.
