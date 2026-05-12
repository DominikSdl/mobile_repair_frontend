import streamlit as st
from mobile_repair_frontend.api.client import create_service, get_service, get_services
from mobile_repair_frontend.pages.utils.auth import get_token, is_logged_in, is_staff
from mobile_repair_frontend.components.sidebar import render_sidebar


render_sidebar()
st.title("🛠 Services")

if not is_logged_in():
    st.warning("Zaloguj się")
    st.stop()

token = get_token()

# ======================
# LIST SERVICES
# ======================
st.subheader("Lista usług")

services_res = get_services(token)

if services_res.status_code == 200:
    services = services_res.json()

    if services:
        st.dataframe(
            services,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Brak usług")
else:
    st.error("Nie można pobrać usług")
    st.caption(services_res.text)

# ======================
# CREATE SERVICE
# ======================

if is_staff():
    st.subheader("Dodaj usługę")

    with st.form("create_service_form"):
        service_name = st.text_input("Nazwa usługi")
        service_price = st.number_input(
            "Cena",
            min_value=0,
            step=1
        )

        submitted = st.form_submit_button("Dodaj usługę")

    if submitted:
        if not service_name.strip():
            st.error("Podaj nazwę usługi")
        else:
            data = {
                "name": service_name.strip(),
                "price": int(service_price)
            }

            res = create_service(data, token)

            if res.status_code == 201:
                st.success("Usługa dodana")
                st.rerun()
            elif res.status_code == 403:
                st.error("Nie masz uprawnień. Usługi może dodawać admin albo employee.")
            else:
                st.error(res.text)

# ======================
# GET SERVICE
# ======================

if is_staff():

    st.subheader("Pobierz usługę po ID")

    service_id = st.text_input("Service ID")

    if st.button("Pobierz"):
        res = get_service(service_id, token)

        if res.status_code == 200:
            st.json(res.json())
        else:
            st.error("Nie znaleziono")

