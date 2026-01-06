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
