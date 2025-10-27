# CRITICAL DISCOVERY: Query Structure Issue

## Problem Identified

You're absolutely correct - the companies DO have jobs. The issue is **HOW we're querying SerpAPI**.

### Current (BROKEN) Approach:
```python
query = "GKN Aerospace Engine Systems machinist OR cnc OR welder OR assembler OR inspector"
```

**Why this fails:**
1. Google Jobs interprets this as:
   - "(GKN Aerospace Engine Systems machinist)" OR "cnc" OR "welder" OR "assembler" OR "inspector"
2. This finds jobs with "cnc" ANYWHERE (not specifically at GKN)
3. Then we filter results to only keep jobs with keywords in title
4. Since the OR terms didn't require GKN, we get generic results that don't pass our filter
5. Result: 0 jobs returned

### Correct Approach (SerpAPI Best Practices):

#### Option 1: Company Name Only
```python
params = {
    "engine": "google_jobs",
    "q": "GKN Aerospace",  # Simple company name
    "api_key": API_KEY
}
```
- Let Google Jobs find ALL jobs at that company
- Filter afterwards for skilled trades

#### Option 2: Company + Single Keyword
```python
params = {
    "engine": "google_jobs",
    "q": "GKN Aerospace machinist",  # One keyword at a time
    "api_key": API_KEY
}
```
- Make multiple API calls per company (one per major keyword)
- More API calls but better results

#### Option 3: Use Location Parameter
```python
params = {
    "engine": "google_jobs",
    "q": "machinist",  # Just the job type
    "location": "Connecticut",  # Filter by location
    "chips": "company:GKN Aerospace",  # Filter by company
    "api_key": API_KEY
}
```
- Uses Google Jobs filters properly
- Most accurate results

## Recommended Fix

### Approach A: Simplest (Use Company Name Only)
```python
def fetch_jobs_for_company(company):
    # Simple query - just company name
    params = {
        "engine": "google_jobs",
        "q": company,  # No keywords in query
        "api_key": API_KEY,
        "hl": "en",
        "start": start
    }

    # Get ALL jobs from company
    # Filter afterwards for skilled trades keywords in title
```

**Pros:**
- ✅ Simplest fix
- ✅ 3 API calls per company (same as current)
- ✅ Finds all jobs, we filter client-side
- ✅ Should work immediately

**Cons:**
- ⚠️ May return non-trades jobs (but we filter them)

### Approach B: Multiple Targeted Queries (More API calls but better results)
```python
def fetch_jobs_for_company(company):
    # Query once per major keyword category
    keywords = ["machinist", "welder", "assembler", "inspector", "technician"]

    for keyword in keywords:
        params = {
            "engine": "google_jobs",
            "q": f"{company} {keyword}",
            "api_key": API_KEY,
            "hl": "en"
        }
        # Make API call for each keyword
```

**Pros:**
- ✅ More targeted results
- ✅ Better coverage of different job types

**Cons:**
- ❌ 5x more API calls (15 per company instead of 3)
- ❌ Would need ~685 API calls for full list

## Current API Status

**Temporary Block:**
- Both API keys returning 403 (Access denied)
- Likely temporary IP rate limiting from 207 rapid requests
- Should clear in 15-30 minutes OR try from different network

**API Usage:**
- Primary: 207 calls made (successful, just wrong query structure)
- Secondary: 0 calls made
- Once unblocked, we can re-test with corrected queries

## Immediate Action Plan

1. **Wait 30 minutes** for rate limit to clear
2. **Update query builder** to use simple company name
3. **Re-test with 1 company** (3 API calls)
4. **Verify jobs are found**
5. **Run full test** if successful

## Code Fix Required

**File:** `AeroComps.py`
**Function:** `build_trade_query()`

**Change:**
```python
# OLD (BROKEN):
def build_trade_query(company_name, keywords, max_length=200):
    clean_name = re.sub(r"[^a-zA-Z0-9&\s]", "", company_name).strip()
    query_parts = []
    for kw in keywords:
        tentative = f"{clean_name} {' OR '.join(query_parts + [kw])}"
        if len(tentative) > max_length:
            break
        query_parts.append(kw)
    return f"{clean_name} " + " OR ".join(query_parts)

# NEW (FIXED):
def build_trade_query(company_name, keywords=None, max_length=200):
    # Simple company name query - let Google find all jobs
    clean_name = re.sub(r"[^a-zA-Z0-9&\s]", "", company_name).strip()
    return clean_name  # That's it!
```

**Note:** We still filter results afterwards, so we'll only keep skilled trades jobs.

---

**Bottom Line:** You were 100% correct - the API isn't the problem, our query structure was. Simple fix: use company name only, filter results afterwards.
