# Test Setup Guide - 9 Companies, Max 25 API Calls

**Quick Start:** Run the ultra-strategic test with 9 companies for exactly 25 API calls

**Files created for you:**
- ✅ `data/Test_Max25_9Companies.csv` - Company list (CSV format)
- ✅ `data/convert_test_csv_to_excel.py` - Converter script
- ✅ `resources/config_test_max25.json` - Test configuration

---

## 📋 Pre-Flight Checklist

Before running the test, ensure you have:

- [ ] Python 3.x installed
- [ ] Dependencies installed: `pandas`, `openpyxl`, `requests`, `tqdm`
- [ ] SerpAPI key ready
- [ ] Latest code pulled from GitHub

---

## 🚀 Step-by-Step Test Instructions

### Step 1: Pull Latest Code

```bash
git pull origin claude/session-011CUYQMZ4cuy3Hpxmqv7Hv8
```

**Verify files exist:**
```bash
ls data/Test_Max25_9Companies.csv
ls data/convert_test_csv_to_excel.py
ls resources/config_test_max25.json
```

---

### Step 2: Convert CSV to Excel

**Run the converter script:**

```bash
python data/convert_test_csv_to_excel.py
```

**Expected output:**
```
🔄 Converting CSV to Excel format...
   Input:  data/Test_Max25_9Companies.csv
   Output: data/Test_Max25_9Companies.xlsx

📋 Companies loaded: 9
   1. Pratt & Whitney
   2. Sikorsky Aircraft
   3. Barnes Aerospace
   4. GKN Aerospace
   5. Chromalloy
   6. Curtiss-Wright
   7. Aero Gear
   8. Connecticut Spring
   9. Standard Aero

✅ Successfully created data/Test_Max25_9Companies.xlsx
```

**If you get an error about missing modules:**
```bash
pip install pandas openpyxl
# Then re-run the converter
```

---

### Step 3: Configure API Key

**Edit the config file:**

```bash
# Open the config file
notepad resources/config_test_max25.json   # Windows
# or
nano resources/config_test_max25.json      # Linux/Mac
```

**Replace YOUR_API_KEY_HERE with your actual SerpAPI key:**

```json
{
  "api_keys": [
    {
      "label": "Test-Max25",
      "key": "801d79de5fa4d16e67d77c3b0cf1d2090a394d0f52df23aebd5deecf9d653cc4",
      "limit": 50,
      "priority": 1
    }
  ],
  ...
}
```

**Save and close the file.**

---

### Step 4: Run the Test

**From the project root directory:**

```bash
python AeroComps.py
```

**The script will automatically:**
1. Load `config_test_max25.json` (or your default config)
2. Read the 9 companies from the Excel file
3. Process each company with adaptive caps
4. Save results to `output/Test_Max25_Results.xlsx`

---

### Step 5: Monitor Console Output

**Watch for tier assignments:**

```
[Pratt & Whitney] Tier 1, Job cap: 50
[Pratt & Whitney] → 45 skilled-trade jobs found

[Sikorsky Aircraft] Tier 2, Job cap: 40
[Sikorsky Aircraft] → 32 skilled-trade jobs found

[Barnes Aerospace] Tier 2, Job cap: 40
[Barnes Aerospace] → 28 skilled-trade jobs found

[GKN Aerospace] Tier 3, Job cap: 25
[GKN Aerospace] → 18 skilled-trade jobs found

... etc ...
```

**Expected processing time:** 2-3 minutes

---

## ✅ Validation Checklist

After the test completes, verify:

### Console Output Validation

- [ ] **All 9 companies processed** without errors
- [ ] **Tier assignments correct:**
  - Pratt & Whitney → Tier 1 (50 cap)
  - Sikorsky, Barnes → Tier 2 (40 cap)
  - GKN, Chromalloy → Tier 3 (25 cap)
  - Curtiss-Wright, Aero Gear → Tier 4 (15 cap)
  - Connecticut Spring, Standard Aero → Tier 5 (10 cap)

- [ ] **API call count:** 23-27 calls (25 ±2 is acceptable)
- [ ] **No circuit breaker triggers**
- [ ] **Processing time:** Under 5 minutes

### Excel Output Validation

**Open:** `output/Test_Max25_Results.xlsx`

- [ ] **Multiple companies represented** (should have jobs from 7-9 companies)
- [ ] **Job titles include new keywords:**
  - Look for: "Manufacturing Engineer", "Quality Engineer"
  - Look for: "Production Supervisor", "Shop Foreman"
  - Look for: "Journeyman Electrician", "Master Plumber"

- [ ] **No false positives:**
  - Should NOT see: "Software Engineer", "HR Manager", "Sales"
  - All jobs should be skilled trades related

- [ ] **Job diversity varies by tier:**
  - Pratt & Whitney: Should have 10+ different role types
  - Small shops: Should have 1-3 role types

### Tier Assignment Validation

**Check a few companies manually:**

**Pratt & Whitney (should be Tier 1):**
```bash
# In Python console or script:
from AeroComps import get_company_tier, get_job_cap_for_company

print(get_company_tier("Pratt & Whitney"))  # Should print: 1
print(get_job_cap_for_company("Pratt & Whitney"))  # Should print: 50
```

**Barnes Aerospace (should be Tier 2):**
```python
print(get_company_tier("Barnes Aerospace"))  # Should print: 2
print(get_job_cap_for_company("Barnes Aerospace"))  # Should print: 40
```

---

## 📊 Expected Results Summary

| Metric | Expected Value |
|--------|----------------|
| **Companies processed** | 9 |
| **Total API calls** | 25 (±2) |
| **Processing time** | 2-3 minutes |
| **Total jobs found** | 100-230 |
| **Companies with jobs** | 7-9 (some may have 0 jobs) |
| **Unique role types** | 15-30 |

---

## 🎯 Test Results Interpretation

### ✅ Test PASSED if:

1. All 9 companies processed without errors
2. API calls within 23-27 range
3. Tier assignments correct for all companies
4. New keywords appear (engineers, supervisors, licensed trades)
5. No non-trades roles in results
6. Processing completes in < 5 minutes

**Next step:** Deploy to full 137 companies!

### ⚠️ Test NEEDS REVIEW if:

1. API calls significantly different (< 20 or > 30)
2. Some companies show wrong tier
3. Missing expected keywords (no engineers from Pratt & Whitney)
4. Many false positives (non-trades roles appearing)

**Next step:** Report findings, adjust code, re-test

### ❌ Test FAILED if:

1. Errors or crashes during processing
2. Circuit breaker triggers
3. All companies show 0 jobs (likely API issue)
4. Tier system not working at all

**Next step:** Debug issue, check API key, check network

---

## 📁 File Locations

**Input files:**
- `data/Test_Max25_9Companies.xlsx` - Company list
- `resources/config_test_max25.json` - Configuration

**Output files:**
- `output/Test_Max25_Results.xlsx` - Job results
- `log/api_audit.jsonl` - API call audit log

**Documentation:**
- `TEST_SETUP_GUIDE.md` - This file
- `future/TEST_MAX_25_CALLS.md` - Detailed test analysis
- `future/IMPLEMENTATION_SUMMARY.md` - Complete implementation guide

---

## 🔧 Troubleshooting

### Issue: "File not found: Test_Max25_9Companies.xlsx"

**Solution:**
```bash
# Convert CSV to Excel
python data/convert_test_csv_to_excel.py
```

### Issue: "ModuleNotFoundError: No module named 'pandas'"

**Solution:**
```bash
pip install pandas openpyxl requests tqdm
```

### Issue: "API key not found"

**Solution:**
- Edit `resources/config_test_max25.json`
- Replace `YOUR_API_KEY_HERE` with your actual SerpAPI key

### Issue: Company showing wrong tier

**Example:** Barnes Aerospace showing Tier 5 instead of Tier 2

**Solution:**
- Check company name spelling in Excel file
- Fuzzy matching should handle variations, but exact names work best
- Check console output for: "[Barnes Aerospace] Tier X, Job cap: YY"

### Issue: All companies have 0 jobs

**Possible causes:**
1. API key invalid or out of credits
2. Network issue blocking API calls
3. Rate limiting triggered

**Solution:**
- Check API key is valid
- Check `log/api_audit.jsonl` for error messages
- Try running `diagnostics/quick_check.py` first

---

## 🔍 Quick Diagnostic Commands

**Check if test files exist:**
```bash
ls -la data/Test_Max25_9Companies.*
ls -la resources/config_test_max25.json
```

**Verify Python dependencies:**
```bash
python -c "import pandas, openpyxl, requests, tqdm; print('✅ All dependencies installed')"
```

**Test company tier lookup:**
```bash
python -c "
from AeroComps import get_company_tier, get_job_cap_for_company
print('Pratt & Whitney:', get_company_tier('Pratt & Whitney'), 'cap:', get_job_cap_for_company('Pratt & Whitney'))
print('Barnes Aerospace:', get_company_tier('Barnes Aerospace'), 'cap:', get_job_cap_for_company('Barnes Aerospace'))
"
```

---

## 📈 After Successful Test

**If test passes all validation:**

1. **Review results** in `output/Test_Max25_Results.xlsx`
2. **Check new keywords** are appearing
3. **Verify tier system** is working correctly
4. **Deploy to production:**
   - Update config to use full company list
   - Set `testing_mode: false`
   - Run full 137 companies (~225 API calls)

---

## 🎓 What You're Testing

This 9-company test validates:

✅ **All 5 tier levels** (1 sample Tier 1, 2 samples each for Tier 2-5)
✅ **Adaptive job caps** (10, 15, 25, 40, 50 based on company size)
✅ **Expanded keywords** (185 keywords including engineers, supervisors, licensed trades)
✅ **API efficiency** (25 calls for comprehensive validation)
✅ **No false positives** (only skilled trades roles captured)

**Cost:** $0.25 (25 API calls at standard pricing)
**Time:** 2-3 minutes processing + 5-10 minutes review
**Risk:** Minimal - only 25 calls to validate entire system

---

## 📞 Support

If you encounter issues:

1. Check troubleshooting section above
2. Review `future/TEST_MAX_25_CALLS.md` for detailed analysis
3. Check `log/api_audit.jsonl` for API error details
4. Run `diagnostics/setup_check.py` for system validation

---

**Ready to test?** Follow the steps above and report your findings! 🚀
