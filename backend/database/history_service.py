
from backend.database.connection import get_connection



def get_analysis_history(limit=10, offset=0):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM analysis_history
        ORDER BY created_at DESC
        LIMIT ? OFFSET ?
    """, (limit, offset))

    records = cursor.fetchall()

    connection.close()

    return [dict(record) for record in records]


if __name__ == "__main__":

    history = get_analysis_history()

    print("\nHIREShield AI - HISTORY SERVICE")
    print("--------------------------------")

    for record in history:
        print(record)

def get_analysis_by_id(analysis_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM analysis_history
        WHERE id = ?
    """, (analysis_id,))

    record = cursor.fetchone()

    connection.close()

    if record:
        return dict(record)

    return None
if __name__ == "__main__":

    analysis = get_analysis_by_id(3)

    if analysis:
        print("Analysis Found:")
        print(analysis)
    else:
        print("Analysis not found")

def get_total_analysis_count():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*) FROM analysis_history
    """)

    total = cursor.fetchone()[0]

    connection.close()

    return total
