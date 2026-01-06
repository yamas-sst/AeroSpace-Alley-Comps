#!/usr/bin/env python3
"""
Exhibitor Contact Enrichment Pipeline

Usage:
    python enrich_exhibitors.py                      # Use config defaults
    python enrich_exhibitors.py --input data/exhibitors.csv
    python enrich_exhibitors.py --mock               # Test with mock data (no API calls)

Workflow:
    1. Load exhibitor data from CSV
    2. Enrich each company with contacts via Apollo.io (or mock)
    3. Export to Excel with full provenance
"""

import os
import sys
import json
import argparse
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any

# Add parent directory for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from market_intel.connectors.base import Company, Contact, EnrichmentResult
from market_intel.connectors.apollo import ApolloConnector, MockApolloConnector


def load_config(config_path: str = "market_intel/config.json") -> Dict[str, Any]:
    """Load configuration from JSON file."""
    if not os.path.exists(config_path):
        print(f"❌ Config file not found: {config_path}")
        print("   Creating default config...")
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
        print(f"❌ Input file not found: {input_file}")
        print(f"   Please create your exhibitor list or use the template:")
        print(f"   market_intel/templates/exhibitor_input_template.csv")
        sys.exit(1)

    df = pd.read_csv(input_file)
    companies = []

    print(f"\n📋 Loading exhibitors from: {input_file}")
    print(f"   Found {len(df)} companies")

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

        # Skip empty rows
        if company.name and company.name.lower() != 'nan':
            companies.append(company)

    print(f"   Loaded {len(companies)} valid companies")
    return companies


def export_to_excel(results: List[EnrichmentResult], output_file: str, config: Dict):
    """Export enrichment results to Excel with multiple sheets."""

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Build flat data for main sheet (one row per contact)
    contact_rows = []
    company_rows = []
    failed_rows = []

    for result in results:
        company = result.company

        # Track company-level data
        company_row = {
            "Company Name": company.name,
            "Booth Number": company.booth_number,
            "Address": company.address,
            "City": company.city,
            "State": company.state,
            "Zip": company.zip_code,
            "Country": company.country,
            "Website": company.website,
            "Description": company.description,
            "Category": company.category,
            "Enrichment Status": "Success" if result.success else "Failed",
            "Contacts Found": len(result.contacts),
            "Error": result.error_message
        }
        company_rows.append(company_row)

        if result.success and result.contacts:
            for contact in result.contacts:
                contact_row = {
                    # Company info
                    "Company Name": company.name,
                    "Booth Number": company.booth_number,
                    "Company Website": company.website,
                    "Company Address": f"{company.address}, {company.city}, {company.state} {company.zip_code}".strip(", "),

                    # Contact info
                    "Contact Name": contact.full_name,
                    "Title": contact.title,
                    "Department": contact.department,
                    "Seniority": contact.seniority,
                    "Email": contact.email,
                    "Phone": contact.phone,
                    "LinkedIn": contact.linkedin_url,

                    # Provenance
                    "Enrichment Source": contact.source,
                    "Source Record ID": contact.source_record_id,
                    "Enriched At": contact.enriched_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "Confidence Score": f"{contact.confidence_score:.0%}"
                }
                contact_rows.append(contact_row)

        elif not result.success:
            failed_rows.append({
                "Company Name": company.name,
                "Website": company.website,
                "Error": result.error_message
            })

    # Create Excel writer
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # Main sheet: Contacts
        if contact_rows:
            contacts_df = pd.DataFrame(contact_rows)
            contacts_df.to_excel(writer, sheet_name="Contacts", index=False)
            print(f"   ✅ Contacts sheet: {len(contact_rows)} rows")
        else:
            # Empty contacts sheet
            pd.DataFrame(columns=["Company Name", "Contact Name", "Email"]).to_excel(
                writer, sheet_name="Contacts", index=False
            )
            print(f"   ⚠️ Contacts sheet: 0 rows")

        # Company summary sheet
        if company_rows:
            companies_df = pd.DataFrame(company_rows)
            companies_df.to_excel(writer, sheet_name="Companies", index=False)
            print(f"   ✅ Companies sheet: {len(company_rows)} rows")

        # Failed enrichments sheet
        if failed_rows:
            failed_df = pd.DataFrame(failed_rows)
            failed_df.to_excel(writer, sheet_name="Failed", index=False)
            print(f"   ⚠️ Failed sheet: {len(failed_rows)} rows")

        # Metadata sheet
        metadata = {
            "Field": [
                "Generated At",
                "Input File",
                "Total Companies",
                "Successful Enrichments",
                "Failed Enrichments",
                "Total Contacts Found",
                "Enrichment Provider"
            ],
            "Value": [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                config.get('input_file', 'unknown'),
                len(results),
                sum(1 for r in results if r.success),
                sum(1 for r in results if not r.success),
                sum(len(r.contacts) for r in results),
                config.get('enrichment', {}).get('provider', 'unknown')
            ]
        }
        metadata_df = pd.DataFrame(metadata)
        metadata_df.to_excel(writer, sheet_name="Metadata", index=False)

    print(f"\n✅ Output saved to: {output_file}")


def print_summary(results: List[EnrichmentResult]):
    """Print enrichment summary to console."""
    total = len(results)
    successful = sum(1 for r in results if r.success)
    failed = total - successful
    total_contacts = sum(len(r.contacts) for r in results)

    print("\n" + "=" * 60)
    print("ENRICHMENT SUMMARY")
    print("=" * 60)
    print(f"  Companies Processed: {total}")
    print(f"  Successful:          {successful} ({successful/total*100:.1f}%)")
    print(f"  Failed:              {failed}")
    print(f"  Total Contacts:      {total_contacts}")
    print(f"  Avg Contacts/Company: {total_contacts/successful:.1f}" if successful > 0 else "  Avg Contacts/Company: N/A")
    print("=" * 60)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Exhibitor Contact Enrichment Pipeline',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python enrich_exhibitors.py                           # Use config defaults
    python enrich_exhibitors.py --input data/my_list.csv  # Custom input file
    python enrich_exhibitors.py --mock                    # Test with mock data
    python enrich_exhibitors.py --mock --input data/test.csv
        """
    )
    parser.add_argument('--input', type=str, help='Input CSV file with exhibitor data')
    parser.add_argument('--output', type=str, help='Output Excel file')
    parser.add_argument('--mock', action='store_true', help='Use mock connector (no API calls)')
    parser.add_argument('--config', type=str, default='market_intel/config.json', help='Config file path')

    args = parser.parse_args()

    print("\n" + "=" * 60)
    print("EXHIBITOR CONTACT ENRICHMENT PIPELINE")
    print("=" * 60)

    # Load config
    config = load_config(args.config)

    # Override with command line args
    input_file = args.input or config.get('input_file', 'market_intel/data/exhibitors.csv')
    output_file = args.output or config.get('output_file', 'market_intel/output/enriched_contacts.xlsx')

    # Load exhibitors
    companies = load_exhibitors(input_file)

    if not companies:
        print("\n❌ No companies to process. Exiting.")
        sys.exit(1)

    # Initialize connector
    enrichment_config = config.get('enrichment', {})
    enrichment_config['log_file'] = 'log/enrichment_audit.jsonl'
    enrichment_config['target_titles'] = config.get('target_titles', [])

    if args.mock:
        print("\n🧪 Using MOCK connector (no API calls)")
        connector = MockApolloConnector(enrichment_config)
    else:
        api_key = enrichment_config.get('api_key', '')
        if not api_key or api_key == 'YOUR_API_KEY_HERE':
            print("\n❌ No API key configured!")
            print("   Either:")
            print("   1. Add your Apollo API key to market_intel/config.json")
            print("   2. Run with --mock flag for testing")
            sys.exit(1)

        print(f"\n🔌 Using Apollo.io connector")
        connector = ApolloConnector(enrichment_config)

    # Run enrichment
    print("\n" + "-" * 60)
    print("STARTING ENRICHMENT")
    print("-" * 60)

    results = connector.enrich_batch(companies)

    # Print summary
    print_summary(results)

    # Export to Excel
    print("\n📊 Exporting to Excel...")
    export_to_excel(results, output_file, config)

    print("\n✅ Pipeline complete!")


if __name__ == "__main__":
    main()
