import openai
import sys
import streamlit as st
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

# File paths
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

# Load UNI_DATA
def load_university_data(file_path):
    try:
        doc = Document(file_path)
        universities = [p.text for p in doc.paragraphs if p.text.strip()]
        st.write(f"Loaded {len(universities)} universities.")
        return universities
    except Exception as e:
        st.error(f"Error loading university data: {e}")
        return []

# Load JOB_MARKET data
def load_job_market_data(file_path):
    try:
        job_market = pd.read_csv(file_path)
        st.write(f"Loaded {len(job_market)} job market records.")
        return job_market
    except Exception as e:
        st.error(f"Error loading job market data: {e}")
        return pd.DataFrame()

# Load LIVING_EXPENSES data
def load_living_expenses_data(file_path):
    try:
        living_expenses = pd.read_csv(file_path)
        st.write(f"Loaded {len(living_expenses)} living expense records.")
        return living_expenses
    except Exception as e:
        st.error(f"Error loading living expenses data: {e}")
        return pd.DataFrame()

# Generate chatbot response
def generate_response(location, budget, field_of_study, universities, job_market, living_expenses):
    response = ""

    # Filter universities based on location (mock logic; adjust as per actual data structure)
    matching_universities = [uni for uni in universities if location.lower() in uni.lower()]
    response += "**University Recommendations:**\n"
    if matching_universities:
        response += "\n".join(matching_universities[:5]) + "\n\n"  # Top 5 matches
    else:
        response += "No universities found for the given location.\n\n"

    # Filter job market based on location and field of study
    matching_jobs = job_market[job_market["Occupation Title"].str.contains(field_of_study, case=False, na=False)]
    response += "**Job Market Trends:**\n"
    if not matching_jobs.empty:
        response += ", ".join(matching_jobs["Occupation Title"].head(5)) + "\n\n"  # Top 5 matches
    else:
        response += "No job market trends found for the given field of study.\n\n"

    # Filter living expenses based on location
    matching_expenses = living_expenses[living_expenses["State"].str.contains(location, case=False, na=False)]
    response += "**Living Expenses:**\n"
    if not matching_expenses.empty:
        for _, row in matching_expenses.head(5).iterrows():
            response += f"- {row['State']}: ${row['Index']}\n"
    else:
        response += "No living expense data found for the given location.\n"

    # Add budget information
    response += f"\n**Budget:** ${budget} (provided by user)\n"
    
    return response

# Main chatbot interface
def main():
    st.title("University Recommendation Chatbot")
    st.markdown("### Get detailed recommendations based on location, budget, and field of study!")

    # Load datasets
    universities = load_university_data(file_paths["UNI_DATA"])
    job_market = load_job_market_data(file_paths["JOB_MARKET"])
    living_expenses = load_living_expenses_data(file_paths["LIVING_EXPENSES"])

    # User inputs
    location = st.text_input("Enter your preferred location (e.g., California):")
    budget = st.number_input("Enter your budget (in USD):", min_value=0)
    field_of_study = st.text_input("Enter your field of study (e.g., Data Science):")

    if st.button("Send"):
        if location.strip() and budget > 0 and field_of_study.strip():
            response = generate_response(location, budget, field_of_study, universities, job_market, living_expenses)
            st.write("**You:**")
            st.write(f"- Location: {location}")
            st.write(f"- Budget: ${budget}")
            st.write(f"- Field of Study: {field_of_study}")
            st.write("**Bot:**")
            st.write(response)
        else:
            st.warning("Please provide all the required inputs before clicking Send.")

if __name__ == "__main__":
    main()
