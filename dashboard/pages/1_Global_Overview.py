import streamlit as st
import requests
import pandas as pd
import plotly.express as px

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

st.title("🌐 Airport Analytics Dashboard")

# -------------------------------
# Tabs
# -------------------------------
tab1, tab2 = st.tabs(["Global Airport Comparison", "Time Analysis"])

# -------------------------------
# Tab 1 — Global Airport Comparison
# -------------------------------
with tab1:
    data = safe_get(f"{API}/airports/global-comparison")
    if isinstance(data, list) or ("airports" in data and isinstance(data["airports"], list)):
        df = pd.DataFrame(data.get("airports", data))
        if not df.empty:
            # Rename columns
            rename_map = {
                "airport": "Airport",
                "avg_delay": "Average Delay",
                "on_time_pct": "On-Time %"
            }
            df = df.rename(columns=rename_map)

            # Avg Delay chart
            st.subheader("Average Delay of Major Airports Around The World")
            fig_delay = px.bar(
                df,
                x="Airport",
                y="Average Delay",
                text="Average Delay",
                labels={"Average Delay": "Average Delay (minutes)", "Airport": "Airport"}
            )
            fig_delay.update_traces(textposition="outside", textangle=0)
            fig_delay.update_layout(xaxis_tickangle=0, xaxis_tickfont_size=14, margin=dict(l=40,r=40,t=40,b=40))
            st.plotly_chart(fig_delay, use_container_width=True)

            # On-Time % chart
            st.subheader("On-Time % of Major Aiports Around The World")
            fig_ontime = px.bar(
                df,
                x="Airport",
                y="On-Time %",
                text="On-Time %",
                labels={"On-Time %": "On-Time %", "Airport": "Airport"}
            )
            fig_ontime.update_traces(textposition="outside", textangle=0)
            fig_ontime.update_layout(xaxis_tickangle=0, xaxis_tickfont_size=14, margin=dict(l=40,r=40,t=40,b=40))
            st.plotly_chart(fig_ontime, use_container_width=True)
        else:
            st.warning("No airport data found")
    else:
        st.warning("Global airport comparison data invalid")

# -------------------------------
# Tab 2 — Time Analysis
# -------------------------------
with tab2:
    
    busiest = safe_get(f"{API}/global/airports/busiest-interval")
    worst = safe_get(f"{API}/global/worst-time-intervals")

    # Busiest Interval Table
    if isinstance(busiest, list) and busiest:
        df_busiest = pd.DataFrame(busiest)
        df_busiest = df_busiest.rename(columns={
            "airport": "Airport",
            "interval": "Interval",
            "avg_delay": "Average Delay"
        })
        df_busiest.index = df_busiest.index + 1
        st.subheader("Busiest Time-Intervals by Airport")
        st.dataframe(df_busiest, use_container_width=True)
    else:
        st.warning("Busiest interval data invalid")

    st.markdown("---")

    # Worst Interval Table
    if isinstance(worst, list) and worst:
        df_worst = pd.DataFrame(worst)
        df_worst = df_worst.rename(columns={
            "airport": "Airport",
            "interval": "Interval",
            "avg_delay": "Average Delay"
        })
        df_worst.index = df_worst.index + 1
        st.subheader("Worst Delayed Time-Intervals by Airport")
        st.dataframe(df_worst, use_container_width=True)
    else:
        st.warning("Worst interval data invalid")