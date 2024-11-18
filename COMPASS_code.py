import openai
import sys
import streamlit as st
from chromadb import PersistentClient
import pandas as pd
from docx import Document
import os

# Ensure SQLite compatibility
try:
    __import__('pysqlite3')
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
    st.write("pysqlite3 successfully imported.")
except ImportError:
    st.write("pysqlite3 not available, falling back to sqlite3.")

# Check OpenAI API Key in secrets
if not hasattr(st, "secrets") or "OpenAI_key" not in st.secrets:
    st.error("Missing OpenAI API key in Streamlit secrets. Please configure it.")
    st.stop()
else:
    st.write("OpenAI API key found.")

# Set OpenAI API Key
try:
    openai.api_key = st.secrets["OpenAI_key"]
    st.write("OpenAI API key initialized.")
except Exception as e:
    st.error(f"Error initializing OpenAI API key: {e}")
    st.stop()

# Initialize ChromaDB client
try:
    client = PersistentClient(path="knowledge_base")
    st.write("ChromaDB Client Initialized.")
except Exception as e:
    st.error(f"Error initializing ChromaDB Client: {e}")
    st.stop()

# Verify required files
file_paths = {
    "UNI_DATA": "/workspaces/IST688_COMPASS_Project/uni100.docx",
    "JOB_MARKET": "/workspaces/IST688_COMPASS_Project/Employment Projections.csv",
    "LIVING_EXPENSES": "/workspaces/IST688_COMPASS_Project/avglivingexpenses.csv"
}

for name, path in file_paths.items():
    if not os.path.exists(path):
        st.error(f"File not found: {name} at {path}")
        st.stop()
    else:
        st.write(f"{name} file found: {path}")

# Chatbot interface
def main():
    # Debugging log to confirm main() execution
    st.write("Main function started...")

    # Display chatbot UI
    st.title("University Recommendation Chatbot")
    st.markdown("### Get personalized recommendations!")

    # Input box and button
    user_input = st.text_input("Enter your preferences (e.g., 'I want a university in California for AI'):")
    if st.button("Send"):
        st.write(f"You entered: {user_input}")

        # Mock response to simulate chatbot functionality
        st.write("Processing your request...")
        st.write("**Mock Response:**")
        st.write("**University Recommendations:** Stanford, MIT, UC Berkeley")
        st.write("**Job Market Trends:** Software Engineer, Data Scientist")
        st.write("**Living Expenses:** California: High, Texas: Medium")

    # Debugging log to confirm the end of main()
    st.write("Main function execution completed.")

if __name__ == "__main__":
    # Debugging log for script entry point
    st.write("Initializing the Streamlit app...")

    # Load all data (mock for now)
    st.write("All initialization steps completed successfully.")
    main()