import streamlit as st
import pandas as pd

from datetime import (
    datetime,
    date,
    time,
    timedelta
)

from mobile_repair_frontend.api.client import (
    create_reservation,
    get_services,
    get_users,
    get_reservations,
    delete_reservation
)

from mobile_repair_frontend.pages.utils.auth import (
    get_token,
    is_logged_in,
    is_staff,
    get_user_id
)

from mobile_repair_frontend.components.sidebar import (
    render_sidebar
)

# ======================
# SIDEBAR
# ======================

render_sidebar()

st.title("📅 Rezerwacje")

# ======================
# AUTORYZACJA
# ======================

if not is_logged_in():

    st.warning("Musisz się zalogować")

    st.stop()

token = get_token()

current_user_id = get_user_id()

# ======================
# POBIERANIE USŁUG
# ======================

services_res = get_services(token)

if services_res.status_code != 200:

    st.error("Nie udało się pobrać usług")

    st.stop()

services = services_res.json()

service_map = {
    s["name"]: s["id"]
    for s in services
}

service_name_by_id = {
    s["id"]: s["name"]
    for s in services
}

# ======================
# POBIERANIE UŻYTKOWNIKÓW
# (TYLKO ADMIN / STAFF)
# ======================

user_map = {}

user_email_by_id = {}

if is_staff():

    users_res = get_users(token)

    if users_res.status_code != 200:

        st.error("Nie udało się pobrać użytkowników")

        st.stop()

    users = users_res.json()

    user_map = {
        u["email"]: u["id"]
        for u in users
    }

    user_email_by_id = {
        u["id"]: u["email"]
        for u in users
    }

# ======================
# TWORZENIE REZERWACJI
# ======================

st.subheader("➕ Utwórz rezerwację")

# ======================
# WYBÓR UŻYTKOWNIKA
# ======================

if is_staff():

    selected_user_email = st.selectbox(
        "Użytkownik",
        list(user_map.keys())
    )

    selected_user_id = user_map[
        selected_user_email
    ]

else:

    selected_user_id = get_user_id()

    st.info(
        "Rezerwacja zostanie przypisana do Twojego konta"
    )

# ======================
# WYBÓR USŁUGI
# ======================

selected_service = st.selectbox(
    "🛠 Wybierz usługę",
    list(service_map.keys())
)

# ======================
# WYBÓR DATY
# ======================

selected_date = st.date_input(
    "📅 Wybierz datę",
    min_value=date.today()
)

# ======================
# BLOKADA WEEKENDÓW
# ======================

if selected_date.weekday() >= 5:

    st.error(
        "Rezerwacje w weekendy są niedostępne 🚫"
    )

    st.stop()

# ======================
# POBIERANIE REZERWACJI
# ======================

reservations_res = get_reservations(token)

if reservations_res.status_code != 200:

    st.error(
        "Nie udało się pobrać rezerwacji"
    )

    st.stop()

reservations = reservations_res.json()

existing_slots = []

for reservation in reservations:

    reservation_dt = datetime.fromisoformat(
        reservation["reservation_date"]
    )

    if reservation_dt.date() == selected_date:

        existing_slots.append(
            reservation_dt.strftime("%H:%M")
        )

# ======================
# GENEROWANIE DOSTĘPNYCH GODZIN
# ======================

slots = []

start_time = datetime.combine(
    selected_date,
    time(8, 0)
)

end_time = datetime.combine(
    selected_date,
    time(18, 0)
)

current_time = start_time

now = datetime.now()

while current_time < end_time:

    slot = current_time.strftime("%H:%M")

    if slot not in existing_slots:

        if current_time > now:

            slots.append(slot)

    current_time += timedelta(
        minutes=30
    )

# ======================
# BRAK TERMINÓW
# ======================

if not slots:

    if existing_slots:

        st.error(
            "Wszystkie terminy w tym dniu są już zajęte. Wybierz inny dzień. 📅"
        )

    else:

        st.warning(
            "Brak dostępnych terminów na wybrany dzień 😢"
        )

    st.stop()

# ======================
# WYBÓR GODZINY
# ======================

selected_slot = st.selectbox(
    "🕒 Dostępne godziny",
    slots
)

# ======================
# TWORZENIE DATY REZERWACJI
# ======================

reservation_datetime = datetime.strptime(
    f"{selected_date} {selected_slot}",
    "%Y-%m-%d %H:%M"
)

# ======================
# PRZYCISK TWORZENIA
# ======================

if st.button("Utwórz rezerwację"):

    data = {
        "user_id": selected_user_id,
        "service_id": service_map[
            selected_service
        ],
        "reservation_date": reservation_datetime.isoformat()
    }

    res = create_reservation(
        data,
        token
    )

    if res.status_code == 201:

        st.success(
            "Rezerwacja została utworzona ✅"
        )

        st.rerun()

    elif res.status_code == 409:

        st.error(
            "Ten termin jest już zajęty. Wybierz inną godzinę. 🚫"
        )

    else:

        st.error(
            "Nie udało się utworzyć rezerwacji. Spróbuj ponownie."
        )

# ======================
# LISTA REZERWACJI
# ======================

st.subheader("📋 Lista rezerwacji")

# ======================
# FILTROWANIE REZERWACJI
# staff widzi wszystkie, użytkownik tylko swoje
# ======================

if is_staff():

    filtered_reservations = reservations

    st.caption(
        f"Wyświetlanie wszystkich rezerwacji ({len(filtered_reservations)})"
    )

else:

    filtered_reservations = [
        r for r in reservations
        if str(r["user_id"]) == str(current_user_id)
    ]

    st.caption(
        f"Wyświetlanie Twoich rezerwacji ({len(filtered_reservations)})"
    )

# ======================
# FILTR UŻYTKOWNIKA DLA STAFF
# ======================

if is_staff() and user_email_by_id:

    filter_options = ["Wszyscy użytkownicy"] + list(user_map.keys())

    selected_filter_email = st.selectbox(
        "🔍 Filtruj po użytkowniku",
        filter_options
    )

    if selected_filter_email != "Wszyscy użytkownicy":

        filter_user_id = user_map[selected_filter_email]

        filtered_reservations = [
            r for r in filtered_reservations
            if str(r["user_id"]) == str(filter_user_id)
        ]

# ======================
# WYŚWIETLANIE LISTY
# ======================
if not filtered_reservations:
    st.info("Brak rezerwacji do wyświetlenia")
else:
    for reservation in filtered_reservations:
        service_name = service_name_by_id.get(
            reservation["service_id"],
            "Nieznana usługa"
        )
        reservation_dt = datetime.fromisoformat(
            reservation["reservation_date"]
        )

        col1, col2, col3, col4, col5 = st.columns(
            [2, 2, 1, 2, 1]
        )

        col1.write(service_name)
        col2.write(
            reservation_dt.strftime("%Y-%m-%d %H:%M")
        )

        if is_staff():
            user_label = user_email_by_id.get(
                reservation["user_id"],
                str(reservation["user_id"])
            )
            col3.write(user_label)

        col4.write(f"ID: {reservation['id']}")

        is_owner = str(reservation["user_id"]) == str(current_user_id)

        if is_staff() or is_owner:
            if col5.button(
                "🗑️",
                key=f"del_{reservation['id']}",
                help="Usuń rezerwację"
            ):
                del_res = delete_reservation(
                    reservation["id"],
                    token
                )
                if del_res.status_code == 204:
                    st.success("Rezerwacja usunięta ✅")
                    st.rerun()
                else:
                    st.error(
                        f"Błąd usuwania: {del_res.status_code}"
                    )