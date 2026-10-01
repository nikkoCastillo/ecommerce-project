# This file handles all authentication for the app

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

from app.db import get_db_connection
from app.models import User

# Create a Blueprint for the authentication routes
auth_bp = Blueprint("auth", __name__)


# Flask-Login user loader function
# This function is used by Flask-Login to load the current user from the session.
def get_user_by_id(user_id):
    """
    Get one user by ID from SQL Server.
    This is required by Flask-Login so the session can restore the current user.
    """

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT UserID, Email, PasswordHash, IsAdmin
            FROM dbo.Users
            WHERE UserID = ?
            """,
            (user_id,),
        )

        row = cursor.fetchone()
        conn.close()

        if row is None:
            return None

        return User(row[0], row[1], row[2], bool(row[3]))
    except Exception:
        return None


# Route for user registration
# This route allows new users to create an account. It checks if the email is already registered and hashes the password before storing it in the database.
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """
    Create a new user account.
    """
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        if not email or not password:
            flash("Email and password are required.")
            return redirect(url_for("auth.register"))

        try:
            if not email or not password:
                flash("Email and password are required.")
                return redirect(url_for("auth.register"))

            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM dbo.Users WHERE Email = ?", (email,))
            exists = cursor.fetchone()[0]

            if exists > 0:
                conn.close()
                flash("This email is already registered.")
                return redirect(url_for("auth.register"))

            hashed_password = User.create_hash(password)

            cursor.execute(
                """
                INSERT INTO dbo.Users (Email, PasswordHash, IsAdmin, CreatedAt)
                VALUES (?, ?, 0, GETDATE())
                """,
                (email, hashed_password),
            )

            conn.commit()
            conn.close()

            flash("Registration successful. Please log in.")
            return redirect(url_for("auth.login"))

        except Exception:
            flash(f"Something went wrong while registering. Please try again.")
            return redirect(url_for("auth.register"))

    return render_template("register.html")


# Route for user login
# This route allows existing users to log in. It verifies the email and password against the database and starts a session if the credentials are valid.
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Log in a user and start a session.
    """
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        if not email or not password:
            flash("Email and password are required.")
            return redirect(url_for("auth.login"))

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT UserID, Email, PasswordHash, IsAdmin
                FROM dbo.Users
                WHERE Email = ?
                """,
                (email,),
            )

            row = cursor.fetchone()
            conn.close()

            if row is None:
                flash("Invalid email or password.")
                return redirect(url_for("auth.login"))

            user = User(row[0], row[1], row[2], bool(row[3]))

            if User.verify_hash(password, user.password_hash):
                login_user(user)
                return redirect(url_for("products.index"))

            flash("Invalid email or password.")
            return redirect(url_for("auth.login"))

        except Exception:
            flash(f"Something went wrong while logging in. Please try again.")
            return redirect(url_for("auth.login"))

    return render_template("login.html")


# Route for user logout
# This route logs the user out and ends the session. It requires the user to be logged in to access it, and it redirects them to the login page after logging out.
@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    """
    Log the current user out and end the session.
    """
    try:
        logout_user()
        flash("You have been logged out.")
        return redirect(url_for("auth.login"))
    except Exception:
        flash("Something went wrong while logging out.")
        return redirect(url_for("auth.login"))
