"""
pages/3_🌱_Carbon_Monitor.py - Satellite Green Cover & Biomass Carbon Accounting
5-year NDVI time-series analysis, canopy loss ranking, and vegetation carbon stock tracking.
Powered by NASA AppEEARS (MODIS NDVI) and Global Forest Watch (Hansen Tree Cover Loss).
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from src.utils import (
    load_ndvi_data,
    compute_area_vegetation_loss,
    COLOR_THEME,
    RISK_COLORS,
    apply_clean_layout
)
from src.components import (
    render_header,
    render_takeaway,
    render_footer,
    render_kpi_card
)

st.set_page_config(
    page_title="Carbon Monitor | ClimateSense Pune",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)


def main():
    render_header(
        title="Vegetation & Carbon Sink Monitoring",
        subtitle="5-Year satellite NDVI dynamics and biomass carbon stock accounting across Pune district"
    )

    df_ndvi = load_ndvi_data()
    if df_ndvi.empty:
        st.error("NDVI time-series dataset is empty or not found.")
        return

    # Mandatory visible carbon proxy note
    st.info(
        "🌿 **Carbon Accounting Framework Notice:** *\"Proxy estimate based on vegetation change; assumptions listed below.\"* "
        "Canopy density derived from **NASA AppEEARS (MODIS NDVI - MOD13Q1)** combined with **Global Forest Watch (Hansen)** annual tree loss."
    )

    loss_summary = compute_area_vegetation_loss(df_ndvi)

    total_start_veg = loss_summary["start_veg_sqkm"].sum()
    total_end_veg = loss_summary["end_veg_sqkm"].sum()
    net_veg_change = total_end_veg - total_start_veg
    net_veg_pct = (net_veg_change / total_start_veg) * 100

    total_start_c = loss_summary["start_carbon"].sum()
    total_end_c = loss_summary["end_carbon"].sum()
    net_c_change = total_end_c - total_start_c
    net_c_pct = (net_c_change / total_start_c) * 100
    net_c_mt = net_c_change / 1_000_000.0

    # 4 Clean Metric Cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_kpi_card(
            title="Total Canopy Cover",
            value=f"{total_end_veg:,.0f} km²",
            delta=f"{net_veg_pct:+.1f}% (5-Yr)",
            subtext="Current active district vegetation footprint",
            alert_color=COLOR_THEME["teal_primary"],
            badge_text="Dec 2025"
        )
    with c2:
        render_kpi_card(
            title="Net Canopy Deficit",
            value=f"{abs(net_veg_change):,.1f} km²",
            delta="5-Yr Loss",
            subtext="Cumulative green surface deficit since 2021",
            alert_color=RISK_COLORS["High"] if net_veg_change < 0 else COLOR_THEME["emerald"],
            badge_text="Canopy Lost"
        )
    with c3:
        render_kpi_card(
            title="Active Carbon Stock",
            value=f"{total_end_c/1e6:.2f} Mt",
            delta="Living Biomass",
            subtext="Estimated above-ground biomass carbon",
            alert_color=COLOR_THEME["teal_dark"],
            badge_text="Mt CO₂e"
        )
    with c4:
        render_kpi_card(
            title="Net Carbon Delta",
            value=f"{net_c_mt:.2f} Mt",
            delta=f"{net_c_pct:+.1f}%",
            subtext="Equivalent atmospheric sequestration lost",
            alert_color=RISK_COLORS["High"] if net_c_change < 0 else COLOR_THEME["emerald"],
            badge_text="Mt CO₂e"
        )

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    # Inline Interactive Controls
    st.markdown("### 🌲 Compare Regional Canopy & Carbon Trajectories")
    cm_col1, cm_col2 = st.columns([1.5, 1])

    all_areas = sorted(df_ndvi["area_name"].unique().tolist())
    default_selected = [
        "Pune City (PMC)",
        "Haveli (Hadapsar/Katraj)",
        "Pimpri-Chinchwad (PCMC)",
        "Hinjawadi IT Corridor",
        "Mulshi (Paud/Lavasa)"
    ]
    default_selected = [a for a in default_selected if a in all_areas]

    with cm_col1:
        selected_areas = st.multiselect(
            "Select Talukas to Compare:",
            options=all_areas,
            default=default_selected,
            help="Compare NDVI trajectories across urban, peri-urban, and Ghats zones."
        )

    with cm_col2:
        metric_view = st.radio(
            "Select Display Metric",
            options=["Mean NDVI Index (AppEEARS)", "Green Cover Area (km²)", "Biomass Carbon (Mt CO₂e)"],
            index=0,
            horizontal=True
        )

    if not selected_areas:
        st.warning("Please select at least one taluka above.")
        return

    # 1. 5-Year Time Series Chart
    st.markdown(f"#### 🛰️ 5-Year {metric_view} Trajectory (2021 – 2025)")

    fig_trend = go.Figure()

    for area in selected_areas:
        sub = df_ndvi[df_ndvi["area_name"] == area].sort_values(by="date")
        if "Carbon" in metric_view:
            y_vals = sub["carbon_stock_tco2e"] / 1e6
            hover_fmt = "%{y:.3f} Mt"
        elif "Area" in metric_view:
            y_vals = sub["vegetation_area_sqkm"]
            hover_fmt = "%{y:,.1f} km²"
        else:
            y_vals = sub["ndvi_mean"]
            hover_fmt = "%{y:.3f}"

        fig_trend.add_trace(go.Scatter(
            x=sub["date"],
            y=y_vals,
            mode="lines",
            name=area,
            line=dict(width=2.2),
            hovertemplate=f"<b>{area}</b><br>%{{x|%b %Y}}<br>{metric_view}: {hover_fmt}<extra></extra>"
        ))

    # Add Pune District Mean
    if "Carbon" in metric_view:
        dist_y = df_ndvi.groupby("date")["carbon_stock_tco2e"].mean() / 1e6
    elif "Area" in metric_view:
        dist_y = df_ndvi.groupby("date")["vegetation_area_sqkm"].mean()
    else:
        dist_y = df_ndvi.groupby("date")["ndvi_mean"].mean()

    fig_trend.add_trace(go.Scatter(
        x=dist_y.index,
        y=dist_y.values,
        mode="lines",
        name="Pune District Mean",
        line=dict(color="#0F172A", width=2.8, dash="dash")
    ))

    fig_trend = apply_clean_layout(
        fig_trend,
        title=f"Monthly {metric_view} Trends (NASA AppEEARS MODIS)",
        x_title="Observation Month",
        y_title=metric_view,
        height=420
    )
    st.plotly_chart(fig_trend, use_container_width=True)

    render_takeaway(
        "Strong seasonal oscillations reflect monsoon greening (July–October), but urbanizing centers (PMC, PCMC, Hinjawadi) show secular multi-year declines in dry-season baseline canopy."
    )

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    # 2. Top 8 Canopy Loss Ranking
    st.markdown("#### 🚨 Top 8 Regions by 5-Year Green Cover Loss")

    top_loss = loss_summary.head(8).copy()

    fig_loss = px.bar(
        top_loss,
        x="veg_change_pct",
        y="area_name",
        orientation="h",
        color="veg_change_pct",
        color_continuous_scale=["#EF4444", "#F59E0B", "#10B981"],
        labels={"veg_change_pct": "Green Cover Change (%)", "area_name": "DataMeet Taluka"},
        hover_data={"start_veg_sqkm": ":.1f", "end_veg_sqkm": ":.1f", "carbon_change_tco2e": ":,.0f"}
    )
    fig_loss = apply_clean_layout(
        fig_loss,
        title="Top 8 Regions by Green Cover Loss Percentage (2021 vs 2025 Annual Mean)",
        x_title="Canopy Change Percentage (%)",
        y_title="",
        height=360,
        show_legend=False
    )
    st.plotly_chart(fig_loss, use_container_width=True)

    render_takeaway(
        f"Rapid built infrastructure has driven {top_loss.iloc[0]['area_name']} to lose {abs(top_loss.iloc[0]['veg_change_pct']):.1f}% of its vegetation canopy, accelerating the localized Urban Heat Island."
    )

    # 3. Assumptions Expander
    with st.expander("📖 Click to inspect IPCC Tier 1 & Global Forest Watch Model Assumptions"):
        st.markdown(
            """
            - **NASA AppEEARS MODIS NDVI (MOD13Q1):** 250m 16-day composites extracted over the Pune polygon boundary.
            - **Global Forest Watch (Hansen Tree Loss):** Annual tree cover loss (ha) grounds multi-year deforestation trends.
            - **Biomass Expansion Factor:** Standard **IPCC Tier 1 Guidelines** applying 75.0 metric tonnes CO₂e per km² of sustained canopy.
            """
        )

    render_footer()


if __name__ == "__main__":
    main()
