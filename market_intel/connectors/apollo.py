"""
Apollo.io Connector for Contact Enrichment

Apollo.io API Documentation: https://apolloio.github.io/apollo-api-docs/

Free tier: 50 credits/month
Endpoints used:
- /organizations/enrich (company lookup by domain)
- /mixed_people/search (find contacts at company)
"""

import requests
from typing import List, Dict, Any, Optional
from .base import BaseEnrichmentConnector, Company, Contact


class ApolloConnector(BaseEnrichmentConnector):
    """
    Apollo.io enrichment connector.

    Uses Apollo's API to:
    1. Look up company by domain
    2. Search for contacts at that company
    3. Filter by target titles/departments
    """

    BASE_URL = "https://api.apollo.io/v1"

    @property
    def source_name(self) -> str:
        return "apollo"

    def _fetch_contacts(self, company: Company) -> List[Contact]:
        """
        Fetch contacts from Apollo.io for a company.

        Strategy:
        1. Use company domain if available
        2. Fall back to company name search
        3. Filter results by target titles
        """
        contacts = []

        # Get domain from company
        domain = company.get_domain()

        if domain:
            # Primary path: Search by domain
            contacts = self._search_by_domain(domain, company.name)
        else:
            # Fallback: Search by company name
            contacts = self._search_by_name(company.name)

        # Filter by target titles if configured
        target_titles = self.config.get('target_titles', [])
        if target_titles and contacts:
            contacts = self._filter_by_titles(contacts, target_titles)

        return contacts

    def _search_by_domain(self, domain: str, company_name: str) -> List[Contact]:
        """Search for contacts at a company by domain."""

        headers = {
            "Content-Type": "application/json",
            "Cache-Control": "no-cache"
        }

        # Apollo uses api_key in the request body, not headers
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

        return self._parse_contacts(people, company_name)

    def _search_by_name(self, company_name: str) -> List[Contact]:
        """Search for contacts by company name (fallback)."""

        headers = {
            "Content-Type": "application/json",
            "Cache-Control": "no-cache"
        }

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

        return self._parse_contacts(people, company_name)

    def _parse_contacts(self, people: List[Dict], company_name: str) -> List[Contact]:
        """Parse Apollo API response into Contact objects."""

        contacts = []

        for person in people:
            contact = Contact(
                first_name=person.get("first_name", ""),
                last_name=person.get("last_name", ""),
                title=person.get("title", ""),
                department=person.get("department", "") or self._infer_department(person.get("title", "")),
                email=person.get("email", ""),
                phone=self._extract_phone(person),
                linkedin_url=person.get("linkedin_url", ""),
                seniority=person.get("seniority", ""),
                source="apollo",
                source_record_id=person.get("id", ""),
                confidence_score=self._calculate_confidence(person)
            )

            contacts.append(contact)

        return contacts

    def _extract_phone(self, person: Dict) -> str:
        """Extract phone number from Apollo person data."""
        # Apollo stores phones in organization or phone_numbers
        phone_numbers = person.get("phone_numbers", [])
        if phone_numbers:
            # Prefer direct dial
            for phone in phone_numbers:
                if phone.get("type") == "direct":
                    return phone.get("sanitized_number", "")
            # Fall back to any number
            return phone_numbers[0].get("sanitized_number", "")

        # Try organization phone
        org = person.get("organization", {})
        if org:
            return org.get("primary_phone", {}).get("sanitized_number", "")

        return ""

    def _infer_department(self, title: str) -> str:
        """Infer department from job title."""
        title_lower = title.lower()

        department_keywords = {
            "Engineering": ["engineer", "technical", "developer", "architect", "r&d"],
            "Sales": ["sales", "account", "business development", "revenue"],
            "Marketing": ["marketing", "brand", "communications", "pr"],
            "Operations": ["operations", "supply chain", "logistics", "manufacturing"],
            "Finance": ["finance", "accounting", "cfo", "controller"],
            "HR": ["hr", "human resources", "people", "talent", "recruiting"],
            "Executive": ["ceo", "president", "founder", "owner", "chief"]
        }

        for dept, keywords in department_keywords.items():
            for keyword in keywords:
                if keyword in title_lower:
                    return dept

        return ""

    def _calculate_confidence(self, person: Dict) -> float:
        """Calculate confidence score based on data completeness."""
        score = 0.0

        # Has email = +0.3
        if person.get("email"):
            score += 0.3

        # Has verified email = +0.2
        if person.get("email_status") == "verified":
            score += 0.2

        # Has phone = +0.2
        if person.get("phone_numbers"):
            score += 0.2

        # Has LinkedIn = +0.15
        if person.get("linkedin_url"):
            score += 0.15

        # Has title = +0.15
        if person.get("title"):
            score += 0.15

        return min(score, 1.0)

    def _filter_by_titles(self, contacts: List[Contact], target_titles: List[str]) -> List[Contact]:
        """Filter contacts to only include target titles."""
        filtered = []

        for contact in contacts:
            title_lower = contact.title.lower()
            for target in target_titles:
                if target.lower() in title_lower:
                    filtered.append(contact)
                    break

        return filtered


class MockApolloConnector(BaseEnrichmentConnector):
    """
    Mock Apollo connector for testing without API calls.

    Returns sample data to validate pipeline structure.
    """

    @property
    def source_name(self) -> str:
        return "mock_apollo"

    def _fetch_contacts(self, company: Company) -> List[Contact]:
        """Return mock contacts for testing."""
        import random

        # Generate 1-3 mock contacts
        num_contacts = random.randint(1, 3)
        contacts = []

        first_names = ["John", "Sarah", "Michael", "Emily", "David", "Lisa"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Davis"]
        titles = ["CEO", "VP Engineering", "Director of Sales", "Operations Manager", "Chief Technology Officer"]
        departments = ["Executive", "Engineering", "Sales", "Operations", "Technology"]

        for i in range(num_contacts):
            first = random.choice(first_names)
            last = random.choice(last_names)
            domain = company.get_domain() or "example.com"

            contact = Contact(
                first_name=first,
                last_name=last,
                title=random.choice(titles),
                department=random.choice(departments),
                email=f"{first.lower()}.{last.lower()}@{domain}",
                phone=f"+1-555-{random.randint(100,999)}-{random.randint(1000,9999)}",
                linkedin_url=f"https://linkedin.com/in/{first.lower()}{last.lower()}",
                seniority="director" if "Director" in titles[i % len(titles)] else "manager",
                source="mock_apollo",
                source_record_id=f"MOCK-{i+1}",
                confidence_score=random.uniform(0.6, 0.95)
            )
            contacts.append(contact)

        return contacts
