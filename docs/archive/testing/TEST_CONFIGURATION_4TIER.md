# Test Configuration - 4-Tier Company Testing

**Purpose:** Test adaptive job caps with balanced representation across all company sizes

**Test size:** 40 companies (10 from each tier)

---

## Test Company Selection (10 per tier = 40 total)

### Tier 1: Major OEMs (1,000+ employees) - 10 companies

| # | Company Name | Approx. Employees | Job Cap | API Calls Expected |
|---|--------------|-------------------|---------|-------------------|
| 1 | Pratt & Whitney | 35,000 | 50 | 5 |
| 2 | Collins Aerospace | 15,000 | 50 | 5 |
| 3 | Sikorsky Aircraft | 8,000 | 50 | 5 |
| 4 | GE Aerospace | 3,500 | 50 | 5 |
| 5 | Kaman Corporation | 2,400 | 30 | 3 |
| 6 | Barnes Aerospace | 1,200 | 30 | 3 |
| 7-10 | (4 more Tier 1 if available) | 1,000+ | 30-50 | 3-5 each |

**Tier 1 Subtotal:** 10 companies × avg 4 calls = **40 API calls**

---

### Tier 2: Medium Suppliers (200-999 employees) - 10 companies

| # | Company Name | Approx. Employees | Job Cap | API Calls Expected |
|---|--------------|-------------------|---------|-------------------|
| 1 | GKN Aerospace | 800 | 25 | 3 |
| 2 | Chromalloy Connecticut | 600 | 25 | 3 |
| 3 | Ensign-Bickford Aerospace | 500 | 25 | 3 |
| 4 | Triumph Group | 450 | 25 | 3 |
| 5 | Eaton Aerospace | 400 | 20 | 2 |
| 6 | Senior Aerospace BWT | 350 | 20 | 2 |
| 7 | Precision Castparts Corp | 300 | 20 | 2 |
| 8 | Woodward Inc | 250 | 20 | 2 |
| 9 | Heroux-Devtek | 200 | 20 | 2 |
| 10 | (1 more Tier 2 if available) | 200+ | 20 | 2 |

**Tier 2 Subtotal:** 10 companies × avg 2.4 calls = **24 API calls**

---

### Tier 3: Small-Medium Suppliers (50-199 employees) - 10 companies

| # | Company Name | Approx. Employees | Job Cap | API Calls Expected |
|---|--------------|-------------------|---------|-------------------|
| 1 | Curtiss-Wright Flow Control | 150 | 15 | 2 |
| 2 | Aero Gear Inc | 120 | 15 | 2 |
| 3 | Stanadyne LLC | 100 | 15 | 2 |
| 4 | Parker Hannifin Aerospace | 100 | 15 | 2 |
| 5 | Breeze-Eastern (TransDigm) | 90 | 15 | 2 |
| 6 | Connecticut Spring & Stamping | 85 | 10 | 1 |
| 7 | Standard Aero Components | 75 | 10 | 1 |
| 8 | Tyler Technologies Aerospace | 60 | 10 | 1 |
| 9-10 | (2 more Tier 3 companies) | 50-199 | 10-15 | 1-2 each |

**Tier 3 Subtotal:** 10 companies × avg 1.6 calls = **16 API calls**

---

### Tier 4: Small Shops (10-49 employees) - 10 companies

| # | Company Name | Approx. Employees | Job Cap | API Calls Expected |
|---|--------------|-------------------|---------|-------------------|
| 1-10 | Various small shops | 10-49 | 10 | 1 each |

**Tier 4 Subtotal:** 10 companies × 1 call = **10 API calls**

---

## Test Configuration API Call Summary

| Tier | Companies | Avg Job Cap | Avg API Calls Per Company | Total API Calls |
|------|-----------|-------------|---------------------------|-----------------|
| **Tier 1** | 10 | 40 | 4.0 | **40** |
| **Tier 2** | 10 | 23 | 2.4 | **24** |
| **Tier 3** | 10 | 13 | 1.6 | **16** |
| **Tier 4** | 10 | 10 | 1.0 | **10** |
| **TOTAL** | **40** | **21.5 avg** | **2.25 avg** | **90 API calls** |

---

## Comparison: Test vs Full Production

| Scenario | Companies | Total API Calls | Jobs Collected (Est.) | Cost per Run |
|----------|-----------|-----------------|----------------------|--------------|
| **Current (10 jobs/company)** | 137 | 137 | ~1,370 | $1.37 |
| **Test (40 companies, adaptive)** | 40 | 90 | ~860 | $0.90 |
| **Production (137, conservative)** | 137 | 180 | ~2,200 | $1.80 |
| **Production (137, aggressive)** | 137 | 226 | ~2,520 | $2.26 |

**Test configuration uses 90 API calls** to validate the adaptive cap logic across all tier types.

---

## Expected Test Results

### What to Validate:

1. **Tier 1 companies (10 companies):**
   - Should collect 30-50 jobs each
   - Should find 8-15 unique trades per company
   - Should see high diversity (multiple welders, machinists, supervisors)

2. **Tier 2 companies (10 companies):**
   - Should collect 20-25 jobs each
   - Should find 5-10 unique trades per company
   - Should see moderate diversity

3. **Tier 3 companies (10 companies):**
   - Should collect 10-15 jobs each
   - Should find 3-7 unique trades per company
   - Should see focused hiring (fewer roles)

4. **Tier 4 companies (10 companies):**
   - Should collect 5-10 jobs each (many may have < 10 jobs available)
   - Should find 1-3 unique trades per company
   - Should see very focused hiring (1-2 specific roles)

### Success Criteria:

- ✅ All 40 companies processed without errors
- ✅ API calls match expected (90 ± 10 calls)
- ✅ Tier 1 companies show more diversity than Tier 4
- ✅ New keywords capture licensed trades (electricians, plumbers, HVAC)
- ✅ Technical leadership roles appear (engineers, supervisors)
- ✅ No false positives (non-trades roles)
- ✅ Excel output includes proper categorization

---

## Config File for Testing

**Create:** `resources/config_test_4tier.json`

```json
{
  "api_keys": [
    {
      "label": "Test-4Tier",
      "key": "your_api_key_here",
      "limit": 100,
      "priority": 1
    }
  ],
  "settings": {
    "testing_mode": true,
    "testing_company_limit": 40,
    "input_file": "data/Test_4Tier_40Companies.xlsx",
    "output_file": "output/Test_4Tier_Results.xlsx",
    "max_api_calls_per_key": 100,
    "min_interval_seconds": 3.0,
    "max_threads": 3,
    "adaptive_job_caps": true,
    "enable_categorization": true
  }
}
```

---

## Test Excel File Structure

**Create:** `data/Test_4Tier_40Companies.xlsx`

**Columns:**
- Company Name
- Employees (optional - for validation)
- Tier (optional - for validation)

**Rows:** 40 companies (10 from each tier as listed above)

---

## Post-Test Analysis Checklist

After running the test with 40 companies:

- [ ] Review total API calls (should be ~90)
- [ ] Check job distribution by tier (Tier 1 > Tier 2 > Tier 3 > Tier 4)
- [ ] Validate unique trades count per tier
- [ ] Review Category column (Hands-On vs Engineering vs Supervision)
- [ ] Check for licensed trades (electrician, plumber, HVAC)
- [ ] Verify technical leadership captured (engineers, supervisors)
- [ ] Look for any false positives or missing roles
- [ ] Measure processing time (should be 5-7 minutes for 40 companies)

---

## Adjustments After Testing

Based on test results, may need to adjust:

1. **Job caps per tier** (if hitting limits frequently)
2. **Keywords** (if missing roles or too many false positives)
3. **Company tier assignments** (if employee counts are inaccurate)
4. **Categorization logic** (if categories are wrong)

---

**Next Step:** Create the 40-company test Excel file and run the test with implemented code.
