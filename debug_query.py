import json
from serpapi import GoogleSearch

# Load config
with open('resources/config.json', 'r') as f:
    config = json.load(f)

api_key = config['api_keys'][0]['key']
company = "Barnes Aerospace"

# Test different LOCATION formats
queries = [
    # Format 1: Just state
    {
        "engine": "google_jobs",
        "q": f"{company} machinist",
        "location": "Connecticut",
        "api_key": api_key
    },
    # Format 2: City, State (no USA)
    {
        "engine": "google_jobs",
        "q": f"{company} machinist",
        "location": "East Granby, Connecticut",
        "api_key": api_key
    },
    # Format 3: No location parameter at all
    {
        "engine": "google_jobs",
        "q": f"{company} machinist Connecticut",
        "api_key": api_key
    },
    # Format 4: State abbreviation
    {
        "engine": "google_jobs",
        "q": f"{company} machinist",
        "location": "CT",
        "api_key": api_key
    },
]

for i, params in enumerate(queries, 1):
    print(f"\n{'='*60}")
    print(f"TEST {i}: q='{params.get('q', 'N/A')}' | location='{params.get('location', 'NONE')}'")
    print(f"{'='*60}")
    
    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        
        if 'error' in results:
            print(f"❌ Error: {results['error']}")
        else:
            jobs = results.get('jobs_results', [])
            print(f"✅ SUCCESS! Found {len(jobs)} jobs")
            if jobs:
                print(f"   Sample job: {jobs[0].get('title', 'N/A')}")
                print(f"   Company: {jobs[0].get('company_name', 'N/A')}")
    except Exception as e:
        print(f"❌ Exception: {e}")