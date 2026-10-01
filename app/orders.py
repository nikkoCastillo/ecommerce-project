from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.db import get_db_connection

orders_bp = Blueprint("orders", __name__)


@orders_bp.route("/orders", methods=["GET", "POST"])
@login_required
def index():
	"""Place a demo order and show the signed-in user's order history."""
	if request.method == "POST":
		try:
			product_id = int(request.form.get("product_id", ""))
			quantity = int(request.form.get("quantity", ""))
			if product_id <= 0 or quantity <= 0:
				raise ValueError
		except ValueError:
			flash("Choose a product and enter a quantity greater than zero.")
			return redirect(url_for("orders.index"))

		conn = None
		try:
			conn = get_db_connection()
			cursor = conn.cursor()
			cursor.execute(
				"SELECT Price FROM dbo.Products WHERE ProductID = ? AND IsActive = 1",
				(product_id,),
			)
			product = cursor.fetchone()
			if product is None:
				flash("That product is unavailable. Please choose an active product.")
				return redirect(url_for("orders.index"))

			cursor.execute(
				"""
				INSERT INTO dbo.Orders (UserID, Status)
				OUTPUT INSERTED.OrderID
				VALUES (?, N'Completed')
				""",
				(current_user.id,),
			)
			order_id = cursor.fetchone()[0]
			cursor.execute(
				"""
				INSERT INTO dbo.OrderItems (OrderID, ProductID, Quantity, UnitPrice)
				VALUES (?, ?, ?, ?)
				""",
				(order_id, product_id, quantity, product[0]),
			)
			conn.commit()
			flash("Demo order placed successfully.")
		except Exception:
			if conn is not None:
				conn.rollback()
			flash("Something went wrong while placing your order.")
		finally:
			if conn is not None:
				conn.close()

		return redirect(url_for("orders.index"))

	conn = None
	try:
		conn = get_db_connection()
		cursor = conn.cursor()
		cursor.execute(
			"""
			SELECT ProductID, Name, Category, Price
			FROM dbo.Products
			WHERE IsActive = 1
			ORDER BY Name
			"""
		)
		products = cursor.fetchall()
		cursor.execute(
			"""
			SELECT o.OrderID, o.OrderDate, o.Status, p.Name,
				   oi.Quantity, oi.UnitPrice
			FROM dbo.Orders AS o
			INNER JOIN dbo.OrderItems AS oi ON oi.OrderID = o.OrderID
			INNER JOIN dbo.Products AS p ON p.ProductID = oi.ProductID
			WHERE o.UserID = ?
			ORDER BY o.OrderDate DESC, o.OrderID DESC, oi.OrderItemID
			""",
			(current_user.id,),
		)
		orders = cursor.fetchall()
	except Exception:
		flash("Unable to load your orders right now.")
		return "Unable to load your orders right now.", 500
	finally:
		if conn is not None:
			conn.close()

	return render_template("orders.html", products=products, orders=orders)
