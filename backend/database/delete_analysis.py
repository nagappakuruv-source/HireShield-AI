from backend.database.connection import get_connection


def delete_analysis(analysis_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM analysis_history
        WHERE id = ?
    """, (analysis_id,))

    deleted = cursor.rowcount

    connection.commit()
    connection.close()

    return deleted > 0