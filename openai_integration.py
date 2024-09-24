# openai_integration.py
import openai
from config import OPENAI_API_KEY

# Set up OpenAI API key
openai.api_key = OPENAI_API_KEY

def natural_language_to_sql(query: str) -> str:
    """Convert natural language query to SQL using OpenAI API, with improved handling for ambiguous queries."""
    
    schema_info = """
    The database schema is as follows:

    Table: companies
        - company_id (Primary Key)
        - name (Text): The name of the company
        - industry (Text): The industry sector of the company
        - founded_year (Integer): The year the company was founded
    
    Table: financial_statements
        - statement_id (Primary Key)
        - company_id (Foreign Key to companies.company_id)
        - year (Integer): The fiscal year
        - quarter (Integer): The fiscal quarter (1 to 4)
        - revenue (Real): Total revenue for the quarter
        - expenses (Real): Total expenses for the quarter
        - net_income (Real): Net income for the quarter
        - assets (Real): Total assets at the end of the quarter
        - liabilities (Real): Total liabilities at the end of the quarter
        - equity (Real): Total equity at the end of the quarter

    Table: stock_prices
        - price_id (Primary Key)
        - company_id (Foreign Key to companies.company_id)
        - date (Text in YYYY-MM-DD format): The date of the stock price
        - open_price (Real): The opening price of the stock on that date
        - close_price (Real): The closing price of the stock on that date
        - high_price (Real): The highest price of the stock on that date
        - low_price (Real): The lowest price of the stock on that date
        - volume (Integer): The volume of shares traded on that date
    
    When converting the natural language query, please handle any ambiguity by making reasonable assumptions, and include comments in the SQL query explaining your interpretation. If the query is ambiguous or could be interpreted in multiple ways, provide the most common interpretation.

    Here are some example natural language queries and their expected SQL outputs:
    
    Example 1:
    Natural Language: "Show me the total revenue for TechCorp in 2022."
    SQL: 
    -- Retrieving total revenue for TechCorp in 2022
    SELECT SUM(revenue) AS total_revenue
    FROM financial_statements
    JOIN companies ON financial_statements.company_id = companies.company_id
    WHERE companies.name = 'TechCorp' AND year = 2022;

    Example 2:
    Natural Language: "What was the highest stock price for FinanceCo in December 2022?"
    SQL: 
    -- Fetching the highest stock price for FinanceCo in December 2022
    SELECT MAX(high_price) AS highest_price
    FROM stock_prices
    JOIN companies ON stock_prices.company_id = companies.company_id
    WHERE companies.name = 'FinanceCo' AND date BETWEEN '2022-12-01' AND '2022-12-31';
    
    Please convert the following query:
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a SQL expert with deep knowledge of handling complex and ambiguous queries. Give me only the SQL query"},
            {"role": "user", "content": f"{schema_info} {query}"}
        ],
        temperature=0.2  # Lower temperature for more deterministic responses
    )
    
    return response.choices[0].message.content
