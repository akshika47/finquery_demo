# database.py
import sqlite3
from typing import List, Tuple
import os

from config import DATABASE_PATH

def create_connection():
    return sqlite3.connect(DATABASE_PATH)

def setup_database():
    with create_connection() as conn:
        cursor = conn.cursor()
        # SQL commands to create tables
        create_tables_sql = """
        CREATE TABLE IF NOT EXISTS companies (
            company_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            industry TEXT NOT NULL,
            founded_year INTEGER
        );

        CREATE TABLE IF NOT EXISTS financial_statements (
            statement_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER,
            year INTEGER,
            quarter INTEGER,
            revenue REAL,
            expenses REAL,
            net_income REAL,
            assets REAL,
            liabilities REAL,
            equity REAL,
            FOREIGN KEY (company_id) REFERENCES companies(company_id)
        );

        CREATE TABLE IF NOT EXISTS stock_prices (
            price_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER,
            date TEXT,
            open_price REAL,
            close_price REAL,
            high_price REAL,
            low_price REAL,
            volume INTEGER,
            FOREIGN KEY (company_id) REFERENCES companies(company_id)
        );
        """
        
        cursor.executescript(create_tables_sql)
        conn.commit()

        # Insert sample data only if the tables are empty
        cursor.execute("SELECT COUNT(*) FROM companies")
        if cursor.fetchone()[0] == 0:
            # Insert sample data into the tables
            insert_data_sql = """
            INSERT INTO companies (name, industry, founded_year) VALUES
            ('TechCorp', 'Technology', 1990),
            ('FinanceCo', 'Finance', 1985),
            ('EnergyInc', 'Energy', 1970),
            ('RetailGiant', 'Retail', 1995);

            INSERT INTO financial_statements (company_id, year, quarter, revenue, expenses, net_income, assets, liabilities, equity) VALUES
            (1, 2022, 1, 1000000, 800000, 200000, 5000000, 2000000, 3000000),
            -- Additional insertions...
            """

            cursor.executescript(insert_data_sql)
            conn.commit()

def execute_query(sql: str) -> Tuple[List[str], List[Tuple]]:
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        columns = [description[0] for description in cursor.description]
        results = cursor.fetchall()
    return columns, results
