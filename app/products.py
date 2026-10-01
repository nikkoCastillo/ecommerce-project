# This module manages products in the ecommerce system

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps
from decimal import Decimal, InvalidOperation

from app.db import get_db_connection

products_bp = Blueprint("products", __name__)


# Helper function to parse and validate product form data
def parse_product_form():
    """Validate and normalize product fields before writing to SQL Server."""
    name = (request.form.get("name") or "").strip()
    category = (request.form.get("category") or "").strip()
    raw_price = (request.form.get("price") or "").strip()

    if not name or len(name) > 120:
        return None

    if not category or len(category) > 80:
        return None

    try:
        price = Decimal(raw_price)
        if (
            not price.is_finite()
            or price <= 0
            or price > Decimal("99999999.99")
            or price != price.quantize(Decimal("0.01"))
        ):
            return None
    except InvalidOperation:
        return None

    return name, category, price


def admin_required(func):
    """
    Make sure only admin users can access product management features.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not getattr(
            current_user, "is_admin", False
        ):
            flash("Admin access required.")
            return redirect(url_for("auth.login"))
        return func(*args, **kwargs)

    return wrapper


@products_bp.route("/products")
@login_required
def index():
    """
    Show all active products.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT ProductID, Name, Category, Price, IsActive
            FROM dbo.Products
            WHERE IsActive = 1
            ORDER BY Name
            """)

        products = cursor.fetchall()
        conn.close()

        return render_template("products.html", products=products)

    except Exception:
        flash("Unable to load products right now.")
        return "Unable to load products right now.", 500


@products_bp.route("/products/add", methods=["GET", "POST"])
@login_required
@admin_required
def add_product():
    """
    Add a new product.
    """
    if request.method == "POST":

        product_data = parse_product_form()
        if product_data is None:
            flash(
                "Enter a name up to 120 characters, a category up to 80 characters, and a positive price with at most two decimal places."
            )
            return redirect(url_for("products.add_product"))
        name, category, price = product_data

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO dbo.Products (Name, Category, Price, IsActive)
                VALUES (?, ?, ?, 1)
                """,
                (name, category, price),
            )
            conn.commit()
            conn.close()

            flash("Product added successfully.")
            return redirect(url_for("products.index"))

        except Exception:
            flash("Something went wrong while adding the product.")
            return redirect(url_for("products.add_product"))

    return render_template(
        "product_form.html",
        product=None,
        page_title="Add product",
        form_action=url_for("products.add_product"),
    )


@products_bp.route("/products/edit/<int:product_id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_product(product_id):
    """
    Edit an existing product.
    """
    if request.method == "POST":
        product_data = parse_product_form()
        if product_data is None:
            flash(
                "Enter a name up to 120 characters, a category up to 80 characters, "
                "and a positive price with at most two decimal places."
            )
            return redirect(url_for("products.edit_product", product_id=product_id))

        name, category, price = product_data

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE dbo.Products
                SET Name = ?, Category = ?, Price = ?
                WHERE ProductID = ?
                """,
                (name, category, price, product_id),
            )
            conn.commit()
            conn.close()

            flash("Product updated successfully.")
            return redirect(url_for("products.index"))

        except Exception:
            flash("Something went wrong while updating the product.")
            return redirect(url_for("products.edit_product", product_id=product_id))

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT ProductID, Name, Category, Price
            FROM dbo.Products
            WHERE ProductID = ? AND IsActive = 1
            """,
            (product_id,),
        )
        product = cursor.fetchone()
        conn.close()

        if product is None:
            flash("Product not found or inactive.")
            return redirect(url_for("products.index"))

        return render_template(
            "product_form.html",
            product=product,
            page_title="Edit product",
            form_action=url_for(
                "products.edit_product",
                product_id=product_id,
            ),
        )
    except Exception:
        flash("Unable to load this product for editing.")
        return redirect(url_for("products.index"))


@products_bp.route("/products/delete/<int:product_id>", methods=["POST"])
@login_required
@admin_required
def delete_product(product_id):
    """
    Soft delete a product by marking it inactive.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE dbo.Products
            SET IsActive = 0
            WHERE ProductID = ?
            """,
            (product_id,),
        )
        conn.commit()
        conn.close()

        flash("Product deleted successfully.")
        return redirect(url_for("products.index"))

    except Exception:
        flash("Something went wrong while deleting the product.")
        return redirect(url_for("products.index"))
