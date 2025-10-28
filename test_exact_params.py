import json
from serpapi import GoogleSearch

with open('resources/config.json', 'r') as f:
    config = json.load(f)

api_key = config['api_keys'][0]['key']

print("TEST 1: Without hl and start")
print("="*60)
params1 = {
    "engine": "google_jobs",
    "q": "Barnes Aerospace East Granby machinist OR welder OR fabricator OR technician",
    "api_key": api_key
}

search1 = GoogleSearch(params1)
results1 = search1.get_dict()

if 'error' in results1:
    print(f"❌ Error: {results1['error']}")
else:
    jobs1 = results1.get('jobs_results', [])
    print(f"✅ SUCCESS! Found {len(jobs1)} jobs")

print("\n" + "="*60)
print("TEST 2: WITH hl=en and start=0 (EXACT AeroComps)")
print("="*60)
params2 = {
    "engine": "google_jobs",
    "q": "Barnes Aerospace East Granby machinist OR welder OR fabricator OR technician",
    "api_key": api_key,
    "hl": "en",
    "start": 0
}

search2 = GoogleSearch(params2)
results2 = search2.get_dict()

if 'error' in results2:
    print(f"❌ Error: {results2['error']}")
else:
    jobs2 = results2.get('jobs_results', [])
    print(f"✅ SUCCESS! Found {len(jobs2)} jobs")