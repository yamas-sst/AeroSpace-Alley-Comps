# OPTIMIZED TESTING STRATEGY - API Budget Analysis

## Current API Budget Status
- **Primary-Yamas:** 70 calls remaining (180 used / 250 limit)
- **Secondary-Zac:** 250 calls available (RESERVED for production)
- **Testing Budget:** 70 calls ONLY

---

## Option B Analysis: Companies 21-50

### Original Plan (NOT FEASIBLE):
- 30 companies (rows 21-50)
- 3 pages per company
- **Total: 90 API calls** ❌ OVER BUDGET by 20 calls

### SMART ALTERNATIVE: Cherry-Pick Top Companies

I analyzed rows 21-137 and identified the **TOP TIER-1 & TIER-2 aerospace companies** most likely to have active job postings:

#### Tier-1 Companies (Guaranteed Jobs):
1. **GKN Aerospace Engine Systems** (Row 55)
2. **GKN Aerospace Structures Corp.** (Row 56)
3. **Barnes Aerospace East Granby** (Row 21)
4. **Barnes Aerospace Windsor Division** (Row 22)
5. **Hanwha Aerospace USA** (Row 59)
6. **Hanwha Aerospace USA, East Windsor** (Row 60)
7. **Hanwha Aerospace USA, Glastonbury** (Row 61)
8. **Hanwha Aerospace USA, Newington** (Row 62)
9. **HEICO / Turbine Kinetics** (Row 64)
10. **Triumph Systems, Electronics & Controls, West Hartford** (Row 124)
11. **Triumph Systems, Electronics & Controls, Windsor** (Row 125)

#### Tier-2 Companies (High Probability):
12. **Chromalloy Connecticut** (Row 35)
13. **Curtis-Wright Surface Technologies** (Row 42)
14. **Siemens Industry Inc** (Row 116)
15. **Kinetic Engine Systems** (multiple divisions - Rows 76-81)

---

## RECOMMENDED TESTING APPROACH

### **Scenario A: Conservative (15 companies)**
- 15 top companies × 3 pages = **45 API calls**
- **Budget remaining:** 25 calls (safety buffer)
- **Companies:** All Tier-1 companies listed above
- **Expected outcome:** High probability of finding 50-200+ jobs

### **Scenario B: Aggressive (20 companies)** ⭐ RECOMMENDED
- 20 companies (Tier-1 + select Tier-2) × 3 pages = **60 API calls**
- **Budget remaining:** 10 calls (minimal buffer)
- **Companies:** All Tier-1 + top 5 Tier-2
- **Expected outcome:** Very high probability of 100-300+ jobs

### **Scenario C: Maximum Coverage (23 companies)**
- 23 companies × 3 pages = **69 API calls**
- **Budget remaining:** 1 call (no buffer)
- **Companies:** All companies above
- **Expected outcome:** Maximum job discovery within budget

---

## LOCATION FILTERING STRATEGY

### Current Company List Analysis
Your Excel file has these columns:
- Company Name
- **Address Info** ← Contains location data
- Website
- Coordinates

### Proposed Location Filtering Features:

#### **Feature 1: Use Company Address from Excel**
```python
# Read location from "Address Info" column
# Extract city, state for each company
# Add to API query: "Boeing Hartford CT" instead of just "Boeing"
```
**Benefit:** More geographically relevant results

#### **Feature 2: US-Only Override**
```python
# Add to config.json:
"location_filter": {
  "enabled": true,
  "countries": ["United States"],
  "exclude_international": true
}
```
**Benefit:** Filters out international job postings

#### **Feature 3: State-Level Filtering**
```python
# Add to config.json:
"location_filter": {
  "enabled": true,
  "states": ["CT", "MA", "RI", "NY"],  # New England + NY
  "radius_miles": 50  # Jobs within 50 miles of company HQ
}
```
**Benefit:** Highly targeted local results

---

## API EFFECTIVENESS ANALYSIS

### Why SerpAPI (Google Jobs) May Miss Some Postings:

#### **What Google Jobs API DOES Find:**
✅ Jobs posted on major job boards (Indeed, LinkedIn, ZipRecruiter, Glassdoor)
✅ Jobs posted on company career pages WITH structured data (Schema.org markup)
✅ Jobs aggregated by Google's crawler
✅ Recent postings (typically last 30-60 days)

#### **What Google Jobs API OFTEN MISSES:**
❌ Company career pages WITHOUT structured data
❌ Jobs behind login walls or ATS systems
❌ Jobs on specialized aerospace job boards (e.g., AerospaceJobsUSA)
❌ Internal referral-only positions
❌ Contract/temp positions on staffing agency sites

### Estimated Coverage:
- **Large companies (Boeing, Lockheed, etc.):** 70-90% coverage
- **Mid-size aerospace suppliers (GKN, Barnes):** 50-70% coverage
- **Small manufacturers (A-1 Machining, etc.):** 10-30% coverage

---

## DIRECT CAREER PAGE SCRAPING STRATEGY

### When to Use Direct Scraping:
1. **After API test:** If API finds <50 jobs from 20 companies
2. **For specific companies:** Those with 0 results but known to be hiring
3. **For completeness:** Capture jobs missed by Google indexing

### Scraping Approach: Two-Tier Strategy

#### **Tier 1: Structured Career Pages (Easy to Scrape)**
Many aerospace companies use standard ATS platforms:

**Common ATS Platforms:**
- **Workday:** GKN, Hanwha, many large companies
- **Taleo (Oracle):** Used by Boeing, Lockheed, etc.
- **iCIMS:** Common in aerospace/defense
- **Greenhouse/Lever:** Tech-forward companies

**Scraping Method:**
```python
# Example: Workday-based career pages
# URL pattern: company.com/careers/jobs
# Typically has JSON API: company.com/careers/api/jobs
# Can extract: Job title, location, date posted, apply URL

# Example: Taleo-based career pages
# URL pattern: company.taleo.net/careersection/jobsearch.ftl
# Can parse HTML tables or use hidden JSON endpoints
```

**Pros:**
- ✅ Standardized structure (one scraper handles many companies)
- ✅ Often has JSON APIs (easy to parse)
- ✅ High reliability

**Cons:**
- ⚠️ May require JavaScript rendering (Selenium/Playwright)
- ⚠️ Rate limiting on career pages
- ⚠️ Some require CAPTCHA solving

#### **Tier 2: Custom Career Pages (More Complex)**
Some companies have fully custom career pages:

**Scraping Method:**
```python
# For each company:
# 1. Visit website from Excel "Website" column
# 2. Find career page link (usually /careers, /jobs, /opportunities)
# 3. Identify job listing structure (varies per company)
# 4. Extract relevant jobs (skilled trades keywords)
# 5. Store results with source URL
```

**Pros:**
- ✅ Captures jobs not on job boards
- ✅ Direct from source (most up-to-date)

**Cons:**
- ❌ Requires custom scraper per company
- ❌ Time-consuming to develop
- ❌ Breaks when companies redesign sites
- ❌ Legal/ethical considerations (respect robots.txt)

### Recommended Hybrid Approach:

**Phase 1: API First (Current)**
- Use SerpAPI to quickly scan all companies
- Low cost, fast, standardized data

**Phase 2: Targeted Scraping (If Needed)**
- Identify companies with 0 API results but known hiring
- Manually check their career pages
- Build scrapers for top 10-15 companies only

**Phase 3: Automated Scraping (Future)**
- Build ATS-specific scrapers (Workday, Taleo, iCIMS)
- Schedule weekly runs
- Maintain database of job postings over time

---

## PROPOSED NEXT STEPS

### Immediate (Next 10 Minutes):
1. ✅ I'll update config to test 20 companies (Scenario B)
2. ✅ Add basic US-only location filtering
3. ✅ Run optimized test (60 API calls)
4. ✅ Generate output files for your review

### After Test Results (Phase B Planning):
1. 📊 Analyze which companies had jobs vs. didn't
2. 🔍 Manually check career pages for companies with 0 results
3. 🛠️ Design scraper strategy based on findings
4. 📋 Present comprehensive Phase B implementation plan

---

## YOUR APPROVAL NEEDED

**I recommend Scenario B: Test 20 Tier-1 companies (60 API calls)**

This will:
- ✅ Stay within Primary API budget (10 calls buffer)
- ✅ Target companies most likely to have jobs
- ✅ Generate actual output files for demo
- ✅ Preserve Secondary API for production run

**Companies to test (20 companies, 60 API calls):**
1. Barnes Aerospace East Granby
2. Barnes Aerospace Windsor Division
3. GKN Aerospace Engine Systems
4. GKN Aerospace Structures Corp.
5. Hanwha Aerospace USA (main)
6. Hanwha Aerospace USA, East Windsor
7. Hanwha Aerospace USA, Glastonbury
8. Hanwha Aerospace USA, Newington
9. HEICO / Turbine Kinetics
10. Triumph Systems, West Hartford
11. Triumph Systems, Windsor
12. Chromalloy Connecticut
13. Curtis-Wright Surface Technologies
14. Siemens Industry Inc
15. Kinetic Engine Systems, AeroCision
16. Kinetic Engine Systems, B&E Tool
17. Kinetic Engine Systems, Numet
18. Kinetic Engine Systems, Tell Tool
19. Enjet Aero Bloomfield
20. Enjet Aero Manchester

**Say "proceed" and I'll:**
1. Update config with these 20 companies
2. Add US-only location filtering
3. Run the test (~10 minutes)
4. Provide output files + analysis

---

**Or adjust the plan:** Tell me how many companies or which specific ones you want to test!
