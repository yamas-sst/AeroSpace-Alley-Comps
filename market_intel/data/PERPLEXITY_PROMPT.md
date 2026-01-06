# Perplexity Prompt for SpaceCom 2026 Exhibitor Extraction

Copy and paste the following prompt into Perplexity:

---

## PROMPT:

I need to extract the complete exhibitor list from SpaceCom | Space Mobility 2026.

**Event URL:** https://spc26.mapyourshow.com/8_0/explore/exhibitor-gallery.cfm

**Please provide:**

1. A complete list of ALL exhibiting companies from the SpaceCom | Space Mobility 2026 exhibitor gallery

2. For each company, extract (if available):
   - Company name (exact as listed)
   - Booth number
   - Website URL
   - Brief description or tagline
   - Category/industry segment

3. Format the output as a table or CSV-compatible format with these columns:
   ```
   company_name, booth_number, website, description, category
   ```

4. If the gallery has multiple pages or filters, please capture ALL exhibitors across all pages/categories.

5. Also note:
   - Total number of exhibitors
   - Any sponsor tiers (Platinum, Gold, etc.) if shown
   - Event dates and location

**Context:** I'm building a contact enrichment pipeline and need accurate exhibitor data. The website may require browsing the interactive gallery - please extract as much data as possible.

---

## ALTERNATIVE PROMPT (if first doesn't work):

Search for "SpaceCom Space Mobility 2026 exhibitor list" and find:

1. Any published exhibitor lists or directories for SpaceCom 2026
2. Press releases announcing exhibitors
3. News articles listing participating companies
4. The official floor plan showing booth assignments

Provide company names, booth numbers, and websites in a structured format.

---

## AFTER GETTING RESULTS:

1. Copy the exhibitor data from Perplexity's response
2. Paste into `market_intel/data/spacecom_2026_exhibitors.xlsx` (Exhibitors sheet)
3. Or directly edit `market_intel/data/exhibitors.csv`
4. Minimum required: company_name and website
5. Run test: `python market_intel/enrich_exhibitors.py --mock`
