# Aerospace Alley Job Scanner

**Market Intelligence Tool for Connecticut Aerospace Manufacturing**

Automated competitive intelligence system that tracks hiring activity across 137 Connecticut aerospace companies to identify market trends, growth indicators, and business opportunities.

---

## 📊 For Business Users

### What This Tool Does

Monitors real-time job postings from Connecticut's aerospace sector to provide:

**Market Intelligence:**
- Hiring activity across 137 aerospace manufacturers
- Skilled trades demand trends (machinists, welders, assemblers, inspectors)
- Company expansion indicators
- Regional workforce patterns

**Competitive Intelligence:**
- Which companies are actively hiring (growth signals)
- Types of roles being filled (capability investments)
- Hiring velocity comparisons (aggressive vs. maintenance)
- Tier-1 supplier vs. small manufacturer activity

**Sales & Business Development:**
- **Lead Qualification:** Companies hiring = active programs + budget
- **Sales Timing:** Hiring spikes indicate new contracts, ideal approach windows
- **Partnership Opportunities:** Identify companies scaling up
- **Customer Health:** Track hiring at existing customers

### Current Capabilities

- **Coverage:** 137 Connecticut aerospace companies
- **Job Categories:** 100+ skilled trades automatically classified
- **Tier-Based Processing:** 6 company tiers with adaptive job caps (10-80 jobs per company)
- **Profile System:** Quick test, tier test, and production profiles with command-line override
- **Persistent API Tracking:** Cross-session usage tracking with automatic key rotation
- **Smart Fallback:** Automatic retry for companies with hyphenated names
- **Frequency:** Daily/weekly automated scans (configurable)
- **Output:** Excel files with tier analysis and comprehensive analytics

### Example Insights

**For Sales:** "Barnes Aerospace posted 12 CNC machinist roles this week - they're expanding production capacity. Good time to pitch precision tooling."

**For Marketing:** "15 companies hiring welders in Q1 - target welding safety/automation content to this segment."

**For Executive:** "Tier-1 suppliers showing 40% increase in hiring vs. Q4 - regional aerospace market strengthening."

---

## 🚀 Quick Start (5 Minutes)

### Prerequisites

- Python 3.7+ installed
- SerpAPI account with API key ([sign up free](https://serpapi.com/users/sign_up) - 250 free searches/month)
- Internet connection

### Step 1: Install Dependencies

```bash
pip install -r resources/requirements.txt
```

### Step 2: Configure API Key

Edit `resources/config.json`:

```json
{
  "api_keys": [
    {
      "label": "primary-SerpAPI",
      "key": "YOUR_SERPAPI_KEY_HERE",
      "monthly_limit": 250,
      "billing_cycle_day": 1,
      "priority": 1
    }
  ],

  "active_profile": "quick_test",

  "profiles": {
    "quick_test": {
      "description": "Quick 3-company test (~5-10 API calls)",
      "testing_mode": true,
      "testing_company_limit": 3
    },
    "tier_test": {
      "description": "15 companies diverse tier test (~30-40 API calls)",
      "testing_mode": true,
      "testing_company_limit": 15
    },
    "production": {
      "description": "Full 137-company run (~260-280 API calls)",
      "testing_mode": false,
      "testing_company_limit": null
    }
  },

  "settings": {
    "input_file": "data/Aerospace_Alley_Companies.xlsx",
    "api_limits": {
      "max_api_calls_per_key": 250,
      "min_interval_seconds": 3.2
    },
    "company_limits": {
      "tier1_job_cap": 80,
      "tier2_job_cap": 40,
      "tier3_job_cap": 30,
      "tier4_job_cap": 20,
      "tier5_job_cap": 10,
      "tier99_job_cap": 20
    }
  }
}
```

### Step 3: Verify Setup

```bash
python diagnostics/setup_check.py
```

Expected: All green ✅ checkmarks

### Step 4: Run Quick Test (3 Companies)

```bash
python AeroComps.py
```

**What happens:**
- Processes 3 companies (uses active_profile: "quick_test" from config.json)
- Takes ~30-60 seconds
- Finds 15-30 jobs total
- Uses ~5-10 API calls
- Saves to `output/Test_3Companies_YYYYMMDD_HHMM.xlsx` (timestamped)

### Step 5: Scale Up

**Using Profiles (Recommended):**
```bash
# Quick 3-company test (~5-10 API calls)
python AeroComps.py --profile quick_test

# Diverse tier test with 15 companies (~30-40 API calls)
python AeroComps.py --profile tier_test

# Full 137-company production run (~260-280 API calls)
python AeroComps.py --profile production
```

**Or edit config.json:**
- Change `"active_profile"` to `"quick_test"`, `"tier_test"`, or `"production"`

---

## ⚠️ API Key Requirements

**IMPORTANT:** For full 137-company production runs, you need sufficient API quota:

**Option A: Multiple Free Keys** ✅ Recommended for testing
- 2 free SerpAPI keys (250 searches/month each = 500 total)
- System auto-rotates with 60-second warning before switching
- Perfect for weekly/monthly scans

**Option B: Single Paid Key** ✅ Recommended for frequent use
- 1 paid SerpAPI key ($50/month for 5,000 searches)
- No rotation needed
- Ideal for daily scans or multiple projects

**Expected API Usage:**
- 137 companies × ~2 calls/company (with fallback) = **~260-280 API calls**
- Quick test (3 companies): ~5-10 calls
- Tier test (15 companies): ~30-40 calls
- Production (137 companies): ~260-280 calls

**Setup Multiple Keys:**
```json
{
  "api_keys": [
    {
      "label": "primary-SerpAPI",
      "key": "YOUR_FIRST_KEY",
      "monthly_limit": 250,
      "billing_cycle_day": 1,
      "priority": 1
    },
    {
      "label": "2nd API-Backup",
      "key": "YOUR_SECOND_KEY",
      "monthly_limit": 250,
      "billing_cycle_day": 1,
      "priority": 2
    }
  ]
}
```

**Check API Usage:**
```bash
python resources/api_usage_tracker.py --report
```

---

## 💻 For Technical Users

### System Architecture

**Pipeline Flow:**
```
Company List → Query Builder → SerpAPI →
Response Validator → Company Matcher →
Skilled Trades Filter → Excel Export → Analytics
```

**Key Components:**
- **Rate Limit Protection:** 7-layer system (60 calls/hour max)
- **6-Tier Job Cap System:** Adaptive limits (Tier 1: 80 jobs → Tier 5: 10 jobs, Tier 99: 20 jobs for unknown)
- **Persistent API Tracking:** Cross-session usage tracking with auto-rotation and 60-second warnings
- **Profile System:** Command-line profile override (quick_test, tier_test, production)
- **Smart Fallback System:** Automatic retry with hyphen removal for failed queries
- **Circuit Breaker:** Stops after 3 consecutive failures
- **Batch Processing:** 10 companies per batch with 45 second pauses
- **Health Monitoring:** Real-time success rate tracking with tier analytics
- **Audit Logging:** Complete API call history

### Current System Features

**Feature #1: 6-Tier Adaptive Job Cap System**
- **Implementation:** 6-tier company classification by employee count
- **Tier 1 (10,000+ employees):** 80 job cap (e.g., Pratt & Whitney, Collins Aerospace)
- **Tier 2 (1,000-9,999):** 40 job cap (e.g., GKN Aerospace, Barnes Aerospace)
- **Tier 3 (200-999):** 30 job cap
- **Tier 4 (50-199):** 20 job cap
- **Tier 5 (10-49):** 10 job cap
- **Tier 99 (Unknown size):** 20 job cap (conservative default for companies not in database)
- **Impact:** Optimized API usage (~260-280 calls for 137 companies), captures proportional jobs based on company size

**Feature #2: Smart Fallback for Hyphenated Companies**
- **Problem:** Companies like "Accu-Rite" may be indexed as "AccuRite" by Google
- **Solution:** Automatic 2-strategy retry system
  1. Try with hyphens preserved (default)
  2. If no results, retry without hyphens
- **Impact:** Improved success rate, handles edge cases automatically

**Feature #3: Comprehensive Analytics with Tier Tracking**
- **New Metrics:** Company tier, employee count, job cap per company
- **New Reports:** Tier analysis, tier success rates, failed company tracking
- **Analytics Sheets:**
  - Tier Analysis (companies/jobs by tier)
  - Tier Success Metrics (success rates by company size)
  - Failed Companies (0 jobs found with details)
- **Impact:** Better visibility into hiring patterns by company size

**Feature #4: Persistent API Usage Tracking**
- **Problem:** Previous system reset usage counter on each run, risking quota exhaustion
- **Solution:** Persistent state file survives script restarts and tracks cumulative usage
- **Key Features:**
  - Multi-key support with automatic rotation based on priority
  - Per-key billing cycle tracking (auto-resets on billing day)
  - Usage warnings at 75%, 90%, 100% thresholds
  - 60-second warning before key switch with Ctrl+C safe exit
  - Daily usage history logging
  - Command-line usage reporting: `python resources/api_usage_tracker.py --report`
- **Impact:** Zero risk of quota exhaustion, safe multi-key rotation, full usage visibility

**Feature #5: Profile System with Command-Line Override**
- **Problem:** Multiple config files for different test scenarios was confusing
- **Solution:** Single config with named profiles (quick_test, tier_test, production)
- **Usage:**
  - Default: Uses `active_profile` from config.json
  - Override: `python AeroComps.py --profile quick_test`
  - Profiles include: testing mode, company limit, descriptions
- **Dynamic Output Naming:**
  - Testing: `Test_15Companies_20251029_1430.xlsx` (timestamped, won't overwrite)
  - Production: `Aerospace_Alley_SkilledTrades_Jobs.xlsx` (standard name)
- **Impact:** Simpler configuration, clear testing vs production separation, safer workflow

### Configuration

**Safe Settings (Tested & Working):**
```json
"settings": {
  "min_interval_seconds": 3.2,   // Enforced minimum (safety override)
  "max_threads": 5,               // Safe for paid accounts
  "testing_mode": true,           // Start with test mode
  "testing_company_limit": 15     // Test with 15 companies first
}
```

**Rate Limits:**
- Free tier: 250 searches/month per key
- Paid tier: 5,000 searches/month ($50)
- Current usage: ~2 searches per company (with fallback retry)
- 137 companies = ~260-280 API calls total
- **Recommended for production:** 2 free API keys (250 each = 500 total) OR 1 paid key

### Protection System Details

**Layer 1: Token Bucket Rate Limiter**
- Capacity: 60 calls/hour
- Refill rate: 1 call every 60 seconds
- Prevents burst requests

**Layer 2: Circuit Breaker**
- Threshold: 3 consecutive failures
- Opens circuit → stops all requests
- Timeout: 300 seconds before retry

**Layer 3: Exponential Backoff**
- Retry delays: 2s, 4s, 8s
- Max attempts: 3
- Prevents hammering failed endpoints

**Layer 4: Batch Processing**
- Batch size: 10 companies
- Pause between batches: 45 seconds (fixed)
- Prevents API rate limiting while maintaining efficiency

**Layer 5: Audit Logging**
- File: `log/api_audit.jsonl`
- Records: All API calls, status codes, response times
- Used for: Compliance, debugging, rate analysis

**Layer 6: Health Monitoring**
- Tracks: Success rate, failures, rate limits
- Alerts: Low success rate, repeated failures
- Triggers: Fallback strategies

**Layer 7: Configuration Validation**
- Validates settings before run
- Enforces minimum intervals
- Warns on aggressive configurations

### Technical Diagnostics

**Check API Access:**
```bash
python diagnostics/quick_check.py
```

**View Audit Log:**
```bash
cat log/api_audit.jsonl
```

**Check API Health Summary:**
Run `python AeroComps.py` - summary displayed at end

---

## 📁 Project Structure

```
AeroSpace-Alley-Comps/
├── AeroComps.py                 # Main pipeline (DO NOT MODIFY)
├── README.md                    # This file
├── .gitignore                   # Git exclusions
├── CHANGELOG.md                 # Version history
├── PROJECT_STRUCTURE.md         # Architecture documentation
│
├── resources/
│   ├── config.json              # Master configuration (API keys, profiles, settings)
│   ├── requirements.txt         # Python dependencies
│   ├── rate_limit_protection.py # 7-layer protection system
│   ├── api_usage_tracker.py     # Persistent API usage tracking (NEW)
│   └── analytics.py             # Analytics generation
│
├── data/
│   └── Aerospace_Alley_Companies.xlsx    # Full list (137 companies)
│
├── output/                      # Results folder (auto-created)
│   ├── Aerospace_Alley_SkilledTrades_Jobs.xlsx  # Production output
│   ├── Test_*_*.xlsx            # Test run outputs (timestamped)
│   └── *_Analytics.xlsx         # Analytics reports
│
├── log/                         # Logs (auto-created, gitignored)
│   ├── api_audit.jsonl          # Complete API call history
│   └── api_usage_state.json     # Persistent usage tracking (NEW)
│
├── diagnostics/                 # Diagnostic & test tools
│   ├── setup_check.py           # Verify installation
│   ├── quick_check.py           # Test API access
│   ├── check_block_status.py    # Comprehensive diagnostics
│   └── test_matching_logic.py   # Job matching validation
│
├── future/                      # Future development planning
│   └── DYNAMIC_COMPANY_SIZING_STRATEGY.md  # Scaling strategy (500+ companies)
│
└── docs/
    └── archive/                 # Archived documentation
        ├── testing/             # Historical test documentation
        └── planning/            # Historical planning documents
```

---

## 🔧 Local Setup Guide

### Windows Setup

**1. Install Python**
- Download from [python.org](https://python.org/downloads/)
- ⚠️ **IMPORTANT:** Check "Add Python to PATH" during installation

**2. Install Dependencies**
Open Command Prompt:
```bash
cd path\to\AeroSpace-Alley-Comps
pip install -r resources\requirements.txt
```

**3. Configure & Run**
```bash
notepad resources\config.json
# Add your API key, save
python AeroComps.py
```

### macOS/Linux Setup

**1. Install Python**
```bash
# macOS
brew install python3

# Linux (Ubuntu/Debian)
sudo apt install python3 python3-pip
```

**2. Install Dependencies**
```bash
cd ~/AeroSpace-Alley-Comps
pip3 install -r resources/requirements.txt
```

**3. Configure & Run**
```bash
nano resources/config.json
# Add your API key, save
python3 AeroComps.py
```

### Using Anaconda (Recommended)

**Why Anaconda:** Better environment management, no system conflicts

**Setup:**
```bash
# Create environment
conda create -n aerospace python=3.12

# Activate
conda activate aerospace

# Install
pip install -r resources/requirements.txt

# Run
python AeroComps.py
```

### Using VSCode

**Quick Setup:**
1. Install VSCode: [code.visualstudio.com](https://code.visualstudio.com)
2. Open folder: **File → Open Folder** → Select `AeroSpace-Alley-Comps`
3. Install Python extension (VSCode will prompt)
4. Open terminal: **Terminal → New Terminal**
5. Run: `pip install -r resources/requirements.txt`
6. Run: `python AeroComps.py`

**For Complete Beginners:**
- See VSCODE_BEGINNER_GUIDE.md for step-by-step walkthrough
- Covers: Installation, setup, running, debugging

---

## 🩺 Troubleshooting

### "403 Access Denied" from API

**Causes:**
1. Invalid API key
2. IP address blocked (rate limit violation)
3. Account suspended

**Fixes:**
```bash
# Test your API key at serpapi.com
python diagnostics/quick_check.py

# If blocked: Wait 24-48 hours or try different network
# If invalid: Get new key at serpapi.com/manage-api-key
```

### "400 Bad Request" from API

**This is fixed in current code!** If you see this:
1. Make sure you pulled latest code: `git pull`
2. Verify `start` parameter is removed/commented in AeroComps.py line 582
3. Verify query includes keywords in build_trade_query line 525

### "No jobs found" for all companies

**Possible causes:**
1. Companies not hiring currently (normal)
2. Wrong test file being used
3. Filters too restrictive

**Check:**
```bash
# Test with known active company
# Edit config: "testing_company_limit": 1
# Use Test_3_Companies.xlsx (Barnes Aerospace usually hiring)
python AeroComps.py
```

### Circuit Breaker Opens

**This is good! Protection working!**

**What it means:**
- System detected 3 consecutive failures
- Stopped to prevent IP block
- Check `log/api_audit.jsonl` for error details

**What to do:**
1. Wait 10 minutes
2. Check if API key valid: `python diagnostics/quick_check.py`
3. Run again

### Dependencies Won't Install

```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Try again
pip install -r resources/requirements.txt

# If still fails, install individually:
pip install pandas openpyxl requests tqdm google-search-results
```

---

## 📊 Understanding the Output

### Excel File Structure

**File:** `output/Aerospace_Alley_SkilledTrades_Jobs.xlsx`

**Columns:**
- **Company Name:** Aerospace manufacturer
- **Company Tier:** 1-5 (known size) or 99 (unknown size)
- **Employee Count:** Employee count or "Unknown" for Tier 99 companies
- **Job Cap:** Maximum jobs collected for this company based on tier
- **Job Title:** Position title
- **Location:** City, State
- **Via:** Job board source (Indeed, LinkedIn, etc.)
- **Source URL:** Direct link to application
- **Detected Extensions:** Salary, benefits (if available)
- **Description Snippet:** First 200 chars of description

### Analytics Report

**File:** `output/Aerospace_Alley_SkilledTrades_Jobs_Analytics.xlsx`

**Sheets:**
- **Summary Statistics:** Total jobs, unique companies, date ranges
- **Top Trades:** Most in-demand skills
- **Top Companies:** Highest hiring activity
- **Top Locations:** Geographic distribution
- **Job Board Sources:** Which platforms used most
- **Tier Analysis:** Companies and jobs by tier (NEW)
- **Tier Success Metrics:** Success rates by company size (NEW)
- **Failed Companies:** Companies with 0 jobs found, with tier details (NEW)

### Health Summary (Console Output)

```
============================================================
API HEALTH SUMMARY
============================================================
Runtime: 0.1 minutes

API Calls:
  Total: 1
  Successful: 1 (100.0%)
  Failed: 0
  Rate Limit Errors: 0
  Auth Errors: 0
  Server Errors: 0
  Avg Response Time: 456ms

Company Processing:
  Companies Processed: 1
  Companies with Jobs: 1 (100.0%)
  Total Jobs Found: 6
  Avg Jobs/Company: 6.0
============================================================
```

**What to look for:**
- **Successful:** Should be >95% (API calls succeed)
- **Companies with Jobs:**
  - Tier 1-2 (large): 60-80% success rate
  - Tier 3-4 (medium): 40-60% success rate
  - Tier 4-5 (small): 30-40% success rate (many small shops don't post publicly)
- **Overall Success Rate:** 35-50% is normal across all tiers
- **Rate Limit Errors:** Should be 0 (protection working)

---

## 🎯 Use Cases & Applications

### Sales Intelligence

**Lead Qualification:**
- Companies with 5+ job postings = active growth, high priority
- Companies hiring specialized roles (CNC, inspection) = capability investment
- Hiring spikes (vs. historical) = new contracts, buying window open

**Example Workflow:**
1. Run weekly scan
2. Filter for companies with 3+ new postings
3. Research recent contracts/awards
4. Tailor pitch: "I see you're expanding [specific capability]..."

### Market Analysis

**Quarterly Trends Report:**
- Compare hiring by company tier (Tier-1 vs. small suppliers)
- Track skill demand trends (CNC vs. manual machining vs. assembly)
- Geographic shifts (East Hartford vs. other regions)
- Seasonal patterns (Q1 hiring surge, Q3 slowdown)

**Competitive Benchmarking:**
- Your customer vs. their competitors
- Your region vs. other aerospace hubs
- Skilled trades availability vs. demand

### Workforce Planning

**Recruitment Strategy:**
- Which roles are hardest to fill (most postings, longest duration)
- Salary benchmarking (when data available)
- Geographic concentration of talent
- Competition for specific skills

**Training Program Development:**
- High-demand skills for curriculum design
- Partnership opportunities with hiring companies
- Apprenticeship program targeting

### Business Development

**Partnership Identification:**
- Companies hiring complementary skills (you do A, they need B)
- Geographic proximity for supplier relationships
- Growth trajectory alignment (both scaling up)
- Technology investment signals (automation, advanced manufacturing)

**M&A Target Screening:**
- Rapid hiring = growth
- High-value role hiring = capability building
- Sustained activity = financial health

---

## 🔒 Security & Best Practices

### API Key Security

**DO:**
- ✅ Store keys in `resources/config.json` (excluded from git)
- ✅ Use separate keys for testing vs. production
- ✅ Rotate keys quarterly
- ✅ Monitor usage at serpapi.com/dashboard

**DON'T:**
- ❌ Commit config.json to git
- ❌ Share keys in screenshots/documentation
- ❌ Use same key across multiple projects
- ❌ Store keys in environment variables on shared systems

### Rate Limiting

**Current Safe Rates:**
- 60 calls/hour maximum (protection system enforced)
- 20-30 calls/hour actual (with batch pauses)
- 3.0 second minimum between calls

**Why This Matters:**
- Prevents IP blocks (24-48 hour lockouts)
- Maintains API account good standing
- Reduces costs (fewer wasted calls on errors)

### Data Usage

**Legal Considerations:**
- Data for business intelligence only
- Don't resell or redistribute raw data
- Respect source attributions (Indeed, LinkedIn, etc.)
- Comply with data protection regulations (GDPR if applicable)

**Ethical Guidelines:**
- Don't overwhelm company career pages
- Honor robots.txt when scraping
- Rate limit conservatively
- Provide attribution when presenting insights

---

## 🛠️ Development & Contribution

### Project Status

**Phase:** Production-Ready ✅

**Recent Achievements (v2.2 - Oct 29, 2025):**
- ✅ Implemented 6-tier adaptive job cap system (Tiers 1-5 + Tier 99 for unknown)
- ✅ Persistent API usage tracking with cross-session state persistence
- ✅ Profile system with command-line override (quick_test, tier_test, production)
- ✅ Automatic API key rotation with 60-second warning period
- ✅ Dynamic output filename generation (testing vs production)
- ✅ Increased Tier 1 cap to 80 jobs for mega-corporations
- ✅ Updated API limits to correct 250 searches/month per free key
- ✅ Smart fallback for hyphenated company names
- ✅ Enhanced analytics with tier tracking and success metrics
- ✅ Achieved 100% API call success rate in testing

**Current Capabilities:**
- Automated data collection: 137 companies across 6 tiers
- Skilled trades classification: 100+ keywords
- Adaptive job caps: 10-80 jobs per company based on size (Tier 99: 20 jobs for unknown)
- Persistent API tracking: Usage survives restarts, prevents quota exhaustion
- Profile system: Quick test (3), tier test (15), production (137) with CLI override
- Smart fallback: Automatic retry for hyphenated names
- Excel export with tier analytics
- Multi-key support with priority-based auto-rotation
- Health monitoring with tier-specific insights

### Roadmap

**Short-Term (1-2 weeks):**
- Automated weekly scheduling
- Historical tracking database
- Change detection (new jobs, removed jobs)
- Email notifications for significant changes

**Medium-Term (1-3 months):**
- Alternative data sources (Adzuna API, direct scraping)
- Salary extraction and normalization
- Geographic filtering and radius search
- Enhanced analytics dashboard

**Long-Term (3-6 months):**
- Web interface for non-technical users
- Real-time monitoring and alerts
- Predictive analytics (hiring trends, market forecasts)
- Integration with CRM systems (Salesforce, HubSpot)

### Contributing

**If you're extending this project:**

1. **Don't modify AeroComps.py core logic** without thorough testing
2. **Test with testing_mode: true first** (1-3 companies)
3. **Monitor protection system** - watch for circuit breaker triggers
4. **Document changes** in this README
5. **Commit often** with descriptive messages

**Useful extensions:**
- Additional data sources (see resources/rate_limit_protection.py for integration examples)
- Enhanced analytics (see resources/analytics.py)
- Automation scheduling (cron jobs, Task Scheduler)
- Database storage (SQLite, PostgreSQL)

---

## ⚠️ Known Issues (v2.2)

The following issues were identified during production testing and will be addressed in v2.3:

### 1. API Key Auto-Rotation Failure (CRITICAL)

**Issue:** When the primary API key reaches its monthly limit, the system does not automatically switch to the backup key.

**Impact:**
- Script may fail mid-run when quota exhausted
- Backup API keys remain unused (0 calls)
- Requires manual intervention to continue

**Current Behavior:**
- Tracker shows: `primary-SerpAPI: 261/250 (104.4%)` ← Over limit
- Backup key: `2nd API-Backup: 0/250 (0.0%)` ← Never used

**Workaround:**
- Monitor API usage: `python resources/api_usage_tracker.py --report`
- If primary key approaching limit, manually edit `config.json` to swap key priorities
- Or wait for monthly reset before running production scans

**Status:** Under investigation. Switchover logic in `api_usage_tracker.py` needs review.

---

### 2. API Call Counter Inflation (HIGH)

**Issue:** The API usage tracker overcounts actual API calls by ~15-20%.

**Impact:**
- Tracker reports more calls than actually made to SerpAPI
- May trigger false "quota exhausted" warnings
- Affects multi-key rotation decisions

**Example:**
- Tracker reported: 261 calls
- SerpAPI dashboard: ~212 actual calls
- Discrepancy: ~49 calls overcounted

**Suspected Causes:**
- Failed company lookups incrementing counter
- Fallback retry attempts being double-counted
- Circuit breaker failures counting as API calls

**Workaround:**
- Cross-check with SerpAPI dashboard: https://serpapi.com/dashboard
- Assume tracker is ~15-20% inflated when planning runs
- For 137 companies: Expect ~210-220 actual calls (not 260-280)

**Status:** Needs diagnostic logging to identify where overcounting occurs.

---

### 3. High Failure Rate for Small/Unknown Companies (MEDIUM)

**Issue:** 65.7% of companies returned no jobs (90 out of 137).

**Impact:**
- Lower success rate than expected (34% vs 40-50% expected)
- Many Tier 99 (unknown size) companies in failed list
- May indicate matching issues or companies not posting publicly

**Failed Company Examples:**
- Small manufacturers: A-1 Machining, Accu-Rite Tool, Accuturn Mfg
- Specialty services: Armoloy, Bodycote, National Peening
- Division/subsidiary names: TIGHITCO divisions, Triumph divisions

**Possible Causes:**
1. Small companies don't post jobs on indexed job boards
2. Company name matching issues (hyphens, Inc/LLC variations)
3. Companies using recruiting agencies (jobs listed under agency name)
4. Companies with zero current openings (normal)

**Analysis Needed:**
- Manual spot-check: Do these companies have jobs on their websites?
- Review company name normalization logic
- Test with alternative search strategies

**Status:** Requires investigation. 65% failure is higher than industry baseline.

---

### 4. Job Count Discrepancy in Analytics (LOW)

**Issue:** Analytics report "Total Jobs" count may not match raw data row count, especially for Tier 99 companies.

**Impact:**
- Minor reporting inconsistency
- May cause confusion when cross-checking numbers

**Suspected Cause:**
- Aggregation logic in tier analysis
- Potential duplicate counting in tier summaries

**Workaround:**
- Use "Raw Data" sheet in Excel for accurate job count
- Analytics summaries should be treated as approximate

**Status:** Needs data validation between raw data and analytics aggregations.

---

### Priority for v2.3 Fixes

1. **CRITICAL:** API key auto-rotation (#1)
2. **HIGH:** API call counter accuracy (#2)
3. **MEDIUM:** Company matching and failure rate (#3)
4. **LOW:** Analytics count validation (#4)

**Target:** Address issues #1 and #2 in v2.3 (Q4 2025)

---

## 📞 Support

### For Business Questions

**Understanding output:**
- Review "Understanding the Output" section above
- Check analytics report for high-level insights
- Focus on "Companies with Jobs" metric (15-25% is normal)

**Interpreting results:**
- 0 jobs for a company = not hiring publicly OR posts on private channels
- High-volume hiring (10+) = major expansion or backfill wave
- Specialized roles (inspection, tooling) = capability investments

### For Technical Issues

**Before asking:**
1. Run `python diagnostics/setup_check.py` - fix any ❌ errors
2. Run `python diagnostics/quick_check.py` - verify API access
3. Check `log/api_audit.jsonl` for specific errors
4. Review "Troubleshooting" section above

**Common solutions:**
- 403 errors → Check API key or wait for block to clear
- 400 errors → Pull latest code (deprecated parameter fixed)
- No results → Normal for companies not hiring currently
- Circuit breaker → Good! Protection working. Wait and retry.

### GitHub Issues

When reporting issues, include:
- Error message (full traceback)
- Output of `python diagnostics/setup_check.py`
- Output of `python diagnostics/quick_check.py`
- Last 10 lines of `log/api_audit.jsonl`
- Python version: `python --version`

---

## 📚 Additional Documentation

All documentation has been consolidated into this README. Previous separate documentation files have been integrated:

**Consolidated Sections:**
- Quick Start Guide (from QUICKSTART.md)
- Local Setup (from LOCAL_SETUP_GUIDE.md)
- VSCode Setup (from VSCODE_SETUP.md, VSCODE_BEGINNER_GUIDE.md)
- Protection System (from RATE_LIMIT_PROTECTION_SPECIFICATION.md, PROTECTION_SYSTEM_VALIDATION.md)
- Technical Analysis (from NETWORK_SWITCHING_ANALYSIS.md, INTEGRATION_GUIDE.md)
- Project History (from SESSION_HANDOFF.md)

**Single Source of Truth:** This README serves both technical and non-technical audiences.

---

## 📈 Success Metrics

### What "Success" Looks Like

**Technical Success:**
- ✅ 100% API call success rate (no 400/403/429 errors)
- ✅ Protection system prevents rate limits (no circuit breaker triggers)
- ✅ Completes 137-company run in ~12-15 minutes (with 45s batch pauses)
- ✅ Finds 100-300+ jobs total (35-50% of companies hiring)
- ✅ Tier-based analytics provide granular insights

**Business Success:**
- ✅ Actionable insights for sales team (3-5 high-priority leads per week)
- ✅ Market trend identification (quarterly hiring patterns visible)
- ✅ Competitive intelligence value (know before competitors)
- ✅ Time savings (vs. manual job board checking: 10+ hours/week → 5 minutes automated)

### Current Performance

**Latest Test Run (Oct 29, 2025):**

**3-Company Test:**
- Companies Processed: 3 (Barnes, GKN, Hanwha)
- Success Rate: 100% (3/3 companies found jobs)
- Jobs Found: 43 total
- API Calls Used: 9/250
- Runtime: ~15 seconds
- Tiers Tested: 2, 3, 4

**15-Company Test:**
- Companies Processed: 15 (all Tier 4 small companies)
- Success Rate: 35.7% (5/14 companies found jobs - 1 had fallback error)
- Jobs Found: 55 total
- API Calls Used: 25/250
- Runtime: ~3 minutes
- Fallback System: Active, 1 hyphen retry triggered

**Production Ready:** ✅ System stable, tier analytics working, ready for 137-company run

---

## 🎓 Learning Resources

### Understanding SerpAPI

- **Official Docs:** [serpapi.com/docs](https://serpapi.com/docs)
- **Google Jobs API:** [serpapi.com/google-jobs-api](https://serpapi.com/google-jobs-api)
- **Pricing:** [serpapi.com/pricing](https://serpapi.com/pricing)

### Python for Data Collection

- **Pandas Guide:** [pandas.pydata.org](https://pandas.pydata.org/docs/)
- **Requests Library:** [requests.readthedocs.io](https://requests.readthedocs.io/)
- **Excel with Python:** [openpyxl.readthedocs.io](https://openpyxl.readthedocs.io/)

### Aerospace Industry Context

- **Connecticut Aerospace:** Understanding the 137-company ecosystem
- **Skilled Trades:** Definitions and categories tracked
- **Hiring Patterns:** Typical aerospace recruiting cycles

---

**Last Updated:** October 29, 2025
**Version:** 2.2 (6-Tier System, Persistent API Tracking, Profile System)
**Status:** Production-Ready ✅
**Next Milestone:** Full 137-Company Production Run
