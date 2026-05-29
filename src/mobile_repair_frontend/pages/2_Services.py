import streamlit as st
import pandas as pd

from mobile_repair_frontend.api.client import (
    create_service,
    get_service,
    get_services
)

from mobile_repair_frontend.pages.utils.auth import (
    get_token,
    is_logged_in,
    is_staff
)

from mobile_repair_frontend.components.sidebar import render_sidebar

render_sidebar()

st.title("🛠 Usługi")

# ======================
# AUTORYZACJA
# ======================

if not is_logged_in():
    st.warning("Musisz się zalogować, aby zobaczyć usługi")
    st.stop()

token = get_token()

# ======================
# LISTA USŁUG
# ======================

st.subheader("Lista usług")

services_res = get_services(token)

if services_res.status_code == 200:
    services = services_res.json()

    if services:
        df = pd.DataFrame(services)
        df = df.rename(columns={
            "name": "Nazwa usługi",
            "price": "Cena (PLN)",
            "id": "ID"
        })
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Brak dostępnych usług")
else:
    st.error("Nie udało się pobrać listy usług")
    st.caption(services_res.text)

# ======================
# DODAWANIE USŁUGI
# ======================

if is_staff():

    st.subheader("Dodaj nową usługę")

    with st.form("create_service_form"):

        service_name = st.text_input("Nazwa usługi")

        service_price = st.number_input(
            "Cena (PLN)",
            min_value=0,
            step=1
        )

        submitted = st.form_submit_button("Dodaj usługę")

    if submitted:

        if not service_name.strip():
            st.error("Wpisz nazwę usługi")
        else:

            data = {
                "name": service_name.strip(),
                "price": int(service_price)
            }

            res = create_service(data, token)

            if res.status_code == 201:
                st.success("Usługa została dodana ✅")
                st.rerun()

            elif res.status_code == 403:
                st.error(
                    "Brak uprawnień. Tylko administrator lub pracownik może dodawać usługi."
                )

            else:
                st.error(res.text)

