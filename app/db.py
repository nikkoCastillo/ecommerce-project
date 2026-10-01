# This file is used by the app to connect to EcommerceDemo

import os
import pyodbc
from dotenv import load_dotenv

# Load environment variables from the local .env file
load_dotenv()


def get_db_connection():
    """
    Create and return a SQL Server connection using
    the values defined in the .env file.
    """
    try:
        server = os.getenv("SQL_SERVER")
        database = os.getenv("SQL_DATABASE")
        driver = os.getenv("SQL_DRIVER")

        if not server or not database or not driver:
            raise ValueError("Missing SQL Server environment variables.")

        connection_string = (
            f"DRIVER={{{driver}}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            "Trusted_Connection=yes;"
        )

        return pyodbc.connect(connection_string)

    except Exception as e:
        print(f"Error connecting to the database: {e}")
        raise
