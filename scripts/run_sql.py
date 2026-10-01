import os
import re
import sys
from pathlib import Path

import pyodbc
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/run_sql.py sql/01_create_db.sql")

    sql_file = Path(sys.argv[1])
    if not sql_file.is_absolute():
        sql_file = PROJECT_ROOT / sql_file

    if not sql_file.is_file():
        raise SystemExit(f"SQL file not found: {sql_file}")

    server = os.getenv("SQL_SERVER")
    driver = os.getenv("SQL_DRIVER", "SQL Server")
    if not server:
        raise SystemExit("Set SQL_SERVER in the project .env file.")

    connection_string = (
        f"DRIVER={{{driver}}};"
        f"SERVER={server};"
        "DATABASE=master;"
        "Trusted_Connection=yes;"
    )

    sql_text = sql_file.read_text(encoding="utf-8")
    batches = re.split(r"(?im)^\s*GO\s*(?:--.*)?$", sql_text)

    connection = pyodbc.connect(connection_string, autocommit=True)
    cursor = connection.cursor()
    try:
        for batch in batches:
            if not batch.strip():
                continue

            cursor.execute(batch)
            if cursor.description:
                columns = [column[0] for column in cursor.description]
                print("\t".join(columns))
                for row in cursor.fetchall():
                    print("\t".join(str(value) for value in row))

        print(f"Finished running {sql_file.name}.")
    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    main()
