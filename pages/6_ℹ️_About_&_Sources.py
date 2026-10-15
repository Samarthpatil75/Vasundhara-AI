"""
pages/6_ℹ️_About_&_Sources.py - Technical Documentation, Data Lineage & Model Swapping Guide
Presents the verified 10-task dataset matrix, exact access methodologies, and drop-in real model steps.
"""

import streamlit as st
import os
import pandas as pd

from src.utils import COLOR_THEME, DATA_DIR, DESIGNATED_DATASETS
from src.components import (
    render_header,
    render_sample_data_banner,
    render_designated_datasets_pill_bar,
    render_footer
)

st.set_page_config(
    page_title="About & Data Lineage | ClimateSense Pune",
    page_icon="ℹ️",
    layout="wide"
)


def main():
    render_header(
        title="About ClimateSense: Data Sources & Lineage",
        subtitle="Complete catalog of the 10 designated climate, satellite, and demographic datasets"
    )
    render_sample_data_banner()
    render_designated_datasets_pill_bar()

    # Section 1: The Master 10-Task Dataset Specification Table
    st.markdown("### 🏆 Designated ClimateSense Dataset Architecture (10 Specific Tasks)")
    st.markdown(
        """
        The following 10 data feeds constitute the exact analytical spine of ClimateSense.
        Each was selected for maximum scientific fidelity, zero API barriers for hackathon execution, and authoritative Indian institutional trust.
        """
    )

    df_datasets = pd.DataFrame(DESIGNATED_DATASETS)
    df_datasets.columns = ["Climate Intelligence Task", "Best Pick (Primary)", "Why It Was Chosen", "Alternative / Backup", "Status"]
    
    st.dataframe(
        df_datasets,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    # Section 2: Deep-Dive Implementation Cards for Each Data Feed
    st.markdown("### 🔍 How Each Feed is Implemented in ClimateSense")

    tab1, tab2, tab3 = st.tabs(["⛅ Climatology & Water", "🛰️ Satellite Remote Sensing", "👥 Demographics, Disasters & Boundaries"])

    with tab1:
        st.markdown(
            """
            #### 1. Temperature, Humidity & Wind
            - **Best Pick:** **Open-Meteo Historical Weather API**
            - **Why:** Requires zero API keys or authentication, provides ERA5-grade atmospheric reanalysis with hourly and daily archives back to 1940.
            - **Query Example:** `https://archive-api.open-meteo.com/v1/archive?latitude=18.5204&longitude=73.8567&daily=temperature_2m_max,relative_humidity_2m_mean,wind_speed_10m_max`
            - **Backup:** NASA POWER (daily meteorology CSV).

            #### 2. Precipitation & Monsoon Cloudbursts
            - **Best Pick:** **Open-Meteo Historical API / IMD Gridded Rainfall**
            - **Why:** IMD (India Meteorological Department) 0.25° gridded daily rainfall provides official sovereign trust; Open-Meteo provides immediate ERA5 precipitation integrations without manual licensing.
            - **Backup:** CHIRPS 0.05° high-resolution rainfall or NASA POWER.
            """
        )

    with tab2:
        st.markdown(
            """
            #### 3. Vegetation Canopy (NDVI) for Carbon Accounting
            - **Best Pick:** **NASA AppEEARS (MODIS NDVI - MOD13Q1 / MYD13Q1)**
            - **Why:** Simply draw a polygon around Pune district on the AppEEARS web map to extract clean 250m 16-day time-series CSVs from 2000 to the present with zero coding.
            - **Backup:** Sentinel-2 via Google Earth Engine (GEE).

            #### 4. Land Surface Temperature (LST) for Urban Heat Risk
            - **Best Pick:** **MODIS LST via AppEEARS (MOD11A2)**
            - **Why:** Uses the exact same AppEEARS tool as NDVI, ensuring a unified processing pipeline for day/night 1km surface temperatures and thermal infrared anomalies.
            - **Backup:** Landsat 8/9 Thermal Infrared Sensor (TIRS) via Earth Engine.

            #### 5. Elevation and Slope for Flash-Flood Risk
            - **Best Pick:** **NASA SRTM 30m DEM via Google Earth Engine**
            - **Why:** A 5-line GEE script calculates elevation, terrain slope angle, and Topographic Wetness Index (TWI) across all Pune talukas.
            - **Backup:** Copernicus DEM or OpenTopography.

            #### 6. Land Cover (Built-Up vs Green Canopy)
            - **Best Pick:** **ESA WorldCover 10m**
            - **Why:** Clean, modern European Space Agency global land cover with simple, unambiguous classes (built-up, tree cover, cropland, water).
            - **Backup:** Dynamic World (near real-time 10m Sentinel-2 classification).

            #### 7. Tree Loss & Biomass Carbon Proxy
            - **Best Pick:** **Global Forest Watch (Hansen Global Forest Change)**
            - **Why:** Provides year-by-year forest and canopy cover loss (hectares) that converts directly to above-ground biomass carbon stock changes.
            - **Backup:** ESA CCI Biomass.
            """
        )

    with tab3:
        st.markdown(
            """
            #### 8. Population Exposure & Demographic Vulnerability
            - **Best Pick:** **WorldPop Gridded Population (100m Resolution)**
            - **Why:** Open, high-resolution spatial population counts that seamlessly join to Pune talukas, calculating the exact number of citizens exposed in high-risk zones.
            - **Backup:** Global Human Settlement Layer (GHSL).

            #### 9. Disaster Declarations & Validation Ground Truth
            - **Best Pick:** **EM-DAT International Disaster Database & Dartmouth Flood Observatory (DFO)**
            - **Why:** EM-DAT provides official disaster declaration records; Dartmouth Flood Observatory catalogs historical flood dates, satellite inundation extents, and affected river reaches along the Mula-Mutha.
            - **Backup:** Maharashtra State Disaster Management Authority (SDMA) incident reports.

            #### 10. Official Administrative Map Boundaries
            - **Best Pick:** **DataMeet (Indian Sub-District Shapefiles)**
            - **Why:** Built specifically for India by the DataMeet open geospatial community, correctly matching official Maharashtra taluka names, codes, and rural-urban delimitations.
            - **Backup:** GADM (Global Administrative Areas).
            """
        )

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    # Section 3: How to Swap Sample Data with Real Model Outputs
    st.markdown("### 🔄 How to Plug In Your Real Model Output (Zero Code Changes)")
    st.markdown(
        """
        The ClimateSense dashboard is built with a strictly decoupled architecture. All UI pages read from the `data/` folder.
        To replace the sample data with your real trained model output, follow these simple steps:
        """
    )

    st.code(
        """
# 1. Inspect the target folder:
data/
├── risk_predictions.csv      # Risk scores (0-1.0), levels (Low/Med/High), top factors & recommendations
├── ndvi_timeseries.csv       # 5-year monthly NDVI, green_cover_pct, vegetation_area_sqkm, carbon_stock_tco2e
├── feature_importance.csv    # Feature names, importance_score (SHAP), category, impact_direction
└── model_metrics.json        # Accuracy, precision, recall, f1_score, roc_auc, confusion matrix

# 2. Overwrite the files with your real model outputs using the same column names.
# 3. Refresh the browser tab or restart Streamlit:
streamlit run app.py
        """,
        language="bash"
    )

    with st.expander("📋 Click to view exact CSV column schema specifications"):
        st.markdown(
            """
            **1. `risk_predictions.csv` Columns:**
            - `date`: `YYYY-MM-01` (string or datetime)
            - `year`, `month`, `month_name`: Integer and 3-letter month (e.g., `2025`, `6`, `Jun`)
            - `area_id`: Area identifier (e.g., `PUN_01`)
            - `datameet_code`: Official DataMeet sub-district code (e.g., `DM_521_01`)
            - `area_name`: Name of the taluka (e.g., `Pune City (PMC)`)
            - `area_type`: Region classification (e.g., `Urban Core`, `Western Ghats`)
            - `latitude`, `longitude`: Float coordinates (e.g., `18.5204`, `73.8567`)
            - `elevation_m`, `slope_deg`: SRTM DEM terrain metrics
            - `worldpop_population`: WorldPop gridded resident count
            - `esa_builtup_pct`, `esa_green_pct`: ESA WorldCover surface fractions
            - `openmeteo_tmax_c`, `modis_lst_c`, `openmeteo_rh_pct`, `rainfall_24h_mm`: Environmental indicators
            - `hazard_type`: Hazard name (`Heatwave` or `Flood`)
            - `risk_score`: Numeric probability between `0.0` and `1.0`
            - `risk_level`: String (`Low`, `Medium`, or `High`)
            - `risk_lower_ci`, `risk_upper_ci`: Float 95% confidence interval bounds
            - `top_factor_1`, `top_factor_2`, `top_factor_3`: Text strings describing key risk drivers
            - `primary_recommendation`: Text string for suggested policy action
            - `disaster_validation_source`: EM-DAT / Dartmouth Flood Observatory reference
            - `is_forecast`: `0` for historical / evaluation, `1` for forward-looking forecast

            **2. `ndvi_timeseries.csv` Columns:**
            - `date`, `year`, `month`, `month_name`, `area_id`, `datameet_code`, `area_name`, `area_type`
            - `total_area_sqkm`: Total surface area
            - `worldpop_population`: Taluka resident count
            - `data_source_ndvi`: `NASA AppEEARS (MODIS NDVI - MOD13Q1)`
            - `data_source_carbon`: `Global Forest Watch (Hansen Tree Loss Proxy)`
            - `gfw_tree_cover_loss_ha_annual`: Annual canopy loss from Hansen dataset
            - `ndvi_mean`: Float between `0.0` and `1.0`
            - `green_cover_pct`: Float percentage (`0.0` to `100.0`)
            - `vegetation_area_sqkm`: Absolute canopy surface area in sq km
            - `carbon_stock_tco2e`: Estimated above-ground biomass carbon in metric tonnes CO₂e

            **3. `feature_importance.csv` Columns:**
            - `hazard_type`: `Heatwave` or `Flood`
            - `feature_name`: Display name of predictor
            - `data_source`: Designated source feed (e.g., `MODIS LST via AppEEARS`, `SRTM via GEE`)
            - `category`: Sensor or data family
            - `importance_score`: Mean absolute SHAP value or relative weight
            - `impact_direction`: `Increases Risk` or `Decreases Risk`
            - `description`: Plain-English physical explanation
            """
        )

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    # Section 4: Assumptions, Limitations & Future Scope
    col_lim, col_scope = st.columns(2)

    with col_lim:
        st.markdown("### ⚠️ Assumptions & Limitations")
        st.markdown(
            """
            <div style="background: #FFFBEB; border: 1px solid #FDE68A; border-radius: 8px; padding: 16px; font-size: 13px; color: #92400E; line-height: 1.5;">
                <ul style="margin: 0; padding-left: 18px;">
                    <li><strong>Biomass Carbon Proxy:</strong> Optical MODIS NDVI and GFW tree loss serve as empirical above-ground biomass proxies (IPCC Tier 1). Subterranean root carbon and soil microbial respiration are omitted for conservative accounting.</li>
                    <li><strong>Optical Cloud Occlusion:</strong> Peak monsoon optical imagery (July–August) experiences cloud cover, requiring radar cross-calibration (Sentinel-1 SAR) or historical climatology interpolation.</li>
                    <li><strong>Drainage Micro-Infrastructure:</strong> Sub-surface stormwater pipe dimensions and unauthorized solid waste blockages are modeled via topographic indices rather than subterranean GIS sensors.</li>
                    <li><strong>Baseline Calibration Mode:</strong> Current numbers are high-fidelity synthetic representations calibrated to Pune's published climatology and DataMeet boundaries.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_scope:
        st.markdown("### 🚀 Future Roadmap & Scaling")
        st.markdown(
            """
            <div style="background: #F0FDF4; border: 1px solid #BBF7D0; border-radius: 8px; padding: 16px; font-size: 13px; color: #166534; line-height: 1.5;">
                <ul style="margin: 0; padding-left: 18px;">
                    <li><strong>Sub-Ward Resolution:</strong> Downscale spatial resolution from 16 DataMeet talukas to PMC's 41 administrative prabhags and PCMC wards.</li>
                    <li><strong>Real-time IoT Drainage Telemetry:</strong> Ingest automated river water level sensors (Khadakwasla, Mutha river gauge) via MQTT webhooks.</li>
                    <li><strong>Carbon Credit Verification:</strong> Pair high-resolution tree canopy segmentation (SAM / YOLOv8 on 0.5m aerial imagery) to issue verifiable carbon credits.</li>
                    <li><strong>Citizen Alert SMS API:</strong> Integrate localized WhatsApp / SMS early-warning dispatches through the Maharashtra State Disaster Management Authority (SDMA).</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

    render_footer()


if __name__ == "__main__":
    main()
