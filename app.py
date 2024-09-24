# app.py
import streamlit as st
import pandas as pd
from database import setup_database, execute_query
from openai_integration import natural_language_to_sql

# Customizing the app layout
st.set_page_config(
    page_title="FinQuery",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

def apply_custom_styles():
    st.markdown(
        """
        <style>
        
       
        h1 {
            color: #4CAF50;
            text-align: center;
            font-family: 'Helvetica', sans-serif;
        }

        /* Sidebar styling */
        .sidebar .sidebar-content {
            background-color: #ffffff;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #dddddd;
        }
        
        /* Table styling */
        .dataframe {
            border: 1px solid #ddd;
            border-collapse: collapse;
            width: 100%;
            margin: 25px 0;
        }

        .dataframe th, .dataframe td {
            padding: 10px;
            text-align: center;
            border: 1px solid #ddd;
        }
        </style>
        """, 
        unsafe_allow_html=True
    )

def main():
    apply_custom_styles()
    
    # Sidebar info and branding
    # st.sidebar.image("https://image.shutterstock.com/image-vector/finance-data-analytics-icon-fintech-260nw-1959821145.jpg", use_column_width=True)
    st.sidebar.title("FinQuery 💰")
    st.sidebar.write("Welcome to FinQuery! Your intelligent assistant for querying financial data. Ask natural language questions and explore financial insights effortlessly.")

    # Initialize database setup
    setup_database()

    # Main title
    st.title("💰 FinQuery - Financial Data Insights 💼")

    # User input section
    st.subheader("Ask a question about the financial data:")
    user_input = st.text_input("Enter your query here", placeholder="E.g., What was the highest stock price for TechCorp in 2022?", help="Type any question about the financial data.")

    if user_input:
        with st.spinner("Processing your query..."):
            try:
                # Convert natural language to SQL
                sql_query = natural_language_to_sql(user_input)
                
                # Display the generated SQL
                st.markdown("### 🛠️ Generated SQL Query")
                st.code(sql_query, language="sql")

                # Execute the query
                columns, results = execute_query(sql_query)

                # Display the results
                if results:
                    st.success("✅ Query executed successfully! Here are your results:")
                    df = pd.DataFrame(results, columns=columns)
                    st.dataframe(df)
                else:
                    st.warning("⚠️ No results found for your query.")
            except Exception as e:
                st.error(f"An error occurred while processing your query: {str(e)}")

    # Footer
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<center>Built with ❤️ by [Akshika]</center>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
