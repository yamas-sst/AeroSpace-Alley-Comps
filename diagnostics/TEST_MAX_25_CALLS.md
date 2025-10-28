# Ultra-Strategic Test Configuration - MAX 25 API Calls

**Purpose:** Validate 5-tier adaptive caps with MINIMAL API usage
**Total API calls:** 25 (absolute maximum)
**Total companies:** 9 companies
**Strategy:** Validate all 5 tiers with minimum viable samples

---

## Strategic Distribution - 9 Companies, 25 API Calls

### Tier 1: 10,000+ Employees (1 company)

| # | Company Name | Employees | Job Cap | API Calls |
|---|--------------|-----------|---------|-----------|
| 1 | Pratt & Whitney | 35,000 | 50 | 5 |

**Tier 1 Subtotal:** 1 company × 5 calls = **5 API calls**

**Why just 1:** Most expensive tier (5 calls per company), but critical to validate mega-corp handling

---

### Tier 2: 1,000-9,999 Employees (2 companies)

| # | Company Name | Employees | Job Cap | API Calls |
|---|--------------|-----------|---------|-----------|
| 1 | Sikorsky Aircraft | 8,000 | 40 | 4 |
| 2 | Barnes Aerospace | 1,200 | 40 | 4 |

**Tier 2 Subtotal:** 2 companies × 4 calls = **8 API calls**

**Why 2:** Second most expensive tier, need 2 samples to validate consistency

---

### Tier 3: 200-999 Employees (2 companies)

| # | Company Name | Employees | Job Cap | API Calls |
|---|--------------|-----------|---------|-----------|
| 1 | GKN Aerospace | 800 | 25 | 3 |
| 2 | Chromalloy Connecticut | 600 | 25 | 3 |

**Tier 3 Subtotal:** 2 companies × 3 calls = **6 API calls**

**Why 2:** Medium tier, validate mid-range caps working

---

### Tier 4: 50-199 Employees (2 companies)

| # | Company Name | Employees | Job Cap | API Calls |
|---|--------------|-----------|---------|-----------|
| 1 | Curtiss-Wright | 150 | 15 | 2 |
| 2 | Aero Gear Inc | 120 | 15 | 2 |

**Tier 4 Subtotal:** 2 companies × 2 calls = **4 API calls**

**Why 2:** Lower cost tier, get 2 samples cheaply

---

### Tier 5: 10-49 Employees (2 companies)

| # | Company Name | Employees | Job Cap | API Calls |
|---|--------------|-----------|---------|-----------|
| 1 | Small Shop A | 10-49 | 10 | 1 |
| 2 | Small Shop B | 10-49 | 10 | 1 |

**Tier 5 Subtotal:** 2 companies × 1 call = **2 API calls**

**Why 2:** Cheapest tier (1 call each), easy to get multiple samples

---

## API Call Summary - Ultra-Strategic (MAX 25)

| Tier | Companies | Job Cap | Calls Per Company | Total Calls |
|------|-----------|---------|-------------------|-------------|
| **Tier 1** (10K+) | 1 | 50 | 5 | **5** |
| **Tier 2** (1-10K) | 2 | 40 | 4 | **8** |
| **Tier 3** (200-999) | 2 | 25 | 3 | **6** |
| **Tier 4** (50-199) | 2 | 15 | 2 | **4** |
| **Tier 5** (10-49) | 2 | 10 | 1 | **2** |
| **TOTAL** | **9** | | | **25 API calls** |

✅ **Exactly 25 API calls - maximum efficiency**

---

## Alternative: Even More Conservative (20 calls)

If you want to be extra safe:

| Tier | Companies | API Calls |
|------|-----------|-----------|
| Tier 1 | 1 | 5 |
| Tier 2 | 1 | 4 |
| Tier 3 | 2 | 6 |
| Tier 4 | 2 | 4 |
| Tier 5 | 1 | 1 |
| **TOTAL** | **7** | **20 calls** |

---

## Alternative: Absolute Minimum (15 calls)

Bare minimum to validate system:

| Tier | Companies | API Calls |
|------|-----------|-----------|
| Tier 1 | 1 | 5 |
| Tier 2 | 1 | 4 |
| Tier 3 | 1 | 3 |
| Tier 4 | 1 | 2 |
| Tier 5 | 1 | 1 |
| **TOTAL** | **5** | **15 calls** |

**Risk:** Only 1 sample per tier - no validation of consistency

---

## Test Excel File Structure

**Create:** `data/Test_Max25_9Companies.xlsx`

**Companies to include:**

1. Pratt & Whitney (Tier 1)
2. Sikorsky Aircraft (Tier 2)
3. Barnes Aerospace (Tier 2)
4. GKN Aerospace (Tier 3)
5. Chromalloy Connecticut (Tier 3)
6. Curtiss-Wright (Tier 4)
7. Aero Gear Inc (Tier 4)
8. Small Shop A (Tier 5)
9. Small Shop B (Tier 5)

**Columns:**
- Company Name
- Employees (optional)
- Expected Tier (optional)

---

## Test Config File

**Create:** `resources/config_test_max25.json`

```json
{
  "api_keys": [
    {
      "label": "Test-Max25",
      "key": "YOUR_API_KEY_HERE",
      "limit": 50,
      "priority": 1
    }
  ],
  "settings": {
    "testing_mode": true,
    "testing_company_limit": 9,
    "input_file": "data/Test_Max25_9Companies.xlsx",
    "output_file": "output/Test_Max25_Results.xlsx",
    "max_api_calls_per_key": 50,
    "min_interval_seconds": 3.0,
    "max_threads": 3
  }
}
```

---

## Expected Results

### Processing Time
- **9 companies:** 2-3 minutes
- **25 API calls × 3 seconds:** 75 seconds = 1.25 minutes
- **Plus overhead:** ~1 minute
- **Total:** 2-3 minutes

### Jobs Collected
- **Tier 1 (1 company):** 30-50 jobs (Pratt & Whitney)
- **Tier 2 (2 companies):** 40-80 jobs (20-40 each)
- **Tier 3 (2 companies):** 20-50 jobs (10-25 each)
- **Tier 4 (2 companies):** 10-30 jobs (5-15 each)
- **Tier 5 (2 companies):** 4-20 jobs (2-10 each)
- **Total:** 104-230 jobs estimated

### API Call Validation

**Expected pattern:**

| Company | Tier | Expected Calls | Actual Calls |
|---------|------|----------------|--------------|
| Pratt & Whitney | 1 | 5 | ? |
| Sikorsky | 2 | 4 | ? |
| Barnes | 2 | 4 | ? |
| GKN | 3 | 3 | ? |
| Chromalloy | 3 | 3 | ? |
| Curtiss-Wright | 4 | 2 | ? |
| Aero Gear | 4 | 2 | ? |
| Small Shop A | 5 | 1 | ? |
| Small Shop B | 5 | 1 | ? |

**Total should be:** 25 calls ±2 (some companies may have fewer jobs than expected)

---

## What This Test Validates

✅ **All 5 tiers tested:**
- At least 1 sample from each tier
- Tier 2-5 have 2 samples for validation

✅ **Adaptive caps working:**
- Pratt & Whitney: Up to 50 jobs
- Barnes Aerospace: Up to 40 jobs
- Small shops: Limited to 10 jobs

✅ **API efficiency proven:**
- 25 calls for 9 companies = 2.78 calls per company average
- Mega-corps get 5x more coverage than small shops

✅ **New keywords tested:**
- Pratt & Whitney should have engineers, supervisors
- Barnes should have some leadership roles
- All should have licensed trades if available

---

## Success Criteria (9 Companies, 25 Calls)

- [ ] **All 9 companies processed** without errors
- [ ] **Total API calls:** 23-27 (25 ±2)
- [ ] **Tier assignment correct:** Check console output
- [ ] **Job caps enforced:** No company exceeds their tier's cap
- [ ] **New keywords captured:** At least 2-3 types
- [ ] **Processing time:** < 5 minutes
- [ ] **No circuit breaker triggers**

---

## What You'll Learn from This Test

### From Pratt & Whitney (Tier 1):
- Does 50-job cap work correctly?
- Are engineers and supervisors captured?
- Do we see licensed electricians, plumbers?
- Is job diversity high (10+ unique role types)?

### From Barnes & Sikorsky (Tier 2):
- Does 40-job cap work correctly?
- Consistent tier assignment for different company sizes in tier?
- Mid-range companies have diverse roles?

### From GKN & Chromalloy (Tier 3):
- Does 25-job cap work correctly?
- Medium suppliers have reasonable diversity?

### From Curtiss-Wright & Aero Gear (Tier 4):
- Does 15-job cap work correctly?
- Small-medium companies more focused hiring?

### From Small Shops (Tier 5):
- Does 10-job cap work (or are jobs < 10)?
- Small shops very focused (1-3 role types)?

---

## Quick Start Commands

```bash
# 1. Create Excel file with 9 companies listed above

# 2. Create config file (JSON above)

# 3. Run test
python AeroComps.py

# 4. Monitor console output
# - Should see: "[Company] Tier X, Job cap: YY"
# - Total API calls at end

# 5. Check Excel output
# - Jobs from all 9 companies
# - New keywords appearing
# - No non-trades roles
```

---

## After Testing - Next Steps

**If successful (25 calls validates everything):**
- Deploy to full 137 companies
- Expected: ~225 API calls for production
- Commit and celebrate!

**If issues found:**
- Report specific problems
- Adjust code
- Re-test with same 9 companies (only 25 more calls)

**If you want more validation:**
- Run another 9 companies (another 25 calls)
- Gives 18 companies total for 50 API calls
- Double-checks consistency

---

## Risk Mitigation

**Risk:** Only 1 Tier 1 sample
**Mitigation:** Pratt & Whitney is the best test case (largest, most diverse)

**Risk:** Only 2 samples for Tier 2-5
**Mitigation:** Enough to validate tier assignment and cap logic

**Risk:** Not enough data for statistical confidence
**Mitigation:** This is a functional test, not statistical validation

**If you need more confidence:**
- Run test again with different 9 companies
- Or expand to 15 companies (35-40 calls)

---

## Cost Analysis

**Test cost:** 25 API calls
**At $50/mo for 5,000 calls:** $0.25 (25 cents)
**Time investment:** 2-3 minutes processing + 10 minutes review
**Value:** Validates entire 5-tier system before committing 225 calls

**ROI:** Excellent - catch any issues before burning 200+ calls

---

## Comparison: Testing Approaches

| Approach | Companies | API Calls | Time | Coverage |
|----------|-----------|-----------|------|----------|
| **Minimal (5)** | 5 | 15 | 1-2 min | Basic only |
| **Conservative (7)** | 7 | 20 | 2-3 min | Good |
| **Strategic (9)** ✅ | 9 | 25 | 2-3 min | Excellent |
| **Original (25)** | 25 | 75 | 5-8 min | Overkill |

**Recommendation:** 9 companies, 25 calls (strategic approach)

---

## Alternative: Test Tiers Separately

If you want to be even more cautious:

**Day 1:** Test Tier 1-3 only (5 companies, 17 calls)
**Day 2:** Test Tier 4-5 only (4 companies, 6 calls)
**Day 3:** Test 1 more from each tier (5 companies, varies)

**Benefit:** Spread risk across multiple sessions
**Drawback:** Takes longer to complete validation

---

**Ready to test with just 25 API calls?** This is the most efficient validation possible while still testing all 5 tiers!
