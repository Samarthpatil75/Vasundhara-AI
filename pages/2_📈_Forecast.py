"""
pages/2_📈_Forecast.py - Multi-Month Forward Climate Risk Forecasting
Projects forward risk for 3-6 months with confidence bands and district benchmark comparisons.
Features inline taluka selectors, interactive horizons, and clear comparative charts.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

from src.utils import (
    load_risk_data,
    COLOR_THEME,
    RISK_COLORS,
    apply_clean_layout
)
from src.components import (
    render_header,
    render_takeaway,
    render_footer,
    get_risk_badge_html
)

st.set_page_config(
    page_title="Risk Forecast | ClimateSense Pune",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)


def main():
    render_header(
        title="Forward Predictive Risk Forecast",
        subtitle="3 to 6-month AI risk trajectory with 95% confidence bands and district benchmark comparisons"
    )

    df_risk = load_risk_data()
    if df_risk.empty:
        st.error("Risk prediction dataset is empty or not found.")
        return

    # Inline Interactive Controls
    st.markdown("### 🎛️ Forecast Configuration")
    fc_col1, fc_col2, fc_col3 = st.columns([1.4, 1.2, 1])

    all_areas = sorted(df_risk["area_name"].unique().tolist())
    with fc_col1:
        selected_area = st.selectbox(
            "Select Taluka / Area to Forecast",
            options=all_areas,
            index=0,
            help="Select an area to view historical trend and future risk forecast."
        )

    with fc_col2:
        selected_hazard = st.selectbox(
            "Select Hazard Mode",
            options=["Both Hazards", "Heatwave", "Flood"],
            index=0,
            help="Choose which hazard forecast to display."
        )

    with fc_col3:
        forecast_window = st.slider(
            "Forecast Horizon",
            min_value=3,
            max_value=6,
            value=6,
            step=1,
            format="%d Months"
        )

    hazards_to_plot = ["Heatwave", "Flood"] if selected_hazard == "Both Hazards" else [selected_hazard]

    forecast_start_date = df_risk[df_risk["is_forecast"] == 1]["date"].min()
    earliest_plot_date = forecast_start_date - pd.DateOffset(months=18)
    max_forecast_date = forecast_start_date + pd.DateOffset(months=forecast_window - 1)

    area_df = df_risk[
        (df_risk["area_name"] == selected_area) &
        (df_risk["date"] >= earliest_plot_date) &
        (df_risk["date"] <= max_forecast_date)
    ]

    district_avg = df_risk[
        (df_risk["date"] >= earliest_plot_date) &
        (df_risk["date"] <= max_forecast_date)
    ].groupby(["date", "hazard_type", "is_forecast"]).agg({
        "risk_score": "mean",
        "risk_lower_ci": "mean",
        "risk_upper_ci": "mean"
    }).reset_index()

    # 4 Quick Metric Cards
    latest_forecast_row = area_df[area_df["date"] == max_forecast_date]
    hz_row = latest_forecast_row[latest_forecast_row["hazard_type"] == hazards_to_plot[0]].iloc[0] if not latest_forecast_row.empty else None

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Forecast Horizon", max_forecast_date.strftime("%B %Y"), delta=f"+{forecast_window} Months Lead")
    with c2:
        if hz_row is not None:
            st.metric(
                f"{hazards_to_plot[0]} Projected Risk",
                f"{hz_row['risk_score']*100:.1f}%",
                delta=f"Alert: {hz_row['risk_level']}",
                delta_color="inverse" if hz_row['risk_level'] == "High" else "normal"
            )
        else:
            st.metric("Projected Risk", "N/A")
    with c3:
        if hz_row is not None:
            st.metric("95% Confidence Band", f"{hz_row['risk_lower_ci']*100:.0f}% – {hz_row['risk_upper_ci']*100:.0f}%", delta="Empirical Bayes")
        else:
            st.metric("Confidence Band", "N/A")
    with c4:
        dist_hz = district_avg[(district_avg["date"] == max_forecast_date) & (district_avg["hazard_type"] == hazards_to_plot[0])]
        if not dist_hz.empty and hz_row is not None:
            diff = (hz_row["risk_score"] - dist_hz["risk_score"].iloc[0]) * 100
            st.metric("vs Pune District Mean", f"{dist_hz['risk_score'].iloc[0]*100:.1f}%", delta=f"{diff:+.1f}% vs Mean", delta_color="inverse" if diff > 0 else "normal")
        else:
            st.metric("vs District Mean", "N/A")

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # 1. Main Forecast Line Chart with Confidence Interval
    st.markdown(f"#### 📈 Predicted Risk Trajectory & Confidence Envelope: **{selected_area}**")

    fig = go.Figure()
    palette = {
        "Heatwave": {"line": "#EF4444", "fill": "rgba(239, 68, 68, 0.15)", "dist": "#FCA5A5"},
        "Flood": {"line": "#0284C7", "fill": "rgba(2, 132, 199, 0.15)", "dist": "#93C5FD"}
    }

    for hz in hazards_to_plot:
        hz_area = area_df[area_df["hazard_type"] == hz].sort_values(by="date")
        hz_dist = district_avg[district_avg["hazard_type"] == hz].sort_values(by="date")
        colors = palette.get(hz, {"line": "#0D9488", "fill": "rgba(13,148,136,0.15)", "dist": "#99F6E4"})

        hist_part = hz_area[hz_area["is_forecast"] == 0]
        if not hist_part.empty:
            fig.add_trace(go.Scatter(
                x=hist_part["date"],
                y=hist_part["risk_score"] * 100,
                mode="lines+markers",
                name=f"{selected_area} ({hz} - Historical)",
                line=dict(color=colors["line"], width=2.5),
                marker=dict(size=4),
                hovertemplate="<b>%{x|%b %Y}</b><br>Historical: %{y:.1f}%<extra></extra>"
            ))

        fore_part = hz_area[hz_area["is_forecast"] == 1]
        if not fore_part.empty:
            bridge = pd.concat([hist_part.tail(1), fore_part]) if not hist_part.empty else fore_part

            fig.add_trace(go.Scatter(
                x=fore_part["date"],
                y=fore_part["risk_upper_ci"] * 100,
                mode="lines",
                line=dict(width=0),
                showlegend=False,
                hoverinfo="skip"
            ))

            fig.add_trace(go.Scatter(
                x=fore_part["date"],
                y=fore_part["risk_lower_ci"] * 100,
                mode="lines",
                line=dict(width=0),
                fill="tonexty",
                fillcolor=colors["fill"],
                name=f"{hz} 95% Confidence Band",
                hoverinfo="skip"
            ))

            fig.add_trace(go.Scatter(
                x=bridge["date"],
                y=bridge["risk_score"] * 100,
                mode="lines+markers",
                name=f"{selected_area} ({hz} - Forecast)",
                line=dict(color=colors["line"], width=3, dash="dot"),
                marker=dict(size=6, symbol="diamond"),
                hovertemplate="<b>%{x|%b %Y} [FORECAST]</b><br>Projected: %{y:.1f}%<extra></extra>"
            ))

        fig.add_trace(go.Scatter(
            x=hz_dist["date"],
            y=hz_dist["risk_score"] * 100,
            mode="lines",
            name=f"Pune District Mean ({hz})",
            line=dict(color=colors["dist"], width=1.8, dash="dash"),
            hovertemplate="<b>%{x|%b %Y}</b><br>Pune Mean: %{y:.1f}%<extra></extra>"
        ))

    fig.add_vline(
        x=forecast_start_date.timestamp() * 1000,
        line_width=1.5,
        line_dash="dash",
        line_color="#64748B",
        annotation_text="Forecast Start (2026)",
        annotation_position="top left",
        annotation_font=dict(size=11, color="#64748B")
    )
    fig.add_hline(y=65, line_width=1, line_dash="dot", line_color=RISK_COLORS["High"])
    fig.add_hline(y=40, line_width=1, line_dash="dot", line_color=RISK_COLORS["Medium"])

    fig = apply_clean_layout(
        fig,
        title=f"Multi-Month Risk Trajectory: {selected_area} vs Pune District Mean",
        x_title="Timeline (Historical + 2026 Forecast)",
        y_title="Risk Score (%)",
        height=440
    )
    st.plotly_chart(fig, use_container_width=True)

    render_takeaway(
        f"Early-warning forecast enables municipal agencies to anticipate seasonal risk peaks for {selected_area} up to 6 months in advance."
    )

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    # 2. Upcoming Quarter District Ranking
    st.markdown("#### ⚖️ District-Wide Upcoming Quarter Risk Ranking")
    quarter_dates = df_risk[
        (df_risk["is_forecast"] == 1) &
        (df_risk["date"] <= forecast_start_date + pd.DateOffset(months=3))
    ]
    if selected_hazard != "Both Hazards":
        quarter_dates = quarter_dates[quarter_dates["hazard_type"] == selected_hazard]

    quarter_summary = quarter_dates.groupby("area_name").agg({
        "risk_score": "mean",
        "risk_lower_ci": "mean",
        "risk_upper_ci": "mean",
        "worldpop_population": "first"
    }).reset_index().sort_values(by="risk_score", ascending=False)

    quarter_summary["Projected Risk (%)"] = (quarter_summary["risk_score"] * 100).round(1)

    fig_comp = px.bar(
        quarter_summary,
        x="area_name",
        y="Projected Risk (%)",
        color="Projected Risk (%)",
        color_continuous_scale=["#10B981", "#F59E0B", "#EF4444"],
        labels={"area_name": "DataMeet Taluka"},
        hover_data={"worldpop_population": ":,"}
    )
    fig_comp = apply_clean_layout(
        fig_comp,
        title="Upcoming Quarter Projected Risk Ranking (All 16 Talukas)",
        x_title="DataMeet Taluka",
        y_title="Projected Risk (%)",
        height=380,
        show_legend=False
    )
    st.plotly_chart(fig_comp, use_container_width=True)

    render_takeaway(
        "Quarterly ranking allows disaster response teams to pre-allocate municipal cooling centers, drainage excavation equipment, and emergency stockpiles weeks before extreme weather windows."
    )

    render_footer()


if __name__ == "__main__":
    main()
