#!/usr/bin/env python3
"""
Quick Block Status Checker
Run this every few hours to see if block has cleared
"""

import requests
import json
from datetime import datetime

# Load config
with open('resources/config.json', 'r') as f:
    config = json.load(f)

api_key = config['api_keys'][0]['key']
api_label = config['api_keys'][0]['label']

print(f"\n{'='*60}")
print(f"Quick Block Status Check - {datetime.now().strftime('%H:%M:%S')}")
print(f"{'='*60}\n")

print(f"Testing API Key: {api_label}")
print("Making test request to SerpAPI...")

try:
    params = {
        'engine': 'google_jobs',
        'q': 'test',
        'api_key': api_key
    }

    response = requests.get(
        'https://serpapi.com/search.json',
        params=params,
        timeout=30
    )

    if response.status_code == 200:
        print("\n✅ SUCCESS! Block has been lifted!")
        print("   Status: 200 OK")
        print("   You can now run your job scanner")
        print("\n   Next step: Run test with 1 company")
        print("   Command: python AeroComps.py")

    elif response.status_code == 403:
        print("\n❌ Still blocked (403 - Access Denied)")
        print("   Status: IP block still active")
        print("   Suggestion: Try again in a few hours")

    elif response.status_code == 429:
        print("\n⚠️  Rate limited (429 - Too Many Requests)")
        print("   Status: Soft rate limit")
        print("   Suggestion: Wait 1 hour and try again")

    elif response.status_code == 401:
        print("\n❌ Invalid API key (401 - Unauthorized)")
        print("   Status: API key issue")
        print("   Suggestion: Check your API key in config.json")

    elif response.status_code == 402:
        print("\n❌ Credits exhausted (402 - Payment Required)")
        print("   Status: Account quota used up")
        print("   Suggestion: Add more credits or use different key")

    else:
        print(f"\n⚠️  Unexpected status: {response.status_code}")
        print(f"   Response: {response.text[:200]}")

except Exception as e:
    print(f"\n❌ Connection error: {e}")
    print("   Check your internet connection")

print(f"\n{'='*60}\n")
