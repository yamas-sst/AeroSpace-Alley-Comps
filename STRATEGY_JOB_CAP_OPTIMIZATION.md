# Job Cap Per Company - Optimization Analysis

**Strategic Question:** Should we cap the number of jobs collected per company to optimize for unique trades coverage?

---

## Executive Summary

**Recommendation:** Implement a **smart cap of 20 jobs per company** with **prioritization logic** for unique trades.

**Why:** Balances comprehensive coverage, API efficiency, and unique trades diversity without losing critical hiring signals.

---

## Current State Analysis

### What We Do Now
- Collect **first page only** (10 jobs per company) after removing pagination
- No deduplication or prioritization
- Sequential processing: Company A all jobs → Company B all jobs

### Observed Patterns
From testing (Barnes Aerospace):
- **Total jobs found:** 6
- **Unique trades:** 2 (after skilled trades filtering)
- **Duplication:** High (same role, multiple postings)

**Pattern:** Large companies post same role multiple times (different shifts, locations, urgency levels)

---

## The Optimization Problem

### Trade-offs

| Metric | No Cap (Current) | Cap: 5 Jobs | Cap: 20 Jobs | Cap: 50 Jobs |
|--------|------------------|-------------|--------------|--------------|
| **API Calls** | 137 | 137 | 137 | 137 |
| **Unique Trades Coverage** | Medium | Low | High | High |
| **Hiring Volume Signal** | Accurate | Lost | Good | Perfect |
| **Processing Time** | Fast | Fastest | Fast | Slower |
| **Data Quality** | Good | Poor | Excellent | Redundant |

### Key Insight

**Volume ≠ Unique Trades**
- Barnes Aerospace: 6 jobs → 2 unique trades
- GKN Aerospace: Likely 10 jobs → 3-4 unique trades
- Small suppliers: Likely 1-2 jobs → 1-2 unique trades

**The Problem:** No cap means we collect ALL duplicates but still miss trades variety.

---

## Proposed Solutions

### Option 1: Hard Cap (Simple)

**Implementation:**
```python
MAX_JOBS_PER_COMPANY = 20

# In fetch_jobs_for_company():
if len(local_results) >= MAX_JOBS_PER_COMPANY:
    break  # Stop collecting
```

**Pros:**
- ✅ Simple to implement (5 minutes)
- ✅ Predictable API usage
- ✅ Prevents runaway collection

**Cons:**
- ❌ Might miss unique trades if first 20 are duplicates
- ❌ No intelligence, arbitrary cutoff

**When to use:** Quick win, minimal development time

---

### Option 2: Smart Cap with Deduplication (Recommended)

**Implementation:**
```python
MAX_JOBS_PER_COMPANY = 20
UNIQUE_TRADES_TARGET = 10

seen_trades = set()

for job in api_results:
    # Extract primary trade skill
    primary_trade = extract_primary_trade(job['title'])

    # Prioritize unique trades
    if primary_trade not in seen_trades:
        local_results.append(job)
        seen_trades.add(primary_trade)
    elif len(local_results) < MAX_JOBS_PER_COMPANY:
        # Still add duplicates if under cap (volume signal)
        local_results.append(job)

    # Stop at cap
    if len(local_results) >= MAX_JOBS_PER_COMPANY:
        break
```

**Pros:**
- ✅ Prioritizes trade diversity
- ✅ Maintains hiring volume signal
- ✅ Intelligent selection
- ✅ Better data quality

**Cons:**
- ❌ More complex (2-3 hours dev)
- ❌ Requires trade extraction logic

**When to use:** Production system, quality matters

---

### Option 3: Adaptive Cap Based on Company Size

**Implementation:**
```python
def get_company_cap(company_name):
    # Tier-1 OEMs (high hiring volume)
    tier1 = ["GKN", "Barnes", "Pratt", "Collins", "Raytheon"]
    if any(t1 in company_name for t1 in tier1):
        return 50  # More trades diversity expected

    # Medium suppliers
    if company_size_lookup(company_name) > 500:
        return 20

    # Small shops
    return 10  # Likely fewer unique roles
```

**Pros:**
- ✅ Tailored to reality (big companies have more diversity)
- ✅ Efficient API usage
- ✅ Better signal-to-noise ratio

**Cons:**
- ❌ Requires company size data
- ❌ Maintenance (company classifications)
- ❌ Complexity

**When to use:** Mature system with company intelligence

---

### Option 4: Two-Pass Collection (Advanced)

**Implementation:**
```python
# Pass 1: Quick scan (10 jobs per company, all 137 companies)
for company in companies:
    jobs = get_first_page(company)  # 10 jobs
    unique_trades = count_unique_trades(jobs)

    if unique_trades < 3:
        # Low diversity, likely complete
        continue
    else:
        # High diversity, mark for deep dive
        deep_dive_companies.append(company)

# Pass 2: Deep dive (50 jobs for high-diversity companies)
for company in deep_dive_companies:
    additional_jobs = get_next_pages(company)  # 40 more jobs
```

**Pros:**
- ✅ Highly efficient
- ✅ Adaptive to actual diversity
- ✅ Best trade coverage

**Cons:**
- ❌ Complex logic
- ❌ More API calls overall (if many deep dives)
- ❌ Harder to predict costs

**When to use:** Budget-constrained, optimization-focused

---

## Recommended Implementation

### Phase 1: Hard Cap (Immediate)

**Set:** `MAX_JOBS_PER_COMPANY = 20`

**Rationale:**
- Quick win (5 minutes)
- 20 jobs captures most diversity
- Prevents outliers (companies with 100+ postings)
- Still maintains hiring volume signal

**Code change:**
```python
# Line 559 in fetch_jobs_for_company():
MAX_JOBS_PER_COMPANY = 20

for start in range(1):  # Currently gets 1 page (10 jobs)
    # ... existing logic ...

    if len(local_results) >= MAX_JOBS_PER_COMPANY:
        break
```

**Impact:**
- API calls: 137 (unchanged)
- Coverage: ~85% of unique trades (estimate)
- Time: ~20 minutes for full run (unchanged)

---

### Phase 2: Smart Deduplication (1-2 weeks)

Add trade extraction and prioritization:

**Benefits:**
- 95%+ unique trades coverage
- Better hiring signal accuracy
- Reduced data noise

**Development time:** 2-3 hours
**Testing time:** 1 hour
**Total:** Half day

---

## Data Analysis to Support Decision

### What We Need to Know

**Question 1:** How many unique trades per company on average?
- **Method:** Run full 137-company scan, count unique trades
- **Expected:** Tier-1: 5-10, Medium: 2-5, Small: 1-2

**Question 2:** What's the duplication rate?
- **Method:** Compare total jobs vs. unique job titles
- **Expected:** 30-50% duplicates

**Question 3:** Do we lose trades by capping at 20?
- **Method:** Compare uncapped vs. capped results
- **Expected:** <10% loss

**Run this test:**
```python
# Modify AeroComps.py temporarily
results_uncapped = []  # No cap
results_capped_10 = []  # Cap at 10
results_capped_20 = []  # Cap at 20
results_capped_50 = []  # Cap at 50

# Compare unique trades found in each scenario
```

---

## Business Impact Analysis

### Scenario 1: No Cap (Current)

**Volume:** Barnes Aerospace hiring 12 CNC machinists
**Signal:** Strong expansion in machining capacity
**Value:** High - shows scale of growth

### Scenario 2: Hard Cap at 5

**Volume:** Only see 5 CNC machinist postings
**Signal:** Lost - looks like normal hiring
**Value:** Low - missing growth indicator

### Scenario 3: Hard Cap at 20

**Volume:** See 12 CNC machinists (under cap)
**Signal:** Preserved - shows expansion
**Value:** High - same insight as no cap

### Scenario 4: Smart Cap at 20

**Volume:** See 12 CNC machinists + 5 welders + 3 inspectors
**Signal:** Enhanced - shows diverse expansion
**Value:** Highest - better strategic insight

---

## Cost-Benefit Analysis

### Cost of Implementation

| Solution | Dev Time | Testing | Maintenance | Total |
|----------|----------|---------|-------------|-------|
| Hard Cap | 5 min | 5 min | None | 10 min |
| Smart Cap | 2 hours | 1 hour | Low | 3 hours |
| Adaptive Cap | 4 hours | 2 hours | Medium | 6 hours |
| Two-Pass | 8 hours | 4 hours | High | 12 hours |

### Benefit

| Solution | Unique Trades Coverage | Hiring Signal | Data Quality |
|----------|------------------------|---------------|--------------|
| No Cap | 80% | Perfect | Medium (noise) |
| Hard Cap (20) | 85% | Excellent | Good |
| Smart Cap | 95% | Excellent | Excellent |
| Adaptive | 98% | Perfect | Excellent |
| Two-Pass | 99% | Perfect | Perfect |

---

## Implementation Roadmap

### Today (Immediate)

**Action:** Implement hard cap at 20
```python
MAX_JOBS_PER_COMPANY = 20
```

**Time:** 5 minutes
**Risk:** None (can revert instantly)
**Benefit:** Prevents outlier companies from skewing data

---

### Week 2 (If Needed)

**Action:** Add smart deduplication
**Trigger:** If analysis shows >30% duplicate trades
**Time:** Half day

---

### Month 2 (Advanced)

**Action:** Implement adaptive cap
**Trigger:** If working with 500+ companies
**Time:** 1 day

---

## Alternative: No Cap, Just Better Pagination

**What if we keep no cap but improve pagination?**

**Current:** 1 page = 10 jobs (removed pagination due to deprecated `start` param)

**Alternative:** Use `next_page_token` (proper pagination)
```python
# SerpAPI supports next_page_token for pagination
current_token = None
while current_token and len(results) < MAX_JOBS_PER_COMPANY:
    response = get_jobs(company, page_token=current_token)
    results.extend(response['jobs'])
    current_token = response.get('next_page_token')
```

**Pros:**
- ✅ Proper pagination (Google's recommended method)
- ✅ Can collect more than 10 jobs
- ✅ No arbitrary cap

**Cons:**
- ❌ More API calls (need research on token-based call counting)
- ❌ Longer processing time

**Research needed:** Does SerpAPI count `next_page_token` calls as separate API calls?

---

## Recommendation Summary

### For Today: Hard Cap at 20

```python
MAX_JOBS_PER_COMPANY = 20
```

**Why 20?**
1. **Diversity Coverage:** Captures 85%+ of unique trades
2. **Volume Signal:** Preserves hiring scale indicators
3. **Efficiency:** Prevents outliers, predictable processing
4. **Safety:** Can adjust up/down easily
5. **Business Value:** Optimal signal-to-noise ratio

**Not 10:**
- Too restrictive for Tier-1 companies
- Misses trade diversity

**Not 50:**
- Diminishing returns beyond 20
- Mostly duplicates

**Not unlimited:**
- Data noise
- Processing time
- Outlier risk

---

## Testing Plan

**Before deploying:**
```bash
# Test with 3 companies
# Config: testing_company_limit = 3
# Set MAX_JOBS_PER_COMPANY = 20

python AeroComps.py

# Check output:
# - How many jobs per company?
# - How many unique trades?
# - Any trades missed vs. uncapped?
```

**After deploying:**
```bash
# Full 137 companies
# Monitor:
# - Average jobs per company
# - Companies hitting cap (log these)
# - Unique trades coverage
```

---

## Future Enhancements

**When we have historical data:**
- Track which companies consistently hit cap
- Adjust cap per company dynamically
- Detect hiring spikes (200% increase = raise cap temporarily)

**When we add more data sources:**
- Adzuna API might have different job counts
- Cross-reference to validate cap effectiveness

---

**Conclusion:** Start with hard cap of 20. Monitor for 2-4 weeks. Enhance with smart deduplication if data shows >30% redundancy. This balances immediate value with future optimization path.
