
from backend.database.connection import get_connection


def create_tables():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analysis_history (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

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
    connection.close()

    print("Analysis history table created successfully!")


if __name__ == "__main__":
    create_tables()
