# app.py
import streamlit as st
import pandas as pd
from database import setup_database, execute_query
from openai_integration import natural_language_to_sql

def main():
    st.title("Financial Data Chat")
    
    # Initialize database setup
    setup_database()

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
