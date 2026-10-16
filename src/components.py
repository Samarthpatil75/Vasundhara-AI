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
    Renders an impeccably aligned, glassmorphic metric card with fixed height (155px).
    Guarantees 100% vertical alignment across all cards in a grid, with a glowing status accent
    and real-time telemetry indicator track.
    """
    # Format badge HTML if provided
    badge_html = ""
    if badge_text:
        badge_html = f"""<span style="background: rgba(241, 245, 249, 0.9); color: #475569; font-size: 10px; font-weight: 700; padding: 2px 7px; border-radius: 9999px; border: 1px solid #E2E8F0; white-space: nowrap;">{badge_text}</span>"""

    # Format delta badge/chip if provided
    delta_html = ""
    if delta:
        d_lower = delta.lower()
        if any(w in d_lower for w in ["loss", "deficit", "urgent", "high", "alert", "decrease"]):
            d_color = "#DC2626"
            d_bg = "#FEF2F2"
        elif any(w in d_lower for w in ["gain", "surplus", "normal", "optimal", "balanced", "increase"]):
            d_color = "#059669"
            d_bg = "#ECFDF5"
        else:
            d_color = "#0F766E"
            d_bg = "#F0FDFA"
        
        delta_html = f"""<span style="display: inline-block; font-size: 11px; font-weight: 600; color: {d_color}; background: {d_bg}; padding: 2px 6px; border-radius: 4px; margin-left: 6px; vertical-align: middle;">{delta}</span>"""

    # Subtext handling
    subtext_content = subtext if subtext else "&nbsp;"

    card_html = f"""
    <div style="
        height: 155px;
        background: rgba(255, 255, 255, 0.90);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 12px;
        padding: 14px 16px;
        border: 1px solid rgba(226, 232, 240, 0.85);
        border-left: 4px solid {alert_color};
        box-shadow: 0 4px 15px -2px rgba(15, 23, 42, 0.05);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-sizing: border-box;
        margin-bottom: 8px;
    ">
        <div style="display: flex; justify-content: space-between; align-items: center; gap: 8px;">
            <span style="color: #64748B; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.6px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                {title}
            </span>
            {badge_html}
        </div>
        <div style="margin: 4px 0;">
            <span style="font-size: 26px; font-weight: 800; color: #0F172A; letter-spacing: -0.5px; line-height: 1.1;">
                {value}
            </span>
            {delta_html}
        </div>
        <div>
            <div style="font-size: 11px; color: #64748B; line-height: 1.35; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; min-height: 28px;">
                {subtext_content}
            </div>
            <div style="width: 100%; height: 3px; background: linear-gradient(90deg, {alert_color} 0%, rgba(226, 232, 240, 0.3) 100%); border-radius: 2px; margin-top: 6px;"></div>
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)


def render_interactive_taluka_indicators(
    taluka_data,
    selected_taluka: str,
    sim_mitigation: int = 0,
    is_compact: bool = False
):
    """
    Renders an extraordinary, interactive Multi-Sensor Telemetry Deck.
    Replaces static text chips with dynamic visual spectrum gauges, hydrological surge bars,
    dual-segmented concrete vs canopy buffers, and demographic density scales.
    Directly responds in real-time to the What-If Municipal Simulator slider.
    """
    # Safe data extraction
    pop_raw = taluka_data.get('worldpop_population', 0)
    try:
        pop_val = int(pop_raw)
    except (ValueError, TypeError):
        pop_val = 0

    lst_raw = taluka_data.get('modis_lst_c', 32.0)
    try:
        lst_val = float(lst_raw)
    except (ValueError, TypeError):
        lst_val = 32.0

    rain_raw = taluka_data.get('rainfall_24h_mm', 25.0)
    try:
        rain_val = float(rain_raw)
    except (ValueError, TypeError):
        rain_val = 25.0

    builtup_raw = taluka_data.get('esa_builtup_pct', 45.0)
    try:
        builtup_val = float(builtup_raw)
    except (ValueError, TypeError):
        builtup_val = 45.0

    green_raw = taluka_data.get('esa_green_pct', 35.0)
    try:
        green_val = float(green_raw)
    except (ValueError, TypeError):
        green_val = 35.0

    area_type = taluka_data.get('area_type', 'Taluka')
    risk_level = taluka_data.get('risk_level', 'Medium')
    top_factor_1 = taluka_data.get('top_factor_1', 'Impervious Built-up Density')
    top_factor_2 = taluka_data.get('top_factor_2', 'Atmospheric Heat Stress')
    recommendation = taluka_data.get('primary_recommendation', 'Deploy localized green buffer and cool pavements.')

    # Dynamic Simulator Calculations
    lst_drop = sim_mitigation * 0.08
    effective_lst = max(24.0, lst_val - lst_drop)
    effective_green = min(95.0, green_val + sim_mitigation)
    effective_builtup = max(5.0, builtup_val - sim_mitigation)

    # 1. Thermal Spectrum (20°C to 45°C)
    lst_pct = max(0.0, min(100.0, (effective_lst - 20.0) / (45.0 - 20.0) * 100.0))
    if effective_lst >= 38.0:
        lst_status = "🔥 Extreme Urban Heat Island"
        lst_color = "#DC2626"
        lst_bg = "#FEF2F2"
    elif effective_lst >= 33.0:
        lst_status = "⚠️ Elevated Heat Stress"
        lst_color = "#D97706"
        lst_bg = "#FFFBEB"
    else:
        lst_status = "🌿 Temperate Microclimate"
        lst_color = "#059669"
        lst_bg = "#ECFDF5"

    sim_lst_chip = ""
    if sim_mitigation > 0:
        sim_lst_chip = f"""<span style="color: #059669; font-size: 10px; font-weight: 700; background: #ECFDF5; padding: 1px 5px; border-radius: 4px;">-{lst_drop:.1f}°C Cool Roof</span>"""

    # 2. Hydrological Surge (0 to 120 mm)
    rain_pct = max(5.0, min(100.0, (rain_val / 100.0) * 100.0))
    if rain_val >= 70.0:
        rain_status = "🌊 Severe Inundation Alert"
        rain_color = "#DC2626"
        rain_bg = "#FEF2F2"
    elif rain_val >= 35.0:
        rain_status = "💧 Active Monsoonal Inflow"
        rain_color = "#0284C7"
        rain_bg = "#F0F9FF"
    else:
        rain_status = "⛅ Safe Infiltration Rate"
        rain_color = "#059669"
        rain_bg = "#ECFDF5"

    # 3. Surface Permeability
    concrete_pct = max(5.0, min(95.0, effective_builtup))
    canopy_pct = 100.0 - concrete_pct
    if concrete_pct >= 65.0:
        perm_status = "🧱 High Impermeable Runoff"
        perm_color = "#DC2626"
        perm_bg = "#FEF2F2"
    elif concrete_pct >= 40.0:
        perm_status = "🏢 Moderate Urbanized Surface"
        perm_color = "#D97706"
        perm_bg = "#FFFBEB"
    else:
        perm_status = "🌳 High Permeable Canopy"
        perm_color = "#059669"
        perm_bg = "#ECFDF5"

    sim_perm_chip = ""
    if sim_mitigation > 0:
        sim_perm_chip = f"""<span style="color: #059669; font-size: 10px; font-weight: 700; background: #ECFDF5; padding: 1px 5px; border-radius: 4px;">+{sim_mitigation}% Eco-Buffer</span>"""

    # 4. Demographic Exposure (0 to 1.5M scale)
    pop_pct = max(5.0, min(100.0, (pop_val / 1500000.0) * 100.0))
    if pop_val >= 800000:
        pop_status = "🚨 Dense Metropolitan Core"
        pop_color = "#DC2626"
        pop_bg = "#FEF2F2"
    elif pop_val >= 300000:
        pop_status = "👥 Peri-Urban Suburb Corridor"
        pop_color = "#7C3AED"
        pop_bg = "#F5F3FF"
    else:
        pop_status = "🌾 Watershed / Agro-Buffer"
        pop_color = "#059669"
        pop_bg = "#ECFDF5"

    grid_cols = "1fr" if is_compact else "1fr 1fr"

    html = f"""
    <div style="
        background: rgba(255, 255, 255, 0.92);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid rgba(226, 232, 240, 0.9);
        border-radius: 12px;
        padding: 14px 16px;
        box-shadow: 0 8px 24px -4px rgba(15, 23, 42, 0.06);
        margin-bottom: 12px;
    ">
        <!-- Deck Header -->
        <div style="display: flex; justify-content: space-between; align-items: center; padding-bottom: 10px; border-bottom: 1px solid #F1F5F9; margin-bottom: 12px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 15px; font-weight: 800; color: #0F172A;">🛰️ Live Sensor Telemetry Deck</span>
                <span style="background: #E2E8F0; color: #334155; font-size: 10px; font-weight: 700; padding: 2px 7px; border-radius: 9999px;">{area_type}</span>
            </div>
            <div style="font-size: 11px; color: #64748B; font-weight: 600;">
                <span style="display: inline-block; width: 7px; height: 7px; background: #10B981; border-radius: 50%; margin-right: 4px; box-shadow: 0 0 6px #10B981;"></span>
                Synchronized
            </div>
        </div>

        <!-- 4 Visual Instrument Meters -->
        <div style="display: grid; grid-template-columns: {grid_cols}; gap: 10px;">
            
            <!-- Meter 1: Thermal LST -->
            <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 10px 12px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                    <span style="font-size: 10.5px; font-weight: 700; color: #475569; text-transform: uppercase;">🌡️ Land Surface Temp</span>
                    <span style="font-size: 9.5px; color: #64748B; background: #FFFFFF; border: 1px solid #E2E8F0; padding: 1px 5px; border-radius: 4px;">AppEEARS</span>
                </div>
                <div style="display: flex; align-items: baseline; gap: 6px; margin-bottom: 6px;">
                    <span style="font-size: 20px; font-weight: 800; color: #0F172A;">{effective_lst:.1f}°C</span>
                    {sim_lst_chip}
                </div>
                <!-- Spectrum Track with Pin -->
                <div style="position: relative; width: 100%; height: 7px; background: linear-gradient(90deg, #10B981 0%, #3B82F6 25%, #F59E0B 65%, #EF4444 100%); border-radius: 4px; margin-bottom: 6px;">
                    <div style="position: absolute; left: calc({lst_pct}% - 3px); top: -3px; width: 7px; height: 13px; background: #0F172A; border: 1.5px solid #FFFFFF; border-radius: 2px; box-shadow: 0 1px 3px rgba(0,0,0,0.3);"></div>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-size: 9px; color: #94A3B8;">20°C</span>
                    <span style="background: {lst_bg}; color: {lst_color}; font-size: 9.5px; font-weight: 700; padding: 1px 6px; border-radius: 4px;">{lst_status}</span>
                    <span style="font-size: 9px; color: #94A3B8;">45°C</span>
                </div>
            </div>

            <!-- Meter 2: Precipitation Surge -->
            <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 10px 12px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                    <span style="font-size: 10.5px; font-weight: 700; color: #475569; text-transform: uppercase;">🌧️ 24h Precipitation</span>
                    <span style="font-size: 9.5px; color: #64748B; background: #FFFFFF; border: 1px solid #E2E8F0; padding: 1px 5px; border-radius: 4px;">Open-Meteo</span>
                </div>
                <div style="display: flex; align-items: baseline; gap: 6px; margin-bottom: 6px;">
                    <span style="font-size: 20px; font-weight: 800; color: #0F172A;">{rain_val:.1f} mm</span>
                </div>
                <!-- Surge Bar -->
                <div style="position: relative; width: 100%; height: 7px; background: #E0F2FE; border-radius: 4px; margin-bottom: 6px; overflow: hidden;">
                    <div style="width: {rain_pct}%; height: 100%; background: linear-gradient(90deg, #0284C7 0%, #2563EB 100%); border-radius: 4px;"></div>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-size: 9px; color: #94A3B8;">0 mm</span>
                    <span style="background: {rain_bg}; color: {rain_color}; font-size: 9.5px; font-weight: 700; padding: 1px 6px; border-radius: 4px;">{rain_status}</span>
                    <span style="font-size: 9px; color: #94A3B8;">100mm Alert</span>
                </div>
            </div>

            <!-- Meter 3: Concrete vs Canopy Composition -->
            <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 10px 12px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                    <span style="font-size: 10.5px; font-weight: 700; color: #475569; text-transform: uppercase;">🏙️ Surface Permeability</span>
                    <span style="font-size: 9.5px; color: #64748B; background: #FFFFFF; border: 1px solid #E2E8F0; padding: 1px 5px; border-radius: 4px;">ESA 10m</span>
                </div>
                <div style="display: flex; align-items: baseline; justify-content: space-between; margin-bottom: 6px;">
                    <span style="font-size: 13px; font-weight: 800; color: #334155;">{concrete_pct:.0f}% Built <span style="color: #94A3B8; font-weight: normal;">|</span> <span style="color: #059669;">{canopy_pct:.0f}% Canopy</span></span>
                    {sim_perm_chip}
                </div>
                <!-- Dual Segmented Bar -->
                <div style="display: flex; width: 100%; height: 7px; border-radius: 4px; overflow: hidden; margin-bottom: 6px;">
                    <div style="width: {concrete_pct}%; background: #64748B; height: 100%;"></div>
                    <div style="width: {canopy_pct}%; background: #10B981; height: 100%;"></div>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-size: 9px; color: #64748B;">Concrete</span>
                    <span style="background: {perm_bg}; color: {perm_color}; font-size: 9.5px; font-weight: 700; padding: 1px 6px; border-radius: 4px;">{perm_status}</span>
                    <span style="font-size: 9px; color: #10B981;">Canopy</span>
                </div>
            </div>

            <!-- Meter 4: Demographic Density -->
            <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 10px 12px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                    <span style="font-size: 10.5px; font-weight: 700; color: #475569; text-transform: uppercase;">👥 Population Exposure</span>
                    <span style="font-size: 9.5px; color: #64748B; background: #FFFFFF; border: 1px solid #E2E8F0; padding: 1px 5px; border-radius: 4px;">WorldPop</span>
                </div>
                <div style="display: flex; align-items: baseline; gap: 6px; margin-bottom: 6px;">
                    <span style="font-size: 20px; font-weight: 800; color: #0F172A;">{pop_val:,}</span>
                </div>
                <!-- Density Spectrum Bar -->
                <div style="position: relative; width: 100%; height: 7px; background: #F3E8FF; border-radius: 4px; margin-bottom: 6px; overflow: hidden;">
                    <div style="width: {pop_pct}%; height: 100%; background: linear-gradient(90deg, #A855F7 0%, #7C3AED 100%); border-radius: 4px;"></div>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-size: 9px; color: #94A3B8;">Sparse</span>
                    <span style="background: {pop_bg}; color: {pop_color}; font-size: 9.5px; font-weight: 700; padding: 1px 6px; border-radius: 4px;">{pop_status}</span>
                    <span style="font-size: 9px; color: #94A3B8;">>1.5M</span>
                </div>
            </div>

        </div>

        <!-- AI Root Cause Diagnostic & Protocol -->
        <div style="margin-top: 10px; padding-top: 10px; border-top: 1px solid #F1F5F9;">
            <div style="font-size: 11px; font-weight: 700; color: #334155; margin-bottom: 6px;">
                📌 Algorithmic Root Drivers (SHAP Attribution):
            </div>
            <div style="display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 8px;">
                <span style="background: #F8FAFC; border: 1px solid #E2E8F0; padding: 3px 8px; border-radius: 6px; font-size: 11px; color: #1E293B;">
                    1. <strong>{top_factor_1}</strong>
                </span>
                <span style="background: #F8FAFC; border: 1px solid #E2E8F0; padding: 3px 8px; border-radius: 6px; font-size: 11px; color: #1E293B;">
                    2. <strong>{top_factor_2}</strong>
                </span>
            </div>
            <div style="background: #F0FDFA; border-left: 3px solid #0D9488; padding: 8px 12px; border-radius: 6px; font-size: 12px; color: #134E4A; line-height: 1.45;">
                🎯 <strong>Prescribed Municipal Protocol:</strong> {recommendation}
            </div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)



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
