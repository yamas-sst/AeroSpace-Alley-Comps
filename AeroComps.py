# ======================================================
# Aerospace Alley Skilled Trades Job Scanner
# ======================================================
# PURPOSE: Automatically scan aerospace companies for skilled trades job openings
#          using Google Jobs API via SerpApi, then export results to Excel
#
# WORKFLOW:
#   1. Load configuration from config.json (API keys, settings, file paths)
#   2. Load list of aerospace companies from Excel
#   3. For each company, build optimized search queries with trade keywords
#   4. Query Google Jobs API (up to 3 pages per company)
#   5. Filter results to only skilled trades positions
#   6. Export to Excel with deduplication and checkpoints
#
# CONFIGURATION: Edit config.json to change settings, API keys, testing mode
# Dependencies: pip install pandas openpyxl requests tqdm
# ======================================================

import pandas as pd
import requests
import time
import re
import difflib
import json
import os
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

# ======================================================
# CONFIGURATION LOADER
# ======================================================
def load_config(config_file="config.json"):
    """
    Load configuration from JSON file.

    PARAMETERS:
        config_file (str): Path to configuration file (default: config.json)

    RETURNS:
        dict: Configuration dictionary with API keys and settings

    RAISES:
        FileNotFoundError: If config.json doesn't exist
        json.JSONDecodeError: If config.json has invalid JSON
    """
    if not os.path.exists(config_file):
        print(f"\n❌ ERROR: {config_file} not found!")
        print(f"   Please create {config_file} with your API keys and settings.")
        print(f"   See README.md for configuration instructions.\n")
        raise FileNotFoundError(f"Configuration file {config_file} not found")

    with open(config_file, 'r') as f:
        config = json.load(f)

    # Validate required fields
    if "api_keys" not in config or len(config["api_keys"]) == 0:
        raise ValueError("config.json must contain at least one API key in 'api_keys' array")
    if "settings" not in config:
        raise ValueError("config.json must contain 'settings' object")

    return config


# ======================================================
# LOAD CONFIGURATION
# ======================================================
print("\n" + "="*70)
print("AEROSPACE ALLEY JOB SCANNER - Configuration Loading")
print("="*70)

try:
    CONFIG = load_config()
    print(f"✅ Configuration loaded successfully from config.json")
    print(f"   API Keys found: {len(CONFIG['api_keys'])}")
    for i, key_info in enumerate(CONFIG['api_keys'], 1):
        print(f"   - {key_info['label']}: {key_info['key'][:20]}...{key_info['key'][-10:]} (limit: {key_info.get('limit', 250)})")

    # Testing mode indicator
    if CONFIG['settings'].get('testing_mode', False):
        print(f"\n🧪 TESTING MODE ENABLED: Will process only {CONFIG['settings'].get('testing_company_limit', 1)} companies")
    else:
        print(f"\n🚀 PRODUCTION MODE: Will process all companies")

    print("="*70 + "\n")
except Exception as e:
    print(f"\n❌ ERROR loading configuration: {e}\n")
    exit(1)


# ======================================================
# CONFIGURATION CONSTANTS (Loaded from config.json)
# ======================================================
# API Authentication - Use primary API key by default
API_KEY = CONFIG['api_keys'][0]['key']  # Primary API key
API_KEY_LABEL = CONFIG['api_keys'][0]['label']  # Label for logging

# File Paths (from config)
INPUT_FILE = CONFIG['settings']['input_file']
OUTPUT_FILE = CONFIG['settings']['output_file']

# Query Optimization
MAX_QUERY_LENGTH = CONFIG['settings'].get('max_query_length', 200)

# Performance Tuning
MAX_THREADS = CONFIG['settings'].get('max_threads', 5)

# Testing Mode
TESTING_MODE = CONFIG['settings'].get('testing_mode', False)
TESTING_COMPANY_LIMIT = CONFIG['settings'].get('testing_company_limit', 1)


# ======================================================
# GLOBAL STATE: API USAGE TRACKING & RATE LIMITING
# ======================================================
# These variables ensure we stay within API limits and avoid rate limit errors
# Thread-safe design allows parallel processing without exceeding quotas

api_lock = Lock()  # Ensures only one thread accesses API counter at a time
api_calls = 0  # Tracks total API calls made during this run
MAX_API_CALLS = CONFIG['settings'].get('max_api_calls_per_key', 250)  # API call limit per key
api_limit_reached = False  # Global flag: when True, all threads stop making requests

# Rate Limiting: Prevent burst requests that trigger 429 errors
last_call_time = 0  # Timestamp of most recent API call
MIN_INTERVAL = CONFIG['settings'].get('min_interval_seconds', 1.2)  # Minimum seconds between API calls


# ======================================================
# HEALTH MONITORING SYSTEM
# ======================================================
class APIHealthMonitor:
    """
    Monitors API health and detects when fallback strategies should be triggered.

    Tracks:
    - API call success/failure rates
    - Consecutive failures
    - Rate limit errors
    - Companies with/without jobs

    Triggers fallback when:
    - 5+ consecutive failures
    - 3+ rate limit errors
    - <15% success rate after 10 companies
    """
    def __init__(self):
        self.total_calls = 0
        self.successful_calls = 0
        self.failed_calls = 0
        self.rate_limit_errors = 0
        self.companies_processed = 0
        self.companies_with_jobs = 0
        self.consecutive_failures = 0
        self.total_jobs_found = 0

    def record_call(self, status_code, company, jobs_found):
        """Record API call result"""
        self.total_calls += 1
        self.companies_processed += 1

        if status_code == 200:
            self.successful_calls += 1
            self.consecutive_failures = 0
        else:
            self.failed_calls += 1
            self.consecutive_failures += 1

        if status_code in [403, 429]:
            self.rate_limit_errors += 1

        if jobs_found > 0:
            self.companies_with_jobs += 1
            self.total_jobs_found += jobs_found

    def should_trigger_fallback(self):
        """Determine if fallback strategy should be triggered"""
        # Trigger 1: Consecutive failures
        if self.consecutive_failures >= 5:
            return True, "consecutive_failures"

        # Trigger 2: Rate limited
        if self.rate_limit_errors >= 3:
            return True, "rate_limited"

        # Trigger 3: Low success rate (after minimum sample)
        if self.companies_processed >= 10:
            success_rate = self.companies_with_jobs / self.companies_processed
            if success_rate < 0.15:  # Less than 15%
                return True, "low_success_rate"

        return False, None

    def get_summary(self):
        """Get health summary"""
        success_rate = (self.companies_with_jobs / self.companies_processed * 100
                       if self.companies_processed > 0 else 0)
        avg_jobs = (self.total_jobs_found / self.companies_with_jobs
                   if self.companies_with_jobs > 0 else 0)

        return {
            "companies_processed": self.companies_processed,
            "companies_with_jobs": self.companies_with_jobs,
            "success_rate": f"{success_rate:.1f}%",
            "total_jobs_found": self.total_jobs_found,
            "avg_jobs_per_company": f"{avg_jobs:.1f}",
            "consecutive_failures": self.consecutive_failures,
            "rate_limit_errors": self.rate_limit_errors
        }


# Initialize global health monitor
health_monitor = APIHealthMonitor()


# ======================================================
# RESPONSE VALIDATION
# ======================================================
def validate_api_response(response, company):
    """
    Validates SerpAPI response for errors and data quality.

    CHECKS:
    - HTTP status code
    - JSON parsing
    - API error messages
    - Required fields present

    PARAMETERS:
        response (requests.Response): API response
        company (str): Company name (for logging)

    RETURNS:
        tuple: (is_valid: bool, data: dict or None, error_message: str or None)
    """
    # Check HTTP status
    if response.status_code != 200:
        error_msg = f"HTTP {response.status_code}"

        # Specific error messages
        if response.status_code == 403:
            error_msg += " - API blocked or rate limited (IP restriction)"
        elif response.status_code == 429:
            error_msg += " - Too many requests (rate limit)"
        elif response.status_code == 401:
            error_msg += " - Invalid API key"
        elif response.status_code == 402:
            error_msg += " - API credits exhausted"
        elif response.status_code >= 500:
            error_msg += " - Server error"

        return False, None, error_msg

    # Parse JSON
    try:
        data = response.json()
    except Exception as e:
        return False, None, f"Invalid JSON response: {e}"

    # Check for API error field
    if "error" in data:
        return False, None, f"API Error: {data['error']}"

    # Validate required fields
    if "search_metadata" not in data:
        return False, None, "Missing search_metadata (possible API issue)"

    # Valid response
    return True, data, None


# ======================================================
# COMPANY NAME MATCHING
# ======================================================
def validate_company_match(target_company, api_company, threshold=0.65):
    """
    Validates that job is from target company (fuzzy matching).

    RATIONALE:
    - Google Jobs may return jobs from similarly-named companies
    - E.g., "GKN Aerospace" might return "GKN Industries" jobs
    - Use fuzzy matching to validate company name similarity

    PARAMETERS:
        target_company (str): Company we're searching for
        api_company (str): Company name from API response
        threshold (float): Minimum similarity score (0-1)

    RETURNS:
        bool: True if match is good enough
    """
    if not api_company:
        return False  # No company name in response

    from difflib import SequenceMatcher

    # Normalize names (lowercase, remove special chars)
    target_clean = re.sub(r'[^a-z0-9\s]', '', target_company.lower())
    api_clean = re.sub(r'[^a-z0-9\s]', '', api_company.lower())

    # Calculate similarity
    similarity = SequenceMatcher(None, target_clean, api_clean).ratio()

    return similarity >= threshold

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
        print(f"API call #{api_calls} ({API_KEY_LABEL}) → {company}")

    # Make the actual API request (outside the lock to allow other threads to proceed)
    # 30-second timeout prevents hanging on slow/failed connections
    return requests.get("https://serpapi.com/search.json", params=params, timeout=30)


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
#
# TESTING MODE: If enabled, only process limited number of companies

print(f"Loading company list from: {INPUT_FILE}")
df = pd.read_excel(INPUT_FILE)
companies = df["Company Name"].dropna().unique()  # Remove NaN values and duplicates

# Apply testing mode filter if enabled
total_companies = len(companies)
if TESTING_MODE:
    companies = companies[:TESTING_COMPANY_LIMIT]
    print(f"🧪 TESTING MODE: Processing {len(companies)} of {total_companies} companies")
    print(f"   Companies to test: {', '.join(companies)}")
else:
    print(f"📊 Loaded {total_companies} companies to process")

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

def build_trade_query(company_name, keywords=None, max_length=MAX_QUERY_LENGTH):
    """
    Builds job search query for Google Jobs API.

    SIMPLIFIED APPROACH (FIXED):
    - Uses company name ONLY (no complex OR logic)
    - Lets Google Jobs find ALL jobs at the company
    - Post-filtering handles skilled trades selection

    RATIONALE:
    - Complex OR queries ("Company keyword1 OR keyword2") cause Google to search
      for keyword1/keyword2 ANYWHERE, not just at the target company
    - Simple company name query returns company-specific results
    - More reliable and better results

    PARAMETERS:
        company_name (str): Company name to search
        keywords (list): IGNORED - kept for backward compatibility
        max_length (int): IGNORED - kept for backward compatibility

    RETURNS:
        str: Simple company name query
    """
    # Remove special characters that could interfere with search
    # Keep alphanumeric, ampersands (&), and spaces
    clean_name = re.sub(r"[^a-zA-Z0-9&\s]", "", company_name).strip()

    # SIMPLE: Just return company name
    # Google Jobs will find all positions at this company
    # We filter for skilled trades in post-processing
    return clean_name


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
        data = None
        for attempt in range(3):
            try:
                response = safe_api_request(params, company)
                if response is None:
                    # API limit reached, return what we've collected so far
                    health_monitor.record_call(0, company, len(local_results))
                    return local_results

                # Validate API response using comprehensive validation
                is_valid, data, error_msg = validate_api_response(response, company)
                if is_valid:
                    break  # Success, exit retry loop
                else:
                    print(f"[{company}] Validation failed: {error_msg}")
                    health_monitor.record_call(response.status_code, company, 0)
                    if response.status_code in [403, 429]:  # Rate limit errors - don't retry
                        return local_results
                    time.sleep(3)  # Wait before retrying for other errors
            except Exception as e:
                print(f"[{company}] Connection error, retrying... {e}")
                time.sleep(3)

        # If all retries failed, skip this page
        if data is None:
            if response:
                print(f"[{company}] Skipped after {attempt+1} attempts")
            continue

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
            api_company = job.get("company_name", "")

            # VALIDATION 1: Verify job is actually from target company (fuzzy match)
            # Prevents false positives from similar company names or broad searches
            if not validate_company_match(company, api_company):
                continue  # Skip job from different company

            # VALIDATION 2: Only keep jobs with skilled trades keywords in title
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

    # Record successful processing in health monitor
    health_monitor.record_call(200, company, len(local_results))

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

            # CHECK FOR FALLBACK TRIGGER: Detect API health issues
            should_fallback, reason = health_monitor.should_trigger_fallback()
            if should_fallback:
                print(f"\n{'='*60}")
                print(f"⚠️ FALLBACK TRIGGER DETECTED: {reason}")
                print(f"{'='*60}")
                print(health_monitor.get_summary())
                print(f"\n⚠️ SerpAPI appears ineffective for this dataset.")
                print(f"📋 See COMPLETE_AUDIT_AND_FALLBACK.md for alternative strategies.")
                print(f"{'='*60}\n")
                # Continue processing but user is alerted to investigate alternatives

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
print(f"API Usage: {api_calls}/{MAX_API_CALLS} calls used ({API_KEY_LABEL})")
if api_limit_reached:
    print(f"⚠️ API limit reached — some companies may not have been processed")
print(f"{'='*60}\n")

if results:
    # Create DataFrame and remove duplicates
    final_df = pd.DataFrame(results).drop_duplicates(subset=["Company", "Job Title", "Source URL"])

    # Ensure output directory exists
    output_dir = os.path.dirname(OUTPUT_FILE)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"📁 Created output directory: {output_dir}")

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

# ======================================================
# API HEALTH SUMMARY
# ======================================================
# Display comprehensive API health metrics
print(f"\n{'='*60}")
print("API HEALTH SUMMARY")
print(f"{'='*60}")
print(health_monitor.get_summary())
print(f"{'='*60}\n")

