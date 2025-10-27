# Quick Start Guide - AeroSpace Alley Job Scanner

## 🚀 Get Running in 5 Minutes

This guide will get you from zero to running your first test.

---

## Prerequisites

- **Python 3.7+** installed on your system
- **SerpAPI account** with API key ([sign up free](https://serpapi.com/users/sign_up))
- **Internet connection** (not blocked by SerpAPI)

---

## Step 1: Get the Code

**If using Git:**
```bash
git clone <repository-url>
cd AeroSpace-Alley-Comps
```

**If downloading ZIP:**
```bash
unzip AeroSpace-Alley-Comps.zip
cd AeroSpace-Alley-Comps
```

---

## Step 2: Install Dependencies

```bash
pip install -r resources/requirements.txt
```

**What this installs:**
- `pandas` - Data processing
- `openpyxl` - Excel file handling
- `requests` - API calls
- `tqdm` - Progress bars

**Expected time:** 1-2 minutes

---

## Step 3: Configure Your API Key

**Edit:** `resources/config.json`

**Find this section:**
```json
"api_keys": [
  {
    "label": "Your-Key",
    "key": "PASTE_YOUR_SERPAPI_KEY_HERE",
    "limit": 250,
    "priority": 1,
    "notes": "Your SerpAPI key"
  }
]
```

**Replace** `PASTE_YOUR_SERPAPI_KEY_HERE` with your actual SerpAPI key.

**Where to find your key:** [SerpAPI Dashboard](https://serpapi.com/manage-api-key)

---

## Step 4: Verify Setup

```bash
python setup_check.py
```

**Expected output:**
```
✅ Python Version
✅ Dependencies Installed
✅ Directory Structure
✅ Configuration File
✅ Input Data Files
✅ Protection System
✅ API Connection

✅ ALL CHECKS PASSED - Ready to run!
```

**If you see ❌ errors:** Follow the fix instructions shown.

---

## Step 5: Check API Block Status

```bash
python quick_check.py
```

**Expected outputs:**

**✅ If API is accessible:**
```
✅ SUCCESS! Block has been lifted!
   Status: 200 OK
   API is accessible
```
→ **Proceed to Step 6**

**❌ If IP is blocked:**
```
❌ Still blocked (403 - Access Denied)
   Status: IP block still active
   Suggestion: Try again in a few hours
```
→ **Wait and retry, OR switch networks** (see NETWORK_SWITCHING_ANALYSIS.md)

---

## Step 6: Run Your First Test (1 Company)

**The config is already set for testing!** Check `resources/config.json`:

```json
"settings": {
  "testing_mode": true,
  "testing_company_limit": 3,
  "input_file": "data/Test_3_Companies.xlsx"
}
```

**But let's start with just 1 company for safety:**

**Edit `resources/config.json` - change:**
```json
"testing_company_limit": 1
```

**Run the test:**
```bash
python AeroComps.py
```

**Expected output:**
```
========================================
AEROSPACE ALLEY JOB SCANNER - Configuration Loading
========================================
✅ Configuration loaded successfully
   API Keys found: 1

Initializing rate limit protection system...
✅ Protection system initialized:
   • Token Bucket Rate Limiter (60 calls/hour)
   • Circuit Breaker (3 failure threshold)
   • Batch Processor (10 companies/batch)
   • Audit Logger (log/api_audit.jsonl)
   • Health Monitor (real-time alerts)

🧪 TESTING MODE: Will process only 1 companies

Starting batch processing: 1 companies

API call #1 (Your-Key) → Pratt & Whitney
API call #2 (Your-Key) → Pratt & Whitney
API call #3 (Your-Key) → Pratt & Whitney

[Pratt & Whitney] → 8 skilled-trade jobs found

✅ Completed! 8 skilled-trade jobs saved to output/Aerospace_Alley_SkilledTrades_Jobs.xlsx
```

**Expected time:** ~15 seconds
**Expected API calls:** 3
**Expected result:** Excel file with jobs found

---

## Step 7: Check Your Results

**Open:** `output/Aerospace_Alley_SkilledTrades_Jobs.xlsx`

**You should see columns:**
- Company
- Job Title
- Location
- Via (job board)
- Source URL
- Description Snippet
- Timestamp

**Example jobs found:**
- CNC Machinist
- Welder
- Assembly Technician
- Inspector
- Maintenance Technician

---

## Step 8: Run Test 2 (3 Companies)

**If Test 1 succeeded**, increase to 3 companies:

**Edit `resources/config.json` - change:**
```json
"testing_company_limit": 3
```

**Run:**
```bash
python AeroComps.py
```

**Expected:**
- 9 API calls (3 per company)
- ~30-40 seconds runtime
- Jobs from 3 companies

---

## Step 9: Run Full Production (137 Companies)

**When ready for the full run:**

**Edit `resources/config.json` - change:**
```json
"settings": {
  "testing_mode": false,
  "input_file": "data/Aerospace_Alley_Companies.xlsx"
}
```

**Run:**
```bash
python AeroComps.py
```

**Expected:**
- ~411 API calls (3 per company)
- 40-50 minutes runtime
- 14 batch pauses (2-5 minutes each)
- Checkpoint saves every 25 companies
- Final Excel with all results

---

## Troubleshooting

### Problem: "Module not found"
**Solution:**
```bash
pip install -r resources/requirements.txt
```

### Problem: "config.json not found"
**Solution:**
```bash
# Check you're in the project directory
pwd
# Should show: .../AeroSpace-Alley-Comps

# Verify file exists
ls resources/config.json
```

### Problem: "403 - Access Denied"
**Solution:**
- IP is blocked (see Step 5)
- Wait 24-48 hours OR switch networks
- See: NETWORK_SWITCHING_ANALYSIS.md

### Problem: "Invalid API key"
**Solution:**
- Verify API key in resources/config.json
- Check: [SerpAPI Dashboard](https://serpapi.com/manage-api-key)
- Make sure key has no spaces or quotes

### Problem: "No input file found"
**Solution:**
```bash
# Check data directory
ls data/

# Should contain:
# - Test_3_Companies.xlsx
# - Aerospace_Alley_Companies.xlsx
```

### Problem: Circuit breaker triggered
**Example:**
```
⛔ CIRCUIT BREAKER OPEN - Stopping all API calls
```

**What it means:** 3+ consecutive failures detected

**Solution:**
1. Check `log/api_audit.jsonl` for error details
2. Verify API key is valid
3. Check internet connection
4. Wait a few minutes, try again

---

## What the Protection System Does

**Automatic safeguards** to prevent IP blocking:

| Protection | What It Does | Why It Matters |
|------------|-------------|----------------|
| **Rate Limiter** | Max 60 calls/hour | Prevents burst requests |
| **Circuit Breaker** | Stops after 3 failures | Prevents IP block escalation |
| **Batch Processing** | Pauses every 10 companies | Mimics human behavior |
| **Audit Logger** | Records all API calls | Compliance trail |
| **Health Monitor** | Real-time alerts | Early warning system |

**You don't need to do anything** - these run automatically!

---

## File Structure

```
AeroSpace-Alley-Comps/
├── AeroComps.py              ← Main script (run this)
├── setup_check.py            ← Setup verification
├── quick_check.py            ← API block checker
├── README.md                 ← Full documentation
├── QUICKSTART.md             ← This guide
│
├── resources/
│   ├── config.json           ← YOUR API KEY GOES HERE
│   ├── requirements.txt      ← Dependencies
│   └── rate_limit_protection.py  ← Protection system
│
├── data/
│   ├── Test_3_Companies.xlsx         ← Test data (3 companies)
│   └── Aerospace_Alley_Companies.xlsx ← Full data (137 companies)
│
├── output/
│   └── Aerospace_Alley_SkilledTrades_Jobs.xlsx  ← YOUR RESULTS
│
└── log/
    └── api_audit.jsonl       ← API call log
```

---

## Progressive Testing Summary

| Test | Companies | API Calls | Time | Purpose |
|------|-----------|-----------|------|---------|
| **Test 1** | 1 | 3 | ~15 sec | Verify setup works |
| **Test 2** | 3 | 9 | ~40 sec | Validate protection |
| **Full Run** | 137 | ~411 | 40-50 min | Production data |

**Always start with Test 1!** It validates everything works before committing to the full run.

---

## Configuration Cheat Sheet

**For testing (1 company):**
```json
"testing_mode": true,
"testing_company_limit": 1,
"input_file": "data/Test_3_Companies.xlsx"
```

**For testing (3 companies):**
```json
"testing_mode": true,
"testing_company_limit": 3,
"input_file": "data/Test_3_Companies.xlsx"
```

**For production (all 137 companies):**
```json
"testing_mode": false,
"input_file": "data/Aerospace_Alley_Companies.xlsx"
```

---

## Next Steps After Success

1. **Review output:** Check Excel file for data quality
2. **Share with stakeholders:** Business development, sales, marketing
3. **Schedule regular runs:** Weekly or monthly updates
4. **Monitor audit logs:** Check `log/api_audit.jsonl` for patterns

---

## Getting Help

**Documentation:**
- `README.md` - Full technical documentation
- `PROTECTION_SYSTEM_VALIDATION.md` - How protection works
- `NETWORK_SWITCHING_ANALYSIS.md` - IP block solutions

**Common Issues:**
- IP blocked → Run `python quick_check.py` to check status
- Missing dependencies → Run `pip install -r resources/requirements.txt`
- Configuration errors → Run `python setup_check.py`

**Support:**
- SerpAPI Support: support@serpapi.com
- Rate limit docs: https://serpapi.com/api-status-and-error-codes

---

## Success Checklist

- [✓] Installed dependencies
- [✓] Added API key to config.json
- [✓] Ran setup_check.py (all green)
- [✓] Verified API accessible (quick_check.py)
- [✓] Test 1 completed successfully
- [✓] Test 2 completed successfully
- [✓] Ready for full production run!

---

**Created:** 2025-10-27
**Version:** 1.0
**Estimated setup time:** 5-10 minutes
**Estimated first test:** 15 seconds
