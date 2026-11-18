import sqlite3
from backend.database.connection import get_connection
from backend.database.connection import get_connection


def search_analyses(
    keyword=None,
    risk_level=None,
    limit=10,
    offset=0
):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT *
        FROM analysis_history
        WHERE 1=1
    """

    params = []

    if keyword:
        query += """
            AND (
                job_title LIKE ?
                OR company_name LIKE ?
            )
        """
        search_term = f"%{keyword}%"
        params.extend([search_term, search_term])

    if risk_level:
        query += """
            AND LOWER(TRIM(risk_level)) = LOWER(?)
        """
        params.append(risk_level.strip())

    query += """
        ORDER BY created_at DESC
        LIMIT ? OFFSET ?
    """

    params.extend([limit, offset])

    cursor.execute(query, params)

    records = cursor.fetchall()
    connection.close()

    return [dict(record) for record in records]

def count_search_results(keyword=None, risk_level=None):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT COUNT(*)
        FROM analysis_history
        WHERE 1=1
    """

    params = []

    if keyword:
        query += """
            AND (
                job_title LIKE ?
                OR company_name LIKE ?
            )
        """
        search_term = f"%{keyword}%"
        params.extend([search_term, search_term])

    if risk_level:
        query += """
            AND LOWER(TRIM(risk_level)) = LOWER(?)
        """
        params.append(risk_level.strip())

    cursor.execute(query, params)

    total = cursor.fetchone()[0]

    connection.close()

    return total
