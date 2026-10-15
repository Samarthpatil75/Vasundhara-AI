"""
pages/5_🛡️_Recommended_Actions.py - Automated Climate Resilience Action Blueprint
Prioritized interventions, municipal action plans, and emergency mitigation tasklists for high-risk Pune talukas.
Weighted by WorldPop demographic exposure and Global Forest Watch canopy loss targets.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from src.utils import (
    load_risk_data,
    load_ndvi_data,
    COLOR_THEME,
    RISK_COLORS,
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
    page_title="Action Blueprint | ClimateSense Pune",
    page_icon="🛡️",
    layout="wide"
)

ACTION_CATALOG = {
    "Heatwave": {
        "High": [
            {"tier": "Immediate (0–30 Days)", "action": "Deploy high-albedo reflective cool roof coatings on municipal schools, transit shelters, and low-income settlements.", "lead_agency": "PMC/PCMC Disaster Mgmt Cell"},
            {"tier": "Immediate (0–30 Days)", "action": "Issue targeted SMS extreme heat advisories to outdoor laborers; enforce 12 PM–3 PM work halts during heatwave red alerts.", "lead_agency": "District Labour Dept"},
            {"tier": "Seasonal Prep (1–3 Months)", "action": "Install 25 solar-powered public drinking water kiosks and mist cooling shelters near congested transit hubs (Swargate, Pune Station, Shivaji Nagar).", "lead_agency": "Smart City Mission"},
            {"tier": "Long-Term (6–12 Months)", "action": "Mandate Miyawaki dense micro-forests in all new commercial layouts > 2 hectares to reverse Global Forest Watch canopy deficits.", "lead_agency": "PMRDA & State Forest Dept"}
        ],
        "Medium": [
            {"tier": "Immediate (0–30 Days)", "action": "Distribute electrolyte ORS packets at urban primary healthcare centers (UPHCs) and establish shaded transit pit stops.", "lead_agency": "District Health Office"},
            {"tier": "Seasonal Prep (1–3 Months)", "action": "Perform thermal infrared drone surveys to identify asphalt heat islands and schedule nocturnal road mist spraying.", "lead_agency": "PMC Environment Cell"},
            {"tier": "Long-Term (6–12 Months)", "action": "Incentivize rooftop terrace gardens with a 5% municipal property tax rebate.", "lead_agency": "Municipal Revenue Dept"}
        ],
        "Low": [
            {"tier": "Monitoring", "action": "Maintain routine AppEEARS satellite vegetative health checks and preserve existing peri-urban agricultural buffers.", "lead_agency": "Social Forestry Division"}
        ]
    },
    "Flood": {
        "High": [
            {"tier": "Immediate (0–30 Days)", "action": "Mobilize mechanized hydraulic excavators to desilt critical culverts along Mula, Mutha, and Indrayani drainage nallahs; remove plastic blockages.", "lead_agency": "PMC/PCMC Drainage & Sewerage Dept"},
            {"tier": "Immediate (0–30 Days)", "action": "Calibrate and activate ultrasonic water-level IoT telemetry on low-lying causeways (e.g., Baba Bhide bridge) with automated sirens.", "lead_agency": "Irrigation Dept & Traffic Police"},
            {"tier": "Seasonal Prep (1–3 Months)", "action": "Designate flood shelter relief camps with backup generators, rescue boats, and rations in Dartmouth Flood Observatory inundation zones.", "lead_agency": "District Collectorate"},
            {"tier": "Long-Term (6–12 Months)", "action": "Construct decentralized bioswales and permeable soak-pits; enforce strict no-construction buffers within the blue flood line.", "lead_agency": "Town Planning Dept & PMRDA"}
        ],
        "Medium": [
            {"tier": "Immediate (0–30 Days)", "action": "Inspect arterial roadside storm channels, clear construction debris, and ensure functional backwater flap valves.", "lead_agency": "Roads & Maintenance Dept"},
            {"tier": "Seasonal Prep (1–3 Months)", "action": "Restore riverbank riparian vegetation and plant deep-root Vetiver grass along vulnerable canal slopes to prevent bank scouring.", "lead_agency": "State Forest Dept"},
            {"tier": "Long-Term (6–12 Months)", "action": "Retrofit public grounds and open plazas with subterranean rainwater recharge percolation tanks.", "lead_agency": "GSDA"}
        ],
        "Low": [
            {"tier": "Monitoring", "action": "Coordinate seasonal reservoir discharge schedules between upstream Khadakwasla / Mulshi dams and downstream catchment authorities.", "lead_agency": "Water Resources Dept"}
        ]
    }
}


def main():
    render_header(
        title="Automated Climate Resilience Action Blueprint",
        subtitle="Prioritized intervention matrices, municipal tasklists, and risk-reduction roadmaps"
    )
    render_sample_data_banner()

    df_risk = load_risk_data()
    df_ndvi = load_ndvi_data()

    if df_risk.empty:
        st.error("Risk prediction dataset is empty or not found.")
        return

    hist_risk = df_risk[df_risk["is_forecast"] == 0]
    latest_date = hist_risk["date"].max() if not hist_risk.empty else df_risk["date"].max()
    active_risk = df_risk[df_risk["date"] == latest_date].copy()

    with st.sidebar:
        st.markdown("### 🎯 Action Plan Filters")
        
        selected_hazard = st.selectbox(
            "Select Hazard Focus",
            options=["Both Hazards", "Heatwave", "Flood"],
            index=0,
            help="Filter actions by primary climate hazard."
        )

        filter_priority = st.radio(
            "Priority Filter",
            options=["All Areas", "High Risk Areas Only (Urgent)", "Medium & High Risk"],
            index=1,
            help="Focus specifically on regions exceeding intervention thresholds."
        )

        st.markdown("---")
        st.caption("ℹ️ *Actions are automatically generated based on model-detected feature triggers and WorldPop demographic exposure.*")

    hazard_filtered = active_risk if selected_hazard == "Both Hazards" else active_risk[active_risk["hazard_type"] == selected_hazard]

    if filter_priority == "High Risk Areas Only (Urgent)":
        display_risk = hazard_filtered[hazard_filtered["risk_level"] == "High"]
    elif filter_priority == "Medium & High Risk":
        display_risk = hazard_filtered[hazard_filtered["risk_level"].isin(["High", "Medium"])]
    else:
        display_risk = hazard_filtered

    if display_risk.empty:
        st.info("No areas currently meet this filter threshold. Try selecting 'All Areas' or 'Medium & High Risk'.")
        return

    priority_ranking = display_risk.groupby("area_name").agg({
        "risk_score": "max",
        "risk_level": "last",
        "hazard_type": lambda x: ", ".join(sorted(x.unique())),
        "area_type": "first",
        "datameet_code": "first",
        "worldpop_population": "first",
        "top_factor_1": "first",
        "top_factor_2": "first",
        "primary_recommendation": "first"
    }).reset_index()

    priority_ranking["Priority Rank"] = priority_ranking["risk_score"].rank(ascending=False, method="min").astype(int)
    priority_ranking = priority_ranking.sort_values(by="Priority Rank")

    # 1. Priority Ranking Chart
    st.markdown("#### 🥇 District Priority Intervention Ranking (Urgency Index)")

    fig_rank = px.bar(
        priority_ranking,
        x="risk_score",
        y="area_name",
        orientation="h",
        color="risk_level",
        color_discrete_map=RISK_COLORS,
        text=priority_ranking["Priority Rank"].apply(lambda r: f"Rank #{r}"),
        labels={"risk_score": "Composite Risk Score (0–1.0)", "area_name": "DataMeet Taluka"},
        hover_data={"risk_score": ":.2f", "worldpop_population": ":,", "hazard_type": True, "top_factor_1": True}
    )
    fig_rank.update_traces(textposition="outside")
    fig_rank = apply_clean_layout(
        fig_rank,
        title="Municipal Priority Ranking: Areas Requiring Immediate Action",
        x_title="Severity Score",
        y_title="",
        height=400
    )
    st.plotly_chart(fig_rank, use_container_width=True)

    render_takeaway(
        f"Taluka Rank #1 is {priority_ranking.iloc[0]['area_name']} with a severity score of {priority_ranking.iloc[0]['risk_score']*100:.1f}%, directly impacting ~{priority_ranking.iloc[0]['worldpop_population']:,} residents (WorldPop)."
    )

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    # 2. Area Action Blueprint Accordion Cards
    st.markdown("#### 🛠️ Granular Area Action Blueprints")
    st.caption("Expand any taluka card below to inspect the phased intervention roadmap.")

    for _, row in priority_ranking.iterrows():
        area_name = row["area_name"]
        level = row["risk_level"]
        badge_html = get_risk_badge_html(level)
        hz = row["hazard_type"]
        rank_no = row["Priority Rank"]
        pop_fmt = f"{row.get('worldpop_population', 0):,}"

        primary_hz = "Heatwave" if "Heatwave" in hz else "Flood"
        actions = ACTION_CATALOG.get(primary_hz, {}).get(level, ACTION_CATALOG[primary_hz]["Medium"])

        with st.expander(f"📍 Rank #{rank_no}: {area_name} — {level} Risk ({row['risk_score']*100:.1f}%) | Pop: {pop_fmt}", expanded=(rank_no <= 3)):
            st.markdown(
                f"""
                <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #E2E8F0; padding-bottom: 8px; margin-bottom: 12px;">
                    <div>
                        <strong style="color: #0F172A; font-size: 15px;">{area_name}</strong>
                        <span style="color: #64748B; font-size: 13px; margin-left: 8px;">({row['area_type']} • Code: {row.get('datameet_code', 'N/A')})</span>
                    </div>
                    <div>
                        <span style="font-size: 12px; font-weight: 600; color: #64748B; margin-right: 8px;">Hazards: {hz}</span>
                        {badge_html}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 6px; padding: 10px 14px; margin-bottom: 14px; font-size: 12.5px;">
                    <strong>Primary Triggers:</strong> 1. {row['top_factor_1']} | 2. {row['top_factor_2']}<br>
                    <strong>Exposed Demographics:</strong> {pop_fmt} residents (WorldPop 100m gridded aggregation)
                </div>
                """,
                unsafe_allow_html=True
            )

            act_df = pd.DataFrame(actions)
            act_df.columns = ["Timeframe / Urgency", "Prescribed Intervention Action", "Responsible Municipal Agency"]
            st.table(act_df)

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    # 3. Export Action Plan
    st.markdown("#### 📥 Export Priority Action Plan for Municipal Agencies")
    
    export_rows = []
    for _, row in priority_ranking.iterrows():
        area_name = row["area_name"]
        level = row["risk_level"]
        primary_hz = "Heatwave" if "Heatwave" in row["hazard_type"] else "Flood"
        actions = ACTION_CATALOG.get(primary_hz, {}).get(level, ACTION_CATALOG[primary_hz]["Medium"])
        for act in actions:
            export_rows.append({
                "Priority Rank": row["Priority Rank"],
                "DataMeet Taluka": area_name,
                "Taluka Code": row.get("datameet_code", "N/A"),
                "Zone Type": row["area_type"],
                "WorldPop Population": row.get("worldpop_population", 0),
                "Risk Score (%)": f"{row['risk_score']*100:.1f}%",
                "Alert Level": level,
                "Hazard Focus": row["hazard_type"],
                "Timeframe": act["tier"],
                "Action Description": act["action"],
                "Lead Agency": act["lead_agency"]
            })

    export_df = pd.DataFrame(export_rows)
    csv_bytes = export_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📄 Download Pune Climate Action Plan (CSV)",
        data=csv_bytes,
        file_name="pune_climate_action_plan.csv",
        mime="text/csv",
        help="Export full action matrix for PMC, PCMC, PMRDA, and District Collectorate briefings."
    )

    render_footer()


if __name__ == "__main__":
    main()
