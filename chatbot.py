
import streamlit as st

Compass_code = st.Page("COMPASS_code.py", title = 'Compass_code')


pg = st.navigation([Compass_code])

st.set_page_config(page_title = "HW Manager")

pg.run()
