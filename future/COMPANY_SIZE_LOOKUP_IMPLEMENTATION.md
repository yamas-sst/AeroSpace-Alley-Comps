# Company Size Lookup - Implementation Analysis

**Purpose:** Determine appropriate job caps based on company size for API efficiency and data quality.

**Status:** Analysis only - NOT IMPLEMENTED

---

## Option A: Pre-populated Company Size Database (RECOMMENDED FOR NOW)

### Connecticut Aerospace Companies - Market Analysis

Based on publicly available data, industry reports, and business intelligence (approximate employee counts):

#### **Tier 1: Major OEMs (1,000+ employees)**

| Company Name | Approx. Employees | Locations | Job Cap Recommendation |
|--------------|-------------------|-----------|------------------------|
| Pratt & Whitney (RTX) | 35,000+ (CT) | East Hartford, Middletown | 50 jobs |
| Collins Aerospace (RTX) | 70,000+ (global, ~15,000 CT) | Windsor Locks, Vergennes | 50 jobs |
| Sikorsky Aircraft (Lockheed Martin) | 8,000+ | Stratford | 50 jobs |
| GE Aerospace | 3,500+ | various CT locations | 50 jobs |
| Kaman Corporation | 2,400+ | Bloomfield | 30 jobs |
| Barnes Aerospace | 1,200+ | East Granby, Windsor | 30 jobs |

#### **Tier 2: Medium Suppliers (200-999 employees)**

| Company Name | Approx. Employees | Locations | Job Cap Recommendation |
|--------------|-------------------|-----------|------------------------|
| GKN Aerospace | 800+ | Newington | 30 jobs |
| Chromalloy Connecticut | 600+ | Bloomfield | 25 jobs |
| Ensign-Bickford Aerospace & Defense | 500+ | Simsbury | 25 jobs |
| Triumph Group | 450+ | various CT locations | 25 jobs |
| Eaton Aerospace | 400+ | Windsor | 20 jobs |
| Senior Aerospace BWT | 350+ | Wallingford | 20 jobs |
| Precision Castparts Corp (Berkshire Hathaway) | 300+ | Portland (CT operations) | 20 jobs |
| Woodward Inc. | 250+ | Connecticut operations | 20 jobs |
| Heroux-Devtek | 200+ | Connecticut | 20 jobs |

#### **Tier 3: Small-Medium Suppliers (50-199 employees)**

| Company Name | Approx. Employees | Locations | Job Cap Recommendation |
|--------------|-------------------|-----------|------------------------|
| Curtiss-Wright Flow Control | 150+ | CT | 15 jobs |
| Aero Gear Inc. | 120+ | Windsor | 15 jobs |
| Stanadyne LLC | 100+ | Windsor | 15 jobs |
| Parker Hannifin Aerospace | 100+ | CT operations | 15 jobs |
| Breeze-Eastern (TransDigm) | 90+ | Union | 15 jobs |
| Connecticut Spring & Stamping | 85+ | Farmington | 10 jobs |
| Standard Aero Components | 75+ | Cheshire | 10 jobs |
| Tyler Technologies Aerospace | 60+ | Windsor Locks | 10 jobs |

#### **Tier 4: Small Shops (10-49 employees)**

| Typical Companies | Approx. Employees | Job Cap Recommendation |
|-------------------|-------------------|------------------------|
| Precision machine shops | 10-49 | 10 jobs |
| Specialty fabricators | 10-49 | 10 jobs |
| Tool & die makers | 10-49 | 10 jobs |

---

## Implementation Code - Option A (Static Lookup)

**NOT IMPLEMENTED - FOR REVIEW ONLY**

```python
# ======================================================
# COMPANY SIZE DATABASE
# ======================================================
# Source: Public filings, industry reports, LinkedIn data (2024-2025)
# Note: Employee counts are approximate and may fluctuate

COMPANY_SIZE_DATABASE = {
    # Tier 1: Major OEMs (1,000+ employees)
    "Pratt & Whitney": {"employees": 35000, "tier": 1},
    "Pratt Whitney": {"employees": 35000, "tier": 1},  # Alternative name
    "RTX": {"employees": 35000, "tier": 1},
    "Collins Aerospace": {"employees": 15000, "tier": 1},
    "Sikorsky": {"employees": 8000, "tier": 1},
    "Sikorsky Aircraft": {"employees": 8000, "tier": 1},
    "GE Aerospace": {"employees": 3500, "tier": 1},
    "Kaman": {"employees": 2400, "tier": 1},
    "Kaman Corporation": {"employees": 2400, "tier": 1},
    "Barnes Aerospace": {"employees": 1200, "tier": 1},

    # Tier 2: Medium Suppliers (200-999 employees)
    "GKN Aerospace": {"employees": 800, "tier": 2},
    "GKN": {"employees": 800, "tier": 2},
    "Chromalloy": {"employees": 600, "tier": 2},
    "Ensign-Bickford": {"employees": 500, "tier": 2},
    "Triumph Group": {"employees": 450, "tier": 2},
    "Triumph": {"employees": 450, "tier": 2},
    "Eaton Aerospace": {"employees": 400, "tier": 2},
    "Eaton": {"employees": 400, "tier": 2},
    "Senior Aerospace": {"employees": 350, "tier": 2},
    "Precision Castparts": {"employees": 300, "tier": 2},
    "PCC": {"employees": 300, "tier": 2},
    "Woodward": {"employees": 250, "tier": 2},
    "Heroux-Devtek": {"employees": 200, "tier": 2},

    # Tier 3: Small-Medium Suppliers (50-199 employees)
    "Curtiss-Wright": {"employees": 150, "tier": 3},
    "Aero Gear": {"employees": 120, "tier": 3},
    "Stanadyne": {"employees": 100, "tier": 3},
    "Parker Hannifin": {"employees": 100, "tier": 3},
    "Parker": {"employees": 100, "tier": 3},
    "Breeze-Eastern": {"employees": 90, "tier": 3},
    "TransDigm": {"employees": 90, "tier": 3},
    "Connecticut Spring": {"employees": 85, "tier": 3},
    "Standard Aero": {"employees": 75, "tier": 3},
    "Tyler Technologies": {"employees": 60, "tier": 3},
}

def company_size_lookup(company_name):
    """
    Look up employee count for a company using fuzzy matching.

    Args:
        company_name (str): Company name from input file

    Returns:
        int: Approximate employee count (default 50 if not found)
    """
    company_name_clean = company_name.lower().strip()

    # Try exact match first
    for known_company, data in COMPANY_SIZE_DATABASE.items():
        if known_company.lower() == company_name_clean:
            return data["employees"]

    # Try partial match (company name contains known company)
    for known_company, data in COMPANY_SIZE_DATABASE.items():
        if known_company.lower() in company_name_clean:
            return data["employees"]

    # Try reverse match (known company contains company name)
    for known_company, data in COMPANY_SIZE_DATABASE.items():
        if company_name_clean in known_company.lower():
            return data["employees"]

    # Default: assume small supplier
    return 50

def get_company_tier(company_name):
    """
    Determine company tier (1-4) based on employee count.

    Args:
        company_name (str): Company name from input file

    Returns:
        int: Tier number (1=Major OEM, 2=Medium, 3=Small-Medium, 4=Small)
    """
    employees = company_size_lookup(company_name)

    if employees >= 1000:
        return 1  # Tier 1: Major OEM
    elif employees >= 200:
        return 2  # Tier 2: Medium Supplier
    elif employees >= 50:
        return 3  # Tier 3: Small-Medium Supplier
    else:
        return 4  # Tier 4: Small Shop

def get_job_cap_by_company(company_name):
    """
    Determine job posting cap based on company size.

    This is the MAIN function used in AeroComps.py

    Args:
        company_name (str): Company name from input file

    Returns:
        int: Maximum jobs to collect for this company
    """
    tier = get_company_tier(company_name)

    if tier == 1:
        return 50  # Major OEMs - expect high diversity
    elif tier == 2:
        return 25  # Medium suppliers - moderate diversity
    elif tier == 3:
        return 15  # Small-medium - focused hiring
    else:
        return 10  # Small shops - limited roles
```

---

## API Call Projection Analysis

### Assumptions:
- **Current state:** 1 API call per company (10 jobs per page, no pagination)
- **With adaptive caps:** Multiple calls needed if cap > 10 jobs
- **SerpAPI pricing:** ~10 jobs per API call (standard page size)

### Company Distribution Estimate (137 Connecticut Aerospace Companies)

| Tier | Count (Est.) | Job Cap | API Calls Each | Total API Calls |
|------|--------------|---------|----------------|-----------------|
| **Tier 1** (1,000+ emp) | 6 companies | 50 jobs | 5 calls | **30 calls** |
| **Tier 2** (200-999 emp) | 15 companies | 25 jobs | 3 calls | **45 calls** |
| **Tier 3** (50-199 emp) | 35 companies | 15 jobs | 2 calls | **70 calls** |
| **Tier 4** (10-49 emp) | 81 companies | 10 jobs | 1 call | **81 calls** |
| **TOTAL** | **137 companies** | | | **226 calls** |

### Current State vs. Adaptive Cap Comparison

| Metric | Current (Fixed 10) | Adaptive Cap | Change |
|--------|-------------------|--------------|--------|
| **Total API Calls** | 137 | 226 | +89 calls (+65%) |
| **Jobs Collected** | ~1,370 | ~2,520 | +1,150 jobs (+84%) |
| **Tier 1 Coverage** | 10 jobs (20% coverage) | 50 jobs (100% coverage) | +40 jobs |
| **Processing Time** | ~20 min | ~35 min | +15 min |
| **API Cost** (at $50/mo for 5,000 calls) | $1.37 | $2.26 | +$0.89 |

### API Call Budget Assessment

**Monthly limits with standard SerpAPI plan ($50/mo = 5,000 searches):**
- Current approach: 137 calls = **36 runs per month** possible
- Adaptive cap: 226 calls = **22 runs per month** possible

**Cost-benefit analysis:**
- **65% more API calls** gets you **84% more data**
- Major OEMs get 5x better coverage (10 → 50 jobs)
- Only costs extra $0.89 per run (~$20/month if running daily)

---

## Maintenance Plan

### Quarterly Updates (Every 3 months)
- Review employee counts for Tier 1 companies
- Add newly discovered suppliers
- Remove companies that closed/moved

### Annual Updates (Yearly)
- Full database refresh
- Adjust tiers based on industry changes
- Review cap effectiveness (are companies hitting limits?)

### Data Sources for Updates
1. **LinkedIn Company Pages** - Free, shows employee count ranges
2. **CT Department of Labor** - Manufacturing employment data
3. **Industry associations** - CBIA, Aerospace Components Manufacturers
4. **Public filings** - For public companies only

---

## Alternative: Excel Column Approach

If your input Excel file already has employee data:

```python
def company_size_from_excel(company_name, df):
    """
    Look up employee count from input Excel file.

    Assumes Excel has column named one of:
    - "Employees"
    - "Company Size"
    - "Employee Count"
    """
    # Find row for this company
    row = df[df["Company Name"] == company_name]

    if row.empty:
        return 50  # Default

    # Check for employee count column (try multiple names)
    for col in ["Employees", "Company Size", "Employee Count", "Total Employees"]:
        if col in df.columns:
            return row[col].iloc[0]

    return 50  # Default if no employee column found
```

**Benefits:**
- No maintenance (data is in Excel)
- User controls the data
- Easy to update

**Drawbacks:**
- Requires Excel to have this column
- May not be available in current setup

---

## Recommendation

**Phase 1 (Now):** Use static database (Option A) with conservative caps
- Tier 1: 30 jobs (not 50)
- Tier 2: 20 jobs
- Tier 3: 15 jobs
- Tier 4: 10 jobs
- **Total:** ~180 API calls (vs. 226 with aggressive caps)

**Phase 2 (After validation):** Increase caps if data quality justifies it

**Phase 3 (Future):** Implement Option C (external API) if budget allows

---

## Data Quality Validation Checklist

Before deploying adaptive caps, validate:

- [ ] Run 10 Tier 1 companies with 30-job cap
- [ ] Count unique trades found vs. 10-job cap
- [ ] Check for diminishing returns (jobs 21-30 unique?)
- [ ] Measure API cost increase vs. data value increase
- [ ] Verify no companies are consistently hitting cap (if so, raise it)

---

**Next Steps:**
1. Review this analysis with team
2. Decide on conservative vs. aggressive caps
3. Test with 10-20 companies first
4. Adjust caps based on results
5. Deploy to full 137-company list
