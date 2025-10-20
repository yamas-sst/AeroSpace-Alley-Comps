# ======================================================
# Aerospace Alley Skilled Trades Job Scanner
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

# === CONFIGURATION ===
API_KEY = "4aa81d243250039b571ae3b331214224e0f253369166f54273fa553355c9eaf7"  # (kept as-is per request)
INPUT_FILE = r"C:\Users\JoseYamas\Desktop\SST Core Projects\Zac\AeroSpace Alley Comps\Aerospace_Alley_Companies.xlsx"
OUTPUT_FILE = "Aerospace_Alley_SkilledTrades_Jobs.xlsx"
MAX_QUERY_LENGTH = 200
MAX_THREADS = 5  # adjust to stay under SerpApi rate limits


api_lock = Lock()
api_calls = 0
MAX_API_CALLS = 250

# === GLOBAL RATE LIMIT CONTROL ===
last_call_time = 0
MIN_INTERVAL = 1.2  # seconds between API calls globally to avoid burst rate issues

def safe_api_request(params, company):
    global api_calls, last_call_time
    with api_lock:
        if api_calls >= MAX_API_CALLS:
            print(f"[{company}] API limit reached — skipping further requests.")
            return None
        
        # enforce global rate spacing
        now = time.time()
        elapsed = now - last_call_time
        if elapsed < MIN_INTERVAL:
            time.sleep(MIN_INTERVAL - elapsed)
        last_call_time = time.time()
        
        api_calls += 1
        print(f"API call #{api_calls + 1} → {company}")
    return requests.get("https://serpapi.com/search.json", params=params)


# === SKILLED TRADES KEYWORDS ===
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

# === STEP 1: Load Aerospace Alley Company List ===
df = pd.read_excel(INPUT_FILE)
companies = df["Company Name"].dropna().unique()
results = []


def build_trade_query(company_name, keywords, max_length=MAX_QUERY_LENGTH):
    """Builds job search query ensuring length limit compliance."""
    clean_name = re.sub(r"[^a-zA-Z0-9&\s]", "", company_name).strip()
    query_parts = []
    for kw in keywords:
        tentative = f"{clean_name} {' OR '.join(query_parts + [kw])}"
        if len(tentative) > max_length:
            break
        query_parts.append(kw)
    return f"{clean_name} " + " OR ".join(query_parts)


def fetch_jobs_for_company(company):
    """Queries SerpApi for job results and returns filtered skilled-trade listings."""
    local_results = []
    query = build_trade_query(company, SKILLED_TRADES_KEYWORDS)

    for start in range(0, 30, 10):  # up to 3 pages
        params = {
            "engine": "google_jobs",
            "q": query,
            "api_key": API_KEY,
            "hl": "en",
            "start": start
        }

        for attempt in range(3):  # retry logic
            try:
                response = safe_api_request(params, company)
                if response.status_code == 200:
                    break
                time.sleep(3)
            except Exception as e:
                print(f"[{company}] Connection error, retrying... {e}")
                time.sleep(3)

        if not response.ok:
            print(f"[{company}] Skipped (HTTP {response.status_code})")
            continue

        data = response.json()

        job_results = data.get("jobs_results", [])

        # Stop further pagination if no jobs were found in the first call
        if not job_results:
            if start == 0:  # only stop if first page is empty
                print(f"[{company}] No jobs found — skipping remaining pages.")
                break

        for job in job_results:
            title = job.get("title", "")
            if any(kw.lower() in title.lower() for kw in SKILLED_TRADES_KEYWORDS):
                local_results.append({
                    "Company": company,
                    "Job Title": title,
                    "Location": job.get("location", ""),
                    "Via": job.get("via", ""),
                    "Source URL": job.get("apply_link", ""),
                    "Detected Extensions": job.get("detected_extensions", {}),
                    "Description Snippet": job.get("description", "")[:200],
                    "Timestamp": pd.Timestamp.now()
                })

        time.sleep(1)

    print(f"[{company}] → {len(local_results)} skilled-trade jobs found")
    return local_results


# === STEP 2: Process Companies in Parallel ===
with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
    futures = {executor.submit(fetch_jobs_for_company, company): company for company in companies}

    for i, future in enumerate(tqdm(as_completed(futures), total=len(futures), desc="Processing companies")):
        company = futures[future]
        try:
            company_results = future.result()
            results.extend(company_results)

            # Progressive save every 25 companies
            if i % 25 == 0 and results:
                pd.DataFrame(results).drop_duplicates(subset=["Company", "Job Title", "Source URL"]).to_excel(OUTPUT_FILE, index=False)
                print(f"Checkpoint saved ({len(results)} total records).")

        except Exception as e:
            print(f"⚠️ Error processing {company}: {e}")


# === STEP 3: Final Export ===
if results:
    final_df = pd.DataFrame(results).drop_duplicates(subset=["Company", "Job Title", "Source URL"])
    final_df.to_excel(OUTPUT_FILE, index=False)
    print(f"\n✅ Completed! {len(final_df)} skilled-trade jobs saved to {OUTPUT_FILE}")
else:
    print("\n⚠️ No skilled-trade jobs found. Try adjusting keywords or company list.")

