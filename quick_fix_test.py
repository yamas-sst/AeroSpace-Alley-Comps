import json
from serpapi import GoogleSearch

# Load config
with open('resources/config.json', 'r') as f:
    config = json.load(f)

api_key = config['api_keys'][0]['key']

# Test with proper query format
params = {
    "engine": "google_jobs",
    "q": "Barnes Aerospace machinist OR welder OR fabricator",  # Added keywords!
    "api_key": 4aa81d243250039b571ae3b331214224e0f253369166f54273fa553355c9eaf7,
    "hl": "en"
}

print("Testing query with keywords...")
print(f"Query: {params['q']}")

search = GoogleSearch(params)
results = search.get_dict()

if 'error' in results:
    print(f"❌ Error: {results['error']}")
else:
    jobs = results.get('jobs_results', [])
    print(f"✅ SUCCESS! Found {len(jobs)} jobs")
    if jobs:
        for i, job in enumerate(jobs[:3], 1):
            print(f"{i}. {job.get('title')} at {job.get('company_name')}")