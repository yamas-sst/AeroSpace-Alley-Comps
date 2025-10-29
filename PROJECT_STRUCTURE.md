# AeroSpace Alley Job Scanner - Project Structure

**Production-Ready Architecture**
*Last Updated: October 2025*

---

## 📁 Directory Structure

```
AeroSpace-Alley-Comps/
├── AeroComps.py                    # Main job scanning pipeline
├── README.md                        # Project overview and setup guide
├── PROJECT_STRUCTURE.md             # This file - architecture documentation
├── CHANGELOG.md                     # Version history and release notes
├── .gitignore                       # Git exclusions (config.json, output/, logs)
│
├── data/                            # Input data (company lists)
│   └── Aerospace_Alley_Companies.xlsx   # Full 137-company list (production)
│
├── resources/                       # Core modules and configuration
│   ├── __init__.py                  # Python package marker
│   ├── analytics.py                 # Analytics generation (top trades, locations)
│   ├── rate_limit_protection.py    # 7-layer rate limiting system
│   ├── api_usage_tracker.py        # Persistent API usage tracking (NEW v2.2)
│   ├── salary_extraction_pseudocode.py  # Future feature pseudocode
│   ├── config.json                  # Master config with profiles (GITIGNORED)
│   └── requirements.txt             # Python dependencies
│
├── diagnostics/                     # Diagnostic & test tools
│   ├── check_block_status.py        # Check if IP blocked by SerpAPI
│   ├── quick_check.py               # Quick API connectivity test
│   ├── setup_check.py               # Comprehensive setup validation
│   ├── test_matching_logic.py       # Job matching validation tests
│   └── TEST_SETUP_GUIDE.md          # Step-by-step test instructions
│
├── future/                          # Future development planning
│   ├── DYNAMIC_COMPANY_SIZING_STRATEGY.md  # Scaling strategy (500+ companies)
│   ├── STRATEGY_INDUSTRY_EXPANSION.md       # Industry expansion strategy
│   └── STRATEGY_JOB_CAP_OPTIMIZATION.md     # API optimization strategy
│
├── docs/
│   └── archive/                     # Archived documentation
│       ├── testing/                 # Historical test documentation
│       └── planning/                # Historical planning documents
│
├── log/                             # Runtime logs (GITIGNORED)
│   ├── .gitkeep                     # Preserves directory in git
│   ├── api_audit.jsonl              # API call audit trail (created at runtime)
│   └── api_usage_state.json         # Persistent usage tracking state (NEW v2.2)
│
└── output/                          # Results (GITIGNORED - created at runtime)
    ├── Aerospace_Alley_SkilledTrades_Jobs.xlsx  # Production output
    ├── Test_*_*.xlsx                # Test run outputs (timestamped)
    └── *_Analytics.xlsx             # Analytics reports
```

---

## 🔑 Key Files

### Production Files

**`AeroComps.py`** - Main Pipeline (1,250+ lines)
- 6-tier adaptive job caps (80, 40, 30, 20, 10 jobs + Tier 99: 20 jobs for unknown size)
- Comprehensive job matching (ALL aerospace roles: engineering, IT, business, admin, trades)
- Profile system with command-line override (quick_test, tier_test, production)
- Persistent API usage tracking integration
- Dynamic output filename generation (testing vs production)
- 7-layer rate limiting system (60 calls/hour safe limit)
- Excel analytics generation (top trades, locations, hiring trends, tier analysis)

**`resources/analytics.py`** - Analytics Module
- Top 10 in-demand trades analysis
- Top 10 hiring companies
- Top 10 locations (geographic distribution)
- Job board source analysis
- Excel report generation

**`resources/rate_limit_protection.py`** - 7-Layer Rate Limiting (900+ lines)
- Token Bucket algorithm (60 calls/hour capacity)
- Circuit Breaker pattern (3 failure threshold)
- Exponential backoff (3 retry attempts)
- Batch processor (10 companies/batch with 45-second pauses)
- Dual rate implementation (3.2s active, 60s commented for troubleshooting)
- Audit logger (JSONL format)
- Health monitor (real-time alerts)

**`resources/api_usage_tracker.py`** - Persistent API Usage Tracking (NEW v2.2, 450 lines)
- Cross-session usage tracking (survives script restarts)
- Multi-key support with automatic rotation based on priority
- Per-key billing cycle tracking with auto-reset on billing day
- Usage warnings at 75%, 90%, 100% thresholds
- 60-second warning before key switch with Ctrl+C safe exit option
- Daily usage history logging
- Command-line usage reporting: `python resources/api_usage_tracker.py --report`
- State file: `log/api_usage_state.json` (persistent JSON state)

### Configuration Files

**`resources/config.json`** - Master Config with Profiles (GITIGNORED)
```json
{
  "api_keys": [
    {
      "label": "primary-SerpAPI",
      "key": "YOUR_SERPAPI_KEY_HERE",
      "monthly_limit": 250,
      "billing_cycle_day": 1,
      "priority": 1
    },
    {
      "label": "2nd API-Backup",
      "key": "YOUR_BACKUP_KEY_HERE",
      "monthly_limit": 250,
      "billing_cycle_day": 1,
      "priority": 2
    }
  ],

  "active_profile": "tier_test",

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

### Data Files

**`data/Aerospace_Alley_Companies.xlsx`** - Production Data
- 137 Connecticut aerospace companies
- Company Name column (required)
- Expected API calls: ~260-280 (requires 2 free keys OR 1 paid key)

---

## 🎯 Job Matching Logic

### Comprehensive Scope (ALL Aerospace Roles)

**CORE_TRADE_WORDS** (~100+ keywords):
- **Manufacturing & Trades:** machinist, cnc, welder, fabricator, assembler, operator
- **Engineering (ALL types):** engineer, engineering (manufacturing, software, design, quality, mechanical)
- **IT & Software:** software, developer, programmer, analyst, data, systems, database
- **Business & Admin:** sales, marketing, HR, finance, accounting, purchasing, admin, receptionist
- **Management:** manager, director, VP, president, executive, specialist, representative
- **Skilled Trades:** electrician, plumber, HVAC, inspector, technician, mechanic
- **Planning & Operations:** planner, scheduler, logistics, supply chain, operations
- **Design & Creative:** designer, design, architect, drafter, CAD

**EXCLUSION_PATTERNS** (minimal - only truly unrelated):
- Medical: nurse, doctor, physician, clinical
- Custodial: janitor, custodian, housekeeper

**Result:** Captures 300-500+ jobs per 9-company test (comprehensive market intelligence)

---

## 📊 6-Tier Adaptive Job Cap System

| Tier | Employee Count | Job Cap | Companies (CT) | API Calls/Company |
|------|----------------|---------|----------------|-------------------|
| 1    | 10,000+        | 80      | 2              | 8                 |
| 2    | 1,000-9,999    | 40      | 5              | 4                 |
| 3    | 200-999        | 30      | 15             | 3                 |
| 4    | 50-199         | 20      | 35             | 2                 |
| 5    | 10-49          | 10      | 80             | 1                 |
| 99   | Unknown size   | 20      | ~30 (est)      | 2                 |

**Total:** 137 companies → ~260-280 API calls

**Key Features:**
- **Tier 99:** Conservative default for companies not in size database (20 jobs)
- **Employee Count Display:** Known sizes show count, Tier 99 shows "Unknown"
- **Dynamic Sizing (Future):** See `future/DYNAMIC_COMPANY_SIZING_STRATEGY.md` for 500+ company scaling

**API Key Requirements:**
- **2 free keys recommended:** 250 each = 500 total (ideal for 137 companies)
- **OR 1 paid key:** $50/month for 5,000 searches

---

## 🚀 Usage

### Quick Test (3 Companies)
```bash
python AeroComps.py --profile quick_test

# Expected: 15-30 jobs
# API Calls: ~5-10
# Runtime: ~30-60 seconds
```

### Tier Test (15 Companies)
```bash
python AeroComps.py --profile tier_test

# Expected: 100-200 jobs
# API Calls: ~30-40
# Runtime: 2-3 minutes
```

### Production Run (Full 137 Companies)
```bash
python AeroComps.py --profile production

# Expected: 2,000-4,000+ jobs across all aerospace roles
# API Calls: ~260-280
# Runtime: 12-15 minutes (rate limited to 60 calls/hour, 45s batch pauses)
```

### Using Default Profile
```bash
# Uses active_profile from config.json
python AeroComps.py

# To change default: Edit "active_profile" in config.json
```

### Check API Usage
```bash
python resources/api_usage_tracker.py --report

# Shows:
# - Usage per key (calls used / monthly limit)
# - Remaining calls per key
# - Recent daily usage history
# - Warning/critical status indicators
```

### Diagnostics
```bash
# Check if your IP is blocked
python diagnostics/check_block_status.py

# Quick API connectivity test
python diagnostics/quick_check.py

# Comprehensive setup validation
python diagnostics/setup_check.py
```

---

## 📈 Output Files

**Job Results:** `output/Aerospace_Alley_SkilledTrades_Jobs.xlsx` (production)
or `output/Test_*Companies_*.xlsx` (testing with timestamp)
- Company Name
- Company Tier (1-5 or 99 for unknown)
- Employee Count (number or "Unknown" for Tier 99)
- Job Cap (max jobs collected for this company)
- Job Title
- Location
- Via (job board source)
- Source URL (apply link)
- Detected Extensions (salary, schedule, etc.)
- Description Snippet (first 200 chars)
- Timestamp (when scraped)

**Analytics:** `output/*_Analytics.xlsx`
- Summary Statistics (total jobs, companies, date range, job boards)
- Top 10 In-Demand Trades (with job counts and percentages)
- Top 10 Hiring Companies
- Top 10 Locations
- Tier Analysis (companies and jobs by tier)
- Tier Success Metrics (success rates by company size)
- Failed Companies (0 jobs found, with tier details)

**Audit Log:** `log/api_audit.jsonl`
- Timestamp, API call details, response status, company, job count
- Used for debugging and cost analysis

**API Usage State:** `log/api_usage_state.json` (NEW v2.2)
- Persistent usage tracking across script executions
- Per-key usage counters, daily history, billing cycle tracking
- Auto-resets on billing day, survives restarts
- Used by api_usage_tracker.py for quota management

---

## 🔒 Security & Best Practices

### Secrets Management
- ✅ `config.json` is GITIGNORED (never commit API keys)
- ✅ Test config has placeholder keys
- ✅ README instructs users to add their own keys

### Rate Limiting
- ✅ 7-layer protection system prevents IP blocks
- ✅ Token bucket limits to 60 calls/hour (safe for trial accounts)
- ✅ Circuit breaker stops execution after 3 consecutive failures
- ✅ Audit logging tracks all API usage

### Data Privacy
- ✅ Output files are GITIGNORED
- ✅ No personal information stored
- ✅ Only public job listings collected

---

## 🧹 Maintenance

### Regular Cleanup
```bash
# Remove old output files
rm -rf output/*

# Clear audit logs
rm log/api_audit.jsonl

# Clear Python cache
rm -rf __pycache__
```

### Updating Company Database
1. Update `data/Aerospace_Alley_Companies.xlsx`
2. Ensure "Company Name" column exists
3. Add new companies to `COMPANY_SIZE_DATABASE` in `AeroComps.py` (lines 180-250) if size known
   - Companies not in database default to Tier 99 (20 jobs)
4. For 500+ companies, see `future/DYNAMIC_COMPANY_SIZING_STRATEGY.md` for automated sizing

---

## 📝 Future Development

See `future/` folder for:
- **Dynamic Company Sizing:** `DYNAMIC_COMPANY_SIZING_STRATEGY.md` - Automated company size lookup for 500+ company scaling
- **Industry Expansion:** `STRATEGY_INDUSTRY_EXPANSION.md` - Beyond aerospace
- **Job Cap Optimization:** `STRATEGY_JOB_CAP_OPTIMIZATION.md` - Machine learning approaches

**Archived Documentation:** See `docs/archive/` for historical planning and testing documents

---

## 🐛 Troubleshooting

**Issue:** "API Error: Google hasn't returned any results"
- **Solution:** Check if company name has special characters (& → space, - → cleaned)

**Issue:** "API limit reached"
- **Solution:** Check audit log, verify rate limiting is working, wait 1 hour before retry

**Issue:** "No jobs found"
- **Solution:** Verify company is hiring, check query format, test with diagnostics tools

**Issue:** IP blocked by SerpAPI
- **Solution:** Run `diagnostics/check_block_status.py`, wait 24 hours, contact support

---

## 📞 Support

- **GitHub Issues:** Report bugs and feature requests
- **Documentation:** See README.md for setup and usage
- **Diagnostics:** Use tools in `diagnostics/` folder for troubleshooting

---

**Status:** ✅ Production-Ready
**Version:** 2.2 (6-Tier System, Persistent API Tracking, Profile System)
**Last Updated:** October 29, 2025
**Last Tested:** October 29, 2025
**Next Review:** Quarterly (company size updates)
