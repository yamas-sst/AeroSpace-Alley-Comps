# Dynamic Company Sizing Strategy - Future Development

**Status:** ⏸️ DEFERRED - Not implemented in current version
**Purpose:** Preserved for future implementation when scaling beyond 500 companies
**Priority:** Medium (implement when manual database maintenance becomes burdensome)

---

## Overview

Multi-source company size lookup system for automatic tier classification when scaling to thousands of companies.

## Problem Statement

Current system (as of v2.0):
- Manual database: Only ~30 companies have size data (22% coverage of 137 companies)
- Requires research for each new company added
- Data becomes stale over time (employee counts change)
- Doesn't scale efficiently to thousands of companies
- Unknown companies default to Tier 99 (20 jobs)

## Current Approach (Working Well for 137 Companies)

**6-Tier System:**
- Tier 1 (10,000+): 80 jobs
- Tier 2 (1,000-9,999): 40 jobs
- Tier 3 (200-999): 30 jobs
- Tier 4 (50-199): 20 jobs
- Tier 5 (10-49): 10 jobs
- Tier 99 (Unknown): 20 jobs (conservative default)

**Manual Database:** `COMPANY_SIZE_DATABASE` in AeroComps.py

## Proposed Solutions (for Future Scale)

### Option 1: External API Integration

**APIs to Consider:**
- **Clearbit Company API** (50 free calls/month)
  - High accuracy (90%+)
  - Real-time employee counts
  - Cost: Free tier → $99/month

- **LinkedIn Company Scraper** (via RapidAPI)
  - Official LinkedIn data
  - 100 free calls/month
  - Cost: Free tier → variable

- **OpenCorporates** (Open Data)
  - Unlimited calls
  - Lower accuracy (historical data)
  - Cost: FREE

**Implementation Effort:** 8-12 hours
**Maintenance:** Low (automated)

---

### Option 2: ML-Based Estimation

**Heuristic Model: Job Posting Volume**

**Logic:**
```
If company posts 40+ jobs → Likely Tier 1-2 (large)
If company posts 20-39 jobs → Likely Tier 2-3 (medium-large)
If company posts 10-19 jobs → Likely Tier 3-4 (medium)
If company posts 5-9 jobs → Likely Tier 4-5 (small-medium)
If company posts 1-4 jobs → Likely Tier 5 (small)
```

**Accuracy:** ~75% within 1 tier, 50% exact match
**Implementation Effort:** 4-6 hours
**Maintenance:** None (self-adjusting)
**Cost:** FREE

---

### Option 3: Hybrid Approach (RECOMMENDED)

**Multi-Source Cascade:**
```
1st: Check manual database (100% confidence)
     ↓ (if not found)
2nd: Query external API (90% confidence)
     ↓ (if API fails)
3rd: Use ML estimation from job volume (60% confidence)
     ↓ (if all fail)
4th: Default to Tier 99 (40% confidence)
```

**Implementation Effort:** 12-16 hours
**Maintenance:** Low
**Cost:** $0-$99/month (depending on volume)

**Benefits:**
- ✅ Best accuracy with graceful degradation
- ✅ Persistent caching reduces API costs
- ✅ Automatic fallback if API down
- ✅ Self-improving as database grows

---

## Implementation Timeline

**Phase 1: Current (v2.0)**
- Manual database (30 companies)
- Tier 99 for unknowns
- Adequate for 137 Connecticut aerospace companies

**Phase 2: 500+ Companies**
- Implement ML estimation (Option 2)
- Add persistent SQLite cache
- Estimated timeline: 1-2 months

**Phase 3: 1,000+ Companies**
- Implement hybrid approach (Option 3)
- Integrate Clearbit or similar API
- Add domain guessing logic
- Estimated timeline: 3-6 months

---

## Technical Architecture (Hybrid Approach)

**New File:** `resources/dynamic_company_sizer.py`

```python
class DynamicCompanySizer:
    def __init__(self, clearbit_api_key=None):
        self.curated_db = load_from_aerocomps()
        self.cache_db = sqlite3.connect('data/company_cache.db')
        self.clearbit_api = clearbit_api_key

    def get_company_tier(self, company_name, jobs_found=None):
        # 1. Check curated database
        if company_name in self.curated_db:
            return self.curated_db[company_name]['tier']

        # 2. Check persistent cache
        cached = self.get_from_cache(company_name)
        if cached and not self.is_stale(cached):
            return cached['tier']

        # 3. Try external API
        if self.clearbit_api:
            api_result = self.query_clearbit(company_name)
            if api_result:
                self.save_to_cache(company_name, api_result)
                return api_result['tier']

        # 4. ML estimation (if have job data)
        if jobs_found:
            ml_tier = self.estimate_from_jobs(jobs_found)
            self.save_to_cache(company_name, ml_tier)
            return ml_tier

        # 5. Default to Tier 99
        return 99
```

---

## Dependencies

**Python Packages (if implementing):**
- `requests` (already installed)
- `sqlite3` (built-in)
- Optional: `clearbit` or `linkedin-api`

**API Keys (if implementing):**
- Clearbit API key (optional, $0-$99/month)

---

## Migration Path

**From Manual (Current) → Hybrid (Future):**

1. **Step 1:** Implement caching layer (2-3 hours)
   - SQLite database for persistent storage
   - TTL-based expiration (1 year for API data, 6 months for ML)

2. **Step 2:** Add ML estimation (4-6 hours)
   - Job volume heuristics
   - Test with current 137 companies

3. **Step 3:** Integrate external API (6-8 hours)
   - Clearbit or similar
   - Domain guessing logic
   - Fallback handling

4. **Step 4:** Update AeroComps.py (2-3 hours)
   - Replace `get_company_tier()` calls
   - Add confidence logging
   - Test end-to-end

**Total Effort:** 14-20 hours

---

## Related Documents

- `COMPANY_SIZE_LOOKUP_IMPLEMENTATION.md` - Original technical design
- `EXTERNAL_API_OPTIONS_MINIMAL_COST.md` - API comparison matrix
- `STRATEGY_JOB_CAP_OPTIMIZATION.md` - ML optimization research

---

## Decision Criteria

**When to implement:**
- ✅ Expanding beyond 200 companies
- ✅ Adding companies frequently (weekly)
- ✅ Manual database maintenance becomes burdensome
- ✅ Need real-time data freshness

**When NOT to implement:**
- ❌ Company list is stable (updates < monthly)
- ❌ Tier 99 default is acceptable for unknowns
- ❌ Manual research is feasible (< 50 companies)

---

**Maintained By:** AeroSpace Alley Team
**Last Updated:** October 29, 2025
**Version:** 2.0 (proposal for future implementation)
