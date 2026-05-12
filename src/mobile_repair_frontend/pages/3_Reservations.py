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
    get_reservations
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
# AUTH
# ======================
if not is_logged_in():

    st.warning("Zaloguj się")

    st.stop()

token = get_token()

current_user_id = st.session_state.get(
    "user_id"
)

# ======================
# LOAD SERVICES
# ======================
services_res = get_services(token)

if services_res.status_code != 200:

    st.error("Nie można pobrać usług")

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
# LOAD USERS (ADMIN ONLY)
# ======================
user_map = {}

user_email_by_id = {}

if is_staff():

    users_res = get_users(token)

    if users_res.status_code != 200:

        st.error("Nie można pobrać użytkowników")

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
# CREATE RESERVATION
# ======================
st.subheader("➕ Utwórz rezerwację")

# ======================
# USER SELECTION
# ======================
if is_staff():

    selected_user_email = st.selectbox(
        "User",
        list(user_map.keys())
    )

    selected_user_id = user_map[
        selected_user_email
    ]

else:

    selected_user_id = get_user_id()

    st.info(
        "Rezerwacja dla Twojego konta"
    )

# ======================
# SERVICE SELECTION
# ======================
selected_service = st.selectbox(
    "🛠 Service",
    list(service_map.keys())
)

# ======================
# DATE PICKER
# ======================
selected_date = st.date_input(
    "📅 Select date",
    min_value=date.today()
)

# ======================
# BLOCK WEEKENDS
# ======================
if selected_date.weekday() >= 5:

    st.error(
        "Rezerwacje w weekend są niedostępne 🚫"
    )

    st.stop()

# ======================
# LOAD EXISTING RESERVATIONS
# ======================
reservations_res = get_reservations(token)

if reservations_res.status_code != 200:

    st.error(
        "Nie można pobrać rezerwacji"
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
# GENERATE AVAILABLE SLOTS
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

    # skip occupied slots
    if slot not in existing_slots:

        # skip past hours today
        if current_time > now:

            slots.append(slot)

    current_time += timedelta(
        minutes=30
    )

# ======================
# NO AVAILABLE SLOTS
# ======================
if not slots:

    st.warning(
        "Brak dostępnych terminów 😢"
    )

    st.stop()

# ======================
# SLOT SELECT
# ======================
selected_slot = st.selectbox(
    "🕒 Available hours",
    slots
)

# ======================
# CREATE DATETIME
# ======================
reservation_datetime = datetime.strptime(
    f"{selected_date} {selected_slot}",
    "%Y-%m-%d %H:%M"
)

# ======================
# CREATE BUTTON
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
            "Dodano rezerwację ✅"
        )

        st.rerun()

    else:

        st.error(res.text)

# ======================
# LIST RESERVATIONS
# ======================
st.subheader("📋 Lista rezerwacji")

if not reservations:

    st.info("Brak rezerwacji")

else:

    rows = []

    for reservation in reservations:

        service_name = service_name_by_id.get(
            reservation["service_id"],
            "Unknown Service"
        )

        reservation_dt = datetime.fromisoformat(
            reservation["reservation_date"]
        )

        row = {
            "Reservation ID": reservation["id"],
            "Service": service_name,
            "Date": reservation_dt.strftime(
                "%Y-%m-%d"
            ),
            "Time": reservation_dt.strftime(
                "%H:%M"
            )
        }

        if is_staff():

            row["User"] = user_email_by_id.get(
                reservation["user_id"],
                reservation["user_id"]
            )

        rows.append(row)

    df = pd.DataFrame(rows)

    st.dataframe(
        df,
        use_container_width=True,
        height=400
    )