# THRESHOLD AND FALLBACK DECISIONS - RATIONALE

## Question 1: Why 15% Success Rate Threshold?

### The Logic Behind 15%

**Baseline Assumption:**
- In aerospace industry, approximately 15-25% of companies actively hire skilled trades at any given time
- This varies by:
  - Company size (larger = more likely hiring)
  - Economic conditions
  - Seasonality (more hiring in Q1/Q2)

**Why 15% Specifically:**

**Too High (e.g., 50%):**
- Would miss legitimate scenarios where many companies aren't hiring
- Might trigger fallback unnecessarily during slow hiring periods

**Too Low (e.g., 5%):**
- Would take too long to detect API problems
- Wastes API calls on broken approach

**15% is Conservative:**
- If fewer than 15% of companies return jobs, something is likely wrong with our approach
- Based on your list: 137 companies, we'd expect at least 20-30 to have active postings
- If we process 10 companies and <2 have jobs → red flag

### Data-Driven Adjustment

**Make it Configurable:**
```json
"fallback_triggers": {
  "min_success_rate": 0.15,         // 15% - adjustable
  "sample_size": 10,                // Check after 10 companies
  "consecutive_failures": 5,        // Or 5 straight failures
  "rate_limit_errors": 3           // Or 3 rate limits
}
```

**Should be Tuned Based on:**
1. **Initial Test Results:** Run with your 137 companies, see actual success rate
2. **Industry Benchmarks:** Compare with known hiring rates
3. **Company Type:** Tier-1 vs small manufacturers
4. **Time of Year:** Adjust seasonally

**My Recommendation:**
- Start with 15% as baseline
- After first full run, calculate: `actual_success_rate = companies_with_jobs / total_companies`
- Adjust threshold to: `threshold = 0.7 * actual_success_rate`
  - If 30% of companies have jobs normally, set threshold to 21%
  - If success drops below 21%, trigger fallback

---

## Question 2: What is Adzuna and Why Backup1?

### What is Adzuna?

**Adzuna** is a job search aggregator API (alternative to SerpAPI).

**Key Facts:**
- **Website:** https://www.adzuna.com/
- **Founded:** 2011 (UK-based, US coverage)
- **Function:** Aggregates jobs from 100+ sources
- **Sources:** Indeed, Monster, CareerBuilder, company sites, government job boards
- **Coverage:** Different sources than Google Jobs (some overlap, some unique)

**Comparison to SerpAPI:**

| Feature | SerpAPI | Adzuna |
|---------|---------|--------|
| **Source** | Google Jobs | Own aggregation |
| **Price** | $50/mo (5,000 searches) | $0.50 per 1,000 searches |
| **Coverage** | 70-90% for major OEMs | 50-70% for aerospace |
| **Freshness** | Google's index (~daily) | Weekly aggregation |
| **Ease of Use** | Very easy | Easy |
| **US Focus** | Excellent | Good |

### Why Chosen as Backup1?

**Decision Criteria:**

**Option A: Another API (Adzuna)** ✅ CHOSEN
- **Pros:**
  - Fast to implement (similar to SerpAPI)
  - Very cheap ($0.20 for entire project)
  - Different sources (might find jobs SerpAPI missed)
  - No scraping complexity
  - Instant results
- **Cons:**
  - Still limited (won't find all jobs)
  - Another external dependency

**Option B: Direct Scraping** (Backup2)
- **Pros:**
  - 100% coverage (if done right)
  - No API costs
  - Most up-to-date data
- **Cons:**
  - Development time (5-7 days)
  - Maintenance required
  - Slower execution
  - Legal/ethical considerations

**Option C: Specialized Aerospace Job Boards**
- Example: AerospaceJobsUSA.com, AviationJobSearch.com
- **Pros:**
  - Aerospace-specific
  - Might have niche postings
- **Cons:**
  - Limited APIs available
  - Likely requires scraping anyway
  - Smaller coverage

**Why This Order:**

```
Priority 1: SerpAPI (Google Jobs)
↓ (if fails)
Priority 2: Adzuna API
↓ (if fails)
Priority 3: Direct Scraping
↓ (if fails)
Priority 4: Manual Review
```

**Reasoning:**
1. **Speed:** APIs are fast, scraping is slow
2. **Cost:** Adzuna is dirt cheap ($0.20 total)
3. **Effort:** API integration = 30 minutes, scraping = days
4. **Coverage:** Try two different aggregators before custom solution
5. **Fallback Layers:** Multiple options before giving up

### When to Use Each:

**Use SerpAPI when:**
- Companies post to major job boards (Indeed, LinkedIn)
- Major OEMs (Boeing, Lockheed, etc.)
- Initial broad discovery

**Use Adzuna when:**
- SerpAPI returns empty for company you know hires
- Different source aggregation needed
- SerpAPI rate limited but jobs needed urgently

**Use Direct Scraping when:**
- Both APIs fail for specific company
- Company uses internal ATS (Workday, Taleo)
- Need 100% coverage guarantee
- Long-term recurring runs (cost savings)

**Use Manual Review when:**
- All automated methods exhausted
- High-priority company needs verification
- Quality check required

---

## Cost Analysis

### For Your 137-Company List:

**SerpAPI Only:**
- 137 companies × 3 calls = 411 searches
- Cost: 2 free accounts (250 each) = $0
- If paid: $50/month

**With Adzuna Fallback:**
- SerpAPI: 411 searches = $0 (free accounts)
- Adzuna (if needed for 20 companies): 60 searches × $0.0005 = $0.03
- **Total: $0.03**

**With Direct Scraping:**
- Development: 40 hours × $100/hr = $4,000 (one-time)
- Maintenance: $200/year
- Runtime: Free
- **Break-even: 8 months of $50/month SerpAPI**

**Recommendation for You:**
- **Demo/Short-term:** SerpAPI + Adzuna ($0.03 total)
- **Production (recurring):** Hybrid (APIs for discovery + scraping for gaps)
- **Long-term (weekly runs):** Build scraping framework (cost-effective after 8 months)

---

## Configurable Thresholds

### Add to config.json:

```json
"fallback_detection": {
  "enabled": true,

  "triggers": {
    "min_success_rate": 0.15,
    "sample_size_companies": 10,
    "consecutive_failures": 5,
    "rate_limit_errors": 3
  },

  "strategy_order": [
    "serpapi",
    "adzuna",
    "scraping",
    "manual"
  ],

  "adzuna_config": {
    "enabled": false,
    "app_id": "your_adzuna_app_id",
    "app_key": "your_adzuna_app_key"
  },

  "scraping_config": {
    "enabled": false,
    "timeout_seconds": 30,
    "max_retries": 3
  }
}
```

**Benefits:**
- Easy to tune thresholds based on real data
- Can enable/disable fallback strategies
- No code changes needed for adjustments

---

## Bottom Line

**15% Threshold:**
- Conservative estimate based on aerospace hiring patterns
- Should be validated with real data
- Configurable for tuning

**Adzuna as Backup1:**
- Fast alternative API ($0.20 for entire project)
- Different sources than SerpAPI
- Easy to implement (30 minutes)
- Try before resorting to scraping

**Next Step:**
- Implement Priority Fixes
- Test with corrected queries
- Measure actual success rate
- Adjust thresholds based on real data
