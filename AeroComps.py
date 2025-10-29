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

# Rate Limit Protection System
from resources.rate_limit_protection import (
    ConfigurationValidator,
    RateLimitProtectionCoordinator,
    ComprehensiveAuditLogger,
    EnhancedHealthMonitor
)

# ======================================================
# CONFIGURATION LOADER
# ======================================================
def load_config(config_file="resources/config.json"):
    """
    Load configuration from JSON file.

    PARAMETERS:
        config_file (str): Path to configuration file (default: resources/config.json)

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
    print(f"✅ Configuration loaded successfully from resources/config.json")
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
# PROFILE SYSTEM: Select Active Profile
# ======================================================
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(
    description='Aerospace Alley Job Scanner',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""
Examples:
  python AeroComps.py                         # Use profile from config.json
  python AeroComps.py --profile quick_test    # Quick 3-company test
  python AeroComps.py --profile production    # Full 137-company run
    """
)
parser.add_argument('--profile', type=str, help='Profile to use (overrides config.json)')
args = parser.parse_args()

# Get active profile (command line takes precedence)
if args.profile:
    active_profile_name = args.profile
    print(f"🔀 Profile override: {args.profile} (from command line)")
else:
    active_profile_name = CONFIG.get('active_profile')
    if active_profile_name is None:
        print("\n❌ ERROR: No 'active_profile' specified in config.json")
        print("   Please set 'active_profile' to one of: " + ", ".join(CONFIG['profiles'].keys()))
        print("   Or use --profile flag: python AeroComps.py --profile quick_test")
        exit(1)

# Validate profile exists
if active_profile_name not in CONFIG['profiles']:
    print(f"\n❌ ERROR: Invalid profile '{active_profile_name}'")
    print(f"   Available profiles: {', '.join(CONFIG['profiles'].keys())}")
    exit(1)

# Load settings from active profile
active_profile = CONFIG['profiles'][active_profile_name]
print(f"\n✅ Active Profile: {active_profile_name}")
print(f"   Description: {active_profile['description']}")

# Apply profile settings (override settings section)
TESTING_MODE = active_profile['testing_mode']
TESTING_COMPANY_LIMIT = active_profile.get('testing_company_limit', None)

# Display confirmation
if TESTING_MODE:
    print(f"   Mode: TESTING ({TESTING_COMPANY_LIMIT} companies)")
else:
    print(f"   Mode: PRODUCTION (all companies)")

print("="*70 + "\n")

# ======================================================
# INITIALIZE PROTECTION SYSTEM
# ======================================================
print("Initializing rate limit protection system...")
try:
    protection = RateLimitProtectionCoordinator(CONFIG)
    rate_limiter = protection.rate_limiter
    circuit_breaker = protection.circuit_breaker
    batch_processor = protection.batch_processor
    audit_logger = protection.audit_logger
    health_monitor = protection.health_monitor  # Enhanced version
    print("✅ Protection system initialized:")
    print("   • Token Bucket Rate Limiter (60 calls/hour)")
    print("   • Circuit Breaker (3 failure threshold)")
    print("   • Exponential Backoff (3 max attempts)")
    print("   • Batch Processor (10 companies/batch)")
    print("   • Audit Logger (log/api_audit.jsonl)")
    print("   • Health Monitor (real-time alerts)")
    print("="*70 + "\n")
except Exception as e:
    print(f"\n❌ ERROR initializing protection system: {e}\n")
    exit(1)


# ======================================================
# API USAGE TRACKER: Persistent State Management
# ======================================================
from resources.api_usage_tracker import PersistentAPIUsageTracker

# Initialize tracker
usage_tracker = PersistentAPIUsageTracker(CONFIG)

# Get available API key
api_key_info, remaining_calls = usage_tracker.get_available_key()

if api_key_info is None:
    print("\n" + "="*70)
    print("❌ ALL API KEYS EXHAUSTED")
    print("="*70)
    print(usage_tracker.get_usage_report())
    print("\nOPTIONS:")
    print("  - Wait for monthly reset (check billing cycle at serpapi.com)")
    print("  - Request premium usage limits (contact serpapi.com/support)")
    print("  - Add more API keys to config.json")
    print("="*70 + "\n")
    exit(1)

API_KEY = api_key_info['key']
API_KEY_LABEL = api_key_info['label']

# ======================================================
# CONFIGURATION CONSTANTS (Loaded from config.json)
# ======================================================
# File Paths (from config)
INPUT_FILE = CONFIG['settings']['input_file']

# Dynamic output filename based on mode
if TESTING_MODE:
    timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M")
    OUTPUT_FILE = f"output/Test_{TESTING_COMPANY_LIMIT}Companies_{timestamp}.xlsx"
    print(f"🧪 TESTING MODE: Output → {OUTPUT_FILE}")
else:
    OUTPUT_FILE = "output/Aerospace_Alley_SkilledTrades_Jobs.xlsx"
    print(f"📊 PRODUCTION MODE: Output → {OUTPUT_FILE}")

# Query Optimization
MAX_QUERY_LENGTH = CONFIG['settings'].get('max_query_length', 200)

# Performance Tuning
MAX_THREADS = CONFIG['settings'].get('max_threads', 5)


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
# NOTE: Using EnhancedHealthMonitor from rate_limit_protection module
# Initialized globally as part of protection system (line 108)
# Provides enhanced monitoring with:
# - More detailed metrics and response time tracking
# - Configurable alert thresholds
# - Automatic fallback triggers
# - Real-time health reports


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
        error_msg = str(data['error'])
        # "No results" is valid - allows fallback retry logic
        if "no results" in error_msg.lower() or "hasn't returned any results" in error_msg.lower():
            return True, {"jobs_results": [], "search_metadata": {"status": "Success"}}, None
        return False, None, f"API Error: {error_msg}"

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

    # Normalize names (lowercase, remove special chars, preserve hyphens)
    # PRESERVES HYPHENS: Ensures "Accu-Rite" matches "Accu-Rite" but not "AccuRite"
    target_clean = re.sub(r'[^a-z0-9\s-]', '', target_company.lower())
    api_clean = re.sub(r'[^a-z0-9\s-]', '', api_company.lower())

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

    # CHECK CIRCUIT BREAKER: Stop if too many failures
    if not circuit_breaker.is_available():
        print(f"\n⛔ CIRCUIT BREAKER OPEN - Stopping all API calls")
        print(f"   Reason: Too many consecutive failures detected")
        print(f"   System will pause to prevent further issues")
        api_limit_reached = True
        return None

    # Critical section: Only one thread can access API counter at a time
    with api_lock:
        # Check if we've hit the API quota limit
        if api_calls >= MAX_API_CALLS:
            if not api_limit_reached:
                api_limit_reached = True
                print(f"\n⚠️ API LIMIT REACHED ({MAX_API_CALLS} calls) — All threads will stop processing.\n")
            return None

        # RATE LIMITING: Use token bucket algorithm (blocks if needed)
        # This replaces manual time.sleep() with industry-standard rate limiting
        rate_limiter.acquire(1)

        # Increment counter and log progress
        api_calls += 1
        usage_tracker.increment_usage(API_KEY_LABEL, calls=1)
        print(f"API call #{api_calls} ({API_KEY_LABEL}) → {company}")

    # Make the actual API request (outside the lock to allow other threads to proceed)
    # 30-second timeout prevents hanging on slow/failed connections
    start_time = time.time()

    try:
        # DEBUG: Print actual params being sent
        print(f"\n🔍 DEBUG - Sending API request:")
        print(f"   Company: {company}")
        for key, value in params.items():
            if key == "api_key":
                print(f"   {key}: {value[:20]}...{value[-10:]}")
            else:
                print(f"   {key}: {value}")
                
        response = requests.get("https://serpapi.com/search.json", params=params, timeout=30)
        response_time_ms = (time.time() - start_time) * 1000

        # AUDIT LOG: Record all API calls for compliance
        audit_logger.log_api_call(
            company=company,
            status_code=response.status_code,
            response_time_ms=response_time_ms,
            jobs_found=0,  # Updated later in fetch_jobs_for_company()
            api_key_label=API_KEY_LABEL
        )

        # UPDATE CIRCUIT BREAKER: Track success/failure
        if response.status_code == 200:
            circuit_breaker.record_success()
        else:
            circuit_breaker.record_failure()

            # LOG RATE LIMIT ERRORS SPECIFICALLY
            if response.status_code in [403, 429]:
                audit_logger.log_rate_limit(
                    status_code=response.status_code,
                    company=company,
                    message=f"Rate limit detected: HTTP {response.status_code}"
                )

        return response

    except Exception as e:
        response_time_ms = (time.time() - start_time) * 1000
        circuit_breaker.record_failure()
        audit_logger.log_error(
            error_type="request_exception",
            message=str(e),
            company=company
        )
        raise e


# ======================================================
# SKILLED TRADES KEYWORDS - EXPANDED VERSION
# ======================================================
# PURPOSE: Filter job listings to only skilled trades positions
#
# COVERAGE:
#   - Category 1: Hands-On Skilled Trades (~120 keywords)
#     * Machining, welding, assembly, maintenance, inspection
#     * Licensed trades: electricians, plumbers, HVAC (with certifications)
#     * Certifications: AWS (welding), ASNT (NDT), EPA 608 (HVAC)
#
#   - Category 2: Technical Leadership (~65 keywords)
#     * Manufacturing/quality engineers
#     * Production supervisors, foremen, superintendents
#     * Planning/coordination roles
#
# TOTAL: ~185 keywords (expanded from original 80)
# LAST UPDATED: October 2025

# ======================================================
# COMPREHENSIVE JOB MATCHING - ALL AEROSPACE ROLES
# ======================================================
# Captures ALL job types at aerospace companies using word-based matching.
#
# SCOPE: Complete labor market intelligence for CT aerospace industry
# - Manufacturing: Machinists, Welders, Assemblers, Operators
# - Engineering: ALL types (Manufacturing, Software, Design, Quality, etc.)
# - Business: Sales, Marketing, HR, Finance, Accounting
# - IT: Software Developers, Network Engineers, Data Analysts, IT Support
# - Admin: Office Staff, Receptionists, Administrative Assistants
# - Management: Directors, Managers, Supervisors, Executives
# - Skilled Trades: Electricians, Plumbers, HVAC, Inspectors
#
# EXCLUSIONS: Only truly unrelated jobs (medical staff, janitorial)
# - Everything else is INCLUDED for comprehensive market analysis

CORE_TRADE_WORDS = [
    # Machining & Fabrication
    "machinist", "cnc", "mill", "lathe", "fabricator", "welder", "toolmaker",

    # Assembly & Production
    "assembler", "assembly", "operator", "production",

    # Maintenance & Mechanical
    "mechanic", "millwright", "maintenance", "repair",

    # Electrical & Controls
    "electrician", "electrical", "electronics", "electronic", "controls",

    # Plumbing & HVAC
    "plumber", "pipefitter", "hvac", "boiler", "refrigeration",

    # Inspection & Quality
    "inspector", "inspection", "quality", "metrology", "ndt", "cmm",

    # Technical Roles
    "technician", "tech",

    # Engineering (ALL types)
    "engineer", "engineering", "supervisor", "foreman", "superintendent", "lead",

    # IT & Software (ALL included)
    "software", "developer", "programmer", "analyst", "it ", "information technology",
    "network", "cyber", "data", "systems", "database",

    # Business & Admin (ALL included)
    "sales", "marketing", "hr", "human resources", "recruiter", "accounting",
    "finance", "purchasing", "buyer", "accountant", "financial",
    "office", "administrative", "admin", "receptionist", "assistant",
    "secretary", "clerk", "coordinator",

    # Management & Leadership
    "manager", "director", "vp", "vice president", "president", "executive",
    "specialist", "representative", "associate",

    # Planning & Operations
    "planner", "scheduler", "logistics", "supply chain", "operations",
    "project manager", "program manager",

    # Design & Creative
    "designer", "design", "architect", "drafter", "cad",
]

EXCLUSION_PATTERNS = [
    # Only exclude truly unrelated jobs (medical, custodial)
    # EVERYTHING ELSE is included (all aerospace company jobs)
    "nurse", "doctor", "physician", "medical", "clinical",
    "janitorial", "custodian", "janitor", "housekeeper",
]

def is_skilled_trade_job(job_title):
    """
    Broad matching: checks if job title is aerospace industry-related.

    Returns True if:
    - Title contains at least one CORE_TRADE_WORD
    - AND title does NOT contain EXCLUSION_PATTERNS (only medical/janitorial)

    Captures ALL aerospace company jobs:
        ✅ Manufacturing Engineer, Process Engineer, Software Engineer
        ✅ CNC Machinist, Welder, Electrician, Inspector
        ✅ HR Manager, Accountant, Sales Representative
        ✅ IT Administrator, Network Engineer, Data Analyst
        ✅ Production Supervisor, Project Manager, Director
        ✅ Administrative Assistant, Receptionist, Office Clerk
        ✅ Intern, Co-Op, Trainee positions
        ❌ Nurse, Doctor (medical - not aerospace)
        ❌ Janitor, Custodian (facilities - not aerospace core)
    """
    title_lower = job_title.lower()

    # Check exclusions first (faster to reject early)
    for exclusion in EXCLUSION_PATTERNS:
        if exclusion in title_lower:
            return False

    # Check if any core trade word is present
    for word in CORE_TRADE_WORDS:
        if word in title_lower:
            return True

    return False

# LEGACY: Keep old keyword list for reference/fallback
SKILLED_TRADES_KEYWORDS_LEGACY = [
    # ==========================================
    # CATEGORY 1: HANDS-ON SKILLED TRADES
    # ==========================================

    # --- 1A: Machining & Fabrication ---
    "machinist", "cnc", "mill operator", "lathe operator", "grinder", "toolmaker",
    "fabricator", "metalworker", "sheet metal", "precision machinist", "machine operator",
    "manual machinist", "setup operator", "g-code", "programmer", "tool and die", "die maker",
    "mold maker", "production machinist", "numerical control", "machining technician",
    "swiss machinist", "5-axis operator", "edm operator", "waterjet operator",
    "laser operator", "plasma cutter", "boring mill operator", "horizontal machinist",
    "jig borer", "gear cutter", "honing machine operator", "lapping technician",

    # --- 1B: Assembly & Production ---
    "assembler", "assembly technician", "production operator", "production technician",
    "line operator", "mechanical assembler", "electromechanical assembler",
    "production worker", "manufacturing technician", "machine technician",
    "assembly lead", "manufacturing associate", "packaging operator", "composite technician",
    "engineering technician", "process technician", "prep technician", "part marking technician",

    # --- 1C: Welding & Metalwork (WITH CERTIFICATIONS) ---
    "welder", "tig welder", "mig welder", "arc welder", "fabrication welder",
    "pipe welder", "aluminum welder", "spot welder", "soldering", "brazing",
    "welding technician", "weld inspector", "fitter welder",
    "certified welder", "aws certified welder", "cw welder", "cwi", "cwe",
    "combo welder", "stick welder", "flux core welder", "orbital welder", "robotic welder",

    # --- 1D: Licensed Electrical Trades (CERTIFICATIONS REQUIRED) ---
    "electrician", "electrical technician", "electronics technician", "electronic technician",
    "controls technician", "panel builder", "wire harness assembler",
    "electromechanical technician", "instrumentation technician", "automation technician",
    "journeyman electrician", "master electrician", "industrial electrician",
    "maintenance electrician", "commercial electrician",
    "controls engineer", "automation specialist", "robotics technician",
    "plc programmer", "scada technician", "instrumentation electrician",
    "high voltage electrician", "electrical inspector", "electrical designer",
    "panel designer", "control panel technician", "electronic systems technician",

    # --- 1E: Plumbing, Pipefitting & HVAC (LICENSED TRADES) ---
    "plumber", "journeyman plumber", "master plumber", "pipefitter", "steamfitter",
    "sprinkler fitter", "industrial plumber", "process piping",
    "hvac technician", "hvac mechanic", "hvac service technician", "hvac installer",
    "refrigeration technician", "chiller technician", "boiler technician",
    "building automation", "hvac controls", "hvac apprentice", "journeyman hvac",
    "facilities mechanic", "building engineer", "stationary engineer", "boiler operator",

    # --- 1F: Maintenance & Repair ---
    "maintenance technician", "maintenance mechanic", "maintenance engineer",
    "industrial mechanic", "millwright", "equipment technician", "machine repair",
    "facilities technician", "mechanical technician", "preventive maintenance",
    "repair technician", "plant mechanic", "equipment maintenance",
    "predictive maintenance", "reliability technician", "vibration analyst",
    "lubrication technician", "alignment technician", "hydraulics technician",
    "pneumatics technician", "conveyor technician", "crane technician", "forklift technician",

    # --- 1G: Inspection & Quality (WITH CERTIFICATIONS) ---
    "inspector", "quality inspector", "quality technician", "qc technician",
    "qa inspector", "ndt technician", "cmm operator", "quality assurance",
    "final inspector", "metrology technician", "dimensional inspector",
    "ndt level ii", "ndt level iii", "ultrasonic technician", "radiographic technician",
    "magnetic particle", "liquid penetrant", "eddy current technician",
    "visual inspection", "asnt certified", "calibration technician", "gage technician",
    "optical inspector", "coordinate measuring", "layout inspector",
    "receiving inspector", "in-process inspector",

    # --- 1H: Tooling & Setup ---
    "tool room", "tooling engineer", "setup technician", "fixture builder",
    "tool designer", "jig and fixture", "tooling technician",

    # --- 1I: Composites & Aerospace Fabrication ---
    "composite technician", "lamination technician", "bonding technician",
    "aerospace assembler", "aircraft technician", "avionics technician",
    "sheet metal mechanic", "structures mechanic", "airframe mechanic",

    # --- 1J: Other Skilled Trades ---
    "carpenter", "painter", "coating technician",
    "surface finisher", "heat treat operator", "chemical processor",
    "machining apprentice", "maintenance apprentice", "journeyman",
    "technician apprentice",

    # ==========================================
    # CATEGORY 2: TECHNICAL LEADERSHIP
    # (HIGH + MEDIUM-HIGH CONFIDENCE)
    # ==========================================

    # --- 2A: Manufacturing & Quality Engineering ---
    "manufacturing engineer", "process engineer", "industrial engineer",
    "manufacturing engineering", "process improvement engineer", "methods engineer",
    "tool engineer", "fixture engineer",
    "quality engineer", "qa engineer", "qc engineer", "quality engineering",
    "supplier quality engineer", "sqa", "quality systems engineer",
    "six sigma", "green belt", "black belt", "asq certified",
    "cqe", "cqa", "cre",

    # --- 2B: Production Supervision ---
    "production supervisor", "manufacturing supervisor", "shop supervisor",
    "maintenance supervisor", "quality supervisor", "shift supervisor",
    "area supervisor", "department supervisor", "assembly supervisor",
    "fabrication supervisor", "machining supervisor",
    "shop foreman", "production foreman", "maintenance foreman",
    "general foreman", "working foreman",
    "lead technician", "senior technician", "master technician",
    "lead machinist", "lead welder", "lead assembler",
    "superintendent", "shop superintendent", "production superintendent",
    "manufacturing superintendent", "maintenance superintendent",

    # --- 2C: Production Planning & Coordination ---
    "production planner", "manufacturing planner", "production scheduler",
    "production control", "material planner", "capacity planner",
    "manufacturing coordinator", "production coordinator", "operations coordinator",
    "shift coordinator", "materials coordinator",
    "cnc programmer", "cam programmer", "manufacturing programmer", "robot programmer",
]


# ======================================================
# COMPANY SIZE DATABASE & ADAPTIVE JOB CAPS
# ======================================================
# PURPOSE: Determine appropriate job caps based on company size
#
# TIER SYSTEM:
#   Tier 1 (10,000+ employees): 50 jobs - Mega-corporations
#   Tier 2 (1,000-9,999 employees): 40 jobs - Major OEMs
#   Tier 3 (200-999 employees): 25 jobs - Medium suppliers
#   Tier 4 (50-199 employees): 15 jobs - Small-medium suppliers
#   Tier 5 (10-49 employees): 10 jobs - Small shops
#
# DATA SOURCE: Public filings, LinkedIn, industry reports (2024-2025)
# MAINTENANCE: Update quarterly with employee count changes

COMPANY_SIZE_DATABASE = {
    # ======================================================
    # TIER 1: MEGA-CORPORATIONS (10,000+ employees)
    # Job Cap: 80 jobs
    # ======================================================
    "Pratt & Whitney": {"employees": 35000, "tier": 1},
    "Pratt Whitney": {"employees": 35000, "tier": 1},  # Variant without &
    "RTX": {"employees": 35000, "tier": 1},
    "Collins Aerospace": {"employees": 15000, "tier": 1},
    "Collins": {"employees": 15000, "tier": 1},

    # ======================================================
    # TIER 2: MAJOR OEMs (1,000-9,999 employees)
    # Job Cap: 40 jobs
    # ======================================================
    "Sikorsky": {"employees": 8000, "tier": 2},
    "Sikorsky Aircraft": {"employees": 8000, "tier": 2},
    "GE Aerospace": {"employees": 3500, "tier": 2},
    "Kaman": {"employees": 2400, "tier": 2},
    "Kaman Corporation": {"employees": 2400, "tier": 2},
    "Barnes Aerospace": {"employees": 1200, "tier": 2},
    "Barnes": {"employees": 1200, "tier": 2},

    # ======================================================
    # TIER 3: MEDIUM SUPPLIERS (200-999 employees)
    # Job Cap: 30 jobs
    # ======================================================
    "GKN Aerospace": {"employees": 800, "tier": 3},
    "GKN": {"employees": 800, "tier": 3},
    "Chromalloy": {"employees": 600, "tier": 3},
    "Ensign-Bickford": {"employees": 500, "tier": 3},
    "Triumph Group": {"employees": 450, "tier": 3},
    "Triumph": {"employees": 450, "tier": 3},
    "Eaton Aerospace": {"employees": 400, "tier": 3},
    "Eaton": {"employees": 400, "tier": 3},
    "Senior Aerospace": {"employees": 350, "tier": 3},
    "Precision Castparts": {"employees": 300, "tier": 3},
    "PCC": {"employees": 300, "tier": 3},
    "Woodward": {"employees": 250, "tier": 3},
    "Heroux-Devtek": {"employees": 200, "tier": 3},

    # ======================================================
    # TIER 4: SMALL-MEDIUM SUPPLIERS (50-199 employees)
    # Job Cap: 20 jobs
    # ======================================================
    "Curtiss-Wright": {"employees": 150, "tier": 4},
    "Aero Gear": {"employees": 120, "tier": 4},
    "Stanadyne": {"employees": 100, "tier": 4},
    "Parker Hannifin": {"employees": 100, "tier": 4},
    "Parker": {"employees": 100, "tier": 4},
    "Breeze-Eastern": {"employees": 90, "tier": 4},
    "TransDigm": {"employees": 90, "tier": 4},
    "Connecticut Spring": {"employees": 85, "tier": 4},
    "Standard Aero": {"employees": 75, "tier": 4},
    "Tyler Technologies": {"employees": 60, "tier": 4},

    # ======================================================
    # TIER 5: SMALL COMPANIES (10-49 employees)
    # Job Cap: 10 jobs
    # ======================================================
    # Note: Most small companies not in database
    # They will default to Tier 99 (Unknown)

    # ======================================================
    # TIER 99: UNKNOWN SIZE
    # Job Cap: 20 jobs (conservative default)
    # Note: Companies not in this database default to Tier 99
    # ======================================================
}

def company_size_lookup(company_name):
    """
    Look up approximate employee count for a company.

    Uses fuzzy matching to handle variations in company names.

    Args:
        company_name (str): Company name from input file

    Returns:
        int: Approximate employee count (None if not found)
    """
    company_name_clean = company_name.lower().strip()

    # Try exact match first
    for known_company, data in COMPANY_SIZE_DATABASE.items():
        if known_company.lower() == company_name_clean:
            return data["employees"]

    # Try partial match (company name contains known company)
    for known_company, data in COMPANY_SIZE_DATABASE.items():
        if known_company.lower() in company_name_clean:
            return data["employees"]

    # Try reverse match (known company contains company name)
    for known_company, data in COMPANY_SIZE_DATABASE.items():
        if company_name_clean in known_company.lower():
            return data["employees"]

    # Company not found - return None (Tier 99 will be assigned)
    return None


def get_company_tier(company_name):
    """
    Determine company tier (1-5 for known sizes, 99 for unknown).

    Tier 1: 10,000+ employees (80 jobs) - Mega-corporations
    Tier 2: 1,000-9,999 employees (40 jobs) - Major OEMs
    Tier 3: 200-999 employees (30 jobs) - Medium suppliers
    Tier 4: 50-199 employees (20 jobs) - Small-medium suppliers
    Tier 5: 10-49 employees (10 jobs) - Small companies
    Tier 99: Unknown size (20 jobs) - No data available

    Args:
        company_name (str): Company name from input file

    Returns:
        int: Tier number (1-5 for known, 99 for unknown)
    """
    # Check if company is in curated database
    if company_name in COMPANY_SIZE_DATABASE:
        return COMPANY_SIZE_DATABASE[company_name]["tier"]

    # Company not in database - classify as unknown
    return 99


def get_job_cap_for_company(company_name):
    """
    Determine maximum jobs to collect for this company based on size.

    This is the MAIN function used in fetch_jobs_for_company()

    Args:
        company_name (str): Company name from input file

    Returns:
        int: Maximum jobs to collect (10, 20, 30, 40, or 80)
    """
    tier = get_company_tier(company_name)

    # Job cap mapping by tier
    job_caps = {
        1: 80,   # Tier 1: Mega-corporations (10,000+ employees)
        2: 40,   # Tier 2: Major OEMs (1,000-9,999 employees)
        3: 30,   # Tier 3: Medium suppliers (200-999 employees)
        4: 20,   # Tier 4: Small-medium suppliers (50-199 employees)
        5: 10,   # Tier 5: Small companies (10-49 employees)
        99: 20   # Tier 99: Unknown size (conservative default)
    }

    return job_caps.get(tier, 20)  # Default to 20 if somehow invalid


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
company_tracking = []  # ADDED: Track all companies attempted (for analytics)


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

def build_trade_query(company_name, keywords=None, max_length=MAX_QUERY_LENGTH, remove_hyphens=False):
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
        remove_hyphens (bool): If True, remove hyphens from company name (fallback)

    RETURNS:
        str: Simple company name query
    """
    # Remove special characters that could interfere with search
    if remove_hyphens:
        # Fallback: Remove hyphens (e.g., "Accu-Rite" → "AccuRite")
        clean_name = re.sub(r"[^a-zA-Z0-9&\s]", "", company_name).strip()
    else:
        # Default: Keep hyphens (critical for companies like "Accu-Rite", "Curtiss-Wright")
        clean_name = re.sub(r"[^a-zA-Z0-9&\s-]", "", company_name).strip()

    # Replace ampersands with space for better Google Jobs API compatibility
    # Google Jobs API has issues with & symbol and "and" connector
    # Example: "Pratt & Whitney" → "Pratt Whitney"
    clean_name = clean_name.replace("&", " ").replace("  ", " ").strip()

    # SIMPLE: Just return company name
    # Google Jobs will find all positions at this company
    # We filter for skilled trades in post-processing

    # Add skilled trades keywords to make valid job query
    # SerpAPI requires a job-type search, not just company name
    # Expanded to include technical leadership (engineers, supervisors) and licensed trades
    return f"{clean_name} machinist OR welder OR fabricator OR technician OR engineer OR supervisor OR electrician OR inspector"

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
    query = build_trade_query(company)
    tried_without_hyphens = False  # Simple fallback flag

    # Adaptive pagination based on company size
    # Get company-specific job cap
    MAX_JOBS = get_job_cap_for_company(company)
    tier = get_company_tier(company)

    # Log the tier and cap for this company
    if tier == 99:
        print(f"[{company}] Tier 99 (Unknown size), Job cap: {MAX_JOBS} (conservative default)")
    else:
        print(f"[{company}] Tier {tier}, Job cap: {MAX_JOBS}")

    # Pagination: Request pages until we hit the cap
    # Each page has ~10 jobs, so we need (MAX_JOBS / 10) pages
    for start in range(0, MAX_JOBS, 10):
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
            "location": "Connecticut, United States",  # Geographic focus
            # "start": start  # Pagination offset
        }

        # Retry logic: Try up to 3 times if connection fails
        response = None
        data = None
        response_time_ms = 0
        for attempt in range(3):
            try:
                request_start = time.time()
                response = safe_api_request(params, company)
                response_time_ms = (time.time() - request_start) * 1000

                if response is None:
                    # API limit reached, return what we've collected so far
                    health_monitor.record_call(
                        status_code=0,
                        company=company,
                        jobs_found=len(local_results),
                        response_time_ms=response_time_ms
                    )
                    return local_results

                # Validate API response using comprehensive validation
                is_valid, data, error_msg = validate_api_response(response, company)
                if is_valid:
                    break  # Success, exit retry loop
                else:
                    print(f"[{company}] Validation failed: {error_msg}")
                    health_monitor.record_call(
                        status_code=response.status_code,
                        company=company,
                        jobs_found=0,
                        response_time_ms=response_time_ms
                    )
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

        # Simple fallback: If first page has no results, try without hyphens once
        if not job_results:
            if start == 0:  # Only check on first page
                if not tried_without_hyphens and "-" in company:
                    # Try query without hyphens (e.g., "Accu-Rite" → "AccuRite")
                    print(f"[{company}] No results — trying without hyphens...")
                    tried_without_hyphens = True
                    query = build_trade_query(company, remove_hyphens=True)
                    continue  # Retry from start
                else:
                    print(f"[{company}] No jobs found — skipping remaining pages.")
                    break
            else:
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
            # Uses smart word-based matching (see is_skilled_trade_job function)
            if is_skilled_trade_job(title):
                employee_count = company_size_lookup(company)
                local_results.append({
                    "Company": company,
                    "Company Tier": tier,  # Tier 1-5 or 99 (Unknown)
                    "Employee Count": employee_count if employee_count else "Unknown",  # Show "Unknown" if None
                    "Job Cap": MAX_JOBS,  # Max jobs for this tier
                    "Job Title": title,
                    "Location": job.get("location", ""),
                    "Via": job.get("via", ""),  # Job board source (Indeed, LinkedIn, etc.)
                    "Source URL": job.get("apply_link", ""),
                    "Detected Extensions": job.get("detected_extensions", {}),
                    "Description Snippet": job.get("description", "")[:200],  # First 200 chars
                    "Timestamp": pd.Timestamp.now()  # When we scraped this job
                })

                # Check if we've reached the job cap for this company
                if len(local_results) >= MAX_JOBS:
                    print(f"[{company}] Reached job cap ({MAX_JOBS} jobs) — stopping pagination.")
                    break

        # Check again after processing all jobs on this page
        if len(local_results) >= MAX_JOBS:
            break

        # Brief pause between pages to avoid triggering rate limits
        time.sleep(1)

    # Record successful processing in health monitor
    health_monitor.record_call(
        status_code=200,
        company=company,
        jobs_found=len(local_results),
        response_time_ms=response_time_ms if 'response_time_ms' in locals() else 0
    )

    print(f"[{company}] → {len(local_results)} skilled-trade jobs found")

    # ADDED: Track company-level metrics for analytics
    global company_tracking
    employee_count = company_size_lookup(company)
    company_tracking.append({
        "Company": company,
        "Tier": tier,
        "Employee Count": employee_count if employee_count else "Unknown",
        "Job Cap": MAX_JOBS,
        "Jobs Found": len(local_results),
        "Success": len(local_results) > 0
    })

    return local_results


# ======================================================
# MAIN EXECUTION: Batch Processing with Rate Limit Protection
# ======================================================
# PURPOSE: Process companies in controlled batches to prevent API blocking
#
# HOW IT WORKS:
#   - Batch processor groups companies into batches (10 companies each)
#   - Each batch is processed with pauses between batches
#   - Rate limiter ensures safe spacing between API calls
#   - Circuit breaker stops processing if too many failures occur
#
# FEATURES:
#   - Batch processing: 10 companies per batch (human-like pattern)
#   - Automatic pauses: 2-5 minutes between batches (prevents IP blocking)
#   - Progressive checkpoints: Save results every 25 companies (prevents data loss)
#   - Error handling: Individual company failures don't crash entire process
#   - Health monitoring: Real-time alerts for API issues
#
# PERFORMANCE:
#   - ~40-50 minutes for 137 companies (safe, sustainable pace)
#   - ~3 seconds between API calls (prevents rate limiting)
#   - ~14 batches with automatic pauses (mimics human behavior)
#   - Bottleneck: Intentionally slowed for API compliance

print(f"\n{'='*70}")
print(f"Starting batch processing: {len(companies)} companies")
print(f"{'='*70}\n")

# Process companies in batches
for i, company in enumerate(tqdm(companies, desc="Processing companies")):
    try:
        # Check if we should stop (circuit breaker, API limit, etc.)
        if api_limit_reached:
            print(f"\n⚠️ Processing stopped: API limit reached")
            break

        # Process single company
        company_results = fetch_jobs_for_company(company)
        results.extend(company_results)  # Add to master results list

        # CHECK FOR FALLBACK TRIGGER: Detect API health issues
        should_fallback, reason = health_monitor.should_trigger_fallback()
        if should_fallback:
            print(f"\n{'='*60}")
            print(f"🚨 FALLBACK TRIGGER DETECTED: {reason}")
            print(f"{'='*60}")
            print(health_monitor.get_summary())
            print(f"\n⚠️ SerpAPI appears to have issues. Stopping to prevent IP block.")
            print(f"   Check log/api_audit.jsonl for detailed analysis.")
            print(f"{'='*60}\n")
            break  # Stop processing to prevent further issues

        # CHECKPOINT SAVE: Every 25 companies, save progress to disk
        # This prevents losing all data if script crashes or API limit is hit
        if (i + 1) % 25 == 0 and results:
            pd.DataFrame(results).drop_duplicates(subset=["Company", "Job Title", "Source URL"]).to_excel(OUTPUT_FILE, index=False)
            print(f"💾 Checkpoint saved ({len(results)} total records)")

        # BATCH PAUSE: Every 10 companies, take a human-like break
        if (i + 1) % 10 == 0 and (i + 1) < len(companies):
            pause_duration = int(batch_processor.calculate_pause())
            print(f"\n⏸️  Batch {(i + 1) // 10} complete. Pausing for {pause_duration} seconds...")

            # ===== OPTION 1: SIMPLE COUNTDOWN (COMMENTED OUT) =====
            # Uncomment this section and comment out Option 2 below for simple countdown
            # print(f"   This prevents API rate limiting and mimics human behavior.")
            # for remaining in range(pause_duration, 0, -15):
            #     print(f"   ⏳ {remaining} seconds remaining...")
            #     time.sleep(15)
            # print(f"▶️  Resuming processing...\n")

            # ===== OPTION 2: PROGRESS BAR (ACTIVE) =====
            # Comment this section and uncomment Option 1 above for simple countdown
            print(f"   Prevents API rate limiting and mimics human behavior")
            with tqdm(total=pause_duration, desc="  Pausing", unit="s",
                      bar_format='{l_bar}{bar}| {n:.0f}/{total:.0f}s') as pbar:
                for j in range(pause_duration):
                    time.sleep(1)
                    pbar.update(1)
            print(f"▶️  Resuming processing...\n")

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
        from resources.analytics import JobAnalytics

        analytics_output = OUTPUT_FILE.replace(".xlsx", "_Analytics.xlsx")
        analytics = JobAnalytics(final_df, company_tracking)  # ADDED: Pass company tracking data
        analytics.generate_report(analytics_output)

    except ImportError:
        print("\n⚠️ Analytics module not found. Skipping analytics generation.")
        print("   To enable analytics, ensure 'analytics.py' is in resources/ directory.")
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

