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
