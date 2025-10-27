# SerpAPI Analysis: Is It The Best Choice for Job Discovery?

## What is SerpAPI?

**SerpAPI** is a third-party service that acts as a **proxy/wrapper** for Google Search results. It doesn't have its own job database - it simply:

1. Takes your query
2. Sends it to Google Search (specifically Google Jobs search)
3. Parses the HTML/JSON response from Google
4. Returns structured JSON data to you

**In simple terms:** You're paying SerpAPI to access Google Jobs data in a developer-friendly format.

---

## How Google Jobs Validates Active Listings

### Google's Job Aggregation Process:

**Step 1: Crawling**
- Google's web crawler visits job boards (Indeed, LinkedIn, ZipRecruiter, Glassdoor, etc.)
- Also crawls company career pages that have proper structured data markup (Schema.org JobPosting)
- Frequency: Major job boards crawled daily, smaller sites weekly

**Step 2: Indexing**
- Google extracts job details: title, company, location, salary, description
- Deduplicates jobs (same job posted to multiple boards)
- Adds to Google Jobs index

**Step 3: Validation (Automated)**
- **Freshness check:** Jobs older than 30-60 days may be removed
- **Link validation:** Google checks if "Apply" URLs still work
- **Duplicate detection:** Merges identical jobs from multiple sources
- **Spam filtering:** Removes suspicious/fake postings

**Step 4: Real-Time Verification (Limited)**
- Google does NOT verify with employers in real-time
- Relies on job boards to mark positions as "filled" or expired
- Some listings may be outdated (job filled but posting still live)

### Freshness Issues:

**Common Problems:**
- ❌ Job filled 2 weeks ago but still on Indeed → Still in Google Jobs
- ❌ Company removed posting from career page but Indeed cached it → Still in Google Jobs
- ❌ Staffing agency keeps posting active to build candidate pool → Shows as "active" but not really hiring

**Google's Solution:**
- "Posted X days ago" timestamp
- Links back to original source (user can verify)
- User feedback signals (clicks, applies)

---

## SerpAPI Alternatives for Job Discovery

### Option 1: **SerpAPI** (Current Choice)
**What it is:** Google Jobs data via API wrapper

**Pros:**
- ✅ Aggregates data from 100+ job boards automatically
- ✅ No need to integrate with each board individually
- ✅ Handles deduplication (same job on multiple boards)
- ✅ Simple API, easy to implement
- ✅ No rate limiting issues (they handle it)
- ✅ Location filtering built-in
- ✅ Good for broad discovery across many companies

**Cons:**
- ❌ Limited to what Google has indexed (50-70% coverage for mid-size companies)
- ❌ No direct employer verification (relies on Google's index)
- ❌ Can include outdated listings (filled jobs still showing)
- ❌ Cost: $50/month for 5,000 searches after free tier
- ❌ No salary data for most listings (inconsistent)
- ❌ Misses jobs behind login walls or ATS systems
- ❌ No control over data freshness

**Best for:**
- Quick scans of many companies
- Initial discovery phase
- Companies that post on major job boards

**Cost for your project:**
- 137 companies × 3 pages = 411 searches
- Free tier: 100 searches (covers ~33 companies)
- Paid: Need 2 accounts at 250 each OR 1 paid plan ($50/month)

---

### Option 2: **Direct Job Board APIs** (Indeed, LinkedIn, ZipRecruiter)

#### **Indeed API**
**Status:** ⚠️ **Deprecated** - Indeed shut down public API in 2019

#### **LinkedIn Jobs API**
**What it is:** Direct access to LinkedIn job postings

**Access Requirements:**
- Must be LinkedIn partner (application required)
- Typically granted to recruiting platforms, not individual scrapers
- Cost: Custom pricing (expensive for commercial use)

**Pros:**
- ✅ Direct from source (fresh data)
- ✅ Rich company data (employee count, company page)
- ✅ Salary ranges (when posted)
- ✅ Easy Apply status

**Cons:**
- ❌ LinkedIn only (misses Indeed, ZipRecruiter, etc.)
- ❌ Partner program required (hard to get approved)
- ❌ Expensive
- ❌ Aerospace/manufacturing jobs less common on LinkedIn

#### **ZipRecruiter API**
**What it is:** Direct access to ZipRecruiter postings

**Access Requirements:**
- Partner program required
- Primarily for companies posting jobs, not aggregators

**Pros:**
- ✅ Direct from source
- ✅ Good coverage of skilled trades positions

**Cons:**
- ❌ ZipRecruiter only
- ❌ Limited to what companies post there
- ❌ Partner access required

**Conclusion:** Not practical for your use case (limited access, high cost, single-source)

---

### Option 3: **Adzuna Job Search API** (SerpAPI Alternative)

**What it is:** Job search API aggregating 100+ job boards globally

**Website:** https://www.adzuna.com/

**Pros:**
- ✅ Aggregates multiple job boards (Indeed, Monster, CareerBuilder, etc.)
- ✅ More affordable than SerpAPI ($0.50 per 1,000 searches)
- ✅ Better salary data than SerpAPI
- ✅ Historical data available
- ✅ Location filtering
- ✅ Company filtering

**Cons:**
- ❌ Smaller index than Google (may miss smaller job boards)
- ❌ US coverage not as comprehensive as Google
- ❌ Less aerospace-specific data

**Cost for your project:**
- 411 searches × $0.0005 = **$0.21 total**
- vs SerpAPI: 2 free accounts OR $50/month

**Verdict:** 💰 **Much cheaper** but may have less coverage

---

### Option 4: **RapidAPI Job Search APIs** (Multiple Options)

**Options available:**
- JSearch (Google Jobs wrapper, similar to SerpAPI)
- JScan (Job board aggregator)
- LinkedIn Jobs API (unofficial scraper)

**Pros:**
- ✅ Variety of options
- ✅ Pay-as-you-go pricing
- ✅ Easy to switch between providers

**Cons:**
- ❌ Quality varies widely
- ❌ Some are just scrapers (violate ToS)
- ❌ Less reliable than SerpAPI

---

### Option 5: **Direct Web Scraping** (No API)

**What it is:** Build your own scrapers for each source

**Sources to Scrape:**

#### **A. Job Boards (Easier)**
- **Indeed:** Scrape search results pages
  - URL: `indeed.com/jobs?q=machinist&l=Hartford,CT`
  - Pros: Structured HTML, easy to parse
  - Cons: Rate limiting, CAPTCHA challenges

- **LinkedIn:** Scrape job search
  - URL: `linkedin.com/jobs/search/?keywords=welder`
  - Pros: Rich data
  - Cons: Requires login, aggressive bot detection

- **ZipRecruiter:** Scrape search results
  - Pros: Good skilled trades coverage
  - Cons: CloudFlare protection, harder to scrape

#### **B. Company Career Pages (Medium Difficulty)**
- **ATS-Based Career Pages:**
  - Workday: Used by GKN, Hanwha, many large companies
    - Often has JSON API: `company.wd5.myworkdayjobs.com/api/jobs`
    - Easier to scrape than HTML

  - Taleo (Oracle): Used by Boeing, Lockheed
    - URL pattern: `company.taleo.net/careersection/jobsearch.ftl`
    - Can parse HTML tables

  - iCIMS: Common in aerospace
    - URL pattern: `careers-company.icims.com/jobs`
    - Structured HTML

#### **C. Specialized Aerospace Job Boards (Harder)**
- AerospaceJobsUSA.com
- AviationJobSearch.com
- DefenseJobs.com

**Pros:**
- ✅ **No API costs** (free)
- ✅ Complete control over data
- ✅ Can capture jobs APIs miss
- ✅ Most up-to-date (direct from source)

**Cons:**
- ❌ Time-consuming to build (3-5 days per source)
- ❌ Maintenance required (sites change structure)
- ❌ Rate limiting / IP blocking risks
- ❌ CAPTCHA challenges
- ❌ Legal gray area (violates some ToS)
- ❌ Requires rotating proxies for scale

**Development Time:**
- Basic scraper: 1-2 days per source
- 5 job boards + 10 company careers = 15-30 days development
- Ongoing maintenance: 2-4 hours/month per source

---

## Recommendation Matrix

| Use Case | Best Option | Why |
|----------|-------------|-----|
| **Quick discovery across 137 companies** | SerpAPI | Fast, broad coverage, easy implementation |
| **Budget-constrained (<$10)** | Adzuna | 95% cheaper than SerpAPI |
| **Maximum coverage (API + scraping)** | SerpAPI + selective scraping | API first, scrape gaps |
| **Long-term recurring (weekly scans)** | Direct scraping | No ongoing API costs |
| **High data quality needed** | Company career pages (scraping) | Most accurate, direct from source |
| **Proof of concept (today's demo)** | SerpAPI (current setup) | Already implemented, fast results |

---

## My Recommendation for YOUR Project

### **Short-Term (Today's Demo): Stick with SerpAPI** ✅

**Why:**
1. ✅ Already implemented and tested
2. ✅ Will find jobs from tier-1 companies (GKN, Barnes, Hanwha)
3. ✅ You have 70 API calls remaining (enough for 3-company test)
4. ✅ Fastest path to demo-ready results
5. ✅ Good enough for proof-of-concept

**Action:** Test 3 tier-1 companies, see what we find

---

### **Medium-Term (After Demo): Hybrid Approach** ⭐ RECOMMENDED

**Phase 1: Use SerpAPI for broad discovery**
- Run full 137-company scan with both API keys (411 calls)
- Identify which companies have jobs vs. don't

**Phase 2: Analyze gaps**
- Companies with 0 results but known to be hiring → Scrape their career pages
- Example: If GKN shows 0 jobs via API, check careers.gkn.com directly

**Phase 3: Targeted scraping**
- Build scrapers for top 10-15 companies with most jobs
- Focus on Workday-based sites (easiest to scrape)
- Supplement API data with direct career page data

**Benefits:**
- ✅ 70-90% coverage from API (fast, cheap)
- ✅ 10-30% gap filled by scraping (high value targets)
- ✅ Best of both worlds

---

### **Long-Term (Recurring Production): Consider Scraping** 💡

**If you plan to run this weekly/monthly:**

**Cost Analysis:**
- SerpAPI: $50/month for 5,000 searches = $600/year
- Direct scraping: 40 hours development × $100/hr = $4,000 one-time + $200/year maintenance

**Break-even:** 8 months

**When scraping makes sense:**
- You'll run this >10 times over 2 years
- You need data from specific companies API doesn't cover well
- You want to build proprietary database

---

## How to Validate Job Listing Freshness

**Regardless of data source, always:**

1. **Check "Posted Date"**
   - Only show jobs posted in last 30 days
   - Flag jobs >45 days as "possibly filled"

2. **Verify Apply URL**
   - Test if link still works (HTTP 200 response)
   - If 404, mark job as expired

3. **Add "Last Verified" Timestamp**
   - Track when you last saw each job
   - If job disappears from results, mark as "removed"

4. **User Feedback Loop**
   - Let users report "job no longer available"
   - Build database of filled positions

5. **Direct Verification (Manual for now)**
   - For high-priority jobs, call company to verify
   - Or visit career page directly

---

## Bottom Line for Your Decision

### **For Today (Testing/Demo):**
✅ **Use SerpAPI** - Test 3 tier-1 companies (9 API calls)

### **For Production (After Demo):**
🎯 **Hybrid Approach** - SerpAPI for broad coverage + targeted scraping for gaps

### **For Long-Term Recurring:**
💡 **Evaluate based on results** - If API finds >200 jobs, keep using it. If <50 jobs, consider scraping.

---

## Next Step: 3-Company Test

**I recommend testing these 3 TIER-1 companies (9 API calls):**

1. **GKN Aerospace Engine Systems** - Large supplier, definitely hiring
2. **Hanwha Aerospace USA** - Growing company, active hiring
3. **Barnes Aerospace East Granby** - Major player, consistent openings

**Expected outcome:**
- If we find **50+ jobs:** SerpAPI is working well, proceed with full run
- If we find **10-50 jobs:** SerpAPI is okay, consider supplementing with scraping
- If we find **<10 jobs:** SerpAPI may not be ideal for your company list, pivot to scraping

**Ready to run this test?**
