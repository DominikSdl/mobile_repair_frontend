import streamlit as st
from jose import jwt

from mobile_repair_frontend.pages.utils.auth import (
    logout,
    is_logged_in,
    is_admin
)

# ======================
# POBIERANIE NAZWY UŻYTKOWNIKA
# ======================

def get_username():

    token = st.session_state.get("token")

    if not token:
        return None

    try:

        payload = jwt.get_unverified_claims(
            token
        )

        return payload.get("sub")

    except Exception:

        return None


# ======================
# SIDEBAR
# ======================

def render_sidebar():

    with st.sidebar:

        st.title("📱 Mobile Repair")

        st.divider()

        # ======================
        # NIEZALOGOWANY UŻYTKOWNIK
        # ======================

        if not is_logged_in():

            st.page_link(
                "pages/1_Login.py",
                label="🔐 Logowanie"
            )

            return

        # ======================
        # ZALOGOWANY UŻYTKOWNIK
        # ======================

        username = get_username()

        st.success("Zalogowano pomyślnie ✅")

        if username:

            st.caption(
                f"👤 {username}"
            )

        st.divider()

        # ======================
        # NAWIGACJA
        # ======================

        st.page_link(
            "app.py",
            label="🏠 Strona główna"
        )

        st.page_link(
            "pages/2_Services.py",
            label="🛠 Usługi"
        )

        st.page_link(
            "pages/3_Reservations.py",
            label="📅 Rezerwacje"
        )

        # ======================
        # PANEL ADMINISTRATORA
        # ======================

        if is_admin():

            st.page_link(
                "pages/4_Admin.py",
                label="👑 Panel administratora"
            )

        st.divider()

        # ======================
        # WYLOGOWANIE
        # ======================

        if st.button(
            "🚪 Wyloguj się",
            use_container_width=True
        ):

            logout()

            st.switch_page(
                "pages/1_Login.py"
            )