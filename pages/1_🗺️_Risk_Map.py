"""
pages/1_🗺️_Risk_Map.py - Interactive Climate Risk Map for Pune District
Core Feature: Spatial visualization of Heatwave & Flood vulnerabilities across 16 DataMeet Pune talukas.
Driven by Open-Meteo, IMD, NASA AppEEARS (MODIS LST), SRTM GEE, ESA WorldCover, and WorldPop demographics.
"""

import streamlit as st
import pandas as pd
import folium
from folium import plugins
from streamlit_folium import st_folium
import plotly.express as px

from src.utils import (
    load_risk_data,
    COLOR_THEME,
    RISK_COLORS,
    RISK_BG_COLORS,
    apply_clean_layout
)
from src.components import (
    render_header,
    render_sample_data_banner,
    render_takeaway,
    render_footer,
    get_risk_badge_html
)

st.set_page_config(
    page_title="Risk Map | ClimateSense Pune",
    page_icon="🗺️",
    layout="wide"
)


def main():
    render_header(
        title="Interactive Climate Risk Map",
        subtitle="Geospatial distribution of Heatwave and Flood hazards across Pune district talukas"
    )
    render_sample_data_banner()

    df_risk = load_risk_data()
    if df_risk.empty:
        st.error("Risk prediction dataset is empty or not found.")
        return

    available_hazards = sorted(df_risk["hazard_type"].unique().tolist())
    all_dates = df_risk["date"].sort_values().unique()
    date_options = [pd.to_datetime(d).strftime("%B %Y") for d in all_dates]
    date_map = {pd.to_datetime(d).strftime("%B %Y"): pd.to_datetime(d) for d in all_dates}
    
    hist_dates = df_risk[df_risk["is_forecast"] == 0]["date"].sort_values().unique()
    latest_hist_str = pd.to_datetime(hist_dates[-1]).strftime("%B %Y") if len(hist_dates) > 0 else date_options[-1]
    default_date_idx = date_options.index(latest_hist_str) if latest_hist_str in date_options else len(date_options) - 1

    # Sidebar Filters
    with st.sidebar:
        st.markdown("### 🎛️ Map Controls & Filters")
        
        selected_hazard = st.selectbox(
            "Select Hazard Type",
            options=available_hazards,
            index=0,
            help="Switch between urban heatwave vulnerability and monsoon flood risk."
        )

        selected_date_str = st.selectbox(
            "Select Timeline Period",
            options=date_options,
            index=default_date_idx,
            help="Select historical month or future forecast horizon."
        )
        selected_date = date_map[selected_date_str]

        selected_levels = st.multiselect(
            "Filter by Risk Level",
            options=["Low", "Medium", "High"],
            default=["Low", "Medium", "High"],
            help="Filter displayed areas by predicted severity level."
        )

        map_engine = st.radio(
            "Map Engine",
            options=["Folium Interactive Map", "Plotly Satellite/Scatter Map"],
            index=0,
            horizontal=True
        )

        st.markdown("---")
        st.caption("ℹ️ *Boundaries: DataMeet Indian Sub-districts. Demographic weights: WorldPop 2024.*")

    filtered_df = df_risk[
        (df_risk["hazard_type"] == selected_hazard) &
        (df_risk["date"] == selected_date)
    ]

    if selected_levels:
        filtered_df = filtered_df[filtered_df["risk_level"].isin(selected_levels)]

    if filtered_df.empty:
        st.info("No areas match your current filter combination. Please expand your Risk Level selection in the sidebar.")
        return

    is_forecast_period = filtered_df["is_forecast"].iloc[0] == 1
    if is_forecast_period:
        st.info(f"🔮 **Viewing 2026 Forward AI Forecast** for {selected_date_str}. Risk scores incorporate Open-Meteo climate lead indicators and seasonal shifts.")

    # Top summary metrics strip
    avg_score = filtered_df["risk_score"].mean() * 100
    high_count = (filtered_df["risk_level"] == "High").sum()
    total_pop_exp = filtered_df[filtered_df["risk_level"] == "High"]["worldpop_population"].sum() if "worldpop_population" in filtered_df.columns else 0

    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    with m_col1:
        st.metric("Filtered Talukas", f"{len(filtered_df)} / {df_risk['area_name'].nunique()}")
    with m_col2:
        st.metric("Slice Avg Risk Score", f"{avg_score:.1f}%")
    with m_col3:
        st.metric("High Risk Hotspots", f"{high_count} talukas", delta="Urgent Intervention", delta_color="inverse")
    with m_col4:
        st.metric("Exposed Population", f"{total_pop_exp/1e6:.2f}M", delta="WorldPop Gridded")

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # Layout: Map on left (70%), Area Inspector on right (30%)
    map_col, detail_col = st.columns([1.5, 0.9])

    with map_col:
        st.markdown(f"#### 📍 Spatial Risk Distribution ({selected_hazard} - {selected_date_str})")

        if map_engine == "Folium Interactive Map":
            pune_center = [18.5204, 73.8567]
            fmap = folium.Map(
                location=pune_center,
                zoom_start=9,
                tiles="CartoDB positron",
                control_scale=True
            )

            for _, row in filtered_df.iterrows():
                level = row["risk_level"]
                color = RISK_COLORS.get(level, "#64748B")
                score_pct = row["risk_score"] * 100
                radius = 10 + (row["risk_score"] * 16)

                pop_formatted = f"{row.get('worldpop_population', 0):,}"
                lst_val = f"{row.get('modis_lst_c', 'N/A')}°C"
                rain_val = f"{row.get('rainfall_24h_mm', 'N/A')} mm"
                elev_val = f"{row.get('elevation_m', 'N/A')} m"

                popup_html = f"""
                <div style="font-family: Inter, sans-serif; min-width: 250px; padding: 4px;">
                    <div style="font-weight: 700; font-size: 14px; color: #0F172A; margin-bottom: 2px;">
                        {row['area_name']}
                    </div>
                    <div style="font-size: 11px; color: #64748B; margin-bottom: 6px;">
                        {row['area_type']} • Code: {row.get('datameet_code', 'N/A')}
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <span style="font-size: 12px; font-weight: 600;">Risk Score:</span>
                        <span style="font-size: 13px; font-weight: 800; color: {color};">
                            {score_pct:.1f}% ({level})
                        </span>
                    </div>
                    <div style="font-size: 11px; color: #334155; margin-bottom: 6px;">
                        👥 <strong>WorldPop Population:</strong> {pop_formatted}<br>
                        🌡️ <strong>MODIS LST:</strong> {lst_val} | 🌧️ <strong>Rain (24h):</strong> {rain_val}<br>
                        ⛰️ <strong>SRTM Elevation:</strong> {elev_val}
                    </div>
                    <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 4px; padding: 6px; font-size: 11px; margin-bottom: 8px;">
                        <strong>Key Trigger:</strong> {row['top_factor_1']}
                    </div>
                    <div style="border-top: 1px solid #E2E8F0; padding-top: 6px; font-size: 11px; color: #0D9488;">
                        <strong>Prescribed Action:</strong> {row['primary_recommendation'][:90]}...
                    </div>
                </div>
                """

                tooltip_text = f"{row['area_name']} | Risk: {score_pct:.1f}% ({level}) | Pop: {pop_formatted}"

                folium.CircleMarker(
                    location=[row["latitude"], row["longitude"]],
                    radius=radius,
                    color=color,
                    weight=2,
                    fill=True,
                    fill_color=color,
                    fill_opacity=0.65,
                    popup=folium.Popup(popup_html, max_width=320),
                    tooltip=tooltip_text
                ).add_to(fmap)

            st_folium(fmap, width="100%", height=500, returned_objects=[])

        else:
            fig_map = px.scatter_mapbox(
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
                    "top_factor_1": True,
                    "latitude": False,
                    "longitude": False
                },
                size_max=28,
                zoom=8.5,
                center=dict(lat=18.5204, lon=73.8567),
                mapbox_style="carto-positron",
                title=f"Pune {selected_hazard} Risk Intensity"
            )
            fig_map = apply_clean_layout(fig_map, height=500, show_legend=True)
            st.plotly_chart(fig_map, use_container_width=True)

        render_takeaway(
            f"Spatial clustering confirms {selected_hazard} exposure is highest in dense urban centers (Pune City, PCMC) and specialized geographic corridors, requiring localized micro-interventions."
        )

    with detail_col:
        st.markdown("#### 🔍 Area Risk Inspector")
        area_options = filtered_df["area_name"].tolist()
        sorted_areas = filtered_df.sort_values(by="risk_score", ascending=False)["area_name"].tolist()

        inspect_area = st.selectbox(
            "Select Taluka / Area to Inspect",
            options=sorted_areas,
            index=0,
            help="View localized contributing factors and recommendations."
        )

        area_row = filtered_df[filtered_df["area_name"] == inspect_area].iloc[0]
        level = area_row["risk_level"]
        badge_html = get_risk_badge_html(level)
        score_val = area_row["risk_score"] * 100

        st.markdown(
            f"""
            <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <div>
                        <h3 style="margin: 0; font-size: 17px; color: #0F172A;">{area_row['area_name']}</h3>
                        <span style="font-size: 12px; color: #64748B;">{area_row['area_type']} • Code: {area_row.get('datameet_code', 'N/A')}</span>
                    </div>
                    <div>{badge_html}</div>
                </div>

                <div style="margin: 10px 0; background: #F8FAFC; border-radius: 6px; padding: 10px 14px; border: 1px solid #E2E8F0;">
                    <div style="font-size: 11px; color: #64748B; font-weight: 600; text-transform: uppercase;">
                        Model Predicted Risk Score
                    </div>
                    <div style="font-size: 24px; font-weight: 800; color: {RISK_COLORS.get(level)};">
                        {score_val:.1f}%
                        <span style="font-size: 12px; font-weight: normal; color: #64748B;">
                            (95% CI: {area_row['risk_lower_ci']*100:.0f}% – {area_row['risk_upper_ci']*100:.0f}%)
                        </span>
                    </div>
                </div>

                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 12px; font-size: 11.5px;">
                    <div style="background: #F1F5F9; padding: 6px 8px; border-radius: 4px;">
                        <strong>👥 WorldPop:</strong> {area_row.get('worldpop_population', 0):,}
                    </div>
                    <div style="background: #F1F5F9; padding: 6px 8px; border-radius: 4px;">
                        <strong>🌡️ MODIS LST:</strong> {area_row.get('modis_lst_c', 'N/A')}°C
                    </div>
                    <div style="background: #F1F5F9; padding: 6px 8px; border-radius: 4px;">
                        <strong>🌧️ Rain (24h):</strong> {area_row.get('rainfall_24h_mm', 'N/A')} mm
                    </div>
                    <div style="background: #F1F5F9; padding: 6px 8px; border-radius: 4px;">
                        <strong>⛰️ SRTM Elev:</strong> {area_row.get('elevation_m', 'N/A')} m
                    </div>
                </div>

                <div style="margin-top: 10px;">
                    <div style="font-size: 12px; font-weight: 700; color: #0F172A; margin-bottom: 4px;">
                        📌 Top 3 Contributing Risk Drivers:
                    </div>
                    <ul style="margin: 0; padding-left: 18px; font-size: 12px; color: #334155; line-height: 1.45;">
                        <li><strong>1.</strong> {area_row['top_factor_1']}</li>
                        <li><strong>2.</strong> {area_row['top_factor_2']}</li>
                        <li><strong>3.</strong> {area_row['top_factor_3']}</li>
                    </ul>
                </div>

                <div style="margin-top: 10px; background: #F0FDFA; border-left: 3px solid #0D9488; padding: 8px 10px; border-radius: 4px;">
                    <div style="font-size: 11px; font-weight: 700; color: #0F766E; text-transform: uppercase;">
                        🎯 Recommended Intervention:
                    </div>
                    <div style="font-size: 12px; color: #134E4A; margin-top: 3px; line-height: 1.35;">
                        {area_row['primary_recommendation']}
                    </div>
                </div>

                <div style="margin-top: 8px; font-size: 11px; color: #64748B;">
                    <strong>Validation Record:</strong> {area_row.get('disaster_validation_source', 'None')}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    # Sortable Data Table
    st.markdown("#### 📋 Comprehensive Area Risk Register (Pune District)")
    table_display = filtered_df[[
        "area_name", "datameet_code", "area_type", "hazard_type", "risk_score", "risk_level",
        "worldpop_population", "modis_lst_c", "rainfall_24h_mm", "top_factor_1", "primary_recommendation"
    ]].copy()

    table_display["risk_score_pct"] = (table_display["risk_score"] * 100).round(1).astype(str) + "%"
    table_display["worldpop_population"] = table_display["worldpop_population"].apply(lambda x: f"{x:,}")

    table_display.rename(columns={
        "area_name": "DataMeet Taluka",
        "datameet_code": "Taluka Code",
        "area_type": "Classification",
        "hazard_type": "Hazard",
        "risk_score_pct": "Risk Score",
        "risk_level": "Alert Level",
        "worldpop_population": "Exposed Pop (WorldPop)",
        "modis_lst_c": "MODIS LST (°C)",
        "rainfall_24h_mm": "Rain 24h (mm)",
        "top_factor_1": "Primary Risk Driver",
        "primary_recommendation": "Prescribed Action"
    }, inplace=True)

    st.dataframe(
        table_display[[
            "DataMeet Taluka", "Taluka Code", "Classification", "Hazard", "Risk Score",
            "Alert Level", "Exposed Pop (WorldPop)", "MODIS LST (°C)", "Rain 24h (mm)", "Primary Risk Driver", "Prescribed Action"
        ]].sort_values(by="Risk Score", ascending=False),
        use_container_width=True,
        hide_index=True
    )

    render_takeaway(
        f"Sortable registry enables disaster management officers to quickly rank all 16 talukas and export priority intervention rosters for municipal coordination."
    )

    render_footer()


if __name__ == "__main__":
    main()
