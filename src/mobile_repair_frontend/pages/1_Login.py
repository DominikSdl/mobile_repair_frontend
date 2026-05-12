import streamlit as st
import requests
import os
from mobile_repair_frontend.api.client import login
from mobile_repair_frontend.pages.utils.auth import save_token
from mobile_repair_frontend.components.sidebar import render_sidebar




API_URL = os.getenv("API_URL", "http://localhost:8000/api")

render_sidebar()
st.title("🔐 Autoryzacja")

# ======================
# TRYB (LOGIN / REGISTER)
# ======================
mode = st.radio("Wybierz opcję", ["Login", "Rejestracja"])

# ======================
# LOGIN
# ======================
if mode == "Login":
    st.subheader("Logowanie")

    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login"):
        res = login(email, password)

        if res.status_code == 200:
            token = res.json()["token"]
            save_token(token)
            st.success("Zalogowano")
            st.switch_page("pages/2_Services.py")
        else:
            st.error("Błędne dane")

# ======================
# REGISTER
# ======================
else:
    st.subheader("Rejestracja")

    email = st.text_input("Email", key="reg_email")
    password = st.text_input("Password", type="password", key="reg_pass")

    if st.button("Zarejestruj"):
        data = {
            "email": email,
            "password": password
        }

        res = requests.post(
            f"{API_URL}/register",
            json=data
        )

        if res.status_code == 201:
            st.success("Konto utworzone 🎉 Możesz się zalogować")
        else:
            st.error(res.text)