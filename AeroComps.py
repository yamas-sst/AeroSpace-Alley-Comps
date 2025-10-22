# ======================================================
# Aerospace Alley Skilled Trades Job Scanner
# ======================================================
# PURPOSE: Automatically scan aerospace companies for skilled trades job openings
#          using Google Jobs API via SerpApi, then export results to Excel
#
# WORKFLOW:
#   1. Load list of aerospace companies from Excel
#   2. For each company, build optimized search queries with trade keywords
#   3. Query Google Jobs API (up to 3 pages per company)
#   4. Filter results to only skilled trades positions
#   5. Export to Excel with deduplication and checkpoints
#
# Optimized for: Anaconda + VS Code Environment
# Dependencies: pip install pandas openpyxl requests tqdm
# ======================================================

import pandas as pd
import requests
import time
import re
import difflib
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

# ======================================================
# CONFIGURATION CONSTANTS
# ======================================================
# These settings control API usage, file paths, and performance tuning

# API Authentication
API_KEY = "4aa81d243250039b571ae3b331214224e0f253369166f54273fa553355c9eaf7"  # SerpApi key for Google Jobs API access

# File Paths
INPUT_FILE = r"C:\Users\JoseYamas\Desktop\SST Core Projects\Zac\AeroSpace Alley Comps\Aerospace_Alley_Companies.xlsx"  # Excel file with "Company Name" column
OUTPUT_FILE = "Aerospace_Alley_SkilledTrades_Jobs.xlsx"  # Where to save job results

# Query Optimization
MAX_QUERY_LENGTH = 200  # Google Jobs has ~200 character limit for search queries

# Performance Tuning
MAX_THREADS = 5  # Number of companies to process in parallel (balance speed vs. rate limits)


# ======================================================
# GLOBAL STATE: API USAGE TRACKING & RATE LIMITING
# ======================================================
# These variables ensure we stay within API limits and avoid rate limit errors
# Thread-safe design allows parallel processing without exceeding quotas

api_lock = Lock()  # Ensures only one thread accesses API counter at a time
api_calls = 0  # Tracks total API calls made during this run
MAX_API_CALLS = 250  # Stop processing after this many calls (stay under SerpApi monthly limit)
api_limit_reached = False  # Global flag: when True, all threads stop making requests

# Rate Limiting: Prevent burst requests that trigger 429 errors
last_call_time = 0  # Timestamp of most recent API call
MIN_INTERVAL = 1.2  # Minimum seconds between API calls (prevents rate limit violations)

# ======================================================
# FUNCTION: safe_api_request()
# ======================================================
# PURPOSE: Thread-safe wrapper for SerpApi requests with quota and rate limit protection
#
# FEATURES:
#   - Tracks total API calls to prevent exceeding monthly quota
#   - Enforces minimum time spacing between requests (avoids 429 rate limit errors)
#   - Thread-safe using locks (multiple companies can be processed in parallel)
#   - Graceful shutdown when quota reached (stops all threads)
#
# PARAMETERS:
#   params (dict): SerpApi query parameters (engine, query, api_key, etc.)
#   company (str): Company name for logging purposes
#
# RETURNS:
#   requests.Response object if successful, None if quota exceeded

def safe_api_request(params, company):
    global api_calls, last_call_time, api_limit_reached

    # Critical section: Only one thread can access API counter/timer at a time
    with api_lock:
        # Check if we've hit the API quota limit
        if api_calls >= MAX_API_CALLS:
            if not api_limit_reached:
                api_limit_reached = True
                print(f"\n⚠️ API LIMIT REACHED ({MAX_API_CALLS} calls) — All threads will stop processing.\n")
            return None

        # Rate limiting: Enforce minimum spacing between API calls
        # This prevents burst requests that trigger 429 "Too Many Requests" errors
        now = time.time()
        elapsed = now - last_call_time
        if elapsed < MIN_INTERVAL:
            time.sleep(MIN_INTERVAL - elapsed)
        last_call_time = time.time()

        # Increment counter and log progress
        api_calls += 1
        print(f"API call #{api_calls} → {company}")

    # Make the actual API request (outside the lock to allow other threads to proceed)
    return requests.get("https://serpapi.com/search.json", params=params)


# ======================================================
# SKILLED TRADES KEYWORDS
# ======================================================
# PURPOSE: Comprehensive list of job titles and skills for skilled trades positions
#
# WHY THIS MATTERS:
#   - Used to build search queries (company name + OR-separated keywords)
#   - Also used to filter job results (only keep jobs with these keywords in title)
#   - Covers 100+ terms across 9 categories to maximize job discovery
#
# CATEGORIES:
#   - Machining & Fabrication (CNC, manual machining, tool & die)
#   - Assembly & Production (assemblers, operators, technicians)
#   - Welding & Metalwork (TIG, MIG, arc, specialized welding)
#   - Maintenance & Repair (mechanics, millwrights, equipment maintenance)
#   - Inspection & Quality (QC, NDT, metrology)
#   - Electrical & Technical (electricians, controls, instrumentation)
#   - Tooling & Setup (tool room, fixtures, jigs)
#   - Composites & Aerospace-specific (laminators, avionics, airframe)
#   - Other Skilled Trades (HVAC, coating, heat treat, apprenticeships)
SKILLED_TRADES_KEYWORDS = [
    # --- Machining & Fabrication ---
    "machinist", "cnc", "mill operator", "lathe operator", "grinder", "toolmaker", 
    "fabricator", "metalworker", "sheet metal", "precision machinist", "machine operator",
    "manual machinist", "setup operator", "g-code", "programmer", "tool and die", "die maker",
    "mold maker", "production machinist", "numerical control", "machining technician",
    
    # --- Assembly & Production ---
    "assembler", "assembly technician", "production operator", "production technician", 
    "line operator", "mechanical assembler", "electromechanical assembler", 
    "production worker", "manufacturing technician", "machine technician",
    "assembly lead", "manufacturing associate", "packaging operator", "composite technician",

    # --- Welding & Metalwork ---
    "welder", "tig welder", "mig welder", "arc welder", "fabrication welder", 
    "pipe welder", "aluminum welder", "spot welder", "soldering", "brazing", 
    "welding technician", "weld inspector", "fitter welder",

    # --- Maintenance & Repair ---
    "maintenance technician", "maintenance mechanic", "maintenance engineer", 
    "industrial mechanic", "millwright", "equipment technician", "machine repair", 
    "facilities technician", "mechanical technician", "preventive maintenance", 
    "maintenance electrician", "repair technician", "hvac technician", 
    "plant mechanic", "equipment maintenance",

    # --- Inspection & Quality ---
    "inspector", "quality inspector", "quality technician", "qc technician", 
    "qa inspector", "ndt technician", "cmm operator", "quality assurance", 
    "final inspector", "metrology technician", "dimensional inspector",

    # --- Electrical & Technical ---
    "electrician", "electrical technician", "electronics technician", 
    "controls technician", "panel builder", "wire harness assembler", 
    "electromechanical technician", "instrumentation technician", "automation technician",

    # --- Tooling & Setup ---
    "tool room", "tooling engineer", "setup technician", "fixture builder", 
    "tool designer", "jig and fixture", "tooling technician",

    # --- Composites & Aerospace Fabrication ---
    "composite technician", "lamination technician", "bonding technician", 
    "aerospace assembler", "aircraft technician", "avionics technician", 
    "sheet metal mechanic", "structures mechanic", "airframe mechanic",

    # --- Other Skilled Trades ---
    "plumber", "carpenter", "hvac installer", "painter", "coating technician", 
    "surface finisher", "heat treat operator", "chemical processor", "machining apprentice", 
    "maintenance apprentice", "journeyman", "technician apprentice"
]


# ======================================================
# DATA LOADING: Read Company List from Excel
# ======================================================
# PURPOSE: Load aerospace companies to scan for job openings
#
# INPUT FORMAT:
#   - Excel file must have a "Company Name" column
#   - One company per row (e.g., "Boeing", "Lockheed Martin", etc.)
#   - Additional columns are ignored
#
# OUTPUT:
#   - df: Full DataFrame (kept for potential future use)
#   - companies: Array of unique company names (duplicates removed)
#   - results: Empty list to store job listings (populated during processing)

df = pd.read_excel(INPUT_FILE)
companies = df["Company Name"].dropna().unique()  # Remove NaN values and duplicates
results = []  # Will store all job listings across all companies


# ======================================================
# FUNCTION: build_trade_query()
# ======================================================
# PURPOSE: Construct optimized Google Jobs search query for a specific company
#
# CHALLENGE:
#   Google Jobs has ~200 character query limit. We need to fit:
#   - Company name
#   - As many trade keywords as possible (joined with OR)
#   - Without exceeding character limit
#
# ALGORITHM:
#   1. Clean company name (remove special chars that could break query)
#   2. Iteratively add keywords until we approach the limit
#   3. Stop adding keywords when next one would exceed MAX_QUERY_LENGTH
#
# EXAMPLE OUTPUT:
#   "Boeing machinist OR cnc OR welder OR assembler OR inspector"
#
# PARAMETERS:
#   company_name (str): Name of company to search for
#   keywords (list): List of trade keywords to include in query
#   max_length (int): Maximum query length (default: 200 chars)
#
# RETURNS:
#   str: Optimized search query string

def build_trade_query(company_name, keywords, max_length=MAX_QUERY_LENGTH):
    """Builds job search query ensuring length limit compliance."""
    # Remove special characters that could interfere with search
    # Keep alphanumeric, ampersands (&), and spaces
    clean_name = re.sub(r"[^a-zA-Z0-9&\s]", "", company_name).strip()

    # Build query by adding keywords until we hit the length limit
    query_parts = []
    for kw in keywords:
        # Test if adding this keyword would exceed the limit
        tentative = f"{clean_name} {' OR '.join(query_parts + [kw])}"
        if len(tentative) > max_length:
            break  # Stop adding keywords
        query_parts.append(kw)

    # Return final query: "Company keyword1 OR keyword2 OR keyword3..."
    return f"{clean_name} " + " OR ".join(query_parts)


# ======================================================
# FUNCTION: fetch_jobs_for_company()
# ======================================================
# PURPOSE: Query Google Jobs for a single company and return filtered skilled trades jobs
#
# WORKFLOW:
#   1. Check if API limit reached (early exit if so)
#   2. Build optimized search query for this company
#   3. Query up to 3 pages of results (10 jobs per page = 30 max jobs)
#   4. For each page:
#      - Make API request with retry logic (3 attempts)
#      - Parse JSON response
#      - Filter jobs: only keep if title contains skilled trades keywords
#      - Store job details (title, location, URL, description, etc.)
#   5. Return all matching jobs for this company
#
# PARAMETERS:
#   company (str): Company name to search for
#
# RETURNS:
#   list[dict]: List of job dictionaries, each containing:
#     - Company, Job Title, Location, Via (job board), Source URL,
#       Detected Extensions, Description Snippet, Timestamp
#
# THREAD SAFETY:
#   - Multiple companies can be processed in parallel
#   - safe_api_request() handles thread synchronization
#   - Each thread has its own local_results list (no sharing)

def fetch_jobs_for_company(company):
    """Queries SerpApi for job results and returns filtered skilled-trade listings."""
    global api_limit_reached

    # Early exit if API limit already reached by another thread
    if api_limit_reached:
        print(f"[{company}] Skipping — API limit already reached.")
        return []

    local_results = []  # Store jobs for this company only
    query = build_trade_query(company, SKILLED_TRADES_KEYWORDS)

    # Pagination: Request up to 3 pages (10 jobs per page)
    # start=0 (page 1), start=10 (page 2), start=20 (page 3)
    for start in range(0, 30, 10):
        # Check if limit was reached during pagination
        if api_limit_reached:
            print(f"[{company}] Stopping pagination — API limit reached.")
            break

        # Build SerpApi request parameters
        params = {
            "engine": "google_jobs",  # Use Google Jobs search engine
            "q": query,  # Search query (company + keywords)
            "api_key": API_KEY,  # Authentication
            "hl": "en",  # Language: English
            "start": start  # Pagination offset
        }

        # Retry logic: Try up to 3 times if connection fails
        response = None
        for attempt in range(3):
            try:
                response = safe_api_request(params, company)
                if response is None:
                    # API limit reached, return what we've collected so far
                    return local_results
                if response.status_code == 200:
                    break  # Success, exit retry loop
                time.sleep(3)  # Wait before retrying
            except Exception as e:
                print(f"[{company}] Connection error, retrying... {e}")
                time.sleep(3)

        # If all retries failed, skip this page
        if response is None or not response.ok:
            if response:
                print(f"[{company}] Skipped (HTTP {response.status_code})")
            continue

        # Parse JSON response
        data = response.json()
        job_results = data.get("jobs_results", [])

        # Optimization: If first page has no results, skip remaining pages
        # (Company likely has no job postings at all)
        if not job_results:
            if start == 0:  # Only stop if first page is empty
                print(f"[{company}] No jobs found — skipping remaining pages.")
                break

        # Process each job listing
        for job in job_results:
            title = job.get("title", "")

            # CRITICAL FILTER: Only keep jobs with skilled trades keywords in title
            # This removes management, engineering, software roles, etc.
            if any(kw.lower() in title.lower() for kw in SKILLED_TRADES_KEYWORDS):
                local_results.append({
                    "Company": company,
                    "Job Title": title,
                    "Location": job.get("location", ""),
                    "Via": job.get("via", ""),  # Job board source (Indeed, LinkedIn, etc.)
                    "Source URL": job.get("apply_link", ""),
                    "Detected Extensions": job.get("detected_extensions", {}),
                    "Description Snippet": job.get("description", "")[:200],  # First 200 chars
                    "Timestamp": pd.Timestamp.now()  # When we scraped this job
                })

        # Brief pause between pages to avoid triggering rate limits
        time.sleep(1)

    print(f"[{company}] → {len(local_results)} skilled-trade jobs found")
    return local_results


# ======================================================
# MAIN EXECUTION: Parallel Company Processing
# ======================================================
# PURPOSE: Process multiple companies simultaneously to maximize speed
#
# HOW IT WORKS:
#   - ThreadPoolExecutor creates a pool of worker threads (MAX_THREADS = 5)
#   - Each thread processes one company at a time
#   - As companies finish, new ones are assigned to available threads
#   - Progress bar (tqdm) shows real-time completion status
#
# FEATURES:
#   - Parallel processing: 5 companies at once (configurable)
#   - Progressive checkpoints: Save results every 25 companies (prevents data loss)
#   - Error handling: Individual company failures don't crash entire process
#   - Result aggregation: All jobs collected into single results list
#
# PERFORMANCE:
#   - Single-threaded: ~50 companies/hour (1.2s per API call × 3 pages)
#   - Multi-threaded (5 workers): ~200-250 companies/hour
#   - Bottleneck: API rate limits (MIN_INTERVAL = 1.2s between calls)

with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
    # Submit all companies to the thread pool
    # futures = {Future object: company_name}
    futures = {executor.submit(fetch_jobs_for_company, company): company for company in companies}

    # Process results as they complete (not necessarily in order)
    for i, future in enumerate(tqdm(as_completed(futures), total=len(futures), desc="Processing companies")):
        company = futures[future]
        try:
            # Retrieve job results from completed thread
            company_results = future.result()
            results.extend(company_results)  # Add to master results list

            # CHECKPOINT SAVE: Every 25 companies, save progress to disk
            # This prevents losing all data if script crashes or API limit is hit
            if i % 25 == 0 and results:
                pd.DataFrame(results).drop_duplicates(subset=["Company", "Job Title", "Source URL"]).to_excel(OUTPUT_FILE, index=False)
                print(f"Checkpoint saved ({len(results)} total records).")

        except Exception as e:
            # Log error but continue processing other companies
            print(f"⚠️ Error processing {company}: {e}")


# ======================================================
# FINAL EXPORT: Save All Results to Excel
# ======================================================
# PURPOSE: Save deduplicated job listings and display summary statistics
#
# DEDUPLICATION:
#   - Remove duplicates based on: Company + Job Title + Source URL
#   - Same job posted to multiple boards = kept as separate records (different URLs)
#   - Prevents counting the same job listing twice
#
# OUTPUT FORMAT:
#   - Excel file (.xlsx) with columns:
#     Company | Job Title | Location | Via | Source URL | Detected Extensions | Description Snippet | Timestamp
#   - Sorted by order collected (not alphabetical)
#   - No index column (index=False)

print(f"\n{'='*60}")
print(f"API Usage: {api_calls}/{MAX_API_CALLS} calls used")
if api_limit_reached:
    print(f"⚠️ API limit reached — some companies may not have been processed")
print(f"{'='*60}\n")

if results:
    # Create DataFrame and remove duplicates
    final_df = pd.DataFrame(results).drop_duplicates(subset=["Company", "Job Title", "Source URL"])

    # Save to Excel
    final_df.to_excel(OUTPUT_FILE, index=False)

    # Success message with job count
    print(f"✅ Completed! {len(final_df)} skilled-trade jobs saved to {OUTPUT_FILE}")

    # ======================================================
    # ANALYTICS: Generate Insights Report
    # ======================================================
    # Automatically generate analytics report if we have results
    try:
        from analytics import JobAnalytics

        analytics_output = OUTPUT_FILE.replace(".xlsx", "_Analytics.xlsx")
        analytics = JobAnalytics(final_df)
        analytics.generate_report(analytics_output)

    except ImportError:
        print("\n⚠️ Analytics module not found. Skipping analytics generation.")
        print("   To enable analytics, ensure 'analytics.py' is in the same directory.")
    except Exception as e:
        print(f"\n⚠️ Error generating analytics: {e}")
        print("   Job data has been saved, but analytics report was not generated.")

else:
    # No jobs found across all companies
    print("⚠️ No skilled-trade jobs found. Try adjusting keywords or company list.")

