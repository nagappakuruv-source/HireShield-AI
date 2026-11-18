
from urllib.parse import urlparse
import requests


# STEP 1: Trusted company domains database
OFFICIAL_DOMAINS = {
    "google": ["google.com"],
    "microsoft": ["microsoft.com"],
    "amazon": ["amazon.com", "amazon.jobs"]
}


# STEP 2: Recognized company-name variations
COMPANY_ALIASES = {
    "google company": "google",
    "google inc": "google",
    "microsoft corporation": "microsoft",
    "amazon company": "amazon"
}


# STEP 3: Extract the main domain
def extract_domain(website_url):

    if not isinstance(website_url, str):
        return None

    try:
        parsed_url = urlparse(website_url.strip())

        if parsed_url.scheme not in ("http", "https"):
            return None

        if not parsed_url.hostname:
            return None

        domain = parsed_url.hostname.lower()

        if domain.startswith("www."):
            domain = domain[4:]

        return domain

    except ValueError:
        return None


# STEP 4: Check website reachability
def check_website(website_url):

    try:
        response = requests.get(
            website_url,
            timeout=10
        )

        if response.status_code == 200:
            return "Website is reachable"

        return f"Website responded with status: {response.status_code}"

    except requests.RequestException:
        return "Website is not reachable"


# STEP 5: Combine domain and website checks
def verify_company(website_url):

    domain = extract_domain(website_url)

    if domain is None:
        return {
            "domain": None,
            "website_status": "Invalid URL",
            "verification_status": "Unverified"
        }

    website_status = check_website(website_url)

    if website_status == "Website is reachable":
        verification_status = (
            "Website reachable (company not yet verified)"
        )
    else:
        verification_status = "Unverified"

    return {
        "domain": domain,
        "website_status": website_status,
        "verification_status": verification_status
    }


# STEP 6: Verify official company domain
def verify_official_domain(company_name, website_url):

    if not isinstance(company_name, str):
        return "Company not found in trusted database"

    company = company_name.strip().lower()

    # Normalize recognized company-name variations
    company = COMPANY_ALIASES.get(company, company)

    submitted_domain = extract_domain(website_url)

    if submitted_domain is None:
        return "Invalid website URL"

    trusted_domains = OFFICIAL_DOMAINS.get(company)

    if trusted_domains is None:
        return "Company not found in trusted database"

    for trusted_domain in trusted_domains:

        if (
            submitted_domain == trusted_domain
            or submitted_domain.endswith("." + trusted_domain)
        ):
            return "Official domain matched"

    return "Domain mismatch - suspicious website"


# STEP 7: Check careers-related URL
def check_careers_page(website_url):

    try:
        parsed_url = urlparse(website_url.strip())

        if parsed_url.scheme not in ("http", "https"):
            return "Invalid URL"

        if not parsed_url.hostname:
            return "Invalid URL"

        hostname = parsed_url.hostname.lower()
        path = parsed_url.path.lower()

        careers_keywords = [
            "career",
            "careers",
            "jobs"
        ]

        for keyword in careers_keywords:

            if keyword in hostname or keyword in path:
                return "Careers-related URL detected"

        return "No careers-related URL detected"

    except (AttributeError, ValueError):
        return "Invalid URL"


# STEP 8: Generate complete company verification report
def generate_company_report(company_name, website_url):

    company_result = verify_company(website_url)

    official_result = verify_official_domain(
        company_name,
        website_url
    )

    careers_result = check_careers_page(website_url)

    return {
        "company_name": company_name,
        "domain": company_result["domain"],
        "website_status": company_result["website_status"],
        "official_domain_status": official_result,
        "careers_page_status": careers_result
    }


# STEP 9: Test the complete verification engine
if __name__ == "__main__":

    test_cases = [
        ("Google", "https://www.google.com/careers"),
        ("Google", "https://careers.google.com"),
        ("google company", "https://www.google.com"),
        ("Microsoft", "https://www.microsoft.com"),
        ("Amazon", "https://www.amazon.jobs"),
        ("Google", "https://notgoogle.com")
    ]

    for company, url in test_cases:

        report = generate_company_report(
            company,
            url
        )

        print("\nCOMPANY VERIFICATION REPORT")
        print("----------------------------")

        for key, value in report.items():
            print(f"{key}: {value}")

        print("============================")
