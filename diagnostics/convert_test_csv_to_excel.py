#!/usr/bin/env python3
"""
Convert Test_Max25_9Companies.csv to Excel format

Run this script locally to create the Excel file needed for testing.

Usage:
    python diagnostics/convert_test_csv_to_excel.py
"""

import pandas as pd
import os

def convert_csv_to_excel():
    """Convert CSV test file to Excel format."""

    # Use relative paths from diagnostics/ directory
    csv_path = 'Test_Max25_9Companies.csv'
    excel_path = 'Test_Max25_9Companies.xlsx'

    print("🔄 Converting CSV to Excel format...")
    print(f"   Input:  diagnostics/{csv_path}")
    print(f"   Output: diagnostics/{excel_path}")

    # Check if CSV exists
    if not os.path.exists(csv_path):
        print(f"\n❌ Error: {csv_path} not found in diagnostics/!")
        return False

    # Read CSV
    df = pd.read_csv(csv_path)

    print(f"\n📋 Companies loaded: {len(df)}")
    for i, company in enumerate(df['Company Name'], 1):
        print(f"   {i}. {company}")

    # Save as Excel
    df.to_excel(excel_path, index=False, engine='openpyxl')

    print(f"\n✅ Successfully created {excel_path}")
    print(f"\n📊 Test Configuration:")
    print(f"   - Total companies: 9")
    print(f"   - Expected API calls: 25")
    print(f"   - Processing time: 2-3 minutes")
    print(f"\n🚀 Ready to test! Run: python AeroComps.py")

    return True

if __name__ == '__main__':
    try:
        convert_csv_to_excel()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you have pandas and openpyxl installed:")
        print("   pip install pandas openpyxl")
