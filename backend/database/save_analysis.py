
from backend.database.connection import get_connection


def save_analysis(
    job_title,
    company_name,
    job_description,
    prediction,
    result,
    risk_score,
    risk_level
):

    connection = None

    try:
        connection = get_connection()

        with connection.cursor() as cursor:

            cursor.execute("""
                INSERT INTO analysis_history (
                    job_title,
                    company_name,
                    job_description,
                    prediction,
                    result,
                    risk_score,
                    risk_level
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (
                job_title,
                company_name,
                job_description,
                prediction,
                result,
                risk_score,
                risk_level
            ))

            analysis_id = cursor.fetchone()["id"]

        connection.commit()

        return analysis_id

    except Exception as error:

        if connection:
            connection.rollback()

        print("Database Save Error:", error)
        raise

    finally:

        if connection:
            connection.close()
