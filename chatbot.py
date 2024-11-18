import streamlit as st

Compass_code = st.Page("COMPASS_code.py", title = 'Compass_code')
test_chatbot = st.Page("test_chatbot.py", title = 'test_chatbot')


pg = st.navigation([Compass_code,test_chatbot])

st.set_page_config(page_title = "HW Manager")

pg.run()
