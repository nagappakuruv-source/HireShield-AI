
from backend.database.connection import get_connection


def create_tables():

    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS analysis_history (

                    id SERIAL PRIMARY KEY,

                    job_title TEXT NOT NULL,

                    company_name TEXT NOT NULL,

                    job_description TEXT,

                    prediction INTEGER,

                    result TEXT,

                    risk_score INTEGER,

                    risk_level TEXT,

                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

        connection.commit()

        print("Analysis history table created successfully!")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    create_tables()
