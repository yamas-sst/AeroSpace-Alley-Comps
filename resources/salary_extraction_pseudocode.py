# ======================================================
# SALARY EXTRACTION - PSEUDO CODE & IMPLEMENTATION GUIDE
# ======================================================
# PURPOSE: Extract salary/wage information from job descriptions and titles
#
# CHALLENGES:
#   - Multiple formats: "$50,000", "$25-30/hr", "$80K-$100K", "50k-60k"
#   - Ambiguous terms: "competitive", "DOE" (depends on experience)
#   - Location in text: title, description, extensions, structured data
#   - Hourly vs. annual confusion
#   - Ranges vs. exact amounts
#   - Hidden/missing salary data
#
# APPROACH:
#   1. Check structured data first (if API provides it)
#   2. Use regex patterns for common formats
#   3. Normalize to annual salary for comparison
#   4. Handle ranges (store min, max, average)
#   5. Mark confidence level of extraction
# ======================================================

import re
from typing import Dict, Optional, Tuple


# ======================================================
# PSEUDO CODE: Main Salary Extraction Algorithm
# ======================================================
"""
FUNCTION extract_salary(job_dict):
    # STEP 1: Check structured data (if API provides it)
    IF job_dict has "detected_extensions" field:
        IF "salary" key exists in detected_extensions:
            RETURN structured_salary_data

    # STEP 2: Search job title first (most reliable location)
    salary_info = search_for_salary_patterns(job_dict["title"])
    IF salary_info found:
        RETURN salary_info with high_confidence

    # STEP 3: Search full job description
    salary_info = search_for_salary_patterns(job_dict["description"])
    IF salary_info found:
        RETURN salary_info with medium_confidence

    # STEP 4: Check for non-numeric indicators
    IF description contains "competitive salary":
        RETURN {status: "competitive", confidence: "low"}
    IF description contains "DOE" or "depends on experience":
        RETURN {status: "DOE", confidence: "low"}

    # STEP 5: No salary information found
    RETURN {status: "not_listed", confidence: "none"}


FUNCTION search_for_salary_patterns(text):
    # Try multiple regex patterns in order of specificity

    # Pattern 1: Range with units (e.g., "$50K-$70K", "$25-30/hr")
    IF matches "$XX-$XX" pattern:
        EXTRACT min_value, max_value, unit (hourly/annual)
        NORMALIZE to annual salary
        RETURN {min, max, avg, unit, confidence: "high"}

    # Pattern 2: Single value (e.g., "$65,000/year", "$30/hour")
    IF matches "$XX" with unit:
        EXTRACT value, unit
        NORMALIZE to annual salary
        RETURN {amount, unit, confidence: "medium"}

    # Pattern 3: Numeric without explicit $ (e.g., "50k-60k")
    IF matches "XXk-XXk" pattern:
        EXTRACT min, max
        ASSUME annual (k = thousand)
        RETURN {min, max, avg, confidence: "medium"}

    # Pattern 4: "Up to $XX" or "Starting at $XX"
    IF matches "up to" or "starting at" pattern:
        EXTRACT value
        RETURN {type: "ceiling" or "floor", amount, confidence: "medium"}

    RETURN None


FUNCTION normalize_to_annual(amount, unit):
    IF unit == "hourly":
        # Assume 40 hours/week, 52 weeks/year
        annual = amount * 40 * 52
    ELSE IF unit == "monthly":
        annual = amount * 12
    ELSE:
        annual = amount  # Already annual

    RETURN annual


FUNCTION calculate_confidence(extraction_method, data_source):
    # Confidence scoring system
    IF source == "structured_api_data":
        confidence = 0.95  # Very high
    ELSE IF source == "job_title" AND method == "explicit_range":
        confidence = 0.85  # High
    ELSE IF source == "description" AND method == "explicit_range":
        confidence = 0.70  # Medium-high
    ELSE IF method == "single_value":
        confidence = 0.60  # Medium
    ELSE IF method == "inferred_from_k_notation":
        confidence = 0.50  # Medium-low
    ELSE:
        confidence = 0.30  # Low

    RETURN confidence
"""


# ======================================================
# ACTUAL IMPLEMENTATION (Python)
# ======================================================

class SalaryExtractor:
    """
    Extracts and normalizes salary information from job postings.
    """

    def __init__(self):
        # Regex patterns for different salary formats
        self.patterns = {
            # $50,000 - $70,000 per year
            'range_annual_explicit': re.compile(
                r'\$\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*[-–to]+\s*\$?\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*(?:per\s+year|annually|\/year|\/yr|a year)?',
                re.IGNORECASE
            ),

            # $25-$35/hour or $25-35 per hour
            'range_hourly': re.compile(
                r'\$\s*(\d{1,3}(?:\.\d{2})?)\s*[-–to]+\s*\$?\s*(\d{1,3}(?:\.\d{2})?)\s*(?:per\s+hour|\/hour|\/hr|hourly)',
                re.IGNORECASE
            ),

            # 50k-70k or 50K-70K
            'range_k_notation': re.compile(
                r'(\d{2,3})\s*k\s*[-–to]+\s*(\d{2,3})\s*k',
                re.IGNORECASE
            ),

            # $65,000/year or $65000 per year
            'single_annual': re.compile(
                r'\$\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*(?:per\s+year|annually|\/year|\/yr|a year)',
                re.IGNORECASE
            ),

            # $30/hour or $30.50 per hour
            'single_hourly': re.compile(
                r'\$\s*(\d{1,3}(?:\.\d{2})?)\s*(?:per\s+hour|\/hour|\/hr|hourly)',
                re.IGNORECASE
            ),

            # Up to $75,000 or Starting at $50,000
            'bounded': re.compile(
                r'(up to|starting at|from)\s+\$\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
                re.IGNORECASE
            ),
        }

    def extract_from_job(self, job_dict: Dict) -> Dict:
        """
        Main extraction method for a job dictionary.

        Parameters:
            job_dict (dict): Job data with keys like title, description, detected_extensions

        Returns:
            dict: Salary information with keys:
                - min_annual: Minimum annual salary (None if not found)
                - max_annual: Maximum annual salary (None if not found)
                - avg_annual: Average annual salary
                - hourly_rate: Hourly rate (if applicable)
                - raw_text: Original salary text found
                - confidence: Confidence score (0-1)
                - status: "found", "competitive", "DOE", "not_listed"
        """

        # STEP 1: Check structured API data
        if "Detected Extensions" in job_dict:
            extensions = job_dict["Detected Extensions"]
            if isinstance(extensions, dict) and "salary" in extensions:
                return self._parse_structured_salary(extensions["salary"])

        # STEP 2: Check job title (most reliable)
        title_result = self._extract_from_text(job_dict.get("Job Title", ""))
        if title_result["status"] == "found":
            title_result["confidence"] = min(title_result["confidence"] + 0.1, 1.0)  # Boost confidence
            return title_result

        # STEP 3: Check description
        description = job_dict.get("Description Snippet", "")
        desc_result = self._extract_from_text(description)
        if desc_result["status"] == "found":
            return desc_result

        # STEP 4: Check for non-numeric indicators
        combined_text = f"{job_dict.get('Job Title', '')} {description}".lower()

        if any(term in combined_text for term in ["competitive salary", "competitive pay", "competitive compensation"]):
            return {
                "status": "competitive",
                "min_annual": None,
                "max_annual": None,
                "avg_annual": None,
                "confidence": 0.3,
                "raw_text": "competitive"
            }

        if any(term in combined_text for term in ["doe", "depends on experience", "commensurate with experience"]):
            return {
                "status": "DOE",
                "min_annual": None,
                "max_annual": None,
                "avg_annual": None,
                "confidence": 0.3,
                "raw_text": "DOE"
            }

        # STEP 5: No salary found
        return {
            "status": "not_listed",
            "min_annual": None,
            "max_annual": None,
            "avg_annual": None,
            "confidence": 0.0,
            "raw_text": None
        }

    def _extract_from_text(self, text: str) -> Dict:
        """
        Extract salary from free text using regex patterns.
        """
        if not text:
            return {"status": "not_found", "confidence": 0.0}

        # Try each pattern in order of specificity

        # 1. Annual range: $50,000 - $70,000
        match = self.patterns['range_annual_explicit'].search(text)
        if match:
            min_val = float(match.group(1).replace(',', ''))
            max_val = float(match.group(2).replace(',', ''))
            return {
                "status": "found",
                "min_annual": min_val,
                "max_annual": max_val,
                "avg_annual": (min_val + max_val) / 2,
                "confidence": 0.85,
                "raw_text": match.group(0)
            }

        # 2. Hourly range: $25-$35/hour
        match = self.patterns['range_hourly'].search(text)
        if match:
            min_hourly = float(match.group(1))
            max_hourly = float(match.group(2))
            min_annual = min_hourly * 40 * 52  # 40 hrs/week, 52 weeks/year
            max_annual = max_hourly * 40 * 52
            return {
                "status": "found",
                "min_annual": min_annual,
                "max_annual": max_annual,
                "avg_annual": (min_annual + max_annual) / 2,
                "hourly_rate": f"${min_hourly}-${max_hourly}",
                "confidence": 0.80,
                "raw_text": match.group(0)
            }

        # 3. K notation: 50k-70k
        match = self.patterns['range_k_notation'].search(text)
        if match:
            min_val = float(match.group(1)) * 1000
            max_val = float(match.group(2)) * 1000
            return {
                "status": "found",
                "min_annual": min_val,
                "max_annual": max_val,
                "avg_annual": (min_val + max_val) / 2,
                "confidence": 0.70,
                "raw_text": match.group(0)
            }

        # 4. Single annual: $65,000/year
        match = self.patterns['single_annual'].search(text)
        if match:
            amount = float(match.group(1).replace(',', ''))
            return {
                "status": "found",
                "min_annual": amount,
                "max_annual": amount,
                "avg_annual": amount,
                "confidence": 0.75,
                "raw_text": match.group(0)
            }

        # 5. Single hourly: $30/hour
        match = self.patterns['single_hourly'].search(text)
        if match:
            hourly = float(match.group(1))
            annual = hourly * 40 * 52
            return {
                "status": "found",
                "min_annual": annual,
                "max_annual": annual,
                "avg_annual": annual,
                "hourly_rate": f"${hourly}",
                "confidence": 0.70,
                "raw_text": match.group(0)
            }

        # 6. Bounded: Up to $75,000
        match = self.patterns['bounded'].search(text)
        if match:
            bound_type = match.group(1).lower()
            amount = float(match.group(2).replace(',', ''))

            if "up to" in bound_type:
                return {
                    "status": "found",
                    "min_annual": None,
                    "max_annual": amount,
                    "avg_annual": amount * 0.75,  # Estimate
                    "confidence": 0.60,
                    "raw_text": match.group(0),
                    "note": "ceiling"
                }
            else:  # "starting at" or "from"
                return {
                    "status": "found",
                    "min_annual": amount,
                    "max_annual": None,
                    "avg_annual": amount * 1.25,  # Estimate
                    "confidence": 0.60,
                    "raw_text": match.group(0),
                    "note": "floor"
                }

        return {"status": "not_found", "confidence": 0.0}

    def _parse_structured_salary(self, salary_data):
        """
        Parse structured salary data from API extensions.
        This is the most reliable source when available.
        """
        # Implementation depends on API structure
        # SerpApi typically provides: {"min": "50000", "max": "70000", "currency": "USD"}
        return {
            "status": "found",
            "min_annual": float(salary_data.get("min", 0)),
            "max_annual": float(salary_data.get("max", 0)),
            "avg_annual": (float(salary_data.get("min", 0)) + float(salary_data.get("max", 0))) / 2,
            "confidence": 0.95,
            "raw_text": "API-provided"
        }


# ======================================================
# USAGE EXAMPLE
# ======================================================

def add_salary_analysis_to_jobs(jobs_df):
    """
    Add salary columns to existing jobs DataFrame.

    Parameters:
        jobs_df (DataFrame): Job results

    Returns:
        DataFrame: Enhanced with salary columns
    """
    extractor = SalaryExtractor()

    # Apply extraction to each job
    salary_results = jobs_df.apply(lambda row: extractor.extract_from_job(row.to_dict()), axis=1)

    # Convert to DataFrame and add to original
    salary_df = pd.DataFrame(salary_results.tolist())
    jobs_df['Salary_Min'] = salary_df['min_annual']
    jobs_df['Salary_Max'] = salary_df['max_annual']
    jobs_df['Salary_Avg'] = salary_df['avg_annual']
    jobs_df['Salary_Status'] = salary_df['status']
    jobs_df['Salary_Confidence'] = salary_df['confidence']
    jobs_df['Salary_Raw'] = salary_df['raw_text']

    return jobs_df


# ======================================================
# ANALYTICS: Salary by Trade
# ======================================================

def analyze_salary_by_trade(jobs_df):
    """
    Calculate average salary statistics by trade category.

    PSEUDO CODE:
        FOR each trade keyword:
            filter_jobs = jobs WHERE title contains keyword AND salary found
            IF filter_jobs is not empty:
                calculate median_salary, avg_salary, min_salary, max_salary
                count_jobs_with_salary
                store results

        SORT by median_salary descending
        RETURN top trades by compensation
    """
    # Group jobs by primary trade and calculate salary stats
    trade_keywords = SalaryExtractor().patterns.keys()  # Simplified

    results = []
    for trade in trade_keywords:
        # Filter jobs for this trade with salary data
        mask = (jobs_df['Job Title'].str.contains(trade, case=False, na=False)) & \
               (jobs_df['Salary_Status'] == 'found')

        trade_jobs = jobs_df[mask]

        if len(trade_jobs) > 0:
            results.append({
                'Trade': trade,
                'Job Count': len(trade_jobs),
                'Median Salary': trade_jobs['Salary_Avg'].median(),
                'Average Salary': trade_jobs['Salary_Avg'].mean(),
                'Min Salary': trade_jobs['Salary_Min'].min(),
                'Max Salary': trade_jobs['Salary_Max'].max(),
                'Salary Listed %': (len(trade_jobs) / len(jobs_df[
                    jobs_df['Job Title'].str.contains(trade, case=False, na=False)
                ])) * 100
            })

    import pandas as pd
    return pd.DataFrame(results).sort_values('Median Salary', ascending=False)


# ======================================================
# TEST CASES
# ======================================================

if __name__ == "__main__":
    extractor = SalaryExtractor()

    # Test various salary formats
    test_cases = [
        {"Job Title": "CNC Machinist - $50,000 - $70,000 per year", "Description Snippet": ""},
        {"Job Title": "Welder", "Description Snippet": "$25-$35 per hour depending on experience"},
        {"Job Title": "Quality Inspector", "Description Snippet": "Salary: 60k-75k annually"},
        {"Job Title": "Maintenance Technician", "Description Snippet": "Starting at $28/hour"},
        {"Job Title": "Assembler", "Description Snippet": "Competitive salary and benefits"},
        {"Job Title": "Electrician", "Description Snippet": "Up to $85,000 based on qualifications"},
    ]

    print("="*80)
    print("SALARY EXTRACTION TEST CASES")
    print("="*80 + "\n")

    for i, test in enumerate(test_cases, 1):
        result = extractor.extract_from_job(test)
        print(f"Test {i}: {test['Job Title']}")
        print(f"  Status: {result['status']}")
        if result['status'] == 'found':
            print(f"  Annual Range: ${result.get('min_annual', 'N/A'):,.0f} - ${result.get('max_annual', 'N/A'):,.0f}")
            print(f"  Average: ${result.get('avg_annual', 0):,.0f}")
            print(f"  Confidence: {result['confidence']:.0%}")
        print(f"  Raw: {result.get('raw_text', 'None')}\n")
