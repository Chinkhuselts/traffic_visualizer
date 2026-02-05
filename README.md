# 🛡️ Network Traffic Log Visualizer

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-ff4b4b)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-150458)
![API](https://img.shields.io/badge/REST-API-green)

A data engineering dashboard that processes large network traffic logs, enriches IP addresses with geolocation data via REST API, and visualizes threat intelligence on an interactive map.

---

## 📖 Project Overview

This tool was designed to solve the challenge of analyzing massive server logs that are too large to load into standard spreadsheet software. It utilizes a memory-efficient ingestion pipeline to aggregate bandwidth usage by IP address and identifies the geographic origin of high-traffic sources.

**Key Features:**
* **Big Data Ingestion:** Implements Pandas **chunking** to process large CSV datasets without overloading RAM.
* **Data Enrichment:** Integrates with the `ip-api` REST service to append latitude, longitude, and country data to raw IP addresses.
* **Interactive Visualization:** Renders traffic origins on a global map and statistical breakdowns by country.
* **Reliability:** Includes error handling and rate-limiting logic to manage API request constraints.

---

## 📸 Screenshots

### 1. High-Bandwidth Analysis & Ingestion Logic
The dashboard identifies top bandwidth consumers immediately. The interface displays the underlying ingestion logic, highlighting the chunk-based processing method.
![Dashboard Overview](assets/streamlit_1.png)

### 2. Geospatial Intelligence
Traffic sources are plotted on a dark-mode map, allowing security analysts to visually identify suspicious clusters of activity.
![Map Visualization](assets/streamlit_2.png)

### 3. Traffic Distribution by Country
Aggregated statistics show total data transfer volume per country.
![Country Stats](assets/streamlit_3.png)

---

## 🛠️ Tech Stack

* **Language:** Python
* **Data Manipulation:** Pandas (Chunking, GroupBy, Aggregation)
* **Interface:** Streamlit
* **Network Requests:** `requests` library (RESTful API integration)
* **Visualization:** Plotly & Streamlit Map
* **Data Generation:** `Faker` (for creating mock high-volume logs)

---

## 🚀 How to Run

### 1. Clone and Install
```bash
git clone [https://github.com/yourusername/network-traffic-visualizer.git](https://github.com/yourusername/network-traffic-visualizer.git)
cd network-traffic-visualizer
pip install -r requirements.txt
```
2. Generate Mock Data
Create a realistic, large-scale dataset using the included script. This generates a CSV with columns: timestamp, source_ip, dest_ip, bytes_sent, status_code, and protocol.

Bash
python generate_logs.py
3. Launch the Dashboard
Bash
streamlit run app.py
🧩 Engineering Logic
Data Ingestion Pipeline
To handle large file sizes, the application reads the CSV in chunks (e.g., 10,000 rows at a time) rather than loading the entire file into memory.

Python
```
# Code Snippet from app.py
for chunk in pd.read_csv(file, chunksize=10000):
    process(chunk)
    aggregate_results()
```
API Integration
The application enriches top traffic sources by querying a geolocation API. To ensure system stability and compliance with API limits, the loop includes a delay mechanism.

Python
```
# Rate limiting implementation
for i, (index, row) in enumerate(top_ips.iterrows()):
    lat, lon, country = get_ip_location(row['source_ip'])
    time.sleep(0.5) # Respect API rate limits
```
