# Market Analysis Platform - Complete Migration Plan

**Document Version:** 2.0
**Purpose:** Single source of truth for migrating to the new market analysis platform
**Timeline:** 3 days
**Priority:** Speed and accuracy

---

## Table of Contents

0. [Prerequisites](#0-prerequisites)
1. [Executive Summary](#1-executive-summary)
2. [Current System Analysis](#2-current-system-analysis)
   - 2.1 Legacy System Summary
   - 2.2 Component Classification (Reuse/Refactor/Replace)
   - 2.3 Detailed File Inventory
3. [Target System Architecture](#3-target-system-architecture)
4. [Data Flow Design](#4-data-flow-design)
5. [Implementation Code](#5-implementation-code)
6. [Configuration Files](#6-configuration-files)
7. [Directory Structure](#7-directory-structure)
8. [Step-by-Step Migration](#8-step-by-step-migration)
9. [Testing Procedures](#9-testing-procedures)
10. [Troubleshooting](#10-troubleshooting)
11. [Trust, Governance, and Accuracy Guardrails](#11-trust-governance-and-accuracy-guardrails)
12. [Concrete Next Actions](#12-concrete-next-actions)

**Appendices:**
- A: Apollo.io API Reference
- B: Alternative Enrichment Providers
- C: MapYourShow API Reference (Future Use)
- D: Legacy System Reference

---

## 0. Prerequisites

### Dependencies to Install

```bash
pip install pandas openpyxl requests
```

### Decision Context

**Path Options Evaluated:**
- **Path A**: Get MapYourShow API credentials → Build connector → Clean data (Fastest if credentials available)
- **Path B**: Manual export from MapYourShow + enrichment pipeline ← **SELECTED**
- **Path C**: Use Apify scraper ($5-50) → Build integration

**Why Path B:** User collecting exhibitor data manually from MapYourShow gallery; API credentials not yet available.

**Key Constraint:** 3 days, not 17 weeks. Speed and accuracy prioritized.

---

## 1. Executive Summary

### What We're Building

```
INPUT:  SpaceCom Exhibitor Data (MapYourShow manual export)
        ↓
PROCESS: Contact Enrichment (Apollo.io API)
        ↓
OUTPUT: Excel with Companies + Contacts + Provenance
```

### What We're Keeping from Legacy

| Component | Location | Action |
|-----------|----------|--------|
| Token Bucket Rate Limiter | `resources/rate_limit_protection.py:139-220` | **Reuse directly** |
| Circuit Breaker | `resources/rate_limit_protection.py:227-325` | **Reuse directly** |
| Exponential Backoff | `resources/rate_limit_protection.py:332-409` | **Reuse directly** |
| Audit Logger | `resources/rate_limit_protection.py:533-626` | **Reuse directly** |
| Fuzzy Company Matching | `AeroComps.py:315-345` | **Copy function** |

### What We're NOT Touching

- `AeroComps.py` - Leave as-is (SerpAPI job scanner still works)
- `resources/` - Leave as-is (we import from it)
- `data/` - Leave as-is
- `diagnostics/` - Leave as-is

---

## 2. Current System Analysis

### 2.1 Legacy System Summary (from code inspection)

**Main Script:** `AeroComps.py` (1,318 lines)
- Queries SerpAPI Google Jobs for 137 CT aerospace companies
- Filters jobs by skilled trades keywords
- Exports to Excel with analytics

**Protection Layer:** `resources/rate_limit_protection.py` (956 lines)
- Token Bucket: 60 capacity, refills at configured rate
- Circuit Breaker: Opens after 3 failures, 5-minute timeout
- Exponential Backoff: 2s base, 60s max, 3 attempts
- Audit Logger: JSON Lines to `log/api_audit.jsonl`

**Key Functions to Reuse:**

```python
# From resources/rate_limit_protection.py - IMPORT DIRECTLY
from resources.rate_limit_protection import (
    TokenBucketRateLimiter,
    CircuitBreaker,
    ExponentialBackoff,
    ComprehensiveAuditLogger
)
```

```python
# From AeroComps.py:315-345 - COPY THIS FUNCTION
def validate_company_match(target_company, api_company, threshold=0.65):
    """
    Validates that job is from target company (fuzzy matching).
    """
    if not api_company:
        return False

    from difflib import SequenceMatcher
    import re

    target_clean = re.sub(r'[^a-z0-9\s-]', '', target_company.lower())
    api_clean = re.sub(r'[^a-z0-9\s-]', '', api_company.lower())

    similarity = SequenceMatcher(None, target_clean, api_clean).ratio()
    return similarity >= threshold
```

### 2.2 Component Classification (Reuse/Refactor/Replace)

| Component | Location | Classification | 3-Day Action |
|-----------|----------|----------------|--------------|
| **Token Bucket Rate Limiter** | `rate_limit_protection.py:139-220` | ✅ **Reuse as-is** | Import directly |
| **Circuit Breaker** | `rate_limit_protection.py:227-325` | ✅ **Reuse as-is** | Import directly |
| **Exponential Backoff** | `rate_limit_protection.py:332-409` | ✅ **Reuse as-is** | Import directly |
| **Audit Logger** | `rate_limit_protection.py:533-626` | ✅ **Reuse as-is** | Import directly |
| **Fuzzy Company Matching** | `AeroComps.py:315-345` | ✅ **Reuse as-is** | Copy function |
| **Health Monitor** | `rate_limit_protection.py:633-841` | 🔧 Refactor | Use as-is for now |
| **API Usage Tracker** | `api_usage_tracker.py` | 🔧 Refactor | Use as-is for now |
| **Company Tier System** | `AeroComps.py:702-854` | 🔧 Refactor | Skip (not needed for enrichment) |
| **Job Filtering** | `AeroComps.py:537-568` | 🔧 Refactor | Skip (not needed) |
| **Analytics Module** | `analytics.py` | 🔧 Refactor | Skip for now |
| **SerpAPI Query Builder** | `AeroComps.py:918-962` | 🔄 Replace | New Apollo connector |
| **SerpAPI Response Parser** | `AeroComps.py:1098-1123` | 🔄 Replace | New Apollo parser |
| **Main Execution Loop** | `AeroComps.py:1186-1246` | 🔄 Replace | New pipeline script |

### 2.3 Detailed File Inventory

| File | Lines | Purpose | Disposition |
|------|-------|---------|-------------|
| `AeroComps.py` | 1,318 | SerpAPI job scanner | **Leave as-is** |
| `resources/rate_limit_protection.py` | 956 | API protection layer | **Import from** |
| `resources/api_usage_tracker.py` | 342 | Quota tracking | **Import from** |
| `resources/analytics.py` | 513 | Job analytics | Leave as-is |
| `resources/config.json` | 77 | Legacy config | Leave as-is |
| `diagnostics/setup_check.py` | 184 | Pre-flight checks | Leave as-is |
| `diagnostics/check_block_status.py` | 302 | IP block diagnosis | Leave as-is |
| `data/Aerospace_Alley_Companies.xlsx` | - | 137 CT aerospace companies | Leave as-is |
| `log/api_audit.jsonl` | - | API call audit trail | Leave as-is |

---

## 3. Target System Architecture

### 3.1 System Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    MARKET ANALYSIS PLATFORM                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────────┐                                                   │
│  │  INPUT LAYER     │                                                   │
│  │  ──────────────  │                                                   │
│  │  MapYourShow     │  Manual CSV export from:                          │
│  │  Exhibitor Data  │  spc26.mapyourshow.com/8_0/explore/exhibitor-gallery.cfm
│  │                  │                                                   │
│  │  Fields:         │                                                   │
│  │  - company_name  │                                                   │
│  │  - booth_number  │                                                   │
│  │  - website       │                                                   │
│  │  - address       │                                                   │
│  │  - description   │                                                   │
│  └────────┬─────────┘                                                   │
│           │                                                              │
│           ▼                                                              │
│  ┌──────────────────┐     ┌──────────────────┐                          │
│  │  ENRICHMENT      │     │  PROTECTION      │                          │
│  │  LAYER           │     │  LAYER           │                          │
│  │  ──────────────  │     │  ──────────────  │                          │
│  │  Apollo.io API   │◄────│  Rate Limiter    │  (from legacy)           │
│  │  - Contact lookup│     │  Circuit Breaker │  (from legacy)           │
│  │  - Email/phone   │     │  Exp. Backoff    │  (from legacy)           │
│  │  - Title/dept    │     │  Audit Logger    │  (from legacy)           │
│  └────────┬─────────┘     └──────────────────┘                          │
│           │                                                              │
│           ▼                                                              │
│  ┌──────────────────┐                                                   │
│  │  OUTPUT LAYER    │                                                   │
│  │  ──────────────  │                                                   │
│  │  Excel Export    │                                                   │
│  │                  │                                                   │
│  │  Sheets:         │                                                   │
│  │  - Contacts      │  (one row per contact)                            │
│  │  - Companies     │  (one row per company)                            │
│  │  - Metadata      │  (run info, provenance)                           │
│  │  - Failed        │  (companies that failed enrichment)               │
│  └──────────────────┘                                                   │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Data Model

```python
# Company (Input)
@dataclass
class Company:
    name: str                    # Required: "Lockheed Martin"
    booth_number: str = ""       # "A-101"
    address: str = ""            # "123 Main St"
    city: str = ""               # "Houston"
    state: str = ""              # "TX"
    zip_code: str = ""           # "77001"
    country: str = "USA"         # "USA"
    website: str = ""            # "https://lockheedmartin.com"
    description: str = ""        # "Aerospace and defense"
    category: str = ""           # "Prime Contractor"

# Contact (Output from enrichment)
@dataclass
class Contact:
    first_name: str = ""
    last_name: str = ""
    title: str = ""              # "VP Engineering"
    department: str = ""         # "Engineering"
    email: str = ""              # "john.smith@company.com"
    phone: str = ""              # "+1-555-123-4567"
    linkedin_url: str = ""       # "linkedin.com/in/johnsmith"
    seniority: str = ""          # "director", "manager", "vp"

    # Provenance (CRITICAL for trust)
    source: str = ""             # "apollo"
    source_record_id: str = ""   # "apollo-12345"
    enriched_at: datetime        # When we fetched this
    confidence_score: float      # 0.0-1.0
```

---

## 4. Data Flow Design

### 4.1 Input Format (CSV Template)

```csv
company_name,booth_number,address,city,state,zip,country,website,description,category
"Lockheed Martin","A-101","6801 Rockledge Dr","Bethesda","MD","20817","USA","https://lockheedmartin.com","Aerospace and defense company","Prime Contractor"
"Northrop Grumman","A-205","2980 Fairview Park Dr","Falls Church","VA","22042","USA","https://northropgrumman.com","Global aerospace and defense","Prime Contractor"
"SpaceX","B-310","1 Rocket Rd","Hawthorne","CA","90250","USA","https://spacex.com","Space transportation","Launch Provider"
```

**Required fields:** `company_name`
**Highly recommended:** `website` (needed for domain-based contact lookup)
**Optional:** All others (improve data quality but not required)

### 4.2 Output Format (Excel Sheets)

**Sheet 1: Contacts**
| Company Name | Booth | Website | Address | Contact Name | Title | Department | Email | Phone | LinkedIn | Source | Confidence | Enriched At |
|--------------|-------|---------|---------|--------------|-------|------------|-------|-------|----------|--------|------------|-------------|
| Lockheed Martin | A-101 | lockheedmartin.com | 6801 Rockledge Dr, Bethesda, MD | John Smith | VP Engineering | Engineering | john.smith@lm.com | +1-555-123-4567 | linkedin.com/in/... | apollo | 85% | 2026-01-06 12:00:00 |

**Sheet 2: Companies**
| Company Name | Booth | Website | Address | Enrichment Status | Contacts Found | Error |
|--------------|-------|---------|---------|-------------------|----------------|-------|
| Lockheed Martin | A-101 | lockheedmartin.com | ... | Success | 5 | |
| Unknown Corp | C-999 | | | Failed | 0 | No website provided |

**Sheet 3: Metadata**
| Field | Value |
|-------|-------|
| Generated At | 2026-01-06 12:00:00 |
| Input File | exhibitors.csv |
| Total Companies | 50 |
| Successful | 45 |
| Failed | 5 |
| Total Contacts | 127 |
| Enrichment Provider | apollo |

---

## 5. Implementation Code

### 5.1 Directory Structure to Create

```
market_intel/
├── __init__.py
├── enrich_exhibitors.py      # Main entry point
├── config.json               # Configuration
├── connectors/
│   ├── __init__.py
│   ├── base.py               # Base connector class
│   └── apollo.py             # Apollo.io connector
├── data/
│   └── exhibitors.csv        # Your input data
├── templates/
│   └── exhibitor_template.csv
└── output/                   # Generated files (gitignored)
```

### 5.2 File: `market_intel/__init__.py`

```python
# Market Intel Package
__version__ = "1.0.0"
```

### 5.3 File: `market_intel/connectors/__init__.py`

```python
from .base import BaseEnrichmentConnector, Company, Contact, EnrichmentResult
from .apollo import ApolloConnector, MockApolloConnector

__all__ = [
    'BaseEnrichmentConnector',
    'Company',
    'Contact',
    'EnrichmentResult',
    'ApolloConnector',
    'MockApolloConnector'
]
```

### 5.4 File: `market_intel/connectors/base.py`

```python
"""
Base Connector Interface for Contact Enrichment

Reuses rate limiting from legacy protection layer.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime
import sys
import os
import time

# Add parent directory to path for legacy imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from resources.rate_limit_protection import (
    TokenBucketRateLimiter,
    CircuitBreaker,
    ExponentialBackoff,
    ComprehensiveAuditLogger
)


@dataclass
class Company:
    """Input company data from exhibitor list."""
    name: str
    booth_number: str = ""
    address: str = ""
    city: str = ""
    state: str = ""
    zip_code: str = ""
    country: str = ""
    website: str = ""
    description: str = ""
    category: str = ""

    def get_domain(self) -> Optional[str]:
        """Extract domain from website URL."""
        if not self.website:
            return None
        domain = self.website.lower()
        domain = domain.replace("https://", "").replace("http://", "")
        domain = domain.replace("www.", "")
        domain = domain.split("/")[0]
        return domain


@dataclass
class Contact:
    """Enriched contact information."""
    first_name: str = ""
    last_name: str = ""
    title: str = ""
    department: str = ""
    email: str = ""
    phone: str = ""
    linkedin_url: str = ""
    seniority: str = ""

    # Provenance tracking
    source: str = ""
    source_record_id: str = ""
    enriched_at: datetime = field(default_factory=datetime.now)
    confidence_score: float = 0.0

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()


@dataclass
class EnrichmentResult:
    """Result of enriching a company with contacts."""
    company: Company
    contacts: List[Contact] = field(default_factory=list)
    success: bool = False
    error_message: str = ""
    api_calls_used: int = 0
    response_time_ms: float = 0.0


class BaseEnrichmentConnector(ABC):
    """
    Abstract base class for all enrichment connectors.

    Provides:
    - Rate limiting (Token Bucket) - FROM LEGACY
    - Circuit breaker for fault tolerance - FROM LEGACY
    - Exponential backoff for retries - FROM LEGACY
    - Audit logging for compliance - FROM LEGACY
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.api_key = config.get('api_key', '')

        # Rate limiting config
        rate_config = config.get('rate_limit', {})
        calls_per_minute = rate_config.get('calls_per_minute', 10)

        # Initialize protection layer (REUSED FROM LEGACY)
        self.rate_limiter = TokenBucketRateLimiter(
            capacity=calls_per_minute,
            refill_rate=calls_per_minute / 60.0
        )

        self.circuit_breaker = CircuitBreaker(
            failure_threshold=3,
            timeout=300,
            half_open_max_calls=2
        )

        self.backoff = ExponentialBackoff(
            base_delay=2.0,
            max_delay=30.0,
            max_attempts=3
        )

        # Audit logging
        log_file = config.get('log_file', 'log/enrichment_audit.jsonl')
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        self.audit_logger = ComprehensiveAuditLogger(log_file=log_file)

        print(f"[INIT] {self.source_name} connector initialized")
        print(f"       Rate limit: {calls_per_minute} calls/minute")

    @property
    @abstractmethod
    def source_name(self) -> str:
        """Unique identifier for this enrichment source."""
        pass

    @abstractmethod
    def _fetch_contacts(self, company: Company) -> List[Contact]:
        """
        Fetch contacts for a company from the enrichment source.
        Implement this in subclasses.
        """
        pass

    def enrich(self, company: Company) -> EnrichmentResult:
        """
        Enrich a company with contact information.
        Handles rate limiting, circuit breaker, retries, and logging.
        """
        result = EnrichmentResult(company=company)

        # Check circuit breaker
        if not self.circuit_breaker.is_available():
            result.error_message = "Circuit breaker open - too many failures"
            self.audit_logger.log_error(
                error_type="circuit_breaker_open",
                message=result.error_message,
                company=company.name
            )
            return result

        # Acquire rate limit token
        self.rate_limiter.acquire(1)

        start_time = time.time()

        try:
            # Fetch contacts with retry logic
            contacts = self.backoff.execute(self._fetch_contacts, company)

            result.contacts = contacts
            result.success = True
            result.api_calls_used = 1
            result.response_time_ms = (time.time() - start_time) * 1000

            # Record success
            self.circuit_breaker.record_success()

            # Audit log
            self.audit_logger.log_api_call(
                company=company.name,
                status_code=200,
                response_time_ms=result.response_time_ms,
                jobs_found=len(contacts),
                api_key_label=self.source_name
            )

            print(f"[OK] {company.name}: {len(contacts)} contacts found")

        except Exception as e:
            result.error_message = str(e)
            result.response_time_ms = (time.time() - start_time) * 1000

            self.circuit_breaker.record_failure()

            self.audit_logger.log_error(
                error_type="enrichment_failed",
                message=str(e),
                company=company.name
            )

            print(f"[FAIL] {company.name}: {e}")

        return result

    def enrich_batch(self, companies: List[Company]) -> List[EnrichmentResult]:
        """Enrich multiple companies."""
        results = []

        for i, company in enumerate(companies, 1):
            print(f"\n[{i}/{len(companies)}] {company.name}")
            result = self.enrich(company)
            results.append(result)

            if not self.circuit_breaker.is_available():
                print("\n[STOP] Circuit breaker opened - stopping batch")
                break

        return results
```

### 5.5 File: `market_intel/connectors/apollo.py`

```python
"""
Apollo.io Connector for Contact Enrichment

API Docs: https://apolloio.github.io/apollo-api-docs/
Free tier: 50 credits/month
"""

import requests
from typing import List, Dict, Any
from .base import BaseEnrichmentConnector, Company, Contact
import random


class ApolloConnector(BaseEnrichmentConnector):
    """Apollo.io enrichment connector."""

    BASE_URL = "https://api.apollo.io/v1"

    @property
    def source_name(self) -> str:
        return "apollo"

    def _fetch_contacts(self, company: Company) -> List[Contact]:
        """Fetch contacts from Apollo.io for a company."""
        domain = company.get_domain()

        if domain:
            return self._search_by_domain(domain, company.name)
        else:
            return self._search_by_name(company.name)

    def _search_by_domain(self, domain: str, company_name: str) -> List[Contact]:
        """Search for contacts at a company by domain."""
        headers = {"Content-Type": "application/json", "Cache-Control": "no-cache"}

        payload = {
            "api_key": self.api_key,
            "q_organization_domains": domain,
            "page": 1,
            "per_page": 25,
            "person_seniorities": ["owner", "founder", "c_suite", "partner", "vp", "director", "manager"]
        }

        response = requests.post(
            f"{self.BASE_URL}/mixed_people/search",
            headers=headers,
            json=payload,
            timeout=30
        )

        if response.status_code != 200:
            raise Exception(f"Apollo API error: {response.status_code} - {response.text[:200]}")

        data = response.json()
        people = data.get("people", [])

        return self._parse_contacts(people)

    def _search_by_name(self, company_name: str) -> List[Contact]:
        """Search for contacts by company name (fallback)."""
        headers = {"Content-Type": "application/json", "Cache-Control": "no-cache"}

        payload = {
            "api_key": self.api_key,
            "q_organization_name": company_name,
            "page": 1,
            "per_page": 25,
            "person_seniorities": ["owner", "founder", "c_suite", "partner", "vp", "director", "manager"]
        }

        response = requests.post(
            f"{self.BASE_URL}/mixed_people/search",
            headers=headers,
            json=payload,
            timeout=30
        )

        if response.status_code != 200:
            raise Exception(f"Apollo API error: {response.status_code} - {response.text[:200]}")

        data = response.json()
        people = data.get("people", [])

        return self._parse_contacts(people)

    def _parse_contacts(self, people: List[Dict]) -> List[Contact]:
        """Parse Apollo API response into Contact objects."""
        contacts = []

        for person in people:
            phone = ""
            phone_numbers = person.get("phone_numbers", [])
            if phone_numbers:
                for p in phone_numbers:
                    if p.get("type") == "direct":
                        phone = p.get("sanitized_number", "")
                        break
                if not phone:
                    phone = phone_numbers[0].get("sanitized_number", "")

            contact = Contact(
                first_name=person.get("first_name", ""),
                last_name=person.get("last_name", ""),
                title=person.get("title", ""),
                department=self._infer_department(person.get("title", "")),
                email=person.get("email", ""),
                phone=phone,
                linkedin_url=person.get("linkedin_url", ""),
                seniority=person.get("seniority", ""),
                source="apollo",
                source_record_id=person.get("id", ""),
                confidence_score=self._calculate_confidence(person)
            )
            contacts.append(contact)

        return contacts

    def _infer_department(self, title: str) -> str:
        """Infer department from job title."""
        title_lower = title.lower()
        departments = {
            "Engineering": ["engineer", "technical", "developer", "architect", "r&d"],
            "Sales": ["sales", "account", "business development", "revenue"],
            "Marketing": ["marketing", "brand", "communications"],
            "Operations": ["operations", "supply chain", "logistics", "manufacturing"],
            "Finance": ["finance", "accounting", "cfo", "controller"],
            "Executive": ["ceo", "president", "founder", "owner", "chief"]
        }
        for dept, keywords in departments.items():
            for kw in keywords:
                if kw in title_lower:
                    return dept
        return ""

    def _calculate_confidence(self, person: Dict) -> float:
        """Calculate confidence score based on data completeness."""
        score = 0.0
        if person.get("email"): score += 0.3
        if person.get("email_status") == "verified": score += 0.2
        if person.get("phone_numbers"): score += 0.2
        if person.get("linkedin_url"): score += 0.15
        if person.get("title"): score += 0.15
        return min(score, 1.0)


class MockApolloConnector(BaseEnrichmentConnector):
    """Mock connector for testing without API calls."""

    @property
    def source_name(self) -> str:
        return "mock_apollo"

    def _fetch_contacts(self, company: Company) -> List[Contact]:
        """Return mock contacts for testing."""
        num_contacts = random.randint(1, 3)
        contacts = []

        first_names = ["John", "Sarah", "Michael", "Emily", "David"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones"]
        titles = ["CEO", "VP Engineering", "Director of Sales", "Operations Manager", "CTO"]
        departments = ["Executive", "Engineering", "Sales", "Operations", "Technology"]

        domain = company.get_domain() or "example.com"

        for i in range(num_contacts):
            first = random.choice(first_names)
            last = random.choice(last_names)
            contact = Contact(
                first_name=first,
                last_name=last,
                title=random.choice(titles),
                department=random.choice(departments),
                email=f"{first.lower()}.{last.lower()}@{domain}",
                phone=f"+1-555-{random.randint(100,999)}-{random.randint(1000,9999)}",
                linkedin_url=f"https://linkedin.com/in/{first.lower()}{last.lower()}",
                seniority="director",
                source="mock_apollo",
                source_record_id=f"MOCK-{i+1}",
                confidence_score=random.uniform(0.6, 0.95)
            )
            contacts.append(contact)

        return contacts
```

### 5.6 File: `market_intel/enrich_exhibitors.py`

```python
#!/usr/bin/env python3
"""
Exhibitor Contact Enrichment Pipeline

Usage:
    python market_intel/enrich_exhibitors.py --mock              # Test mode
    python market_intel/enrich_exhibitors.py                     # Production
    python market_intel/enrich_exhibitors.py --input data/my.csv # Custom input
"""

import os
import sys
import json
import argparse
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from market_intel.connectors.base import Company, EnrichmentResult
from market_intel.connectors.apollo import ApolloConnector, MockApolloConnector


def load_config(config_path: str = "market_intel/config.json") -> Dict[str, Any]:
    """Load configuration from JSON file."""
    if not os.path.exists(config_path):
        return {
            "input_file": "market_intel/data/exhibitors.csv",
            "output_file": "market_intel/output/enriched_contacts.xlsx",
            "enrichment": {
                "provider": "apollo",
                "api_key": "YOUR_API_KEY_HERE",
                "rate_limit": {"calls_per_minute": 10}
            }
        }
    with open(config_path, 'r') as f:
        return json.load(f)


def load_exhibitors(input_file: str) -> List[Company]:
    """Load exhibitor data from CSV file."""
    if not os.path.exists(input_file):
        print(f"[ERROR] Input file not found: {input_file}")
        sys.exit(1)

    df = pd.read_csv(input_file)
    companies = []

    for _, row in df.iterrows():
        company = Company(
            name=str(row.get('company_name', '')).strip(),
            booth_number=str(row.get('booth_number', '')).strip(),
            address=str(row.get('address', '')).strip(),
            city=str(row.get('city', '')).strip(),
            state=str(row.get('state', '')).strip(),
            zip_code=str(row.get('zip', '')).strip(),
            country=str(row.get('country', 'USA')).strip(),
            website=str(row.get('website', '')).strip(),
            description=str(row.get('description', '')).strip(),
            category=str(row.get('category', '')).strip()
        )
        if company.name and company.name.lower() != 'nan':
            companies.append(company)

    print(f"[LOAD] {len(companies)} companies from {input_file}")
    return companies


def export_to_excel(results: List[EnrichmentResult], output_file: str, config: Dict):
    """Export enrichment results to Excel."""
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    contact_rows = []
    company_rows = []

    for result in results:
        company = result.company
        company_rows.append({
            "Company Name": company.name,
            "Booth Number": company.booth_number,
            "Website": company.website,
            "Address": f"{company.address}, {company.city}, {company.state} {company.zip_code}".strip(", "),
            "Status": "Success" if result.success else "Failed",
            "Contacts Found": len(result.contacts),
            "Error": result.error_message
        })

        for contact in result.contacts:
            contact_rows.append({
                "Company Name": company.name,
                "Booth Number": company.booth_number,
                "Company Website": company.website,
                "Contact Name": contact.full_name,
                "Title": contact.title,
                "Department": contact.department,
                "Email": contact.email,
                "Phone": contact.phone,
                "LinkedIn": contact.linkedin_url,
                "Source": contact.source,
                "Source Record ID": contact.source_record_id,
                "Enriched At": contact.enriched_at.strftime("%Y-%m-%d %H:%M:%S"),
                "Confidence": f"{contact.confidence_score:.0%}"
            })

    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        if contact_rows:
            pd.DataFrame(contact_rows).to_excel(writer, sheet_name="Contacts", index=False)
        pd.DataFrame(company_rows).to_excel(writer, sheet_name="Companies", index=False)

        metadata = pd.DataFrame({
            "Field": ["Generated At", "Total Companies", "Successful", "Failed", "Total Contacts", "Provider"],
            "Value": [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                len(results),
                sum(1 for r in results if r.success),
                sum(1 for r in results if not r.success),
                sum(len(r.contacts) for r in results),
                config.get('enrichment', {}).get('provider', 'unknown')
            ]
        })
        metadata.to_excel(writer, sheet_name="Metadata", index=False)

    print(f"[SAVE] {output_file}")


def main():
    parser = argparse.ArgumentParser(description='Exhibitor Contact Enrichment')
    parser.add_argument('--input', type=str, help='Input CSV file')
    parser.add_argument('--output', type=str, help='Output Excel file')
    parser.add_argument('--mock', action='store_true', help='Use mock data (no API)')
    parser.add_argument('--config', type=str, default='market_intel/config.json')
    args = parser.parse_args()

    print("\n" + "=" * 60)
    print("EXHIBITOR CONTACT ENRICHMENT")
    print("=" * 60)

    config = load_config(args.config)
    input_file = args.input or config.get('input_file')
    output_file = args.output or config.get('output_file')

    companies = load_exhibitors(input_file)
    if not companies:
        print("[ERROR] No companies to process")
        sys.exit(1)

    enrichment_config = config.get('enrichment', {})
    enrichment_config['log_file'] = 'log/enrichment_audit.jsonl'

    if args.mock:
        print("[MODE] Mock (no API calls)")
        connector = MockApolloConnector(enrichment_config)
    else:
        api_key = enrichment_config.get('api_key', '')
        if not api_key or api_key == 'YOUR_API_KEY_HERE':
            print("[ERROR] No API key configured. Use --mock for testing.")
            sys.exit(1)
        print("[MODE] Production (Apollo.io)")
        connector = ApolloConnector(enrichment_config)

    print("\n" + "-" * 60)
    results = connector.enrich_batch(companies)
    print("-" * 60)

    # Summary
    successful = sum(1 for r in results if r.success)
    total_contacts = sum(len(r.contacts) for r in results)
    print(f"\n[SUMMARY] {successful}/{len(results)} companies enriched, {total_contacts} contacts found")

    export_to_excel(results, output_file, config)
    print("\n[DONE]")


if __name__ == "__main__":
    main()
```

---

## 6. Configuration Files

### 6.1 File: `market_intel/config.json`

```json
{
  "input_file": "market_intel/data/exhibitors.csv",
  "output_file": "market_intel/output/enriched_contacts.xlsx",

  "enrichment": {
    "provider": "apollo",
    "api_key": "YOUR_APOLLO_API_KEY_HERE",
    "rate_limit": {
      "calls_per_minute": 10,
      "min_interval_seconds": 6
    }
  },

  "target_titles": [
    "CEO", "President", "Owner", "Founder",
    "VP", "Vice President",
    "Director",
    "Manager",
    "Head of",
    "Chief"
  ],

  "target_departments": [
    "Engineering",
    "Sales",
    "Business Development",
    "Operations",
    "Procurement"
  ]
}
```

### 6.2 File: `market_intel/templates/exhibitor_template.csv`

```csv
company_name,booth_number,address,city,state,zip,country,website,description,category
"Example Company","A-101","123 Main St","Houston","TX","77001","USA","https://example.com","Description here","Category"
```

---

## 7. Directory Structure

### 7.1 Create These Directories

```bash
mkdir -p market_intel/connectors
mkdir -p market_intel/data
mkdir -p market_intel/templates
mkdir -p market_intel/output
```

### 7.2 Create These Files

| File | Content From |
|------|--------------|
| `market_intel/__init__.py` | Section 5.2 |
| `market_intel/connectors/__init__.py` | Section 5.3 |
| `market_intel/connectors/base.py` | Section 5.4 |
| `market_intel/connectors/apollo.py` | Section 5.5 |
| `market_intel/enrich_exhibitors.py` | Section 5.6 |
| `market_intel/config.json` | Section 6.1 |
| `market_intel/templates/exhibitor_template.csv` | Section 6.2 |

---

## 8. Step-by-Step Migration

### Day 1: Setup and Test

```bash
# 1. Create directory structure
mkdir -p market_intel/connectors
mkdir -p market_intel/data
mkdir -p market_intel/templates
mkdir -p market_intel/output

# 2. Create all files from Section 5 and 6 above

# 3. Copy template to data directory
cp market_intel/templates/exhibitor_template.csv market_intel/data/exhibitors.csv

# 4. Test with mock data (no API needed)
python market_intel/enrich_exhibitors.py --mock

# 5. Verify output
ls -la market_intel/output/
```

### Day 2: Data Collection and API Setup

```bash
# 1. Go to MapYourShow: https://spc26.mapyourshow.com/8_0/explore/exhibitor-gallery.cfm
# 2. Manually copy exhibitor data to market_intel/data/exhibitors.csv
# 3. Get Apollo.io API key: https://app.apollo.io/#/settings/integrations/api
# 4. Add API key to market_intel/config.json
# 5. Test with real API
python market_intel/enrich_exhibitors.py --input market_intel/data/exhibitors.csv
```

### Day 3: Production Run and Validation

```bash
# 1. Full production run
python market_intel/enrich_exhibitors.py

# 2. Check output
# - Open market_intel/output/enriched_contacts.xlsx
# - Verify Contacts sheet has data
# - Check Metadata sheet for summary
# - Review Failed sheet for issues

# 3. Check audit log
cat log/enrichment_audit.jsonl | head -20
```

---

## 9. Testing Procedures

### 9.1 Mock Test (No API)

```bash
python market_intel/enrich_exhibitors.py --mock --input market_intel/data/exhibitors.csv
```

**Expected output:**
```
============================================================
EXHIBITOR CONTACT ENRICHMENT
============================================================
[LOAD] 3 companies from market_intel/data/exhibitors.csv
[MODE] Mock (no API calls)
[INIT] mock_apollo connector initialized

[1/3] Example Company
[OK] Example Company: 2 contacts found

[2/3] Another Corp
[OK] Another Corp: 1 contacts found

[SUMMARY] 3/3 companies enriched, 5 contacts found
[SAVE] market_intel/output/enriched_contacts.xlsx
[DONE]
```

### 9.2 Verify Output Structure

```python
import pandas as pd

# Check Contacts sheet
df = pd.read_excel('market_intel/output/enriched_contacts.xlsx', sheet_name='Contacts')
print(df.columns.tolist())
# Should show: ['Company Name', 'Booth Number', 'Company Website', 'Contact Name',
#               'Title', 'Department', 'Email', 'Phone', 'LinkedIn', 'Source',
#               'Source Record ID', 'Enriched At', 'Confidence']

# Check Companies sheet
df = pd.read_excel('market_intel/output/enriched_contacts.xlsx', sheet_name='Companies')
print(df.columns.tolist())
# Should show: ['Company Name', 'Booth Number', 'Website', 'Address',
#               'Status', 'Contacts Found', 'Error']
```

---

## 10. Troubleshooting

### 10.1 Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `ModuleNotFoundError: pandas` | Missing dependency | `pip install pandas openpyxl requests` |
| `No API key configured` | Missing API key | Add key to `config.json` or use `--mock` |
| `Apollo API error: 401` | Invalid API key | Check API key is correct |
| `Apollo API error: 429` | Rate limit exceeded | Reduce `calls_per_minute` in config |
| `Circuit breaker open` | Too many failures | Wait 5 minutes, check API key |
| `No companies to process` | Empty/missing CSV | Check input file path and format |

### 10.2 Check Audit Logs

```bash
# View recent API calls
tail -20 log/enrichment_audit.jsonl

# Count successes vs failures
grep '"status_code": 200' log/enrichment_audit.jsonl | wc -l
grep '"error_type"' log/enrichment_audit.jsonl | wc -l
```

### 10.3 Validate CSV Format

```python
import pandas as pd

df = pd.read_csv('market_intel/data/exhibitors.csv')
print("Columns:", df.columns.tolist())
print("Rows:", len(df))
print("\nFirst row:")
print(df.iloc[0])
```

**Required column:** `company_name`
**Recommended column:** `website` (for domain-based lookup)

---

## 11. Trust, Governance, and Accuracy Guardrails

### 11.1 Provenance Tracking (Built Into System)

Every contact record includes:

| Field | Purpose | Example |
|-------|---------|---------|
| `source` | Which API provided the data | "apollo" |
| `source_record_id` | Original record ID in source system | "apollo-abc123" |
| `enriched_at` | Timestamp when data was fetched | "2026-01-06 12:00:00" |
| `confidence_score` | Data completeness score (0-100%) | "85%" |

### 11.2 Data Quality Signals

The confidence score is calculated based on:

```python
score = 0.0
if email: score += 0.3           # Has email
if email_verified: score += 0.2  # Email is verified
if phone: score += 0.2           # Has phone number
if linkedin: score += 0.15       # Has LinkedIn URL
if title: score += 0.15          # Has job title
# Max score: 1.0 (100%)
```

### 11.3 Audit Trail

All API calls are logged to `log/enrichment_audit.jsonl`:

```json
{
  "timestamp": "2026-01-06T12:00:00Z",
  "event_type": "api_call",
  "company": "Lockheed Martin",
  "status_code": 200,
  "response_time_ms": 450.5,
  "contacts_found": 5,
  "api_key_label": "apollo"
}
```

### 11.4 What's NOT Covered (Future Scope)

| Requirement | Status | Notes |
|-------------|--------|-------|
| Export audit logs (who exported what) | ❌ Future | Add when CRM integration built |
| Multi-source survivorship rules | ❌ Future | Only one source (Apollo) currently |
| Data retention policies | ❌ Future | Define when compliance requires |
| GDPR/privacy compliance | ⚠️ Manual | User responsible for data handling |

---

## 12. Concrete Next Actions

### Immediate (Day 1)

1. **Create directory structure** (5 min)
   ```bash
   mkdir -p market_intel/connectors market_intel/data market_intel/templates market_intel/output
   ```

2. **Copy code from Section 5** into files (30 min)

3. **Test with mock data** (5 min)
   ```bash
   python market_intel/enrich_exhibitors.py --mock
   ```

### Day 2

4. **Collect exhibitor data from MapYourShow** (manual)
   - URL: https://spc26.mapyourshow.com/8_0/explore/exhibitor-gallery.cfm
   - Save to: `market_intel/data/exhibitors.csv`

5. **Get Apollo.io API key**
   - URL: https://app.apollo.io/#/settings/integrations/api
   - Free tier: 50 credits/month

6. **Update config with API key**
   - Edit: `market_intel/config.json`

### Day 3

7. **Run production enrichment**
   ```bash
   python market_intel/enrich_exhibitors.py
   ```

8. **Validate output**
   - Check `market_intel/output/enriched_contacts.xlsx`
   - Review Contacts, Companies, Metadata sheets

9. **Review audit log**
   ```bash
   cat log/enrichment_audit.jsonl
   ```

### What Can Be Postponed

| Item | Reason |
|------|--------|
| ZoomInfo integration | Paid, enterprise only |
| CRM export | Not needed for POC |
| Multi-source enrichment | One source sufficient for POC |
| Historical trend analysis | Future scope |

---

## Appendix A: Apollo.io API Reference

### Authentication

Apollo uses API key in request body, not headers:

```python
payload = {
    "api_key": "YOUR_KEY_HERE",
    ...
}
```

### People Search Endpoint

```
POST https://api.apollo.io/v1/mixed_people/search
```

**Request body:**
```json
{
  "api_key": "...",
  "q_organization_domains": "spacex.com",
  "page": 1,
  "per_page": 25,
  "person_seniorities": ["owner", "founder", "c_suite", "vp", "director", "manager"]
}
```

**Response:**
```json
{
  "people": [
    {
      "id": "abc123",
      "first_name": "Elon",
      "last_name": "Musk",
      "title": "CEO",
      "email": "elon@spacex.com",
      "email_status": "verified",
      "linkedin_url": "linkedin.com/in/elonmusk",
      "seniority": "c_suite",
      "phone_numbers": [{"type": "direct", "sanitized_number": "+1-555-123-4567"}]
    }
  ]
}
```

### Rate Limits

- Free tier: 50 credits/month
- Each search = 1 credit
- Recommended: 10 calls/minute max

---

## Appendix B: Alternative Enrichment Providers

If Apollo.io doesn't work, these are alternatives:

| Provider | Free Tier | Endpoint | Notes |
|----------|-----------|----------|-------|
| Hunter.io | 50/month | `/domain-search` | Email-focused |
| Clearbit | 50/month | `/companies/find` | Needs domain |
| ZoomInfo | None | Enterprise | Most comprehensive |
| LinkedIn Sales Navigator | None | Enterprise | Requires subscription |

To add a new provider:

1. Create `market_intel/connectors/newprovider.py`
2. Inherit from `BaseEnrichmentConnector`
3. Implement `source_name` property and `_fetch_contacts` method
4. Import in `market_intel/connectors/__init__.py`

---

## Appendix C: MapYourShow API Reference (Future Use)

If MapYourShow API credentials become available:

### Official REST API

- **Documentation:** https://api.mapyourshow.com/mysRest/v2/
- **Authentication:** Bearer token (60-minute validity)

### Key Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/Exhibitors` | GET | Get exhibitor details by ID or booth |
| `/Exhibitors/Modified` | GET | Get recently updated exhibitors |
| `/Exhibitors/Detail` | GET | Full exhibitor data including contacts |

### Authentication Flow

```python
# 1. Get auth token
response = requests.post(
    "https://api.mapyourshow.com/mysRest/v2/auth",
    json={"api_key": "YOUR_KEY", "api_secret": "YOUR_SECRET"}
)
token = response.json()["token"]  # Valid 60 minutes

# 2. Use token in subsequent calls
headers = {"Authorization": f"Bearer {token}"}
response = requests.get(
    "https://api.mapyourshow.com/mysRest/v2/Exhibitors",
    headers=headers
)
```

### Alternative: Apify Scraper

If API access not available:
- **URL:** https://apify.com/skython/map-your-show-exhibitor-list-scraper
- **Cost:** ~$5-50 depending on volume
- **Output:** JSON with exhibitor data

### Event-Specific URL

SpaceCom | Space Mobility 2026:
- **Gallery:** https://spc26.mapyourshow.com/8_0/explore/exhibitor-gallery.cfm
- **Floor Plan:** https://spc26.mapyourshow.com/8_0/floorplan/index.cfm

---

## Appendix D: Legacy System Reference

### Files NOT to Modify

| File | Purpose | Leave As-Is |
|------|---------|-------------|
| `AeroComps.py` | SerpAPI job scanner | YES |
| `resources/rate_limit_protection.py` | Protection layer | YES (import from) |
| `resources/api_usage_tracker.py` | API quota tracker | YES |
| `resources/analytics.py` | Job analytics | YES |
| `resources/config.json` | Legacy config | YES |
| `data/Aerospace_Alley_Companies.xlsx` | Company list | YES |

### Functions Imported from Legacy

```python
# These are imported from resources/rate_limit_protection.py
from resources.rate_limit_protection import (
    TokenBucketRateLimiter,    # Line 139-220
    CircuitBreaker,            # Line 227-325
    ExponentialBackoff,        # Line 332-409
    ComprehensiveAuditLogger   # Line 533-626
)
```

---

**END OF MIGRATION PLAN**

*This document is the single source of truth. Copy code sections directly into files.*
