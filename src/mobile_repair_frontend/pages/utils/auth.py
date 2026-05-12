from jose import jwt
import streamlit as st


def get_user_id():

    token = st.session_state.get("token")

    if not token:
        return None

    try:
        payload = jwt.get_unverified_claims(token)
        user_id = payload.get("user_id")

        return user_id

    except Exception:
        return None

def get_roles():

    token = st.session_state.get("token")

    if not token:
        return []

    try:
        payload = jwt.get_unverified_claims(token)

        roles = payload.get("roles", [])

        if isinstance(roles, str):
            roles = [roles]

        return roles

    except Exception:
        return []

def save_token(token):
    st.session_state["token"] = token

def is_admin():
    return "admin" in get_roles()


def is_employee():
    return "employee" in get_roles()


def is_staff():
    return (
        is_admin()
        or is_employee()
    )

def get_token():
    return st.session_state.get("token")


def is_logged_in():
    return "token" in st.session_state

def logout():
    del st.session_state["token"]