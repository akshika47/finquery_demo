# openai_integration.py
import openai
from config import OPENAI_API_KEY

# Set up OpenAI API key
openai.api_key = OPENAI_API_KEY

def natural_language_to_sql(query: str) -> str:
    """Convert natural language query to SQL using OpenAI API"""
    schema_info = """
    The database has the following schema:
    
    companies (company_id, name, industry, founded_year)
    financial_statements (statement_id, company_id, year, quarter, revenue, expenses, net_income, assets, liabilities, equity)
    stock_prices (price_id, company_id, date, open_price, close_price, high_price, low_price, volume)
    
    companies.company_id is a foreign key in both financial_statements and stock_prices.
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are a SQL expert. Convert the following natural language query to SQL. {schema_info}"},
            {"role": "user", "content": query}
        ]
    )
    return response.choices[0].message.content