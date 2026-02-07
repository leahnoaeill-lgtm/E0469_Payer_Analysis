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

### Current Database Counts:
- **Local**: 70 payers, 70 policies, 116 searched
- **AWS**: 70 payers, 70 policies, 116 searched
- **Pending re-verification**: BCBS Massachusetts, Cigna (may need re-adding — agents found updated policies with E0469)
- **Behind secure portals** (need manual verification): Highmark BCBS PA (E-20-016), Arkansas BCBS (Policy 2022013)
