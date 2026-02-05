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

## Project Structure

```
E0469_Payer_Analysis/
├── CLAUDE.md                           # This file
├── SESSION_HANDOVER.md                 # Detailed session history and findings
├── E0469_Payer_Coverage_Analysis.py    # Original analysis script
├── E0469_Payer_Coverage_Analysis.xlsx  # Original spreadsheet output
├── E0469_Explicit_Payer_Policies.py    # Current analysis script (63 payers)
├── E0469_Explicit_Payer_Policies.xlsx  # Current spreadsheet output
└── mcp_pdf_server/                     # PDF extraction tool
    ├── pdf_extractor.py                # Extracts text from PDF URLs
    └── requirements.txt                # PyMuPDF dependency
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
# Regenerate spreadsheet
python3 E0469_Explicit_Payer_Policies.py

# Extract text from a PDF policy
python3 mcp_pdf_server/pdf_extractor.py search "<PDF_URL>" "E0469"

# View current payer count
grep -c '"name":' E0469_Explicit_Payer_Policies.py
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

- **Total Payers with Explicit E0469 Policies**: 63
- **NOT COVERED** (explicit): 4
- **Investigational/Experimental**: ~10
- **Covered with Criteria**: 16
- **Partial Coverage**: 20
- **Case-by-Case/Prior Auth**: 13

## Key Findings

1. **No Medicare LCD/NCD**: CMS has no specific coverage determination
2. **Most Consider OLE Investigational**: Volara, BiWaze Clear devices largely experimental
3. **New Code Challenge**: E0469 effective 10/1/2024 - many payers haven't published policies
4. **HFCWO vs OLE**: Many payers cover HFCWO (E0483) but NOT OLE devices (E0469)

## Reference

See `SESSION_HANDOVER.md` for complete session history, all payers searched, and detailed findings.
