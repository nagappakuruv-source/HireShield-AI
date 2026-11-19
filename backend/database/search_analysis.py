
from backend.database.connection import get_connection


def search_analyses(
    keyword=None,
    risk_level=None,
    limit=10,
    offset=0
):

    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            query = """
                SELECT *
                FROM analysis_history
                WHERE 1=1
            """

            params = []

            if keyword:
                query += """
                    AND (
                        job_title ILIKE %s
                        OR company_name ILIKE %s
                    )
                """

                search_term = f"%{keyword}%"
                params.extend([search_term, search_term])

            if risk_level:
                query += """
                    AND LOWER(TRIM(risk_level)) = LOWER(%s)
                """

                params.append(risk_level.strip())

            query += """
                ORDER BY created_at DESC
                LIMIT %s OFFSET %s
            """

            params.extend([limit, offset])

            cursor.execute(query, params)

            return cursor.fetchall()

    finally:
        connection.close()


def count_search_results(keyword=None, risk_level=None):

    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            query = """
                SELECT COUNT(*) AS total
                FROM analysis_history
                WHERE 1=1
            """

            params = []

            if keyword:
                query += """
                    AND (
                        job_title ILIKE %s
                        OR company_name ILIKE %s
                    )
                """

                search_term = f"%{keyword}%"
                params.extend([search_term, search_term])

            if risk_level:
                query += """
                    AND LOWER(TRIM(risk_level)) = LOWER(%s)
                """

                params.append(risk_level.strip())

            cursor.execute(query, params)

            return cursor.fetchone()["total"]

    finally:
        connection.close()
