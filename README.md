# ✈️ Flight Analytics Dashboard

An end-to-end data analytics system for analyzing flight delays, airline performance, and route efficiency.
This project focuses on a deep analysis of Toronto Pearson Airport (YYZ) while also providing global comparisons across major international airports. The analysis is based on one month of flight data, offering a focused snapshot of performance trends.

Built using **FastAPI, DuckDB, and Streamlit**, the system allows users to explore flight performance through interactive dashboards and API endpoints, demonstrating skills in backend API development, data engineering, SQL-based analytics, and interactive data visualization.

---

## 🚀 Features

### 🌍 Global Analysis

* Compare average delays across major international airports
* Identify busiest and most delay-prone time intervals
* Analyze airline performance at different airports

### ✈️ YYZ Deep Dive

* Busiest routes and busiest international routes from YYZ
* Most delayed routes and airlines
* Airline performance metrics:

  * Average delay (minutes)
  * On-time percentage (%)
  * Cancellation rate (%)
* Time-based delay patterns (3-hour intervals)

### 🔎 Interactive Exploration

* Query airline performance by airport
* Analyze route-level airline delays and identify the most reliable airline for each route based on lowest average delay and highest on-time rate
* Dynamic filtering through dashboard inputs

---

## 🛠 Tech Stack

* **Backend:** FastAPI
* **Database:** DuckDB
* **Frontend:** Streamlit
* **Visualization:** Plotly, Pandas
* **Languages:** Python, SQL

---

## 🧠 System Architecture

1. Raw flight data is fetched from an external API
2. A data pipeline processes, cleans, and transforms the data into a structured format
3. The processed data is loaded into DuckDB for efficient analytical querying
4. FastAPI exposes analytical endpoints for querying the data
5. Streamlit dashboard consumes these endpoints and visualizes insights

**Flow:**
Frontend (Streamlit) ↔ API (FastAPI) ↔ Database (DuckDB)

---

## 📁 Project Structure

```bash
flight-analytics-system/
│
├── backend/              # FastAPI application
├── database/             # DuckDB database
├── dashboard/            # Streamlit dashboard
│   ├── Home.py           # Dashboard entry point
│   └── pages/            # Dashboard pages
├── data_pipeline/        # Data ingestion and processing scripts
├── raw_data/             # Raw airport JSON files
└── README.md
```
---

## ⚙️ How to Run

## 1. Database Setup

Run both scripts to fully initialize the analytics database:

```bash
python backend/load_to_duckdb.py
python backend/load_airport_delay_duckdb.py
```

### 2. Start the backend

```bash
uvicorn backend.app:app --reload
```

### 3. Run the dashboard

```bash
streamlit run dashboard/Home.py
```

### 4. Open in browser

* API docs: http://localhost:8000/docs
* Dashboard: http://localhost:8501

---

## 🔌 Example API Endpoints

* `/global/airports/global-comparison`
* `/yyz/routes/busiest`
* `/yyz/analytics/routes/worst-delays`
* `/yyz/airlines/delay`
* `/yyz/analytics/delay/by-time`
* `/global/airports/{airport}/airlines/summary`

---
## 📐 Delay Calculation Methodology

Flight delays in this project are calculated using the difference between scheduled times and actual runway times:

Departure Delay (minutes) = Actual runway departure time − Scheduled departure time
Arrival Delay (minutes) = Actual runway arrival time − Scheduled arrival time

These calculations ensure that delays reflect real operational performance rather than gate-level timing, providing a more accurate measure of how flights are impacted on the runway.

Additional derived metrics include:

* On-time flights: Flights with delay ≤ 15 minutes
* Average delay: Mean delay across flights for a given airline, route, or airport
* Cancellation rate: Percentage of flights marked as cancelled in the dataset

---

## 📸 Dashboard Preview

### Global Overview  
Shows delay comparison across major international airports
<img width="2173" height="664" alt="Screenshot 2026-05-05 004147" src="https://github.com/user-attachments/assets/a127f6a7-399e-48c3-af6b-34c2898047e0" />


### Time Analytics 
Shows the busiest 3 hour time intervals across major international airports
<img width="2191" height="638" alt="Screenshot 2026-05-05 004205" src="https://github.com/user-attachments/assets/6bc1dabc-c63a-4fbc-a287-a5b616434030" />


### YYZ Airline Analytics  
Displays airlines with the highest average delay at YYZ
<img width="2205" height="654" alt="Screenshot 2026-05-05 004248" src="https://github.com/user-attachments/assets/41224982-f93b-44a2-9f3e-b925e03eb1c6" />


### Airline Performance Explorer
Displays the performance of airlines at different airports around the world
<img width="2182" height="686" alt="Screenshot 2026-05-05 004333" src="https://github.com/user-attachments/assets/4c512a36-d125-4824-ab0f-a87204dc0ffe" />


### Route Analysis 
Shows the best performing airlines based on average delay for specific routes
<img width="2197" height="530" alt="Screenshot 2026-05-05 004358" src="https://github.com/user-attachments/assets/ce29084d-49a0-4a4e-951e-b453d5aebeda" />

---

## 📊 Key Insights

* Airline performance varies significantly by airport
* High-volume, short-haul routes tend to experience relatively lower average delays due to more frequent scheduling and operational efficiency, whereas long-haul and international flights generally exhibit higher average delays due to increased complexity and longer turnaround times
* Different airlines that travel on the same route can exhibit noticeably different delay patterns, with some carriers proving more reliable than others for specific routes
* Airports worldwide all have different peak times, though nearby airports often share similar busiest intervals
* Airlines and routes operating during peak hours tend to experience higher delays due to congestion, while those scheduled during less busy periods generally achieve higher on-time rates and lower average delays

---

## 🧠 Skills Demonstrated

* **Backend Development:** Designed and implemented RESTful APIs using FastAPI
* **Data Engineering:** Built a data pipeline to extract, transform, and load flight data into DuckDB
* **Database Management:** Utilized DuckDB for efficient analytical querying and data storage
* **SQL Analytics:** Wrote complex queries to extract insights on delays, routes, and airline performance
* **Data Visualization:** Built interactive dashboards using Streamlit and Plotly
* **Full-Stack Integration:** Connected frontend dashboards with backend APIs for real-time data exploration
* **Problem Solving:** Identified patterns in flight delays and optimized queries for performance
* **Project Structuring:** Organized a scalable and maintainable full-stack data application

---

## 🔮 Future Improvements

* Real-time flight data integration
* Machine learning models for delay prediction
* User authentication and saved queries
* Cloud deployment (AWS / GCP)

---

## 📌 Summary

This project demonstrates:

* Backend API design with FastAPI
* Data pipeline development for ingestion and transformation
* Efficient analytical querying using DuckDB
* Interactive dashboard development with Streamlit and Plotly
* Real-world data analysis and visualization

---
