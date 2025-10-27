# Comprehensive Rate Limit Protection System
## Industry Standards & Best Practices Specification

**Version:** 1.0
**Date:** October 27, 2025
**Purpose:** Bulletproof protection against API rate limiting and IP blocking

---

## 📋 Table of Contents

1. [Legal & Compliance Framework](#legal--compliance-framework)
2. [Industry Standards Applied](#industry-standards-applied)
3. [SerpAPI Specific Requirements](#serpapi-specific-requirements)
4. [Protection Layers](#protection-layers)
5. [Implementation Specification](#implementation-specification)
6. [Monitoring & Logging](#monitoring--logging)
7. [Testing & Validation](#testing--validation)

---

## 🏛️ Legal & Compliance Framework

### SerpAPI Terms of Service Compliance

**Based on standard API provider ToS:**

1. **Rate Limiting Compliance**
   - Respect all rate limits (explicit and implicit)
   - Stop immediately upon receiving 429 (Too Many Requests)
   - Stop immediately upon receiving 403 (Forbidden/IP Block)
   - Implement exponential backoff for retries

2. **Acceptable Use Policy**
   - Automated access allowed (we're using official API)
   - Must not overwhelm infrastructure
   - Must identify ourselves (User-Agent header)
   - Must respect all HTTP status codes

3. **Data Usage**
   - Data for legitimate business intelligence only
   - No resale of data
   - Comply with job board source Terms of Service
   - Attribution where required

### General Legal Compliance

1. **CFAA Compliance (Computer Fraud and Abuse Act)**
   - We have authorized access (using API keys)
   - Not circumventing security measures
   - Not accessing more than permitted

2. **DMCA Compliance (if applicable)**
   - Not scraping copyrighted content without permission
   - Using API = authorized access method

3. **GDPR/Privacy (if applicable)**
   - Job postings are publicly available data
   - No personal information collected
   - Data used for business intelligence

---

## 🏭 Industry Standards Applied

### 1. Token Bucket Algorithm (RFC 6585)
**Standard for:** Rate limiting in distributed systems

**How it works:**
- Bucket has maximum capacity (tokens)
- Tokens added at fixed rate
- Each API call consumes 1 token
- If no tokens available → wait until refilled

**Benefits:**
- Allows bursts within limits
- Smooth long-term average
- Industry-proven algorithm

**Implementation:**
```python
class TokenBucket:
    """
    Industry-standard token bucket rate limiter
    Reference: https://en.wikipedia.org/wiki/Token_bucket
    """
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity  # Max tokens
        self.tokens = capacity  # Current tokens
        self.refill_rate = refill_rate  # Tokens per second
        self.last_refill = time.time()
```

### 2. Exponential Backoff (RFC 7231)
**Standard for:** HTTP retry logic

**Formula:** `wait_time = base_delay * (2 ^ attempt_number)`

**Example:**
- 1st retry: 2 seconds
- 2nd retry: 4 seconds
- 3rd retry: 8 seconds
- 4th retry: 16 seconds (with jitter)

**Benefits:**
- Reduces server load
- Increases success probability
- Prevents thundering herd problem

### 3. Circuit Breaker Pattern (Netflix Hystrix)
**Standard for:** Fault tolerance in microservices

**States:**
- **CLOSED:** Normal operation
- **OPEN:** Stop all calls (triggered after threshold failures)
- **HALF-OPEN:** Test if service recovered

**Benefits:**
- Prevents cascading failures
- Fast failure response
- Automatic recovery testing

### 4. Graceful Degradation
**Standard for:** System resilience

**Principle:** System continues to operate with reduced functionality when errors occur

**Our Implementation:**
- Primary API fails → Switch to secondary API key
- All SerpAPI keys fail → Suggest Adzuna fallback
- Save all progress before failure

### 5. Observability (Three Pillars)
**Standards:** OpenTelemetry, Prometheus metrics

**Three Pillars:**
1. **Logging:** Structured logs (JSON format)
2. **Metrics:** Success rate, latency, error rate
3. **Tracing:** Request flow tracking

---

## 🎯 SerpAPI Specific Requirements

### Known Rate Limits (from SerpAPI documentation)

**Free Tier:**
- 100 searches/month
- Unclear requests per second (inferred: ~1 per second safe)

**Trial Accounts (what you have):**
- 250 searches per key
- IP-based rate limiting (triggered at ~20 req/min sustained)
- 403 errors indicate IP block (24-48 hour duration)
- 429 errors indicate soft rate limit (retry after delay)

**Paid Accounts:**
- Higher limits (vary by plan)
- More lenient rate limiting
- Priority support

### SerpAPI Error Codes

**200 OK** - Success
```json
{
  "search_metadata": {...},
  "jobs_results": [...]
}
```

**401 Unauthorized** - Invalid API key
```json
{
  "error": "Invalid API key"
}
```

**402 Payment Required** - Credits exhausted
```json
{
  "error": "You have reached your search limit"
}
```

**403 Forbidden** - IP blocked or ToS violation
```json
{
  "error": "Access denied"
}
```

**429 Too Many Requests** - Rate limit exceeded
```json
{
  "error": "Too many requests"
}
```

**500 Server Error** - SerpAPI internal issue
```json
{
  "error": "Internal server error"
}
```

### SerpAPI Best Practices (Inferred)

1. **Rate Limiting:**
   - Keep under 60 requests/hour for trial accounts
   - Add 2-3 second delay between requests minimum
   - Batch process with pauses (don't process continuously)

2. **Error Handling:**
   - Stop immediately on 403 (don't retry, it won't help)
   - Implement exponential backoff for 429
   - Retry 500 errors with backoff
   - Switch API keys on 401/402

3. **Request Headers:**
   - Include User-Agent (identify your application)
   - Accept gzip compression
   - Keep connections alive (HTTP keep-alive)

4. **Monitoring:**
   - Track credits remaining
   - Monitor success rate
   - Log all errors with context

---

## 🛡️ Protection Layers (Comprehensive System)

### Layer 1: Configuration Validation
**Purpose:** Prevent misconfiguration before any API calls

```python
def validate_configuration(config):
    """Validate config meets safety requirements"""
    errors = []

    # Minimum delay check
    min_delay = config['settings']['min_interval_seconds']
    if min_delay < 2.0:
        errors.append(f"min_interval_seconds too low: {min_delay}s (minimum: 2.0s)")

    # Max threads check
    max_threads = config['settings']['max_threads']
    if max_threads > 3:
        errors.append(f"max_threads too high: {max_threads} (maximum: 3 for trial accounts)")

    # API key validation
    if not config.get('api_keys') or len(config['api_keys']) == 0:
        errors.append("No API keys configured")

    if errors:
        print("❌ CONFIGURATION VALIDATION FAILED:")
        for error in errors:
            print(f"   - {error}")
        raise ValueError("Invalid configuration - refusing to start")

    print("✅ Configuration validation passed")
```

### Layer 2: Token Bucket Rate Limiter
**Purpose:** Smooth rate limiting with burst allowance

```python
class TokenBucketRateLimiter:
    """
    Industry-standard token bucket algorithm
    Reference: RFC 6585, Leaky Bucket Algorithm
    """
    def __init__(self, capacity=60, refill_rate=1.0):
        """
        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens added per second
        """
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate
        self.last_refill = time.time()
        self.lock = Lock()

    def _refill(self):
        """Add tokens based on time elapsed"""
        now = time.time()
        elapsed = now - self.last_refill
        tokens_to_add = elapsed * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refill = now

    def acquire(self, tokens=1):
        """
        Acquire tokens (blocking if not available)
        Returns: Time waited
        """
        with self.lock:
            start = time.time()

            while True:
                self._refill()

                if self.tokens >= tokens:
                    self.tokens -= tokens
                    return time.time() - start

                # Calculate wait time
                deficit = tokens - self.tokens
                wait_time = deficit / self.refill_rate

                time.sleep(min(wait_time, 1.0))  # Sleep in 1s increments
```

### Layer 3: Circuit Breaker
**Purpose:** Fast failure and automatic recovery

```python
class CircuitBreaker:
    """
    Circuit Breaker pattern (Netflix Hystrix)
    States: CLOSED (normal) → OPEN (failing) → HALF_OPEN (testing)
    """
    def __init__(self, failure_threshold=3, timeout=300, half_open_max_calls=3):
        """
        Args:
            failure_threshold: Failures before opening circuit
            timeout: Seconds before attempting recovery (HALF_OPEN)
            half_open_max_calls: Test calls in HALF_OPEN state
        """
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.half_open_max_calls = half_open_max_calls

        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'CLOSED'  # CLOSED, OPEN, HALF_OPEN
        self.half_open_calls = 0

    def call(self, func, *args, **kwargs):
        """Execute function with circuit breaker protection"""

        if self.state == 'OPEN':
            # Check if timeout expired
            if time.time() - self.last_failure_time > self.timeout:
                print("🔄 Circuit breaker: OPEN → HALF_OPEN (testing recovery)")
                self.state = 'HALF_OPEN'
                self.half_open_calls = 0
            else:
                raise Exception("Circuit breaker OPEN - service unavailable")

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result

        except Exception as e:
            self._on_failure()
            raise e

    def _on_success(self):
        """Handle successful call"""
        if self.state == 'HALF_OPEN':
            self.half_open_calls += 1
            if self.half_open_calls >= self.half_open_max_calls:
                print("✅ Circuit breaker: HALF_OPEN → CLOSED (service recovered)")
                self.state = 'CLOSED'
                self.failure_count = 0
        else:
            self.failure_count = 0

    def _on_failure(self):
        """Handle failed call"""
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.state == 'HALF_OPEN':
            print("❌ Circuit breaker: HALF_OPEN → OPEN (recovery failed)")
            self.state = 'OPEN'
        elif self.failure_count >= self.failure_threshold:
            print(f"❌ Circuit breaker: CLOSED → OPEN (threshold: {self.failure_threshold})")
            self.state = 'OPEN'
```

### Layer 4: Exponential Backoff Retry
**Purpose:** Smart retry logic with increasing delays

```python
class ExponentialBackoff:
    """
    Exponential backoff retry logic (RFC 7231)
    With jitter to prevent thundering herd
    """
    def __init__(self, base_delay=1.0, max_delay=60.0, max_attempts=5):
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.max_attempts = max_attempts

    def execute(self, func, *args, **kwargs):
        """Execute function with exponential backoff retry"""

        for attempt in range(self.max_attempts):
            try:
                return func(*args, **kwargs)

            except Exception as e:
                if attempt == self.max_attempts - 1:
                    raise e  # Last attempt, give up

                # Calculate delay with exponential backoff
                delay = min(self.base_delay * (2 ** attempt), self.max_delay)

                # Add jitter (randomness) to prevent thundering herd
                jitter = random.uniform(0, delay * 0.1)
                total_delay = delay + jitter

                print(f"⚠️  Attempt {attempt + 1} failed, retrying in {total_delay:.1f}s...")
                time.sleep(total_delay)

        raise Exception("All retry attempts exhausted")
```

### Layer 5: Batch Processor with Intelligent Pausing
**Purpose:** Process in batches with automatic pauses

```python
class BatchProcessor:
    """
    Batch processing with intelligent pause calculation
    Mimics human usage patterns
    """
    def __init__(self, batch_size=10, min_pause=60, max_pause=300):
        """
        Args:
            batch_size: Items per batch
            min_pause: Minimum pause between batches (seconds)
            max_pause: Maximum pause between batches (seconds)
        """
        self.batch_size = batch_size
        self.min_pause = min_pause
        self.max_pause = max_pause
        self.batches_processed = 0

    def calculate_pause_duration(self):
        """Calculate intelligent pause duration"""
        # Longer pauses as we process more batches (fatigue simulation)
        base_pause = self.min_pause
        fatigue_multiplier = 1 + (self.batches_processed * 0.1)
        calculated_pause = min(base_pause * fatigue_multiplier, self.max_pause)

        # Add randomness (15-30% variation)
        jitter = random.uniform(0.15, 0.30) * calculated_pause

        return calculated_pause + jitter

    def process_batch(self, items, process_func):
        """Process a batch of items"""
        results = []

        for item in items:
            result = process_func(item)
            results.append(result)

        self.batches_processed += 1
        return results

    def process_all(self, items, process_func):
        """Process all items in batches with pauses"""
        all_results = []
        total_batches = (len(items) + self.batch_size - 1) // self.batch_size

        for i in range(0, len(items), self.batch_size):
            batch = items[i:i + self.batch_size]
            batch_num = i // self.batch_size + 1

            print(f"\n📦 Processing batch {batch_num}/{total_batches} ({len(batch)} items)")

            batch_results = self.process_batch(batch, process_func)
            all_results.extend(batch_results)

            # Pause between batches (except after last)
            if i + self.batch_size < len(items):
                pause = self.calculate_pause_duration()
                print(f"⏸️  Pausing for {pause/60:.1f} minutes before next batch...")
                print(f"   (Simulates human usage pattern, prevents rate limiting)")
                time.sleep(pause)

        return all_results
```

### Layer 6: Comprehensive Audit Logging
**Purpose:** Compliance, debugging, and forensics

```python
import logging
import json
from datetime import datetime

class AuditLogger:
    """
    Structured audit logging for compliance and debugging
    Follows industry standard log formats
    """
    def __init__(self, log_file="log/api_audit.jsonl"):
        self.log_file = log_file

        # Ensure directory exists
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        # Configure logger
        self.logger = logging.getLogger('SerpAPI_Audit')
        self.logger.setLevel(logging.INFO)

        # File handler (JSON Lines format)
        handler = logging.FileHandler(log_file)
        handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(handler)

    def log_api_call(self, **kwargs):
        """Log API call with full context"""
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': 'api_call',
            **kwargs
        }
        self.logger.info(json.dumps(log_entry))

    def log_error(self, **kwargs):
        """Log error with full context"""
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': 'error',
            **kwargs
        }
        self.logger.error(json.dumps(log_entry))

    def log_rate_limit(self, **kwargs):
        """Log rate limit event"""
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': 'rate_limit',
            'severity': 'WARNING',
            **kwargs
        }
        self.logger.warning(json.dumps(log_entry))
```

### Layer 7: Health Monitor with Alerts
**Purpose:** Real-time monitoring and alerting

```python
class ComprehensiveHealthMonitor:
    """
    Enhanced health monitoring with alerting
    Tracks multiple metrics and triggers warnings
    """
    def __init__(self):
        self.metrics = {
            'total_calls': 0,
            'successful_calls': 0,
            'failed_calls': 0,
            'rate_limit_errors': 0,
            'server_errors': 0,
            'auth_errors': 0,
            'companies_processed': 0,
            'companies_with_jobs': 0,
            'total_jobs_found': 0,
            'avg_response_time_ms': 0
        }

        self.response_times = []
        self.consecutive_failures = 0
        self.start_time = time.time()

        # Alert thresholds
        self.ALERT_THRESHOLDS = {
            'failure_rate': 0.20,  # 20% failure rate
            'consecutive_failures': 3,
            'rate_limit_errors': 2,
            'success_rate': 0.10  # 10% success rate (companies with jobs)
        }

    def record_call(self, status_code, company, jobs_found, response_time_ms):
        """Record comprehensive call metrics"""
        self.metrics['total_calls'] += 1
        self.metrics['companies_processed'] += 1
        self.response_times.append(response_time_ms)

        if status_code == 200:
            self.metrics['successful_calls'] += 1
            self.consecutive_failures = 0
        else:
            self.metrics['failed_calls'] += 1
            self.consecutive_failures += 1

        # Categorize errors
        if status_code in [403, 429]:
            self.metrics['rate_limit_errors'] += 1
        elif status_code in [401, 402]:
            self.metrics['auth_errors'] += 1
        elif status_code >= 500:
            self.metrics['server_errors'] += 1

        # Track jobs
        if jobs_found > 0:
            self.metrics['companies_with_jobs'] += 1
            self.metrics['total_jobs_found'] += jobs_found

        # Update average response time
        self.metrics['avg_response_time_ms'] = sum(self.response_times) / len(self.response_times)

        # Check for alerts
        self._check_alerts()

    def _check_alerts(self):
        """Check if any alert thresholds are exceeded"""
        alerts = []

        # Failure rate alert
        if self.metrics['total_calls'] > 0:
            failure_rate = self.metrics['failed_calls'] / self.metrics['total_calls']
            if failure_rate > self.ALERT_THRESHOLDS['failure_rate']:
                alerts.append(f"High failure rate: {failure_rate*100:.1f}%")

        # Consecutive failures
        if self.consecutive_failures >= self.ALERT_THRESHOLDS['consecutive_failures']:
            alerts.append(f"Consecutive failures: {self.consecutive_failures}")

        # Rate limit errors
        if self.metrics['rate_limit_errors'] >= self.ALERT_THRESHOLDS['rate_limit_errors']:
            alerts.append(f"Rate limit errors detected: {self.metrics['rate_limit_errors']}")

        # Low success rate (companies with jobs)
        if self.metrics['companies_processed'] >= 10:
            success_rate = self.metrics['companies_with_jobs'] / self.metrics['companies_processed']
            if success_rate < self.ALERT_THRESHOLDS['success_rate']:
                alerts.append(f"Low success rate: {success_rate*100:.1f}%")

        if alerts:
            print("\n🚨 HEALTH ALERTS:")
            for alert in alerts:
                print(f"   ⚠️  {alert}")
            print()

    def get_comprehensive_report(self):
        """Generate comprehensive health report"""
        runtime = time.time() - self.start_time

        report = {
            'runtime_seconds': runtime,
            'runtime_formatted': f"{runtime/60:.1f} minutes",
            'total_calls': self.metrics['total_calls'],
            'successful_calls': self.metrics['successful_calls'],
            'failed_calls': self.metrics['failed_calls'],
            'success_rate_pct': (self.metrics['successful_calls'] / self.metrics['total_calls'] * 100)
                                if self.metrics['total_calls'] > 0 else 0,
            'companies_processed': self.metrics['companies_processed'],
            'companies_with_jobs': self.metrics['companies_with_jobs'],
            'company_success_rate_pct': (self.metrics['companies_with_jobs'] / self.metrics['companies_processed'] * 100)
                                        if self.metrics['companies_processed'] > 0 else 0,
            'total_jobs_found': self.metrics['total_jobs_found'],
            'avg_jobs_per_company': (self.metrics['total_jobs_found'] / self.metrics['companies_with_jobs'])
                                    if self.metrics['companies_with_jobs'] > 0 else 0,
            'avg_response_time_ms': self.metrics['avg_response_time_ms'],
            'rate_limit_errors': self.metrics['rate_limit_errors'],
            'auth_errors': self.metrics['auth_errors'],
            'server_errors': self.metrics['server_errors'],
            'calls_per_minute': (self.metrics['total_calls'] / (runtime / 60))
                                if runtime > 0 else 0
        }

        return report
```

---

## 📊 Implementation Checklist

### Pre-Implementation
- [ ] Review SerpAPI Terms of Service
- [ ] Document all rate limits
- [ ] Establish monitoring baseline
- [ ] Create audit log directory

### Code Implementation
- [ ] Layer 1: Configuration Validation
- [ ] Layer 2: Token Bucket Rate Limiter
- [ ] Layer 3: Circuit Breaker
- [ ] Layer 4: Exponential Backoff
- [ ] Layer 5: Batch Processor
- [ ] Layer 6: Audit Logger
- [ ] Layer 7: Health Monitor

### Integration
- [ ] Integrate all layers into AeroComps.py
- [ ] Update configuration with safe defaults
- [ ] Add comprehensive error messages
- [ ] Create operator documentation

### Testing
- [ ] Test configuration validation
- [ ] Test rate limiter with single company
- [ ] Test circuit breaker triggers
- [ ] Test batch processing
- [ ] Test full run with 3 companies
- [ ] Verify audit logs created

### Documentation
- [ ] Update README with new safeguards
- [ ] Document all configuration options
- [ ] Create troubleshooting guide
- [ ] Add compliance documentation

---

## 🎯 Success Criteria

**System is bulletproof when:**

1. ✅ Cannot be misconfigured to cause IP block
2. ✅ Automatically stops on first sign of rate limiting
3. ✅ Logs all API calls for audit/debugging
4. ✅ Processes at safe rate (max 60 calls/hour)
5. ✅ Gracefully degrades on errors
6. ✅ Provides clear error messages and guidance
7. ✅ Complies with all ToS and legal requirements
8. ✅ Can recover automatically from temporary issues

---

**This specification ensures:**
- Legal compliance with SerpAPI ToS
- Industry-standard rate limiting
- Comprehensive monitoring and logging
- Bulletproof protection against IP blocking
- Clear audit trail for compliance
- Professional-grade error handling
