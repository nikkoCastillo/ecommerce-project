# This file initializes the app and login system

import os

from dotenv import load_dotenv
from flask_wtf.csrf import CSRFProtect

load_dotenv()

csrf = CSRFProtect()

# Load environment variables from the local .env file
from flask import Flask
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = "auth.login"


def create_app():
    """
    Create the Flask application instance and register all blueprints.
    """
    app = Flask(__name__)
    secret_key = os.getenv("SECRET_KEY")
    if not secret_key or secret_key == "replace-this-placeholder":
        raise RuntimeError("Set a non-placeholder SECRET_KEY in your .env file.")

    app.config["SECRET_KEY"] = secret_key
    csrf.init_app(app)

    login_manager.init_app(app)

    # Import blueprints only when the app is created
    # This keeps the app structure flexible and avoids import issues
    from .auth import auth_bp
    from .products import products_bp
    from .orders import orders_bp
    from .dashboard import dashboard_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(dashboard_bp)

    # Flask-Login user loader function
    @login_manager.user_loader
    def load_user(user_id):
        """
        Flask-Login loads the current user from the user ID stored in session.
        """
        from .auth import get_user_by_id

        return get_user_by_id(user_id)

    # Error handlers for common HTTP errors
    @app.errorhandler(404)
    def page_not_found(error):
        return "Page not found", 404

    @app.errorhandler(500)
    def server_error(error):
        return "Internal server error", 500

    return app
