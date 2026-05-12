import streamlit as st

from mobile_repair_frontend.pages.utils.auth import is_logged_in
from mobile_repair_frontend.components.sidebar import render_sidebar

# sidebar
render_sidebar()

# ======================
# REDIRECT TO LOGIN
# ======================
if not is_logged_in():

    st.switch_page("pages/1_Login.py")

# ======================
# HOME PAGE
# ======================
st.title("📱 Mobile Repair System")

st.success("Witaj w systemie")

st.write("Wybierz opcję z menu po lewej stronie.")