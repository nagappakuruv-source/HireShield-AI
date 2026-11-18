import sqlite3
import sqlite3
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
        cursor = connection.cursor()

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
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            job_title,
            company_name,
            job_description,
            prediction,
            result,
            risk_score,
            risk_level
        ))

        connection.commit()

        return cursor.lastrowid

    except sqlite3.Error as error:

        if connection:
            connection.rollback()

        print("Database Save Error:", error)
        raise

    finally:

        if connection:
            connection.close()

if __name__ == "__main__":

    analysis_id = save_analysis(
        job_title="Python Developer",
        company_name="Example Company",
        job_description="Python developer required.",
        prediction=1,
        result="Fraudulent Job",
        risk_score=75,
        risk_level="High Risk"
    )

    print("Analysis saved successfully!")
    print("Analysis ID:", analysis_id)
