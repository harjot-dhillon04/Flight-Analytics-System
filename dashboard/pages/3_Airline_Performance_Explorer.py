import streamlit as st
import requests
import pandas as pd

API = "http://backend:8000"

def safe_get(url, params=None):
    res = requests.get(url, params=params)

    try:
        data = res.json()
    except Exception:
        st.error("API did not return JSON")
        st.stop()

    if isinstance(data, dict) and "error" in data:
        st.error(data["error"])
        st.stop()

    return data

st.title("🔎 Airline Performance Explorer")

st.markdown("""
### Explore the performance of airlines at airports across the world!
This tool allows you to examine key performance metrics of an airline, including average delays, on-time percentages, and delay rankings at various airports. Get insights into how airlines perform globally to help make better-informed travel decisions.
""")


airport = st.selectbox(
    "Select Airport",
    ["YYZ","JFK","LHR", "LAX","DXB","HND","ORD","CDG","FRA","IST","SIN", "AMS", "ICN", "HKG", "SYD"]
)

airline = st.text_input("Enter Airline Name")


if st.button("Get Performance"):

    if not airline:
        st.warning("Please enter an airline")
        st.stop()

    data = safe_get(
        f"{API}/global/airports/{airport}/airlines/summary",
        params={"airline": airline}
    )

    if isinstance(data, dict) and "avg_delay" in data:
        st.metric("Average Delay (minutes)", data["avg_delay"])
        st.metric("On-Time %", data["on_time_pct"])
        st.metric(
            "Delay Rank",
            f"{data['delay_rank_at_airport']}/{data['total_airlines_at_airport']}"
        )
    else:
        st.warning("No data found")