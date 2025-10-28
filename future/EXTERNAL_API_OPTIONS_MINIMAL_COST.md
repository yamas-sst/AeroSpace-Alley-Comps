# Option C: External API for Company Size Lookup

**Goal:** Automated company data retrieval with **MINIMAL or NO COST**

**Status:** Future implementation - NOT ACTIVE

---

## Overview

External APIs can provide real-time company data (employee counts, industry, location) without manual maintenance. This analysis focuses on **free and low-cost options** suitable for a bootstrap operation.

---

## Option C1: LinkedIn Company Search (FREE - Manual Scraping Alternative)

### Approach: LinkedIn Company Pages via Web Search

**How it works:**
1. For each company, construct search query: `"[Company Name] Connecticut site:linkedin.com/company"`
2. Parse LinkedIn company page to extract employee count range
3. Cache results to avoid repeated lookups

**Implementation:**
```python
import requests
from bs4 import BeautifulSoup
import re
import time

def get_linkedin_employee_count(company_name):
    """
    Estimate employee count from LinkedIn company page.

    IMPORTANT: This is scraping public data, not using LinkedIn API.
    Respect rate limits and LinkedIn's ToS.

    Returns:
        int: Estimated employee count
    """
    # Search Google for LinkedIn company page
    search_query = f"{company_name} Connecticut site:linkedin.com/company"
    google_url = f"https://www.google.com/search?q={search_query}"

    try:
        # Get search results (need to handle anti-bot measures)
        response = requests.get(google_url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })

        # Parse to find LinkedIn URL
        soup = BeautifulSoup(response.text, 'html.parser')
        linkedin_url = None

        for link in soup.find_all('a'):
            href = link.get('href', '')
            if 'linkedin.com/company/' in href:
                linkedin_url = href
                break

        if not linkedin_url:
            return 50  # Default if not found

        # Visit LinkedIn company page
        time.sleep(2)  # Rate limiting
        response = requests.get(linkedin_url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })

        # Extract employee count from page
        # LinkedIn shows ranges like "201-500 employees"
        employee_match = re.search(r'(\d{1,3}[,\d]*)\s*[-–]\s*(\d{1,3}[,\d]*)\s*employees', response.text)

        if employee_match:
            # Take midpoint of range
            low = int(employee_match.group(1).replace(',', ''))
            high = int(employee_match.group(2).replace(',', ''))
            return (low + high) // 2

        return 50  # Default

    except Exception as e:
        print(f"Error fetching LinkedIn data for {company_name}: {e}")
        return 50  # Default on error

# Cache results to avoid repeated lookups
COMPANY_SIZE_CACHE = {}

def cached_company_lookup(company_name):
    """Lookup with caching to minimize API/scraping calls."""
    if company_name in COMPANY_SIZE_CACHE:
        return COMPANY_SIZE_CACHE[company_name]

    employee_count = get_linkedin_employee_count(company_name)
    COMPANY_SIZE_CACHE[company_name] = employee_count

    return employee_count
```

**Pros:**
- ✅ **FREE** - No API costs
- ✅ Real-time data from LinkedIn
- ✅ LinkedIn data is generally accurate

**Cons:**
- ❌ Scraping may violate LinkedIn ToS
- ❌ Fragile (breaks if LinkedIn changes HTML)
- ❌ Slow (need rate limiting to avoid blocks)
- ❌ Not reliable for production

**Verdict:** ⚠️ Use with caution - only for initial data collection, not production

---

## Option C2: Clearbit Free Tier (FREEMIUM)

### Clearbit Company Enrichment API

**Pricing:**
- **Free tier:** 50 requests/month
- **Growth tier:** $99/month for 2,500 requests
- **Pro tier:** $249/month for 10,000 requests

**How it works:**
```python
import requests

CLEARBIT_API_KEY = "your_key_here"

def clearbit_lookup(company_name):
    """
    Look up company data via Clearbit Enrichment API.

    Free tier: 50 lookups/month
    """
    # Need company domain, not just name
    # First, get domain from company name (could use another service)
    domain = guess_domain(company_name)  # e.g., "barnes aerospace" → "barnesaerospace.com"

    url = f"https://company.clearbit.com/v2/companies/find?domain={domain}"

    headers = {
        "Authorization": f"Bearer {CLEARBIT_API_KEY}"
    }

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            employees = data.get('metrics', {}).get('employees', 50)
            return employees
        else:
            return 50  # Default

    except Exception as e:
        print(f"Clearbit error for {company_name}: {e}")
        return 50

def guess_domain(company_name):
    """
    Guess company domain from name.

    Example:
        "Barnes Aerospace" → "barnesaerospace.com"
        "Pratt & Whitney" → "pratt-whitney.com"
    """
    # Remove special chars, lowercase, add .com
    domain = company_name.lower()
    domain = re.sub(r'[^a-z0-9\s]', '', domain)  # Remove special chars
    domain = domain.replace(' ', '')  # Remove spaces
    domain = f"{domain}.com"
    return domain
```

**Pros:**
- ✅ High-quality data
- ✅ Simple API
- ✅ 50 free lookups/month (enough for testing)

**Cons:**
- ❌ Requires company domain (not always known)
- ❌ Free tier too limited (137 companies = need paid tier)
- ❌ $99/month ongoing cost

**Verdict:** 💰 Good for testing, too expensive for production at this scale

---

## Option C3: OpenCorporates API (FREE with rate limits)

### World's largest open database of companies

**Pricing:**
- **Free tier:** 500 requests/day (with API key)
- **No free tier:** 50 requests/day (without API key)
- **Paid tier:** $150/month for unlimited

**How it works:**
```python
import requests

OPENCORPORATES_API_KEY = "your_key_here"  # Optional, increases rate limit

def opencorporates_lookup(company_name, state="ct"):
    """
    Look up company via OpenCorporates API.

    Free tier: 500 requests/day with API key
    """
    url = f"https://api.opencorporates.com/v0.4/companies/search"

    params = {
        "q": company_name,
        "jurisdiction_code": f"us_{state}",  # "us_ct" for Connecticut
        "api_token": OPENCORPORATES_API_KEY  # Optional
    }

    try:
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            companies = data.get('results', {}).get('companies', [])

            if companies:
                # OpenCorporates doesn't always have employee count
                # But has other useful data (address, status, registration)
                company = companies[0]['company']

                # Try to extract employee count if available
                # (Not always present in OpenCorporates)
                return 50  # Default for now

        return 50

    except Exception as e:
        print(f"OpenCorporates error for {company_name}: {e}")
        return 50
```

**Pros:**
- ✅ **FREE** for 500 requests/day
- ✅ Legal, official company data
- ✅ Good for verifying company exists

**Cons:**
- ❌ Often doesn't have employee count data
- ❌ More useful for legal/registration info than headcount

**Verdict:** 🟡 Good for company validation, not ideal for employee counts

---

## Option C4: Google Custom Search API (FREEMIUM)

### Automated Google searches for company data

**Pricing:**
- **Free tier:** 100 searches/day
- **Paid tier:** $5 per 1,000 additional queries (up to 10,000/day max)

**How it works:**
```python
import requests

GOOGLE_API_KEY = "your_key_here"
GOOGLE_CSE_ID = "your_custom_search_engine_id"

def google_search_employee_count(company_name):
    """
    Use Google Custom Search to find employee count.

    Searches for: "[Company Name] Connecticut employees"
    Then parses results for numbers.
    """
    url = "https://www.googleapis.com/customsearch/v1"

    params = {
        "key": GOOGLE_API_KEY,
        "cx": GOOGLE_CSE_ID,
        "q": f"{company_name} Connecticut employees"
    }

    try:
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            items = data.get('items', [])

            # Parse snippets for employee counts
            for item in items:
                snippet = item.get('snippet', '')

                # Look for patterns like "500 employees" or "employs 500"
                match = re.search(r'(\d{1,5})\s*employees', snippet)
                if match:
                    return int(match.group(1))

        return 50  # Default

    except Exception as e:
        print(f"Google search error for {company_name}: {e}")
        return 50
```

**Pros:**
- ✅ 100 free searches/day (enough for daily runs)
- ✅ Flexible - can search any data
- ✅ Cheap scaling ($5 per 1,000 additional)

**Cons:**
- ❌ Requires parsing unstructured data
- ❌ Not always accurate
- ❌ Need to set up Custom Search Engine

**Verdict:** 🟢 Good free option with flexible scaling

---

## Option C5: Hunter.io Company API (FREEMIUM)

### Email domain data enrichment

**Pricing:**
- **Free tier:** 50 searches/month
- **Starter:** $49/month for 1,000 searches
- **Growth:** $99/month for 5,000 searches

**How it works:**
```python
import requests

HUNTER_API_KEY = "your_key_here"

def hunter_lookup(company_domain):
    """
    Look up company via Hunter.io.

    Provides employee count estimates.
    """
    url = f"https://api.hunter.io/v2/domain-search"

    params = {
        "domain": company_domain,
        "api_key": HUNTER_API_KEY
    }

    try:
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()

            # Hunter provides "company_size" field
            company_size = data.get('data', {}).get('organization', {}).get('company_size', 50)
            return company_size

        return 50

    except Exception as e:
        print(f"Hunter error for {company_domain}: {e}")
        return 50
```

**Pros:**
- ✅ Includes employee count data
- ✅ High accuracy for established companies

**Cons:**
- ❌ Only 50 free searches/month
- ❌ Needs company domain

**Verdict:** 🟡 Good data, but free tier too limited

---

## RECOMMENDED SOLUTION: Hybrid Approach (FREE)

### Strategy: Combine multiple free tiers

**Implementation:**
```python
def hybrid_company_lookup(company_name):
    """
    Try multiple free APIs in order until one succeeds.

    1. Check static database first (Option A - instant, no API call)
    2. Try Google Custom Search (100/day free)
    3. Try OpenCorporates (500/day free)
    4. Fall back to default (50 employees)
    """
    # Step 1: Static database (from Option A)
    static_result = COMPANY_SIZE_DATABASE.get(company_name)
    if static_result:
        return static_result["employees"]

    # Step 2: Google Custom Search (if under daily limit)
    if google_api_calls_today < 100:
        result = google_search_employee_count(company_name)
        if result != 50:  # Found something
            # Cache it for future use
            COMPANY_SIZE_DATABASE[company_name] = {"employees": result, "tier": calculate_tier(result)}
            return result

    # Step 3: OpenCorporates (if under daily limit)
    if opencorporates_calls_today < 500:
        result = opencorporates_lookup(company_name)
        if result != 50:
            COMPANY_SIZE_DATABASE[company_name] = {"employees": result, "tier": calculate_tier(result)}
            return result

    # Step 4: Default fallback
    return 50
```

**Benefits:**
- ✅ **ZERO COST** (all free tiers)
- ✅ 100+ companies/day capacity (Google: 100, OpenCorporates: 500)
- ✅ Automatic fallback if APIs fail
- ✅ Builds static database over time (cached results)

**Limitations:**
- 137 companies would take 2 days (day 1: 100 companies, day 2: 37 companies)
- Or run once manually and save results for future use

---

## Implementation Roadmap

### Phase 1: Static Database (NOW)
- Use pre-populated COMPANY_SIZE_DATABASE from Option A
- **Cost:** $0
- **Maintenance:** Quarterly manual updates
- **Coverage:** ~60-70 major companies

### Phase 2: Google Custom Search (1 MONTH)
- Add Google CSE for unknown companies
- **Cost:** $0 (under 100/day limit)
- **Setup time:** 2 hours (create CSE, get API key)
- **Coverage:** 100% automated for new companies

### Phase 3: Caching Layer (2 MONTHS)
- Save all lookups to JSON file
- Build comprehensive database over time
- **Cost:** $0
- **Benefit:** Reduces API calls to near-zero after initial run

### Phase 4: Optional Paid Upgrade (6 MONTHS+)
- If business scales and budget allows
- Consider Clearbit ($99/mo) or Hunter.io ($49/mo)
- **Only if:** Processing 1,000+ companies regularly

---

## Code Example: Complete Free Solution

```python
import json
import os

CACHE_FILE = "resources/company_size_cache.json"

def load_cache():
    """Load cached company sizes from file."""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_cache(cache):
    """Save company size cache to file."""
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f, indent=2)

def get_company_size_free(company_name):
    """
    Get company size using only FREE methods.

    Order of operations:
    1. Check cache file
    2. Check static database
    3. Try Google Custom Search (100/day free)
    4. Default to 50
    """
    # Load cache
    cache = load_cache()

    # Check cache first
    if company_name in cache:
        return cache[company_name]

    # Check static database
    if company_name in COMPANY_SIZE_DATABASE:
        size = COMPANY_SIZE_DATABASE[company_name]["employees"]
        cache[company_name] = size
        save_cache(cache)
        return size

    # Try Google Custom Search (if available)
    size = google_search_employee_count(company_name)

    # Cache the result
    cache[company_name] = size
    save_cache(cache)

    return size
```

**Usage:**
```python
# First time: might use Google API
size1 = get_company_size_free("Barnes Aerospace")  # → 1200 (from Google)

# Second time: instant from cache
size2 = get_company_size_free("Barnes Aerospace")  # → 1200 (from cache file)

# Unknown company: default
size3 = get_company_size_free("Unknown Aerospace Inc")  # → 50 (default)
```

---

## Conclusion: Best Minimal-Cost Approach

**Recommended:** Hybrid static database + Google Custom Search + caching

**Total cost:** **$0/month**

**Capabilities:**
- 100 automated lookups/day (Google free tier)
- Unlimited cached lookups (instant, free)
- 60-70 major companies pre-populated
- Automatic learning (builds database over time)

**Implementation effort:** 4-6 hours one-time setup

**Maintenance:** ~30 minutes quarterly (review cache, update static data)

---

## Next Steps

1. **Immediate:** Use Option A static database (no API needed)
2. **Week 2-3:** Set up Google Custom Search API (free tier)
3. **Month 1:** Add caching layer to minimize API calls
4. **Month 2-3:** Evaluate if paid APIs needed (likely not)

**When to consider paid APIs:**
- Processing 500+ companies regularly
- Need real-time updates (not batch processing)
- Revenue justifies $50-100/month expense
