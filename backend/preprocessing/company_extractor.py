
def extract_company_name(job_description):
    """
    Extract company name from job description text.
    """

    if not job_description:
        return None

    for line in job_description.splitlines():
        line = line.strip()

        if line.lower().startswith("company:"):
            company_name = line.split(":", 1)[1].strip()

            if company_name:
                return company_name

    return None


def compare_company_names(input_company, pdf_company):
    """
    Compare user-entered company name
    with the company name extracted from PDF.
    """

    if not input_company or not pdf_company:
        return {
            "status": "Unable to verify",
            "match": None
        }

    input_name = input_company.strip().lower()
    pdf_name = pdf_company.strip().lower()

    if input_name == pdf_name:
        return {
            "status": "Company name matched",
            "match": True
        }

    return {
        "status": "Company name mismatch detected",
        "match": False
    }


if __name__ == "__main__":

    sample_text = """
    PYTHON DEVELOPER JOB
    Company: Example Company
    Job Description:
    Python developer required.
    """

    extracted_company = extract_company_name(sample_text)

    print("Extracted Company:", extracted_company)

    result = compare_company_names(
        "Google",
        extracted_company
    )

    print("Comparison Result:", result)
