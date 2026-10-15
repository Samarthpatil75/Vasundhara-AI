# 🌍 ClimateSense: AI-Driven Climate Risk & Carbon Monitoring Dashboard

> **Pune District, Maharashtra, India**  
> *Hackathon Prototype | Theme: AI/ML & Data-Driven Models for Climate Prediction*

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-teal.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-emerald.svg)](LICENSE)

---

## 📌 Executive Summary
Pune district encompasses dense urban zones (Pune PMC, PCMC, Hinjawadi), Western Ghats biodiversity catchments (Mulshi, Maval, Velhe), and semi-arid agrarian plains (Shirur, Baramati, Indapur). Rapid infrastructure development has exacerbated localized **Urban Heat Islands (UHI)** and **flash-flood vulnerabilities**, while fragmenting natural carbon sinks.

**ClimateSense** is a presentation-ready, multi-page AI intelligence dashboard designed for city administrators, disaster response teams, and environmental planners. It harmonizes **10 designated best-pick datasets** for multi-hazard climate risk forecasting and verifiable carbon accounting across **16 DataMeet Pune sub-districts**.

---

## 🛰️ Designated Dataset Architecture (10 Specific Tasks)

| Climate Intelligence Task | Best Pick (Primary) | Why Chosen | Backup / Alternative |
|---|---|---|---|
| **1. Temperature, humidity, wind** | **Open-Meteo Historical API** | No account or key, one URL or a few lines of Python, ERA5-quality data, daily history from 1940 | NASA POWER (CSV download) |
| **2. Rainfall** | **Open-Meteo / IMD Gridded Rainfall** | IMD is India's official sovereign data and judges trust it; Open-Meteo provides immediate ERA5 daily rain | CHIRPS or NASA POWER |
| **3. Vegetation (NDVI) for carbon** | **NASA AppEEARS (MODIS NDVI)** | Draw Pune on a map and download a clean CSV with no coding; continuous history since 2000 | Sentinel-2 via Google Earth Engine |
| **4. Land surface temp (heat risk)** | **MODIS LST via AppEEARS** | Same tool as NDVI, so you learn only one workflow and get standardized 1km Day/Night LST | Landsat 8/9 via Earth Engine |
| **5. Elevation & slope (flood risk)** | **SRTM via Google Earth Engine** | One small script gives elevation, slope angle, and topographic wetness per location | Copernicus DEM or OpenTopography |
| **6. Land cover (built-up vs green)** | **ESA WorldCover** | Clean, recent (10m), and simple categories (built-up, tree cover, cropland, water) | Dynamic World |
| **7. Tree loss / carbon estimate** | **Global Forest Watch (Hansen)** | Year-by-year tree cover loss that can be converted directly to an above-ground carbon proxy | ESA CCI Biomass |
| **8. Population exposure** | **WorldPop** | Gridded population (100m) that is easy to aggregate and join to local Pune talukas | GHSL |
| **9. Disaster events for validation** | **EM-DAT & Dartmouth Flood Observatory** | EM-DAT covers events broadly, and Dartmouth gives precise flood dates and extents | Maharashtra SDMA reports |
| **10. Map boundaries** | **DataMeet (Indian sub-districts)** | Built specifically for India and matches official administrative taluka names and codes | GADM |

---

## ⚡ 2-Minute Judge Walkthrough Script

| Time | Page | What to Click / Inspect | Key Takeaway to Present |
|---|---|---|---|
| **0:00 - 0:30** | **Home / Overview** (`app.py`) | 4 Top KPI cards & Verified Feeds ribbon. | *"ClimateSense computes live district health across 16 DataMeet talukas: high-risk areas, WorldPop population exposure, 5-yr canopy change, and biomass carbon delta."* |
| **0:30 - 0:55** | **1. 🗺️ Risk Map** | Toggle **Hazard** (Heatwave vs Flood) and **Map Engine** (Folium vs Plotly). Click on *Pune City PMC*. | *"Spatial mapping highlights urban heat traps and riparian flood zones, displaying MODIS LST, Open-Meteo rain, SRTM elevation, and WorldPop exposed residents."* |
| **0:55 - 1:20** | **2. 📈 Forecast** | Select *Pune City (PMC)*, adjust forecast horizon slider to **6 Months**. | *"XGBoost ensemble projects seasonal risk shifts into 2026 with 95% confidence bounds, comparing the local area against the Pune district benchmark."* |
| **1:20 - 1:40** | **3. 🌱 Carbon Monitor** | View 5-year NDVI trend chart and Top 8 areas by canopy loss. | *"Tracks 5-year vegetation loss using NASA AppEEARS (MODIS NDVI) and Global Forest Watch (Hansen Tree Loss) under IPCC Tier 1 proxy equations."* |
| **1:40 - 2:00** | **4. 🧠 Model Insights** & **5. 🛡️ Actions** | Review SHAP feature importance, EM-DAT/DFO flood validation, and download the municipal action plan CSV. | *"Complete model transparency and instant operational utility—turning predictions directly into population-weighted municipal policy actions."* |

---

## 🛠️ Tech Stack
- **Web Framework:** Python 3.10+, [Streamlit](https://streamlit.io/) (Multi-page native routing).
- **Interactive Geospatial Visualization:** [Folium](https://python-visualization.github.io/folium/) + [streamlit-folium](https://github.com/randyzwitch/streamlit-folium) (CartoDB Positron tiles, dynamic SVG markers, custom HTML tooltips), [Plotly](https://plotly.com/python/) (choropleth/scatter).
- **Data Analytics:** [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/).
- **AI/ML Engine:** XGBoost Classifier + Scikit-Learn with SHAP TreeExplainer, validated on EM-DAT and Dartmouth Flood Observatory (DFO) flood benchmarks.
- **Design System:** Custom CSS light theme with an emerald/teal climate palette (`#0D9488`), clean card surfaces, and colorblind-friendly risk cues (Green / Amber / Coral Red).

---

## 📂 Project Structure

```text
Vasundhara AI/
├── .streamlit/
│   └── config.toml               # Light theme configuration & teal palette
├── data/
│   ├── risk_predictions.csv      # Risk predictions for 16 DataMeet Pune areas (2021-2026)
│   ├── ndvi_timeseries.csv       # 5-year monthly AppEEARS NDVI & GFW carbon stock time-series
│   ├── feature_importance.csv    # SHAP feature importance scores & data source attributions
│   └── model_metrics.json        # Test metrics, confusion matrix, 10-dataset registry
├── scripts/
│   ├── generate_sample_data.py   # Realistic synthetic data generator for Pune
│   └── verify_app.py             # Automated health & data validation script
├── src/
│   ├── __init__.py
│   ├── utils.py                  # Dynamic data loaders, 10-feed master registry, KPI calculators
│   └── components.py             # Reusable UI cards, sample data banner, dataset pills
├── pages/
│   ├── 1_🗺️_Risk_Map.py          # Spatial risk map (Folium & Plotly) with filters & WorldPop
│   ├── 2_📈_Forecast.py          # 3-6 month lookahead with confidence intervals
│   ├── 3_🌱_Carbon_Monitor.py    # NASA AppEEARS NDVI & Global Forest Watch (Hansen)
│   ├── 4_🧠_Model_Insights.py    # SHAP explanations & EM-DAT/DFO flood validation
│   ├── 5_🛡️_Recommended_Actions.py# Phased municipal blueprints weighted by WorldPop
│   └── 6_ℹ️_About_&_Sources.py   # Complete 10-task dataset catalog & swapping instructions
├── app.py                        # Landing Home / Overview page
├── requirements.txt              # Production Python dependencies
└── README.md                     # Documentation & presentation guide
```

---

## 🚀 Quickstart: Run Locally

### 1. Clone & Set Up Environment
```bash
git clone https://github.com/your-username/climatesense-pune.git
cd climatesense-pune

# Create and activate virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS / Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Generate / Verify Sample Data
The repository includes sample datasets calibrated to the 10 designated feeds for Pune district:
```bash
python scripts/generate_sample_data.py
```

### 3. Launch Streamlit Application
```bash
streamlit run app.py
```
The app will open in your default browser at `http://localhost:8501`.

---

## ☁️ Deployment Guide (Streamlit Community Cloud)

Deploy your live dashboard in under 3 minutes for hackathon judges:

1. **Push Code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "feat: ClimateSense Pune dashboard presentation-ready"
   git remote add origin https://github.com/<your-username>/climatesense-pune.git
   git branch -M main
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud:**
   - Log into [share.streamlit.io](https://share.streamlit.io/) with your GitHub account.
   - Click **"New app"**.
   - Select your repository: `<your-username>/climatesense-pune`.
   - Set **Branch** to `main`.
   - Set **Main file path** to `app.py`.
   - Click **"Deploy!"**.

---

## 🔄 How to Plug In Real Model Outputs (Zero Code Changes)

The application has **zero hardcoded values** in the UI—everything is dynamically rendered from the files in `/data`. To substitute your production model inferences:

1. **Replace the 4 files in `data/`:**
   - `data/risk_predictions.csv`
   - `data/ndvi_timeseries.csv`
   - `data/feature_importance.csv`
   - `data/model_metrics.json`

2. Maintain the column schemas documented in Page 6 ([`pages/6_ℹ️_About_&_Sources.py`](file:///c:/Samarth.pro/Vasundhara%20AI/pages/6_ℹ️_About_&_Sources.py)).
3. Refresh your browser tab. The dashboard immediately updates all maps, KPIs, trends, and action matrices!

---

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).
