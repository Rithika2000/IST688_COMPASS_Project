import streamlit as st

def main():
    st.title("Chatbot Interface")
    st.markdown("### Ask your question below:")

    user_input = st.text_input("Your Question:", placeholder="Type your query here...")
    if st.button("Send"):
        st.write(f"**You:** {user_input}")
        st.write("**Bot:** Mock response to your question.")

if __name__ == "__main__":
    main()
