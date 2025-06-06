import sqlite3

DB_NAME = "bookmakers.db"

def connect_to_db():
    conn = sqlite3.connect(DB_NAME)
    return conn, conn.cursor()

def create_table():
    conn, cursor = connect_to_db()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookmakers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bookmaker_name TEXT,
            country TEXT,
            products TEXT,
            licensing TEXT,
            affiliates TEXT,
            customer_base TEXT,
            employees TEXT,
            revenue_estimate TEXT,
            security_certifications TEXT,
            source_url TEXT
        );
    """)
    conn.commit()
    conn.close()

def insert_bookmaker(data):
    conn, cursor = connect_to_db()
    cursor.execute("""
        INSERT INTO bookmakers (
            bookmaker_name,
            country,
            products,
            licensing,
            affiliates,
            customer_base,
            employees,
            revenue_estimate,
            security_certifications,
            source_url
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get("bookmaker_name"),
        data.get("country"),
        ", ".join(data.get("products", [])) if data.get("products") else None,
        ", ".join(data.get("licensing", [])) if data.get("licensing") else None,
        data.get("affiliates"),
        data.get("customer_base"),
        data.get("employees"),
        data.get("revenue_estimate"),
        data.get("security_certifications"),
        data.get("source_url")
    ))
    conn.commit()
    conn.close()