# Load completed monthly sales from SQL Server and prepare dashboard totals.
import pandas as pd
from flask import Blueprint, flash, render_template
from flask_login import login_required

from app.db import get_db_connection

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
@login_required
def index():
    conn = None

    try:
        conn = get_db_connection()
        sales = pd.read_sql_query(
            """
            SELECT MonthStart, OrderCount, Revenue
            FROM dbo.vw_MonthlySales
            ORDER BY MonthStart
            """,
            conn,
        )
    except Exception:
        flash("Unable to load sales data right now.")
        return "Unable to load sales data right now.", 500
    finally:
        if conn is not None:
            conn.close()

    sales["MonthStart"] = pd.to_datetime(sales["MonthStart"]).dt.strftime("%Y-%m")
    total_revenue = float(sales["Revenue"].sum()) if not sales.empty else 0.0
    total_orders = int(sales["OrderCount"].sum()) if not sales.empty else 0

    return render_template(
        "dashboard.html",
        sales=sales.to_dict(orient="records"),
        total_revenue=total_revenue,
        total_orders=total_orders,
    )
