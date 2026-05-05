import streamlit as st

st.set_page_config(
    page_title="Flight Analytics Dashboard",
    layout="wide"
)

st.title("✈️ Flight Analytics Dashboard")

st.markdown("""
### Welcome to the Flight Analytics Dashboard!

This dashboard provides insights into global flight operations and performance metrics collected over **one month** with a specific deep dive into Toronto Pearson International Airport (YYZ). Use the tabs and sidebar to explore different aspects of the data.

---

### What this dashboard shows:
- 🌍 **Global Airport Performance** – Average delays, on-time percentages, and airline performances of the busiest airports worldwide.
- ✈️ **YYZ Deep Dive** – Detailed analysis of Toronto Pearson International Airport operations.
- 🔎 **Airline & Route Exploration** – Most delayed airlines, best on-time performers, and top routes.
- ⏱ **Delay Patterns by Time** – Insights into delays and flight activity across different time intervals.

**Note:** All flight data is collected from a single month.
""")