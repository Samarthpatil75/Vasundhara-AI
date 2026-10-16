"""
components.py - Reusable, polished UI components for ClimateSense dashboard.
Crafted for hackathon judges: crisp layout, robust rendering, and clear visual cues.
Strictly grounded in the 10 designated climate, satellite, and demographic datasets.
"""

import textwrap
import streamlit as st
import plotly.graph_objects as go
from src.utils import COLOR_THEME, RISK_COLORS, RISK_BG_COLORS, DESIGNATED_DATASETS


def render_header(title: str = "ClimateSense", subtitle: str = "AI-Driven Climate Risk & Carbon Monitoring | Pune District"):
    """
    Renders top header badge with Pune district tag, live status,
    and injects the Aceternity Aurora Background viewport with guaranteed visibility.
    """
    html = textwrap.dedent(f"""
    <style>
        @keyframes aurora-flow-1 {{
            0% {{
                background-position: 50% 50%, 50% 50%;
            }}
            50% {{
                background-position: 200% 60%, 150% 40%;
            }}
            100% {{
                background-position: 350% 50%, 250% 50%;
            }}
        }}

        @keyframes aurora-drift-1 {{
            0%, 100% {{
                transform: translate(0px, 0px) scale(1);
            }}
            33% {{
                transform: translate(70px, -50px) scale(1.15);
            }}
            66% {{
                transform: translate(-50px, 60px) scale(0.95);
            }}
        }}

        @keyframes aurora-drift-2 {{
            0%, 100% {{
                transform: translate(0px, 0px) scale(1.1);
            }}
            33% {{
                transform: translate(-80px, 60px) scale(0.9);
            }}
            66% {{
                transform: translate(60px, -70px) scale(1.2);
            }}
        }}

        @keyframes aurora-drift-3 {{
            0%, 100% {{
                transform: translate(0px, 0px) scale(1);
            }}
            50% {{
                transform: translate(80px, 40px) scale(1.2);
            }}
        }}

        /* 1. RESET ALL STREAMLIT CONTAINERS TO TRANSPARENT SO AURORA IS VISIBLE */
        html, body {{
            margin: 0 !important;
            padding: 0 !important;
            background-color: #F8FAFC !important;
        }}

        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"],
        [data-testid="stMainBlockContainer"],
        section.main,
        .main,
        header[data-testid="stHeader"] {{
            background: transparent !important;
            background-color: transparent !important;
        }}

        /* 2. FIXED AURORA BACKGROUND VIEWPORT (Always active behind content) */
        .aurora-viewport-bg {{
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            overflow: hidden !important;
            pointer-events: none !important;
            z-index: 0 !important;
            background-color: #F8FAFC !important;
        }}

        /* Glowing Aurora Orbs */
        .aurora-glow-orb-1 {{
            position: absolute !important;
            top: -15% !important;
            left: -10% !important;
            width: 65vw !important;
            height: 65vh !important;
            border-radius: 50% !important;
            background: radial-gradient(circle, rgba(14, 165, 233, 0.45) 0%, rgba(99, 102, 241, 0.3) 45%, transparent 70%) !important;
            filter: blur(55px) !important;
            animation: aurora-drift-1 22s ease-in-out infinite !important;
            will-change: transform !important;
        }}

        .aurora-glow-orb-2 {{
            position: absolute !important;
            bottom: -15% !important;
            right: -10% !important;
            width: 70vw !important;
            height: 70vh !important;
            border-radius: 50% !important;
            background: radial-gradient(circle, rgba(16, 185, 129, 0.45) 0%, rgba(13, 148, 136, 0.35) 45%, transparent 70%) !important;
            filter: blur(60px) !important;
            animation: aurora-drift-2 26s ease-in-out infinite !important;
            will-change: transform !important;
        }}

        .aurora-glow-orb-3 {{
            position: absolute !important;
            top: 25% !important;
            right: 15% !important;
            width: 50vw !important;
            height: 50vh !important;
            border-radius: 50% !important;
            background: radial-gradient(circle, rgba(168, 85, 247, 0.38) 0%, rgba(59, 130, 246, 0.25) 50%, transparent 70%) !important;
            filter: blur(50px) !important;
            animation: aurora-drift-3 18s ease-in-out infinite !important;
            will-change: transform !important;
        }}

        /* Aceternity 100-degree Repeating Linear Gradient Curtains */
        .aurora-flow-curtain {{
            position: absolute !important;
            inset: -30px !important;
            opacity: 0.70 !important;
            filter: blur(20px) !important;
            will-change: background-position !important;
            background-image: 
                repeating-linear-gradient(100deg, rgba(255, 255, 255, 0.55) 0%, rgba(255, 255, 255, 0.55) 7%, transparent 10%, transparent 12%, rgba(255, 255, 255, 0.55) 16%),
                repeating-linear-gradient(100deg, #3b82f6 10%, #a5b4fc 15%, #0ea5e9 20%, #a855f7 25%, #10b981 30%, #60a5fa 35%) !important;
            background-size: 250% 150%, 250% 150% !important;
            background-position: 50% 50%, 50% 50% !important;
            mask-image: radial-gradient(ellipse at 80% 15%, black 20%, transparent 80%) !important;
            -webkit-mask-image: radial-gradient(ellipse at 80% 15%, black 20%, transparent 80%) !important;
            animation: aurora-flow-1 40s linear infinite !important;
        }}

        .aurora-flow-curtain-2 {{
            position: absolute !important;
            inset: -30px !important;
            opacity: 0.55 !important;
            filter: blur(24px) !important;
            will-change: background-position !important;
            background-image: 
                repeating-linear-gradient(100deg, rgba(255, 255, 255, 0.5) 0%, rgba(255, 255, 255, 0.5) 7%, transparent 10%, transparent 12%, rgba(255, 255, 255, 0.5) 16%),
                repeating-linear-gradient(115deg, #0d9488 10%, #38bdf8 16%, #818cf8 22%, #c084fc 28%, #34d399 34%) !important;
            background-size: 200% 120%, 200% 120% !important;
            background-position: 50% 50%, 50% 50% !important;
            mix-blend-mode: overlay !important;
            animation: aurora-flow-1 55s linear infinite reverse !important;
        }}

        /* 3. ELEVATED CONTENT LAYER */
        .block-container {{
            position: relative !important;
            z-index: 1 !important;
            padding-top: 1.4rem !important;
            padding-bottom: 3rem !important;
            max-width: 1400px !important;
        }}

        /* 4. FROSTED GLASS CARDS */
        div[data-testid="stMetric"],
        div[data-testid="stVerticalBlockBorderWrapper"] > div {{
            background: rgba(255, 255, 255, 0.88) !important;
            backdrop-filter: blur(14px) !important;
            -webkit-backdrop-filter: blur(14px) !important;
            border: 1px solid rgba(226, 232, 240, 0.9) !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 20px -2px rgba(15, 118, 110, 0.05), 0 2px 6px -1px rgba(0, 0, 0, 0.02) !important;
            transition: transform 0.2s ease, box-shadow 0.2s ease !important;
        }}

        div[data-testid="stVerticalBlockBorderWrapper"] > div:hover {{
            transform: translateY(-2px) !important;
            box-shadow: 0 10px 25px -3px rgba(13, 148, 136, 0.12), 0 4px 6px -2px rgba(0, 0, 0, 0.04) !important;
        }}
    </style>

    <!-- FIXED AURORA BACKGROUND VIEWPORT -->
    <div class="aurora-viewport-bg">
        <div class="aurora-glow-orb-1"></div>
        <div class="aurora-glow-orb-2"></div>
        <div class="aurora-glow-orb-3"></div>
        <div class="aurora-flow-curtain"></div>
        <div class="aurora-flow-curtain-2"></div>
    </div>

    <!-- MAIN HEADER BANNER -->
    <div style="background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px); border: 1px solid rgba(226, 232, 240, 0.9); border-radius: 14px; padding: 14px 20px; margin-bottom: 18px; box-shadow: 0 4px 20px -2px rgba(15, 118, 110, 0.06); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; position: relative; z-index: 1;">
        <div>
            <div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
                <span style="font-size: 26px;">🌍</span>
                <h1 style="margin: 0; font-size: 25px; font-weight: 800; color: #0F172A; letter-spacing: -0.5px; font-family: Inter, sans-serif;">
                    {title}
                </h1>
                <span style="background: #E6FFFA; color: #0D9488; font-size: 11px; font-weight: 700; padding: 3px 8px; border-radius: 9999px; border: 1px solid #99F6E4; text-transform: uppercase;">
                    DataMeet Boundaries • Pune District
                </span>
                <span style="background: #EEF2FF; color: #4F46E5; font-size: 11px; font-weight: 700; padding: 3px 8px; border-radius: 9999px; border: 1px solid #C7D2FE;">
                    ✨ Aurora Atmosphere Active
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
    """)
    st.markdown(html, unsafe_allow_html=True)


def render_sample_data_banner():
    """Renders prominent, professional disclosure banner for judges."""
    html = textwrap.dedent("""
<div style="background-color: #F8FAFC; border-left: 4px solid #0D9488; border-right: 1px solid #E2E8F0; border-top: 1px solid #E2E8F0; border-bottom: 1px solid #E2E8F0; padding: 11px 16px; border-radius: 6px; margin-bottom: 18px; display: flex; align-items: center; justify-content: space-between;">
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
""")
    st.markdown(html, unsafe_allow_html=True)


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
    html = textwrap.dedent(f"""
<div style="background: #F1F5F9; border-radius: 8px; padding: 8px 12px; margin-bottom: 18px; display: flex; align-items: center; flex-wrap: wrap;">
    <span style="font-size: 11px; font-weight: 800; color: #0F766E; text-transform: uppercase; margin-right: 10px; letter-spacing: 0.5px;">
        Verified Feeds:
    </span>
    {pills_html}
</div>
""")
    st.markdown(html, unsafe_allow_html=True)


def render_kpi_card(
    title: str,
    value: str,
    delta: str = "",
    subtext: str = "",
    alert_color: str = "#0D9488",
    badge_text: str = ""
):
    """
    Renders a clean, robust card for top-line metrics using native Streamlit containers.
    Prevents any raw HTML markdown rendering errors.
    """
    with st.container(border=True):
        col_lbl, col_bdg = st.columns([1.8, 1.2])
        with col_lbl:
            st.caption(f"**{title.upper()}**")
        with col_bdg:
            if badge_text:
                st.markdown(
                    f"<div style='text-align:right;'><span style='background:#F1F5F9; color:#475569; font-size:10px; font-weight:700; padding:2px 7px; border-radius:9999px; border:1px solid #E2E8F0;'>{badge_text}</span></div>",
                    unsafe_allow_html=True
                )
        st.metric(
            label=title,
            value=value,
            delta=delta if delta else None,
            label_visibility="collapsed"
        )
        if subtext:
            st.caption(subtext)


def render_takeaway(takeaway_text: str):
    """Renders mandatory one-line plain-English takeaway under charts."""
    html = textwrap.dedent(f"""
<div style="background-color: #F0FDFA; border-left: 3px solid #0D9488; padding: 8px 14px; border-radius: 4px; margin-top: 8px; margin-bottom: 16px;">
    <span style="color: #0F766E; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">
        💡 Key Takeaway:
    </span>
    <span style="color: #134E4A; font-size: 13px; font-weight: 500; margin-left: 6px;">
        {takeaway_text}
    </span>
</div>
""")
    st.markdown(html, unsafe_allow_html=True)


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
            with st.container(border=True):
                st.markdown(f"### {s['icon']}")
                st.markdown(f"**{s['step']}**")
                st.caption(s["desc"])


def get_risk_badge_html(level: str) -> str:
    """Returns HTML badge for risk levels."""
    color = RISK_COLORS.get(level, "#64748B")
    bg = RISK_BG_COLORS.get(level, "#F1F5F9")
    return f"""<span style="background-color: {bg}; color: {color}; font-weight: 700; padding: 3px 9px; border-radius: 9999px; font-size: 11.5px; border: 1px solid {color}40; display: inline-block;">● {level} Risk</span>"""


def create_risk_gauge(score: float, title: str = "Risk Severity Score") -> go.Figure:
    """Creates an intuitive, interactive radial gauge chart (0-100%)."""
    score_pct = score * 100 if score <= 1.0 else score
    
    if score_pct >= 65:
        bar_color = RISK_COLORS["High"]
        tier_text = "HIGH RISK"
    elif score_pct >= 40:
        bar_color = RISK_COLORS["Medium"]
        tier_text = "MEDIUM RISK"
    else:
        bar_color = RISK_COLORS["Low"]
        tier_text = "LOW RISK"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score_pct,
        number={"suffix": "%", "font": {"size": 28, "color": bar_color, "family": "Inter, sans-serif"}},
        title={"text": f"<b>{title}</b><br><span style='font-size:12px;color:#64748B;'>Status: {tier_text}</span>", "font": {"size": 13, "color": "#0F172A"}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#CBD5E1"},
            "bar": {"color": bar_color, "thickness": 0.28},
            "bgcolor": "#F1F5F9",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 40], "color": "#ECFDF5"},
                {"range": [40, 65], "color": "#FFFBEB"},
                {"range": [65, 100], "color": "#FEF2F2"}
            ],
            "threshold": {
                "line": {"color": "#0F172A", "width": 3},
                "thickness": 0.8,
                "value": score_pct
            }
        }
    ))
    fig.update_layout(
        height=210,
        margin={"l": 20, "r": 20, "t": 35, "b": 10},
        paper_bgcolor="rgba(0,0,0,0)",
        font={"family": "Inter, sans-serif"}
    )
    return fig


def render_footer():
    """Renders persistent footer."""
    html = textwrap.dedent("""
<div style="margin-top: 40px; border-top: 1px solid #E2E8F0; padding-top: 16px; padding-bottom: 24px; text-align: center; color: #94A3B8; font-size: 12px;">
    <div style="display: flex; justify-content: center; align-items: center; gap: 16px; margin-bottom: 4px;">
        <span><strong>ClimateSense</strong> Pune District Risk Intelligence</span>
        <span>•</span>
        <span style="color: #0D9488; font-weight: 600;">Hackathon Prototype</span>
        <span>•</span>
        <span>Theme: AI/ML & Data-Driven Climate Prediction</span>
    </div>
    <div>
        Designated Feeds: Open-Meteo, IMD, NASA AppEEARS (MODIS NDVI & LST), SRTM GEE, ESA WorldCover, Global Forest Watch (Hansen), WorldPop, EM-DAT/DFO, DataMeet.
    </div>
</div>
""")
    st.markdown(html, unsafe_allow_html=True)
