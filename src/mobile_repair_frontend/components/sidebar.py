import streamlit as st
from jose import jwt

from mobile_repair_frontend.pages.utils.auth import (
    logout,
    is_logged_in,
    is_admin
)

def get_username():

    token = st.session_state.get("token")

    if not token:
        return None

    try:
        payload = jwt.get_unverified_claims(token)
        return payload.get("sub")

    except Exception:
        return None


def render_sidebar():

    with st.sidebar:

        st.title("📱 Mobile Repair")

        st.divider()

        # ======================
        # NOT LOGGED
        # ======================
        if not is_logged_in():

            st.page_link(
                "pages/1_Login.py",
                label="🔐 Login"
            )

            return

        # ======================
        # LOGGED USER
        # ======================
        username = get_username()

        st.success("Zalogowany")

        if username:
            st.caption(f"👤 {username}")

        st.divider()

        # ======================
        # NAVIGATION
        # ======================
        st.page_link(
            "app.py",
            label="🏠 Home"
        )

        st.page_link(
            "pages/2_Services.py",
            label="🛠 Services"
        )

        st.page_link(
            "pages/3_Reservations.py",
            label="📅 Reservations"
        )

        # 🔐 ONLY ADMIN
        if is_admin():

            st.page_link(
                "pages/4_Admin.py",
                label="👑 Admin Panel"
            )

        st.divider()

        # ======================
        # LOGOUT
        # ======================
        if st.button(
            "🚪 Wyloguj",
            use_container_width=True
        ):

            logout()

            st.switch_page("pages/1_Login.py")