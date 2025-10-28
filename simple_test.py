import json
from serpapi import GoogleSearch

with open('resources/config.json', 'r') as f:
    config = json.load(f)

api_key = config['api_keys'][0]['key']

print("TEST 1: Simple query (we know this works)")
print("="*60)
params = {
    "engine": "google_jobs",
    "q": "Barnes Aerospace machinist",
    "api_key": api_key
}

search = GoogleSearch(params)
results = search.get_dict()

if 'error' in results:
    print(f"❌ Error: {results['error']}")
else:
    jobs = results.get('jobs_results', [])
    print(f"✅ SUCCESS! Found {len(jobs)} jobs")

print("\n" + "="*60)
print("TEST 2: With OR operators")
print("="*60)
params2 = {
    "engine": "google_jobs",
    "q": "Barnes Aerospace machinist OR welder",
    "api_key": api_key
}

search2 = GoogleSearch(params2)
results2 = search2.get_dict()

if 'error' in results2:
    print(f"❌ Error: {results2['error']}")
else:
    jobs2 = results2.get('jobs_results', [])
    print(f"✅ SUCCESS! Found {len(jobs2)} jobs")

print("\n" + "="*60)
print("TEST 3: Full company name")
print("="*60)
params3 = {
    "engine": "google_jobs",
    "q": "Barnes Aerospace East Granby machinist",
    "api_key": api_key
}

search3 = GoogleSearch(params3)
results3 = search3.get_dict()

if 'error' in results3:
    print(f"❌ Error: {results3['error']}")
else:
    jobs3 = results3.get('jobs_results', [])
    print(f"✅ SUCCESS! Found {len(jobs3)} jobs")