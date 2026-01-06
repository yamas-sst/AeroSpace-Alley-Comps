# Legacy Repository Review & Migration to Market Analysis Platform

**Document Version:** 1.0
**Analysis Date:** January 2026
**Repository:** AeroSpace-Alley-Comps
**Analyst:** Technical Architect Review

---

## Executive Summary

This document provides a comprehensive code-level analysis of the AeroSpace-Alley-Comps repository and designs a forward-looking migration path to a scalable internal market analysis platform. The analysis is based on **actual file inspection**, not documentation inference.

**Key Findings:**
- The codebase is a **single-file monolith** (AeroComps.py at 1,318 lines) with well-structured supporting modules
- Rate limiting and API protection systems are **production-ready** and exceed documentation claims
- Company tiering logic is **hardcoded** but architecturally sound for extraction
- The system currently depends on **SerpAPI** (Google Jobs) as its sole data source
- Strategic planning documents reveal intent to expand to multiple industries and data sources

**Recommendation:** Phased migration preserving the robust protection layer while modularizing data acquisition and introducing licensed API integrations.

---

## Step 1: Repository Inventory (Verified from Code Inspection)

### 1.1 Root Directory Layout

```
AeroSpace-Alley-Comps/
├── AeroComps.py              # Main executable (1,318 lines, 56KB)
├── README.md                 # Documentation (36KB)
├── CHANGELOG.md              # Version history
├── PROJECT_STRUCTURE.md      # Architecture docs
├── .gitignore                # Excludes logs, state files, test outputs
├── data/                     # Input data
├── diagnostics/              # Testing and troubleshooting tools
├── docs/                     # Archived planning documents
├── future/                   # Strategic expansion plans
├── log/                      # Runtime logs and audit trails
└── resources/                # Configuration and modules
```

### 1.2 Executable Scripts and Their Purposes

| File | Lines | Actual Purpose (from code inspection) |
|------|-------|---------------------------------------|
| `AeroComps.py` | 1,318 | Main job scanner - queries SerpAPI, filters by trade keywords, exports to Excel |
| `resources/rate_limit_protection.py` | 956 | Comprehensive API protection: Token Bucket, Circuit Breaker, Exponential Backoff, Audit Logging |
| `resources/api_usage_tracker.py` | 342 | Persistent API quota tracking across sessions with multi-key rotation |
| `resources/analytics.py` | 513 | Post-run analytics: trade analysis, company rankings, tier breakdowns |
| `diagnostics/setup_check.py` | 184 | Pre-flight validation: dependencies, config, directories, API connectivity |
| `diagnostics/check_block_status.py` | 302 | IP block diagnostic: tests all keys, checks headers, provides recovery guidance |
| `diagnostics/quick_check.py` | ~80 | Minimal API connectivity test |
| `diagnostics/convert_test_csv_to_excel.py` | ~50 | Test data format conversion utility |

### 1.3 Configuration Files

| File | Format | Loading Mechanism |
|------|--------|-------------------|
| `resources/config.json` | JSON | Loaded at startup via `load_config()` function (lines 41-70 of AeroComps.py) |

**Configuration Structure (verified):**
```json
{
  "api_keys": [{"label": "...", "key": "...", "monthly_limit": 250, "priority": 1}],
  "active_profile": "tier_test",
  "profiles": {
    "quick_test": {"testing_mode": true, "testing_company_limit": 3},
    "production": {"testing_mode": false}
  },
  "settings": {
    "input_file": "data/Aerospace_Alley_Companies.xlsx",
    "api_limits": {"max_api_calls_per_key": 250, "min_interval_seconds": 3.2},
    "company_limits": {"tier1_job_cap": 80, "tier2_job_cap": 40, ...}
  }
}
```

### 1.4 Data Folders and Output Artifacts

| Directory | Contents | Purpose |
|-----------|----------|---------|
| `data/` | `Aerospace_Alley_Companies.xlsx` (22KB) | Input: 137 Connecticut aerospace companies |
| `log/` | `api_audit.jsonl`, `.gitkeep` | Runtime: JSON Lines audit log of all API calls |
| `output/` | (gitignored) | Generated Excel files with job results |
| `diagnostics/` | `Test_3_Companies.xlsx`, CSV test files | Testing datasets |

### 1.5 Logging, Diagnostics, and Safety Mechanisms

**Audit Logging (verified in `rate_limit_protection.py:533-626`):**
- JSON Lines format to `log/api_audit.jsonl`
- Records: timestamp, event_type, company, status_code, response_time_ms, jobs_found, api_key_label
- Event types: `api_call`, `rate_limit_detected`, `circuit_breaker_state_change`, `error`

**Health Monitoring (verified in `rate_limit_protection.py:633-841`):**
- Tracks: total_calls, successful_calls, failed_calls, rate_limit_errors, server_errors
- Alert thresholds: 20% failure rate, 3 consecutive failures, 2 rate limit errors
- Automatic fallback triggers with reason reporting

**State Persistence (verified in `api_usage_tracker.py:47-109`):**
- File: `log/api_usage_state.json`
- Tracks cumulative usage across script executions
- Automatic monthly reset based on billing cycle day

### 1.6 API References and Rate Limiting

**External API Dependency:**
- **SerpAPI** (https://serpapi.com/search.json)
- Engine: `google_jobs`
- Authentication: API key in query params
- Rate limits enforced: 3.2s minimum between calls, 60 calls/hour bucket capacity

**Rate Limit Implementation (verified):**
```
Token Bucket: capacity=60, refill_rate=0.3125/s (1 token per 3.2s)
Circuit Breaker: failure_threshold=3, timeout=300s, half_open_max_calls=3
Exponential Backoff: base_delay=2s, max_delay=60s, max_attempts=3
Batch Processor: batch_size=10, pause=45s between batches
```

---

## Step 2: Code-Level Intent Verification

### 2.1 AeroComps.py - Main Scanner

**What the code actually does (lines 993-1159):**

1. **Input Loading** (lines 874-889): Reads Excel file, extracts unique company names, applies testing limit if configured
2. **Query Building** (lines 918-962): Constructs search query as `"{company} machinist OR welder OR fabricator OR technician OR engineer OR supervisor OR electrician OR inspector"`
3. **API Requests** (lines 365-444): Thread-safe requests with rate limiting, circuit breaker checks, audit logging
4. **Response Validation** (lines 255-309): Validates HTTP status, JSON parsing, API error fields
5. **Job Filtering** (lines 537-568): Word-based matching against `CORE_TRADE_WORDS` list (65+ keywords), excludes medical/janitorial
6. **Company Matching** (lines 315-345): Fuzzy matching (65% threshold) to validate job is from target company
7. **Tier-Based Caps** (lines 702-854): Hardcoded company size database determines job caps (Tier 1: 80 jobs, Tier 99: 20 jobs)
8. **Output Generation** (lines 1264-1306): Deduplicates by Company+Title+URL, exports to Excel, generates analytics

**Inputs:**
- `data/Aerospace_Alley_Companies.xlsx` (Company Name column)
- `resources/config.json` (API keys, settings, profiles)

**Outputs:**
- `output/Aerospace_Alley_SkilledTrades_Jobs.xlsx`
- `output/*_Analytics.xlsx`
- `log/api_audit.jsonl`
- `log/api_usage_state.json`

**Side Effects:**
- API quota consumption (tracked persistently)
- Checkpoint saves every 25 companies (prevents data loss)

**Hardcoded Assumptions Limiting Reuse:**
- Connecticut location hardcoded in API params (line 1032)
- Trade keywords embedded in source (lines 483-528)
- Company size database embedded (lines 702-770) - ~40 companies manually curated
- SerpAPI-specific response parsing throughout

### 2.2 rate_limit_protection.py - Protection System

**What the code actually does:**

| Component | Implementation | Verification |
|-----------|---------------|--------------|
| `ConfigurationValidator` (lines 34-132) | Validates min_interval >= 2s, max_threads <= 3, calculates theoretical max calls/hour | **Stronger than documented** - enforces safety at startup |
| `TokenBucketRateLimiter` (lines 139-220) | RFC 6585 compliant, thread-safe with Lock, blocks until token available | **Production-ready** |
| `CircuitBreaker` (lines 227-325) | Netflix Hystrix pattern, CLOSED/OPEN/HALF_OPEN states, automatic recovery | **Production-ready** |
| `ExponentialBackoff` (lines 332-409) | RFC 7231 compliant, jitter for thundering herd prevention | **Production-ready** |
| `IntelligentBatchProcessor` (lines 416-526) | Human-like pausing between batches | Works but **simpler than documented** (no fatigue simulation) |
| `ComprehensiveAuditLogger` (lines 533-626) | JSON Lines structured logging | **Excellent for compliance** |
| `EnhancedHealthMonitor` (lines 633-841) | Real-time metrics, alert thresholds, fallback triggers | **Stronger than documented** - proactive failure detection |

**Where implementation exceeds documentation:**
- Health monitor has automatic fallback triggers not mentioned in README
- Circuit breaker recovery is fully automatic
- Audit logging captures more fields than documented

**Where implementation is weaker:**
- Batch processor pause calculation ignores fatigue factor (always returns `min_pause`)
- No actual parallel processing despite ThreadPoolExecutor import

### 2.3 api_usage_tracker.py - Quota Management

**What the code actually does:**
- Maintains persistent state in `log/api_usage_state.json`
- Tracks per-key usage with daily granularity
- Auto-rotates to next key when current exhausted
- Provides 60-second warning period before key switch (allows Ctrl+C)
- Automatic monthly reset based on billing cycle day

**Governance mechanisms present:**
- Usage warnings at 75%, 90%, 100% thresholds
- Full usage report generation (`get_usage_report()`)
- Daily usage breakdown for auditing

### 2.4 analytics.py - Reporting Module

**What the code actually does:**
- Analyzes job results DataFrame post-collection
- Generates: top trades, top companies, locations, job boards, trade-by-company matrix
- Tier analysis with success rate calculations
- Failed company identification
- Multi-sheet Excel export

**Limitation:** Analytics runs only after data collection; no historical trend analysis.

---

## Step 3: Reusable Primitives

### 3.1 Component Classification

| Component | Location | Classification | Justification |
|-----------|----------|----------------|---------------|
| **Token Bucket Rate Limiter** | `rate_limit_protection.py:139-220` | ✅ **Reuse as-is** | Industry-standard implementation, API-agnostic, thread-safe |
| **Circuit Breaker** | `rate_limit_protection.py:227-325` | ✅ **Reuse as-is** | Clean Netflix Hystrix pattern, no external dependencies |
| **Exponential Backoff** | `rate_limit_protection.py:332-409` | ✅ **Reuse as-is** | RFC-compliant, configurable, includes jitter |
| **Audit Logger** | `rate_limit_protection.py:533-626` | ✅ **Reuse as-is** | JSON Lines format, structured events, compliance-ready |
| **Health Monitor** | `rate_limit_protection.py:633-841` | 🔧 **Refactor and reuse** | Good metrics but alert thresholds are hardcoded |
| **API Usage Tracker** | `api_usage_tracker.py` | 🔧 **Refactor and reuse** | Multi-key rotation excellent; needs abstraction from SerpAPI specifics |
| **Configuration Validator** | `rate_limit_protection.py:34-132` | 🔧 **Refactor and reuse** | Validation logic sound; thresholds should be configurable |
| **Batch Processor** | `rate_limit_protection.py:416-526` | 🔧 **Refactor and reuse** | Pattern good but pause calculation oversimplified |
| **Company Tier System** | `AeroComps.py:702-854` | 🔧 **Refactor and reuse** | Logic sound; needs externalization to database/config |
| **Job Filtering (is_skilled_trade_job)** | `AeroComps.py:537-568` | 🔧 **Refactor and reuse** | Word-based matching works; keywords should be configurable |
| **Company Matching (fuzzy)** | `AeroComps.py:315-345` | ✅ **Reuse as-is** | Clean implementation using difflib |
| **Analytics Module** | `analytics.py` | 🔧 **Refactor and reuse** | Good reports; needs separation from pandas DataFrame coupling |
| **SerpAPI Query Builder** | `AeroComps.py:918-962` | 🔄 **Replace entirely** | Too tightly coupled to Google Jobs API specifics |
| **SerpAPI Response Parser** | `AeroComps.py:1098-1123` | 🔄 **Replace entirely** | Vendor-specific field extraction |
| **Main Execution Loop** | `AeroComps.py:1186-1246` | 🔄 **Replace entirely** | Monolithic; needs orchestration layer |

### 3.2 Extraction Priority

**High Value / Low Effort (Extract First):**
1. Rate Limit Protection Coordinator (entire module)
2. Fuzzy Company Matching
3. Audit Logger

**High Value / Medium Effort:**
4. API Usage Tracker (abstract from SerpAPI)
5. Company Tier System (externalize to JSON/database)
6. Job Filtering (configurable keyword lists)

**Medium Value / High Effort:**
7. Analytics Module (decouple from pandas)
8. Health Monitor (configurable thresholds)

---

## Step 4: Target System Architecture

### 4.1 Logical Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        MARKET ANALYSIS PLATFORM                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │
│  │  Event Sources  │  │  Company Intel  │  │  Contact Intel  │              │
│  │  ─────────────  │  │  ─────────────  │  │  ─────────────  │              │
│  │  • Trade Shows  │  │  • Dodge DCN    │  │  • ZoomInfo     │              │
│  │  • Conferences  │  │  • D&B          │  │  • Apollo       │              │
│  │  • SAM.gov      │  │  • Internal CRM │  │  • LinkedIn*    │              │
│  │  • FDA Approvals│  │  • SEC Filings  │  │  • Internal     │              │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘              │
│           │                    │                    │                        │
│           ▼                    ▼                    ▼                        │
│  ┌──────────────────────────────────────────────────────────────────┐       │
│  │                    INGESTION LAYER                                │       │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │       │
│  │  │ Rate Limiter │  │ Circuit      │  │ Audit        │            │       │
│  │  │ (Token       │  │ Breaker      │  │ Logger       │            │       │
│  │  │  Bucket)     │  │              │  │ (JSON Lines) │            │       │
│  │  └──────────────┘  └──────────────┘  └──────────────┘            │       │
│  │  ┌──────────────────────────────────────────────────┐            │       │
│  │  │         Source-Specific Connectors               │            │       │
│  │  │  • DodgeConnector  • ZoomInfoConnector           │            │       │
│  │  │  • SAMGovConnector • EventDirectoryConnector     │            │       │
│  │  └──────────────────────────────────────────────────┘            │       │
│  └──────────────────────────────────────────────────────────────────┘       │
│                                    │                                         │
│                                    ▼                                         │
│  ┌──────────────────────────────────────────────────────────────────┐       │
│  │                  NORMALIZATION LAYER                              │       │
│  │                                                                   │       │
│  │   Raw Data → Canonical Entities                                   │       │
│  │   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │       │
│  │   │  Company    │  │  Contact    │  │  Event      │              │       │
│  │   │  Entity     │  │  Entity     │  │  Entity     │              │       │
│  │   │  ─────────  │  │  ─────────  │  │  ─────────  │              │       │
│  │   │  • ID       │  │  • ID       │  │  • ID       │              │       │
│  │   │  • Name     │  │  • Name     │  │  • Name     │              │       │
│  │   │  • Size     │  │  • Title    │  │  • Date     │              │       │
│  │   │  • Industry │  │  • Company  │  │  • Location │              │       │
│  │   │  • Location │  │  • Email    │  │  • Type     │              │       │
│  │   │  • Tier     │  │  • Phone    │  │  • Companies│              │       │
│  │   └─────────────┘  └─────────────┘  └─────────────┘              │       │
│  │                                                                   │       │
│  │   Survivorship Rules: Latest wins, Confidence scoring            │       │
│  └──────────────────────────────────────────────────────────────────┘       │
│                                    │                                         │
│                                    ▼                                         │
│  ┌──────────────────────────────────────────────────────────────────┐       │
│  │                  SCORING & ENRICHMENT LAYER                       │       │
│  │                                                                   │       │
│  │   ┌─────────────────────────────────────────────────┐            │       │
│  │   │              Scoring Engine                      │            │       │
│  │   │  • Company Score (size, growth, industry fit)   │            │       │
│  │   │  • Contact Score (title, department, seniority) │            │       │
│  │   │  • Timing Score (event proximity, hiring spike) │            │       │
│  │   │  • Composite Score (weighted combination)       │            │       │
│  │   └─────────────────────────────────────────────────┘            │       │
│  │                                                                   │       │
│  │   ┌─────────────────────────────────────────────────┐            │       │
│  │   │           Explainability Module                  │            │       │
│  │   │  • Score breakdown per signal                   │            │       │
│  │   │  • Source attribution                           │            │       │
│  │   │  • Confidence intervals                         │            │       │
│  │   └─────────────────────────────────────────────────┘            │       │
│  └──────────────────────────────────────────────────────────────────┘       │
│                                    │                                         │
│                                    ▼                                         │
│  ┌──────────────────────────────────────────────────────────────────┐       │
│  │                  ACTIVATION & EXPORT LAYER                        │       │
│  │                                                                   │       │
│  │   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │       │
│  │   │ Target Lists │  │ CRM Export   │  │ Analytics    │           │       │
│  │   │ (Audited)    │  │ (Salesforce) │  │ Dashboard    │           │       │
│  │   └──────────────┘  └──────────────┘  └──────────────┘           │       │
│  │                                                                   │       │
│  │   Export Audit: who, when, what, why (full traceability)         │       │
│  └──────────────────────────────────────────────────────────────────┘       │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Data Model Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CANONICAL DATA MODEL                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  COMPANY                          CONTACT                                    │
│  ────────────────────────         ────────────────────────                   │
│  company_id (PK)                  contact_id (PK)                            │
│  canonical_name                   first_name                                 │
│  display_name                     last_name                                  │
│  employee_count                   title                                      │
│  employee_count_source            department                                 │
│  employee_count_date              seniority_level                            │
│  tier (1-5, 99)                   company_id (FK)                            │
│  industry_codes[]                 email                                      │
│  naics_codes[]                    email_source                               │
│  location_hq                      phone                                      │
│  locations[]                      linkedin_url                               │
│  website                          source_system                              │
│  linkedin_url                     source_record_id                           │
│  duns_number                      confidence_score                           │
│  created_at                       created_at                                 │
│  updated_at                       updated_at                                 │
│  source_provenance[]              source_provenance[]                        │
│                                                                              │
│  EVENT                            COMPANY_EVENT (Junction)                   │
│  ────────────────────────         ────────────────────────                   │
│  event_id (PK)                    company_id (FK)                            │
│  event_name                       event_id (FK)                              │
│  event_type (trade_show,          participation_type (exhibitor,             │
│    conference, contract_award)      attendee, sponsor)                       │
│  start_date                       booth_number                               │
│  end_date                         confirmed_at                               │
│  location                         source_system                              │
│  industry_focus[]                                                            │
│  expected_attendance                                                         │
│  source_url                       SCORING_SIGNAL                             │
│  source_system                    ────────────────────────                   │
│  created_at                       signal_id (PK)                             │
│                                   entity_type (company/contact)              │
│  SOURCE_PROVENANCE                entity_id                                  │
│  ────────────────────────         signal_type (hiring_spike,                 │
│  provenance_id (PK)                 contract_award, event_proximity)         │
│  entity_type                      signal_value                               │
│  entity_id                        signal_date                                │
│  field_name                       evidence_url                               │
│  source_system                    confidence                                 │
│  source_record_id                 expires_at                                 │
│  captured_at                                                                 │
│  raw_value                        EXPORT_AUDIT                               │
│  confidence                       ────────────────────────                   │
│                                   export_id (PK)                             │
│                                   exported_by                                │
│                                   exported_at                                │
│                                   export_type (list, report)                 │
│                                   entity_ids[]                               │
│                                   filter_criteria                            │
│                                   purpose                                    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4.3 Ingestion Flow

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Schedule   │────▶│   Connector  │────▶│  Rate Limit  │────▶│   Raw Data   │
│   Trigger    │     │   Selection  │     │  + Circuit   │     │   Storage    │
│  (Weekly)    │     │              │     │   Breaker    │     │              │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
                                                                      │
                     ┌──────────────┐     ┌──────────────┐            │
                     │   Canonical  │◀────│   Schema     │◀───────────┘
                     │   Entity     │     │   Mapping    │
                     │   Storage    │     │              │
                     └──────────────┘     └──────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │  Provenance  │
                     │   Logging    │
                     └──────────────┘
```

**Connector Interface (proposed):**

```python
class SourceConnector(ABC):
    """Base class for all data source connectors."""

    @abstractmethod
    def connect(self) -> bool:
        """Establish connection to data source."""
        pass

    @abstractmethod
    def fetch_companies(self, filters: dict) -> Iterator[RawCompany]:
        """Yield raw company records."""
        pass

    @abstractmethod
    def fetch_contacts(self, company_id: str) -> Iterator[RawContact]:
        """Yield raw contact records for a company."""
        pass

    @abstractmethod
    def get_rate_limits(self) -> RateLimitConfig:
        """Return rate limit configuration for this source."""
        pass

    @property
    @abstractmethod
    def source_name(self) -> str:
        """Unique identifier for this source."""
        pass
```

### 4.4 Scoring and Enrichment Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         SCORING PIPELINE                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   INPUT: Canonical Company Entity                                            │
│                                                                              │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │  SIGNAL COLLECTORS                                                   │   │
│   │                                                                      │   │
│   │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │   │
│   │  │ Size Signal  │  │ Growth Signal│  │ Timing Signal│               │   │
│   │  │ ──────────── │  │ ──────────── │  │ ──────────── │               │   │
│   │  │ employee_cnt │  │ hiring_delta │  │ event_days   │               │   │
│   │  │ tier         │  │ contract_won │  │ contract_age │               │   │
│   │  │ revenue_est  │  │ funding_round│  │ fiscal_cycle │               │   │
│   │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘               │   │
│   │         │                 │                 │                        │   │
│   │         ▼                 ▼                 ▼                        │   │
│   │  ┌─────────────────────────────────────────────────────────────┐    │   │
│   │  │              WEIGHTED SCORE CALCULATOR                       │    │   │
│   │  │                                                              │    │   │
│   │  │  composite = (size_score * 0.3) +                           │    │   │
│   │  │              (growth_score * 0.4) +                         │    │   │
│   │  │              (timing_score * 0.3)                           │    │   │
│   │  │                                                              │    │   │
│   │  │  Weights configurable per use case                          │    │   │
│   │  └─────────────────────────────────────────────────────────────┘    │   │
│   │                              │                                       │   │
│   └──────────────────────────────┼───────────────────────────────────────┘   │
│                                  ▼                                           │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │  EXPLAINABILITY OUTPUT                                               │   │
│   │                                                                      │   │
│   │  {                                                                   │   │
│   │    "company_id": "COMP-12345",                                      │   │
│   │    "composite_score": 87,                                           │   │
│   │    "breakdown": {                                                   │   │
│   │      "size": {"score": 80, "reason": "Tier 2 (1000+ employees)"},  │   │
│   │      "growth": {"score": 95, "reason": "Hiring +40% vs baseline"}, │   │
│   │      "timing": {"score": 85, "reason": "Trade show in 45 days"}    │   │
│   │    },                                                               │   │
│   │    "evidence": [                                                    │   │
│   │      {"source": "dodge_dcn", "field": "employee_count", "date": ...}│   │
│   │    ],                                                               │   │
│   │    "confidence": 0.82                                               │   │
│   │  }                                                                   │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4.5 Activation and Export Flow

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   User       │────▶│   Filter &   │────▶│   Audit      │────▶│   Export     │
│   Request    │     │   Select     │     │   Record     │     │   Generate   │
│              │     │              │     │              │     │              │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
                                                                      │
                     ┌───────────────────────────────────────────────┐
                     │                                               │
                     ▼                                               ▼
              ┌──────────────┐                              ┌──────────────┐
              │   Excel      │                              │   CRM        │
              │   Download   │                              │   Push       │
              │              │                              │ (Salesforce) │
              └──────────────┘                              └──────────────┘

EXPORT_AUDIT record created for every export:
- Who requested
- When exported
- Which entities included
- Filter criteria used
- Stated purpose
```

---

## Step 5: Migration Strategy

### 5.1 Phased Approach Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         MIGRATION PHASES                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  PHASE 1: Foundation (Weeks 1-4)                                            │
│  ────────────────────────────────                                           │
│  • Extract protection layer to standalone package                            │
│  • Create connector interface abstraction                                    │
│  • Build configuration externalization                                       │
│  • Legacy continues running unchanged                                        │
│                                                                              │
│  PHASE 2: Parallel Operation (Weeks 5-8)                                    │
│  ────────────────────────────────────────                                   │
│  • Build first licensed connector (Dodge DCN)                               │
│  • Create normalization layer                                                │
│  • Run new system in shadow mode alongside legacy                           │
│  • Compare outputs for validation                                            │
│                                                                              │
│  PHASE 3: Feature Parity (Weeks 9-12)                                       │
│  ─────────────────────────────────────                                      │
│  • Add remaining connectors (ZoomInfo, event directories)                   │
│  • Implement scoring engine                                                  │
│  • Build export/audit layer                                                  │
│  • Legacy frozen (no new features)                                          │
│                                                                              │
│  PHASE 4: Cutover (Weeks 13-16)                                             │
│  ──────────────────────────────                                             │
│  • Production traffic to new system                                          │
│  • Legacy available for rollback                                             │
│  • Deprecation warnings on legacy                                            │
│                                                                              │
│  PHASE 5: Archive (Week 17+)                                                │
│  ───────────────────────────                                                │
│  • Legacy code archived to branch                                            │
│  • Documentation updated                                                     │
│  • SerpAPI dependency removed                                                │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 What Moves First

| Component | Phase | Rationale |
|-----------|-------|-----------|
| `rate_limit_protection.py` (entire module) | Phase 1 | Zero dependencies, production-ready, enables all connectors |
| Configuration externalization | Phase 1 | Unblocks all other work |
| Company tier system | Phase 1 | Core business logic, needs database backing |
| Fuzzy company matching | Phase 1 | Reusable across all sources |
| First licensed connector | Phase 2 | Proves architecture, provides real value |
| Normalization layer | Phase 2 | Required for multi-source integration |
| Analytics module | Phase 3 | Lower priority, works on any data |

### 5.3 What Stays Temporarily

| Component | Until Phase | Reason |
|-----------|-------------|--------|
| `AeroComps.py` main loop | Phase 4 | Continues providing value during migration |
| SerpAPI integration | Phase 4 | Backup data source until licensed sources proven |
| Excel output format | Phase 3 | Users familiar with format |
| `api_usage_tracker.py` | Phase 2 | Adapt for multi-source tracking |

### 5.4 What Is Frozen and Archived

| Component | Freeze Point | Archive Point |
|-----------|--------------|---------------|
| `COMPANY_SIZE_DATABASE` hardcoded dict | Phase 1 | Phase 5 (move to database) |
| `CORE_TRADE_WORDS` embedded list | Phase 1 | Phase 5 (move to config) |
| SerpAPI query builder | Phase 2 | Phase 5 |
| SerpAPI response parser | Phase 2 | Phase 5 |
| Monolithic main loop | Phase 3 | Phase 5 |

### 5.5 What Is Rebuilt Cleanly

| Component | New Implementation |
|-----------|-------------------|
| Data acquisition | Connector interface with pluggable sources |
| Company identification | Entity resolution with confidence scoring |
| Job/hiring detection | Multi-source signal aggregation |
| Output generation | Templated exports with audit trail |
| Scheduling | Proper job scheduler (not script invocation) |

### 5.6 Legacy Wrapper Strategy

During Phase 2-3, legacy code can be wrapped to participate in new architecture:

```python
class LegacySerpAPIConnector(SourceConnector):
    """Wraps existing AeroComps.py logic as a connector."""

    def __init__(self):
        # Import existing modules
        from resources.rate_limit_protection import RateLimitProtectionCoordinator
        from resources.api_usage_tracker import PersistentAPIUsageTracker

        self.protection = RateLimitProtectionCoordinator(config)
        self.tracker = PersistentAPIUsageTracker(config)

    def fetch_companies(self, filters: dict) -> Iterator[RawCompany]:
        # Reuse existing fetch_jobs_for_company logic
        # Transform output to canonical format
        pass

    @property
    def source_name(self) -> str:
        return "legacy_serpapi"
```

---

## Step 6: Trust, Governance, and Accuracy Guardrails

### 6.1 Source Provenance Requirements

**Every field must track:**

```python
@dataclass
class FieldProvenance:
    source_system: str        # "dodge_dcn", "zoominfo", "legacy_serpapi"
    source_record_id: str     # Original record ID in source system
    captured_at: datetime     # When we fetched this data
    raw_value: Any            # Original value before transformation
    transformed_value: Any    # Value after normalization
    confidence: float         # 0.0-1.0 confidence score
    transformation_rules: List[str]  # What transformations applied
```

**Legacy Gap:** Current system does not track provenance. Jobs are stored with `Timestamp` of when scraped but no source_record_id or confidence scoring.

### 6.2 Timestamped Evidence for Scoring Signals

**Requirement:** Every scoring signal must have:

```python
@dataclass
class ScoringSignal:
    signal_type: str          # "hiring_spike", "contract_award", "event_proximity"
    signal_value: float       # Normalized score 0-100
    evidence_date: datetime   # When the underlying event occurred
    evidence_url: Optional[str]  # Link to source if available
    evidence_snapshot: str    # Text excerpt proving the signal
    expires_at: datetime      # When this signal should be discounted
    confidence: float         # How sure we are this signal is accurate
```

**Legacy Gap:** Current system has no scoring signals - just binary job presence. The tier system (lines 702-854) is static, not evidence-based.

### 6.3 Survivorship Rules for Conflicting Sources

**When sources disagree, apply these rules:**

| Field | Rule | Rationale |
|-------|------|-----------|
| `employee_count` | Prefer licensed source (Dodge/D&B) > ZoomInfo > legacy | Licensed sources contractually accurate |
| `company_name` | Use canonical name from highest-confidence source | Avoid duplicates |
| `contact_email` | Most recent verified > older unverified | Email validity decays |
| `contact_title` | Most recent > older | Titles change frequently |
| `company_location` | HQ from licensed source, all locations aggregated | Multi-location companies |

**Conflict Resolution Log:**

```python
@dataclass
class ConflictResolution:
    entity_id: str
    field_name: str
    winning_value: Any
    winning_source: str
    losing_values: List[Tuple[Any, str]]  # (value, source) pairs
    resolution_rule: str
    resolved_at: datetime
```

**Legacy Gap:** No multi-source support, no conflict resolution. Single source (SerpAPI) only.

### 6.4 Export Audit Requirements

**Every export must create audit record:**

```python
@dataclass
class ExportAudit:
    export_id: str
    exported_by: str          # User ID or API key
    exported_at: datetime
    export_type: str          # "contact_list", "company_report", "analytics"
    entity_count: int
    entity_ids: List[str]     # Full list of exported entities
    filter_criteria: dict     # How the list was filtered
    purpose: str              # User-stated purpose
    destination: str          # "excel_download", "salesforce_push", "email"
    retention_days: int       # How long export is valid
```

**Legacy Gap:** Current system has no export auditing. Excel files generated without tracking who requested or why.

### 6.5 Separation of Data Layers

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         DATA LAYER SEPARATION                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  RAW DATA LAYER                                                              │
│  ───────────────                                                             │
│  • Unchanged from source                                                     │
│  • Full provenance metadata                                                  │
│  • Retained for audit trail                                                  │
│  • Never exposed to end users                                                │
│                                                                              │
│  NORMALIZED DATA LAYER                                                       │
│  ─────────────────────                                                       │
│  • Canonical entity format                                                   │
│  • Survivorship rules applied                                                │
│  • Confidence scores calculated                                              │
│  • Used for scoring and enrichment                                           │
│                                                                              │
│  DERIVED INSIGHTS LAYER                                                      │
│  ──────────────────────                                                      │
│  • Scoring signals                                                           │
│  • Composite scores                                                          │
│  • Explainability outputs                                                    │
│  • Expires/refreshes on schedule                                             │
│                                                                              │
│  ACTIVATION LAYER                                                            │
│  ────────────────                                                            │
│  • Target lists (audited)                                                    │
│  • CRM-ready exports                                                         │
│  • Analytics dashboards                                                      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 6.6 Legacy System Governance Assessment

| Governance Requirement | Legacy Support | Gap Severity |
|----------------------|----------------|--------------|
| Source provenance per field | ❌ Not present | **High** |
| Timestamped evidence | ⚠️ Partial (Timestamp field only) | **Medium** |
| Survivorship rules | ❌ Not applicable (single source) | **Low** (no conflict) |
| Export audit logs | ❌ Not present | **High** |
| Data layer separation | ❌ All in one Excel file | **Medium** |
| API audit logging | ✅ **Excellent** (JSON Lines) | None |
| Rate limit compliance | ✅ **Excellent** | None |
| Usage tracking | ✅ **Good** (persistent state) | None |

---

## Step 7: Concrete Next Actions

### 7.1 Immediate Actions (This Week)

| Action | Owner | Files | Effort |
|--------|-------|-------|--------|
| **Extract protection module to package** | Dev | `resources/rate_limit_protection.py` | 2 hours |
| **Create `connectors/` directory structure** | Dev | New directory | 30 min |
| **Externalize company tier data to JSON** | Dev | `AeroComps.py:702-770` → `resources/company_tiers.json` | 2 hours |
| **Externalize trade keywords to JSON** | Dev | `AeroComps.py:483-528` → `resources/trade_keywords.json` | 1 hour |
| **Document connector interface spec** | Architect | New `docs/connector_interface.md` | 3 hours |

### 7.2 First Connector Build (Weeks 2-3)

| Action | Files | Effort |
|--------|-------|--------|
| **Evaluate Dodge DCN API documentation** | Research | 4 hours |
| **Build DodgeConnector skeleton** | `connectors/dodge_dcn.py` | 8 hours |
| **Implement rate limiting for Dodge** | Reuse `rate_limit_protection.py` | 2 hours |
| **Test with 10 companies** | Test scripts | 4 hours |
| **Compare output to legacy SerpAPI** | Validation | 4 hours |

### 7.3 MVP Outputs to Produce

**By End of Phase 1 (Week 4):**
- [ ] Protection layer as installable package
- [ ] Connector interface documentation
- [ ] Company tiers externalized and validated
- [ ] Trade keywords configurable

**By End of Phase 2 (Week 8):**
- [ ] One licensed connector operational (Dodge DCN recommended)
- [ ] Normalization layer for companies
- [ ] Shadow comparison report (legacy vs. new)
- [ ] Source provenance tracking implemented

**By End of Phase 3 (Week 12):**
- [ ] Scoring engine with explainability
- [ ] Export audit logging
- [ ] Second connector (ZoomInfo or event directory)
- [ ] User-facing analytics dashboard

### 7.4 What Can Be Safely Postponed

| Component | Postpone Until | Reason |
|-----------|----------------|--------|
| Contact acquisition (ZoomInfo) | Phase 3+ | Company intelligence is higher priority |
| CRM integration (Salesforce) | Phase 4+ | Excel exports sufficient initially |
| Multi-industry expansion | Post-Phase 5 | Validate single industry first |
| Real-time streaming ingestion | Future | Batch weekly/monthly is sufficient |
| Machine learning scoring | Future | Rule-based scoring adequate initially |

### 7.5 Validation Approach

**Cannot validate from repository:**
- Actual API response formats from licensed sources (Dodge, ZoomInfo)
- Current data quality and coverage gaps
- User workflows and pain points
- Budget constraints for licensed data

**Requires stakeholder input:**
- Priority ranking of data sources
- Scoring weight preferences
- Export format requirements
- Compliance/legal review of data usage

---

## Appendix A: File-by-File Reference

| File | Lines | Primary Function | Migration Disposition |
|------|-------|------------------|----------------------|
| `AeroComps.py` | 1,318 | Main scanner | Phase 4 deprecation |
| `resources/rate_limit_protection.py` | 956 | API protection | Phase 1 extraction |
| `resources/api_usage_tracker.py` | 342 | Quota tracking | Phase 2 refactor |
| `resources/analytics.py` | 513 | Report generation | Phase 3 refactor |
| `resources/config.json` | 77 | Configuration | Phase 1 expansion |
| `diagnostics/setup_check.py` | 184 | Pre-flight checks | Keep as-is |
| `diagnostics/check_block_status.py` | 302 | IP block diagnosis | Keep as-is |
| `future/EXTERNAL_API_OPTIONS_MINIMAL_COST.md` | 554 | API evaluation | Reference for Phase 2 |
| `future/STRATEGY_INDUSTRY_EXPANSION.md` | 694 | Expansion strategy | Reference for post-Phase 5 |

---

## Appendix B: Risk Register

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Licensed API costs exceed budget | Medium | High | Start with Dodge free trial; validate ROI before commitment |
| Data quality from new sources worse than legacy | Medium | Medium | Run shadow comparison for full month before cutover |
| Migration timeline extends | High | Medium | Legacy continues operating; no hard deadline |
| Key personnel unavailable | Low | High | Document thoroughly; no single point of failure |
| Compliance issues with data usage | Low | High | Legal review before Phase 2 connector work |

---

## Appendix C: Glossary

| Term | Definition |
|------|------------|
| **Canonical Entity** | Standardized representation of a company, contact, or event after normalization |
| **Connector** | Module that interfaces with a specific data source API |
| **Provenance** | Metadata tracking the origin and transformation history of a data field |
| **Survivorship Rule** | Logic determining which value wins when multiple sources conflict |
| **Scoring Signal** | A discrete piece of evidence contributing to a company/contact score |
| **Tier** | Company size classification (1-5 based on employees, 99 for unknown) |

---

*Document generated from code inspection of AeroSpace-Alley-Comps repository. All assertions verified against actual source files unless explicitly noted as requiring stakeholder validation.*
