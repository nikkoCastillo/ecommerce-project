# E-commerce Sales Analytics

A small end-to-end project using Microsoft SQL Server, Python, and Power BI. SQL Server stores sample order lines and calculates sales summaries, Python exports those summaries to CSV, and Power BI turns them into a simple report.

## Project layout

```text
sql/
	01_schema.sql          Create the database and order-lines table
	02_sample_data.sql     Insert repeatable sample data
	03_analysis_views.sql  Create reporting views
src/
	export_reports.py      Export the views to CSV
data/exports/            Generated CSV files (not committed)
.env.example             Connection settings template
requirements.txt         Python dependencies
```

## Step-by-step setup

### 1. Check SQL Server

SSMS is the management application; the SQL Server Database Engine must also be installed and running. In SSMS, connect to your instance using Windows Authentication. Note the server name shown in the connection dialog, for example `localhost`, `localhost\\SQLEXPRESS`, or `MYPC\\SQLEXPRESS`.

Install the Microsoft ODBC Driver 18 for SQL Server if it is not already installed. The Python connection settings below use that driver.

### 2. Create and populate the database

In SSMS, open and execute these files in order:

1. `sql/01_schema.sql` creates the `EcommerceAnalytics` database and its `dbo.order_lines` table.
2. `sql/02_sample_data.sql` inserts the sample orders. It only inserts them when the table is empty, so it is safe to run again.
3. `sql/03_analysis_views.sql` creates the monthly, product-category, and regional sales views.

Refresh the `EcommerceAnalytics` database in Object Explorer and confirm that the table and three views appear under `Tables` and `Views`.

### 3. Set up Python

From the project folder, create and activate a virtual environment, then install the dependencies:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If PowerShell blocks environment activation, run the install and script with the environment's Python directly instead:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 4. Configure the SQL Server connection

Copy the example settings and edit the server name to match the one you used in SSMS:

```powershell
Copy-Item .env.example .env
```

Open `.env` and update `SQL_SERVER_NAME`. The starter uses Windows Authentication, like an SSMS connection configured for Windows Authentication. `.env` is excluded from Git.

### 5. Export the reports with Python

Run:

```powershell
python src/export_reports.py
```

The script reads the three SQL views and writes `monthly_sales.csv`, `category_sales.csv`, and `regional_sales.csv` to `data/exports/`. If the connection fails, check that the SQL Server service is running, the server name is correct, Windows Authentication is enabled for your account, and ODBC Driver 18 is installed.

### 6. Build a small Power BI report

In Power BI Desktop, choose **Get data** and use either approach:

- **Connect to SQL Server:** enter the same server and `EcommerceAnalytics` database, choose **Import**, and select `dbo.vw_monthly_sales`, `dbo.vw_category_sales`, and `dbo.vw_regional_sales`. Authenticate with Windows credentials.
- **Use the Python exports:** choose **Text/CSV** and load the three files from `data/exports/`.

Create a line chart with `year_month` and `revenue`, bar charts with `category` and `region` against `revenue`, and a card for total revenue. Save the report as `reports/ecommerce-sales.pbix` if you want to keep it in this repository; Power BI Desktop is a separate install and the `.pbix` file is optional.

## GitHub

After checking that the files do not include credentials or other private data, commit and push the project:

Run these commands in Git Bash or a terminal where Git is on `PATH`. If PowerShell says `git` is not recognized, add Git's `cmd` folder (commonly `C:\Program Files\Git\cmd`) to `PATH` and open a new terminal.

```powershell
git add README.md .gitignore .env.example requirements.txt sql src
git commit -m "Add SQL Server e-commerce analytics starter"
git push origin main
```

The `.env`, virtual environment, Python cache, generated CSVs, and local Power BI report are excluded by `.gitignore`.
