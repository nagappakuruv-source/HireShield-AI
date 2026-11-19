
import os
import time
import json

from dotenv import load_dotenv
from google import genai
from google.genai import types


# Load environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")


# Gemini client
client = genai.Client(
    api_key=api_key,
    http_options=types.HttpOptions(timeout=60000)
)

MODEL_NAME = "gemini-3.5-flash-lite"


def generate_risk_explanation(
    job_title,
    company_name,
    job_description,
    prediction,
    company_verification,
    risk_assessment
):

    prediction_result = (
        "Fraudulent Job"
        if int(prediction) == 1
        else "Genuine Job"
    )

    # Extract risk information directly
    risk_score = risk_assessment.get("risk_score", "Not available")
    risk_level = risk_assessment.get("risk_level", "Not available")
    risk_reasons = risk_assessment.get("reasons", [])

    # Format supplied verification data
    company_data = json.dumps(
        company_verification or {},
        indent=2,
        default=str
    )

    # Format risk reasons
    reasons_text = (
        "\n".join(f"- {reason}" for reason in risk_reasons)
        if risk_reasons
        else "No specific risk reasons were supplied."
    )

    prompt = f"""
You are HireShield AI, an assistant that explains
job fraud analysis results.

Analyze the supplied information and generate a clear,
professional security analysis report.

JOB DETAILS
-----------
Job Title: {job_title}
Company Name: {company_name}
Job Description:
{job_description[:12000] if job_description else "Not provided"}

MACHINE LEARNING RESULT
----------------------
ML Prediction: {prediction_result}

RISK ASSESSMENT
---------------
Risk Score: {risk_score}/100
Risk Level: {risk_level}

Risk Indicators:
{reasons_text}

COMPANY VERIFICATION DATA
-------------------------
{company_data}

REPORT FORMAT
-------------

### 1. Overall Risk Explanation

Write one complete paragraph explaining the overall risk.

You MUST explicitly include:
- The exact risk score: {risk_score}/100.
- The exact risk level: {risk_level}.
- The ML prediction: {prediction_result}.
- Why the risk assessment supports its classification.

IMPORTANT: Never leave the risk score or risk level incomplete.

### 2. Suspicious Warning Signs

Explain the supplied risk indicators using clear bullet points.

For each indicator:
- Explain what it means.
- Explain why it may be suspicious.
- Use only evidence from the supplied information.

If no indicators exist, clearly say so.

### 3. Company Verification Observations

Explain the company verification information.

- Identify available verification evidence.
- Clearly mention missing information.
- Do not assume that an empty verification result proves fraud.
- A reachable website alone does not establish legitimacy.

### 4. Safety Recommendations

Give practical recommendations based on the actual warning signs.

REPORT QUALITY RULES
--------------------
1. Use simple, professional English.
2. Write complete sentences.
3. Never produce unfinished sentences or bullet points.
4. Never leave a sentence ending with words such as
   "of", "because", "with", or "including".
5. Do not invent company details or verification results.
6. Do not contradict the supplied ML prediction.
7. Explain that ML prediction and risk assessment are
   separate signals when they differ.
8. A risk score is not a probability.
9. Do not invent additional risk indicators.
10. Do not repeat the same warning unnecessarily.
11. Include all four report sections.
12. Finish every section before moving to the next.
13. Return only the completed report.
"""

    max_retries = 3

    for attempt in range(max_retries):

        try:
            print(
                f"Connecting to Gemini... "
                f"Attempt {attempt + 1}/{max_retries}"
            )

            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.3,
                    max_output_tokens=1800
                )
            )

            explanation = response.text

            if explanation and explanation.strip():
                return explanation.strip()

            print("Gemini returned an empty response.")

        except Exception as error:

            error_message = str(error).upper()

            print("Gemini API Error:", error)

            temporary_error = any(
                error_code in error_message
                for error_code in [
                    "503",
                    "UNAVAILABLE",
                    "429",
                    "RESOURCE_EXHAUSTED",
                    "504",
                    "DEADLINE_EXCEEDED"
                ]
            )

            if temporary_error and attempt < max_retries - 1:

                wait_time = 2 ** (attempt + 1)

                print(
                    f"Temporary error. Retrying in "
                    f"{wait_time} seconds..."
                )

                time.sleep(wait_time)

            else:
                break

    return (
        "AI explanation is temporarily unavailable. "
        "The ML prediction, company verification "
        "and risk assessment are still available."
    )


# Independent Gemini test
if __name__ == "__main__":

    explanation = generate_risk_explanation(
        job_title="Python Developer",

        company_name="Example Company",

        job_description=(
            "Pay a registration fee of 2000 rupees "
            "to receive a guaranteed job."
        ),

        prediction=1,

        company_verification={
            "official_domain": False,
            "website_reachable": True
        },

        risk_assessment={
            "risk_score": 90,
            "risk_level": "High Risk",
            "reasons": [
                "Registration fee required",
                "Guaranteed job promise",
                "Official domain mismatch"
            ]
        }
    )

    print("\nHIRESHIELD AI - GEMINI EXPLANATION")
    print("-----------------------------------")
    print(explanation)
