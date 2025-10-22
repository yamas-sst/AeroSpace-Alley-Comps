# Job Analytics Module

## Overview

The analytics module (`analytics.py`) provides comprehensive insights into skilled trades hiring patterns from your job scraping results. It automatically identifies top trades, hiring companies, geographic hotspots, and more.

## Features

### 1. **Top Trades Analysis**
Identifies which skilled trades are most in-demand by analyzing job title keywords.

**Insights:**
- Most frequently posted trade positions
- Percentage of total job market per trade
- Trend identification (machining vs. assembly vs. welding, etc.)

**Example Output:**
```
Trade                    Job Count    Percentage
CNC Machinist           245          15.3%
Welder                  198          12.4%
Quality Inspector       156          9.7%
```

### 2. **Top Hiring Companies**
Ranks companies by number of skilled trades job openings.

**Insights:**
- Which companies are hiring most aggressively
- Market share per company
- Concentration vs. distribution of opportunities

**Example Output:**
```
Company              Job Count    Market Share
Boeing               142          8.9%
Lockheed Martin      98           6.1%
Northrop Grumman     87           5.4%
```

### 3. **Geographic Distribution**
Analyzes where skilled trades jobs are located.

**Insights:**
- Top cities/states for job opportunities
- Geographic clustering (aerospace hubs)
- Relocation considerations

**Example Output:**
```
Location                 Job Count    Percentage
Seattle, WA             156          9.7%
Fort Worth, TX          134          8.4%
Huntington Beach, CA    98           6.1%
```

### 4. **Job Board Analysis**
Identifies which job boards have the most listings.

**Insights:**
- Most effective job boards for aerospace trades
- Source diversification
- Where to focus job search efforts

**Example Output:**
```
Job Board       Job Count    Percentage
Indeed          542          33.9%
LinkedIn        387          24.2%
ZipRecruiter    298          18.6%
```

### 5. **Trade-by-Company Matrix**
Cross-tabulation showing which trades each company is hiring for.

**Insights:**
- Company-specific hiring patterns
- Specialization identification (e.g., welding-heavy vs. assembly-heavy)
- Strategic job application targeting

### 6. **Summary Statistics**
High-level overview of the dataset.

**Metrics:**
- Total jobs collected
- Unique companies analyzed
- Date range
- Average jobs per company
- Companies with 10+ openings

## Usage

### Automatic Integration

The analytics module is **automatically invoked** when you run `AeroComps.py`. After scraping completes, it generates:

1. **Main job file**: `Aerospace_Alley_SkilledTrades_Jobs.xlsx`
2. **Analytics report**: `Aerospace_Alley_SkilledTrades_Jobs_Analytics.xlsx`

No additional configuration needed!

### Standalone Usage

You can also run analytics on existing job data:

```bash
# Analyze an existing job results file
python analytics.py Aerospace_Alley_SkilledTrades_Jobs.xlsx

# Specify custom output filename
python analytics.py input.xlsx custom_analytics.xlsx
```

### Programmatic Usage

```python
from analytics import JobAnalytics
import pandas as pd

# Load your job data
df = pd.read_excel("jobs.xlsx")

# Create analytics instance
analytics = JobAnalytics(df)

# Get specific analyses
top_trades = analytics.analyze_top_trades(top_n=20)
top_companies = analytics.analyze_top_companies(top_n=25)
locations = analytics.analyze_locations(top_n=30)

# Generate full report
analytics.generate_report("my_analytics.xlsx")
```

## Output Format

The analytics report is a multi-sheet Excel workbook:

| Sheet Name | Description |
|------------|-------------|
| **Summary** | Key metrics and overview statistics |
| **Top Trades** | Most in-demand skilled trades |
| **Top Companies** | Companies with most job openings |
| **Locations** | Geographic distribution of jobs |
| **Job Boards** | Job posting sources analysis |
| **Trade by Company** | Matrix of trades × companies |
| **Raw Data** | Complete job listings for reference |

## Customization

### Adjust Number of Results

```python
# Show top 30 trades instead of default 15
top_trades = analytics.analyze_top_trades(top_n=30)

# Show top 50 companies
top_companies = analytics.analyze_top_companies(top_n=50)
```

### Filter by Date Range

```python
# Filter to recent jobs only (last 30 days)
import datetime as dt
recent_cutoff = dt.datetime.now() - dt.timedelta(days=30)
recent_jobs = df[df['Timestamp'] >= recent_cutoff]

analytics = JobAnalytics(recent_jobs)
```

### Filter by Location

```python
# Analyze only California jobs
ca_jobs = df[df['Location'].str.contains('CA', na=False)]
analytics = JobAnalytics(ca_jobs)
analytics.generate_report("california_analytics.xlsx")
```

## Use Cases

### 1. **Job Seekers**
- Identify most in-demand skills to prioritize training
- Find companies with most opportunities
- Discover geographic hotspots
- Target high-activity job boards

### 2. **Recruiters**
- Benchmark company hiring activity
- Identify competitive landscape
- Understand market demand by trade
- Optimize job posting strategies

### 3. **Workforce Development**
- Identify skills gaps in the market
- Guide training program development
- Track hiring trends over time
- Support regional economic planning

### 4. **Business Intelligence**
- Market research for staffing agencies
- Competitive intelligence gathering
- Industry trend analysis
- Salary benchmarking (with salary extraction)

## Future Enhancements

### Planned Features:
- **Time-series analysis**: Track hiring trends week-over-week
- **Salary analytics**: Average compensation by trade (see `salary_extraction_pseudocode.py`)
- **Skill extraction**: Parse required certifications and skills
- **Experience level analysis**: Entry vs. mid vs. senior positions
- **Company size correlation**: Small vs. large company hiring patterns
- **Seasonal trends**: Identify hiring cycles

### Advanced Analytics:
- **Predictive modeling**: Forecast future hiring demand
- **Skill gap analysis**: Compare supply vs. demand
- **Geospatial visualization**: Interactive maps of job distribution
- **Network analysis**: Company relationships and talent flow

## Requirements

```bash
pip install pandas openpyxl
```

## Troubleshooting

### "No module named 'analytics'"
- Ensure `analytics.py` is in the same directory as `AeroComps.py`
- Check Python path settings

### "Empty DataFrame" error
- Verify input Excel file has data
- Check column names match expected format

### Low job counts in analytics
- Ensure main scraper ran successfully
- Check for API limit issues during scraping
- Verify company list includes active hiring companies

## Examples

### Console Output Sample

```
============================================================
GENERATING ANALYTICS REPORT
============================================================

📊 SUMMARY STATISTICS
------------------------------------------------------------
  Total Jobs: 1,247
  Unique Companies: 156
  Unique Locations: 89
  Date Range: 2025-10-22 to 2025-10-22
  Job Boards Used: 12
  Average Jobs per Company: 8.0
  Companies with 10+ Jobs: 42
  Companies with 1 Job: 67

🔧 TOP 10 IN-DEMAND TRADES
------------------------------------------------------------
           Trade  Job Count Percentage
     Machinist        245       19.6%
        Welder        198       15.9%
     Inspector        156       12.5%
     Assembler        142       11.4%
   Maintenance         98        7.9%
   Electrician         87        7.0%

🏢 TOP 10 HIRING COMPANIES
------------------------------------------------------------
          Company  Job Count Percentage
          Boeing        142       11.4%
 Lockheed Martin         98        7.9%
Northrop Grumman         87        7.0%

📍 TOP 10 LOCATIONS
------------------------------------------------------------
        Location  Job Count Percentage
     Seattle, WA        156       12.5%
  Fort Worth, TX        134       10.7%

✅ Analytics report saved to: Aerospace_Alley_SkilledTrades_Jobs_Analytics.xlsx
============================================================
```

## Support

For issues or feature requests, please open an issue on GitHub.

---

**Part of the Aerospace Alley Job Scanner project**
