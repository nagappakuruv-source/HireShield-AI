
from backend.database.connection import get_connection


def delete_analysis(analysis_id):

    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute("""
                DELETE FROM analysis_history
                WHERE id = %s
            """, (analysis_id,))

            deleted = cursor.rowcount

        connection.commit()

        return deleted > 0

    except Exception as error:

        connection.rollback()
        print("Database Delete Error:", error)
        raise

    finally:
        connection.close()
