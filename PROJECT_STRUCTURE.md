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
├── .gitignore                       # Git exclusions (config.json, output/, logs)
│
├── data/                            # Input data (company lists)
│   └── Aerospace_Alley_Companies.xlsx   # Full 137-company list (production)
│
├── resources/                       # Core modules and configuration
│   ├── __init__.py                  # Python package marker
│   ├── analytics.py                 # Analytics generation (top trades, locations)
│   ├── rate_limit_protection.py    # 7-layer rate limiting system
│   ├── salary_extraction_pseudocode.py  # Future feature pseudocode
│   ├── config.json                  # API keys & settings (GITIGNORED - not committed)
│   └── config_test_max25.json       # Test configuration (25 API calls max)
│
├── diagnostics/                     # Diagnostic tools (troubleshooting)
│   ├── check_block_status.py        # Check if IP blocked by SerpAPI
│   ├── quick_check.py               # Quick API connectivity test
│   └── setup_check.py               # Comprehensive setup validation
│
├── docs/                            # Documentation
│   └── testing/                     # Test documentation & files
│       ├── TEST_SETUP_GUIDE.md          # Step-by-step test instructions
│       ├── TEST_25_STRATEGIC.md         # 25-company test strategy
│       ├── TEST_CONFIGURATION_4TIER.md  # 4-tier test configuration
│       ├── TEST_MAX_25_CALLS.md         # 9-company test (25 API calls)
│       ├── Test_3_Companies.xlsx        # 3-company quick test file
│       ├── Test_Max25_9Companies.csv    # 9-company test CSV
│       └── convert_test_csv_to_excel.py # CSV→Excel converter
│
├── future/                          # Future development planning
│   ├── COMPANY_SIZE_LOOKUP_IMPLEMENTATION.md   # Company size database docs
│   ├── EXTERNAL_API_OPTIONS_MINIMAL_COST.md    # Alternative data sources
│   ├── IMPLEMENTATION_REVIEW_SUMMARY.md        # Implementation analysis
│   ├── IMPLEMENTATION_SUMMARY.md               # Implementation guide
│   ├── KEYWORD_EXPANSION_ANALYSIS.md           # Keyword research
│   ├── PRE_IMPLEMENTATION_REVIEW.md            # Pre-launch review
│   ├── STRATEGY_INDUSTRY_EXPANSION.md          # Industry expansion strategy
│   └── STRATEGY_JOB_CAP_OPTIMIZATION.md        # API optimization strategy
│
├── log/                             # Runtime logs (GITIGNORED)
│   ├── .gitkeep                     # Preserves directory in git
│   └── api_audit.jsonl              # API call audit trail (created at runtime)
│
└── output/                          # Results (GITIGNORED - created at runtime)
    ├── <Company>_Results.xlsx           # Job listings (per run)
    └── <Company>_Results_Analytics.xlsx # Analytics summary (per run)
```

---

## 🔑 Key Files

### Production Files

**`AeroComps.py`** - Main Pipeline (1,000+ lines)
- 5-tier adaptive job caps (10, 15, 25, 40, 50 jobs based on company size)
- Comprehensive job matching (ALL aerospace roles: engineering, IT, business, admin, trades)
- 7-layer rate limiting system (60 calls/hour safe limit)
- Excel analytics generation (top trades, locations, hiring trends)

**`resources/analytics.py`** - Analytics Module
- Top 10 in-demand trades analysis
- Top 10 hiring companies
- Top 10 locations (geographic distribution)
- Job board source analysis
- Excel report generation

**`resources/rate_limit_protection.py`** - Rate Limiting
- Token Bucket algorithm (60 calls/hour capacity)
- Circuit Breaker pattern (3 failure threshold)
- Exponential backoff (3 retry attempts)
- Batch processor (10 companies/batch with 2-5 min pauses)
- Audit logger (JSONL format)
- Health monitor (real-time alerts)

### Configuration Files

**`resources/config.json`** - Production Config (GITIGNORED)
```json
{
  "api_keys": [
    {"label": "Primary", "key": "YOUR_KEY", "limit": 250, "priority": 1}
  ],
  "settings": {
    "testing_mode": false,
    "input_file": "data/Aerospace_Alley_Companies.xlsx",
    "output_file": "output/AeroAlley_Results.xlsx",
    "max_api_calls_per_key": 250,
    "min_interval_seconds": 3.0,
    "max_threads": 3
  }
}
```

**`resources/config_test_max25.json`** - Test Config (9 companies, 25 API calls)

### Data Files

**`data/Aerospace_Alley_Companies.xlsx`** - Production Data
- 137 Connecticut aerospace companies
- Company Name column (required)
- Expected API calls: ~225-250 (within free tier limits)

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

## 📊 5-Tier Adaptive Job Caps

| Tier | Employee Count | Job Cap | Companies (CT) | API Calls/Company |
|------|----------------|---------|----------------|-------------------|
| 1    | 10,000+        | 50      | 2              | 5                 |
| 2    | 1,000-9,999    | 40      | 5              | 4                 |
| 3    | 200-999        | 25      | 15             | 3 (avg 2.5)       |
| 4    | 50-199         | 15      | 35             | 2 (avg 1.5)       |
| 5    | 10-49          | 10      | 80             | 1                 |

**Total:** 137 companies → ~225 API calls (under 250 free tier limit)

---

## 🚀 Usage

### Production Run (Full 137 Companies)
```bash
# 1. Add your API key to resources/config.json
# 2. Run full scan
python AeroComps.py

# Expected: 2,000-4,000+ jobs across all aerospace roles
# Runtime: 30-40 minutes (rate limited to 60 calls/hour)
```

### Test Run (9 Companies, 25 API Calls)
```bash
python AeroComps.py --config resources/config_test_max25.json

# Expected: 300-500 jobs
# Runtime: 2-3 minutes
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

**Job Results:** `output/<InputFile>_Results.xlsx`
- Company Name
- Job Title
- Location
- Via (job board source)
- Source URL (apply link)
- Detected Extensions (salary, schedule, etc.)
- Description Snippet (first 200 chars)
- Timestamp (when scraped)

**Analytics:** `output/<InputFile>_Results_Analytics.xlsx`
- Summary Statistics (total jobs, companies, date range, job boards)
- Top 10 In-Demand Trades (with job counts and percentages)
- Top 10 Hiring Companies
- Top 10 Locations

**Audit Log:** `log/api_audit.jsonl`
- Timestamp, API call details, response status, company, job count
- Used for debugging and cost analysis

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
3. Verify company size tiers in `COMPANY_SIZE_DATABASE` (AeroComps.py:510-553)

---

## 📝 Future Development

See `future/` folder for:
- External API integration options (zero-cost alternatives)
- Salary extraction implementation
- Industry expansion strategies (beyond aerospace)
- Job cap optimization (machine learning approaches)

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
**Last Tested:** October 2025
**Next Review:** Quarterly (company size updates)
