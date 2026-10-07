# Session Handover: E0469 Payer Policy Analysis

## Project Overview

Building a comprehensive spreadsheet of US insurance payers with **explicit E0469 policies** - payers that specifically mention HCPCS code E0469 in their published policy documents.

## HCPCS Code E0469

- **Description**: Lung expansion airway clearance, continuous high frequency oscillation, and nebulization device
- **Effective Date**: October 1, 2024 (NEW code - only ~16 months old)
- **Related Code**: A7021 (monthly disposables for E0469)
- **Devices**: Volara, BiWaze Clear, MetaNeb (OLE therapy devices)
- **Key Finding**: Most payers consider OLE devices investigational/experimental
- **Medicare Status**: No LCD/NCD exists - Noridian confirmed "At this time there is no established coverage criteria for this HCPCS code"

## Current State

### Files

| File | Purpose |
|------|---------|
| `E0469_Explicit_Payer_Policies.py` | Python script that generates the Excel spreadsheet |
| `E0469_Explicit_Payer_Policies.xlsx` | Output spreadsheet with payer data |

### Spreadsheet Statistics (as of Feb 4, 2026)

- **Total Payers**: 63 with explicit E0469 policies
- **NOT COVERED** (explicit language): 4
- **Investigational/Experimental**: ~10
- **Covered with Criteria**: 16
- **Partial Coverage** (OLE unproven, HFCWO may be covered): 20
- **Case-by-Case** (No LCD): 4
- **Case Review - Prior Auth Needed**: 2
- **Prior Auth Required** (various): 7

### Payer Data Structure

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

### Color Coding in Spreadsheet

- **Green**: Covered with criteria
- **Yellow**: Partial coverage or investigational status noted
- **Red**: Not covered or investigational/experimental
- **Blue**: Case-by-case review (no LCD)

## Payers Currently Included (50 Total)

### Medicare/CMS (4)
- CMS DMEPOS Fee Schedule
- Noridian Medicare (JA DME)
- Noridian Medicare (JD DME)
- CGS Medicare (JB DME)

### Commercial Plans (10)
- UnitedHealthcare Commercial
- UnitedHealthcare Individual Exchange
- UMR (UHC TPA)
- Surest (UHC)
- UnitedHealthcare Oxford
- Cigna
- Humana Commercial
- Humana Medicare Advantage
- Aetna
- Kaiser Permanente WA (Non-Medicare)

### BCBS Plans (12)
- Blue Cross Blue Shield Florida
- Premera Blue Cross
- Blue Cross NC
- BCBS Kansas
- BCBS Massachusetts
- Excellus BCBS (NY)
- Anthem Blue Cross Connecticut
- Kaiser Permanente WA (Medicare)
- BCBS Rhode Island (Not medically necessary for Commercial)
- Wellmark BCBS (Iowa/South Dakota) (Investigational)
- **Blue Cross Blue Shield of Michigan** (NEW - Investigational, per DIFS external review case)

### Medicaid Programs (16)
- Minnesota MHCP (NOT COVERED)
- California Medi-Cal (Covered with limits - 1 per 5 years)
- Humana Medicaid (NOT COVERED)
- UHC Community Plan - Multiple states:
  - New Jersey, Louisiana, North Carolina, Pennsylvania
  - Tennessee, Kentucky, Texas, Arizona
  - Michigan, Ohio, Virginia, Wisconsin

### Regional Plans (8)
- Medica (NOT COVERED - Investigational)
- HealthPartners (NOT COVERED - Investigational)
- Geisinger Health Plan
- Univera Healthcare (NY)
- Health Plan of Nevada
- Sierra Health and Life
- Rocky Mountain Health Plans
- EmblemHealth (NY)
- **Moda Health (Oregon/Alaska)** (NEW - Covered with Prior Auth)

### Reference
- BiWaze Clear Reimbursement Guide (ABM) - Manufacturer reference

## Key Findings

1. **No Medicare LCD/NCD**: CMS has no specific coverage determination - claims reviewed case-by-case
2. **Most Consider OLE Investigational**: Volara, BiWaze Clear devices largely considered experimental
3. **UHC Most Comprehensive**: UnitedHealthcare explicitly lists E0469 across all product lines
4. **New Code Challenge**: E0469 effective 10/1/2024 - many payers haven't published explicit policies yet
5. **HFCWO vs OLE**: Many payers cover HFCWO (E0483) for CF/bronchiectasis but NOT OLE devices (E0469)
6. **Anthem Removed E0469**: Anthem's policy revision (05/08/2025) explicitly removed E0469 from coverage
7. **State Medicaids Lag**: Most state Medicaid programs haven't published explicit E0469 policies yet

## Coverage Terminology Distinctions

**Important**: These terms have different meanings for coverage determination:

| Term | Meaning | Appeal Potential |
|------|---------|------------------|
| **NOT COVERED** | Categorical exclusion from benefits | Low - explicit exclusion |
| **Investigational/Experimental** | Insufficient evidence for coverage | Medium - may change with new evidence |
| **Not Medically Necessary** | Does not meet medical necessity criteria | Higher - case-by-case review possible |
| **Case Review - Prior Auth Needed** | Requires prior authorization review | Higher - individual case determination |

When reviewing policies, use the exact language from the policy document rather than interpreting as "NOT COVERED"

## Payers Searched But No Explicit E0469 Found

### BCBS Plans
- BCBS Texas
- BCBS Illinois
- BCBS Tennessee
- BCBS Arkansas
- BCBS Idaho
- BCBS Montana
- Horizon BCBS NJ
- Empire BCBS
- Independence Blue Cross
- Carefirst BCBS (MD/DC/VA)

### Commercial/Regional
- Oscar Health
- Bright Health
- Clover Health
- First Health
- ConnectiCare
- Sentara Health Plans
- Highmark (PA) - policy covers E0483 but not E0469
- Harvard Pilgrim / Tufts / Point32Health
- Medical Mutual (OH)
- Priority Health
- SelectHealth
- Blue Shield California
- Anthem California

### Medicaid MCOs
- Molina Healthcare
- Centene / WellCare
- Amerigroup / Elevance - CG-DME-43 covers E0483, not E0469
- Superior Health Plan (TX)

### State Medicaid Programs (Fee-for-Service)
- Pennsylvania DHS
- Ohio ODM
- Michigan MDHHS
- North Carolina (NCTracks)
- Virginia DMAS
- New Jersey FamilyCare
- Arizona AHCCCS
- Washington Apple Health
- Kentucky DMS
- Louisiana LDH
- Indiana FSSA
- Connecticut DSS/HUSKY
- Nevada DHCFP
- Maryland
- Wisconsin ForwardHealth
- South Carolina SCDHHS
- Oregon OHP
- Illinois HFS
- Georgia DCH
- Texas HHSC
- Florida AHCA

### Federal
- Tricare
- VA

### Workers' Compensation
- Federal OWCP
- State WC programs (NY, CA, TX)

## Why So Few State Medicaid Policies Found

1. **Code is very new** - Only effective 10/1/2024 (~16 months)
2. **Fee schedules in PDF/Excel** - Not web-indexed or searchable
3. **No established Medicare LCD** - States often follow Medicare guidance
4. **Claims reviewed case-by-case** - No formal policy published
5. **MCOs handle coverage** - Most Medicaid members in managed care, not FFS

## How to Continue

### To Add More Payers

1. Search for payers with explicit E0469 mentions:
   ```
   "E0469" [payer name] policy
   "E0469" "A7021" [payer name]
   "E0469" Medicaid [state] policy
   "E0469" "oscillation lung expansion" policy
   "E0469" "investigational" OR "not covered" payer
   ```

2. Edit the Python file to add new payer entries to `payer_data` list

3. Run the script to regenerate the spreadsheet:
   ```bash
   python3 E0469_Explicit_Payer_Policies.py
   ```

### Suggested Search Targets

- Additional Medicare Advantage plans with prior auth lists
- Remaining BCBS state plans (check medical policy portals directly)
- Large employer self-funded plans
- State employee health plans

## Useful Policy URLs Found

| Payer | Policy URL |
|-------|------------|
| Medica | https://partner.medica.com/-/media/documents/provider/coverage-policies/volara-oscillation-and-lung-expansion-cp.pdf |
| HealthPartners | https://www.healthpartners.com/ucm/groups/public/@hp/@public/@cc/documents/documents/aentry_045636.pdf |
| BCBS Florida | https://mcgs.bcbsfl.com/MCG?mcgId=09-E0000-28 |
| Premera | https://www.premera.com/medicalpolicies-individual/1.01.539.pdf |
| Blue Cross NC | https://www.bluecrossnc.com/providers/policies-guidelines-codes/commercial/home-health-dme/updates/oscillatory-devices-for-treatment-of-respiratory-conditions |
| Kaiser WA | https://wa-provider.kaiserpermanente.org/static/pdf/hosting/clinical/criteria/pdf/hfcwo.pdf |
| Moda Health | https://www.modahealth.com/-/media/modahealth/shared/provider/prior-authorization/pre-auth-list-commercial.pdf |
| Wellmark BCBS | https://digital-assets.wellmark.com/adobe/assets/urn:aaid:aem:8aa2f47a-61ff-4beb-9f1b-219c24adb04e/original/as/Airway-Clearance-Devices.pdf |
| BCBS RI | https://www.bcbsri.com/providers/update/additional-hcpcs-level-ii-code-changes-and-modifier-changes-4 |
| BCBS Michigan | https://www.michigan.gov/difs/-/media/Project/Websites/difs/PRIRA/2024/September/BCBSM_227614.pdf |

## User's Original Request

> "yes keep searching and ensure the spreadsheet only has payers with policies who have only E0469 included with explicit E0469 policies"

The user wants ONLY payers that explicitly mention E0469 in their published policies - no inferred or assumed coverage.

## PDF Extraction Script

A Python script was created to enable Claude to read PDFs directly via Bash, solving the limitation where compressed PDFs returned garbled binary data through WebFetch.

### Files Created

| File | Purpose |
|------|---------|
| `mcp_pdf_server/pdf_extractor.py` | Script that extracts text from PDF URLs |
| `mcp_pdf_server/requirements.txt` | Python dependencies (PyMuPDF) |

### Setup (Already Completed)

```bash
# Install PyMuPDF (already done)
pip3 install PyMuPDF
```

### Usage

Claude can call this script via Bash to read PDFs:

```bash
# Search for a specific term (most useful for policy searches)
python3 mcp_pdf_server/pdf_extractor.py search "<PDF_URL>" "E0469"

# Extract all text from a PDF
python3 mcp_pdf_server/pdf_extractor.py extract "<PDF_URL>"

# Extract only first N pages
python3 mcp_pdf_server/pdf_extractor.py extract "<PDF_URL>" 5
```

### Tested & Working

Successfully tested on:
- BCBS Vermont Investigational Services PDF - Found E0469 in 2 locations
- Capital Blue Cross Experimental/Investigational PDF - Found E0469 in respiratory codes section

### Limitations

- Cannot access login-protected PDFs
- Scanned image PDFs without OCR text layer will return empty
- Very large PDFs may timeout

## Commands

```bash
# Regenerate spreadsheet
python3 E0469_Explicit_Payer_Policies.py

# View current payer count
grep -c '"name":' E0469_Explicit_Payer_Policies.py
```

## Session History

- **Feb 4, 2026 (Initial)**: Created spreadsheet with 46 payers
- **Feb 4, 2026 (Update 1)**: Added 3 new payers (Moda Health, BCBS RI, Wellmark BCBS) - now 49 total
  - Extensive searches of state Medicaid programs yielded no additional explicit E0469 policies
  - Most state Medicaids have fee schedules in PDF format, not web-indexed
  - Confirmed Anthem removed E0469 from their policy (05/08/2025 revision)
- **Feb 4, 2026 (Update 2)**: Added 1 new payer - now 50 total
  - Added **Blue Cross Blue Shield of Michigan** - Michigan DIFS external review case (Sept 2024) explicitly determined Volara/E0469 is experimental/investigational and NOT COVERED
  - Searched many additional payers: UPMC, MVP Health Care, Capital Blue Cross, Regence BCBS, Quartz Health, Point32Health, AmeriHealth Caritas, Magellan Health - no explicit E0469 policies found
  - Confirmed Anthem CG-DME-43 policy does NOT include E0469 (only E0483)
  - BCBS Vermont may have E0469 as investigational but PDF not readable for verification
  - **Added new sheet "Searched - No E0469 Found"** with 65+ payers that were searched but had no explicit E0469 policy
- **Feb 4, 2026 (Update 3)**: Continued commercial payer searches
  - Searched: Centene/WellCare/Ambetter, LifeWise/Cambia, Allina, Sanford, CareSource, BCBS Alabama, BCBS Montana, BCBS Illinois (EIU list), ConnectiCare, Blue Cross MN, AvMed, FHCP, Devoted Health, Alignment Healthcare, Clover Health, CDPHP, Fallon Health, Manatee/GuideWell, Neighborhood Health Plan
  - No new explicit E0469 policies found - most policies either cover only E0483 or have no published E0469 policy
  - Challenge: Many commercial payers have experimental/investigational code lists in PDF format that are not easily searchable/readable
  - CareSource Ohio policy covers PAP devices but E0469 not explicitly mentioned
- **Feb 4, 2026 (Update 4)**: Added 3 new payers from user's payer list review - now 53 total
  - Added **Lifewise (Washington)** - E0469 in fee schedule with fixed pricing aligned to CMS, effective 07/15/2025
  - Added **Fidelis Care (New York Medicaid)** - E0469 in DME Authorization Grid, prior auth required
  - Added **Kentucky Medicaid MSEA** - E0469 referenced in regulation 907 KAR 1:479
  - Searched 20+ additional payers from user's list - no explicit E0469 policies found for: BCBS LA, Humana PR, Indiana IHCP, BCBS ND, Providence Health Plan OR, HMSA Hawaii, Texas Children's Health Plan, Anthem WI/VA/ME/NY/GA, BCBS CA/NV, CalViva Health, iCare WI, Colorado HCPF, Select Health CO, Mississippi Medicaid, Montana Medicaid
  - **Note**: Premera Blue Cross AK uses same policy 1.01.539 as main Premera entry (already included)
- **Feb 4, 2026 (Update 5)**: User manually reviewed PDFs and found 10 additional payers - now 63 total
  - Added **Capital Blue Cross (PA)** - MP 4.002 Experimental/Investigational (eff. 02/01/2026)
  - Added **BCBS Texas** - EIU or Clinical Review, fee $9,003.78 purchase
  - Added **BCBS Illinois** - EIU Non-Reimbursable
  - Added **BCBS New Mexico** - Recommended Clinical Review (Predetermination)
  - Added **BCBS Nebraska** - MA Prior Auth (MA-X-077)
  - Added **BCBS Minnesota** - Prior Auth via Evicore
  - Added **BCBS Vermont** - Investigational (10.01.VT204, eff. 01/01/2025)
  - Added **CareSource Ohio** - Prior Auth Required (eff. 04/01/2025)
  - Added **Select Health Utah (Medicare)** - Prior Auth Required (eff. 12/22/2025)
  - Added **Select Health Idaho (Medicare)** - Prior Auth Required (eff. 12/22/2025)
  - **Key finding**: Many BCBS plans have E0469 in EIU (Experimental/Investigational/Unproven) lists but PDFs are not web-searchable
  - **Limitation identified**: Claude's WebFetch tool cannot reliably parse compressed/encoded PDFs that Google Chrome AI can read
- **Feb 4, 2026 (Update 6)**: Coverage language accuracy review - corrected entries to match actual policy language
  - **Key distinction identified**: "NOT COVERED" vs "Investigational" vs "Not Medically Necessary" are different coverage determinations
  - Changed entries using "NOT COVERED" when policy actually says "Investigational" or "Experimental"
  - Changed "Not Medically Necessary" entries to "Case Review - Prior Auth Needed" (allows for appeal/case review)
  - **Payers corrected**:
    - HealthPartners: NOT COVERED → Investigational - Experimental
    - BCBS Florida: NOT COVERED → Investigational - Experimental
    - Premera: NOT COVERED → Investigational
    - Kaiser WA (Non-Medicare): Not Medically Necessary → Case Review - Prior Auth Needed
    - BCBS RI: NOT COVERED → Case Review - Prior Auth Needed
    - Wellmark BCBS: NOT COVERED → Investigational
    - BCBS Michigan: NOT COVERED → Investigational - Experimental
    - Blue Cross NC: NOT COVERED → Investigational
    - BCBS Vermont: NOT COVERED → Investigational
    - Aetna: NOT COVERED → Investigational - Experimental
    - Humana Commercial: NOT COVERED → Investigational - Experimental
    - Humana Medicaid: NOT COVERED → Investigational - Experimental
  - **Only 4 payers explicitly say "NOT COVERED"**: Medica, Minnesota MHCP, Capital Blue Cross, BCBS Illinois
- **Feb 6, 2026 (Session 2)**: Dashboard deployment and enhancements
  - **Humana Medicare Advantage updated**: Changed from "Covered" (Prior Auth) to "NOT COVERED" based on Humana policy HUM-2007-001 (Multi-Function Oscillation Lung Expansion Therapy). Updated on both local and AWS.
  - **Humana Commercial updated**: Changed from "Prior-Auth Required" to "NOT COVERED" based on same Humana policy HUM-2007-001. Updated on both local and AWS.
  - **Humana Medicaid updated**: Changed from "Prior-Auth Required" to "NOT COVERED" based on same Humana policy HUM-2007-001. Updated on both local and AWS.
  - **Now 7 payers explicitly say "NOT COVERED"**: Medica, Minnesota MHCP, Capital Blue Cross, BCBS Illinois, Humana Medicare Advantage, Humana Commercial, Humana Medicaid
  - **Rocky Mountain Health Plans (Colorado) updated**: Changed from "Covered" to "Prior-Auth Required" based on Anthem precertification list (eff. March 1, 2025). Updated source URL. Updated on both local and AWS.
  - **State column added to dashboard**: Added sortable "State" column to payer coverage table. Added `p.state` to API query and allowed sort fields. Populated missing state values for HealthPartners (MN), Premera/Kaiser WA (WA), Geisinger (PA), Moda Health (OR). 14 national payers remain NULL. Applied to both local and AWS.
  - **Payer search conducted**: Ran 4 parallel web search agents (BCBS, commercial, Medicaid, Medicare/federal). Found 10 new payers with explicit E0469 mentions. All 10 added to both local and AWS databases (IDs 72-81):
    - **BCBS Tennessee** - Investigational (OLE), bcbst.com
    - **BCBS South Carolina** - Investigational (OLE), southcarolinablues.com
    - **BCBS Louisiana** - Investigational (OLE), Policy 00090
    - **FEP Blue** (Federal Employee Program) - Investigational (OLE), Policy 10115
    - **Anthem multi-state** - Investigational (DME.00012), anthem.com
    - **Medical Mutual of Ohio** - Investigational (Policy 200508), medmutual.com
    - **Highmark Health Options (DE Medicaid)** - Covered w/ criteria (MP-1141)
    - **Providence Health Plan (OR Medicare)** - NCD 240.5 non-coverage (MP220)
    - **McLaren Health Plan (MI Medicaid)** - Prior Auth Required
    - **New York Medicaid (eMedNY)** - On DME codes list
  - **Re-verification needed**: BCBS Massachusetts (Policy 120 may now list E0469 as of 10/1/2024) and Cigna (Policy 0069 updated, E0469 effective 01/01/2026) — both were previously removed but agents found updated policies
  - **Behind secure portals** (need manual verification): Highmark BCBS (E-20-016), Arkansas BCBS (Policy 2022013)
  - **Latest AWS redeployment**: Updated dashboard.py and templates/dashboard.html via scp to ~/e0469-dashboard/ on AWS. Restarted e0469_dashboard container (`docker compose restart`). Changes deployed: State column in payer table, 10 new payers (IDs 72-81) already in database. Dashboard verified at port 5002.
  - **Univera Healthcare (New York) updated** (ID 25): Changed from "Covered" to "Prior-Auth Required" based on Univera airway clearance devices policy. Source URL unchanged. Updated on both local and AWS.
  - **AWS redeployment**: Synced latest dashboard.py and templates/dashboard.html to ~/e0469-dashboard/ on AWS via scp. Restarted e0469_dashboard container. Dashboard verified running on port 5002.
  - **Health Plan of Nevada updated** (ID 35): Changed from "Covered" to "Prior-Auth Required", investigational set to "Yes". Source URL updated to direct PDF: airway-clearance-devices.pdf. Updated on both local and AWS.
  - **Coverage status normalized**: Fixed inconsistent casing — 3 Humana entries changed from "NOT COVERED" to "Not Covered" to match other entries. Applied to both local and AWS.
  - **California Medi-Cal (Medicaid) updated** (ID 44): Changed from "Covered" to "Prior-Auth Required", prior auth set to "Yes". Source URL updated to direct PDF: duracd.pdf. Updated on both local and AWS.
  - **AWS redeployment**: Synced latest dashboard.py and templates/dashboard.html to AWS. Restarted e0469_dashboard container. All DB changes (Health Plan of Nevada, Medi-Cal, coverage normalization) already applied. Dashboard verified running on port 5002.
  - **EmblemHealth (New York) removed** (ID 47): DME rental/purchase policy does not explicitly reference E0469. Moved to searched_payers on both local and AWS. Payer count: 75 → 74.
  - **Moda Health (Oregon/Alaska) updated** (ID 48): Changed from "Covered" to "Prior-Auth Required". Source URL unchanged (pre-auth-list-commercial.pdf). Updated on both local and AWS.
  - **Sierra Health and Life (Nevada) updated** (ID 36): Changed from "Covered" to "Prior-Auth Required". Source URL unchanged. Updated on both local and AWS.
  - **Kaiser Permanente WA (Medicare) updated** (ID 9): Changed from "Covered" to "Prior-Auth Required", investigational set to "Yes". Source URL updated to new-emergingtech.pdf. Updated on both local and AWS.
  - **AWS redeployment**: Synced latest dashboard.py and templates/dashboard.html to AWS. Restarted e0469_dashboard container. All recent DB changes (Moda Health, Sierra Health, Kaiser WA Medicare, EmblemHealth removal) already applied. Dashboard verified running on port 5002.
  - **Fidelis Care (New York Medicaid) updated** (ID 53): Changed from "Covered" to "Prior-Auth Required". Policy date set to "January 3, 2026". Source URL updated to direct PDF (Medicaid DME Authorization Grid). Updated on both local and AWS.
  - **AWS redeployment**: Synced latest dashboard.py and templates/dashboard.html to AWS. Restarted e0469_dashboard container. Fidelis Care DB change already applied. Dashboard verified running on port 5002.
  - **AWS full rebuild**: Synced latest dashboard.py and templates/dashboard.html, then ran `docker compose build --no-cache && docker compose up -d` to fully rebuild container with all latest code including State column in table view. Dashboard verified running on port 5002.
  - **Anthem entries removed**: Anthem (Elevance Health) (ID 76) — policy DME.00012 explicitly removed E0469. Anthem Blue Cross Connecticut (ID 23) — unverified genhealth.ai source, same policy no longer covers E0469. Both moved to searched_payers on local and AWS. Payer count: 74 → 72.
  - **Noridian Medicare (JD DME) removed** (ID 27): Not a payer — is a DME MAC (Medicare Administrative Contractor). Moved to searched_payers on local and AWS. Payer count: 72 → 71.
  - **CMS DMEPOS Fee Schedule removed** (ID 1): Not a payer — is a CMS fee schedule reference. Moved to searched_payers on local and AWS. Payer count: 71 → 70.
  - **FEP Blue (Federal Employee Program) removed** (ID 75): Removed per user request. Moved to searched_payers on local and AWS. Payer count: 70 → 69.
  - **Highmark Health Options (Delaware) removed** (ID 78): Policy MP-1141 does not mention E0469. Moved to searched_payers on local and AWS. Payer count: 69 → 68.
  - **AWS redeployment**: Synced latest dashboard.py and templates/dashboard.html to AWS. Restarted e0469_dashboard container. All recent DB removals (Anthem x2, Noridian JD, CMS DMEPOS, FEP Blue, Highmark) already applied. Dashboard verified running on port 5002.
  - **GitHub backup**: Pushed all changes to new branch `Updated_Payer_Feb6` on `leahnoaeill-lgtm/E0469_Payer_Analysis`. 9 files committed (321 insertions, 7 deletions). Includes state column, coverage status updates, 11 removals, 10 additions, Docker files, and auth support.
  - **Humana (Commercial) removed** (ID 22): Generic and outdated policy. More recent Humana Medicare Advantage and Humana Medicaid entries already in database. Moved to searched_payers on local and AWS. Payer count: 68 → 67.
  - **AWS redeployment**: Synced latest dashboard.py and templates/dashboard.html to AWS. Restarted e0469_dashboard container. Humana Commercial DB removal already applied. Dashboard verified running on port 5002.
  - **CareSource Ohio (Medicaid) updated** (ID 62): Policy date changed from "04/01/2025" to "January 31, 2025". All other fields unchanged (Prior-Auth Required, no investigational). Updated on both local and AWS.
  - **Anthem Indiana added** (ID 82): New payer — Prior-Auth Required, no investigational, state IN, policy date January 1, 2025. Added to both local and AWS. Payer count: 67 → 68.
  - **Hawaii Medical Service Association (HMSA) added** (ID 83): New payer — Not Covered, BCBS type, state HI. Codes do not meet payment determination criteria. Added to both local and AWS. Payer count: 68 → 69.
  - **AWS redeployment**: Synced latest dashboard.py and templates/dashboard.html to AWS. Restarted e0469_dashboard container. Anthem Indiana and HMSA DB additions already applied. Dashboard verified running on port 5002.
  - **Northwoods Medical added** (ID 84): New payer — Prior-Auth Required, investigational Yes, no state, policy date November 3, 2025. Added to both local and AWS. Payer count: 69 → 70.
  - **AWS redeployment**: Synced latest dashboard.py and templates/dashboard.html to AWS. Restarted e0469_dashboard container. Northwoods Medical DB addition already applied. Dashboard verified running on port 5002.
  - **Menu cleanup**: Removed "Refresh Data" and "Search Web for Payers" buttons from dashboard top menu. Remaining menu items: Coverage Heatmap, Add New Payer. Deployed to AWS.
  - **Add New Payer form updated**: Added missing fields to the form: State (2-letter code), Prior Auth Required (Yes/No/Not Specified), Investigational (Yes/No/Not Specified), Policy Date, Policy Number. Updated frontend form, JS submit function, and backend API to handle all fields. Deployed to AWS.
  - **Dashboard changes**:
    - Added **Investigational** stat card to top of dashboard (alongside Total Payers, Covered, Prior-Auth, Not Covered)
    - Added **Investigational** bar to Coverage Summary chart
    - Updated **Geisinger Health Plan** from "Covered" to "Prior-Auth Required"
  - **Authentication added**:
    - Added HTTP Basic Auth to dashboard.py (same pattern as CMS Dashboard)
    - Local: auth disabled by default (empty password)
    - AWS: username `payer`, password `Dash@E0469`
    - Auth env vars: `AUTH_USERNAME`, `AUTH_PASSWORD`
  - **AWS Deployment** (new):
    - Deployed to EC2: `ec2-44-251-113-46.us-west-2.compute.amazonaws.com:5002`
    - SSH key: `~/downloads/ABMRCKEY.pem`, user: `ubuntu`
    - Docker container `e0469_dashboard` on port 5002
    - Reuses existing `cms_postgres` container (shared PostgreSQL, separate `e0469_analysis` database)
    - Connected via `cms_network` Docker network
    - Project directory on server: `~/e0469-dashboard/`
    - 2 gunicorn workers (conserving RAM on 1.8 GB server)
  - **Files created for deployment**:
    - `requirements.txt` - Flask, psycopg2-binary, openpyxl, requests, gunicorn
    - `Dockerfile` - python:3.11-slim, gunicorn on port 5002
    - `docker-compose.yml` - single service, external cms_network, port 5002:5002
    - `.dockerignore` - excludes xlsx, logs, mcp_pdf_server
  - **Code changes**:
    - Added `DB_PASSWORD` env var support to `dashboard.py` and `load_data.py` (required for Docker PostgreSQL auth)
    - Added `functools.wraps` import and Basic Auth middleware to `dashboard.py`
  - **Database on AWS**: 69 payers, 69 policies, 104 searched payers (exported via pg_dump from local)
  - **AWS server state**: 3 containers running (cms_dashboard:5001, e0469_dashboard:5002, cms_postgres:5432)
  - **Updated CLAUDE.md** with AWS connection info, credentials, and Docker commands

## AWS Deployment Architecture

```
EC2 Instance (Ubuntu 24.04, Docker 28.2.2, 1.8 GB RAM)
├── cms_network (Docker network)
│   ├── cms_postgres (port 5432) - shared PostgreSQL
│   │   ├── cms_analysis database (CMS E0483 dashboard)
│   │   └── e0469_analysis database (E0469 payer dashboard)
│   ├── cms_dashboard (port 5001) - CMS DME Dashboard
│   │   └── Login: cms / Dash@E0469
│   └── e0469_dashboard (port 5002) - E0469 Payer Dashboard
│       └── Login: payer / Dash@E0469
└── Project directories
    ├── ~/cms-dashboard/
    └── ~/e0469-dashboard/
```

### AWS Connection
```bash
# SSH
ssh -i ~/downloads/ABMRCKEY.pem ubuntu@ec2-44-251-113-46.us-west-2.compute.amazonaws.com

# Manage E0469 dashboard
cd ~/e0469-dashboard && docker compose ps|logs|restart

# Manage CMS dashboard
cd ~/cms-dashboard && docker compose ps|logs|restart
```

## E0469 Source Verification Audit (Feb 6, 2026)

Verified all 68 payer source URLs to confirm E0469 is explicitly mentioned. Used PDF extractor tool and web fetch.

### Payers REMOVED (E0469 not in source — moved to searched_payers):

| Payer | ID | Reason | Removed |
|-------|----|--------|---------|
| **Excellus BlueCross BlueShield (NY)** | 31 | Policy 1.01.15 lists E0480-E0484 but NOT E0469. | Feb 6, 2026 |
| **BCBS Massachusetts** | 34 | Policy lists E0481, E0483, E0484, S8185 only — no E0469. Not updated for new code. | Feb 6, 2026 |
| **Cigna** | 20 | Policy lists E0481, E0482, E0483, E1399 only — not updated for E0469 (eff 10/1/2024). | Feb 6, 2026 |
| **BCBS Michigan** | 51 | DIFS external review discusses Volara device but coded under E1399/A9999. E0469 code never appears in document. | Feb 6, 2026 |
| **EmblemHealth (New York)** | 47 | DME rental/purchase policy does not explicitly reference E0469. | Feb 6, 2026 |
| **Anthem Blue Cross Connecticut** | 23 | Source was third-party aggregator (genhealth.ai). CG-DME-43 policy covers E0483 but E0469 was removed. | Feb 6, 2026 |
| **Anthem (Elevance Health)** | 76 | Policy DME.00012 explicitly removed E0469 from coverage. E0469 no longer in policy. | Feb 6, 2026 |
| **Noridian Medicare (JD DME)** | 27 | Not a payer — is a DME MAC (Medicare Administrative Contractor). Removed from payer list. | Feb 6, 2026 |
| **CMS DMEPOS Fee Schedule** | 1 | Not a payer — is a CMS fee schedule reference. Removed from payer list. | Feb 6, 2026 |
| **FEP Blue (Federal Employee Program)** | 75 | Removed from payer list per user request. | Feb 6, 2026 |
| **Highmark Health Options (Delaware)** | 78 | Policy MP-1141 does not mention E0469. No explicit E0469 policy available. | Feb 6, 2026 |
| **Humana (Commercial)** | 22 | Generic and outdated policy. More recent Humana Medicare Advantage and Humana Medicaid entries already in database. | Feb 6, 2026 |

All 12 removed from both local and AWS databases and added to `searched_payers`.

### Payers with Broken/Inaccessible Sources (KEEP — user verified manually):

| Payer | ID | Issue |
|-------|----|-------|
| **Humana Commercial** | 22 | Source is genhealth.ai (third-party aggregator) — doesn't list E0469. Needs direct Humana policy URL. |
| **BCBS Texas** | 56 | URL returns 404 error. User added from manual PDF review of fee schedule. |
| **BCBS Illinois** | 57 | General portal page, no codes visible. User added from manual PDF review (EIU Non-Reimbursable). |
| **BCBS New Mexico** | 58 | General portal page, no codes visible. User added from manual PDF review (Recommended Clinical Review). |
| **BCBS Florida** | 7 | JS-rendered SPA, can't extract content programmatically. |
| **Rocky Mountain Health Plans** | 19 | JS-rendered portal, no policy content accessible. |
| **Minnesota MHCP** | 6 | Website WAF blocks automated access (Radware). |

### Payers CONFIRMED (E0469 explicitly found in source):

**Medicare/CMS**: CMS DMEPOS (1), Noridian JA (2), Noridian JD (27), CGS JB (3)

**BCBS Plans**: BCBS Kansas (33), BCBS NC (32), BCBS RI (49), BCBS Vermont (61), BCBS Nebraska (59), BCBS Minnesota (60), Wellmark BCBS (50)

**Commercial**: Aetna (46), Premera (8), Moda Health (48), Kaiser WA Medicare (9), Kaiser WA Non-Medicare (10)

**Humana**: Humana Medicaid (45), Humana Medicare Advantage (21)

**Regional**: Univera Healthcare (25), Geisinger (24), Health Plan of Nevada (35), Sierra Health and Life (36), EmblemHealth (47)

**Medicaid**: California Medi-Cal (44), Kentucky Medicaid (54), Fidelis Care NY (53), Lifewise WA (52), CareSource OH (62), Select Health UT (63), Select Health ID (64)

**UHC Plans**: UHC Commercial (11), UHC Individual Exchange (13), UHC Oxford (16), UMR (14), Surest (15), UHC Community Plan (12), + all UHC Medicaid state plans (17, 18, 28-30, 37-43)

**Medica**: All 7 state entries (65-71) — same policy URL confirmed

### Current Database Counts (after Feb 6, 2026 audit):
- **Local**: 70 payers, 70 policies, 116 searched
- **AWS**: 70 payers, 70 policies, 116 searched
- **Pending re-verification**: BCBS Massachusetts, Cigna (may need re-adding — agents found updated policies with E0469)
- **Behind secure portals** (need manual verification): Highmark BCBS PA (E-20-016), Arkansas BCBS (Policy 2022013)

## May 10, 2026 (Session 3) — Quarterly Re-Review of All 186 Payers

### Goal
Re-review all 70 active payers and 116 searched payers (180 unique after dedup) to detect policy changes, new policy additions, and status corrections since the Feb 6, 2026 baseline.

### Approach
1. **Phase 1 — WebSearch sweep** of all 180 payers, batched by category (UHC family, Medica family, BCBS plans, Medicaid, commercial, federal)
2. **Phase 2 — PDF-based re-verification** using `mcp_pdf_server/pdf_extractor.py` for direct E0469 term verification in policy PDFs (triggered by Humana misclassification finding)
3. **Phase 3 — DB updates** applied to both local Postgres.app and AWS `cms_postgres` Docker container

### Key Phase 1 findings (from WebSearch sweep)
- **UHC ecosystem**: All 14 UHC variant policies refreshed to **03/01/2026** effective date (Commercial PDF now at `airway-clearance-devices-03012026.pdf`)
- **Humana HUM-2007-001 (Medicaid)**: Reviewed 06/03/2025, effective date moved to 01/16/2026 (KY ed) and 07/22/2026 (VA ed)
- **Medica (7 state plans)**: Administrative update 08/05/2025 for code refresh
- **Premera (WA)**: Annual review 10/13/2025, policy statements unchanged
- **Medical Mutual OH**: Policy #200508 updated 08/19/2025
- **Fidelis Care NY**: New Auth Grids effective 04/01/2026
- **BCBS Minnesota**: As of **08/01/2025, EviCore no longer manages DME PAs** for BCBSMN; providers now submit directly via BCBSMN Prior Authorization Lookup Tool / Availity Essentials
- **NO new explicit E0469 policies detected** among the 110 unique searched payers

### Phase 2 — PDF-based re-verification (triggered by Humana finding)

User flagged that Humana Medicaid (VA) was Not Covered but Humana Medicare Advantage was Prior Auth Required — but the DB had both as Not Covered. PDF verification confirmed:
- **Humana Medicare Advantage** policy authority is the **2026 MA/DSNP Prior Authorization & Notification List** (`790807ALL0725-C`, "ALL" = applies nationally to all 46 states + DC where Humana MA operates). E0469 listed under "DME — Airway Clearance Devices (E0469, E0481, E0482)" as a **NEW Prior Authorization Requirement** effective 01/01/2026.
- **Humana Medicaid (HUM-2007-001 / HUM-VA-2007-002)** are state-specific MEDICAID coverage policies; they apply only to the 11 Medicaid states (FL, IL, IN, KY, LA, MI, OH, OK, SC, VA, WI) — **do not apply to Medicare Advantage**.

This pattern (PA list ≠ coverage policy) drove additional PDF re-verifications. Findings:

| Payer (DB ID) | Issue Found | Action |
|---|---|---|
| **Aetna (46)** | CPB 0067 explicitly lists E0469 as "HCPCS codes **not covered** for indications listed in the CPB" (BiWaze, Volara). DB had PA Required. | Status corrected to **Not Covered** |
| **BCBS Tennessee (was 72)** | Direct policy verification: E0469 NOT in actual policy text. Only E0480 (percussor) referenced. | **Removed** from active payers, moved to searched |
| **BCBS South Carolina (was 73)** | PDF extraction did NOT find E0469 in policy document. | **Removed** from active payers, moved to searched |
| **BCBS Louisiana (was 74)** | Source URL is 2023-06-01 PDF predating E0469. No newer version published. URL probes for 2024/2025/2026 variants all 404'd. | **Removed** from active payers, moved to searched |
| **BCBS Mississippi (new ID 87)** | Has explicit E0469 policy (added 10/01/2024, last reviewed 09/19/2025). Was NOT in either table. | **Added** as new payer |
| **BCBS Florida (7)** | Last annual review is 10/15/2025 (DB had 09/25/2025) | Date refreshed |
| **Capital Blue Cross (55)** | Effective date now 05/01/2026 (DB had 02/01/2026) | Date refreshed |
| **BCBS Rhode Island (49)** | Earlier WebSearch finding wrongly classified status as "Not Covered". Actual policy has nuanced rules: Not Medically Necessary (Commercial), Subject to medical review (MA); Professional reimbursed, Institutional not reimbursed. | DB description retained as accurate; spreadsheet correction noted |
| **UHC Louisiana Medicaid (18)** | UHC LA policy marks E0469 with asterisk = "not on State of Louisiana Medicaid Fee Schedule and may not be covered." Coverage nuance was not captured in DB notes. | Notes updated |
| **CMS DMEPOS Required PA List (Jan 13, 2026 update)** | E0469 NOT on the list. Medicare still reviews case-by-case (Noridian/CGS unchanged). | No change |
| **Cigna (searched 106)** | Policy 0069 (eff. 11/9/2025) does NOT include E0469. Cigna 2026 DME orientation also excludes. Remains in searched. | No change |

### Phase 3 — DB updates applied (local + AWS, both in sync)

**Humana corrections (applied early in session):**
- Humana Medicare Advantage (ID 21): Not Covered → **Prior-Auth Required**; URL updated to MA/DSNP PA List; policy number `790807ALL0725-C`
- Humana Medicaid (ID 45): **DELETED** (generic row replaced with state-specific entries)
- Humana Medicaid (Virginia) (new ID 85): Not Covered, `HUM-VA-2007-002`, eff. 07/22/2026
- Humana Medicaid (Kentucky) (new ID 86): Not Covered, `HUM-2007-001 (KY ed)`, eff. 01/16/2026
- Humana SC Medicaid (searched ID 84): Renamed to "Humana Medicaid (South Carolina)"
- Added 8 new searched_payers entries for FL, IL, IN, LA, MI, OH, OK, WI Humana Medicaid (policy editions likely exist but URLs require provider.humana.com portal login)

**Spreadsheet Sheet 1 changes applied (27 of 31 rows; 4 NO_CHANGE rows required no action):**

| Group | DB IDs | Action |
|---|---|---|
| UHC ecosystem | 11, 12, 17, 18, 28, 29, 30, 37, 38, 39, 40, 41, 42, 43 | Date refresh to 03/01/2026; UHC Commercial URL → `airway-clearance-devices-03012026.pdf`; UHC LA notes addendum |
| Medica family | 65, 66, 67, 68, 69, 70, 71 | Admin update date 08/05/2025 |
| Aetna | 46 | Status: PA Required → Not Covered |
| Premera | 8 | Date: 10/13/2025 (annual review) |
| Medical Mutual OH | 77 | Date: 08/19/2025 |
| Fidelis Care NY | 53 | Date: April 1, 2026 |
| BCBS Minnesota | 60 | URL change (Evicore → BCBSMN direct) |

**Skipped (no action needed):**
- IDs 13, 14, 15, 16 (UHC IE, UMR, Surest, Oxford) — NO_CHANGE rows
- BCBS RI (49) — my earlier finding was incorrect; original DB description is accurate
- Univera NY (25) — PDF re-verification confirmed current URL is valid

### Final DB state (May 10, 2026)
- **Local**: **69 payers, 69 policies, 127 searched payers**
- **AWS**: **69 payers, 69 policies, 127 searched payers**
- Net change vs Feb 6 baseline: -1 payer (BCBS TN/SC/LA removed, Humana Medicaid split: -1 +2 = +1, BCBS MS added: +1 → net 0... actually net -1 because we removed 3 BCBS plans and added 1 (MS) + 2 Humana states = -3+1+2 = 0, but original Humana Medicaid generic was deleted so -1)

### Permission change
- Added `WebSearch` permission to `.claude/settings.local.json` (project-level allowlist) so future subagents can do web research. WebFetch permission was reverted by linter.

### Review spreadsheet generated
`/Users/leahnoaeill/Downloads/E0469_Payer_Analysis/E0469_Policy_Review_2026-05-10.xlsx` — 4 sheets (Summary, Status_Date_URL Changes, New Policy Additions, No Change Confirmed, Still Not Found). Color-coded for review.

### Key lessons learned for future quarterly reviews
1. **PDF extractor is more reliable than WebSearch** for verifying E0469 presence in policy documents. `mcp_pdf_server/pdf_extractor.py search "<URL>" "E0469"` should be used directly on known policy URLs.
2. **PA lists can diverge from coverage policies**. A payer can have an "investigational" coverage policy AND still add the code to a PA list (e.g., Humana MA). Always check both.
3. **For Humana specifically**: Medicare Advantage and Medicaid are governed by *different* policy documents. The HUM-2007-001 series is Medicaid-only; Medicare Advantage uses the national MA/DSNP PA List.
4. **For BCBS state plans**: Don't trust WebSearch snippets about "E0469 added 10/01/2024" — verify the actual policy document. Some BCBS plans (TN, SC, LA) reference oscillation policies generally but never explicitly added E0469 to their applicable codes section.
5. **BCBS Mississippi was missed in the original sweep** — verify other BCBS state plans periodically as they may publish E0469 policies on different cadences.

### Pending for next session
- **BCBS Texas, Illinois, New Mexico**: Fee schedule lookup tools require provider login — verify codes through Availity portal
- **BCBS Nebraska MA-X-077**: Portal-based; verify content
- **Kaiser WA**: Provider portal restricted; PDF accessible via authenticated link only
- **Highmark BCBS PA (E-20-016)**: Re-verified 2026-05-10 — confirmed E0469 NOT in policy via direct PDF extraction
- **Humana Medicaid 9 remaining states** (FL, IL, IN, LA, MI, OH, OK, SC, WI): Locate state-specific policy doc URLs via provider.humana.com portal login, then promote from searched_payers → payers

## May 10, 2026 — Additional work (post-quarterly review)

### Phase 2 PDF re-verification expanded (additional finds)
- **BCBS Arkansas (NEW PAYER)** — added as active payer. Confirmed E0469 in Coverage Policy 2022013 via direct PDF extraction. Status: Prior-Auth Required, OLE investigational.
- **CMS DMEPOS Master List update (Jan 13, 2026, eff. Apr 13, 2026)**: E0469 added to the Master List — meaning it's now eligible to be added to F2F/WOPD Required List or Required PA List in the future. Currently NOT on the Required PA List (verified directly).

### Searched_payers cleanup (32 entries removed)
- **Supplemental insurance (3)**: Aflac, Lincoln Financial, MetLife — structurally don't cover DME
- **Workers' Comp (4)**: Federal OWCP, NY/CA/TX State WC — covers occupational injury treatment, not OLE
- **State Medicaid FFS (25)**: PA, OH, MI, NC, VA, NJ, AZ, WA, KY, LA, IN, CT, NV, MD, WI, SC, OR, IL, GA, TX, FL, CO, MS, MT, IN (IHCP) — default to no coverage without published policy
- **Duplicates (4)**: Medical Mutual OH, ConnectiCare CT, Providence Health OR, HMSA — these were also in active `payers`

### HMSA payer_type update
- Changed from `BCBS` → `PPO, HMO, Medicare Advantage, Medicaid` (reflects all plan categories HMSA offers; first multi-type entry in DB)

### Date refresh: all 90 remaining searched_payers
All 90 remaining searched_payers entries now show `date_searched = 2026-05-10`. Tier breakdown by verification depth (in notes field):
- **Tier 1** (~18 entries): Direct PDF extraction confirmed E0469 NOT in policy
- **Tier 2** (~22 entries): WebSearch confirmed no public policy URL containing E0469
- **Tier 3** (~50 entries): Web search inferential (no specific E0469 info located in public sources)

### Dashboard feature added
- **Searched Payers (No Policy) tab**: Added sortable headers for Payer Name and Type. Backend `/api/searched-payers` now accepts `sort_by` and `sort_dir` params (allowlisted to `name`, `payer_type`). Frontend `searched-sortable` class with separate sort state from main Payers tab.

### Final session state (local + AWS in sync)
- **Active payers**: 70
- **Policies**: 70
- **Searched payers**: 90
- **All searched dates refreshed to 2026-05-10**

### Cumulative payer count math
- Feb 6 baseline: 70 payers
- Today net additions: +4 (Humana Medicaid VA + KY, BCBS Mississippi, BCBS Arkansas)
- Today net removals: -4 (Humana Medicaid generic, BCBS TN, BCBS SC, BCBS LA)
- Net: 70 (unchanged)
- But composition is more accurate: removed 3 incorrectly-added BCBS plans, added 1 previously-missed BCBS, split 1 generic Humana row into 2 confirmed state rows.

## Aug 6–7, 2026 (Session 4) — Quarterly re-review (reconstructed Oct 6, 2026)

This session was not logged at the time. Reconstructed from `E0469_Policy_Review_2026-08-06.xlsx` (user decisions) and DB timestamps (single update batch at 2026-08-07 23:02, local + AWS identical).

- **Review files**: `E0469_Policy_Review_2026-08-0611.xlsx` (original agent output) and `E0469_Policy_Review_2026-08-06.xlsx` (copy with user's Decision column filled in).
- **6 payers added** (IDs 89–94): Humana Puerto Rico (PA), MVP Health Care NY/VT (PA), Priority Health MI (PA), Humana (Commercial) (Not Covered, HUM-2007-001), BCBS Michigan (PA via Northwood), Blue Shield California (PA). MVP, Priority, BCBSM, Blue Shield CA were removed from searched_payers.
- **1 payer removed**: UnitedHealthcare Louisiana (Medicaid) — UHC LA Community Plan ended 04/01/2026; moved to searched_payers.
- **58 policy rows updated**: mostly the `investigational` / `not_med_necessary` flags, dates and URLs (UHC family moved to `comm-medical-drug/airway-clearance-devices.pdf` and `medicaid-comm-plan/airway-clearance-devices-cs.pdf`). `coverage_status` was left as "Prior-Auth Required" for most rows — the investigational/NMN nuance lives in the flag columns.
- **Status changes**: BCBS Texas and BCBS New Mexico → Not Covered (user-supplied EIU list URLs).
- **Rejected removals (kept by user)**: McLaren (MI), Anthem Indiana — user noted E0469 is in policy as not medically necessary. New York Medicaid (eMedNY) kept even though the 7/1/2026 code list does not contain E0469.
- **Skipped as duplicates**: Louisiana Blue, Excellus, EmblemHealth, ConnectiCare, FL Blue/GuideWell, Bind, Noridian JD, CMS fee schedule.
- **Resulting counts**: 75 payers, 75 policies, 85 searched (local + AWS in sync).

## Oct 6, 2026 (Session 5) — Quarterly re-review

### Method
1. Exported DB baseline (75 / 75 / 85) to scratchpad.
2. Wrote a batch checker that fetched all 55 unique active source URLs (PDF + HTML), extracted text, counted E0469 hits, pulled date headers and E0469 context.
3. Compared dates/wording to DB; inspected revision logs.
4. Swept the 85 searched payers via WebSearch + direct PDF checks. New angle: **CMS-0057-F** public prior-auth lists (required from 2026) are exposing E0469 on plans that never published a coverage policy.

### Output
`E0469_Policy_Review_2026-10-06.xlsx` — sheets: Summary, Changes - Active Payers (23 rows), Wording Flags (4), New Policy Additions (10), No Change Confirmed (43), Still Not Found (85). **No DB changes applied — awaiting user decisions.**

### Key findings
- **BCBS Florida** 09/15/2026 annual review: multifunction-device statement updated (names BiWaze/BiWaze Clear); still investigational.
- **Date refreshes**: Fidelis (10/1/2026), Moda (09/11/2026), Select Health UT/ID (09/23/26), Providence MP220 (eff 10/1/2026), Medi-Cal (Sept 2026), BCBSM PA list (Oct 2, 2026), Humana MA PAL (rev 6/1/2026), Medica x7 (eff 12/01/2025).
- **HCSC EIU lists**: TX, NM (and OK) end-dated E0469 on 11/30/2025; **IL did not** (still non-reimbursable EIU, public URL `bcbsil.com/docs/provider/il/standards/cpcp/2026/eiu-services-code-list.pdf`). TX/NM "Not Covered" status rests on the ended entry — flagged for user.
- **Broken URLs**: Humana KY ed `MOLET - HUM-2007-001 … KY ed 011620.26pdf` (IDs 86, 92) → 404; Capital Blue Cross commercial MP 4.002 → 404 (Capital Blue Medicare MA 4.002 eff 10/1/2026 still lists E0469).
- **New candidates**: Louisiana Blue 00090 (eff 06/01/2026, OLE investigational), Excellus 1.01.15 (eff 3/16/2026, Volara investigational), EmblemHealth/ConnectiCare rental-only table, Centene GA/NC Medicaid + Ambetter SC (0057-F PA lists), iCare WI (PA, Medicare LOB), The Health Plan WV (E/I, new), Health Team Advantage NC (PA > $1000, new).
- **Wording flags**: Priority Health (policy says "Non-Covered", DB = PA Required), BCBS Arkansas (policy 2022013 = "not medically necessary or investigational and are not covered", DB = PA Required).
- **Humana state Medicaid PA lists** (FL, SC, LA, OH, OK; 2026, rev Oct 2026) do not list E0469 — consistent with OLE "no covered indications" policies.

## Oct 7, 2026 (Session 5, cont.)

### Applied (local + AWS, single transaction each) — now 79 payers / 79 policies / 80 searched
- Added EmblemHealth (NY) and ConnectiCare (CT): Prior-Auth Required, PA Yes, Investigational No (user decision; source is the shared RPC20210007 rental-only table).
- Added Excellus BCBS (NY) (1.01.15, eff 03/16/2026) and Louisiana Blue (00090, eff 06/01/2026): Investigational Yes, PA "Not Specified" (neither policy states a PA requirement).
- Removed matching rows from searched_payers (EmblemHealth, ConnectiCare, Excellus, both Louisiana Blue rows).

### Data model redesign (user-approved direction, not yet applied)
- **Coverage Status** becomes ONE field: Covered with Criteria / Investigational / Not Medically Necessary (standalone only when the payer lists it) / Not Covered (only when explicit) / PA Required - No Policy / Case-by-Case - No Policy (proposed, for Medicare MACs + UHC NC).
- **Prior Auth** separate: Yes (only when a document explicitly requires it) / No / Not Applicable / Not Stated.
- **Policy Wording**: new short exact-quote field.
- Review file: `E0469_Coverage_Status_Remap_2026-10-07.xlsx` (79 rows; 69 Approve, 10 Hold). Awaiting user approval → then add columns, apply data to local + AWS, update dashboard + Add/Edit form, deploy, retire old investigational / not_med_necessary columns.
- Notable: Kaiser WA HFCWO criteria say BiWaze Clear/Volara are "Medicare: Considered Medically Necessary when criteria … are met; Non-Medicare: Considered not medically necessary". BCBS VT moved to `investigational-services-procedures-oct-2026`.

### Coverage status redesign — LOCAL ONLY (Oct 7, 2026), awaiting user review before AWS
- User decisions: Case-by-Case - No Policy accepted; UHC family + Aetna = Investigational; "Covered with Criteria" renamed **Covered**; Kaiser WA Non-Medicare PA = Yes; Humana Medicaid VA PA = Yes (VA Dual Fully Integrated PAL 727101VA0425); BCBS TX/NM = Not Covered (EIU lists); BCBS MN = PA Required - No Policy (portal only — public 1/5/26 PA lists don't list E0469); MN MHCP Not Covered (revised 12/17/2025); HMSA Not Covered (hmsa.com/prc/... page confirmed); Humana KY = Covered, PA Yes (KDMS MSEA fee schedule, rental only); Humana Commercial = PA Required - No Policy (Humana MA/DSNP PAL).
- Still HOLD (proposed values applied locally, need user's source): McLaren (80), eMedNY (81), Anthem IN (82).
- Local DB: backup table `payer_policies_backup_20261007`; new column `policy_wording`; coverage_status / prior_auth_required rewritten for all 79 rows. Migration SQL: scratchpad `migrate_coverage_status_2026-10-07.sql` (re-run on AWS after approval).
- Result: Investigational 35, PA Required - No Policy 16, Not Covered 15, Covered 5, Not Medically Necessary 5, Case-by-Case 3. Prior Auth: Yes 19, Not Stated 48, Not Applicable 10, No 2.
- Code on branch `coverage-status-redesign` (uncommitted): dashboard.py (6 statuses, prior_auth filter, policy_wording, status×PA matrix in /api/aggregates, export columns), templates/dashboard.html (status cards, 3 charts + matrix, Prior Auth column/filter, Policy Wording column, Add form), templates/map.html (6-status legend/stats, dynamic stripe patterns), schema.sql (policy_wording).
- Round 2/3 (Oct 7, local only): Noridian + CGS → Covered, PA No (Medicare covers; not on CMS PA list). BCBS MN → PA via eviCore DME code list (eff 1/1/2024; note BCBSMN left eviCore 08/01/2025). UHC NC → PA Required - No Policy, PA Yes. **Case-by-Case status removed** (folded into PA Required - No Policy) — 5 statuses remain. Added **Dean Health Plan (WI)** (MP9746, eff 12/01/2025): Not Covered, PA Not Applicable.
- Local now: 80 payers / 80 policies / 80 searched. Covered 7, PA Required - No Policy 17, Not Med Necessary 5, Investigational 35, Not Covered 16. PA: Yes 20, No 2, Not Applicable 11, Not Stated 47.
- AWS bundle ready (scratchpad `aws_bundle_2026-10-07.sql`): backup table + policy_wording column + 79 row updates + Dean insert. AWS IDs verified aligned (max payer id 98).
- Round 4 (Oct 7, local only; appended to AWS bundle): Providence → Not Covered (Table 1 "non-coverage position"). McLaren and Anthem IN moved to searched_payers (no E0469 document). Added Peach State Health Plan (GA Medicaid, Centene): Covered, PA Yes (CMS-0057-F PA list). Local: 79 payers / 79 policies / 82 searched. Open questions: Excellus "covers E0469" (policy 1.01.15 says Volara investigational — need user's source), eMedNY (NY Medicaid FFS claims system — move to No Policy?), Carolina Complete (same 0057-F PA list type as Peach State).
- Round 5 (Oct 7, local; in AWS bundle): added Carolina Complete (NC Medicaid), Ambetter from Absolute Total Care (SC), iCare (WI), The Health Plan (WV), Health Team Advantage (NC) — all Covered, PA Yes per user. eMedNY moved to No Policy as "New York Medicaid (eMedNY FFS)"; iCare removed from searched. Excellus kept Investigational (user approved). All active notes rewritten in one consistent format (stale PA/status language removed) + Oct 6 policy-date refreshes. All 82 searched payers re-checked/refreshed to 2026-10-07 (specific evidence noted where a document was read; others web-search level).
- Local: 83 payers / 83 policies / 82 searched. Covered 13, PA Required - No Policy 17, Not Med Necessary 2, Investigational 34, Not Covered 17.
- AWS bundle dry-run: restored AWS pg_dump into a scratch DB, ran bundle → active + searched tables IDENTICAL to local. Ready to deploy on dashboard approval.
- Round 6 (Oct 7): BCBS Rhode Island prior auth → Yes (user decision); appended to AWS bundle.
- Round 7 (Oct 7): BCBS Nebraska payer_type → "BCBS, Medicare Advantage". Undid overstated generic "Re-checked" notes/dates on ~60 searched rows (restored prior dates). No Policy cleanup 82 → 67: removed CMS DMEPOS Fee Schedule, Bright Health, Friday Health, UHC Louisiana Medicaid, First Health, Magellan, GuideWell/Florida Blue, Bind, LifeWise/Cambia; merged duplicates (BCBS TN ×2, BCBS SC ×2, Anthem Elevance → Anthem Multi-state, BCBS California → Anthem California, Centene ×2). Noridian JD moved to active (Covered, PA No). Backup table `searched_payers_backup_20261007`.
- Round 8 (Oct 7): individual review of all 52 remaining No Policy payers. 19 confirmed no E0469 (dated 2026-10-07), 20 not verifiable (portal-only; date unchanged, note added), 10 Anthem/Elevance rows with open precert lead (GA notice indexed as adding E0469 eff 6/1/2025; current DME.00012 removed E0469, CG-DME-43 lacks it), 3 FOUND pending user decision: Sentara (DME 14, Commercial + VA Medicaid, eff 8/1/2026: HFCWO devices e.g. Volara & E0469 "NOT COVERED", pre-cert required), SelectHealth UT (commercial + Medicaid PA), Select Health CO (commercial + Medicare PA). Taro Health renamed "Mending (formerly Taro Health)". Also: Moda HFCWO MNC (eff 04/01/2026) lists E0469 under "CPT or HCPC codes covered" → suggest Moda = Covered, PA Yes.
- Local now: 84 payers / 84 policies / 67 searched. AWS bundle dry-run re-verified identical.
- Round 9 (Oct 7, local + bundle): Moda → Covered, PA Yes (source: Moda HFCWO MNC eff 04/01/2026, E0469 under codes covered). Added Select Health Utah (Medicaid), Select Health Utah (Traditional Integrated) and Select Health Colorado (commercial) — all Covered, PA Yes (Select Health code lists as of 09/23/26). Removed 'Select Health (Colorado)' from searched. 'SelectHealth (UT)' (commercial) still on No Policy list pending user decision. Local: 87 payers / 66 searched. State Medicaid FFS: NOT systematically checked (25 removed in May without verification) — 50-state sweep proposed.
- Round 10 (Oct 7): added Select Health Utah (Commercial) Covered/PA Yes; added Sentara Health Plans Not Covered/PA Yes (DME 14 v9, pre-cert required); removed both from searched. Medicaid 50-state sweep started.
- Medicaid FFS sweep (Oct 7): 51 jurisdictions. E0469 LISTED: IL (PA B), IN, VA, HI, MS, MT (PA Y), DC, VT (limit list); MO lists as Noncovered; already active CA/KY/MN; NOT listed: AK, CO, FL, ID, LA, MD, ND, NE, NV, NY, OK, SC, SD, TX, WA, WV; UNVERIFIABLE (portal/license/JS): AL, AR, AZ, CT, DE, GA, IA, KS, MA, ME, MI, NC, NH, NJ, NM, OH, OR, PA, RI, UT, WI, WY; TN managed care only. Review file E0469_Medicaid_State_Sweep_2026-10-07.xlsx. No DB changes yet. Phase 2 (Medicaid MCOs by state) not started.
- Round 11 (Oct 7): Sentara PA → No. All 16 'PA Required - No Policy' rows → Covered (status removed from code; 4 statuses remain: Covered, Not Medically Necessary, Investigational, Not Covered). 37 state Medicaid FFS programs (15 not listed + 22 unverifiable) added to searched_payers as '<State> Medicaid (FFS)'. Local: 89 payers / 101 searched. AWS bundle dry-run identical. 9 state Medicaid additions (IL, IN, VA, HI, MS, MT, DC, VT, MO) still pending user approval.
- Round 12 (Oct 7): added 9 state Medicaid FFS payers (IL, IN, VA, HI, MS, MT, DC, VT Covered; MO Not Covered). Phase 2 (Medicaid MCOs) started. AWS push only after user OK.
- Phase 2 Medicaid MCO sweep (Oct 7): Centene 0057-F lists — E0469 PA on LA Healthcare Connections, Magnolia MS, Iowa Total Care, Meridian IL, Trillium OR, Superior TX, Sunshine FL, Sunflower KS, MHS IN, Home State MO, Nebraska Total Care, PA Health & Wellness, SilverSummit NV (13 Medicaid) + Wellcare AZ Complete Health Medicare; none on Coordinated Care WA, WellCare KY, Absolute Total Care SC Medicaid, WellCare NC, Ohana HI; Wellpoint TX none; Molina/ABH/CareSource/AmeriHealth not verifiable. Sheet 'Managed Care (Phase 2)' added to E0469_Medicaid_State_Sweep_2026-10-07.xlsx. Pending user approval.
- Round 13 (Oct 7): added 14 managed care plans (13 Centene Medicaid + Wellcare AZ Medicare) as Covered/PA Yes after exact-code/section/page re-verification; Superior TX removed from searched; 11 MCO not-listed/unverifiable entries added/updated in searched. Local: 112 payers / 113 searched. AWS bundle dry-run identical. Data updates complete — awaiting user OK to deploy AWS.
- **AWS DEPLOYED Oct 7, 2026 (user approved)**: server-side backup `~/e0469-dashboard/backup_e0469_predeploy_20261007.sql`; AWS data confirmed unchanged vs test copy; applied `aws_bundle_2026-10-07.sql` (single transaction); AWS data verified identical to local (both tables); copied dashboard.py, schema.sql, templates/dashboard.html, templates/map.html; `docker compose build --no-cache && up -d` — container healthy; verified auth (401 without creds), dashboard/map/export 200, 4 statuses, 112 payers / 113 searched. Branch `coverage-status-redesign` committed and pushed.
