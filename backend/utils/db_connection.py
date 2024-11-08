import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def get_db_connection():
    """Establishes and returns a database connection."""
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=os.getenv("DB_PORT"),
            # ssl_disabled=False
        )
        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None

def create_user_table(connection):
    """Creates the users table if it does not already exist."""
    cursor = connection.cursor()
    try:
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        password_hash VARCHAR(255) NOT NULL,
        free_api_calls_remaining INT DEFAULT 20,
        total_api_calls INT DEFAULT 0,
        is_admin BOOLEAN DEFAULT FALSE
        )
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("User table created")
    except Error as e:
        print("Error creating table", e)
        return None
    finally:
        cursor.close() 

def insert_user(connection, first_name, email, password_hash):
    """Inserts a new user into the users table."""
    cursor = connection.cursor()
    try:
        insert_user_query = """
        INSERT INTO users (first_name, email, password_hash) VALUES (%s, %s, %s)
        """
        cursor.execute(insert_user_query, (first_name, email, password_hash))
        connection.commit()
        print("User inserted successfully.")
    except Error as e:
        print("Error inserting user", e)
        connection.rollback()
    finally:
        cursor.close() 

def get_user_by_email(connection, email):
    """Retrieve a user from the database by email."""
    cursor = connection.cursor(dictionary=True)
    try:
        select_query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(select_query, (email,))
        user = cursor.fetchone()
        return user
    except Error as e:
        print("Error retrieving user by email:", e)
        return None
    finally:
        cursor.close()

def update_user_password(connection, email, hashed_password):
    """Updates user password"""
    cursor = connection.cursor()
    try:
        update_query = """
        UPDATE users SET password_hash = %s WHERE email = %s
        """
        cursor.execute(update_query,(hashed_password, email))
        connection.commit()
    except Error as e:
        print("Error updating user password:", e)
        connection.rollback()
    finally:
        cursor.close()

def close_db_connection(connection):
    """Closes the database connection."""
    if connection.is_connected():
        connection.close()
        print("MySQL connection closed")
