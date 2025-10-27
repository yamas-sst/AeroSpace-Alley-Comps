#!/usr/bin/env python3
"""
Setup Verification Script for AeroSpace-Alley-Comps
Checks that all dependencies and configuration are correct before running
"""

import sys
import os
import json

def print_status(check_name, passed, message=""):
    """Print colored status message"""
    if passed:
        print(f"✅ {check_name}")
        if message:
            print(f"   {message}")
    else:
        print(f"❌ {check_name}")
        if message:
            print(f"   {message}")

def check_python_version():
    """Check Python version is 3.7+"""
    version = sys.version_info
    passed = version.major == 3 and version.minor >= 7
    message = f"Python {version.major}.{version.minor}.{version.micro}"
    if not passed:
        message += " (need 3.7 or higher)"
    return passed, message

def check_dependencies():
    """Check all required packages are installed"""
    required = ['pandas', 'openpyxl', 'requests', 'tqdm']
    missing = []

    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)

    if missing:
        return False, f"Missing: {', '.join(missing)}"
    return True, "All dependencies installed"

def check_directory_structure():
    """Check required directories exist"""
    required_dirs = ['data', 'output', 'log', 'resources']
    missing = []

    for dir_name in required_dirs:
        if not os.path.exists(dir_name):
            missing.append(dir_name)

    if missing:
        return False, f"Missing directories: {', '.join(missing)}"
    return True, "All directories present"

def check_config_file():
    """Check config.json exists and is valid"""
    config_path = "resources/config.json"

    if not os.path.exists(config_path):
        return False, "resources/config.json not found"

    try:
        with open(config_path, 'r') as f:
            config = json.load(f)

        # Check required fields
        if 'api_keys' not in config or len(config['api_keys']) == 0:
            return False, "No API keys configured"

        if 'settings' not in config:
            return False, "Missing 'settings' section"

        # Check API key format
        first_key = config['api_keys'][0]['key']
        if len(first_key) < 20:
            return False, "API key looks invalid (too short)"

        return True, f"{len(config['api_keys'])} API key(s) configured"

    except json.JSONDecodeError:
        return False, "Invalid JSON in config.json"
    except Exception as e:
        return False, f"Error reading config: {e}"

def check_input_files():
    """Check input data files exist"""
    test_file = "data/Test_3_Companies.xlsx"
    full_file = "data/Aerospace_Alley_Companies.xlsx"

    test_exists = os.path.exists(test_file)
    full_exists = os.path.exists(full_file)

    if test_exists and full_exists:
        return True, "Both test and full data files present"
    elif test_exists:
        return True, "Test data file present (full file missing - OK for testing)"
    elif full_exists:
        return True, "Full data file present (test file missing - OK)"
    else:
        return False, "No input data files found in data/"

def check_api_connection():
    """Check if SerpAPI is accessible (without using quota)"""
    try:
        import requests

        # Just check if we can reach SerpAPI (not using API key)
        response = requests.get("https://serpapi.com", timeout=10)

        if response.status_code in [200, 301, 302]:
            return True, "SerpAPI is accessible"
        elif response.status_code == 403:
            # 403 might be IP block, but connection itself works
            return True, "SerpAPI reachable (403 may indicate IP block - check with quick_check.py)"
        else:
            return False, f"SerpAPI returned status {response.status_code}"

    except Exception as e:
        return False, f"Cannot reach SerpAPI: {e}"

def check_protection_system():
    """Check rate limit protection module exists"""
    protection_file = "resources/rate_limit_protection.py"

    if not os.path.exists(protection_file):
        return False, "rate_limit_protection.py not found"

    try:
        # Try to import it
        sys.path.insert(0, 'resources')
        from rate_limit_protection import RateLimitProtectionCoordinator
        return True, "Protection system ready"
    except ImportError as e:
        return False, f"Cannot import protection system: {e}"

def main():
    print("\n" + "="*70)
    print("AEROSPACE ALLEY JOB SCANNER - Setup Verification")
    print("="*70 + "\n")

    checks = [
        ("Python Version", check_python_version),
        ("Dependencies Installed", check_dependencies),
        ("Directory Structure", check_directory_structure),
        ("Configuration File", check_config_file),
        ("Input Data Files", check_input_files),
        ("Protection System", check_protection_system),
        ("API Connection", check_api_connection),
    ]

    all_passed = True

    for check_name, check_func in checks:
        passed, message = check_func()
        print_status(check_name, passed, message)
        if not passed:
            all_passed = False

    print("\n" + "="*70)

    if all_passed:
        print("✅ ALL CHECKS PASSED - Ready to run!")
        print("\n📋 Next Steps:")
        print("   1. Verify IP block has cleared: python quick_check.py")
        print("   2. Run Test 1 (1 company):      python AeroComps.py")
        print("   3. Check output in:             output/")
        print("="*70 + "\n")
        return 0
    else:
        print("❌ SOME CHECKS FAILED - See errors above")
        print("\n📋 Fix Required:")
        print("   - Install missing dependencies: pip install -r resources/requirements.txt")
        print("   - Create missing directories:   mkdir -p data output log resources")
        print("   - Add API keys to:              resources/config.json")
        print("="*70 + "\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
