
from backend.database.connection import get_connection


def get_all_analyses():

    connection = None

    try:
        connection = get_connection()

        with connection.cursor() as cursor:

            cursor.execute("""
                SELECT *
                FROM analysis_history
                ORDER BY created_at DESC
            """)

            records = cursor.fetchall()

        return records

    except Exception as error:

        print("Database Retrieval Error:", error)
        raise

    finally:

        if connection:
            connection.close()


if __name__ == "__main__":

    analyses = get_all_analyses()

    print("\nHIRESHIELD AI - ANALYSIS HISTORY")
    print("--------------------------------")

    for analysis in analyses:

        print("\nAnalysis ID:", analysis["id"])
        print("Job Title:", analysis["job_title"])
        print("Company:", analysis["company_name"])
        print("Prediction:", analysis["result"])
        print("Risk Score:", analysis["risk_score"])
        print("Risk Level:", analysis["risk_level"])
        print("Created At:", analysis["created_at"])
