"""
components.py - Reusable, polished UI components for ClimateSense dashboard.
Crafted for hackathon judges: crisp layout, presentation-grade cards, and clear visual cues.
Strictly grounded in the 10 designated climate, satellite, and demographic datasets.
"""

import streamlit as st
from src.utils import COLOR_THEME, RISK_COLORS, RISK_BG_COLORS, DESIGNATED_DATASETS


def render_header(title: str = "ClimateSense", subtitle: str = "AI-Driven Climate Risk & Carbon Monitoring | Pune District"):
    """Renders top header badge with Pune district tag and live status."""
    st.markdown(
        f"""
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #E2E8F0; padding-bottom: 12px; margin-bottom: 18px;">
            <div>
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 26px;">🌍</span>
                    <h1 style="margin: 0; font-size: 28px; font-weight: 800; color: #0F172A; letter-spacing: -0.5px; font-family: Inter, sans-serif;">
                        {title}
                    </h1>
                    <span style="background: #E6FFFA; color: #0D9488; font-size: 11px; font-weight: 700; padding: 3px 8px; border-radius: 9999px; border: 1px solid #99F6E4; text-transform: uppercase;">
                        DataMeet Boundaries • Pune District
                    </span>
                </div>
                <p style="margin: 4px 0 0 0; color: #64748B; font-size: 13.5px; font-weight: 400;">
                    {subtitle}
                </p>
            </div>
            <div style="text-align: right;">
                <span style="display: inline-flex; align-items: center; gap: 6px; background: #FEF3C7; color: #92400E; font-size: 12px; font-weight: 600; padding: 4px 10px; border-radius: 6px; border: 1px solid #FDE68A;">
                    <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #D97706;"></span>
                    Sample Baseline Mode
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_sample_data_banner():
    """Renders prominent, professional disclosure banner for judges."""
    st.markdown(
        """
        <div style="background-color: #F8FAFC; border-left: 4px solid #0D9488; border-right: 1px solid #E2E8F0; border-top: 1px solid #E2E8F0; border-bottom: 1px solid #E2E8F0; padding: 11px 16px; border-radius: 6px; margin-bottom: 20px; display: flex; align-items: center; justify-content: space-between;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <span style="font-size: 20px;">ℹ️</span>
                <div>
                    <strong style="color: #0F172A; font-size: 13px;">Data Architecture: Calibrated Sample Pipeline Active</strong>
                    <div style="color: #475569; font-size: 12px; margin-top: 2px;">
                        Standardized to 10 authorized feeds (Open-Meteo, IMD, AppEEARS MODIS NDVI/LST, GEE SRTM, ESA WorldCover, Global Forest Watch, WorldPop, EM-DAT/DFO, DataMeet). Drop updated CSVs into <code>/data</code> to refresh live without changing UI code.
                    </div>
                </div>
            </div>
            <div style="white-space: nowrap; margin-left: 16px;">
                <span style="background: #0D9488; color: white; padding: 4px 10px; border-radius: 4px; font-size: 11px; font-weight: 600;">
                    10 Datasets Integrated
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_designated_datasets_pill_bar():
    """Renders an interactive quick pill-bar showcasing the 10 designated datasets."""
    pills = [
        "⛅ Open-Meteo (Temp/Wind)",
        "🌧️ IMD / Open-Meteo Rain",
        "🌱 AppEEARS MODIS NDVI",
        "🔥 MODIS LST (Heat)",
        "⛰️ SRTM via GEE",
        "🏙️ ESA WorldCover",
        "🌲 Global Forest Watch",
        "👥 WorldPop Exposure",
        "🌊 EM-DAT / DFO Floods",
        "🗺️ DataMeet Boundaries"
    ]
    pills_html = " ".join([
        f'<span style="display: inline-block; background: #FFFFFF; border: 1px solid #E2E8F0; color: #334155; font-size: 11px; font-weight: 600; padding: 3px 8px; border-radius: 6px; margin: 2px 4px 2px 0;">{p}</span>'
        for p in pills
    ])
    st.markdown(
        f"""
        <div style="background: #F1F5F9; border-radius: 8px; padding: 8px 12px; margin-bottom: 20px; display: flex; align-items: center; flex-wrap: wrap;">
            <span style="font-size: 11px; font-weight: 800; color: #0F766E; text-transform: uppercase; margin-right: 10px; letter-spacing: 0.5px;">
                Verified Feeds:
            </span>
            {pills_html}
        </div>
        """,
        unsafe_allow_html=True
    )


def render_kpi_card(
    title: str,
    value: str,
    delta: str = "",
    subtext: str = "",
    alert_color: str = "#0D9488",
    badge_text: str = ""
):
    """Renders a card for top-line metrics."""
    delta_markup = ""
    if delta:
        delta_color = "#EF4444" if "-" in delta or "High" in delta or "Urgent" in delta else "#10B981"
        delta_markup = f"""
        <span style="color: {delta_color}; font-size: 12px; font-weight: 600; background: #F8FAFC; padding: 2px 6px; border-radius: 4px; border: 1px solid #E2E8F0;">
            {delta}
        </span>
        """

    badge_markup = ""
    if badge_text:
        badge_markup = f"""
        <span style="background: #F1F5F9; color: #475569; font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 9999px;">
            {badge_text}
        </span>
        """

    card_html = f"""
    <div style="background: #FFFFFF; border-radius: 10px; padding: 18px 20px; border: 1px solid #E2E8F0; box-shadow: 0 1px 3px rgba(0,0,0,0.05); height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
            <span style="color: #64748B; font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">
                {title}
            </span>
            {badge_markup}
        </div>
        <div style="display: flex; align-items: baseline; gap: 10px; margin: 4px 0 6px 0;">
            <span style="color: {alert_color}; font-size: 30px; font-weight: 800; font-family: Inter, sans-serif; letter-spacing: -1px;">
                {value}
            </span>
            {delta_markup}
        </div>
        <div style="color: #94A3B8; font-size: 12px; font-weight: 400; border-top: 1px solid #F8FAFC; padding-top: 8px; margin-top: 4px;">
            {subtext}
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)


def render_takeaway(takeaway_text: str):
    """Renders mandatory one-line plain-English takeaway under charts."""
    st.markdown(
        f"""
        <div style="background-color: #F0FDFA; border-left: 3px solid #0D9488; padding: 8px 14px; border-radius: 4px; margin-top: 8px; margin-bottom: 18px;">
            <span style="color: #0F766E; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">
                💡 Key Takeaway:
            </span>
            <span style="color: #134E4A; font-size: 13px; font-weight: 500; margin-left: 6px;">
                {takeaway_text}
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_how_it_works():
    """Renders the 4-step 'How it works' strip grounded in the designated datasets."""
    steps = [
        {
            "icon": "📡",
            "step": "01. Multi-Feed Ingestion",
            "desc": "Open-Meteo, IMD rain, NASA AppEEARS (MODIS NDVI/LST), SRTM GEE, ESA WorldCover & WorldPop demographics."
        },
        {
            "icon": "⚡",
            "step": "02. Validated ML Ensemble",
            "desc": "XGBoost + SHAP explainers cross-validated against EM-DAT declarations and Dartmouth Flood Observatory events."
        },
        {
            "icon": "🗺️",
            "step": "03. DataMeet Boundary Map",
            "desc": "16 Pune sub-districts classified into Low, Medium, High risk with live contributing factor weights."
        },
        {
            "icon": "🛡️",
            "step": "04. Targeted Municipal Action",
            "desc": "Prioritized interventions (cool roofs, canal desilting, mist shelters) weighted by WorldPop exposed populations."
        }
    ]

    cols = st.columns(4)
    for col, s in zip(cols, steps):
        with col:
            col_html = f"""
            <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 14px; height: 100%; border-top: 3px solid #0D9488;">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                    <span style="font-size: 20px;">{s['icon']}</span>
                    <strong style="color: #0F172A; font-size: 13px;">{s['step']}</strong>
                </div>
                <p style="color: #64748B; font-size: 12px; margin: 0; line-height: 1.4;">
                    {s['desc']}
                </p>
            </div>
            """
            st.markdown(col_html, unsafe_allow_html=True)


def get_risk_badge_html(level: str) -> str:
    """Returns HTML badge for risk levels."""
    color = RISK_COLORS.get(level, "#64748B")
    bg = RISK_BG_COLORS.get(level, "#F1F5F9")
    return f"""
    <span style="background-color: {bg}; color: {color}; font-weight: 700; padding: 3px 9px; border-radius: 9999px; font-size: 11.5px; border: 1px solid {color}40; display: inline-block;">
        ● {level} Risk
    </span>
    """


def render_footer():
    """Renders persistent footer."""
    st.markdown(
        """
        <div style="margin-top: 50px; border-top: 1px solid #E2E8F0; padding-top: 18px; padding-bottom: 24px; text-align: center; color: #94A3B8; font-size: 12px;">
            <div style="display: flex; justify-content: center; align-items: center; gap: 16px; margin-bottom: 6px;">
                <span><strong>ClimateSense</strong> Pune District Risk Intelligence</span>
                <span>•</span>
                <span style="color: #0D9488; font-weight: 600;">Hackathon Prototype</span>
                <span>•</span>
                <span>Theme: AI/ML & Data-Driven Climate Prediction</span>
            </div>
            <div>
                Designated Datasets: Open-Meteo, IMD, NASA AppEEARS (MODIS NDVI & LST), SRTM GEE, ESA WorldCover, Global Forest Watch (Hansen), WorldPop, EM-DAT/DFO, DataMeet.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
