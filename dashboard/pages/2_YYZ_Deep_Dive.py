import streamlit as st
import requests
import pandas as pd
import plotly.express as px

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

st.title("✈️ YYZ Deep Dive")

tab1, tab2, tab3 = st.tabs([
    "🛣 Routes",
    "✈️ Airline Analytics",
    "⏱ Time Analytics"
])

import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# TAB 1 — ROUTES
# -------------------------------
with tab1:
    st.subheader("Busiest Routes from YYZ")

    routes = safe_get(f"{API}/yyz/routes/busiest")
    intl_routes = safe_get(f"{API}/yyz/routes/busiest/international")

    if isinstance(routes, list) and len(routes) > 0:
        df_routes = pd.DataFrame(routes)
        # Capitalize column names
        df_routes.columns = [col.title() for col in df_routes.columns]
        # Start index at 1
        df_routes.index = df_routes.index + 1
        st.dataframe(df_routes, use_container_width=True)
    else:
        st.warning("No route data available")

    st.markdown("---")

    st.subheader("Busiest International Routes")

    if isinstance(intl_routes, list) and len(intl_routes) > 0:
        df_intl = pd.DataFrame(intl_routes)
        df_intl.columns = [col.title() for col in df_intl.columns]
        df_intl.index = df_intl.index + 1
        st.dataframe(df_intl, use_container_width=True)
    else:
        st.warning("No international route data")

    st.markdown("---")

    st.subheader("Most Delayed Routes from YYZ")

    delayed_routes = safe_get(f"{API}/yyz/analytics/routes/worst-delays")

    if isinstance(delayed_routes, list) and len(delayed_routes) > 0:
        df_delayed_routes = pd.DataFrame(delayed_routes)

    # Format column names
        df_delayed_routes.columns = [col.replace("_", " ").title() for col in df_delayed_routes.columns]

    # Rename delay column to clean label
        for col in df_delayed_routes.columns:
            if "Delay" in col:
                df_delayed_routes = df_delayed_routes.rename(columns={col: "Average Delay (minutes)"})

    # Sort by delay (after renaming)
                df_delayed_routes = df_delayed_routes.sort_values("Average Delay (minutes)", ascending=False)

                df_delayed_routes.index = df_delayed_routes.index + 1

                st.dataframe(df_delayed_routes, use_container_width=True)
    else:
        st.warning("No delayed route data")
# -------------------------------
# TAB 2 — AIRLINE ANALYTICS
# -------------------------------
with tab2:
    st.subheader("Most Delayed Airlines")
    delayed = safe_get(f"{API}/yyz/airlines/delay")

    if isinstance(delayed, list) and len(delayed) > 0:
        df_delayed = pd.DataFrame(delayed)
        # Rename columns
        df_delayed.columns = [col.replace("_", " ").title() for col in df_delayed.columns]
        for col in df_delayed.columns:
            if "Avg Delay" in col:
                df_delayed = df_delayed.rename(columns={col: f"Average Delay (minutes)"})

            if "Flights" in col:
                df_delayed = df_delayed.rename(columns={col: f"Total Fligths"})
        df_delayed = df_delayed.sort_values([col for col in df_delayed.columns if "Delay" in col][0], ascending=False)
        df_delayed.index = df_delayed.index + 1
        st.dataframe(df_delayed, use_container_width=True)
    else:
        st.warning("No delayed airline data")

    st.markdown("---")

    st.subheader("Best On-Time Airlines")
    ontime = safe_get(f"{API}/yyz/airlines/on-time")

    if isinstance(ontime, list) and len(ontime) > 0:
        df_ontime = pd.DataFrame(ontime)
        df_ontime.columns = [col.replace("_", " ").title() for col in df_ontime.columns]
        for col in df_ontime.columns:
            if "On Time" in col:
                df_ontime = df_ontime.rename(columns={col: f"{col} (%)"})
        
        df_ontime = df_ontime.sort_values([col for col in df_ontime.columns if "On Time Rate" in col][0], ascending=False)
        df_ontime.index = df_ontime.index + 1
        st.dataframe(df_ontime, use_container_width=True)
    else:
        st.warning("No on-time airline data")

    st.markdown("---")

    st.subheader("Airlines by Cancellation Rate")

    cancel = safe_get(f"{API}/yyz/airlines/cancellations")

    if isinstance(cancel, list) and len(cancel) > 0:
        df_cancel = pd.DataFrame(cancel)

        df_cancel.columns = [col.replace("_", " ").title() for col in df_cancel.columns]
        for col in df_cancel.columns:
            if "Cancel Rate" in col:
                df_cancel = df_cancel.rename(columns={col: f"{col} (%)"})
        
        cancel_col = [col for col in df_cancel.columns if "Cancel Rate" in col][0]
        df_cancel = df_cancel.sort_values(cancel_col, ascending=False)
        df_cancel.index = df_cancel.index + 1
        st.dataframe(df_cancel, use_container_width=True)
    else:
        st.warning("No cancellation data")
    

# -------------------------------
# TAB 3 — TIME ANALYTICS
# -------------------------------
with tab3:
    st.subheader("Average Delay by Time Interval")
    time_data = safe_get(f"{API}/yyz/analytics/delay/by-time")

    if isinstance(time_data, list) and len(time_data) > 0:
        df_time = pd.DataFrame(time_data)
        df_time.columns = [col.replace("_", " ").title() for col in df_time.columns]

        # Avg Delay chart
        fig_delay = px.bar(
            df_time,
            x="Time Interval",
            y="Avg Delay",
            text="Avg Delay",
            labels={"Avg Delay": "Delay (minutes)", "Time Interval": "Time Interval"}
        )
        fig_delay.update_traces(textposition="outside", textangle=0)
        fig_delay.update_layout(xaxis_tickangle=0, xaxis_tickfont_size=14, margin=dict(l=40,r=40,t=40,b=40))
        st.plotly_chart(fig_delay, use_container_width=True)

        st.markdown("---")

        st.subheader("Number of Flights by Time Interval")

        # Total Flights chart
        fig_flights = px.bar(
            df_time,
            x="Time Interval",
            y="Total Flights",
            text="Total Flights",
            labels={"Total Flights": "Flights", "Time Interval": "Time Interval"}
        )
        fig_flights.update_traces(textposition="outside", textangle=0)
        fig_flights.update_layout(xaxis_tickangle=0, xaxis_tickfont_size=14, margin=dict(l=40,r=40,t=40,b=40))
        st.plotly_chart(fig_flights, use_container_width=True)
    else:
        st.warning("No time delay data")
