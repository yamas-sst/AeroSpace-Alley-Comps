# Market Intel - Contact Enrichment Pipeline

A self-contained package for enriching exhibitor data with contact information.

## Quick Start

```bash
# Install dependencies
pip install pandas openpyxl requests

# Test with mock data (no API key needed)
python market_intel/enrich_exhibitors.py --mock

# Production run (requires Apollo.io API key)
python market_intel/enrich_exhibitors.py
```

## Setup in New Project

1. Copy the entire `market_intel/` folder to your project root
2. Install dependencies: `pip install pandas openpyxl requests`
3. Add your exhibitor data to `market_intel/data/exhibitors.csv`
4. Add your Apollo.io API key to `market_intel/config.json`
5. Run the pipeline

## Directory Structure

```
market_intel/
├── __init__.py                 # Package marker
├── enrich_exhibitors.py        # Main CLI entry point
├── config.json                 # Configuration (add API key here)
│
├── connectors/
│   ├── __init__.py
│   ├── base.py                 # Base connector with protection layer
│   └── apollo.py               # Apollo.io + Mock connectors
│
├── legacy/                     # Preserved protection layer
│   ├── __init__.py
│   └── rate_limit_protection.py
│
├── data/
│   ├── exhibitors.csv          # Your input data (fill this in)
│   ├── spacecom_2026_exhibitors.xlsx  # Excel template
│   └── PERPLEXITY_PROMPT.md    # Prompt to extract exhibitor data
│
├── templates/
│   └── exhibitor_template.csv  # CSV format reference
│
└── output/                     # Generated files (gitignored)
```

## Input Format (CSV)

Required columns:
- `company_name` (REQUIRED)
- `website` (strongly recommended for enrichment)

Optional columns:
- `booth_number`, `address`, `city`, `state`, `zip`, `country`, `description`, `category`

## Configuration

Edit `market_intel/config.json`:

```json
{
  "enrichment": {
    "api_key": "YOUR_APOLLO_API_KEY_HERE"
  }
}
```

Get your Apollo.io API key at: https://app.apollo.io/#/settings/integrations/api

## Usage

```bash
# Test mode (no API calls)
python market_intel/enrich_exhibitors.py --mock

# Production mode
python market_intel/enrich_exhibitors.py

# Custom input/output
python market_intel/enrich_exhibitors.py --input path/to/data.csv --output path/to/output.xlsx
```

## Output

Excel file with 3 sheets:
- **Contacts**: One row per contact (name, title, email, phone, LinkedIn)
- **Companies**: One row per company (status, contacts found, errors)
- **Metadata**: Run summary and statistics

## Protection Layer

Built-in from legacy system:
- **Token Bucket Rate Limiter**: Prevents API rate limit hits
- **Circuit Breaker**: Stops on repeated failures
- **Exponential Backoff**: Graceful retry on errors
- **Audit Logger**: JSON Lines log at `log/enrichment_audit.jsonl`

## Dependencies

- Python 3.8+
- pandas
- openpyxl
- requests
