import streamlit as st
import datetime
import requests
from streamlit_folium import st_folium
import folium
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError




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

# pickup_longitude = st.number_input(
#     "Pickup longitude",
# )

# pickup_latitude = st.number_input(
#     "Pickup latitude",
# )

# -----------------------------
# Dropoff coordinates
# -----------------------------

# dropoff_longitude = st.number_input(
#     "Dropoff longitude",
# )

# dropoff_latitude = st.number_input(
#     "Dropoff latitude",
# )

# -----------------------------
# Passenger count
# -----------------------------

passenger_count = st.slider(
    "Passenger count",
    min_value=1,
    max_value=10,
    value=3
)


#-------------
#on est ou on vas ou
#-----------------


depart = st.text_input("📍 adresse de départ", "26 avenue d'eylau 75016 paris")
arrive = st.text_input("🏁 adresse d'arriver" ," 88 rue du Faubourg Saint-Honoré")



# # center on Liberty Bell, add marker
# m = folium.Map(location=[pickup_longitude, pickup_latitude], zoom_start=16)

# # call to render Folium map in Streamlit
# st_data = st_folium(m, width=725)


geolocator = Nominatim(user_agent="taxifare", timeout=10)

@st.cache_data
def geocode_cached(address):
    geolocator = Nominatim(user_agent="taxifare_app_louis_vidal", timeout=10)
    try:
        return geolocator.geocode(address)
    except (GeocoderTimedOut, GeocoderServiceError):
        return None

pickup_location = geocode_cached(depart)
destination_location = geocode_cached(arrive)




if pickup_location and destination_location:
    pickup_lat, pickup_lon = pickup_location.latitude, pickup_location.longitude
    destination_lat, destination_lon = destination_location.latitude, destination_location.longitude

    m = folium.Map(location=[pickup_lat, pickup_lon], zoom_start=13)
    folium.Marker([pickup_lat, pickup_lon], tooltip="Départ").add_to(m)
    folium.Marker([destination_lat, destination_lon], tooltip="Arrivée", icon=folium.Icon(color="red")).add_to(m)

    st_folium(m, width=725)
else:
    st.warning("Adresse de départ ou d'arrivée introuvable.")


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
        "pickup_longitude": pickup_lon,
        "pickup_latitude": pickup_lat,
        "dropoff_longitude": destination_lon,
        "dropoff_latitude": destination_lat,
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
