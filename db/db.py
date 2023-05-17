import os
import psycopg2
import psycopg2.extras

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")


# Connect to the PostgreSQL database
def connect_to_database():
    connection = psycopg2.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT,
    )
    return connection


# Create the database table
def create_invoices_table():
    connection = connect_to_database()
    cursor = connection.cursor()

    create_table_query = """
        CREATE TABLE invoices (
            user_uuid VARCHAR(64),
            r_hash VARCHAR(64) PRIMARY KEY,
            query TEXT,
            used BOOLEAN NOT NULL DEFAULT FALSE
        );
    """

    cursor.execute(create_table_query)
    connection.commit()

    cursor.close()
    connection.close()

# Create users table
def create_users_table():
    connection = connect_to_database()
    cursor = connection.cursor()

    create_table_query = """
        CREATE TABLE users (
            user_uuid VARCHAR(64) PRIMARY KEY
            credit_satoshis INT NOT NULL DEFAULT 0
        );
    """

    cursor.execute(create_table_query)
    connection.commit()

    cursor.close()
    connection.close()


# Set 'used' to True if r_hash matches any value in the database
def set_invoice_used(r_hash):
    connection = connect_to_database()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    select_query = """
        SELECT r_hash FROM invoices WHERE r_hash = %(r_hash)s
    """
    cursor.execute(select_query, {"r_hash": r_hash})

    if cursor.rowcount > 0:
        update_query = """
            UPDATE invoices SET used = TRUE WHERE r_hash = %(r_hash)s
        """
        cursor.execute(update_query, {"r_hash": r_hash})
        connection.commit()

    cursor.close()
    connection.close()


def check_invoice_used(r_hash):
    connection = connect_to_database()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:
        select_query = """
            SELECT used FROM invoices WHERE r_hash = %(r_hash)s
        """
        cursor.execute(select_query, {"r_hash": r_hash})

        if cursor.rowcount > 0:
            result = cursor.fetchone()
            used = result["used"]
            return used

    finally:
        cursor.close()
        connection.close()


# Add the r_hash and query, and the user_uuid to the database
def add_r_hash_and_query(r_hash, query, user_uuid):
    connection = connect_to_database()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    insert_query = """
        INSERT INTO invoices (r_hash, query, user_uuid) VALUES (%(r_hash)s, %(query)s, %(user_uuid)s)
    """
    cursor.execute(insert_query, {"r_hash": r_hash, "query": query, "user_uuid": user_uuid})
    connection.commit()

    cursor.close()
    connection.close()

    return r_hash


# Get query associated with r_hash
def lookup_query(r_hash):
    connection = connect_to_database()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:
        select_query = """
            SELECT query FROM invoices WHERE r_hash = %(r_hash)s
        """
        cursor.execute(select_query, {"r_hash": r_hash})

        if cursor.rowcount > 0:
            result = cursor.fetchone()
            query = result["query"]
            return query

    finally:
        cursor.close()
        connection.close()

# Add user by their uuid to database
def add_user_uuid(user_uuid):
    connection = connect_to_database()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    insert_query = """
        INSERT INTO users (user_uuid, credit_satoshis) VALUES (%(user_uuid)s, 0)
    """
    cursor.execute(insert_query, {"user_uuid": user_uuid})
    connection.commit()

    cursor.close()
    connection.close()

    return user_uuid

# Get user_uuid by r_hash:
def lookup_user_by_r_hash(r_hash):
    connection = connect_to_database()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:
        select_query = """
            SELECT user_uuid FROM invoices WHERE r_hash = %(r_hash)s
        """
        cursor.execute(select_query, {"r_hash": r_hash})

        if cursor.rowcount > 0:
            result = cursor.fetchone()
            user_uuid = result["user_uuid"]
            return user_uuid

    finally:
        cursor.close()
        connection.close()

# Get user credit_satoshis
def lookup_user_credit(user_uuid):
    connection = connect_to_database()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:
        select_query = """
            SELECT credit_satoshis FROM users WHERE user_uuid = %(user_uuid)s
        """
        cursor.execute(select_query, {"user_uuid": user_uuid})

        if cursor.rowcount > 0:
            result = cursor.fetchone()
            credit_satoshis = result["credit_satoshis"]
            return credit_satoshis

    except Exception as e:
        print(e)
        raise e

    finally:
        cursor.close()
        connection.close()

# Add credit_satoshis to user
def set_user_credit(user_uuid, credit_satoshis, deduct=False):
    connection = connect_to_database()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:
        if deduct:
            select_query = """
                UPDATE users SET credit_satoshis = credit_satoshis - %(credit_satoshis)s WHERE user_uuid = %(user_uuid)s
            """
        else :
            select_query = """
                UPDATE users SET credit_satoshis = %(credit_satoshis)s WHERE user_uuid = %(user_uuid)s
            """
        cursor.execute(select_query, {"user_uuid": user_uuid, "credit_satoshis": credit_satoshis})

        if cursor.rowcount > 0:
            result = cursor.fetchone()
            credit_satoshis = result["credit_satoshis"]
            return credit_satoshis

    finally:
        cursor.close()
        connection.close()