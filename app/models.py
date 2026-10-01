# This file represents each user in the database

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin):
    """
    A user object used by Flask-Login.
    It stores the user information needed for the session.
    """

    # The constructor initializes the User object with the provided user_id, email, password_hash, and is_admin flag.
    def __init__(self, user_id, email, password_hash, is_admin=False):
        self.id = user_id
        self.email = email
        self.password_hash = password_hash
        self.is_admin = is_admin

    # The create_hash method is a static method that takes a plain-text password as input and returns its hashed version using the generate_password_hash function from Werkzeug. This is used to securely store passwords in the database.
    @staticmethod
    def create_hash(password):
        """
        Hash the plain-text password before saving to SQL Server.
        """
        return generate_password_hash(password)

    # The verify_hash method is a static method that takes a plain-text password and a stored password hash as input. It compares the two using the check_password_hash function from Werkzeug and returns True if they match, indicating that the provided password is correct, or False otherwise.
    @staticmethod
    def verify_hash(password, password_hash):
        """
        Compare a plain password to the stored password hash.
        """
        return check_password_hash(password_hash, password)

    # The get_id method is an instance method that returns the user's ID as a string. This is required by Flask-Login to uniquely identify the user during the session.
    def get_id(self):
        return str(self.id)
