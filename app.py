"""
app.py - ClimateSense: AI-driven Climate Risk + Carbon Monitoring Dashboard
Main Landing & Overview Page for Pune District, Maharashtra, India.
Designed for Hackathon Judges: Fast loading, visual clarity, presentation-ready.
Features interactive season toggles, real-time Taluka Spotlight, and What-If Action Simulator.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Set page config as the very first Streamlit command
st.set_page_config(
    page_title="ClimateSense | Pune Climate Risk & Carbon AI",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

from src.utils import (
    load_risk_data,
    load_ndvi_data,
    load_model_metrics,
    compute_overview_kpis,
    apply_clean_layout,
    COLOR_THEME,
    RISK_COLORS,
    DESIGNATED_DATASETS
)
from src.components import (
    render_header,
    render_kpi_card,
    render_takeaway,
    render_footer,
    get_risk_badge_html,
    create_risk_gauge
)

# Custom Clean CSS
st.markdown("""
<style>
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2.5rem;
    }
    /* Metric Card Modern Styling */
    div[data-testid="stMetricValue"] {
        font-size: 26px !important;
        font-weight: 800 !important;
    }
    /* Clean Radio buttons */
    div[role="radiogroup"] {
        background-color: #F1F5F9;
        padding: 4px;
        border-radius: 8px;
    }
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px;
        font-weight: 600;
        padding: 8px 16px;
    }
</style>
""", unsafe_allow_html=True)


def main():
    # Load Data dynamically from /data
    df_risk = load_risk_data()
    df_ndvi = load_ndvi_data()
    metrics = load_model_metrics()

    if df_risk.empty or df_ndvi.empty:
        st.warning("Data files are loading or not found in /data. Please verify CSV files.")
        return

    # Clean Header
    render_header(
        title="ClimateSense",
        subtitle="AI-driven Climate Risk + Carbon Monitoring for Pune District | 16 DataMeet Talukas"
    )

    # 1. INTERACTIVE SCENARIO & SEASON SELECTOR (Inline right at the top!)
    st.markdown("### 🎛️ Select Climate Observation Scenario")
    scenario_col1, scenario_col2 = st.columns([1.6, 1])

    with scenario_col1:
        scenario = st.radio(
            "Choose Climate Perspective",
            options=[
                "🔥 Peak Heatwave Window (Summer - May 2025)",
                "🌊 Peak Monsoon Flood Window (August 2025)",
                "📆 Baseline Annual Overview (Dec 2025)"
            ],
            index=0,
            horizontal=True,
            label_visibility="collapsed"
        )

    # Map scenario to date & hazard
    if "Heatwave" in scenario:
        selected_date = pd.to_datetime("2025-05-01")
        selected_hazard = "Heatwave"
        scenario_note = "Showing pre-monsoon thermal maximum (LST up to 43°C, Open-Meteo ambient temp >40°C, concrete UHI)."
    elif "Flood" in scenario:
        selected_date = pd.to_datetime("2025-08-01")
        selected_hazard = "Flood"
        scenario_note = "Showing peak monsoon precipitation (Open-Meteo / IMD rain >120mm/24h, Mula-Mutha river basin inundation)."
    else:
        selected_date = pd.to_datetime("2025-12-01")
        selected_hazard = None
        scenario_note = "Showing multi-hazard baseline with 5-year deseasonalized carbon accounting."

    with scenario_col2:
        st.caption(f"💡 **Active Context:** {scenario_note}")

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    # 2. THE 4 REFINED, CLEAR KPI CARDS
    kpis = compute_overview_kpis(df_risk, df_ndvi, selected_hazard=selected_hazard, selected_date=selected_date)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        pop_millions = kpis["high_risk_population"] / 1_000_000.0
        pop_subtext = f"~{pop_millions:.1f}M residents exposed" if pop_millions > 0 else "Low population stress"
        render_kpi_card(
            title="High-Risk Hotspots",
            value=f"{kpis['high_risk_count']} / {kpis['total_areas']} Areas",
            delta=f"{kpis['high_risk_pct']}% of district",
            subtext=f"Exposing {pop_subtext} (WorldPop)",
            alert_color=RISK_COLORS["High"] if kpis['high_risk_count'] > 2 else COLOR_THEME["emerald"],
            badge_text="Urgent" if kpis['high_risk_count'] > 2 else "Normal"
        )

    with c2:
        avg_score_text = f"{kpis['avg_risk_score']:.1f}%"
        risk_tier = "High Alert" if kpis['avg_risk_score'] >= 65 else ("Elevated" if kpis['avg_risk_score'] >= 45 else "Moderate")
        render_kpi_card(
            title="District Risk Index",
            value=avg_score_text,
            delta=risk_tier,
            subtext=f"Multi-hazard intensity score ({kpis['latest_date_str']})",
            alert_color=RISK_COLORS["High"] if kpis['avg_risk_score'] >= 60 else COLOR_THEME["teal_primary"],
            badge_text="0-100 Scale"
        )

    with c3:
        veg_delta_text = f"{kpis['green_cover_change_pct']:+.1f}%"
        render_kpi_card(
            title="5-Yr Canopy Loss",
            value=veg_delta_text,
            delta="Tree Cover Deficit",
            subtext="NASA AppEEARS & Global Forest Watch",
            alert_color=RISK_COLORS["High"] if kpis['green_cover_change_pct'] < 0 else COLOR_THEME["emerald"],
            badge_text="2021–2025"
        )

    with c4:
        carbon_val = f"{kpis['carbon_change_mt']:.2f} Mt"
        render_kpi_card(
            title="Biomass Carbon Deficit",
            value=f"{carbon_val}",
            delta=f"{kpis['carbon_change_pct']:+.1f}%",
            subtext="Estimated living canopy carbon loss (tCO₂e)",
            alert_color=RISK_COLORS["High"] if kpis['carbon_change_mt'] < 0 else COLOR_THEME["emerald"],
            badge_text="IPCC Tier 1"
        )

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    # 3. INTERACTIVE TALUKA SPOTLIGHT (The core user-friendly feature!)
    st.markdown("### 🔍 Interactive Taluka Diagnosis & Simulator")
    
    slice_df = df_risk[df_risk["date"] == selected_date]
    if selected_hazard:
        slice_df = slice_df[slice_df["hazard_type"] == selected_hazard]

    # Area selector
    area_options = slice_df.sort_values(by="risk_score", ascending=False)["area_name"].tolist()
    
    col_sel, col_sim = st.columns([1.2, 1])

    with col_sel:
        selected_taluka = st.selectbox(
            "👉 Select a Pune Taluka to inspect in real-time:",
            options=area_options,
            index=0,
            help="Choose any taluka to view localized satellite sensors and risk drivers."
        )

    with col_sim:
        sim_mitigation = st.slider(
            "⚡ What-If Simulator: Municipal Intervention Strength",
            min_value=0,
            max_value=35,
            value=0,
            step=5,
            format="+%d%% Greenery / Cool Roofs",
            help="Slide to simulate real-time risk reduction from deploying cool roofs and Miyawaki forests!"
        )

    # Get data for selected area
    taluka_data = slice_df[slice_df["area_name"] == selected_taluka].iloc[0]
    raw_risk = taluka_data["risk_score"]
    
    # Apply simulator reduction
    mitigated_risk = max(0.08, raw_risk * (1.0 - (sim_mitigation * 0.012)))
    level = "High" if mitigated_risk >= 0.65 else ("Medium" if mitigated_risk >= 0.40 else "Low")
    badge_html = get_risk_badge_html(level)

    # Layout: Radial Gauge on Left, Sensor Chips & Action on Right
    spot_col1, spot_col2 = st.columns([1, 1.6])

    with spot_col1:
        fig_gauge = create_risk_gauge(mitigated_risk, title=f"{selected_taluka}")
        st.plotly_chart(fig_gauge, use_container_width=True)
        if sim_mitigation > 0:
            st.success(f"🌱 Simulation Effect: Risk reduced by -{(raw_risk - mitigated_risk)*100:.1f}% through {sim_mitigation}% intervention expansion!")

    with spot_col2:
        # 4 Sensor Chips
        chip1, chip2, chip3, chip4 = st.columns(4)
        with chip1:
            st.metric("👥 Population", f"{taluka_data.get('worldpop_population', 0):,}", delta="WorldPop")
        with chip2:
            st.metric("🌡️ MODIS LST", f"{taluka_data.get('modis_lst_c', 'N/A')}°C", delta="AppEEARS")
        with chip3:
            st.metric("🌧️ 24h Rainfall", f"{taluka_data.get('rainfall_24h_mm', 'N/A')} mm", delta="Open-Meteo")
        with chip4:
            st.metric("🏙️ Built-up Area", f"{taluka_data.get('esa_builtup_pct', 'N/A')}%", delta="ESA WorldCover")

        # Top factors & Prescribed Action
        st.markdown(
            f"""
            <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 12px 16px; margin-top: 10px;">
                <div style="font-size: 12px; font-weight: 700; color: #0F172A; margin-bottom: 4px;">
                    📌 Top Risk Drivers:
                </div>
                <div style="font-size: 12px; color: #334155;">
                    1. <strong>{taluka_data['top_factor_1']}</strong> &nbsp;|&nbsp; 2. <strong>{taluka_data['top_factor_2']}</strong>
                </div>
                <div style="background: #F0FDFA; border-left: 3px solid #0D9488; padding: 8px 12px; border-radius: 4px; margin-top: 8px; font-size: 12.5px; color: #134E4A;">
                    🎯 <strong>Prescribed Municipal Action:</strong> {taluka_data['primary_recommendation']}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # 4. DISTRICT RISK RANKING (Clean & Interactive)
    st.markdown(f"### 📊 Full District Vulnerability Ranking ({kpis['latest_date_str']})")

    ranking_df = slice_df.groupby("area_name").agg({
        "risk_score": "max",
        "risk_level": "last",
        "worldpop_population": "first",
        "hazard_type": lambda x: "/".join(x.unique())
    }).reset_index().sort_values(by="risk_score", ascending=True)

    fig_bar = px.bar(
        ranking_df,
        x="risk_score",
        y="area_name",
        orientation="h",
        color="risk_level",
        color_discrete_map=RISK_COLORS,
        labels={"risk_score": "Predicted Risk Score (0–1.0)", "area_name": "DataMeet Taluka"},
        hover_data={"risk_score": ":.2f", "worldpop_population": ":,"}
    )
    fig_bar = apply_clean_layout(
        fig_bar,
        title=f"All 16 Talukas Ranked by Vulnerability ({kpis['latest_date_str']})",
        x_title="Severity Score",
        y_title="",
        height=420
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    render_takeaway(
        f"In {kpis['latest_date_str']}, {ranking_df.iloc[-1]['area_name']} faces the highest vulnerability score ({ranking_df.iloc[-1]['risk_score']*100:.1f}%), requiring priority deployment of municipal disaster teams."
    )

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    # 5. STREAMLINED HOW IT WORKS & VERIFIED DATA FEEDS EXPANDER
    with st.expander("ℹ️ Click to view the 10 Verified Datasets & System Architecture"):
        st.markdown(
            """
            | Data Task | Best Pick | Purpose |
            |---|---|---|
            | **1. Weather & Wind** | **Open-Meteo Historical API** | Real-time ERA5-quality atmospheric data without API keys |
            | **2. Monsoon Rain** | **Open-Meteo / IMD Gridded Rain** | Peak 24-hour rainfall intensity modeling |
            | **3. Vegetation (NDVI)** | **NASA AppEEARS (MODIS NDVI)** | 250m multi-year photosynthetic canopy health |
            | **4. Land Surface Temp** | **MODIS LST via AppEEARS** | 1km day/night surface thermal infrared anomalies |
            | **5. Elevation & Slope** | **SRTM via Google Earth Engine** | 30m Digital Elevation Model & Topographic Wetness Index |
            | **6. Land Cover** | **ESA WorldCover** | 10m high-resolution built-up vs vegetative land classification |
            | **7. Forest Loss** | **Global Forest Watch (Hansen)** | Year-by-year canopy loss for biomass carbon proxy accounting |
            | **8. Population Count** | **WorldPop Gridded Population** | 100m spatial demographics to assess human exposure |
            | **9. Disaster Ground-Truth** | **EM-DAT & Dartmouth Flood Observatory** | Historical flood and heatwave emergency validation |
            | **10. Boundaries** | **DataMeet Indian Sub-districts** | Official administrative taluka shapes for Pune |
            """
        )

    render_footer()


if __name__ == "__main__":
    main()
