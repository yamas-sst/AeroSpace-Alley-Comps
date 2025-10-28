# Strategic Test Configuration - 25 Companies (5 per Tier)

**Purpose:** Validate 5-tier adaptive caps with minimal API usage
**Total companies:** 25 (5 per tier)
**Expected API calls:** ~75 (vs 150 for 50 companies)
**Strategy:** Balanced validation across all tiers with minimal cost

---

## Strategic Distribution - 25 Companies

### Tier 1: 10,000+ Employees (5 companies)

| # | Company Name | Employees | Job Cap | API Calls |
|---|--------------|-----------|---------|-----------|
| 1 | Pratt & Whitney | 35,000 | 50 | 5 |
| 2 | Collins Aerospace | 15,000 | 50 | 5 |
| 3-5 | (3 more if available, or use these 2 multiple times) | 10K+ | 50 | 5 each |

**Tier 1 Subtotal:** 5 companies × 5 calls = **25 API calls**

**Note:** If you only have 2 Tier 1 companies in your dataset, you can:
- Test with just those 2 (10 API calls)
- Reduce to 3 companies for Tier 1
- Allocate extra companies to Tier 2-3 instead

---

### Tier 2: 1,000-9,999 Employees (5 companies)

| # | Company Name | Employees | Job Cap | API Calls |
|---|--------------|-----------|---------|-----------|
| 1 | Sikorsky Aircraft | 8,000 | 40 | 4 |
| 2 | GE Aerospace | 3,500 | 40 | 4 |
| 3 | Kaman Corporation | 2,400 | 40 | 4 |
| 4 | Barnes Aerospace | 1,200 | 40 | 4 |
| 5 | (1 more Tier 2) | 1-10K | 40 | 4 |

**Tier 2 Subtotal:** 5 companies × 4 calls = **20 API calls**

---

### Tier 3: 200-999 Employees (5 companies)

| # | Company Name | Employees | Job Cap | API Calls |
|---|--------------|-----------|---------|-----------|
| 1 | GKN Aerospace | 800 | 25 | 3 |
| 2 | Chromalloy Connecticut | 600 | 25 | 3 |
| 3 | Ensign-Bickford | 500 | 25 | 3 |
| 4 | Triumph Group | 450 | 25 | 3 |
| 5 | Eaton Aerospace | 400 | 25 | 3 |

**Tier 3 Subtotal:** 5 companies × 3 calls = **15 API calls**

---

### Tier 4: 50-199 Employees (5 companies)

| # | Company Name | Employees | Job Cap | API Calls |
|---|--------------|-----------|---------|-----------|
| 1 | Curtiss-Wright | 150 | 15 | 2 |
| 2 | Aero Gear Inc | 120 | 15 | 2 |
| 3 | Stanadyne LLC | 100 | 15 | 2 |
| 4 | Parker Hannifin | 100 | 15 | 2 |
| 5 | Breeze-Eastern | 90 | 15 | 2 |

**Tier 4 Subtotal:** 5 companies × 2 calls = **10 API calls**

---

### Tier 5: 10-49 Employees (5 companies)

| # | Company Name | Employees | Job Cap | API Calls |
|---|--------------|-----------|---------|-----------|
| 1-5 | Various small shops | 10-49 | 10 | 1 each |

**Tier 5 Subtotal:** 5 companies × 1 call = **5 API calls**

---

## API Call Summary - Strategic Test

| Tier | Companies | Job Cap | Calls Per Company | Total Calls |
|------|-----------|---------|-------------------|-------------|
| **Tier 1** (10K+) | 5 | 50 | 5 | **25** |
| **Tier 2** (1-10K) | 5 | 40 | 4 | **20** |
| **Tier 3** (200-999) | 5 | 25 | 3 | **15** |
| **Tier 4** (50-199) | 5 | 15 | 2 | **10** |
| **Tier 5** (10-49) | 5 | 10 | 1 | **5** |
| **TOTAL** | **25** | | | **75 API calls** |

**Cost savings vs 50-company test:** 75 calls vs 150 calls = **50% reduction**

**Still validates:**
- ✅ All 5 tiers tested
- ✅ Tier assignment logic
- ✅ Adaptive caps working
- ✅ New keywords captured
- ✅ API call calculations accurate

---

## Alternative: Ultra-Conservative Test (15 companies)

If you want even fewer API calls:

| Tier | Companies | API Calls |
|------|-----------|-----------|
| Tier 1 | 2 | 10 |
| Tier 2 | 3 | 12 |
| Tier 3 | 3 | 9 |
| Tier 4 | 4 | 8 |
| Tier 5 | 3 | 3 |
| **TOTAL** | **15** | **42 API calls** |

---

## Alternative: Minimum Viable Test (10 companies)

Bare minimum to validate all tiers:

| Tier | Companies | API Calls |
|------|-----------|-----------|
| Tier 1 | 2 | 10 |
| Tier 2 | 2 | 8 |
| Tier 3 | 2 | 6 |
| Tier 4 | 2 | 4 |
| Tier 5 | 2 | 2 |
| **TOTAL** | **10** | **30 API calls** |

---

## Recommended: 25 Companies (5 per tier)

**Why this is optimal:**

1. **Balanced validation:** Equal representation across all tiers
2. **Statistical significance:** 5 samples per tier gives confidence
3. **Reasonable cost:** 75 API calls is manageable
4. **Complete coverage:** Tests all tier logic and cap levels
5. **Error detection:** Enough samples to catch outliers

**Alternatives if needed:**
- **Conservative:** 15 companies (42 calls) if budget is tight
- **Minimum:** 10 companies (30 calls) for quick validation only

---

## Test Excel File Structure

**Create:** `data/Test_25_Strategic.xlsx`

**Columns:**
- Company Name
- Employees (optional, for validation)
- Expected Tier (optional, for validation)

**25 rows:** 5 companies from each tier (as listed above)

---

## Test Config File

**Create:** `resources/config_test_25.json`

```json
{
  "api_keys": [
    {
      "label": "Test-25-Strategic",
      "key": "YOUR_API_KEY_HERE",
      "limit": 100,
      "priority": 1
    }
  ],
  "settings": {
    "testing_mode": true,
    "testing_company_limit": 25,
    "input_file": "data/Test_25_Strategic.xlsx",
    "output_file": "output/Test_25_Results.xlsx",
    "max_api_calls_per_key": 100,
    "min_interval_seconds": 3.0,
    "max_threads": 3
  }
}
```

---

## Expected Results

### Processing Time
- **25 companies:** 4-6 minutes (75 API calls × 3 seconds = 225 seconds = 3.75 min)
- Plus processing overhead: ~2 minutes
- **Total:** 5-8 minutes

### Jobs Collected
- **Tier 1 (5 companies):** 150-250 jobs (30-50 each)
- **Tier 2 (5 companies):** 100-200 jobs (20-40 each)
- **Tier 3 (5 companies):** 50-125 jobs (10-25 each)
- **Tier 4 (5 companies):** 25-75 jobs (5-15 each)
- **Tier 5 (5 companies):** 10-50 jobs (2-10 each)
- **Total:** 335-700 jobs estimated

### API Call Validation

**Check that actual calls match expected:**

| Company | Expected Tier | Expected Calls | Actual Calls |
|---------|---------------|----------------|--------------|
| Pratt & Whitney | 1 | 5 | ? |
| Barnes Aerospace | 2 | 4 | ? |
| GKN Aerospace | 3 | 3 | ? |
| Curtiss-Wright | 4 | 2 | ? |
| Small shop | 5 | 1 | ? |

**Variance tolerance:** ±1 call is OK (due to empty pages)

---

## Success Criteria (25 Companies)

- [ ] **All 25 companies processed** without errors
- [ ] **API calls within range:** 70-80 calls (75 ±5)
- [ ] **Tier assignment correct:** Spot check 5 companies
- [ ] **New keywords captured:** At least 3 types (engineer, supervisor, licensed)
- [ ] **Job caps enforced:** No company exceeds its tier cap
- [ ] **Processing time reasonable:** < 10 minutes
- [ ] **No circuit breaker triggers**

---

## What This Test Validates

✅ **Tier System:**
- All 5 tiers represented
- Correct tier assignment
- Appropriate caps per tier

✅ **API Efficiency:**
- 75 calls for 25 companies (3:1 ratio)
- Mega-corps get 5x coverage vs small shops
- No wasted calls

✅ **Keyword Expansion:**
- Licensed trades (electricians, plumbers)
- Technical leadership (engineers, supervisors)
- Certifications (AWS, ASNT, EPA 608)

✅ **Adaptive Caps Working:**
- Tier 1: Can collect up to 50 jobs
- Tier 5: Limited to 10 jobs
- Pagination stops at cap

---

## Quick Start Commands

```bash
# 1. Create test file with 25 companies
# (Use Excel or CSV with the companies listed above)

# 2. Create test config
# (Use the JSON above)

# 3. Run test
python AeroComps.py

# 4. Check results
# - Console output shows tiers and caps
# - Excel output has jobs from all tiers
# - API audit log shows ~75 calls
```

---

## If You Need Fewer API Calls

### Option A: Test Tiers Separately

**Day 1:** Test Tier 1-2 only (10 companies, 45 calls)
**Day 2:** Test Tier 3-4 only (10 companies, 25 calls)
**Day 3:** Test Tier 5 only (5 companies, 5 calls)

**Total:** Still 25 companies, but spread over 3 days

### Option B: Start with Minimum (10 companies)

Test with 2 companies per tier first (30 calls)
- If successful, expand to 25 companies
- If issues found, fix and re-test with 10

### Option C: Focus on Key Tiers

**Priority tiers:** Tier 1-3 (where most jobs are)
- Tier 1: 5 companies (25 calls)
- Tier 2: 5 companies (20 calls)
- Tier 3: 5 companies (15 calls)
- **Total:** 15 companies, 60 calls

**Skip:** Tier 4-5 for initial test (can add later)

---

## Recommendation

**Start with 25 companies (5 per tier):**
- Strategic use of 75 API calls
- Validates all tiers
- Balanced coverage
- Reasonable test time (5-8 minutes)

**Alternative if needed:**
- 15 companies (42 calls) for tighter budget
- 10 companies (30 calls) for quick validation

---

**Next Step:** Create your test Excel file with 25 companies (5 from each tier) and run the test!
