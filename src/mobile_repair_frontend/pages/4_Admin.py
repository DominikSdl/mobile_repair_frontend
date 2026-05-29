import streamlit as st
import requests
import os

from mobile_repair_frontend.pages.utils.auth import (
    get_token,
    is_logged_in,
    is_admin
)

from mobile_repair_frontend.components.sidebar import (
    render_sidebar
)

API_URL = os.getenv(
    "API_URL",
    "http://localhost:8000/api"
)

# ======================
# SIDEBAR
# ======================

render_sidebar()

st.title("👑 Panel administratora")

# ======================
# SPRAWDZENIE DOSTĘPU
# ======================

if not is_logged_in():

    st.warning("Musisz się zalogować")

    st.stop()

if not is_admin():

    st.error(
        "Brak dostępu 🚫 (tylko administrator)"
    )

    st.stop()

headers = {
    "Authorization": f"Bearer {get_token()}"
}

# ======================
# POBIERANIE DANYCH
# ======================

def get_roles():

    res = requests.get(
        f"{API_URL}/roles",
        headers=headers
    )

    if res.status_code == 200:
        return res.json()

    return []


def get_users():

    res = requests.get(
        f"{API_URL}/users",
        headers=headers
    )

    if res.status_code == 200:
        return res.json()

    return []


roles_data = get_roles()

users_data = get_users()

role_options = [
    r["name"]
    for r in roles_data
]

user_options = {
    f"{u['email']} ({u['id']})": u["id"]
    for u in users_data
}

# ======================
# TWORZENIE ROLI
# ======================

st.subheader("➕ Utwórz rolę")

new_role = st.text_input(
    "Nazwa roli"
)

if st.button("Utwórz rolę"):

    res = requests.post(
        f"{API_URL}/roles",
        params={"role_name": new_role},
        headers=headers
    )

    if res.status_code == 201:

        st.success("Rola została utworzona ✅")

        st.cache_data.clear()

        st.rerun()

    else:

        st.error(res.text)

# ======================
# PRZYPISYWANIE ROLI
# ======================

st.subheader(
    "👤 Przypisz rolę użytkownikowi"
)

if user_options and role_options:

    selected_user_label = st.selectbox(
        "Użytkownik",
        list(user_options.keys())
    )

    selected_user_id = user_options[
        selected_user_label
    ]

    selected_role = st.selectbox(
        "Rola",
        role_options
    )

    if st.button("Przypisz rolę"):

        res = requests.post(
            f"{API_URL}/users/{selected_user_id}/roles",
            params={
                "role_name": selected_role
            },
            headers=headers
        )

        if res.status_code == 200:

            st.success(
                "Rola została przypisana ✅"
            )

        else:

            st.error(res.text)

else:

    st.warning(
        "Brak użytkowników lub ról"
    )

# ======================
# USUWANIE ROLI
# ======================

st.subheader(
    "❌ Usuń rolę użytkownikowi"
)

if user_options and role_options:

    selected_user_label_remove = st.selectbox(
        "Użytkownik do usunięcia roli",
        list(user_options.keys())
    )

    selected_user_id_remove = user_options[
        selected_user_label_remove
    ]

    selected_role_remove = st.selectbox(
        "Rola do usunięcia",
        role_options
    )

    if st.button("Usuń rolę"):

        res = requests.delete(
            f"{API_URL}/users/{selected_user_id_remove}/roles",
            params={
                "role_name": selected_role_remove
            },
            headers=headers
        )

        if res.status_code == 200:

            st.success(
                "Rola została usunięta ✅"
            )

        else:

            st.error(res.text)

# ======================
# PODGLĄD RÓL UŻYTKOWNIKA
# ======================

st.subheader(
    "📋 Role użytkownika"
)

if user_options:

    selected_user_label_roles = st.selectbox(
        "Wybierz użytkownika",
        list(user_options.keys())
    )

    selected_user_id_roles = user_options[
        selected_user_label_roles
    ]

    if st.button("Pobierz role"):

        res = requests.get(
            f"{API_URL}/users/{selected_user_id_roles}/roles",
            headers=headers
        )

        if res.status_code == 200:

            st.json(res.json())

        else:

            st.error(res.text)