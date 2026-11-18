
import re


def calculate_risk_score(
    prediction,
    company_verification,
    company_consistency=None,
    job_description=None
):
    risk_score = 0
    reasons = []

    company_verification = company_verification or {}
    description = (job_description or "").lower()

    # Rule 1: ML prediction
    if prediction == 1:
        risk_score += 60
        reasons.append(
            "ML model detected a potentially fraudulent job"
        )

    # Rule 2: Company consistency
    if company_consistency:
        if company_consistency.get("match") is False:
            risk_score += 15
            reasons.append(
                "Company name mismatch between form and PDF"
            )

    # Rule 3: Registration or application fee
    fee_pattern = (
        r"\b(r[ei]gistration|application|processing)\s+fee\b"
        r"|\b(pay|payment|deposit)\b.{0,40}\b(fee|money|amount)\b"
    )

    fee_negation = re.search(
    r"\b(no|without|not)\b[^.!?;]{0,50}"
    r"(?:registration|application|processing)\s+fee\b",
    description
)

    if re.search(fee_pattern, description) and not fee_negation:
        risk_score += 40
        reasons.append(
            "Job description requests a registration or application fee"
        )

    # Rule 4: Guaranteed placement
    if re.search(   r"\b(?:guaranteed\s+(?:job\s+)?placement|"
    r"guaranteed\s+job|"
    r"100%\s*job\s+guarantee|"
    r"(?:we\s+)?guarantee(?:s)?\s+100%\s+job\s+placement|"
    r"100%\s+job\s+placement\s+guarantee)\b",
    description,
    re.IGNORECASE):
        risk_score += 20
        reasons.append(
            "Job promises guaranteed placement"
        )

    # Rule 5: No interview required
    if re.search(
            r"\b(?:no\s+interview(?:\s+(?:is\s+)?(?:required|needed))?|"
    r"without\s+interview|"
    r"interview\s+is\s+not\s+required)\b",
    description,
    re.IGNORECASE
    ):
        risk_score += 20
        reasons.append(
            "Job claims that no interview is required"
        )

    # Rule 6: Urgency and pressure tactics
    urgency_words = [
        "urgent hiring",
        "limited vacancies",
        "contact us immediately",
        "apply immediately"
    ]

    if any(word in description for word in urgency_words):
        risk_score += 10
        reasons.append(
            "Job description uses urgency or pressure tactics"
        )

    # Rule 7: Official domain verification
    domain_status = company_verification.get(
        "official_domain_status"
    )

    if domain_status == "Domain mismatch - suspicious website":
        risk_score += 30
        reasons.append("Company domain mismatch detected")

    elif domain_status == "Company not found in trusted database":
        risk_score += 15
        reasons.append(
            "Company is not in our trusted database"
        )

    # Rule 8: Website accessibility
    website_status = company_verification.get(
        "website_status"
    )

    if website_status == "Website is not reachable":
        risk_score += 10
        reasons.append("Company website is not reachable")

    elif website_status == "Invalid URL":
        risk_score += 20
        reasons.append("Invalid company website URL")

    # Maximum score
    risk_score = min(risk_score, 100)

    # Risk classification
    if risk_score >= 60:
        risk_level = "High Risk"
    elif risk_score >= 30:
        risk_level = "Medium Risk"
    else:
        risk_level = "Low Risk"

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "reasons": reasons
    }

# Test the Risk Assessment Engine
if __name__ == "__main__":

    test_cases = [
        {
            "name": "High Risk Test",
            "prediction": 1,
            "company_verification": {
                "official_domain_status":
                    "Domain mismatch - suspicious website",
                "website_status": "Website is reachable"
            },
            "company_consistency": None
        },
        {
            "name": "Company Mismatch Test",
            "prediction": 1,
            "company_verification": {
                "official_domain_status": "Official domain matched",
                "website_status": "Website is reachable"
            },
            "company_consistency": {
                "status": "Company name mismatch detected",
                "match": False
            }
        },
        {
            "name": "Low Risk Test",
            "prediction": 0,
            "company_verification": {
                "official_domain_status": "Official domain matched",
                "website_status": "Website is reachable"
            },
            "company_consistency": {
                "status": "Company name matched",
                "match": True
            }
        }
    ]

    for test in test_cases:

        result = calculate_risk_score(
            test["prediction"],
            test["company_verification"],
            test["company_consistency"]
        )

        print("\n" + test["name"])
        print("----------------------")
        print(f"Risk Score: {result['risk_score']}/100")
        print(f"Risk Level: {result['risk_level']}")
        print(f"Reasons: {result['reasons']}")
