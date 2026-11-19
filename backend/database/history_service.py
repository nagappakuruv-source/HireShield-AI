
from backend.database.connection import get_connection


def get_analysis_history(limit=10, offset=0):

    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute("""
                SELECT *
                FROM analysis_history
                ORDER BY created_at DESC
                LIMIT %s OFFSET %s
            """, (limit, offset))

            records = cursor.fetchall()

            return records

    finally:
        connection.close()


def get_analysis_by_id(analysis_id):

    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute("""
                SELECT *
                FROM analysis_history
                WHERE id = %s
            """, (analysis_id,))

            record = cursor.fetchone()

            return record

    finally:
        connection.close()


def get_total_analysis_count():

    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute("""
                SELECT COUNT(*) AS total
                FROM analysis_history
            """)

            result = cursor.fetchone()

            return result["total"]

    finally:
        connection.close()
