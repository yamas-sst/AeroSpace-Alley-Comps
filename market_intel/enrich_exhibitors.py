#!/usr/bin/env python3
"""
Exhibitor Contact Enrichment Pipeline

Usage:
    python market_intel/enrich_exhibitors.py --mock              # Test mode
    python market_intel/enrich_exhibitors.py                     # Production
    python market_intel/enrich_exhibitors.py --input data/my.csv # Custom input
"""

import os
import sys
import json
import argparse
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from market_intel.connectors.base import Company, EnrichmentResult
from market_intel.connectors.apollo import ApolloConnector, MockApolloConnector


def load_config(config_path: str = "market_intel/config.json") -> Dict[str, Any]:
    """Load configuration from JSON file."""
    if not os.path.exists(config_path):
        return {
            "input_file": "market_intel/data/exhibitors.csv",
            "output_file": "market_intel/output/enriched_contacts.xlsx",
            "enrichment": {
                "provider": "apollo",
                "api_key": "YOUR_API_KEY_HERE",
                "rate_limit": {"calls_per_minute": 10}
            }
        }
    with open(config_path, 'r') as f:
        return json.load(f)


def load_exhibitors(input_file: str) -> List[Company]:
    """Load exhibitor data from CSV file."""
    if not os.path.exists(input_file):
        print(f"[ERROR] Input file not found: {input_file}")
        sys.exit(1)

    df = pd.read_csv(input_file)
    companies = []

    for _, row in df.iterrows():
        company = Company(
            name=str(row.get('company_name', '')).strip(),
            booth_number=str(row.get('booth_number', '')).strip(),
            address=str(row.get('address', '')).strip(),
            city=str(row.get('city', '')).strip(),
            state=str(row.get('state', '')).strip(),
            zip_code=str(row.get('zip', '')).strip(),
            country=str(row.get('country', 'USA')).strip(),
            website=str(row.get('website', '')).strip(),
            description=str(row.get('description', '')).strip(),
            category=str(row.get('category', '')).strip()
        )
        if company.name and company.name.lower() != 'nan':
            companies.append(company)

    print(f"[LOAD] {len(companies)} companies from {input_file}")
    return companies


def export_to_excel(results: List[EnrichmentResult], output_file: str, config: Dict):
    """Export enrichment results to Excel."""
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    contact_rows = []
    company_rows = []

    for result in results:
        company = result.company
        company_rows.append({
            "Company Name": company.name,
            "Booth Number": company.booth_number,
            "Website": company.website,
            "Address": f"{company.address}, {company.city}, {company.state} {company.zip_code}".strip(", "),
            "Status": "Success" if result.success else "Failed",
            "Contacts Found": len(result.contacts),
            "Error": result.error_message
        })

        for contact in result.contacts:
            contact_rows.append({
                "Company Name": company.name,
                "Booth Number": company.booth_number,
                "Company Website": company.website,
                "Contact Name": contact.full_name,
                "Title": contact.title,
                "Department": contact.department,
                "Email": contact.email,
                "Phone": contact.phone,
                "LinkedIn": contact.linkedin_url,
                "Source": contact.source,
                "Source Record ID": contact.source_record_id,
                "Enriched At": contact.enriched_at.strftime("%Y-%m-%d %H:%M:%S"),
                "Confidence": f"{contact.confidence_score:.0%}"
            })

    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        if contact_rows:
            pd.DataFrame(contact_rows).to_excel(writer, sheet_name="Contacts", index=False)
        pd.DataFrame(company_rows).to_excel(writer, sheet_name="Companies", index=False)

        metadata = pd.DataFrame({
            "Field": ["Generated At", "Total Companies", "Successful", "Failed", "Total Contacts", "Provider"],
            "Value": [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                len(results),
                sum(1 for r in results if r.success),
                sum(1 for r in results if not r.success),
                sum(len(r.contacts) for r in results),
                config.get('enrichment', {}).get('provider', 'unknown')
            ]
        })
        metadata.to_excel(writer, sheet_name="Metadata", index=False)

    print(f"[SAVE] {output_file}")


def main():
    parser = argparse.ArgumentParser(description='Exhibitor Contact Enrichment')
    parser.add_argument('--input', type=str, help='Input CSV file')
    parser.add_argument('--output', type=str, help='Output Excel file')
    parser.add_argument('--mock', action='store_true', help='Use mock data (no API)')
    parser.add_argument('--config', type=str, default='market_intel/config.json')
    args = parser.parse_args()

    print("\n" + "=" * 60)
    print("EXHIBITOR CONTACT ENRICHMENT")
    print("=" * 60)

    config = load_config(args.config)
    input_file = args.input or config.get('input_file')
    output_file = args.output or config.get('output_file')

    companies = load_exhibitors(input_file)
    if not companies:
        print("[ERROR] No companies to process")
        sys.exit(1)

    enrichment_config = config.get('enrichment', {})
    enrichment_config['log_file'] = 'log/enrichment_audit.jsonl'

    if args.mock:
        print("[MODE] Mock (no API calls)")
        connector = MockApolloConnector(enrichment_config)
    else:
        api_key = enrichment_config.get('api_key', '')
        if not api_key or api_key == 'YOUR_API_KEY_HERE' or api_key == 'YOUR_APOLLO_API_KEY_HERE':
            print("[ERROR] No API key configured. Use --mock for testing.")
            sys.exit(1)
        print("[MODE] Production (Apollo.io)")
        connector = ApolloConnector(enrichment_config)

    print("\n" + "-" * 60)
    results = connector.enrich_batch(companies)
    print("-" * 60)

    # Summary
    successful = sum(1 for r in results if r.success)
    total_contacts = sum(len(r.contacts) for r in results)
    print(f"\n[SUMMARY] {successful}/{len(results)} companies enriched, {total_contacts} contacts found")

    export_to_excel(results, output_file, config)
    print("\n[DONE]")


if __name__ == "__main__":
    main()
