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

## AWS Server Deployment

| Setting | Value |
|---------|-------|
| **Hostname** | `ec2-44-251-113-46.us-west-2.compute.amazonaws.com` |
| **Public IP** | `44.251.113.46` |
| **Region** | us-west-2 (Oregon) |
| **SSH User** | `ubuntu` |
| **SSH Key** | `~/downloads/ABMRCKEY.pem` |
| **Dashboard URL** | `http://ec2-44-251-113-46.us-west-2.compute.amazonaws.com:5002` |
| **Portal Username** | `payer` |
| **Portal Password** | `Dash@E0469` |

### SSH Access
```bash
ssh -i ~/downloads/ABMRCKEY.pem ubuntu@ec2-44-251-113-46.us-west-2.compute.amazonaws.com
```

### Docker Commands (on AWS)
```bash
cd ~/e0469-dashboard
docker compose ps
docker compose logs -f
docker compose restart
docker compose down
docker compose build --no-cache && docker compose up -d
```

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

## Coverage Classification (CRITICAL) — redesigned Oct 7, 2026

Each policy row has ONE **Coverage Status** plus a separate **Prior Auth** field and an exact **Policy Wording** quote (`payer_policies.policy_wording`).

| Coverage Status | Use when | Appeal Potential |
|---|---|---|
| **Covered** | Policy covers E0469 with criteria, OR E0469 is on a PA list / fee schedule (listed = covered; criteria always apply). Medicare MACs = Covered, PA No. | — |
| **Investigational** | Policy calls E0469 / OLE devices investigational, experimental or unproven (incl. UHC "unproven and not medically necessary", Aetna EIU). | Medium |
| **Not Medically Necessary** | Payer lists E0469 as "not medically necessary" without an investigational basis (Kaiser WA non-Medicare, BCBS RI commercial). | Higher |
| **Not Covered** | Policy explicitly says "not covered" / "non-covered" / "no covered indications" / "Noncovered". | Low |

**Prior Auth** values: `Yes` (only when a document explicitly requires PA for E0469, or by user decision), `No`, `Not Applicable` (policy says PA not applicable), `Not Stated`.

Rules:
- **Only use "Not Covered" when the policy explicitly says it.** Do not interpret "Investigational" as "Not Covered".
- The former statuses "PA Required - No Policy" and "Case-by-Case - No Policy" were retired Oct 7, 2026 (folded into Covered).
- Legacy columns `investigational` and `not_med_necessary` are still in the table but no longer shown; retire later.
- Never stamp a searched payer as re-checked unless a document was actually read — record "NOT VERIFIABLE" otherwise.

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

## Current Statistics (as of Oct 7, 2026 — deployed)

- **Total Payers**: 112 (local + AWS in sync) — Covered 57, Investigational 34, Not Covered 19, Not Medically Necessary 2
- **Prior Auth**: Yes 47, Not Stated 49, Not Applicable 12, No 4
- **Searched Payers (No Policy)**: 113 — includes 37 state Medicaid FFS programs and Medicaid MCO sweep results
- **Last Re-Review**: Oct 6–7, 2026 (Session 5) — full re-read of all sources, individual review of No Policy list, 50-state Medicaid FFS sweep, Centene Medicaid MCO sweep (CMS-0057-F PA lists). Review files: `E0469_Policy_Review_2026-10-06.xlsx`, `E0469_Coverage_Status_Remap_2026-10-07.xlsx`, `E0469_Medicaid_State_Sweep_2026-10-07.xlsx`
- **Previous**: Aug 7, 2026 (Session 4), May 10, 2026 (Session 3), Feb 6, 2026 (Session 2)
- **CMS DMEPOS Master List update (Jan 13, 2026, eff Apr 13, 2026)**: E0469 added to Master List — NOT on the Required PA List
- **AWS backup before Oct 7 deploy**: `~/e0469-dashboard/backup_e0469_predeploy_20261007.sql`; DB tables `payer_policies_backup_20261007`, `searched_payers_backup_20261007`
- **Warning**: `load_data.py` / `E0469_Explicit_Payer_Policies.py` use the OLD status model — running `load_data.py` would overwrite the database.

### Coverage status distribution
Run this query for current breakdown:
```bash
/Applications/Postgres.app/Contents/Versions/latest/bin/psql -U postgres -d e0469_analysis \
  -c "SELECT coverage_status, COUNT(*) FROM payer_policies GROUP BY coverage_status ORDER BY COUNT(*) DESC;"
```

## Key Findings

1. **No Medicare LCD/NCD**: CMS has no specific coverage determination. E0469 is NOT on the CMS DMEPOS Required PA List (verified Jan 13, 2026 update). Claims reviewed case-by-case via Noridian (JA) and CGS (JB).
2. **Most Consider OLE Investigational**: Volara, BiWaze Clear devices largely experimental
3. **New Code Challenge**: E0469 effective 10/1/2024 - many payers haven't published policies
4. **HFCWO vs OLE**: Many payers cover HFCWO (E0483) but NOT OLE devices (E0469)
5. **PA list ≠ coverage policy** (verified May 10, 2026): A payer can have an "investigational/Not Covered" coverage policy AND still add E0469 to a PA list. Example: Humana MA — coverage policy HUM-2007-001 says "no covered indications" for Medicaid, but Medicare Advantage uses a *different* document (2026 MA/DSNP PA List `790807ALL0725-C`) that adds E0469 as a NEW PA Required code effective 01/01/2026.
6. **State-by-state tracking is critical** (verified May 10, 2026): Humana Medicaid operates in 11 states (FL, IL, IN, KY, LA, MI, OH, OK, SC, VA, WI) with state-specific policy editions. Medica Volara policy covers 7 states (IA, KS, MN, NE, ND, SD, WI). Always verify per-state when policies exist per-state.
7. **BCBS plans referencing oscillation policies may not include E0469**: Some plans (TN, SC, LA) have oscillating-devices policies that never explicitly added E0469 to the applicable codes section. Always verify the actual policy text — don't trust WebSearch snippets.

## Authoritative Source URLs

| Payer | Type | URL |
|-------|------|-----|
| **Humana Medicare Advantage** | National PA list | https://assets.humana.com/is/content/humana/FINAL_Medicare%20and%20DSNP%20Prior%20Authorization%20and%20Notification%20List%20-%201-1-2026pdf |
| **Humana Medicaid (VA)** | State coverage | https://assets.humana.com/is/content/humana/MCD%20Multi-Function%20Oscillation%20Lung%20Expansion%20Therapy%20HUM-VA-2007-002%20ed%207.22.26pdf |
| **Humana Medicaid (KY)** | State coverage | https://assets.humana.com/is/content/humana/MOLET%20-%20HUM-2007-001%2006-2025%20-%20KY%20ed%20011620.26pdf |
| **Aetna CPB 0067** | Coverage policy (HTML) | https://www.aetna.com/cpb/medical/data/1_99/0067.html |
| **UHC Commercial (Mar 2026)** | National policy | https://www.uhcprovider.com/content/dam/provider/docs/public/policies/index/commercial/airway-clearance-devices-03012026.pdf |
| **CMS DMEPOS Required PA List** | Federal | https://www.cms.gov/research-statistics-data-and-systems/monitoring-programs/medicare-ffs-compliance-programs/dmepos/downloads/dmepos_pa_required-prior-authorization-list.pdf |

## Reference

See `SESSION_HANDOVER.md` for complete session history, all payers searched, and detailed findings.

## Quarterly Re-Review Workflow (established May 10, 2026)

Approach for periodic re-verification of all payers:

1. **Pull current data** — Export payers + payer_policies + searched_payers via `psql COPY ... TO STDOUT WITH (FORMAT csv, HEADER true)`
2. **WebSearch sweep** — Batch by category (UHC, BCBS, Medicaid, etc.). Note: WebSearch snippets are unreliable for verifying E0469 presence — they often miss it or hallucinate inclusion. Use them only as a *signal* that a policy may have changed.
3. **PDF-based verification** (CRITICAL — adds 5x reliability) — For every "change detected" or "no change" claim, run `python3 mcp_pdf_server/pdf_extractor.py search "<policy_url>" "E0469"` directly. The extractor will return exact text matches if found.
4. **Verify PA list separately from coverage policy** — A payer can have BOTH a "Not Covered" coverage policy AND a "PA Required" PA list (Humana MA pattern). Pull both documents.
5. **State-by-state for multi-state Medicaid plans** — Humana Healthy Horizons, UHC Community Plan, Medica, and any other multi-state Medicaid require per-state entries when state policy editions exist.
6. **Generate review spreadsheet** — Output to `E0469_Policy_Review_YYYY-MM-DD.xlsx` with 4 sheets: Status/Date/URL Changes, New Policy Additions, No Change Confirmed, Still Not Found.
7. **User reviews spreadsheet → approves → apply DB updates** to BOTH local Postgres.app AND AWS `cms_postgres` Docker container. Use a single SQL transaction; verify counts after.
8. **Update SESSION_HANDOVER.md** with session log.
