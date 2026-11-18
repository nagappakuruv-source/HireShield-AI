
import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types


# Load environment variables from .env
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY not found in .env file"
    )


# Create Gemini client
client = genai.Client(
    api_key=api_key,
    http_options=types.HttpOptions(timeout=60000)
)


# Model recommended by Google's API error message
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
        if prediction == 1
        else "Genuine Job"
    )

    prompt = f"""
You are an AI job fraud analysis assistant
for HireShield AI.

Analyze the following information.

JOB DETAILS
-----------
Job Title: {job_title}
Company: {company_name}
Description: {job_description}

MACHINE LEARNING PREDICTION
--------------------------
{prediction_result}

COMPANY VERIFICATION
--------------------
{company_verification}

RISK ASSESSMENT
---------------
{risk_assessment}

YOUR TASK
---------
Provide:

1. Overall risk explanation.
2. Suspicious warning signs.
3. Company verification observations.
4. Safety recommendations.

IMPORTANT RULES
---------------
- Use simple English.
- Explain only using the supplied evidence.
- Do not invent facts.
- A reachable website does not prove a job is genuine.
- Clearly explain missing verification information.
- Do not treat the risk score as a probability.
- Do not make unsupported claims.
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
                contents=prompt
            )

            if response.text:
                return response.text

            return "Gemini returned an empty response."

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
                "ML fraud prediction",
                "Official domain mismatch"
            ]
        }
    )

    print("\nHIRE SHIELD AI - GEMINI EXPLANATION")
    print("-----------------------------------")
    print(explanation)
