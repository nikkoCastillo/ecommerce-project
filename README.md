# E-commerce CRUD and Sales Dashboard

A beginner project with a Flask app for registration, login, product/order CRUD, SQL Server as the data store, pandas for sales analysis, and Power BI for reporting.

## Current project status

The database schema and completed-sales view are working. The Flask registration/login flow, product management, order placement/history, and pandas dashboard have been implemented and tested locally. The Power BI report is saved as `powerbi/ecommerce_sales.pbix`.

This is a local learning/demo project. Orders are marked completed for reporting demonstrations; the app does not process real payments. Review security, input validation, error logging, and deployment configuration before production use.

Configure the SQL Server connection locally in `.env`:

- Server: your SQL Server instance name (`SQL_SERVER`)
- Database: `EcommerceDemo`
- Authentication: Windows integrated authentication
- ODBC driver name: `SQL Server`

SSMS 22 is the client used to manage and query SQL Server. A running SQL Server Database Engine is also required.

## Project layout

```text
README.md
requirements.txt
.gitignore
.env.example
run.py
app/
  __init__.py
  db.py
  models.py
  auth.py
  products.py
  orders.py
  dashboard.py
  templates/
    login.html
    register.html
    products.html
    product_form.html
    orders.html
    dashboard.html
sql/
  01_create_db.sql
  02_create_tables.sql
  03_analysis_queries.sql
scripts/
  run_sql.py
powerbi/
  ecommerce_sales.pbix
```

## 1. Check the prerequisites

Install Python, Power BI Desktop, and the Microsoft SQL Server ODBC driver. In a project-folder PowerShell terminal, after installing `pyodbc`, check the driver names Python can see:

```powershell
.\.venv\Scripts\python.exe -c "import pyodbc; print(pyodbc.drivers())"
```

Confirm `SQL Server` appears in the output. If it does not, install a supported SQL Server ODBC driver and use its exact listed name for `SQL_DRIVER`. The newer Microsoft driver is commonly named `ODBC Driver 18 for SQL Server`.

## 2. Prepare Python and local settings

`requirements.txt` should contain:

```text
Flask
Flask-Login
Flask-WTF
python-dotenv
pyodbc
pandas
```

Create the virtual environment and install those packages from the project root:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Copy `.env.example` to `.env`, replace `YOUR_SQL_SERVER_NAME` with your own SQL Server instance name, and set a strong local `SECRET_KEY`. Keep `.env` private and never commit it. `.gitignore` excludes `.env`; `.env.example` contains only placeholders and can be shared.

The app should build the connection string from those settings in `app/db.py`, approximately like this:

```python
connection_string = (
    f"DRIVER={{{driver}}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    "Trusted_Connection=yes;"
)
connection = pyodbc.connect(connection_string)
```

The connection string is assembled from your local `.env` values and uses Windows integrated authentication. Never commit the real `.env` file.

## 3. Run SQL scripts with Python

Python executes the project SQL files. The existing `scripts/run_sql.py` runner connects to `master` so it can create `EcommerceDemo` even when that database does not exist. It also splits on standalone `GO` lines, because `GO` is a batch separator rather than a SQL Server command understood by `pyodbc`.

```python
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
    raise SystemExit(
      "Usage: python scripts/run_sql.py sql/01_create_db.sql"
    )

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
```

The `EcommerceDemo` database and tables have already been created. Do not rerun `02_create_tables.sql` against this database because its tables already exist. For a fresh database, run scripts from the project root in this order:

```powershell
.\.venv\Scripts\python.exe scripts\run_sql.py sql\01_create_db.sql
.\.venv\Scripts\python.exe scripts\run_sql.py sql\02_create_tables.sql
.\.venv\Scripts\python.exe scripts\run_sql.py sql\03_analysis_queries.sql
```

The first script creates the database, the second creates tables and sample products, and the third creates the reporting view. To rerun only the analysis script from the project root, use `python scripts/run_sql.py sql/03_analysis_queries.sql` (or the equivalent command for your Python environment).

In `sql/02_create_tables.sql`, define these tables:

| Table | Important columns |
| --- | --- |
| `Users` | `UserID` primary key, unique `Email`, `PasswordHash`, `IsAdmin`, `CreatedAt` |
| `Products` | `ProductID` primary key, `Name`, `Category`, `Price`, `IsActive` |
| `Orders` | `OrderID` primary key, `UserID` foreign key, `OrderDate`, `Status` |
| `OrderItems` | `OrderItemID` primary key, `OrderID` and `ProductID` foreign keys, `Quantity`, `UnitPrice` |

Use `decimal(10,2)` for prices, positive quantity checks, and foreign-key constraints. `OrderItems.UnitPrice` is the price at purchase time, so later product price changes do not rewrite sales history. Add a few fictional products with `INSERT` statements.

`sql/03_analysis_queries.sql` creates `dbo.vw_MonthlySales`. It includes completed orders only, groups by year and month, and returns `MonthStart`, `OrderCount`, and `Revenue`, where revenue is `SUM(OrderItems.Quantity * OrderItems.UnitPrice)`. The view has been executed and its results checked through Python.

Do not put user emails or password hashes into reporting views.

## 4. Verified features

The following local workflows have been exercised:

- SQL Server database, tables, sample products, and completed-sales view.
- Registration with hashed passwords, login/logout, and CSRF protection.
- Login-protected product listing and admin-only add, edit, and POST deactivation.
- Demo order placement and per-user order history.
- Login-protected pandas dashboard reading `dbo.vw_MonthlySales`.
- Flask development server launched through `run.py` and viewed in a browser.
- Power BI report saved at `powerbi/ecommerce_sales.pbix`.

Integration checks were performed during development. The local test helper is excluded from this public repository.

## 5. Run the application

Open `run.py` in VS Code and select **Run Python File**. The local development app is available at:

```text
http://127.0.0.1:5000/login
```

Flask debug mode is for local development only. Use fictional data when demonstrating the project.

## 6. Power BI report

The report is saved at `powerbi/ecommerce_sales.pbix` and uses the SQL Server database `EcommerceDemo` and view `dbo.vw_MonthlySales`. To reconnect it in Power BI Desktop, choose **Get data > SQL Server**, use Windows authentication, and load that view. For a local SQL Server without a trusted TLS certificate, Power BI may require disabling **Use encrypted connection** for this local connection; use a trusted certificate for network or production use.

## 7. Possible next improvements

- Add structured database error logging.
- Expand accessibility and visual styling across the HTML templates.
- Review the application’s security and configuration before any production deployment.

## Troubleshooting connection errors

- Confirm the SQL Server Database Engine is running and the server name matches the one that connected in SSMS.
- Confirm `pyodbc.drivers()` lists the exact name in `SQL_DRIVER`.
- Confirm `.env` is beside `run.py`, and that you edited `.env`, not only `.env.example`.
- Confirm Windows authentication is enabled and your Windows account has access to `EcommerceDemo`.
- Do not share `.env` contents; it contains local configuration and may contain secrets.