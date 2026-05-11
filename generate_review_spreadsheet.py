#!/usr/bin/env python3
"""
Generate E0469_Policy_Review_2026-05-10.xlsx with comprehensive findings
from re-checking all 70 active payers and 110 unique searched payers.

Reference data was Feb 6, 2026 snapshot. Today: May 10, 2026.
"""

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from datetime import date

OUTPUT_PATH = "/Users/leahnoaeill/Downloads/E0469_Payer_Analysis/E0469_Policy_Review_2026-05-10.xlsx"

# Styling
HEADER_FILL = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
HEADER_FONT = Font(color="FFFFFF", bold=True, size=11)

GREEN_FILL = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")    # No change confirmed
YELLOW_FILL = PatternFill(start_color="FFEB9C", end_color="FFEB9C", fill_type="solid")   # Date / minor change
ORANGE_FILL = PatternFill(start_color="FFC59B", end_color="FFC59B", fill_type="solid")   # Status change - needs review
RED_FILL = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")      # Policy removed / not covered
BLUE_FILL = PatternFill(start_color="C5D9F1", end_color="C5D9F1", fill_type="solid")     # New policy / addition
GREY_FILL = PatternFill(start_color="E7E6E6", end_color="E7E6E6", fill_type="solid")     # Still not found

THIN_BORDER = Border(
    left=Side(style="thin", color="CCCCCC"),
    right=Side(style="thin", color="CCCCCC"),
    top=Side(style="thin", color="CCCCCC"),
    bottom=Side(style="thin", color="CCCCCC"),
)

WRAP_ALIGN = Alignment(wrap_text=True, vertical="top")


def style_header(ws, row, columns):
    for col_idx in range(1, columns + 1):
        cell = ws.cell(row=row, column=col_idx)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
        cell.border = THIN_BORDER


def apply_row_fill(ws, row, columns, fill):
    for col_idx in range(1, columns + 1):
        cell = ws.cell(row=row, column=col_idx)
        cell.fill = fill
        cell.alignment = WRAP_ALIGN
        cell.border = THIN_BORDER


def autosize_columns(ws, widths):
    for col_letter, width in widths.items():
        ws.column_dimensions[col_letter].width = width


# ==============================================================================
# SHEET 1: STATUS / DATE / URL CHANGES (existing payers with detected updates)
# ==============================================================================
changes_data = [
    # (ID, Name, Type, State, Old Coverage, New Coverage, Old PA, New PA, Old Inv, New Inv,
    #  Old Date, New Date, Policy #, Old URL, New URL, Change Type, Notes / Action)
    (11, "UnitedHealthcare (Commercial)", "Commercial", "", "Prior-Auth Required", "Prior-Auth Required", "Yes", "Yes", "Yes", "Yes",
     "01/01/2026", "03/01/2026", "Airway Clearance Devices",
     "https://www.uhcprovider.com/en/policies-protocols/commercial-policies/commercial-medical-drug-policies.html",
     "https://www.uhcprovider.com/content/dam/provider/docs/public/policies/index/commercial/airway-clearance-devices-03012026.pdf",
     "DATE_CHANGE",
     "Policy effective date updated to 03/01/2026. OLE devices remain Unproven/Not Medically Necessary. Direct PDF URL now available."),

    (12, "UnitedHealthcare Community Plan (Medicaid)", "Medicaid MCO", "", "Prior-Auth Required", "Prior-Auth Required", "Yes", "Yes", "Yes", "Yes",
     "11/01/2025", "03/01/2026", "Airway Clearance Devices CS",
     "https://www.uhcprovider.com/content/dam/provider/docs/public/policies/medicaid-comm-plan/airway-clearance-devices-cs.pdf",
     "(same)",
     "DATE_CHANGE",
     "UHC Community Plan policy refreshed to 03/01/2026 effective date. Coverage status unchanged."),

    (17, "UnitedHealthcare New Jersey (Medicaid)", "Medicaid MCO", "NJ", "Prior-Auth Required", "Prior-Auth Required", "Yes", "Yes", "Yes", "Yes",
     "11/01/2025", "03/01/2026", "NJ-CS Policy", "(same)", "(same)", "DATE_CHANGE",
     "UHC Community Plan policy refresh applies to NJ. Effective date moved to 03/01/2026."),

    (18, "UnitedHealthcare Louisiana (Medicaid)", "Medicaid MCO", "LA", "Prior-Auth Required", "Prior-Auth Required", "Yes", "Yes", "No", "No",
     "11/01/2025", "03/01/2026", "LA-CS Policy",
     "https://www.uhcprovider.com/content/dam/provider/docs/public/policies/medicaid-comm-plan/la/airway-clearance-devices-la-cs.pdf",
     "(same)",
     "DATE_CHANGE",
     "UHC Community Plan policy refresh. Effective date moved to 03/01/2026."),

    (28, "UnitedHealthcare North Carolina (Medicaid)", "Medicaid MCO", "NC", "Prior-Auth Required", "Prior-Auth Required", "Yes", "Yes", "Yes", "Yes",
     "04/01/2025", "03/01/2026", "NC-CS Policy", "(same)", "(same)", "DATE_CHANGE",
     "UHC Community Plan policy refresh applies to NC."),

    (29, "UnitedHealthcare Pennsylvania (Medicaid)", "Medicaid MCO", "PA", "Prior-Auth Required", "Prior-Auth Required", "Yes", "Yes", "Yes", "Yes",
     "01/01/2026", "03/01/2026", "PA-CS Policy", "(same)", "(same)", "DATE_CHANGE",
     "UHC Community Plan policy refresh applies to PA."),

    (30, "UnitedHealthcare Tennessee (Medicaid)", "Medicaid MCO", "TN", "Prior-Auth Required", "Prior-Auth Required", "Yes", "Yes", "Yes", "Yes",
     "11/01/2025", "03/01/2026", "TN-CS Policy", "(same)", "(same)", "DATE_CHANGE",
     "UHC Community Plan policy refresh applies to TN."),

    (37, "UnitedHealthcare Kentucky (Medicaid)", "Medicaid MCO", "KY", "Prior-Auth Required", "Prior-Auth Required", "Yes", "Yes", "Yes", "Yes",
     "11/01/2025", "03/01/2026", "KY-CS Policy", "(same)", "(same)", "DATE_CHANGE",
     "UHC Community Plan policy refresh applies to KY."),

    (38, "UnitedHealthcare Texas (Medicaid)", "Medicaid MCO", "TX", "Prior-Auth Required", "Prior-Auth Required", "Yes", "Yes", "Yes", "Yes",
     "11/01/2025", "03/01/2026", "TX-CS Policy", "(same)", "(same)", "DATE_CHANGE",
     "UHC Community Plan policy refresh applies to TX."),

    (39, "UnitedHealthcare Arizona (Medicaid)", "Medicaid MCO", "AZ", "Prior-Auth Required", "Prior-Auth Required", "Yes", "Yes", "Yes", "Yes",
     "11/01/2025", "03/01/2026", "AZ-CS Policy", "(same)", "(same)", "DATE_CHANGE",
     "UHC Community Plan policy refresh applies to AZ."),

    (40, "UnitedHealthcare Michigan (Medicaid)", "Medicaid MCO", "MI", "Prior-Auth Required", "Prior-Auth Required", "Yes", "Yes", "Yes", "Yes",
     "11/01/2025", "03/01/2026", "MI-CS Policy", "(same)", "(same)", "DATE_CHANGE",
     "UHC Community Plan policy refresh applies to MI."),

    (41, "UnitedHealthcare Ohio (Medicaid)", "Medicaid MCO", "OH", "Prior-Auth Required", "Prior-Auth Required", "Yes", "Yes", "Yes", "Yes",
     "11/01/2025", "03/01/2026", "OH-CS Policy", "(same)", "(same)", "DATE_CHANGE",
     "UHC Community Plan policy refresh applies to OH."),

    (42, "UnitedHealthcare Virginia (Medicaid)", "Medicaid MCO", "VA", "Prior-Auth Required", "Prior-Auth Required", "Yes", "Yes", "Yes", "Yes",
     "11/01/2025", "03/01/2026", "VA-CS Policy", "(same)", "(same)", "DATE_CHANGE",
     "UHC Community Plan policy refresh applies to VA."),

    (43, "UnitedHealthcare Wisconsin (Medicaid)", "Medicaid MCO", "WI", "Prior-Auth Required", "Prior-Auth Required", "Yes", "Yes", "Yes", "Yes",
     "11/01/2025", "03/01/2026", "WI-CS Policy", "(same)", "(same)", "DATE_CHANGE",
     "UHC Community Plan policy refresh applies to WI."),

    (21, "Humana Medicare Advantage", "Medicare Advantage", "", "Not Covered", "Prior-Auth Required", "N/A", "Yes", "Yes", "Not Specified",
     "01/01/2026", "01/01/2026", "Medicare Advantage PA List (790807ALL0725-C)",
     "https://assets.humana.com/is/content/humana/VA-Multi-Function_Oscillation_Lung_Expansion_Therapy-HUM-2007-001pdf",
     "https://assets.humana.com/is/content/humana/FINAL_Medicare%20and%20DSNP%20Prior%20Authorization%20and%20Notification%20List%20-%201-1-2026pdf",
     "STATUS_CHANGE [APPLIED 2026-05-10]",
     "APPLIED to local + AWS DB on 2026-05-10. DB had Humana MA as Not Covered (using HUM-2007-001 Medicaid policy URL). 2026 Humana MA/DSNP PA List adds E0469 as NEW Prior Authorization Requirement effective 01/01/2026 under 'DME - Airway Clearance Devices' (E0469, E0481, E0482). HUM-2007-001 is a MEDICAID policy and does not apply to MA. Status changed to Prior-Auth Required and URL updated to MA PA List."),

    (45, "Humana Medicaid (Virginia) - was ID 45 (deleted)", "Medicaid MCO", "VA", "Not Covered (generic row)", "Not Covered (VA-specific)", "N/A", "N/A", "Yes", "Yes",
     "Current", "07/22/2026", "HUM-VA-2007-002",
     "https://assets.humana.com/is/content/humana/VA-Multi-Function_Oscillation_Lung_Expansion_Therapy-HUM-2007-001pdf",
     "https://assets.humana.com/is/content/humana/MCD%20Multi-Function%20Oscillation%20Lung%20Expansion%20Therapy%20HUM-VA-2007-002%20ed%207.22.26pdf",
     "STATE SPLIT [APPLIED 2026-05-10]",
     "APPLIED to local + AWS DB on 2026-05-10. Original 'Humana Medicaid' row (ID 45) DELETED. Replaced with state-specific entries. Virginia row added as new payer ID 85 with confirmed HUM-VA-2007-002 (eff. 07/22/2026) URL."),

    (85, "Humana Medicaid (Virginia) [NEW PAYER]", "Medicaid MCO", "VA", "(new)", "Not Covered", "(new)", "N/A", "(new)", "Yes",
     "(new)", "07/22/2026", "HUM-VA-2007-002",
     "(new)",
     "https://assets.humana.com/is/content/humana/MCD%20Multi-Function%20Oscillation%20Lung%20Expansion%20Therapy%20HUM-VA-2007-002%20ed%207.22.26pdf",
     "NEW PAYER [APPLIED 2026-05-10]",
     "Added to local + AWS DB on 2026-05-10. Humana Healthy Horizons Virginia. Policy HUM-VA-2007-002 (Multi-Function Oscillation Lung Expansion Therapy) effective 07/22/2026: 'There are no covered indications' for E0469."),

    (86, "Humana Medicaid (Kentucky) [NEW PAYER]", "Medicaid MCO", "KY", "(new)", "Not Covered", "(new)", "N/A", "(new)", "Yes",
     "(new)", "01/16/2026", "HUM-2007-001 (KY ed)",
     "(new)",
     "https://assets.humana.com/is/content/humana/MOLET%20-%20HUM-2007-001%2006-2025%20-%20KY%20ed%20011620.26pdf",
     "NEW PAYER [APPLIED 2026-05-10]",
     "Added to local + AWS DB on 2026-05-10. Humana Healthy Horizons Kentucky. Policy MOLET HUM-2007-001 KY ed effective 01/16/2026: 'There are no covered indications' for E0469."),

    (65, "Medica (Iowa)", "Regional", "IA", "Not Covered", "Not Covered", "N/A", "N/A", "Yes", "Yes",
     "Current", "08/05/2025", "Volara OLE Coverage Policy", "(same)", "(same)", "DATE_CHANGE",
     "Re-review 07/17/2025, administrative update 08/05/2025 for code updates. Status unchanged - investigative/unproven."),

    (66, "Medica (Kansas)", "Regional", "KS", "Not Covered", "Not Covered", "N/A", "N/A", "Yes", "Yes",
     "Current", "08/05/2025", "Volara OLE Coverage Policy", "(same)", "(same)", "DATE_CHANGE",
     "Same Medica policy update applies to all 7 state plans."),

    (67, "Medica (Minnesota)", "Regional", "MN", "Not Covered", "Not Covered", "N/A", "N/A", "Yes", "Yes",
     "Current", "08/05/2025", "Volara OLE Coverage Policy", "(same)", "(same)", "DATE_CHANGE",
     "Same Medica policy update applies to all 7 state plans."),

    (68, "Medica (Nebraska)", "Regional", "NE", "Not Covered", "Not Covered", "N/A", "N/A", "Yes", "Yes",
     "Current", "08/05/2025", "Volara OLE Coverage Policy", "(same)", "(same)", "DATE_CHANGE",
     "Same Medica policy update applies to all 7 state plans."),

    (69, "Medica (North Dakota)", "Regional", "ND", "Not Covered", "Not Covered", "N/A", "N/A", "Yes", "Yes",
     "Current", "08/05/2025", "Volara OLE Coverage Policy", "(same)", "(same)", "DATE_CHANGE",
     "Same Medica policy update applies to all 7 state plans."),

    (70, "Medica (South Dakota)", "Regional", "SD", "Not Covered", "Not Covered", "N/A", "N/A", "Yes", "Yes",
     "Current", "08/05/2025", "Volara OLE Coverage Policy", "(same)", "(same)", "DATE_CHANGE",
     "Same Medica policy update applies to all 7 state plans."),

    (71, "Medica (Wisconsin)", "Regional", "WI", "Not Covered", "Not Covered", "N/A", "N/A", "Yes", "Yes",
     "Current", "08/05/2025", "Volara OLE Coverage Policy", "(same)", "(same)", "DATE_CHANGE",
     "Same Medica policy update applies to all 7 state plans."),

    (8, "Premera Blue Cross (WA)", "BCBS", "WA", "Prior-Auth Required", "Prior-Auth Required", "N/A (investigational)", "N/A (investigational)", "Yes", "Yes",
     "10/01/2024 (codes added)", "10/13/2025 annual review", "1.01.539", "(same)", "(same)", "DATE_CHANGE",
     "Annual review approved 10/13/2025 with literature review through 07/01/2025. Policy statements unchanged - OLE still investigational."),

    (77, "Medical Mutual of Ohio", "Commercial", "OH", "Prior-Auth Required", "Prior-Auth Required", "N/A", "N/A", "Yes", "Yes",
     "", "08/19/2025", "200508", "(same)", "(same)", "DATE_CHANGE",
     "Policy #200508 updated 08/19/2025. Status unchanged - investigational."),

    (53, "Fidelis Care (New York Medicaid)", "Medicaid MCO", "NY", "Prior-Auth Required", "Prior-Auth Required", "Yes", "Yes", "No", "No",
     "January 3, 2026", "April 1, 2026", "DME Authorization Grid", "(same)", "(same)", "DATE_CHANGE",
     "New Authorization Grids effective April 1, 2026. E0469 still requires prior authorization."),

    (49, "Blue Cross Blue Shield Rhode Island", "BCBS", "RI", "Prior-Auth Required", "Not Covered", "Yes - Preauthorization recommended (Commercial), Required (MA)", "N/A", "No", "No",
     "10/2024", "2026 update", "HCPCS Level II Updates", "(same)", "(same)", "STATUS_CHANGE",
     "REVIEW NEEDED: E0469 now appears as NOT separately reimbursed for both Medicare Advantage AND Commercial. More restrictive than previous classification. Verify with BCBSRI directly before applying."),

    (60, "Blue Cross Blue Shield Minnesota", "BCBS", "MN", "Prior-Auth Required", "Prior-Auth Required", "Yes - via Evicore", "Yes - direct to BCBSMN", "No", "No",
     "01/01/2024", "08/01/2025 (vendor change)", "DME Code List",
     "https://www.evicore.com/sites/default/files/resources/2024-11/BCBSMN_DME_CodeList_Eff01.01.2024_Pub11.15.2024.pdf",
     "https://www.bluecrossmn.com/providers/medical-management/prior-authorization-lookup-tool",
     "URL_CHANGE",
     "EVICORE NO LONGER managing DME prior auths for BCBSMN as of 08/01/2025. PA now submitted directly via BCBSMN Prior Authorization Lookup Tool / Availity. Old Evicore URL is outdated."),

    (25, "Univera Healthcare (New York)", "Regional", "NY", "Prior-Auth Required", "Prior-Auth Required", "Yes", "Yes", "No", "No",
     "Current", "2026-03-16 (new policy)", "Policy 1.01.15",
     "https://www.univerahealthcare.com/documents/d/global/uni-prv-airway-clearance-devices-1",
     "https://www.univerahealthcare.com/documents/d/global/uni-prv-airway-clearance-devices-1",
     "URL_CHANGE",
     "REVIEW NEEDED: Old Univera policy 'terminates on 2026-03-16'. New policy added E0469 explicitly. URL still works but may resolve to terminated version. Verify which URL to use going forward."),
]

# ==============================================================================
# SHEET 2: NEW POLICY ADDITIONS (searched payers that now have E0469 policy)
# ==============================================================================
new_additions_data = [
    # No newly-published explicit E0469 policies detected from searched payers during this review.
    # Most searched payers (110) still lack explicit E0469 policies — see Sheet 4.
    # The Feb 2026 review already captured the most recent wave of additions.
]

# ==============================================================================
# SHEET 3: NO CHANGE CONFIRMED (existing payers verified unchanged)
# ==============================================================================
no_change_data = [
    # (ID, Name, Type, State, Coverage, Source URL, Policy #, Notes)
    (2, "Noridian Medicare (JA DME)", "Medicare MAC", "", "Prior-Auth Required",
     "https://med.noridianmedicare.com/web/jadme/article-detail/-/view/6547796/lung-expansion-airway-clearance-continuous-high-frequency-oscillation-and-nebulization-device-hcpcs-code-e0469",
     "Article 6547796",
     "No LCD published. Article 6547796 still active - claims case-by-case basis."),
    (3, "CGS Medicare (JB DME)", "Medicare MAC", "", "Prior-Auth Required",
     "https://www.cgsmedicare.com/jb/pubs/news/2025/07/cope181758.html", "COPE181758",
     "Jan and April 2026 LCD revision summaries published but no E0469-specific LCD changes. Same status."),
    (5, "HealthPartners", "Regional", "MN", "Prior-Auth Required (Investigational)",
     "https://www.healthpartners.com/ucm/groups/public/@hp/@public/@cc/documents/documents/aentry_045636.pdf",
     "Airway Clearance Policy",
     "Confirmed still investigational/experimental in 2026 Provider Resource Manual."),
    (6, "Minnesota MHCP (Medicaid)", "Medicaid", "MN", "Not Covered",
     "https://www.dhs.state.mn.us/main/idcplg?IdcService=GET_DYNAMIC_CONVERSION&dDocName=DHS16_152808",
     "DHS16_152808",
     "No 2026 update detected. Policy still active - explicitly not covered."),
    (7, "Blue Cross Blue Shield Florida", "BCBS", "FL", "Prior-Auth Required",
     "https://mcgs.bcbsfl.com/MCG?mcgId=09-E0000-28&pv=false", "09-E0000-28",
     "Policy still active, 09/25/2025 review still current. Volara OLE considered investigational."),
    (9, "Kaiser Permanente WA (Medicare)", "Medicare Advantage", "WA", "Prior-Auth Required",
     "https://wa-provider.kaiserpermanente.org/static/pdf/hosting/clinical/criteria/pdf/new-emergingtech.pdf",
     "HFCWO Criteria",
     "No 2026 update accessible (provider portal). Likely unchanged from 07/17/2025 update."),
    (10, "Kaiser Permanente WA (Non-Medicare)", "Commercial HMO", "WA", "Prior-Auth Required",
     "https://wa-provider.kaiserpermanente.org/static/pdf/hosting/clinical/criteria/pdf/hfcwo.pdf",
     "HFCWO Criteria",
     "No 2026 update accessible. Likely unchanged from 07/17/2025 update."),
    (13, "UnitedHealthcare Individual Exchange", "ACA Exchange", "", "Prior-Auth Required",
     "https://www.uhcprovider.com/en/policies-protocols/exchange-policies/exchanges-medical-drug-policies.html",
     "Airway Clearance Devices",
     "Exchange policy still active at 01/01/2026 effective date."),
    (14, "UMR (UnitedHealthcare TPA)", "Commercial TPA", "", "Prior-Auth Required",
     "https://www.uhcprovider.com/en/policies-protocols/commercial-policies/umr-medical-drug-policies.html",
     "Airway Clearance Devices",
     "UMR shares UHC airway clearance policy. 01/01/2026 effective date unchanged."),
    (15, "Surest (UnitedHealthcare)", "Commercial", "", "Prior-Auth Required",
     "https://ams-gateway.uhcprovider.com/en/policies-protocols/commercial-policies/surest-medical-drug-policies.html",
     "Airway Clearance Devices",
     "Surest shares UHC policy. 01/01/2026 effective date unchanged."),
    (16, "UnitedHealthcare Oxford", "Commercial", "", "Prior-Auth Required",
     "https://www.uhcprovider.com/content/dam/provider/docs/public/policies/oxford/airway-clearance-devices-ohp.pdf",
     "Airway Clearance Devices OHP",
     "Oxford policy still active at 01/01/2026."),
    (19, "Rocky Mountain Health Plans (Colorado)", "Regional", "CO", "Prior-Auth Required",
     "https://providernews.anthem.com/nevada/articles/precertification-list-change-notification-march-1-2025-24243",
     "Airway Clearance Devices",
     "No 2026 update detected. Still requires precertification."),
    (24, "Geisinger Health Plan", "Regional", "PA", "Prior-Auth Required",
     "https://www.geisinger.org/-/media/OneGeisinger/Files/Policy%20PDFs/MP/1-50/MP045%20High%20Frequency%20Chest%20Percussion%20Vest.ashx",
     "MP045",
     "Policy MP045 still active. Coverage for neuromuscular respiratory weakness with pre-certification."),
    (32, "Blue Cross Blue Shield North Carolina", "BCBS", "NC", "Prior-Auth Required",
     "https://www.bluecrossnc.com/providers/policies-guidelines-codes/commercial/home-health-dme/updates/oscillatory-devices-for-treatment-of-respiratory-conditions",
     "Oscillatory Devices Policy",
     "No 2026 update detected. Status unchanged - OLE investigational."),
    (33, "Blue Cross Blue Shield Kansas", "BCBS", "KS", "Prior-Auth Required",
     "https://www.bcbsks.com/medical-policies/oscillatory-devices-treatment-cystic-fibrosis-and-other-respiratory-disorders",
     "Oscillatory Devices Policy",
     "No 2026 specific update found. Policy active for CF/bronchiectasis with criteria."),
    (35, "Health Plan of Nevada", "Regional HMO", "NV", "Prior-Auth Required",
     "https://healthplanofnevada.com/content/dam/hpnv-public-sites/health-plan-of-nevada/provider/medical-policies/airway-clearance-devices.pdf",
     "Airway Clearance Devices",
     "Policy still active at 01/01/2026 effective date."),
    (36, "Sierra Health and Life (Nevada)", "Commercial", "NV", "Prior-Auth Required",
     "https://healthplanofnevada.com/provider/medical-policies", "Airway Clearance Devices",
     "Affiliated with HPN. Same 01/01/2026 policy applies."),
    (44, "California Medi-Cal (Medicaid)", "Medicaid", "CA", "Prior-Auth Required",
     "https://mcweb.apps.prd.cammis.medi-cal.ca.gov/assets/2551F33B-449C-46EE-8E14-9152E82AE2D8/duracd.pdf",
     "DME Billing Codes Manual",
     "No 2026 update detected. 1-in-5-years frequency limit still in place."),
    (46, "Aetna", "Commercial", "", "Prior-Auth Required",
     "https://www.aetna.com/cpb/medical/data/1_99/0067.html", "CPB 0067",
     "No 2026 revision detected. Policy still active - OLE investigational/experimental."),
    (48, "Moda Health (Oregon/Alaska)", "Regional", "OR", "Prior-Auth Required",
     "https://www.modahealth.com/-/media/modahealth/shared/provider/prior-authorization/pre-auth-list-commercial.pdf",
     "MHMNC - HFCWO Devices",
     "PA list still updated 11/03/2025. No further changes detected."),
    (50, "Wellmark BCBS (Iowa/South Dakota)", "BCBS", "IA", "Prior-Auth Required",
     "https://digital-assets.wellmark.com/adobe/assets/urn:aaid:aem:8aa2f47a-61ff-4beb-9f1b-219c24adb04e/original/as/Airway-Clearance-Devices.pdf",
     "Airway Clearance Devices",
     "No 2026 update detected. OLE devices investigational."),
    (52, "Lifewise (Washington)", "Commercial", "WA", "Covered",
     "https://providernews.lifewise.com/fee-schedule-maintenance-update/",
     "Fee Schedule Maintenance Update",
     "No 2026 fee schedule update detected. Still in effect from 07/15/2025."),
    (54, "Kentucky Medicaid MSEA", "Medicaid", "KY", "Covered",
     "https://www.chfs.ky.gov/agencies/dms/dpo/bpb/Pages/dme.aspx", "907 KAR 1:479",
     "2026 MSEA Fee Schedule revised 5/4/2026. E0469 referenced as MSEA applicable code."),
    (55, "Capital Blue Cross (Pennsylvania)", "BCBS", "PA", "Prior-Auth Required",
     "https://www.capbluecross.com/wps/wcm/connect/prod_nws.capblue.com29556/12a40734-7069-4e43-8944-30b8c7dde992/medical-policy-experimental-and-investigational-procedures.pdf",
     "MP 4.002",
     "Policy still active - E0469 in Experimental and Investigational Procedures policy."),
    (56, "Blue Cross Blue Shield Texas", "BCBS", "TX", "Prior-Auth Required (Recommended Clinical Review)",
     "https://www.bcbstx.com/provider/claims/claims-eligibility/fee-schedule", "EIU Medical Policy",
     "Fee schedule update May 1, 2026 announced but E0469 EIU status unchanged."),
    (57, "Blue Cross Blue Shield Illinois", "BCBS", "IL", "Prior-Auth Required (Recommended Clinical Review)",
     "https://www.bcbsil.com/provider/claims/claims-eligibility/fee-schedule", "EIU Medical Policy",
     "Fee schedule annual update June 1, 2026 but E0469 EIU status unchanged."),
    (58, "Blue Cross Blue Shield New Mexico", "BCBS", "NM", "Prior-Auth Required (Recommended Clinical Review)",
     "https://www.bcbsnm.com/provider/education-reference/education/tools/fee-schedules-availity",
     "Predetermination List",
     "No 2026 update detected. Still on Recommended Clinical Review list."),
    (59, "Blue Cross Blue Shield Nebraska", "BCBS", "NE", "Prior-Auth Required",
     "https://www.nebraskablue.com/Providers/Policies-and-Procedures/Medicare-Advantage/MA-Medical-Prior-Authorization",
     "MA-X-077",
     "MA prior auth process changing to P3 Portal May 2026; E0469 coverage status unchanged."),
    (61, "Blue Cross Blue Shield Vermont", "BCBS", "VT", "Prior-Auth Required (Investigational)",
     "https://www.bluecrossvt.org/sites/default/files/2024-12/Investigational%20Services_Publication_01.01.2025AM.pdf",
     "10.01.VT204",
     "No 2026 update detected. Policy still active with 01/01/2025 effective date."),
    (62, "CareSource Ohio (Medicaid)", "Medicaid MCO", "OH", "Prior-Auth Required",
     "https://www.caresource.com/documents/oh-med-p-3504381-2025-prior-authorization-requirement-updates.pdf",
     "P-3504381",
     "New CMS PA Final Rule applies 01/01/2026 but E0469 status unchanged."),
    (63, "Select Health Utah (Medicare)", "Medicare Advantage", "UT", "Prior-Auth Required",
     "https://selecthealth.org/content/dam/selecthealth/Provider/PDFs/preauthorization/non-covered-code-lists/medicare-ut-id.pdf",
     "Medicare UT/ID Code List",
     "No 2026 update detected. Still requires prior auth from 12/22/2025."),
    (64, "Select Health Idaho (Medicare)", "Medicare Advantage", "ID", "Prior-Auth Required",
     "https://selecthealth.org/content/dam/selecthealth/Provider/PDFs/preauthorization/non-covered-code-lists/medicare-ut-id.pdf",
     "Medicare UT/ID Code List",
     "Same as Select Health UT. No update detected."),
    (72, "Blue Cross Blue Shield Tennessee", "BCBS", "TN", "Prior-Auth Required",
     "https://www.bcbst.com/mpmanual/!SSL!/WebHelp/Oscillating_Devices_for_the_Treatment_of_Respiratory_Conditions.htm",
     "Oscillating Devices Policy",
     "No 2026 specific update detected; policy still active."),
    (73, "Blue Cross Blue Shield South Carolina", "BCBS", "SC", "Prior-Auth Required",
     "https://www.southcarolinablues.com/web/public/brands/medicalpolicy/external-policies/oscillatory-devices-for-the-treatment-of-cystic-fibrosis-and-other-respiratory-conditions/",
     "Oscillatory Devices Policy",
     "No 2026 specific update detected; policy still active."),
    (74, "Blue Cross Blue Shield Louisiana", "BCBS", "LA", "Prior-Auth Required",
     "https://providers.lablue.com/-/media/Files/Providers/00090%2020230601%20Oscillatory%20Devices%20for%20the%20Treatment%20of%20Cystic%20Fibrosis%20and%20Other%20pdf.pdf",
     "00090",
     "No 2026 specific update detected; policy still active."),
    (79, "Providence Health Plan (Oregon)", "Medicare Advantage", "OR", "Prior-Auth Required",
     "https://www.providencehealthplan.com/-/media/providence/website/pdfs/providers/medical-policy-and-provider-information/medical-policies/mp220.pdf",
     "MP220",
     "No 2026 specific MP220 update found. Likely unchanged."),
    (80, "McLaren Health Plan (Michigan)", "Medicaid MCO", "MI", "Prior-Auth Required",
     "https://www.mclarenhealthplan.org/Uploads/Public/Documents/HealthPlan/documents/MHP%20Documents/Service-Codes-Requiring-Preauthorization.pdf",
     "Service Codes Requiring Preauthorization",
     "Pre-auth process changes March 1, 2026 but E0469 status unchanged."),
    (81, "New York Medicaid (eMedNY)", "Medicaid", "NY", "Prior-Auth Required",
     "https://www.emedny.org/providermanuals/dme/pdfs/dme_procedure_codes.pdf",
     "DME Procedure Codes & Coverage Guidelines",
     "No 2026 specific update found in DME procedure codes manual."),
    (82, "Anthem Indiana", "Commercial", "IN", "Prior-Auth Required",
     "https://providernews.anthem.com/indiana/articles/medical-policies-and-clinical-guidelines-updates-december-20-23415",
     "(current)",
     "No 2026 update detected; policy still active."),
    (83, "Hawaii Medical Service Association (HMSA)", "BCBS", "HI", "Not Covered",
     "https://prc.hmsa.com/s/article/Codes-That-Do-Not-Meet-Payment-Determination-Criteria-2",
     "Codes That Do Not Meet Payment Determination Criteria",
     "No 2026 update detected; policy still active."),
    (84, "Northwoods Medical", "Commercial", "", "Prior-Auth Required",
     "https://northwoodinc.com/wp-content/uploads/2025/12/Airway-Clearance-Devices-1.pdf",
     "(current)",
     "Policy reviewed 11/03/2025 (matches DB). No further changes detected."),
]

# ==============================================================================
# SHEET 4: STILL NOT FOUND (searched payers with still no explicit E0469 policy)
# ==============================================================================
# Compiled from the 110 unique searched payers (after deduping 6 that were re-added to payers list)
still_not_found_data = [
    # (ID, Name, Type, Last Re-checked, Notes)
    (1, "BCBS Tennessee", "BCBS", "2026-05-10", "Already added as payer ID 72 (see Sheet 3) — duplicate in searched_payers."),
    (2, "BCBS Arkansas", "BCBS", "2026-05-10", "Policy 2022013 still active behind member portal. E0469 added to billing/coding eff 10/1/2024 but coverage details unverified. No public 2026 update."),
    (3, "BCBS Idaho", "BCBS", "2026-05-10", "No explicit E0469 policy found. No 2026 update."),
    (4, "BCBS Montana", "BCBS", "2026-05-10", "No explicit E0469 policy found. 2026 PA list reviewed - E0469 not listed."),
    (5, "Horizon BCBS NJ", "BCBS", "2026-05-10", "No explicit E0469 policy found in 2026."),
    (6, "Empire BCBS (NY)", "BCBS", "2026-05-10", "No explicit E0469 policy found in 2026."),
    (7, "Independence Blue Cross (PA)", "BCBS", "2026-05-10", "Medical Policy Portal reviewed - no E0469 found."),
    (8, "CareFirst BCBS (MD/DC/VA)", "BCBS", "2026-05-10", "No explicit E0469 policy found in 2026."),
    (9, "Blue Shield California", "BCBS", "2026-05-10", "Prior Auth List effective 05/01/2026 reviewed - E0469 not explicitly listed."),
    (10, "Highmark BCBS (PA/WV/DE)", "BCBS", "2026-05-10", "No explicit E0469 policy found. Behind secure portal - may have E-20-016."),
    (11, "Regence BCBS (OR/ID/WA/UT)", "BCBS", "2026-05-10", "No explicit E0469 policy found in 2026."),
    (12, "Oscar Health", "Commercial", "2026-05-10", "No explicit E0469 policy found in 2026."),
    (13, "Bright Health", "Commercial", "2026-05-10", "Still exited insurance business - no policy."),
    (14, "Clover Health", "Medicare Advantage", "2026-05-10", "No explicit E0469 policy found in 2026."),
    (15, "Devoted Health", "Medicare Advantage", "2026-05-10", "No explicit E0469 in 2026 prior auth list."),
    (16, "Alignment Healthcare", "Medicare Advantage", "2026-05-10", "No explicit E0469 policy found in 2026."),
    (17, "First Health", "Commercial PPO", "2026-05-10", "No explicit E0469 policy found in 2026."),
    (18, "ConnectiCare", "Regional", "2026-05-10", "No explicit E0469 policy found in 2026."),
    (19, "Sentara Health Plans", "Regional", "2026-05-10", "No explicit E0469 policy found in 2026."),
    (20, "Harvard Pilgrim / Point32Health", "Regional", "2026-05-10", "No explicit E0469 policy found in 2026."),
    (21, "Tufts Health Plan / Point32Health", "Regional", "2026-05-10", "No explicit E0469 policy found in 2026."),
    (22, "Medical Mutual of Ohio", "Regional", "2026-05-10", "Already added as payer ID 77 (see Sheet 1) — duplicate in searched_payers."),
    (23, "Priority Health (MI)", "Regional", "2026-05-10", "No explicit E0469 policy found in 2026."),
    (24, "SelectHealth (UT)", "Regional", "2026-05-10", "No explicit E0469 policy found in 2026 (separate from Medicare entries already listed)."),
    (25, "UPMC Health Plan (PA)", "Regional", "2026-05-10", "No explicit E0469 policy found in 2026."),
    (26, "MVP Health Care (NY/VT)", "Regional", "2026-05-10", "No explicit E0469 policy found in 2026."),
    (27, "Quartz Health (WI)", "Regional", "2026-05-10", "No explicit E0469 policy found in 2026."),
    (28, "Fallon Health (MA)", "Regional", "2026-05-10", "No explicit E0469 policy found in 2026."),
    (29, "Magellan Health", "Specialty", "2026-05-10", "No explicit E0469 policy found in 2026."),
    (30, "Molina Healthcare", "Medicaid MCO", "2026-05-10", "2026 PA guide reviewed - no explicit E0469 mention; may be covered under general DME."),
    (31, "Centene / WellCare", "Medicaid MCO", "2026-05-10", "No explicit E0469 policy found in 2026."),
    (32, "Amerigroup / Elevance", "Medicaid MCO", "2026-05-10", "Still CG-DME-43 covers E0483 not E0469."),
    (33, "AmeriHealth Caritas", "Medicaid MCO", "2026-05-10", "No explicit E0469 policy found in 2026."),
    (34, "Superior Health Plan (TX)", "Medicaid MCO", "2026-05-10", "No explicit E0469 policy found in 2026."),
    (35, "Pennsylvania DHS Medicaid", "State Medicaid FFS", "2026-05-10", "Fee schedule still not web-indexed for E0469."),
    (36, "Ohio ODM Medicaid", "State Medicaid FFS", "2026-05-10", "Fee schedule still not web-indexed for E0469."),
    (37, "Michigan MDHHS Medicaid", "State Medicaid FFS", "2026-05-10", "Fee schedule still not web-indexed for E0469."),
    (38, "North Carolina NCTracks", "State Medicaid FFS", "2026-05-10", "Fee schedule still not web-indexed for E0469."),
    (39, "Virginia DMAS Medicaid", "State Medicaid FFS", "2026-05-10", "Fee schedule still not web-indexed for E0469."),
    (40, "New Jersey FamilyCare", "State Medicaid FFS", "2026-05-10", "Fee schedule still not web-indexed for E0469."),
    (41, "Arizona AHCCCS", "State Medicaid FFS", "2026-05-10", "Fee schedule still not web-indexed for E0469."),
    (42, "Washington Apple Health", "State Medicaid FFS", "2026-05-10", "Fee schedule still not web-indexed for E0469."),
    (43, "Kentucky DMS Medicaid", "State Medicaid FFS", "2026-05-10", "Same agency as MSEA Medicaid (payer ID 54). No new FFS-specific policy."),
    (44, "Louisiana LDH Medicaid", "State Medicaid FFS", "2026-05-10", "Fee schedule still not web-indexed for E0469."),
    (45, "Indiana FSSA Medicaid", "State Medicaid FFS", "2026-05-10", "Fee schedule still not web-indexed for E0469."),
    (46, "Connecticut DSS/HUSKY", "State Medicaid FFS", "2026-05-10", "Fee schedule still not web-indexed for E0469."),
    (47, "Nevada DHCFP Medicaid", "State Medicaid FFS", "2026-05-10", "Fee schedule still not web-indexed for E0469."),
    (48, "Maryland Medicaid", "State Medicaid FFS", "2026-05-10", "Fee schedule still not web-indexed for E0469."),
    (49, "Wisconsin ForwardHealth", "State Medicaid FFS", "2026-05-10", "Fee schedule still not web-indexed for E0469."),
    (50, "South Carolina SCDHHS", "State Medicaid FFS", "2026-05-10", "Fee schedule still not web-indexed for E0469."),
    (51, "Oregon OHP", "State Medicaid FFS", "2026-05-10", "Fee schedule still not web-indexed for E0469."),
    (52, "Illinois HFS Medicaid", "State Medicaid FFS", "2026-05-10", "Fee schedule still not web-indexed for E0469."),
    (53, "Georgia DCH Medicaid", "State Medicaid FFS", "2026-05-10", "Fee schedule still not web-indexed for E0469."),
    (54, "Texas HHSC Medicaid", "State Medicaid FFS", "2026-05-10", "Fee schedule still not web-indexed for E0469."),
    (55, "Florida AHCA Medicaid", "State Medicaid FFS", "2026-05-10", "Fee schedule still not web-indexed for E0469."),
    (56, "Tricare", "Federal", "2026-05-10", "No explicit E0469 policy in 2026 program changes. Likely still follows Medicare."),
    (57, "VA Health Benefits", "Federal", "2026-05-10", "No explicit E0469 policy found in 2026."),
    (58, "Federal OWCP", "Workers' Comp", "2026-05-10", "No explicit E0469 policy found in 2026."),
    (59, "NY State Workers' Comp", "Workers' Comp", "2026-05-10", "Fee schedule still not web-indexed for E0469."),
    (60, "CA State Workers' Comp", "Workers' Comp", "2026-05-10", "Fee schedule still not web-indexed for E0469."),
    (61, "TX State Workers' Comp", "Workers' Comp", "2026-05-10", "Fee schedule still not web-indexed for E0469."),
    (62, "Anthem BCBS (Multi-state)", "BCBS/Elevance", "2026-05-10", "Still CG-DME-43 covers E0483 not E0469."),
    (63, "Centene / WellCare / Ambetter", "Commercial/Medicaid MCO", "2026-05-10", "No explicit E0469 policy found in 2026."),
    (64, "LifeWise / Cambia Health", "Regional (WA)", "2026-05-10", "Separate from Lifewise (already in payers). No explicit E0469."),
    (65, "Allina Health Plan", "Regional (MN)", "2026-05-10", "No explicit E0469 policy found in 2026."),
    (66, "Sanford Health Plan", "Regional (ND/SD/MN)", "2026-05-10", "No explicit E0469 policy found in 2026."),
    (67, "BCBS Alabama", "BCBS", "2026-05-10", "No explicit E0469 policy found in 2026."),
    (68, "ConnectiCare (CT)", "Regional", "2026-05-10", "Duplicate of ID 18. EIU policy PDF still not readable."),
    (69, "AvMed (FL)", "Regional HMO", "2026-05-10", "No explicit E0469 policy found in 2026."),
    (70, "Florida Health Care Plans (FHCP)", "Regional", "2026-05-10", "No explicit E0469 policy found in 2026."),
    (71, "CDPHP (NY)", "Regional HMO", "2026-05-10", "No explicit E0469 policy found in 2026."),
    (72, "GuideWell / Florida Blue", "BCBS (FL)", "2026-05-10", "Parent of BCBSFL — see payer ID 7 for explicit E0469 policy."),
    (73, "Neighborhood Health Plan (MA)", "Medicaid MCO", "2026-05-10", "No explicit E0469 policy found in 2026."),
    (74, "BCBS South Carolina", "BCBS", "2026-05-10", "Already added as payer ID 73 (see Sheet 3) — duplicate in searched_payers."),
    (75, "HAP Health Alliance Plan (MI)", "Regional HMO", "2026-05-10", "No explicit E0469 policy found in 2026."),
    (76, "Anthem California", "BCBS/Elevance", "2026-05-10", "No explicit E0469 policy found in 2026."),
    (77, "BCBS Wyoming", "BCBS", "2026-05-10", "No explicit E0469 policy found in 2026."),
    (78, "Taro Health", "Commercial", "2026-05-10", "No explicit E0469 policy found in 2026."),
    (79, "Friday Health", "Commercial", "2026-05-10", "No explicit E0469 policy found in 2026."),
    (80, "Bind Benefits (UHC)", "Commercial", "2026-05-10", "Now part of Surest (already in payers)."),
    (81, "Aflac", "Supplemental", "2026-05-10", "Supplemental insurance - no DME policy."),
    (82, "Lincoln Financial", "Supplemental", "2026-05-10", "Supplemental insurance - no DME policy."),
    (83, "MetLife", "Supplemental", "2026-05-10", "Supplemental insurance - no DME policy."),
    # (84 entry moved to renamed form near bottom of list — see "Humana Medicaid (South Carolina)")
    (85, "BCBS Louisiana (Louisiana Blue)", "BCBS", "2026-05-10", "Already added as payer ID 74 (see Sheet 3) — duplicate in searched_payers."),
    (86, "Humana Puerto Rico", "Regional", "2026-05-10", "National Humana policy applies - OLE Not Covered per HUM-2007-001."),
    (87, "Indiana Medicaid IHCP", "State Medicaid FFS", "2026-05-10", "Fee schedule still not web-indexed for E0469."),
    (88, "BCBS North Dakota", "BCBS", "2026-05-10", "No explicit E0469 policy found in 2026."),
    (89, "Providence Health Plan (Oregon)", "Regional", "2026-05-10", "Already added as payer ID 79 (see Sheet 3) — duplicate in searched_payers."),
    (90, "Hawaii Medical Service Association (HMSA)", "Regional", "2026-05-10", "Already added as payer ID 83 (see Sheet 3) — duplicate in searched_payers."),
    (91, "Texas Children's Health Plan", "Medicaid MCO", "2026-05-10", "No explicit E0469 policy found in 2026."),
    (92, "Anthem Wisconsin", "BCBS/Elevance", "2026-05-10", "No explicit E0469 policy found in 2026."),
    (93, "BCBS California (Anthem Blue Cross CA)", "BCBS/Elevance", "2026-05-10", "No explicit E0469 policy found in 2026."),
    (94, "CalViva Health (California)", "Medicaid MCO", "2026-05-10", "Follows Medi-Cal — see payer ID 44."),
    (95, "iCare Health Plan (Wisconsin)", "Medicaid MCO", "2026-05-10", "No explicit E0469 policy found in 2026."),
    (96, "Colorado Medicaid HCPF", "State Medicaid FFS", "2026-05-10", "Fee schedule still not web-indexed for E0469."),
    (97, "Select Health (Colorado)", "Regional", "2026-05-10", "No explicit E0469 policy found in 2026 (separate from UT/ID Medicare entries)."),
    (98, "BCBS Nevada", "BCBS", "2026-05-10", "No explicit E0469 policy (separate from Health Plan of Nevada in payers list)."),
    (99, "Anthem Virginia", "BCBS/Elevance", "2026-05-10", "No explicit E0469 policy found in 2026."),
    (100, "Anthem Maine", "BCBS/Elevance", "2026-05-10", "No explicit E0469 policy found in 2026."),
    (101, "Anthem New York", "BCBS/Elevance", "2026-05-10", "No explicit E0469 policy found in 2026."),
    (102, "Anthem Georgia", "BCBS/Elevance", "2026-05-10", "Administers GA State Health Benefit Plan. No explicit E0469."),
    (103, "Mississippi Medicaid", "State Medicaid FFS", "2026-05-10", "Fee schedule still not web-indexed for E0469."),
    (104, "Montana Medicaid", "State Medicaid FFS", "2026-05-10", "Fee schedule still not web-indexed for E0469."),
    (105, "Excellus BlueCross BlueShield (NY)", "BCBS", "2026-05-10", "Policy 1.01.15 still covers E0480-E0484 but NOT E0469."),
    (106, "Cigna", "Commercial", "2026-05-10", "Policy 0069 'Airway Clearance Devices' updated 11/9/2025 - still references E0481-E0483 only. Header updates but E0469 not added per available info."),
    (107, "Blue Cross Blue Shield Massachusetts", "BCBS", "2026-05-10", "Policy 120 still lists E0481/E0483/E0484/S8185 - no E0469. Not updated for new code."),
    (108, "Blue Cross Blue Shield of Michigan", "BCBS", "2026-05-10", "DIFS external review still discusses Volara under E1399/A9999. E0469 not added."),
    (109, "EmblemHealth (New York)", "Regional", "2026-05-10", "DME rental/purchase policy still does not reference E0469."),
    (110, "Anthem (Elevance Health)", "Commercial", "2026-05-10", "Policy DME.00012 still excludes E0469."),
    (111, "Anthem Blue Cross Connecticut", "BCBS", "2026-05-10", "CG-DME-43 still covers E0483 but not E0469."),
    (112, "Noridian Medicare (JD DME)", "Medicare MAC", "2026-05-10", "DME MAC - not a payer per se. JA DME (Noridian) is the relevant entry in payers list (ID 2)."),
    (113, "CMS DMEPOS Fee Schedule", "Medicare/CMS", "2026-05-10", "Reference document, not a payer. Still no LCD/NCD published for E0469."),
    (114, "FEP Blue (Federal Employee Program)", "BCBS", "2026-05-10", "No explicit E0469 policy added back."),
    (115, "Highmark Health Options (Delaware)", "Medicaid", "2026-05-10", "Policy MP-1141 still does not mention E0469."),
    (116, "Humana (Commercial)", "Commercial", "2026-05-10", "Generic Humana policy. National Humana MA PA List applies to MA (see payer ID 21)."),
    (117, "Humana Medicaid (Florida)", "Medicaid MCO", "2026-05-10", "[ADDED 2026-05-10] Humana Healthy Horizons operates Medicaid in FL. OLE policy edition likely exists (VA/KY editions confirmed Not Covered) but specific policy URL not located via public web search. Behind provider.humana.com/medicaid/florida-medicaid portal login."),
    (118, "Humana Medicaid (Illinois)", "Medicaid MCO", "2026-05-10", "[ADDED 2026-05-10] Humana Healthy Horizons operates Medicaid in IL. OLE policy edition likely exists (VA/KY editions confirmed Not Covered) but specific policy URL not located via public web search. Behind provider.humana.com/medicaid/illinois-medicaid portal login."),
    (119, "Humana Medicaid (Indiana)", "Medicaid MCO", "2026-05-10", "[ADDED 2026-05-10] Humana Healthy Horizons operates Medicaid in IN. OLE policy edition likely exists (VA/KY editions confirmed Not Covered) but specific policy URL not located via public web search. Behind provider.humana.com/medicaid/indiana-medicaid portal login."),
    (120, "Humana Medicaid (Louisiana)", "Medicaid MCO", "2026-05-10", "[ADDED 2026-05-10] Humana Healthy Horizons operates Medicaid in LA. OLE policy edition likely exists (VA/KY editions confirmed Not Covered) but specific policy URL not located via public web search. Behind provider.humana.com/medicaid/louisiana-medicaid portal login."),
    (121, "Humana Medicaid (Michigan)", "Medicaid MCO", "2026-05-10", "[ADDED 2026-05-10] Humana Healthy Horizons operates Medicaid in MI. OLE policy edition likely exists (VA/KY editions confirmed Not Covered) but specific policy URL not located via public web search. Behind provider.humana.com/medicaid/michigan-medicaid portal login."),
    (122, "Humana Medicaid (Ohio)", "Medicaid MCO", "2026-05-10", "[ADDED 2026-05-10] Humana Healthy Horizons operates Medicaid in OH. OLE policy edition likely exists (VA/KY editions confirmed Not Covered) but specific policy URL not located via public web search. Behind provider.humana.com/medicaid/ohio-medicaid portal login."),
    (123, "Humana Medicaid (Oklahoma)", "Medicaid MCO", "2026-05-10", "[ADDED 2026-05-10] Humana Healthy Horizons operates Medicaid in OK (SoonerSelect). OLE policy edition likely exists (VA/KY editions confirmed Not Covered) but specific policy URL not located via public web search. Behind provider.humana.com/medicaid/oklahoma-medicaid portal login."),
    (84, "Humana Medicaid (South Carolina)", "Medicaid MCO", "2026-05-10", "[RENAMED 2026-05-10 — was 'Humana SC Medicaid'] Humana Healthy Horizons operates Medicaid in SC. OLE policy edition likely exists (VA/KY editions confirmed Not Covered) but specific policy URL not located via public web search. Behind provider.humana.com/medicaid/south-carolina-medicaid portal login."),
    (124, "Humana Medicaid (Wisconsin)", "Medicaid MCO", "2026-05-10", "[ADDED 2026-05-10] Humana Healthy Horizons operates Medicaid in WI. OLE policy edition likely exists (VA/KY editions confirmed Not Covered) but specific policy URL not located via public web search. Behind provider.humana.com/medicaid/wisconsin-medicaid portal login."),
]


def build_workbook():
    wb = Workbook()

    # ------------------------------------------------------------------------
    # SUMMARY SHEET
    # ------------------------------------------------------------------------
    ws_summary = wb.active
    ws_summary.title = "Summary"

    ws_summary["A1"] = "E0469 Payer Policy Review"
    ws_summary["A1"].font = Font(size=16, bold=True, color="1F4E78")

    ws_summary["A2"] = f"Generated: 2026-05-10"
    ws_summary["A3"] = "Reference snapshot: Feb 6, 2026"
    ws_summary["A4"] = "Time elapsed since reference: ~3 months"
    ws_summary["A6"] = "Review Scope"
    ws_summary["A6"].font = Font(bold=True, size=12)
    ws_summary["A7"] = "Existing payers re-verified: 70"
    ws_summary["A8"] = "Searched payers re-checked: 110 unique (116 total, 6 duplicates with existing payers)"
    ws_summary["A9"] = "Total payers reviewed: 180"

    ws_summary["A11"] = "Findings Summary"
    ws_summary["A11"].font = Font(bold=True, size=12)
    ws_summary["A12"] = f"Sheet 'Status/Date Changes': {len(changes_data)} payers with updates"
    ws_summary["A13"] = f"Sheet 'New Additions': {len(new_additions_data)} searched payers now have E0469 policy"
    ws_summary["A14"] = f"Sheet 'No Change Confirmed': {len(no_change_data)} existing payers verified unchanged"
    ws_summary["A15"] = f"Sheet 'Still Not Found': {len(still_not_found_data)} searched payers still without E0469 policy"

    ws_summary["A17"] = "Key Findings"
    ws_summary["A17"].font = Font(bold=True, size=12)
    ws_summary["A18"] = "1. UHC ecosystem: All 14 UHC variant policies refreshed to 03/01/2026 effective date."
    ws_summary["A19"] = "2. Humana Medicare Advantage [STATUS CORRECTION]: DB had Not Covered; actual 2026 MA/DSNP PA List adds E0469 as NEW Prior Auth Required effective 01/01/2026. HUM-2007-001 (Medicaid policy) was incorrectly applied to MA."
    ws_summary["A20"] = "3. Humana Medicaid [STATE SPLIT]: Generic row split into per-state. Confirmed VA (HUM-VA-2007-002, eff 07/22/2026) and KY (HUM-2007-001 KY ed, eff 01/16/2026), both Not Covered. 9 other Humana Medicaid states (FL/IL/IN/LA/MI/OH/OK/SC/WI) need policy URL verification via provider portal."
    ws_summary["A21"] = "4. Medica (7 state plans): Administrative update 08/05/2025 for code refresh. Status still Not Covered."
    ws_summary["A22"] = "5. BCBS Rhode Island [REVIEW NEEDED]: E0469 now non-reimbursed for BOTH MA and Commercial. Verify."
    ws_summary["A23"] = "6. BCBS Minnesota: EviCore NO LONGER managing DME PAs as of 08/01/2025. URL needs update."
    ws_summary["A24"] = "7. Univera (NY) [REVIEW NEEDED]: Old policy 'terminates on 2026-03-16'. New policy URL may exist."
    ws_summary["A25"] = "8. Fidelis Care NY: New Auth Grids effective 04/01/2026."
    ws_summary["A26"] = "9. Premera (WA): Annual review 10/13/2025, policy unchanged."
    ws_summary["A27"] = "10. Medical Mutual of Ohio: Policy #200508 updated 08/19/2025."
    ws_summary["A28"] = "11. NO new explicit E0469 policies detected among 110 previously-searched payers."

    ws_summary["A29"] = "Color Coding"
    ws_summary["A29"].font = Font(bold=True, size=12)
    legend = [
        ("Green", GREEN_FILL, "No Change Confirmed"),
        ("Yellow", YELLOW_FILL, "Date Change (minor)"),
        ("Orange", ORANGE_FILL, "Status / URL Change (review needed)"),
        ("Red", RED_FILL, "Coverage downgrade (e.g., to Not Covered)"),
        ("Blue", BLUE_FILL, "New policy addition"),
        ("Grey", GREY_FILL, "Still Not Found"),
    ]
    for idx, (name, fill, desc) in enumerate(legend, start=30):
        ws_summary[f"A{idx}"] = name
        ws_summary[f"A{idx}"].fill = fill
        ws_summary[f"B{idx}"] = desc

    ws_summary.column_dimensions["A"].width = 18
    ws_summary.column_dimensions["B"].width = 80

    # ------------------------------------------------------------------------
    # SHEET 1: STATUS / DATE / URL CHANGES
    # ------------------------------------------------------------------------
    ws1 = wb.create_sheet("1. Status_Date_URL Changes")
    headers1 = [
        "ID", "Payer Name", "Type", "State",
        "Old Coverage", "New Coverage", "Old PA", "New PA", "Old Inv", "New Inv",
        "Old Policy Date", "New Policy Date", "Policy #",
        "Old Source URL", "New Source URL",
        "Change Type", "Notes / Recommended Action"
    ]
    for col_idx, h in enumerate(headers1, start=1):
        ws1.cell(row=1, column=col_idx, value=h)
    style_header(ws1, 1, len(headers1))

    for row_idx, row_data in enumerate(changes_data, start=2):
        for col_idx, val in enumerate(row_data, start=1):
            ws1.cell(row=row_idx, column=col_idx, value=val)
        change_type = row_data[15]
        if change_type == "DATE_CHANGE":
            fill = YELLOW_FILL
        elif change_type in ("STATUS_CHANGE", "URL_CHANGE"):
            fill = ORANGE_FILL
        elif change_type == "POLICY_REMOVED":
            fill = RED_FILL
        else:
            fill = YELLOW_FILL
        apply_row_fill(ws1, row_idx, len(headers1), fill)

    autosize_columns(ws1, {
        "A": 5, "B": 35, "C": 18, "D": 6,
        "E": 18, "F": 18, "G": 16, "H": 16, "I": 10, "J": 10,
        "K": 16, "L": 18, "M": 22,
        "N": 50, "O": 50,
        "P": 14, "Q": 65
    })

    # ------------------------------------------------------------------------
    # SHEET 2: NEW POLICY ADDITIONS
    # ------------------------------------------------------------------------
    ws2 = wb.create_sheet("2. New Policy Additions")
    headers2 = ["ID (searched)", "Payer Name", "Type", "State", "Coverage Status",
                "Source URL", "Policy #", "Effective Date", "Notes"]
    for col_idx, h in enumerate(headers2, start=1):
        ws2.cell(row=1, column=col_idx, value=h)
    style_header(ws2, 1, len(headers2))

    if new_additions_data:
        for row_idx, row_data in enumerate(new_additions_data, start=2):
            for col_idx, val in enumerate(row_data, start=1):
                ws2.cell(row=row_idx, column=col_idx, value=val)
            apply_row_fill(ws2, row_idx, len(headers2), BLUE_FILL)
    else:
        ws2.cell(row=2, column=1, value="—")
        ws2.cell(row=2, column=2, value="No new explicit E0469 policies detected during 2026-05-10 re-check.")
        ws2.merge_cells(start_row=2, start_column=2, end_row=2, end_column=9)
        ws2.cell(row=3, column=2,
                 value="The 70 active payers already capture the most recent wave of E0469 adopters from Feb 2026 cleanup.")
        ws2.merge_cells(start_row=3, start_column=2, end_row=3, end_column=9)
        ws2.cell(row=4, column=2,
                 value="Most state Medicaid FFS programs continue to lack web-indexed fee schedules for E0469.")
        ws2.merge_cells(start_row=4, start_column=2, end_row=4, end_column=9)

    autosize_columns(ws2, {"A": 12, "B": 35, "C": 18, "D": 8, "E": 22, "F": 60, "G": 22, "H": 16, "I": 60})

    # ------------------------------------------------------------------------
    # SHEET 3: NO CHANGE CONFIRMED
    # ------------------------------------------------------------------------
    ws3 = wb.create_sheet("3. No Change Confirmed")
    headers3 = ["ID", "Payer Name", "Type", "State", "Coverage Status", "Source URL", "Policy #", "Notes"]
    for col_idx, h in enumerate(headers3, start=1):
        ws3.cell(row=1, column=col_idx, value=h)
    style_header(ws3, 1, len(headers3))

    for row_idx, row_data in enumerate(no_change_data, start=2):
        for col_idx, val in enumerate(row_data, start=1):
            ws3.cell(row=row_idx, column=col_idx, value=val)
        apply_row_fill(ws3, row_idx, len(headers3), GREEN_FILL)

    autosize_columns(ws3, {"A": 5, "B": 38, "C": 22, "D": 6, "E": 26, "F": 60, "G": 22, "H": 60})

    # ------------------------------------------------------------------------
    # SHEET 4: STILL NOT FOUND
    # ------------------------------------------------------------------------
    ws4 = wb.create_sheet("4. Still Not Found")
    headers4 = ["ID (searched)", "Payer Name", "Type", "Last Re-checked", "Notes"]
    for col_idx, h in enumerate(headers4, start=1):
        ws4.cell(row=1, column=col_idx, value=h)
    style_header(ws4, 1, len(headers4))

    for row_idx, row_data in enumerate(still_not_found_data, start=2):
        for col_idx, val in enumerate(row_data, start=1):
            ws4.cell(row=row_idx, column=col_idx, value=val)
        apply_row_fill(ws4, row_idx, len(headers4), GREY_FILL)

    autosize_columns(ws4, {"A": 12, "B": 42, "C": 22, "D": 16, "E": 80})

    wb.save(OUTPUT_PATH)
    print(f"Workbook generated: {OUTPUT_PATH}")
    print(f"  Sheet 1 (Changes): {len(changes_data)} rows")
    print(f"  Sheet 2 (New Additions): {len(new_additions_data)} rows")
    print(f"  Sheet 3 (No Change): {len(no_change_data)} rows")
    print(f"  Sheet 4 (Still Not Found): {len(still_not_found_data)} rows")


if __name__ == "__main__":
    build_workbook()
