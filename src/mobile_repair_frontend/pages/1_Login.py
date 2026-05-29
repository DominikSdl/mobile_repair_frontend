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
# TRYB (LOGOWANIE / REJESTRACJA)
# ======================
mode = st.radio("Wybierz opcję", ["Logowanie", "Rejestracja"])

# ======================
# LOGOWANIE
# ======================
if mode == "Logowanie":
    st.subheader("Logowanie")

    email = st.text_input("Adres e-mail", key="login_email")
    password = st.text_input("Hasło", type="password", key="login_pass")

    if st.button("Zaloguj się"):
        res = login(email, password)

        if res.status_code == 200:
            token = res.json()["token"]
            save_token(token)

            st.success("Zalogowano pomyślnie ✅")
            st.switch_page("pages/2_Services.py")
        else:
            st.error("Nieprawidłowy adres e-mail lub hasło")

# ======================
# REJESTRACJA
# ======================
else:
    st.subheader("Rejestracja")

    email = st.text_input("Adres e-mail", key="reg_email")
    password = st.text_input("Hasło", type="password", key="reg_pass")

    if st.button("Utwórz konto"):
        data = {
            "email": email,
            "password": password
        }

        res = requests.post(
            f"{API_URL}/register",
            json=data
        )

        if res.status_code == 201:
            st.success("Konto zostało utworzone 🎉 Możesz się teraz zalogować")
        else:
            st.error("Nie udało się utworzyć konta")