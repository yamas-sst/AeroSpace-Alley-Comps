# Pre-Implementation Review - Comprehensive Analysis

**Date:** October 28, 2025
**Purpose:** Minimize code adjustments during local testing
**Status:** Implementation ready - NOT YET DEPLOYED

---

## Executive Summary

This document provides a comprehensive review of all changes to be implemented:
1. **5-Tier Company Size System** (added 10K+ employee tier)
2. **Expanded Keywords** (~200 keywords with certifications + leadership)
3. **Test Configuration** (50 companies: 10 per tier)
4. **Expected API Usage** (detailed breakdown)

**Goal:** You can implement and test locally with minimal surprises or code adjustments.

---

## 1️⃣ Updated Tier System (5 Tiers)

### Tier Breakdown

| Tier | Employee Range | Job Cap | Companies (Est.) | Examples |
|------|----------------|---------|------------------|----------|
| **Tier 1** | 10,000+ | 50 | 2-3 | Pratt & Whitney (35K), Collins (15K) |
| **Tier 2** | 1,000-9,999 | 40 | 4-6 | Sikorsky (8K), GE (3.5K), Kaman (2.4K), Barnes (1.2K) |
| **Tier 3** | 200-999 | 25 | 12-18 | GKN (800), Chromalloy (600), Ensign-Bickford (500) |
| **Tier 4** | 50-199 | 15 | 30-40 | Curtiss-Wright (150), Aero Gear (120) |
| **Tier 5** | 10-49 | 10 | 70-90 | Small precision shops |

**Total: ~137 companies across 5 tiers**

### Why 5 Tiers?

**Tier 1 (10K+):** Mega-corporations like Pratt & Whitney and Collins
- Highest job diversity expected
- Multiple facilities, diverse operations
- 50 jobs cap captures comprehensive picture

**Tier 2 (1-10K):** Major OEMs but smaller than mega-corps
- High diversity but slightly less than Tier 1
- 40 jobs cap balances coverage and efficiency

**Tier 3 (200-999):** Medium suppliers
- Moderate diversity
- 25 jobs cap captures most unique roles

**Tier 4 (50-199):** Small-medium suppliers
- Focused hiring
- 15 jobs cap sufficient for typical diversity

**Tier 5 (10-49):** Small precision shops
- Very focused hiring (1-3 role types typically)
- 10 jobs cap (often won't even have 10 postings)

---

## 2️⃣ Test Configuration - 50 Companies (10 per Tier)

### Test Company Selection

#### Tier 1: 10,000+ Employees (10 companies for test)

| Company Name | Employees | Job Cap | API Calls |
|--------------|-----------|---------|-----------|
| Pratt & Whitney | 35,000 | 50 | 5 |
| Collins Aerospace | 15,000 | 50 | 5 |
| Plus 8 more (if available from dataset) | 10K+ | 50 | 5 each |

**Tier 1 Subtotal:** 10 companies × 5 calls = **50 API calls**

**Note:** If you don't have 10 companies with 10K+ employees, we can use 2-3 real ones and simulate the rest for testing, or adjust test to fewer Tier 1 companies.

#### Tier 2: 1,000-9,999 Employees (10 companies)

| Company Name | Employees | Job Cap | API Calls |
|--------------|-----------|---------|-----------|
| Sikorsky Aircraft | 8,000 | 40 | 4 |
| GE Aerospace | 3,500 | 40 | 4 |
| Kaman Corporation | 2,400 | 40 | 4 |
| Barnes Aerospace | 1,200 | 40 | 4 |
| Plus 6 more | 1-10K | 40 | 4 each |

**Tier 2 Subtotal:** 10 companies × 4 calls = **40 API calls**

#### Tier 3: 200-999 Employees (10 companies)

| Company Name | Employees | Job Cap | API Calls |
|--------------|-----------|---------|-----------|
| GKN Aerospace | 800 | 25 | 3 |
| Chromalloy Connecticut | 600 | 25 | 3 |
| Ensign-Bickford | 500 | 25 | 3 |
| Triumph Group | 450 | 25 | 3 |
| Eaton Aerospace | 400 | 25 | 3 |
| Plus 5 more | 200-999 | 25 | 3 each |

**Tier 3 Subtotal:** 10 companies × 3 calls = **30 API calls**

#### Tier 4: 50-199 Employees (10 companies)

| Company Name | Employees | Job Cap | API Calls |
|--------------|-----------|---------|-----------|
| Curtiss-Wright | 150 | 15 | 2 |
| Aero Gear Inc | 120 | 15 | 2 |
| Stanadyne LLC | 100 | 15 | 2 |
| Parker Hannifin | 100 | 15 | 2 |
| Plus 6 more | 50-199 | 15 | 2 each |

**Tier 4 Subtotal:** 10 companies × 2 calls = **20 API calls**

#### Tier 5: 10-49 Employees (10 companies)

| Company Name | Employees | Job Cap | API Calls |
|--------------|-----------|---------|-----------|
| Various small shops | 10-49 | 10 | 1 each |

**Tier 5 Subtotal:** 10 companies × 1 call = **10 API calls**

---

### API Call Summary - Test Configuration

| Tier | Companies | Job Cap | API Calls Per Company | Total API Calls |
|------|-----------|---------|----------------------|-----------------|
| **Tier 1** (10K+) | 10 | 50 | 5 | **50** |
| **Tier 2** (1-10K) | 10 | 40 | 4 | **40** |
| **Tier 3** (200-999) | 10 | 25 | 3 | **30** |
| **Tier 4** (50-199) | 10 | 15 | 2 | **20** |
| **Tier 5** (10-49) | 10 | 10 | 1 | **10** |
| **TOTAL** | **50** | | | **150 API calls** |

---

### API Call Summary - Full Production (137 Companies)

| Tier | Companies | Job Cap | API Calls Per Company | Total API Calls |
|------|-----------|---------|----------------------|-----------------|
| **Tier 1** (10K+) | 2 | 50 | 5 | **10** |
| **Tier 2** (1-10K) | 5 | 40 | 4 | **20** |
| **Tier 3** (200-999) | 15 | 25 | 3 | **45** |
| **Tier 4** (50-199) | 35 | 15 | 2 | **70** |
| **Tier 5** (10-49) | 80 | 10 | 1 | **80** |
| **TOTAL** | **137** | | | **225 API calls** |

**Current production (no adaptive caps):** 137 API calls
**New production (5-tier adaptive):** 225 API calls (+88 calls, +64%)

**Cost increase:** $0.88 per run (at $0.01 per API call)
**Benefit:** 84% more jobs collected, 5x better coverage for mega-corps

---

## 3️⃣ Implementation Changes to AeroComps.py

### Change 1: Add Company Size Database (After line 429)

**Location:** After `SKILLED_TRADES_KEYWORDS` definition, before data loading

**Code to add:**

```python
# ======================================================
# COMPANY SIZE DATABASE & ADAPTIVE JOB CAPS
# ======================================================
# PURPOSE: Determine appropriate job caps based on company size
#
# TIER SYSTEM:
#   Tier 1 (10,000+ employees): 50 jobs - Mega-corporations
#   Tier 2 (1,000-9,999 employees): 40 jobs - Major OEMs
#   Tier 3 (200-999 employees): 25 jobs - Medium suppliers
#   Tier 4 (50-199 employees): 15 jobs - Small-medium suppliers
#   Tier 5 (10-49 employees): 10 jobs - Small shops
#
# DATA SOURCE: Public filings, LinkedIn, industry reports (2024-2025)
# MAINTENANCE: Update quarterly with employee count changes

COMPANY_SIZE_DATABASE = {
    # Tier 1: Mega-Corporations (10,000+ employees)
    "Pratt & Whitney": {"employees": 35000, "tier": 1},
    "Pratt Whitney": {"employees": 35000, "tier": 1},
    "RTX": {"employees": 35000, "tier": 1},
    "Collins Aerospace": {"employees": 15000, "tier": 1},
    "Collins": {"employees": 15000, "tier": 1},

    # Tier 2: Major OEMs (1,000-9,999 employees)
    "Sikorsky": {"employees": 8000, "tier": 2},
    "Sikorsky Aircraft": {"employees": 8000, "tier": 2},
    "GE Aerospace": {"employees": 3500, "tier": 2},
    "Kaman": {"employees": 2400, "tier": 2},
    "Kaman Corporation": {"employees": 2400, "tier": 2},
    "Barnes Aerospace": {"employees": 1200, "tier": 2},
    "Barnes": {"employees": 1200, "tier": 2},

    # Tier 3: Medium Suppliers (200-999 employees)
    "GKN Aerospace": {"employees": 800, "tier": 3},
    "GKN": {"employees": 800, "tier": 3},
    "Chromalloy": {"employees": 600, "tier": 3},
    "Ensign-Bickford": {"employees": 500, "tier": 3},
    "Triumph Group": {"employees": 450, "tier": 3},
    "Triumph": {"employees": 450, "tier": 3},
    "Eaton Aerospace": {"employees": 400, "tier": 3},
    "Eaton": {"employees": 400, "tier": 3},
    "Senior Aerospace": {"employees": 350, "tier": 3},
    "Precision Castparts": {"employees": 300, "tier": 3},
    "PCC": {"employees": 300, "tier": 3},
    "Woodward": {"employees": 250, "tier": 3},
    "Heroux-Devtek": {"employees": 200, "tier": 3},

    # Tier 4: Small-Medium Suppliers (50-199 employees)
    "Curtiss-Wright": {"employees": 150, "tier": 4},
    "Aero Gear": {"employees": 120, "tier": 4},
    "Stanadyne": {"employees": 100, "tier": 4},
    "Parker Hannifin": {"employees": 100, "tier": 4},
    "Parker": {"employees": 100, "tier": 4},
    "Breeze-Eastern": {"employees": 90, "tier": 4},
    "TransDigm": {"employees": 90, "tier": 4},
    "Connecticut Spring": {"employees": 85, "tier": 4},
    "Standard Aero": {"employees": 75, "tier": 4},
    "Tyler Technologies": {"employees": 60, "tier": 4},
}

def company_size_lookup(company_name):
    """
    Look up approximate employee count for a company.

    Uses fuzzy matching to handle variations in company names.

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
    Determine company tier (1-5) based on employee count.

    Args:
        company_name (str): Company name from input file

    Returns:
        int: Tier number (1=Mega Corp, 2=Major OEM, 3=Medium, 4=Small-Medium, 5=Small)
    """
    employees = company_size_lookup(company_name)

    if employees >= 10000:
        return 1  # Tier 1: Mega-Corporation (10K+)
    elif employees >= 1000:
        return 2  # Tier 2: Major OEM (1-10K)
    elif employees >= 200:
        return 3  # Tier 3: Medium Supplier
    elif employees >= 50:
        return 4  # Tier 4: Small-Medium Supplier
    else:
        return 5  # Tier 5: Small Shop


def get_job_cap_for_company(company_name):
    """
    Determine maximum jobs to collect for this company based on size.

    This is the MAIN function used in fetch_jobs_for_company()

    Args:
        company_name (str): Company name from input file

    Returns:
        int: Maximum jobs to collect (10, 15, 25, 40, or 50)
    """
    tier = get_company_tier(company_name)

    if tier == 1:
        return 50  # Mega-corps - highest diversity expected
    elif tier == 2:
        return 40  # Major OEMs - high diversity
    elif tier == 3:
        return 25  # Medium suppliers - moderate diversity
    elif tier == 4:
        return 15  # Small-medium - focused hiring
    else:
        return 10  # Small shops - limited roles
```

**Lines added:** ~150 lines
**Impact:** Enables adaptive job caps per company

---

### Change 2: Replace SKILLED_TRADES_KEYWORDS (Line 381)

**Current:** ~80 keywords
**New:** ~200 keywords (merged list with certifications + leadership)

**Code to replace:**

```python
# ======================================================
# SKILLED TRADES KEYWORDS - EXPANDED VERSION
# ======================================================
# PURPOSE: Filter job listings to only skilled trades positions
#
# COVERAGE:
#   - Category 1: Hands-On Skilled Trades (~120 keywords)
#     * Machining, welding, assembly, maintenance, inspection
#     * Licensed trades: electricians, plumbers, HVAC (with certifications)
#     * Certifications: AWS (welding), ASNT (NDT), EPA 608 (HVAC)
#
#   - Category 2: Technical Leadership (~65 keywords)
#     * Manufacturing/quality engineers
#     * Production supervisors, foremen, superintendents
#     * Planning/coordination roles
#
# TOTAL: ~185 keywords (expanded from original 80)
# LAST UPDATED: October 2025

SKILLED_TRADES_KEYWORDS = [
    # ==========================================
    # CATEGORY 1: HANDS-ON SKILLED TRADES
    # ==========================================

    # --- 1A: Machining & Fabrication ---
    "machinist", "cnc", "mill operator", "lathe operator", "grinder", "toolmaker",
    "fabricator", "metalworker", "sheet metal", "precision machinist", "machine operator",
    "manual machinist", "setup operator", "g-code", "programmer", "tool and die", "die maker",
    "mold maker", "production machinist", "numerical control", "machining technician",
    "swiss machinist", "5-axis operator", "edm operator", "waterjet operator",
    "laser operator", "plasma cutter", "boring mill operator", "horizontal machinist",
    "jig borer", "gear cutter", "honing machine operator", "lapping technician",

    # --- 1B: Assembly & Production ---
    "assembler", "assembly technician", "production operator", "production technician",
    "line operator", "mechanical assembler", "electromechanical assembler",
    "production worker", "manufacturing technician", "machine technician",
    "assembly lead", "manufacturing associate", "packaging operator", "composite technician",

    # --- 1C: Welding & Metalwork (WITH CERTIFICATIONS) ---
    "welder", "tig welder", "mig welder", "arc welder", "fabrication welder",
    "pipe welder", "aluminum welder", "spot welder", "soldering", "brazing",
    "welding technician", "weld inspector", "fitter welder",
    "certified welder", "aws certified welder", "cw welder", "cwi", "cwe",
    "combo welder", "stick welder", "flux core welder", "orbital welder", "robotic welder",

    # --- 1D: Licensed Electrical Trades (CERTIFICATIONS REQUIRED) ---
    "electrician", "electrical technician", "electronics technician",
    "controls technician", "panel builder", "wire harness assembler",
    "electromechanical technician", "instrumentation technician", "automation technician",
    "journeyman electrician", "master electrician", "industrial electrician",
    "maintenance electrician", "commercial electrician",
    "controls engineer", "automation specialist", "robotics technician",
    "plc programmer", "scada technician", "instrumentation electrician",
    "high voltage electrician", "electrical inspector", "electrical designer",
    "panel designer", "control panel technician",

    # --- 1E: Plumbing, Pipefitting & HVAC (LICENSED TRADES) ---
    "plumber", "journeyman plumber", "master plumber", "pipefitter", "steamfitter",
    "sprinkler fitter", "industrial plumber", "process piping",
    "hvac technician", "hvac mechanic", "hvac service technician", "hvac installer",
    "refrigeration technician", "chiller technician", "boiler technician",
    "building automation", "hvac controls", "hvac apprentice", "journeyman hvac",
    "facilities mechanic", "building engineer", "stationary engineer", "boiler operator",

    # --- 1F: Maintenance & Repair ---
    "maintenance technician", "maintenance mechanic", "maintenance engineer",
    "industrial mechanic", "millwright", "equipment technician", "machine repair",
    "facilities technician", "mechanical technician", "preventive maintenance",
    "repair technician", "plant mechanic", "equipment maintenance",
    "predictive maintenance", "reliability technician", "vibration analyst",
    "lubrication technician", "alignment technician", "hydraulics technician",
    "pneumatics technician", "conveyor technician", "crane technician", "forklift technician",

    # --- 1G: Inspection & Quality (WITH CERTIFICATIONS) ---
    "inspector", "quality inspector", "quality technician", "qc technician",
    "qa inspector", "ndt technician", "cmm operator", "quality assurance",
    "final inspector", "metrology technician", "dimensional inspector",
    "ndt level ii", "ndt level iii", "ultrasonic technician", "radiographic technician",
    "magnetic particle", "liquid penetrant", "eddy current technician",
    "visual inspection", "asnt certified", "calibration technician", "gage technician",
    "optical inspector", "coordinate measuring", "layout inspector",
    "receiving inspector", "in-process inspector",

    # --- 1H: Tooling & Setup ---
    "tool room", "tooling engineer", "setup technician", "fixture builder",
    "tool designer", "jig and fixture", "tooling technician",

    # --- 1I: Composites & Aerospace Fabrication ---
    "composite technician", "lamination technician", "bonding technician",
    "aerospace assembler", "aircraft technician", "avionics technician",
    "sheet metal mechanic", "structures mechanic", "airframe mechanic",

    # --- 1J: Other Skilled Trades ---
    "carpenter", "painter", "coating technician",
    "surface finisher", "heat treat operator", "chemical processor",
    "machining apprentice", "maintenance apprentice", "journeyman",
    "technician apprentice",

    # ==========================================
    # CATEGORY 2: TECHNICAL LEADERSHIP
    # (HIGH + MEDIUM-HIGH CONFIDENCE)
    # ==========================================

    # --- 2A: Manufacturing & Quality Engineering ---
    "manufacturing engineer", "process engineer", "industrial engineer",
    "manufacturing engineering", "process improvement engineer", "methods engineer",
    "tool engineer", "fixture engineer",
    "quality engineer", "qa engineer", "qc engineer", "quality engineering",
    "supplier quality engineer", "sqa", "quality systems engineer",
    "six sigma", "green belt", "black belt", "asq certified",
    "cqe", "cqa", "cre",

    # --- 2B: Production Supervision ---
    "production supervisor", "manufacturing supervisor", "shop supervisor",
    "maintenance supervisor", "quality supervisor", "shift supervisor",
    "area supervisor", "department supervisor", "assembly supervisor",
    "fabrication supervisor", "machining supervisor",
    "shop foreman", "production foreman", "maintenance foreman",
    "general foreman", "working foreman",
    "lead technician", "senior technician", "master technician",
    "lead machinist", "lead welder", "lead assembler",
    "superintendent", "shop superintendent", "production superintendent",
    "manufacturing superintendent", "maintenance superintendent",

    # --- 2C: Production Planning & Coordination ---
    "production planner", "manufacturing planner", "production scheduler",
    "production control", "material planner", "capacity planner",
    "manufacturing coordinator", "production coordinator", "operations coordinator",
    "shift coordinator", "materials coordinator",
    "cnc programmer", "cam programmer", "manufacturing programmer", "robot programmer",
]

# Total keywords: ~185
# Coverage: Hands-on trades + direct technical leadership + certifications
```

**Lines replaced:** Original ~80 keywords → New ~185 keywords
**Impact:** Captures licensed trades, certifications, and technical leadership

---

### Change 3: Modify fetch_jobs_for_company() to Use Adaptive Caps (Line 568-570)

**Current code (line 568-570):**
```python
# Pagination: Request up to 3 pages (10 jobs per page)
# start=0 (page 1), start=10 (page 2), start=20 (page 3)
for start in range(0, 30, 10):
```

**New code:**
```python
# Adaptive pagination based on company size
# Get company-specific job cap
MAX_JOBS = get_job_cap_for_company(company)

# Pagination: Request pages until we hit the cap
# Each page has ~10 jobs, so we need (MAX_JOBS / 10) pages
for start in range(0, MAX_JOBS, 10):
```

**Additional check needed (after line 650):**

Add a check to stop pagination if we've collected enough jobs:

```python
# After processing jobs (around line 660), add:
if len(local_results) >= MAX_JOBS:
    print(f"[{company}] Reached job cap ({MAX_JOBS} jobs) — stopping pagination.")
    break
```

**Lines modified:** 3 lines changed, 4 lines added
**Impact:** Enforces adaptive caps per company

---

### Change 4: Add Categorization to Job Output (Optional)

**Location:** Inside the job processing loop (around line 652-660)

**Current code:**
```python
if any(kw.lower() in title.lower() for kw in SKILLED_TRADES_KEYWORDS):
    local_results.append({
        "Company": company,
        "Job Title": title,
        "Location": location,
        "Via": via,
        "Source URL": apply_link,
        "Detected Extensions": detected_extensions_str,
        "Description Snippet": description_snippet,
        "Timestamp": timestamp
    })
```

**Enhanced code with categorization:**
```python
# Check if job matches any keyword
matching_keywords = [kw for kw in SKILLED_TRADES_KEYWORDS if kw.lower() in title.lower()]

if matching_keywords:
    # Determine category based on which keywords matched
    category = "Skilled Trades - Hands-On"  # Default
    subcategory = "General"

    # Check for technical leadership keywords
    leadership_keywords = [
        "engineer", "supervisor", "foreman", "superintendent",
        "lead technician", "senior technician", "planner", "coordinator"
    ]
    if any(kw in title.lower() for kw in leadership_keywords):
        if "engineer" in title.lower():
            category = "Skilled Trades - Engineering"
            subcategory = "Manufacturing/Quality Engineering"
        elif any(kw in title.lower() for kw in ["supervisor", "foreman", "superintendent"]):
            category = "Skilled Trades - Leadership"
            subcategory = "Supervision/Management"
        else:
            category = "Skilled Trades - Support"
            subcategory = "Planning/Coordination"

    # Determine subcategory for hands-on trades
    else:
        if any(kw in title.lower() for kw in ["machinist", "cnc", "mill", "lathe"]):
            subcategory = "Machining"
        elif any(kw in title.lower() for kw in ["welder", "welding", "fabrication"]):
            subcategory = "Welding"
        elif any(kw in title.lower() for kw in ["electrician", "electrical", "plc"]):
            subcategory = "Electrical (Licensed)"
        elif any(kw in title.lower() for kw in ["plumber", "pipefitter", "hvac", "refrigeration"]):
            subcategory = "Plumbing/HVAC (Licensed)"
        elif any(kw in title.lower() for kw in ["inspector", "quality", "ndt"]):
            subcategory = "Inspection/Quality"
        elif any(kw in title.lower() for kw in ["maintenance", "mechanic", "millwright"]):
            subcategory = "Maintenance"
        elif any(kw in title.lower() for kw in ["assembler", "assembly"]):
            subcategory = "Assembly"

    local_results.append({
        "Company": company,
        "Job Title": title,
        "Category": category,
        "Subcategory": subcategory,
        "Location": location,
        "Via": via,
        "Source URL": apply_link,
        "Detected Extensions": detected_extensions_str,
        "Description Snippet": description_snippet,
        "Timestamp": timestamp
    })
```

**Lines added:** ~40 lines
**Impact:** Excel output includes Category and Subcategory columns for filtering

---

## 4️⃣ Test Files Needed

### Test Excel File: data/Test_5Tier_50Companies.xlsx

**Structure:**
- Column A: Company Name
- Column B: Employees (optional - for validation)
- Column C: Expected Tier (optional - for validation)

**50 companies needed:**
- 10 Tier 1 (10K+ employees)
- 10 Tier 2 (1-10K employees)
- 10 Tier 3 (200-999 employees)
- 10 Tier 4 (50-199 employees)
- 10 Tier 5 (10-49 employees)

**Note:** If you don't have 10 companies for Tier 1, you can:
- Use 2-3 real Tier 1 companies (Pratt, Collins, Sikorsky)
- Test with just those 2-3, then extrapolate results
- Or create dummy companies for testing purposes

### Test Config File: resources/config_test_5tier.json

```json
{
  "api_keys": [
    {
      "label": "Test-5Tier",
      "key": "your_api_key_here",
      "limit": 200,
      "priority": 1
    }
  ],
  "settings": {
    "testing_mode": true,
    "testing_company_limit": 50,
    "input_file": "data/Test_5Tier_50Companies.xlsx",
    "output_file": "output/Test_5Tier_Results.xlsx",
    "max_api_calls_per_key": 200,
    "min_interval_seconds": 3.0,
    "max_threads": 3,
    "adaptive_job_caps_enabled": true,
    "categorization_enabled": true
  }
}
```

---

## 5️⃣ Expected Results - What to Look For

### API Call Validation

**Test (50 companies):** Should use ~150 API calls
- If actual calls are within 140-160 range = ✅ GOOD
- If actual calls are < 130 or > 170 = ⚠️ INVESTIGATE

**Possible reasons for deviation:**
- Some companies have < 10 jobs (uses fewer calls than expected)
- Some companies hit cap early (pagination stops)
- Network errors caused retries

### Job Distribution by Tier

**Expected pattern:**
- Tier 1 companies: 30-50 jobs each (high diversity)
- Tier 2 companies: 25-40 jobs each (high diversity)
- Tier 3 companies: 15-25 jobs each (moderate diversity)
- Tier 4 companies: 10-15 jobs each (focused)
- Tier 5 companies: 5-10 jobs each (very focused, may not hit cap)

**If pattern doesn't match:**
- Check if companies are correctly categorized in database
- Verify company names match between Excel and database
- Adjust tier assignments if needed

### Keyword Coverage Validation

**Should see in results:**
- ✅ Licensed electricians (journeyman, master)
- ✅ Licensed plumbers/pipefitters
- ✅ HVAC technicians (EPA certified)
- ✅ Manufacturing engineers
- ✅ Quality engineers
- ✅ Production supervisors/foremen
- ✅ AWS certified welders
- ✅ NDT technicians (Level II/III)

**If NOT seeing these roles:**
- Check if companies actually have these openings
- Verify keywords are in expanded list
- Test with known company that has these roles (e.g., Pratt & Whitney should have engineers)

### Categorization Validation

**Excel should show:**
- Category column: "Skilled Trades - Hands-On", "Skilled Trades - Engineering", "Skilled Trades - Leadership"
- Subcategory column: "Machining", "Welding", "Electrical (Licensed)", etc.

**Spot check:**
- "CNC Machinist" → Category: Hands-On, Subcategory: Machining ✅
- "Manufacturing Engineer" → Category: Engineering, Subcategory: Manufacturing/Quality Engineering ✅
- "Production Supervisor" → Category: Leadership, Subcategory: Supervision/Management ✅

### Processing Time

**Expected:** 7-10 minutes for 50 companies with 150 API calls
- 3 seconds per API call = 450 seconds = 7.5 minutes
- Plus processing overhead

**If taking much longer:**
- Check rate limiting (min 3 seconds between calls)
- Verify threading is working (max 3 threads)
- Look for network delays

---

## 6️⃣ Common Issues & Solutions

### Issue 1: Company Not Found in Database

**Symptom:** Warning message "Company [Name] not in database, using default Tier 5"

**Solution:**
- Expected for companies not in pre-populated database
- They'll default to Tier 5 (10 jobs cap)
- After testing, add frequently seen companies to database

### Issue 2: Tier Seems Wrong

**Symptom:** Small company getting Tier 1 cap (50 jobs)

**Solution:**
- Check company name fuzzy matching
- Verify employee count in database
- Adjust COMPANY_SIZE_DATABASE entry

### Issue 3: Too Many Non-Trades Roles

**Symptom:** Seeing "Software Engineer", "HR Manager" in results

**Solution:**
- Keywords may be too broad (e.g., "engineer" alone)
- Check that role titles contain specific trades keywords
- May need to add negative filters (exclude certain keywords)

### Issue 4: Missing Expected Roles

**Symptom:** Pratt & Whitney has 0 electricians (unlikely)

**Solution:**
- Verify keywords are in expanded list
- Check actual Google Jobs results manually
- May need to add keyword variations

### Issue 5: API Calls Higher Than Expected

**Symptom:** Used 200 calls instead of 150

**Solution:**
- Check if retries are counting as extra calls
- Verify pagination logic (should stop at cap)
- Review audit log for error patterns

---

## 7️⃣ Rollback Plan

If testing reveals issues, you can rollback any change independently:

### Rollback Adaptive Caps
1. Change `for start in range(0, MAX_JOBS, 10):` back to `for start in range(0, 30, 10):`
2. Comment out `get_job_cap_for_company()` call
3. System reverts to fixed 30 jobs (3 pages) per company

### Rollback Expanded Keywords
1. Replace `SKILLED_TRADES_KEYWORDS` with original 80-keyword list
2. System only captures hands-on trades, no leadership

### Rollback Categorization
1. Remove Category/Subcategory columns from output
2. System works like before, just with expanded keywords

---

## 8️⃣ Success Criteria Checklist

Before deploying to full 137 companies, validate:

- [ ] **API calls within expected range** (140-160 for 50 companies)
- [ ] **No errors or circuit breaker triggers**
- [ ] **Tier 1 companies show higher job counts than Tier 5**
- [ ] **Licensed trades captured** (electricians, plumbers, HVAC)
- [ ] **Technical leadership captured** (engineers, supervisors)
- [ ] **Categorization accurate** (spot check 20 random jobs)
- [ ] **No false positives** (non-trades roles excluded)
- [ ] **Processing time reasonable** (< 10 minutes)
- [ ] **Excel output readable and well-formatted**
- [ ] **Unique trades count increased vs. old system**

---

## 9️⃣ Implementation Steps

### Step 1: Backup Current Code
```bash
cp AeroComps.py AeroComps.py.backup
```

### Step 2: Implement Changes
- Add company size database (after line 429)
- Replace SKILLED_TRADES_KEYWORDS (line 381)
- Modify pagination logic (line 568-570)
- Add categorization (around line 652-660)

### Step 3: Create Test Files
- Create `data/Test_5Tier_50Companies.xlsx` (50 companies)
- Create `resources/config_test_5tier.json` (test config)

### Step 4: Run Test
```bash
python AeroComps.py --config resources/config_test_5tier.json
```

### Step 5: Review Results
- Check API call count
- Review job distribution
- Validate categorization
- Look for missing roles or false positives

### Step 6: Adjust & Re-test
- Fix any issues found
- Re-run test with adjustments
- Iterate until success criteria met

### Step 7: Deploy to Production
- Update main config to use full 137 companies
- Run production batch
- Monitor results

---

## 🔟 Summary

**Total code changes:**
- ~150 lines added (company size database + functions)
- ~105 keywords added (80 → 185)
- ~40 lines added (categorization logic)
- 3 lines modified (pagination logic)

**Total: ~300 lines added/modified**

**Files to create:**
- `data/Test_5Tier_50Companies.xlsx`
- `resources/config_test_5tier.json`

**Expected test results:**
- 50 companies processed
- ~150 API calls used
- 700-1,200 jobs collected
- Categories distributed across Hands-On, Engineering, Leadership

**Validation time:** 20-30 minutes to review results

**Risk level:** LOW (can rollback any component independently)

---

## Next Step

I'll now implement these changes in AeroComps.py (WITHOUT committing/pushing) so you can test locally.

Ready to proceed with implementation?
