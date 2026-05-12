import streamlit as st
import requests
import os
from mobile_repair_frontend.pages.utils.auth import get_token, is_logged_in, is_admin
from mobile_repair_frontend.components.sidebar import render_sidebar

API_URL = os.getenv("API_URL", "http://localhost:8000/api")


render_sidebar()
st.title("👑 Admin Panel")

# ======================
# AUTH CHECK
# ======================
if not is_logged_in():
    st.warning("Zaloguj się")
    st.stop()

if not is_admin():
    st.error("Brak dostępu 🚫 (tylko admin)")
    st.stop()

headers = {
    "Authorization": f"Bearer {get_token()}"
}

# ======================
# LOAD DATA
# ======================

def get_roles():
    res = requests.get(f"{API_URL}/roles", headers=headers)
    if res.status_code == 200:
        return res.json()
    return []


def get_users():
    res = requests.get(f"{API_URL}/users", headers=headers)
    if res.status_code == 200:
        return res.json()
    return []

roles_data = get_roles()
users_data = get_users()

role_options = [r["name"] for r in roles_data]
user_options = {
    f"{u['email']} ({u['id']})": u["id"]
    for u in users_data
}

# ======================
# CREATE ROLE
# ======================
st.subheader("➕ Create Role")

new_role = st.text_input("Role name")

if st.button("Create Role"):
    res = requests.post(
        f"{API_URL}/roles",
        params={"role_name": new_role},
        headers=headers
    )

    if res.status_code == 201:
        st.success("Rola utworzona")
        st.cache_data.clear()
        st.rerun()
    else:
        st.error(res.text)

# ======================
# ASSIGN ROLE
# ======================
st.subheader("👤 Assign Role to User")

if user_options and role_options:
    selected_user_label = st.selectbox("User", list(user_options.keys()))
    selected_user_id = user_options[selected_user_label]

    selected_role = st.selectbox("Role", role_options)

    if st.button("Assign Role"):
        res = requests.post(
            f"{API_URL}/users/{selected_user_id}/roles",
            params={"role_name": selected_role},
            headers=headers
        )

        if res.status_code == 200:
            st.success("Rola przypisana")
        else:
            st.error(res.text)
else:
    st.warning("Brak użytkowników lub ról")

# ======================
# REMOVE ROLE
# ======================
st.subheader("❌ Remove Role from User")

if user_options and role_options:
    selected_user_label_remove = st.selectbox("User (remove)", list(user_options.keys()))
    selected_user_id_remove = user_options[selected_user_label_remove]

    selected_role_remove = st.selectbox("Role (remove)", role_options)

    if st.button("Remove Role"):
        res = requests.delete(
            f"{API_URL}/users/{selected_user_id_remove}/roles",
            params={"role_name": selected_role_remove},
            headers=headers
        )

        if res.status_code == 200:
            st.success("Rola usunięta")
        else:
            st.error(res.text)

# ======================
# GET USER ROLES
# ======================
st.subheader("📋 Get User Roles")

if user_options:
    selected_user_label_roles = st.selectbox("User (roles)", list(user_options.keys()))
    selected_user_id_roles = user_options[selected_user_label_roles]

    if st.button("Get Roles"):
        res = requests.get(
            f"{API_URL}/users/{selected_user_id_roles}/roles",
            headers=headers
        )

        if res.status_code == 200:
            st.json(res.json())
        else:
            st.error(res.text)