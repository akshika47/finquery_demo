import streamlit as st
import sqlite3
import pandas as pd
import openai
from typing import List, Tuple

# Set up OpenAI API key
openai.api_key = "your-openai-api-key-here"

# Create a connection to the SQLite database
conn = sqlite3.connect("financial_data.db")
cursor = conn.cursor()
# Establishing a new connection when needed
def execute_query(sql: str) -> Tuple[List[str], List[Tuple]]:
    """Execute SQL query and return column names and results"""
    with sqlite3.connect("financial_data.db") as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        columns = [description[0] for description in cursor.description]
        results = cursor.fetchall()
    return columns, results

def setup_database():
    with sqlite3.connect("financial_data.db") as conn:
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
            insert_data_sql = """
            INSERT INTO companies (name, industry, founded_year) VALUES
            ('TechCorp', 'Technology', 1990),
            ('FinanceCo', 'Finance', 1985),
            ('EnergyInc', 'Energy', 1970),
            ('RetailGiant', 'Retail', 1995);

            INSERT INTO financial_statements (company_id, year, quarter, revenue, expenses, net_income, assets, liabilities, equity) VALUES
            (1, 2022, 1, 1000000, 800000, 200000, 5000000, 2000000, 3000000),
            (1, 2022, 2, 1100000, 850000, 250000, 5200000, 2100000, 3100000),
            (1, 2022, 3, 1050000, 820000, 230000, 5300000, 2150000, 3150000),
            (1, 2022, 4, 1200000, 900000, 300000, 5500000, 2200000, 3300000),
            (2, 2022, 1, 800000, 600000, 200000, 10000000, 8000000, 2000000),
            (2, 2022, 2, 850000, 620000, 230000, 10500000, 8300000, 2200000),
            (2, 2022, 3, 900000, 650000, 250000, 11000000, 8600000, 2400000),
            (2, 2022, 4, 950000, 680000, 270000, 11500000, 8900000, 2600000),
            (3, 2022, 1, 1500000, 1200000, 300000, 8000000, 5000000, 3000000),
            (3, 2022, 2, 1600000, 1250000, 350000, 8200000, 5100000, 3100000),
            (3, 2022, 3, 1550000, 1220000, 330000, 8300000, 5150000, 3150000),
            (3, 2022, 4, 1700000, 1300000, 400000, 8500000, 5200000, 3300000),
            (4, 2022, 1, 2000000, 1800000, 200000, 6000000, 4000000, 2000000),
            (4, 2022, 2, 2100000, 1900000, 200000, 6200000, 4100000, 2100000),
            (4, 2022, 3, 2050000, 1850000, 200000, 6300000, 4150000, 2150000),
            (4, 2022, 4, 2200000, 1950000, 250000, 6500000, 4200000, 2300000);

            INSERT INTO stock_prices (company_id, date, open_price, close_price, high_price, low_price, volume) VALUES
            (1, '2022-12-30', 150.00, 152.50, 153.00, 149.50, 1000000),
            (1, '2022-12-29', 148.50, 150.00, 151.00, 148.00, 950000),
            (2, '2022-12-30', 80.00, 81.25, 81.50, 79.75, 500000),
            (2, '2022-12-29', 79.50, 80.00, 80.50, 79.00, 480000),
            (3, '2022-12-30', 65.00, 66.50, 67.00, 64.75, 750000),
            (3, '2022-12-29', 64.50, 65.00, 65.50, 64.00, 720000),
            (4, '2022-12-30', 45.00, 46.25, 46.50, 44.75, 1200000),
            (4, '2022-12-29', 44.50, 45.00, 45.50, 44.00, 1150000);
            """
            cursor.executescript(insert_data_sql)
            conn.commit()


# Create a sample table with dummy data
cursor.execute("""
CREATE TABLE IF NOT EXISTS financial_data (
    date TEXT,
    company TEXT,
    revenue REAL,
    profit REAL
)
""")

# Insert some dummy data
dummy_data = [
    ("2023-01-01", "TechCorp", 1000000, 200000),
    ("2023-01-01", "FinanceCo", 800000, 150000),
    ("2023-02-01", "TechCorp", 1100000, 220000),
    ("2023-02-01", "FinanceCo", 850000, 160000),
]

cursor.executemany("INSERT INTO financial_data VALUES (?, ?, ?, ?)", dummy_data)
conn.commit()

def natural_language_to_sql(query: str) -> str:
    """Convert natural language query to SQL using OpenAI API"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a SQL expert. Convert the following natural language query to SQL. The query is for a table named 'financial_data' with columns: date, company, revenue, profit."},
            {"role": "user", "content": query}
        ]
    )
    return response.choices[0].message.content

def execute_query(sql: str) -> Tuple[List[str], List[Tuple]]:
    """Execute SQL query and return column names and results"""
    cursor.execute(sql)
    columns = [description[0] for description in cursor.description]
    results = cursor.fetchall()
    return columns, results

def main():
    st.title("Financial Data Chat")

    # Chat input
    user_input = st.text_input("Ask a question about the financial data:")

    if user_input:
        try:
            # Convert natural language to SQL
            sql_query = natural_language_to_sql(user_input)
            st.text(f"Generated SQL: {sql_query}")

            # Execute the query
            columns, results = execute_query(sql_query)

            # Display the results
            if results:
                df = pd.DataFrame(results, columns=columns)
                st.dataframe(df)
            else:
                st.write("No results found.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()

# Close the database connection when the app is done
conn.close()