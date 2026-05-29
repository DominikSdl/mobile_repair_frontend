import streamlit as st
from mobile_repair_frontend.pages.utils.auth import is_logged_in, is_staff
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

st.success("Witaj w systemie naprawy telefonów!")

st.markdown("---")

# ======================
# KARTY INFORMACYJNE
# ======================

col1, col2, col3 = st.columns(3)

with col1:
    st.info("### 📅 Rezerwacje\nUmów wizytę serwisową w kilka sekund. Wybierz usługę, datę i godzinę.")

with col2:
    st.info("### 🛠 Usługi\nSzerokie spektrum napraw — od wymiany ekranu po diagnostykę software'ową.")

with col3:
    st.info("### 👤 Twoje konto\nZarządzaj swoimi rezerwacjami i śledź status naprawy.")

st.markdown("---")

# ======================
# JAK TO DZIAŁA
# ======================

st.subheader("🚀 Jak to działa?")

steps = {
    "1️⃣ Wybierz usługę": "Znajdź odpowiednią naprawę z naszej listy usług serwisowych.",
    "2️⃣ Zarezerwuj termin": "Wybierz wolny termin w kalendarzu — dostępne godziny 8:00–18:00, pon.–pt.",
    "3️⃣ Przynieś urządzenie": "Zgłoś się o wybranej porze, a nasi technicy zajmą się resztą.",
    "4️⃣ Odbierz naprawiony sprzęt": "Po zakończeniu naprawy powiadomimy Cię i oddamy sprawne urządzenie.",
}

for title, desc in steps.items():
    with st.expander(title):
        st.write(desc)

st.markdown("---")

# ======================
# PANEL ADMINA
# ======================

if is_staff():

    st.subheader("🔧 Panel administratora")

    st.warning(
        "Masz uprawnienia administratora. "
        "Możesz zarządzać użytkownikami, usługami i wszystkimi rezerwacjami."
    )

    acol1, acol2 = st.columns(2)

    with acol1:
        if st.button("📋 Przejdź do rezerwacji", use_container_width=True):
            st.switch_page("pages/3_Reservations.py")

    with acol2:
        if st.button("🛠 Zarządzaj usługami", use_container_width=True):
            st.switch_page("pages/2_Services.py")

else:

    st.subheader("⚡ Szybkie akcje")

    qcol1, qcol2 = st.columns(2)

    with qcol1:
        if st.button("📅 Umów wizytę", use_container_width=True):
            st.switch_page("pages/3_Reservations.py")

    with qcol2:
        if st.button("🛠 Zobacz usługi", use_container_width=True):
            st.switch_page("pages/2_Services.py")

st.markdown("---")

st.caption("© 2025 Mobile Repair System · Wszelkie prawa zastrzeżone")