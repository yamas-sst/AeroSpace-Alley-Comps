# ======================================================
# Job Analytics Module
# ======================================================
# PURPOSE: Generate insights and statistics from job scraping results
#
# FEATURES:
#   - Identify most in-demand skilled trades
#   - Rank companies by hiring activity
#   - Analyze geographic job distribution
#   - Track job board sources
#   - Export analytics to Excel with charts
#
# USAGE:
#   from analytics import JobAnalytics
#   analytics = JobAnalytics(results_dataframe)
#   analytics.generate_report("analytics_report.xlsx")
# ======================================================

import pandas as pd
from collections import Counter
import re
from typing import List, Dict, Tuple


class JobAnalytics:
    """
    Analyzes job scraping results to provide hiring insights and trends.
    """

    def __init__(self, df: pd.DataFrame, company_tracking: List[Dict] = None):
        """
        Initialize analytics with job results DataFrame.

        Parameters:
            df (pd.DataFrame): Job results with columns:
                - Company, Job Title, Location, Via, Source URL,
                  Description Snippet, Timestamp
            company_tracking (List[Dict], optional): ADDED - Company-level metrics for tier analysis
        """
        self.df = df
        self.company_tracking = company_tracking if company_tracking else []  # ADDED
        self.trade_keywords = self._load_trade_keywords()

    def _load_trade_keywords(self) -> List[str]:
        """
        Load the same skilled trades keywords used in AeroComps.py
        This allows us to categorize jobs by trade type.
        """
        return [
            # Machining & Fabrication
            "machinist", "cnc", "mill operator", "lathe operator", "grinder", "toolmaker",
            "fabricator", "metalworker", "sheet metal", "precision machinist", "machine operator",
            "manual machinist", "setup operator", "g-code", "programmer", "tool and die", "die maker",
            "mold maker", "production machinist", "numerical control", "machining technician",

            # Assembly & Production
            "assembler", "assembly technician", "production operator", "production technician",
            "line operator", "mechanical assembler", "electromechanical assembler",
            "production worker", "manufacturing technician", "machine technician",
            "assembly lead", "manufacturing associate", "packaging operator", "composite technician",

            # Welding & Metalwork
            "welder", "tig welder", "mig welder", "arc welder", "fabrication welder",
            "pipe welder", "aluminum welder", "spot welder", "soldering", "brazing",
            "welding technician", "weld inspector", "fitter welder",

            # Maintenance & Repair
            "maintenance technician", "maintenance mechanic", "maintenance engineer",
            "industrial mechanic", "millwright", "equipment technician", "machine repair",
            "facilities technician", "mechanical technician", "preventive maintenance",
            "maintenance electrician", "repair technician", "hvac technician",
            "plant mechanic", "equipment maintenance",

            # Inspection & Quality
            "inspector", "quality inspector", "quality technician", "qc technician",
            "qa inspector", "ndt technician", "cmm operator", "quality assurance",
            "final inspector", "metrology technician", "dimensional inspector",

            # Electrical & Technical
            "electrician", "electrical technician", "electronics technician",
            "controls technician", "panel builder", "wire harness assembler",
            "electromechanical technician", "instrumentation technician", "automation technician",

            # Tooling & Setup
            "tool room", "tooling engineer", "setup technician", "fixture builder",
            "tool designer", "jig and fixture", "tooling technician",

            # Composites & Aerospace
            "composite technician", "lamination technician", "bonding technician",
            "aerospace assembler", "aircraft technician", "avionics technician",
            "sheet metal mechanic", "structures mechanic", "airframe mechanic",

            # Other Skilled Trades
            "plumber", "carpenter", "hvac installer", "painter", "coating technician",
            "surface finisher", "heat treat operator", "chemical processor", "machining apprentice",
            "maintenance apprentice", "journeyman", "technician apprentice"
        ]

    def analyze_top_trades(self, top_n: int = 15) -> pd.DataFrame:
        """
        Identify the most in-demand skilled trades by counting keyword occurrences in job titles.

        Algorithm:
            1. For each job title, identify all matching trade keywords
            2. Count frequency of each keyword across all jobs
            3. Return top N most frequent trades

        Parameters:
            top_n (int): Number of top trades to return (default: 15)

        Returns:
            pd.DataFrame: Columns [Trade, Job Count, Percentage]
        """
        trade_counts = Counter()

        # Count keyword occurrences in job titles
        for title in self.df["Job Title"]:
            title_lower = title.lower()
            for keyword in self.trade_keywords:
                if keyword.lower() in title_lower:
                    trade_counts[keyword] += 1

        # Convert to DataFrame
        total_jobs = len(self.df)
        top_trades = pd.DataFrame([
            {
                "Trade": trade,
                "Job Count": count,
                "Percentage": f"{(count/total_jobs)*100:.1f}%"
            }
            for trade, count in trade_counts.most_common(top_n)
        ])

        return top_trades

    def analyze_top_companies(self, top_n: int = 20) -> pd.DataFrame:
        """
        Identify companies with the most skilled trades job openings.

        Algorithm:
            1. Group jobs by company
            2. Count jobs per company
            3. Calculate percentage of total market
            4. Return top N companies

        Parameters:
            top_n (int): Number of top companies to return (default: 20)

        Returns:
            pd.DataFrame: Columns [Company, Job Count, Percentage, Market Share]
        """
        company_counts = self.df["Company"].value_counts().head(top_n)
        total_jobs = len(self.df)

        top_companies = pd.DataFrame({
            "Company": company_counts.index,
            "Job Count": company_counts.values,
            "Percentage": [f"{(count/total_jobs)*100:.1f}%" for count in company_counts.values],
            "Market Share": [f"{(count/total_jobs)*100:.2f}%" for count in company_counts.values]
        })

        return top_companies.reset_index(drop=True)

    def analyze_locations(self, top_n: int = 25) -> pd.DataFrame:
        """
        Identify geographic hotspots for skilled trades hiring.

        Algorithm:
            1. Extract city/state from location field
            2. Normalize location names (handle variations)
            3. Count jobs by location
            4. Return top N locations

        Parameters:
            top_n (int): Number of top locations to return (default: 25)

        Returns:
            pd.DataFrame: Columns [Location, Job Count, Percentage]
        """
        # Clean and standardize location data
        locations = self.df["Location"].fillna("Unknown")
        location_counts = locations.value_counts().head(top_n)
        total_jobs = len(self.df)

        top_locations = pd.DataFrame({
            "Location": location_counts.index,
            "Job Count": location_counts.values,
            "Percentage": [f"{(count/total_jobs)*100:.1f}%" for count in location_counts.values]
        })

        return top_locations.reset_index(drop=True)

    def analyze_job_boards(self) -> pd.DataFrame:
        """
        Identify which job boards/platforms have the most listings.

        This helps understand which job boards are most effective for
        skilled trades recruitment in aerospace.

        Returns:
            pd.DataFrame: Columns [Job Board, Job Count, Percentage]
        """
        board_counts = self.df["Via"].fillna("Unknown").value_counts()
        total_jobs = len(self.df)

        job_boards = pd.DataFrame({
            "Job Board": board_counts.index,
            "Job Count": board_counts.values,
            "Percentage": [f"{(count/total_jobs)*100:.1f}%" for count in board_counts.values]
        })

        return job_boards.reset_index(drop=True)

    def analyze_trade_by_company(self, top_companies: int = 10, top_trades: int = 10) -> pd.DataFrame:
        """
        Cross-analysis: Which trades are in highest demand at each company?

        Creates a matrix showing trade keyword frequency by company.
        Useful for understanding company-specific hiring patterns.

        Parameters:
            top_companies (int): Number of companies to analyze
            top_trades (int): Number of trades to show per company

        Returns:
            pd.DataFrame: Pivot table of trades by company
        """
        # Get top companies
        top_co_list = self.df["Company"].value_counts().head(top_companies).index.tolist()

        # Filter to top companies
        df_filtered = self.df[self.df["Company"].isin(top_co_list)].copy()

        # Extract primary trade keyword from each job title
        def extract_primary_trade(title):
            title_lower = title.lower()
            for keyword in self.trade_keywords:
                if keyword.lower() in title_lower:
                    return keyword.title()
            return "Other"

        df_filtered["Primary Trade"] = df_filtered["Job Title"].apply(extract_primary_trade)

        # Create pivot table
        pivot = pd.crosstab(
            df_filtered["Company"],
            df_filtered["Primary Trade"],
            margins=True,
            margins_name="Total"
        )

        return pivot

    def generate_summary_statistics(self) -> Dict[str, any]:
        """
        Generate overall summary statistics about the job dataset.

        Returns:
            dict: Key metrics about the dataset
        """
        return {
            "Total Jobs": len(self.df),
            "Unique Companies": self.df["Company"].nunique(),
            "Unique Locations": self.df["Location"].nunique(),
            "Date Range": f"{self.df['Timestamp'].min()} to {self.df['Timestamp'].max()}",
            "Job Boards Used": self.df["Via"].nunique(),
            "Average Jobs per Company": f"{len(self.df) / self.df['Company'].nunique():.1f}",
            "Companies with 10+ Jobs": len(self.df.groupby("Company").size()[lambda x: x >= 10]),
            "Companies with 1 Job": len(self.df.groupby("Company").size()[lambda x: x == 1]),
        }

    # ======================================================
    # ADDED: NEW TIER ANALYSIS METHODS
    # ======================================================

    def analyze_by_tier(self) -> pd.DataFrame:
        """
        ADDED: Analyze companies and jobs by tier.

        Returns:
            pd.DataFrame: Tier-level breakdown with success rates
        """
        if not self.company_tracking:
            return pd.DataFrame()  # Return empty if no tracking data

        tracking_df = pd.DataFrame(self.company_tracking)

        tier_analysis = tracking_df.groupby('Tier').agg({
            'Company': 'count',  # Total companies
            'Success': 'sum',  # Successful companies
            'Jobs Found': 'sum',  # Total jobs
            'Job Cap': 'first',  # Job cap for this tier
            'Employee Count': 'mean'  # Average employees
        }).reset_index()

        tier_analysis.columns = ['Tier', 'Companies Attempted', 'Companies Successful', 'Total Jobs', 'Job Cap', 'Avg Employees']
        tier_analysis['Success Rate'] = (tier_analysis['Companies Successful'] / tier_analysis['Companies Attempted'] * 100).round(1).astype(str) + '%'
        tier_analysis['Avg Jobs per Company'] = (tier_analysis['Total Jobs'] / tier_analysis['Companies Successful']).round(1)
        tier_analysis['Avg Employees'] = tier_analysis['Avg Employees'].round(0).astype(int)

        # Reorder columns
        tier_analysis = tier_analysis[['Tier', 'Companies Attempted', 'Companies Successful', 'Success Rate',
                                       'Total Jobs', 'Avg Jobs per Company', 'Job Cap', 'Avg Employees']]

        return tier_analysis.sort_values('Tier')

    def analyze_failed_companies(self) -> pd.DataFrame:
        """
        ADDED: Identify companies that returned no jobs.

        Returns:
            pd.DataFrame: Failed companies with tier info
        """
        if not self.company_tracking:
            return pd.DataFrame()

        tracking_df = pd.DataFrame(self.company_tracking)
        failed = tracking_df[tracking_df['Success'] == False].copy()

        failed = failed[['Company', 'Tier', 'Employee Count', 'Job Cap', 'Jobs Found']]
        failed = failed.sort_values('Tier')

        return failed

    def analyze_success_by_tier(self) -> Dict[str, any]:
        """
        ADDED: Generate tier-focused summary statistics.

        Returns:
            dict: Tier-level success metrics
        """
        if not self.company_tracking:
            return {}

        tracking_df = pd.DataFrame(self.company_tracking)

        total_companies = len(tracking_df)
        successful_companies = tracking_df['Success'].sum()
        overall_success_rate = (successful_companies / total_companies * 100) if total_companies > 0 else 0

        return {
            "Total Companies Attempted": total_companies,
            "Companies with Jobs Found": successful_companies,
            "Companies with No Jobs": total_companies - successful_companies,
            "Overall Success Rate": f"{overall_success_rate:.1f}%",
            "Tier 1 Success Rate": self._tier_success_rate(tracking_df, 1),
            "Tier 2 Success Rate": self._tier_success_rate(tracking_df, 2),
            "Tier 3 Success Rate": self._tier_success_rate(tracking_df, 3),
            "Tier 4 Success Rate": self._tier_success_rate(tracking_df, 4),
            "Tier 5 Success Rate": self._tier_success_rate(tracking_df, 5),
        }

    def _tier_success_rate(self, tracking_df: pd.DataFrame, tier: int) -> str:
        """Helper to calculate success rate for a specific tier"""
        tier_data = tracking_df[tracking_df['Tier'] == tier]
        if len(tier_data) == 0:
            return "N/A"
        success_rate = (tier_data['Success'].sum() / len(tier_data) * 100)
        return f"{success_rate:.1f}%"

    # ======================================================
    # END OF ADDED TIER ANALYSIS METHODS
    # ======================================================

    def generate_report(self, output_file: str = "job_analytics_report.xlsx"):
        """
        Generate comprehensive analytics report and export to Excel.

        Creates multi-sheet Excel workbook with:
            - Summary statistics
            - Top trades analysis
            - Top companies analysis
            - Location distribution
            - Job board analysis
            - Trade-by-company matrix

        Parameters:
            output_file (str): Path for output Excel file
        """
        print("\n" + "="*60)
        print("GENERATING ANALYTICS REPORT")
        print("="*60 + "\n")

        # Generate all analytics
        summary = self.generate_summary_statistics()
        top_trades = self.analyze_top_trades(top_n=20)
        top_companies = self.analyze_top_companies(top_n=25)
        top_locations = self.analyze_locations(top_n=30)
        job_boards = self.analyze_job_boards()
        trade_by_company = self.analyze_trade_by_company(top_companies=15, top_trades=15)

        # ADDED: Generate tier analytics
        tier_analysis = self.analyze_by_tier()
        tier_summary = self.analyze_success_by_tier()
        failed_companies = self.analyze_failed_companies()

        # Print summary to console
        print("📊 SUMMARY STATISTICS")
        print("-" * 60)
        for key, value in summary.items():
            print(f"  {key}: {value}")

        print("\n🔧 TOP 10 IN-DEMAND TRADES")
        print("-" * 60)
        print(top_trades.head(10).to_string(index=False))

        print("\n🏢 TOP 10 HIRING COMPANIES")
        print("-" * 60)
        print(top_companies.head(10)[["Company", "Job Count", "Percentage"]].to_string(index=False))

        print("\n📍 TOP 10 LOCATIONS")
        print("-" * 60)
        print(top_locations.head(10).to_string(index=False))

        # ADDED: Print tier analytics to console
        if not tier_analysis.empty:
            print("\n📊 TIER ANALYSIS")
            print("-" * 60)
            print(tier_analysis.to_string(index=False))

            print("\n📈 TIER SUCCESS METRICS")
            print("-" * 60)
            for key, value in tier_summary.items():
                print(f"  {key}: {value}")

            if not failed_companies.empty:
                print(f"\n❌ COMPANIES WITH NO JOBS ({len(failed_companies)} total)")
                print("-" * 60)
                print(failed_companies.head(10).to_string(index=False))
                if len(failed_companies) > 10:
                    print(f"   ... and {len(failed_companies) - 10} more (see Excel report)")

        # Export to Excel with multiple sheets
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            # Summary sheet
            summary_df = pd.DataFrame(list(summary.items()), columns=["Metric", "Value"])
            summary_df.to_excel(writer, sheet_name="Summary", index=False)

            # Top trades
            top_trades.to_excel(writer, sheet_name="Top Trades", index=False)

            # Top companies
            top_companies.to_excel(writer, sheet_name="Top Companies", index=False)

            # Locations
            top_locations.to_excel(writer, sheet_name="Locations", index=False)

            # Job boards
            job_boards.to_excel(writer, sheet_name="Job Boards", index=False)

            # Trade by company matrix
            trade_by_company.to_excel(writer, sheet_name="Trade by Company")

            # Raw data
            self.df.to_excel(writer, sheet_name="Raw Data", index=False)

            # ADDED: New tier analysis sheets
            if not tier_analysis.empty:
                tier_analysis.to_excel(writer, sheet_name="Tier Analysis", index=False)

            if tier_summary:
                tier_summary_df = pd.DataFrame(list(tier_summary.items()), columns=["Metric", "Value"])
                tier_summary_df.to_excel(writer, sheet_name="Tier Success Metrics", index=False)

            if not failed_companies.empty:
                failed_companies.to_excel(writer, sheet_name="Failed Companies", index=False)

        print(f"\n✅ Analytics report saved to: {output_file}")
        print("="*60 + "\n")


# ======================================================
# STANDALONE USAGE
# ======================================================
# If run directly, this script will analyze an existing job results file

if __name__ == "__main__":
    import sys

    # Default input file (can be overridden via command line)
    input_file = "Aerospace_Alley_SkilledTrades_Jobs.xlsx"
    output_file = "Job_Analytics_Report.xlsx"

    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]

    try:
        # Load job results
        print(f"Loading job data from: {input_file}")
        df = pd.read_excel(input_file)

        # Generate analytics
        analytics = JobAnalytics(df)
        analytics.generate_report(output_file)

    except FileNotFoundError:
        print(f"❌ Error: File '{input_file}' not found.")
        print("\nUsage: python analytics.py [input_file.xlsx] [output_file.xlsx]")
    except Exception as e:
        print(f"❌ Error generating analytics: {e}")
