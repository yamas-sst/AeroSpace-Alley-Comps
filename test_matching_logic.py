#!/usr/bin/env python3
"""
Test script to validate job title matching logic
Tests actual job titles from user's output to ensure correctness
"""

# Copy exact logic from AeroComps.py
CORE_TRADE_WORDS = [
    "machinist", "cnc", "mill", "lathe", "fabricator", "welder", "toolmaker",
    "assembler", "assembly", "operator", "production",
    "mechanic", "millwright", "maintenance", "repair",
    "electrician", "electrical", "electronics", "electronic", "controls",
    "plumber", "pipefitter", "hvac", "boiler", "refrigeration",
    "inspector", "inspection", "quality", "metrology", "ndt", "cmm",
    "technician", "tech",
    "engineer", "engineering", "supervisor", "foreman", "superintendent", "lead",
    "programmer", "planner",
]

EXCLUSION_PATTERNS = [
    "software", "it ", "information technology", "network", "cyber", "data",
    "service desk", "help desk", "desktop", "systems admin",
    "sales", "marketing", "hr", "human resources", "accounting", "finance",
    "office", "administrative", "admin", "receptionist", "coordinator",
    "business office", "business development",
    "architect", "graphic", "ui/ux", "product design", "design engineer",
    "- design", "design tech", "designer",
    " vp ", "vice president", " director", " president", " ceo ", " cfo ", " cto ",
    "intern", "co-op",
    "nurse", "doctor", "medical", "clinical", "janitorial", "custodian",
    "field service rep", "operations excellence",
]

def is_skilled_trade_job(job_title):
    title_lower = job_title.lower()

    # Check exclusions first
    for exclusion in EXCLUSION_PATTERNS:
        if exclusion in title_lower:
            return False, f"EXCLUDED by '{exclusion}'"

    # Check if any core trade word is present
    for word in CORE_TRADE_WORDS:
        if word in title_lower:
            return True, f"MATCHED by '{word}'"

    return False, "NO MATCH (no core words)"

# Test cases from user's actual output
test_cases = [
    # SHOULD MATCH (skilled trades)
    ("QC In-process Inspector", True),
    ("Quality Inspector (2nd Shift)", True),
    ("Dimensional Inspector (1st Shift)", True),
    ("CMM Inspector", True),
    ("Quality Control Inspector", True),
    ("Lead Inspector TFE731", True),
    ("NDT Inspector", True),
    ("Powerhouse Mechanic (Onsite)", True),
    ("Senior Process Manufacturing Engineer", True),
    ("Industrial Engineering Technical Manager (Onsite)", True),
    ("CNC Milling Machinist (2nd Shift)", True),
    ("Manual VTL/Lathe Machinist (1st Shift)", True),
    ("Welder (2nd Shift)", True),
    ("CNC Programmer", True),
    ("Production Supervisor", True),
    ("Manufacturing Engineering Manager", True),
    ("Engineering Technician, Assoc - Full-time", True),
    ("Maintenance Repair Technician, Senior", True),
    ("Process Engineer, Sr", True),
    ("Part Marking Technician - 1st Shift", True),
    ("Senior Quality Engineer", True),
    ("A&P Mechanic", True),
    ("Aircraft Mechanic, Corporate MRO", True),
    ("Aerospace Manufacturing Production Engineer", True),

    # SHOULD NOT MATCH (non-trades, excluded, or missing core words)
    ("Expeditor", False),
    ("Burr Hand", False),  # No core words (might want to add)
    ("Senior Service Desk Technician", False),  # Excluded by "service desk"
    ("Engineer - Design", False),  # Should be excluded (design role)
    ("Summer/Fall Engineering Co-Op Intern", False),  # Excluded by "intern" and "co-op"
    ("Inspector Intern", False),  # Excluded by "intern"
    ("Operations Excellence Intern", False),  # Excluded by "operations excellence"
    ("Business Office Administrator", False),  # Excluded by "office"
    ("Field Service Representative (Florida)", False),  # Excluded by "field service rep"
]

print("=" * 80)
print("JOB TITLE MATCHING VALIDATION")
print("=" * 80)
print()

passed = 0
failed = 0
bugs_found = []

for title, expected_match in test_cases:
    actual_match, reason = is_skilled_trade_job(title)
    status = "✅ PASS" if actual_match == expected_match else "❌ FAIL"

    if actual_match == expected_match:
        passed += 1
    else:
        failed += 1
        bugs_found.append((title, expected_match, actual_match, reason))

    print(f"{status} | Expected: {expected_match:5} | Got: {actual_match:5} | {title}")
    print(f"        Reason: {reason}")
    print()

print("=" * 80)
print(f"RESULTS: {passed} passed, {failed} failed")
print("=" * 80)

if bugs_found:
    print()
    print("🚨 BUGS FOUND:")
    print("-" * 80)
    for title, expected, actual, reason in bugs_found:
        print(f"Title: {title}")
        print(f"  Expected: {'MATCH' if expected else 'REJECT'}")
        print(f"  Got: {'MATCH' if actual else 'REJECT'}")
        print(f"  Reason: {reason}")
        print()
