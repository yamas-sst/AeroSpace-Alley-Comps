import sys
import json

# Add the path to import from AeroComps
sys.path.insert(0, '.')

from AeroComps import build_trade_query, SKILLED_TRADES_KEYWORDS

company = "Barnes Aerospace East Granby"
query = build_trade_query(company, SKILLED_TRADES_KEYWORDS)

print(f"Company: {company}")
print(f"Query: {query}")
print(f"Query length: {len(query)} characters")
print(f"\nMax allowed: 200 characters")

# Show what would be sent to API
params = {
    "engine": "google_jobs",
    "q": query,
    "api_key": "4aa81d243250039b571ae3b331214224e0f253369166f54273fa553355c9eaf7",
    "hl": "en"
}

print(f"\nParams that would be sent:")
for key, value in params.items():
    if key == "api_key":
        print(f"  {key}: {value[:20]}...")
    else:
        print(f"  {key}: {value}")