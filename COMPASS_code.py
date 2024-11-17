import openai
import sys
import streamlit as st
from chromadb import PersistentClient
import pandas as pd
from docx import Document

# Ensure SQLite compatibility
__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

# Set OpenAI API Key
openai.api_key = st.secrets["OpenAI_key"]  # Ensure this is set in Streamlit secrets

# Initialize ChromaDB client
client = PersistentClient(path="knowledge_base")

# Extract text from UNI_DATA.docx
def extract_university_data(file_path):
    document = Document(file_path)
    universities = []
    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            universities.append(paragraph.text.strip())
    return universities

# Store data in ChromaDB
def store_in_chromadb(collection_name, client, data):
    collection = client.get_or_create_collection(collection_name)
    for idx, item in enumerate(data):
        collection.add(
            documents=[item],
            metadatas=[{"id": idx}],
            ids=[str(idx)]
        )
    return f"Stored {len(data)} items in collection '{collection_name}'"

# Query ChromaDB
def query_chromadb(collection_name, query_text):
    try:
        collection = client.get_collection(collection_name)
        results = collection.query(query_texts=[query_text], n_results=5)
        return [result["document"] for result in results]
    except Exception as e:
        return [f"Error querying {collection_name}: {str(e)}"]

# Streamlit chatbot interface
def main():
    st.title("University Recommendation Chatbot")
    st.markdown("### Get personalized recommendations!")

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "You are a helpful assistant providing university recommendations."}
        ]

    # User input section
    user_input = st.text_input(
        "Your preferences (e.g., 'I want a university in California for Computer Science')", key="user_input"
    )
    if st.button("Send") and user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Query ChromaDB
        uni_recommendations = query_chromadb("university_data", user_input)
        job_recommendations = query_chromadb("job_market_data", user_input)
        living_expense_recommendations = query_chromadb("living_expenses_data", user_input)

        # Summarize recommendations
        recommendation_summary = (
            f"**University Recommendations:**\n{', '.join(uni_recommendations)}\n\n"
            f"**Job Market Trends:**\n{', '.join(job_recommendations)}\n\n"
            f"**Living Expenses:**\n{', '.join(living_expense_recommendations)}"
        )

        # Use OpenAI to refine the response
        openai_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages + [{"role": "assistant", "content": recommendation_summary}]
        )

        assistant_response = openai_response.choices[0].message["content"]
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})

    # Display chat history
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"**You:** {message['content']}")
        else:
            st.markdown(f"**Chatbot:** {message['content']}")

if __name__ == "__main__":
    # Load and store datasets in ChromaDB (run once in Streamlit Cloud)
    uni_data_path = "UNI_DATA.docx"
    job_market_path = "Employment Projections.csv"
    living_expenses_path = "avglivingexpenses.csv"

    # Extract University Data
    university_data = extract_university_data(uni_data_path)

    # Load Employment Projections Data
    job_market_data = pd.read_csv(job_market_path)
    job_titles = job_market_data["Occupation Title"].tolist()

    # Load Living Expenses Data
    living_expenses_data = pd.read_csv(living_expenses_path)
    states = living_expenses_data["State"].tolist()

    # Store in ChromaDB
    store_in_chromadb("university_data", client, university_data)
    store_in_chromadb("job_market_data", client, job_titles)
    store_in_chromadb("living_expenses_data", client, states)

    # Start Streamlit Interface
    main()
