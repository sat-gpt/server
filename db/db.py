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
            r_hash VARCHAR(64) PRIMARY KEY,
            query TEXT,
            used BOOLEAN NOT NULL DEFAULT FALSE
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


# Add the r_hash and query to the database
def add_r_hash_and_query(r_hash, query):
    connection = connect_to_database()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    insert_query = """
        INSERT INTO invoices (r_hash, query) VALUES (%(r_hash)s, %(query)s)
    """
    cursor.execute(insert_query, {"r_hash": r_hash, "query": query})
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
