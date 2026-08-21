import streamlit as st
import datetime
import requests

# -----------------------------
# Title
# -----------------------------

st.title("TaxiFareModel")

st.write(
    "Enter the parameters of your taxi ride to estimate the fare."
)

# -----------------------------
# Date and time
# -----------------------------

pickup_date = st.date_input(
    "Date de pickup",
    datetime.date(2026, 8, 21)
)

pickup_time = st.time_input(
    "Heure de pickup",
    datetime.time(12, 0)
)

pickup_datetime = datetime.datetime.combine(
    pickup_date,
    pickup_time
)

# Convert datetime to string for the API
pickup_datetime_str = pickup_datetime.strftime("%Y-%m-%d %H:%M:%S")

# -----------------------------
# Pickup coordinates
# -----------------------------

pickup_longitude = st.number_input(
    "Pickup longitude",
)

pickup_latitude = st.number_input(
    "Pickup latitude",
)

# -----------------------------
# Dropoff coordinates
# -----------------------------

dropoff_longitude = st.number_input(
    "Dropoff longitude",
)

dropoff_latitude = st.number_input(
    "Dropoff latitude",
)

# -----------------------------
# Passenger count
# -----------------------------

passenger_count = st.slider(
    "Passenger count",
    min_value=1,
    max_value=10,
    value=3
)

# -----------------------------
# API
# -----------------------------

url = "https://taxifare.lewagon.ai/predict"

# -----------------------------
# Prediction
# -----------------------------

if st.button("Predict fare"):

    voyage = {
        "pickup_datetime": pickup_datetime_str,
        "pickup_longitude": pickup_longitude,
        "pickup_latitude": pickup_latitude,
        "dropoff_longitude": dropoff_longitude,
        "dropoff_latitude": dropoff_latitude,
        "passenger_count": passenger_count
    }

    try:
        response = requests.get(url, params=voyage)

        if response.status_code == 200:

            result = response.json()

            fare = result["fare"]

            st.success(f"Estimated fare: ${fare:.2f}")

            st.json(result)

        else:

            st.error(f"API error: {response.status_code}")
            st.write(response.text)

    except requests.exceptions.RequestException as e:

        st.error("Unable to connect to the API.")
        st.write(e)
