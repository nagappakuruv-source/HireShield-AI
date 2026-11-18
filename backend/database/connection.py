
import sqlite3
from pathlib import Path

# Get the project root directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Database file location
DATABASE_PATH = BASE_DIR / "hireshield.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)

    # Return rows as dictionary-like objects
    connection.row_factory = sqlite3.Row

    return connection


if __name__ == "__main__":

    connection = get_connection()

    print("Database connected successfully!")
    print("Database location:", DATABASE_PATH)

    connection.close()
