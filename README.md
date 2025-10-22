# Aerospace Alley Job Scanner

A Python-based job aggregation tool that automatically scans and collects skilled trades job postings from aerospace companies using the SerpApi Google Jobs API.

## Overview

This tool streamlines the process of finding skilled trades positions across multiple aerospace companies by:
- Automatically querying job boards for 100+ skilled trades keywords
- Filtering results to match specific trade categories
- Exporting structured data to Excel for easy analysis
- Handling API rate limits with intelligent throttling
- Supporting multi-threaded processing for faster results

## Features

- **Comprehensive Keyword Coverage**: Searches for 100+ skilled trades keywords across categories:
  - Machining & Fabrication (CNC, machinist, toolmaker, etc.)
  - Assembly & Production (assembler, production technician, etc.)
  - Welding & Metalwork (TIG, MIG, arc welding, etc.)
  - Maintenance & Repair (maintenance technician, millwright, etc.)
  - Inspection & Quality (QC inspector, NDT technician, etc.)
  - Electrical & Technical (electrician, controls technician, etc.)
  - Composites & Aerospace-specific (composite technician, avionics, etc.)

- **Intelligent API Management**:
  - Rate limiting to prevent API abuse
  - Retry logic for failed requests
  - API call counter with configurable limits
  - Progressive checkpoint saves

- **Multi-threaded Processing**: Parallel execution for faster company scanning

- **Structured Output**: Excel file with job details including:
  - Company name
  - Job title
  - Location
  - Source/job board
  - Application link
  - Description snippet
  - Timestamp

- **Built-in Analytics**: Automatically generates insights after scraping
  - Top in-demand trades and hiring companies
  - Geographic distribution and job board analysis
  - Multi-sheet Excel report with summary statistics

## Requirements

### Python Version
- Python 3.7 or higher

### Dependencies
```bash
pip install pandas openpyxl requests tqdm
```

### API Access
- SerpApi account with API key (get one at https://serpapi.com/)
- Note: Free tier limited to 100 searches/month, paid plans available

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/AeroSpace-Alley-Comps.git
cd AeroSpace-Alley-Comps
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your settings in `AeroComps.py`:
   - Set your `API_KEY`
   - Update `INPUT_FILE` path to your company list
   - Adjust `OUTPUT_FILE` path as needed
   - Configure `MAX_API_CALLS` based on your plan

## Usage

### Basic Usage

1. Prepare an Excel file with aerospace companies:
   - Required column: "Company Name"
   - One company per row

2. Run the scanner:
```bash
python AeroComps.py
```

3. Monitor progress in the console:
   - API call counter
   - Per-company job counts
   - Checkpoint saves

4. Results saved to `Aerospace_Alley_SkilledTrades_Jobs.xlsx`
5. Analytics report automatically generated: `Aerospace_Alley_SkilledTrades_Jobs_Analytics.xlsx`

### What the Analytics Report Includes

The analytics module automatically generates a multi-sheet Excel report with:
- **Top Trades**: Most in-demand positions (Machinist, Welder, Inspector, etc.) with job counts
- **Top Companies**: Companies ranked by hiring activity and market share
- **Geographic Distribution**: Job hotspots by city/state
- **Job Board Analysis**: Which platforms have the most listings (Indeed, LinkedIn, etc.)
- **Trade-by-Company Matrix**: Cross-tabulation showing hiring patterns per company
- **Summary Statistics**: Total jobs, unique companies, date range, and key metrics

Run analytics standalone on existing data: `python analytics.py input.xlsx output.xlsx`

### Advanced: Salary Extraction

A salary extraction framework is included in `salary_extraction_pseudocode.py` for future integration:
- Parses multiple formats: $50K-70K, $25-35/hr, ranges and exact amounts
- Normalizes to annual salary with confidence scoring
- Ready to integrate for compensation analysis by trade

### Configuration Options

Edit these variables in `AeroComps.py`:

```python
API_KEY = "your_serpapi_key"              # Your SerpApi key
INPUT_FILE = "path/to/companies.xlsx"     # Company list location
OUTPUT_FILE = "output.xlsx"                # Results filename
MAX_QUERY_LENGTH = 200                     # Google Jobs query limit
MAX_THREADS = 5                            # Parallel threads (adjust for rate limits)
MAX_API_CALLS = 250                        # Stop after N API calls
MIN_INTERVAL = 1.2                         # Seconds between API calls
```

## Input File Format

Your Excel file should have at minimum:

| Company Name |
|--------------|
| Boeing |
| Lockheed Martin |
| Northrop Grumman |
| ... |

Additional columns are ignored.

## Output File Format

The generated Excel file contains:

| Column | Description |
|--------|-------------|
| Company | Company name from input file |
| Job Title | Full job title |
| Location | Job location (city, state) |
| Via | Job board source (Indeed, LinkedIn, etc.) |
| Source URL | Direct application link |
| Detected Extensions | Metadata from SerpApi (employment type, etc.) |
| Description Snippet | First 200 characters of job description |
| Timestamp | When the job was scraped |

## How It Works

1. **Load Companies**: Reads company list from Excel input file
2. **Build Queries**: Creates optimized search queries combining company name + trade keywords
3. **API Requests**: Queries Google Jobs via SerpApi (up to 3 pages per company)
4. **Filter Results**: Only keeps jobs matching skilled trades keywords in the title
5. **Deduplicate**: Removes duplicate listings based on company, title, and URL
6. **Export**: Saves to Excel with periodic checkpoints

## API Limits & Cost Management

### Free Tier (100 searches/month)
- Set `MAX_API_CALLS = 95` to stay under limit
- Process ~30-35 companies (3 pages each)

### Paid Plans
- Scale package: 5,000 searches/month ($50)
- Business package: 15,000 searches/month ($130)
- Adjust `MAX_API_CALLS` accordingly

### Cost Optimization Tips
- Reduce `MAX_THREADS` to avoid rate limit errors
- Process companies in batches
- Use shorter keyword lists for initial scans
- Skip pagination for companies unlikely to have jobs

## Troubleshooting

### "API LIMIT REACHED" message
- You've hit `MAX_API_CALLS` limit
- Check your SerpApi dashboard for actual usage
- Results up to that point are saved

### Connection errors / Timeouts
- Retry logic built-in (3 attempts per request)
- Check internet connection
- Verify SerpApi service status

### No jobs found
- Verify company names match real job postings
- Try broader keyword sets
- Check that companies actually have openings
- Examine query length (might be truncated)

### Rate limit errors (429)
- Increase `MIN_INTERVAL` to 2.0+ seconds
- Reduce `MAX_THREADS` to 3 or fewer
- Wait and retry later

## Future Expansion Opportunities

This codebase can be extended into a comprehensive job intelligence platform with:

**Data & Intelligence**
- Multi-industry support (automotive, defense, manufacturing, maritime)
- Database integration (PostgreSQL/SQLite) for historical tracking
- Time-series trend analysis and demand forecasting
- Salary benchmarking and competitive intelligence
- Multiple data source integration (LinkedIn, Indeed, Glassdoor APIs)

**User Features**
- Real-time notifications (email, SMS, Slack/Teams)
- Web dashboard with interactive visualizations
- Job matching with resume parsing and NLP skill extraction
- Job application CRM for tracking interviews and offers
- Mobile apps with location-based alerts

**Enterprise & Integration**
- Cloud deployment with scheduled scans (AWS/GCP/Azure)
- REST API for third-party integration
- ATS and CRM integrations (Salesforce, HubSpot)
- Machine learning for job categorization and salary prediction

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is provided as-is for educational and commercial use.

## Disclaimer

- This tool uses SerpApi to query Google Jobs results
- Respect robots.txt and terms of service for all data sources
- API usage is subject to SerpApi's terms and pricing
- Job data is sourced from public job boards and company sites
- For high-volume usage, consider direct API agreements with job boards

## Support

For issues, questions, or feature requests:
- Open an issue on GitHub
- Check SerpApi documentation: https://serpapi.com/google-jobs-api

## Changelog

### v1.1.0 (Current)
- Added automatic analytics generation
- Top trades, companies, locations, and job board analysis
- Multi-sheet Excel analytics report
- Salary extraction framework (pseudo code)
- Comprehensive inline code documentation

### v1.0.0
- Initial release
- Multi-threaded company processing
- 100+ skilled trades keywords
- Rate limiting and retry logic
- Progressive checkpoint saves
- API limit handling

---

**Built for skilled trades recruitment in the aerospace industry**
