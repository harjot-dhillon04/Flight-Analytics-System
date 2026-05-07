import streamlit as st 
import requests
import pandas as pd

API = "http://backend:8000"

def safe_get(url, params=None):
    try:
        res = requests.get(url, params=params)
        data = res.json()
    except Exception:
        st.error("API did not return JSON")
        st.stop()

    if isinstance(data, dict) and "error" in data:
        st.error(data["error"])
        st.stop()

    return data

st.title("🛣 Route Explorer")

st.markdown("""
### Discover the best airlines for your travel route!
This tool allows you to explore and compare airline performance on specific routes. Enter your desired route (e.g., YYZ-LAX), and we'll provide a list of airlines ranked by their delay performance. Make better decisions about your travel based on real-time airline performance data.
""")

route = st.text_input("Enter Route (e.g. YYZ-LAX)")

if st.button("Analyze"):

    data = safe_get(
        f"{API}/yyz/analytics/route/airlines",
        params={"route": route}
    )

    if isinstance(data, list) and len(data) > 0:
        df = pd.DataFrame(data)

        # Rename columns
        rename_map = {
            "total_flights": "Total Flights",
            "avg_delay": "Average Delay (minutes)",
            "on_time_rate": "On-Time Rate (%)"
        }
        df = df.rename(columns=rename_map)

        # Capitalize any other columns
        df.columns = [col.title() if col not in rename_map.values() else col for col in df.columns]

        # Start index at 1
        df.index = df.index + 1

        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No route data found")