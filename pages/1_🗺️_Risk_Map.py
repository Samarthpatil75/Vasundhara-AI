"""
pages/1_🗺️_Risk_Map.py - Interactive Climate Risk Map for Pune District
Core Feature: Geospatial visualization of Heatwave & Flood vulnerabilities across 16 DataMeet Pune talukas.
Optimized for instant interactivity, fast WebGL rendering, and intuitive click-to-inspect cards.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium

from src.utils import (
    load_risk_data,
    COLOR_THEME,
    RISK_COLORS,
    RISK_BG_COLORS,
    apply_clean_layout,
    apply_map_layout
)
from src.components import (
    render_header,
    render_kpi_card,
    render_interactive_taluka_indicators,
    render_takeaway,
    render_footer,
    get_risk_badge_html,
    create_risk_gauge
)

st.set_page_config(
    page_title="Risk Map | ClimateSense Pune",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


def main():
    render_header(
        title="Interactive Climate Risk Map",
        subtitle="Geospatial distribution of Heatwave and Flood hazards across 16 Pune district talukas"
    )

    df_risk = load_risk_data()
    if df_risk.empty:
        st.error("Risk prediction dataset is empty or not found.")
        return

    # 1. INLINE INTERACTIVE CONTROLS (Right at the top!)
    st.markdown("### 🎛️ Map Controls & Hazard Filters")
    ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([1.2, 1.2, 1])

    with ctrl_col1:
        hazard_type = st.radio(
            "Select Hazard",
            options=["🔥 Heatwave Vulnerability", "🌊 Flood Risk Index"],
            index=0,
            horizontal=True
        )
        selected_hazard = "Heatwave" if "Heatwave" in hazard_type else "Flood"

    all_dates = df_risk["date"].sort_values().unique()
    date_options = [pd.to_datetime(d).strftime("%B %Y") for d in all_dates]
    date_map = {pd.to_datetime(d).strftime("%B %Y"): pd.to_datetime(d) for d in all_dates}

    with ctrl_col2:
        # Default to peak month for chosen hazard
        default_month = "May 2025" if selected_hazard == "Heatwave" else "August 2025"
        default_idx = date_options.index(default_month) if default_month in date_options else len(date_options) - 7
        
        selected_date_str = st.selectbox(
            "Observation Month (Historical & 2026 Forecast)",
            options=date_options,
            index=default_idx
        )
        selected_date = date_map[selected_date_str]

    with ctrl_col3:
        map_mode = st.radio(
            "Display Engine",
            options=["⚡ Plotly Fast Map", "🗺️ Folium Tiles"],
            index=0,
            horizontal=True
        )

    # Filter Dataset
    filtered_df = df_risk[
        (df_risk["hazard_type"] == selected_hazard) &
        (df_risk["date"] == selected_date)
    ].copy()

    if filtered_df.empty:
        st.info("No data available for this filter combination. Please select another month.")
        return

    is_forecast_period = filtered_df["is_forecast"].iloc[0] == 1
    if is_forecast_period:
        st.info(f"🔮 **2026 Forward AI Forecast** active for {selected_date_str}. Values include Open-Meteo lead signals.")

    # Top summary metrics strip
    avg_score = filtered_df["risk_score"].mean() * 100
    high_count = (filtered_df["risk_level"] == "High").sum()
    total_pop_exp = filtered_df[filtered_df["risk_level"] == "High"]["worldpop_population"].sum()

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        render_kpi_card(
            title="Surveyed Talukas",
            value=f"{len(filtered_df)} / 16",
            delta="Complete Coverage",
            subtext="DataMeet Official Pune Admin Boundaries",
            alert_color=COLOR_THEME["teal_primary"],
            badge_text="Spatial Scope"
        )
    with m2:
        render_kpi_card(
            title="Average Risk Score",
            value=f"{avg_score:.1f}%",
            delta="District Mean",
            subtext=f"Composite hazard severity ({selected_hazard})",
            alert_color=RISK_COLORS["High"] if avg_score >= 60 else COLOR_THEME["teal_primary"],
            badge_text="0–100 Scale"
        )
    with m3:
        render_kpi_card(
            title="High-Risk Hotspots",
            value=f"{high_count} Talukas",
            delta="Urgent Alert" if high_count > 0 else "Optimal",
            subtext="Zones exceeding danger threshold (≥65%)",
            alert_color=RISK_COLORS["High"] if high_count > 0 else COLOR_THEME["emerald"],
            badge_text="Urgent" if high_count > 0 else "Normal"
        )
    with m4:
        render_kpi_card(
            title="Exposed Population",
            value=f"{total_pop_exp/1e6:.2f}M",
            delta="WorldPop 100m",
            subtext="Gridded population residing in high-risk zones",
            alert_color=RISK_COLORS["High"] if total_pop_exp > 0 else COLOR_THEME["emerald"],
            badge_text="Human Exposure"
        )

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # 2. MAIN MAP & INSPECTOR LAYOUT
    map_col, inspect_col = st.columns([1.5, 1])

    with map_col:
        st.markdown(f"#### 📍 Spatial Severity Map ({selected_hazard} • {selected_date_str})")

        if "Plotly" in map_mode:
            try:
                # Modern Plotly 5.24+ / 6.0+ MapLibre open-source (no token required!)
                fig_map = px.scatter_map(
                    filtered_df,
                    lat="latitude",
                    lon="longitude",
                    size="risk_score",
                    color="risk_level",
                    color_discrete_map=RISK_COLORS,
                    hover_name="area_name",
                    hover_data={
                        "risk_score": ":.2f",
                        "worldpop_population": ":,",
                        "modis_lst_c": ":.1f",
                        "rainfall_24h_mm": ":.1f",
                        "top_factor_1": True,
                        "latitude": False,
                        "longitude": False
                    },
                    size_max=28,
                    zoom=8.5,
                    center=dict(lat=18.5204, lon=73.8567),
                    map_style="open-street-map"
                )
            except Exception:
                # Fallback to scatter_mapbox with open-street-map
                fig_map = px.scatter_mapbox(
                    filtered_df,
                    lat="latitude",
                    lon="longitude",
                    size="risk_score",
                    color="risk_level",
                    color_discrete_map=RISK_COLORS,
                    hover_name="area_name",
                    hover_data={
                        "risk_score": True,
                        "top_factor_1": True,
                        "latitude": False,
                        "longitude": False
                    },
                    size_max=28,
                    zoom=8.5,
                    center=dict(lat=18.5204, lon=73.8567),
                    mapbox_style="open-street-map"
                )
            fig_map = apply_map_layout(fig_map, height=480)
            st.plotly_chart(fig_map, use_container_width=True)
        else:
            pune_center = [18.5204, 73.8567]
            fmap = folium.Map(location=pune_center, zoom_start=9, tiles="OpenStreetMap", control_scale=True)
            for _, row in filtered_df.iterrows():
                level = row["risk_level"]
                color = RISK_COLORS.get(level, "#64748B")
                score_pct = row["risk_score"] * 100
                radius = 10 + (row["risk_score"] * 16)
                pop_formatted = f"{row.get('worldpop_population', 0):,}"

                popup_html = f"""
                <div style="font-family: Inter, sans-serif; min-width: 230px;">
                    <strong>{row['area_name']}</strong> ({row['area_type']})<br>
                    <span style="color: {color}; font-weight: 800; font-size: 14px;">Risk: {score_pct:.1f}% ({level})</span><br>
                    👥 Pop: {pop_formatted} | 🌡️ LST: {row.get('modis_lst_c', 'N/A')}°C<br>
                    🌧️ Rain: {row.get('rainfall_24h_mm', 'N/A')} mm<br>
                    <div style="margin-top:6px; font-size:11px; background:#F8FAFC; padding:4px;">
                        • {row['top_factor_1']}
                    </div>
                </div>
                """
                folium.CircleMarker(
                    location=[row["latitude"], row["longitude"]],
                    radius=radius,
                    color=color,
                    weight=2,
                    fill=True,
                    fill_color=color,
                    fill_opacity=0.65,
                    popup=folium.Popup(popup_html, max_width=300),
                    tooltip=f"{row['area_name']}: {score_pct:.1f}% ({level})"
                ).add_to(fmap)
            st_folium(fmap, use_container_width=True, height=480, returned_objects=[])

        render_takeaway(
            f"{selected_hazard} severity clusters heavily in specific micro-corridors. Toggle areas on the right to see immediate policy actions."
        )

    with inspect_col:
        st.markdown("#### 🔍 Area Risk Inspector")
        sorted_areas = filtered_df.sort_values(by="risk_score", ascending=False)["area_name"].tolist()

        selected_inspect = st.selectbox(
            "Select Area to Inspect:",
            options=sorted_areas,
            index=0
        )

        area_row = filtered_df[filtered_df["area_name"] == selected_inspect].iloc[0]
        score_val = area_row["risk_score"]
        level = area_row["risk_level"]
        badge_html = get_risk_badge_html(level)

        # Radial Gauge
        fig_g = create_risk_gauge(score_val, title=f"{selected_inspect}")
        st.plotly_chart(fig_g, use_container_width=True)

        # Interactive Multi-Sensor Telemetry Deck (Compact Mode)
        render_interactive_taluka_indicators(
            taluka_data=area_row,
            selected_taluka=selected_inspect,
            sim_mitigation=0,
            is_compact=True
        )

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    # 3. SORTABLE AREA REGISTER TABLE
    st.markdown("#### 📋 Taluka Risk Register")
    table_df = filtered_df[[
        "area_name", "datameet_code", "area_type", "hazard_type", "risk_score", "risk_level",
        "worldpop_population", "modis_lst_c", "rainfall_24h_mm", "top_factor_1", "primary_recommendation"
    ]].copy()

    table_df["risk_score_pct"] = (table_df["risk_score"] * 100).round(1).astype(str) + "%"
    table_df["worldpop_population"] = table_df["worldpop_population"].apply(lambda x: f"{x:,}")

    table_df.rename(columns={
        "area_name": "DataMeet Taluka",
        "datameet_code": "Code",
        "area_type": "Classification",
        "hazard_type": "Hazard",
        "risk_score_pct": "Risk Score",
        "risk_level": "Alert Tier",
        "worldpop_population": "Population (WorldPop)",
        "modis_lst_c": "LST (°C)",
        "rainfall_24h_mm": "Rain (mm)",
        "top_factor_1": "Primary Risk Trigger",
        "primary_recommendation": "Prescribed Policy Action"
    }, inplace=True)

    st.dataframe(
        table_df[[
            "DataMeet Taluka", "Classification", "Hazard", "Risk Score",
            "Alert Tier", "Population (WorldPop)", "LST (°C)", "Rain (mm)", "Primary Risk Trigger", "Prescribed Policy Action"
        ]].sort_values(by="Risk Score", ascending=False),
        use_container_width=True,
        hide_index=True
    )

    render_footer()


if __name__ == "__main__":
    main()
