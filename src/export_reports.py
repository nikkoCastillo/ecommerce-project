import csv
import os
from pathlib import Path

import pyodbc
from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parents[1]
REPORTS = {
    "dbo.vw_monthly_sales": "monthly_sales.csv",
    "dbo.vw_category_sales": "category_sales.csv",
    "dbo.vw_regional_sales": "regional_sales.csv",
}


def main():
    load_dotenv(ROOT / ".env")
    server = os.getenv("SQL_SERVER_NAME")
    if not server:
        raise SystemExit("Set SQL_SERVER_NAME in the project's .env file.")

    database = os.getenv("SQL_DATABASE_NAME", "EcommerceAnalytics")
    driver = os.getenv("SQL_DRIVER", "ODBC Driver 18 for SQL Server")
    connection_string = (
        f"DRIVER={{{driver}}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        "Trusted_Connection=yes;"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
    )

    output_dir = ROOT / "data" / "exports"
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        with pyodbc.connect(connection_string, timeout=10) as connection:
            for view_name, filename in REPORTS.items():
                cursor = connection.cursor()
                cursor.execute(f"SELECT * FROM {view_name} ORDER BY 1")
                column_names = [column[0] for column in cursor.description]
                output_path = output_dir / filename

                with output_path.open("w", newline="", encoding="utf-8-sig") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(column_names)
                    writer.writerows(cursor.fetchall())

                print(f"Exported {output_path.relative_to(ROOT)}")
    except pyodbc.Error as error:
        raise SystemExit(f"Could not connect to SQL Server or read a report view: {error}") from error


if __name__ == "__main__":
    main()