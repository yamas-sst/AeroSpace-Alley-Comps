#!/usr/bin/env python3
"""
SerpAPI Block Diagnostic Tool
Tests various scenarios to determine the exact nature of the block
"""

import requests
import json
import time
from datetime import datetime

# Load config
with open('resources/config.json', 'r') as f:
    config = json.load(f)

print("="*80)
print("SERPAPI BLOCK DIAGNOSTIC TOOL")
print("="*80)
print(f"Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Test scenarios
results = {}

# =============================================================================
# TEST 1: Check HTTP response headers for rate limit info
# =============================================================================
print("\n" + "="*80)
print("TEST 1: Checking Response Headers for Rate Limit Info")
print("="*80)

api_key = config['api_keys'][0]['key']
params = {
    'engine': 'google_jobs',
    'q': 'test',
    'api_key': api_key
}

try:
    response = requests.get(
        'https://serpapi.com/search.json',
        params=params,
        timeout=30
    )

    print(f"\nStatus Code: {response.status_code}")
    print("\nResponse Headers:")
    for header, value in response.headers.items():
        print(f"  {header}: {value}")

    # Look for rate limit headers
    rate_limit_headers = [
        'X-RateLimit-Limit',
        'X-RateLimit-Remaining',
        'X-RateLimit-Reset',
        'Retry-After',
        'X-Rate-Limit-Limit',
        'X-Rate-Limit-Remaining',
        'X-Rate-Limit-Reset'
    ]

    print("\nRate Limit Headers Found:")
    found_any = False
    for header in rate_limit_headers:
        if header in response.headers:
            print(f"  {header}: {response.headers[header]}")
            found_any = True

    if not found_any:
        print("  None found (SerpAPI may not expose these)")

    results['test1_status'] = response.status_code
    results['test1_headers'] = dict(response.headers)

    # Try to parse body
    try:
        body = response.json()
        print(f"\nResponse Body:")
        print(json.dumps(body, indent=2)[:500])
    except:
        print(f"\nResponse Body (text):")
        print(response.text[:500])

except Exception as e:
    print(f"\nERROR: {e}")
    results['test1_error'] = str(e)

# =============================================================================
# TEST 2: Try account status endpoint
# =============================================================================
print("\n" + "="*80)
print("TEST 2: Checking Account Status Endpoint")
print("="*80)

try:
    account_url = f'https://serpapi.com/account.json?api_key={api_key}'
    response = requests.get(account_url, timeout=30)

    print(f"\nStatus Code: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print("\nAccount Information:")
        print(f"  Total Searches Left: {data.get('total_searches_left', 'N/A')}")
        print(f"  Plan: {data.get('plan_name', 'N/A')}")
        print(f"  Account Email: {data.get('account_email', 'N/A')}")
        print(f"  Rate Limit (per hour): {data.get('rate_limit_per_hour', 'N/A')}")
        print(f"  This Month Searches: {data.get('this_month_usage', 'N/A')}")

        results['test2_account_info'] = data

        if data.get('total_searches_left', 0) == 0:
            print("\n⚠️  FINDING: Account has 0 searches left (quota exhausted)")

    else:
        print(f"\nAccount endpoint also blocked: {response.status_code}")
        print(response.text[:200])
        results['test2_status'] = response.status_code

except Exception as e:
    print(f"\nERROR: {e}")
    results['test2_error'] = str(e)

# =============================================================================
# TEST 3: Test all API keys from same IP
# =============================================================================
print("\n" + "="*80)
print("TEST 3: Testing All API Keys from Same IP")
print("="*80)

for idx, api_key_info in enumerate(config['api_keys'], 1):
    print(f"\n--- API Key {idx}: {api_key_info['label']} ---")

    params = {
        'engine': 'google_jobs',
        'q': 'test',
        'api_key': api_key_info['key']
    }

    try:
        response = requests.get(
            'https://serpapi.com/search.json',
            params=params,
            timeout=30
        )

        print(f"Status: {response.status_code}")

        if response.status_code == 403:
            print("Result: BLOCKED (403)")
        elif response.status_code == 429:
            print("Result: RATE LIMITED (429)")
        elif response.status_code == 401:
            print("Result: INVALID KEY (401)")
        elif response.status_code == 200:
            print("Result: SUCCESS (200)")
        else:
            print(f"Result: UNKNOWN ({response.status_code})")

        results[f'test3_key{idx}'] = response.status_code

    except Exception as e:
        print(f"ERROR: {e}")
        results[f'test3_key{idx}_error'] = str(e)

# =============================================================================
# TEST 4: Check what IP we're using
# =============================================================================
print("\n" + "="*80)
print("TEST 4: Determining Current IP Address")
print("="*80)

ip_services = [
    'https://api.ipify.org?format=json',
    'https://ifconfig.me/ip',
    'https://icanhazip.com'
]

for service in ip_services:
    try:
        response = requests.get(service, timeout=10)
        if response.status_code == 200:
            if 'json' in service:
                ip = response.json().get('ip', 'Unknown')
            else:
                ip = response.text.strip()
            print(f"\nYour IP Address: {ip}")
            results['current_ip'] = ip
            break
    except Exception as e:
        continue
else:
    print("\nCould not determine IP (network restrictions)")
    results['current_ip'] = 'Unknown (network blocked)'

# =============================================================================
# TEST 5: Simple connectivity test (is internet working?)
# =============================================================================
print("\n" + "="*80)
print("TEST 5: Internet Connectivity Test")
print("="*80)

try:
    response = requests.get('https://www.google.com', timeout=10)
    print(f"\nGoogle Status: {response.status_code} (Internet is working)")
    results['test5_internet'] = 'working'
except Exception as e:
    print(f"\nInternet test failed: {e}")
    results['test5_internet'] = 'failed'

# =============================================================================
# ANALYSIS
# =============================================================================
print("\n" + "="*80)
print("DIAGNOSIS & ANALYSIS")
print("="*80)

# Determine block type
print("\n1. BLOCK TYPE:")
test3_all_blocked = all(
    results.get(f'test3_key{i}') == 403
    for i in range(1, len(config['api_keys']) + 1)
    if f'test3_key{i}' in results
)

if test3_all_blocked:
    print("   ✅ CONFIRMED: IP-Level Block")
    print("   - All API keys return 403 from same IP")
    print("   - This is NOT an account issue")
    print("   - This is NOT an API key issue")
    print("   - Your IP address has been blocked by SerpAPI")
else:
    print("   ⚠️  MIXED: Partial block or key-specific issue")

# Check account status
print("\n2. ACCOUNT STATUS:")
if 'test2_account_info' in results:
    account_data = results['test2_account_info']
    searches_left = account_data.get('total_searches_left', 'Unknown')
    print(f"   Searches Remaining: {searches_left}")
    if searches_left == 0:
        print("   ⚠️  Account quota exhausted (but this shows as 402, not 403)")
else:
    print("   ❌ Cannot access account endpoint (also blocked)")

# Check for rate limit headers
print("\n3. RATE LIMIT HEADERS:")
if results.get('test1_headers'):
    retry_after = results['test1_headers'].get('Retry-After')
    if retry_after:
        print(f"   ⏰ Retry-After header found: {retry_after} seconds")
        print(f"   Expected unblock: {datetime.now().timestamp() + int(retry_after)}")
    else:
        print("   ❌ No Retry-After header (SerpAPI doesn't provide it)")
        print("   - Cannot determine exact unblock time from API")
else:
    print("   ❌ No headers available")

# Provide recommendations
print("\n4. HOW TO VERIFY IT'S AN IP BLOCK:")
print("\n   METHOD 1: Try from Different Network (DEFINITIVE)")
print("   - Use mobile hotspot (different carrier)")
print("   - Use VPN service")
print("   - Try from home (if currently at office)")
print("   - Try from coffee shop WiFi")
print("   - If it WORKS from different network → CONFIRMS IP block")
print("   - If it FAILS from different network → Account or key issue")

print("\n   METHOD 2: Wait and Retry Periodically")
print("   - Typical IP blocks: 1-48 hours")
print("   - Most common: 24 hours")
print("   - Check every 6 hours:")
print(f"     • Now: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print(f"     • +6h: {datetime.fromtimestamp(time.time() + 21600).strftime('%Y-%m-%d %H:%M')}")
print(f"     • +12h: {datetime.fromtimestamp(time.time() + 43200).strftime('%Y-%m-%d %H:%M')}")
print(f"     • +24h: {datetime.fromtimestamp(time.time() + 86400).strftime('%Y-%m-%d %H:%M')}")

print("\n   METHOD 3: Contact SerpAPI Support")
print("   - Email: support@serpapi.com")
print("   - Ask: 'How long is IP block duration?'")
print("   - Ask: 'Can you unblock my IP manually?'")
print(f"   - Provide: Your IP ({results.get('current_ip', 'Unknown')})")

# Save results
print("\n" + "="*80)
print("SAVING DIAGNOSTIC RESULTS")
print("="*80)

results['timestamp'] = datetime.now().isoformat()
results['diagnosis'] = 'IP-level block' if test3_all_blocked else 'Unknown'

output_file = 'log/block_diagnostic.json'
with open(output_file, 'w') as f:
    json.dump(results, f, indent=2)

print(f"\nResults saved to: {output_file}")
print("\n✅ Diagnostic complete!")
print("\nNEXT STEPS:")
print("1. Try from different network to confirm IP block")
print("2. If confirmed, wait 24 hours and retry")
print("3. Or contact support@serpapi.com for manual unblock")
