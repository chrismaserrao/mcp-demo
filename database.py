import sqlite3
import pandas as pd

DB_NAME = "finance.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            date TEXT,
            description TEXT,
            amount REAL,
            transaction_type TEXT,
            category TEXT,
            account_name TEXT
        )
    """)

    conn.commit()
    conn.close()


def insert_transaction(user_id, date, description, amount, transaction_type, category, account_name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO transactions 
        (user_id, date, description, amount, transaction_type, category, account_name)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (user_id, date, description, amount, transaction_type, category, account_name))

    conn.commit()
    conn.close()


def get_transactions_df(user_id):
    conn = sqlite3.connect(DB_NAME)

    df = pd.read_sql_query(
        "SELECT * FROM transactions WHERE user_id = ?",
        conn,
        params=(user_id,)
    )

    conn.close()
    return df
