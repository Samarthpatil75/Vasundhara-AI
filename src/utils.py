"""
utils.py - Shared data loaders, analytical helpers, and styling utilities for ClimateSense.
Strictly integrated with the 10 designated climate, satellite, and demographic datasets.
Optimized for high-speed interactivity, human-readable numbers, and clear UI presentation.
"""

import os
import json
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

# Directory Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

# Color Palette Constants (Colorblind safe, climate theme)
COLOR_THEME = {
    "teal_dark": "#0F766E",
    "teal_primary": "#0D9488",
    "teal_light": "#14B8A6",
    "teal_subtle": "#CCFBF1",
    "emerald": "#10B981",
    "slate_dark": "#0F172A",
    "slate_text": "#334155",
    "slate_muted": "#64748B",
    "slate_border": "#E2E8F0",
    "card_bg": "#FFFFFF",
    "canvas_bg": "#F8FAFC",
}

RISK_COLORS = {
    "Low": "#10B981",     # Emerald Green
    "Medium": "#F59E0B",  # Amber / Warm Ochre
    "High": "#EF4444"     # Coral Red
}

RISK_BG_COLORS = {
    "Low": "#ECFDF5",
    "Medium": "#FFFBEB",
    "High": "#FEF2F2"
}

# The 10 Designated Datasets Master Registry
DESIGNATED_DATASETS = [
    {
        "task": "Temperature, humidity, wind",
        "best_pick": "Open-Meteo Historical API",
        "why": "No account or key, one URL or a few lines of Python, ERA5-quality data, daily history from 1940",
        "backup": "NASA POWER (CSV download)",
        "badge": "Active API"
    },
    {
        "task": "Rainfall",
        "best_pick": "Open-Meteo / IMD Gridded Rainfall",
        "why": "IMD is India's official data and judges will trust it; Open-Meteo provides convenient historical ERA5 precipitation",
        "backup": "CHIRPS or NASA POWER",
        "badge": "Active (India Climatology)"
    },
    {
        "task": "Vegetation (NDVI) for carbon monitoring",
        "best_pick": "NASA AppEEARS (MODIS NDVI)",
        "why": "Draw Pune on a map and download a CSV with no coding, and it has continuous data since 2000",
        "backup": "Sentinel-2 via Google Earth Engine",
        "badge": "Active (250m 16-day)"
    },
    {
        "task": "Land surface temperature (heat risk)",
        "best_pick": "MODIS LST via AppEEARS",
        "why": "Same tool as NDVI, so you learn only one workflow and get standardized thermal data",
        "backup": "Landsat 8/9 via Earth Engine",
        "badge": "Active (1km Day/Night LST)"
    },
    {
        "task": "Elevation and slope (flood risk)",
        "best_pick": "SRTM via Google Earth Engine",
        "why": "One small script gives you elevation, slope angle, and topographic wetness index per taluka",
        "backup": "Copernicus DEM or OpenTopography",
        "badge": "Active (30m DEM)"
    },
    {
        "task": "Land cover (built-up vs green)",
        "best_pick": "ESA WorldCover",
        "why": "Clean, recent, and simple categories (built-up, tree cover, grassland, cropland, water)",
        "backup": "Dynamic World",
        "badge": "Active (10m Resolution)"
    },
    {
        "task": "Tree loss / carbon estimate",
        "best_pick": "Global Forest Watch (Hansen)",
        "why": "Year-by-year tree cover loss that can be converted directly to a biomass carbon proxy",
        "backup": "ESA CCI Biomass",
        "badge": "Active (Annual Canopy Deficit)"
    },
    {
        "task": "Population exposure",
        "best_pick": "WorldPop",
        "why": "Gridded population estimates easy to aggregate and join to local Pune talukas",
        "backup": "GHSL",
        "badge": "Active (100m Demographics)"
    },
    {
        "task": "Disaster events for validation",
        "best_pick": "EM-DAT & Dartmouth Flood Observatory (DFO)",
        "why": "EM-DAT covers disaster declarations broadly, and Dartmouth gives precise flood dates and extents",
        "backup": "Maharashtra SDMA reports",
        "badge": "Active (Benchmark Ground-Truth)"
    },
    {
        "task": "Map boundaries",
        "best_pick": "DataMeet (Indian sub-district shapefiles)",
        "why": "Built specifically for India and matches official administrative taluka names and codes",
        "backup": "GADM",
        "badge": "Active (16 Pune Talukas)"
    }
]


# ---------------------------------------------------------
# DATA LOADERS (Cached with Streamlit)
# ---------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_risk_data() -> pd.DataFrame:
    """Load risk predictions data from data/risk_predictions.csv."""
    path = os.path.join(DATA_DIR, "risk_predictions.csv")
    if not os.path.exists(path):
        return pd.DataFrame()
    
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])
    df["risk_score"] = pd.to_numeric(df["risk_score"], errors="coerce").fillna(0.0)
    df["risk_lower_ci"] = pd.to_numeric(df["risk_lower_ci"], errors="coerce").fillna(0.0)
    df["risk_upper_ci"] = pd.to_numeric(df["risk_upper_ci"], errors="coerce").fillna(0.0)
    if "worldpop_population" in df.columns:
        df["worldpop_population"] = pd.to_numeric(df["worldpop_population"], errors="coerce").fillna(0)
    return df


@st.cache_data(show_spinner=False)
def load_ndvi_data() -> pd.DataFrame:
    """Load NDVI and green cover time-series from data/ndvi_timeseries.csv."""
    path = os.path.join(DATA_DIR, "ndvi_timeseries.csv")
    if not os.path.exists(path):
        return pd.DataFrame()
    
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])
    df["ndvi_mean"] = pd.to_numeric(df["ndvi_mean"], errors="coerce").fillna(0.0)
    df["green_cover_pct"] = pd.to_numeric(df["green_cover_pct"], errors="coerce").fillna(0.0)
    df["vegetation_area_sqkm"] = pd.to_numeric(df["vegetation_area_sqkm"], errors="coerce").fillna(0.0)
    df["carbon_stock_tco2e"] = pd.to_numeric(df["carbon_stock_tco2e"], errors="coerce").fillna(0.0)
    return df


@st.cache_data(show_spinner=False)
def load_feature_importance() -> pd.DataFrame:
    """Load feature importance data from data/feature_importance.csv."""
    path = os.path.join(DATA_DIR, "feature_importance.csv")
    if not os.path.exists(path):
        return pd.DataFrame()
    
    df = pd.read_csv(path)
    df["importance_score"] = pd.to_numeric(df["importance_score"], errors="coerce").fillna(0.0)
    return df


@st.cache_data(show_spinner=False)
def load_model_metrics() -> dict:
    """Load model evaluation metrics from data/model_metrics.json."""
    path = os.path.join(DATA_DIR, "model_metrics.json")
    if not os.path.exists(path):
        return {}
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


# ---------------------------------------------------------
# COMPUTATION HELPERS
# ---------------------------------------------------------
def compute_overview_kpis(
    df_risk: pd.DataFrame,
    df_ndvi: pd.DataFrame,
    selected_hazard: str = None,
    selected_date: pd.Timestamp = None
) -> dict:
    """
    Computes real-time dynamic KPIs for the dashboard home/overview.
    Returns clean, human-readable numbers with proper units (e.g. Mt CO2e, Millions of citizens).
    """
    if df_risk.empty or df_ndvi.empty:
        return {
            "high_risk_count": 0,
            "total_areas": 16,
            "high_risk_pct": 0.0,
            "avg_risk_score": 0.0,
            "green_cover_change_pct": 0.0,
            "carbon_change_tco2e": 0.0,
            "carbon_change_mt": 0.0,
            "high_risk_population": 0,
            "total_district_population": 9400000,
            "latest_date_str": "N/A"
        }

    hist_risk = df_risk[df_risk["is_forecast"] == 0]
    if hist_risk.empty:
        hist_risk = df_risk
    
    # If no specific date requested, select pre-monsoon heat peak (May 2025) or latest active slice
    if selected_date is None:
        selected_date = hist_risk["date"].max()
    
    latest_slice = hist_risk[hist_risk["date"] == selected_date]

    if selected_hazard and selected_hazard in latest_slice["hazard_type"].values:
        latest_slice = latest_slice[latest_slice["hazard_type"] == selected_hazard]

    total_areas = latest_slice["area_name"].nunique() if not latest_slice.empty else 16
    high_risk_df = latest_slice[latest_slice["risk_level"] == "High"]
    high_risk_count = high_risk_df["area_name"].nunique() if not latest_slice.empty else 0
    high_risk_pct = (high_risk_count / total_areas * 100.0) if total_areas > 0 else 0.0
    avg_risk_score = latest_slice["risk_score"].mean() * 100.0 if not latest_slice.empty else 0.0

    # WorldPop exposure calculation
    pop_col = "worldpop_population" if "worldpop_population" in latest_slice.columns else None
    if pop_col:
        high_risk_pop = high_risk_df.drop_duplicates(subset=["area_name"])[pop_col].sum()
        total_pop = latest_slice.drop_duplicates(subset=["area_name"])[pop_col].sum()
    else:
        high_risk_pop = 0
        total_pop = 9420000

    # 5-Year Green Cover & Carbon Change (2021 vs 2025 annual baseline):
    y_start = df_ndvi["year"].min()
    y_end = df_ndvi["year"].max()

    start_totals = df_ndvi[df_ndvi["year"] == y_start].groupby("area_name").agg({
        "vegetation_area_sqkm": "mean",
        "carbon_stock_tco2e": "mean"
    }).sum()

    end_totals = df_ndvi[df_ndvi["year"] == y_end].groupby("area_name").agg({
        "vegetation_area_sqkm": "mean",
        "carbon_stock_tco2e": "mean"
    }).sum()

    start_veg = start_totals["vegetation_area_sqkm"]
    end_veg = end_totals["vegetation_area_sqkm"]
    veg_change_pct = ((end_veg - start_veg) / start_veg * 100.0) if start_veg > 0 else 0.0

    start_carbon = start_totals["carbon_stock_tco2e"]
    end_carbon = end_totals["carbon_stock_tco2e"]
    carbon_diff_tco2e = end_carbon - start_carbon
    carbon_change_pct = ((end_carbon - start_carbon) / start_carbon * 100.0) if start_carbon > 0 else 0.0
    carbon_change_mt = carbon_diff_tco2e / 1_000_000.0

    return {
        "high_risk_count": int(high_risk_count),
        "total_areas": int(total_areas),
        "high_risk_pct": round(high_risk_pct, 1),
        "avg_risk_score": round(avg_risk_score, 1),
        "green_cover_change_pct": round(veg_change_pct, 2),
        "carbon_change_tco2e": round(carbon_diff_tco2e, 0),
        "carbon_change_mt": round(carbon_change_mt, 2),
        "carbon_change_pct": round(carbon_change_pct, 2),
        "high_risk_population": int(high_risk_pop),
        "total_district_population": int(total_pop),
        "latest_date_str": selected_date.strftime("%B %Y")
    }


def compute_area_vegetation_loss(df_ndvi: pd.DataFrame) -> pd.DataFrame:
    """Computes area-level vegetation change over the 5-year timeline."""
    if df_ndvi.empty:
        return pd.DataFrame()
    
    y_start = df_ndvi["year"].min()
    y_end = df_ndvi["year"].max()

    first_df = df_ndvi[df_ndvi["year"] == y_start].groupby(["area_name", "area_type"]).agg({
        "vegetation_area_sqkm": "mean",
        "carbon_stock_tco2e": "mean",
        "ndvi_mean": "mean",
        "green_cover_pct": "mean",
        "gfw_tree_cover_loss_ha_annual": "first" if "gfw_tree_cover_loss_ha_annual" in df_ndvi.columns else "count"
    }).reset_index().rename(
        columns={
            "vegetation_area_sqkm": "start_veg_sqkm",
            "carbon_stock_tco2e": "start_carbon",
            "ndvi_mean": "start_ndvi",
            "green_cover_pct": "start_green_pct"
        }
    )

    last_df = df_ndvi[df_ndvi["year"] == y_end].groupby(["area_name"]).agg({
        "vegetation_area_sqkm": "mean",
        "carbon_stock_tco2e": "mean",
        "ndvi_mean": "mean",
        "green_cover_pct": "mean"
    }).reset_index().rename(
        columns={
            "vegetation_area_sqkm": "end_veg_sqkm",
            "carbon_stock_tco2e": "end_carbon",
            "ndvi_mean": "end_ndvi",
            "green_cover_pct": "end_green_pct"
        }
    )

    merged = pd.merge(first_df, last_df, on="area_name")
    merged["veg_change_sqkm"] = (merged["end_veg_sqkm"] - merged["start_veg_sqkm"]).round(2)
    merged["veg_change_pct"] = ((merged["end_veg_sqkm"] - merged["start_veg_sqkm"]) / merged["start_veg_sqkm"] * 100.0).round(2)
    merged["carbon_change_tco2e"] = (merged["end_carbon"] - merged["start_carbon"]).round(1)
    merged["carbon_change_pct"] = ((merged["end_carbon"] - merged["start_carbon"]) / merged["start_carbon"] * 100.0).round(2)
    merged["ndvi_change"] = (merged["end_ndvi"] - merged["start_ndvi"]).round(3)

    return merged.sort_values(by="veg_change_pct", ascending=True)


# ---------------------------------------------------------
# INTERACTIVE GAUGE HELPER
# ---------------------------------------------------------
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
        title={"text": f"<b>{title}</b><br><span style='font-size:12px;color:#64748B;'>Status: {tier_text}</span>", "font": {"size": 14, "color": "#0F172A"}},
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
        height=220,
        margin={"l": 25, "r": 25, "t": 35, "b": 10},
        paper_bgcolor="rgba(0,0,0,0)",
        font={"family": "Inter, sans-serif"}
    )
    return fig


# ---------------------------------------------------------
# PLOTLY STYLING HELPERS
# ---------------------------------------------------------
def apply_clean_layout(
    fig: go.Figure,
    title: str = "",
    x_title: str = "",
    y_title: str = "",
    height: int = 400,
    show_legend: bool = True
) -> go.Figure:
    """Applies clean, high-contrast, presentation-ready layout styling to any Plotly figure."""
    fig.update_layout(
        title={
            "text": f"<b>{title}</b>" if title else "",
            "font": {"size": 15, "color": COLOR_THEME["slate_dark"], "family": "Inter, sans-serif"},
            "x": 0.01,
            "y": 0.96
        },
        height=height,
        margin={"l": 40, "r": 20, "t": 48 if title else 20, "b": 40},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#FFFFFF",
        hoverlabel={
            "bgcolor": "#0F172A",
            "font_size": 12,
            "font_color": "#F8FAFC",
            "font_family": "Inter, sans-serif"
        },
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "right",
            "x": 1.0,
            "font": {"size": 11, "color": COLOR_THEME["slate_text"]},
            "bgcolor": "rgba(255,255,255,0.85)"
        } if show_legend else {},
        xaxis={
            "title": {"text": x_title, "font": {"size": 11, "color": COLOR_THEME["slate_muted"]}},
            "tickfont": {"size": 10, "color": COLOR_THEME["slate_text"]},
            "showgrid": True,
            "gridcolor": "#F1F5F9",
            "zeroline": False,
            "linecolor": "#E2E8F0"
        },
        yaxis={
            "title": {"text": y_title, "font": {"size": 11, "color": COLOR_THEME["slate_muted"]}},
            "tickfont": {"size": 10, "color": COLOR_THEME["slate_text"]},
            "showgrid": True,
            "gridcolor": "#F1F5F9",
            "zeroline": False,
            "linecolor": "#E2E8F0"
        }
    )
    return fig


def apply_map_layout(fig: go.Figure, height: int = 480) -> go.Figure:
    """Applies clean layout specifically to map figures (without cartesian axes)."""
    fig.update_layout(
        height=height,
        margin={"l": 0, "r": 0, "t": 30, "b": 0},
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(255,255,255,0.85)",
            font={"size": 11, "color": COLOR_THEME["slate_text"]}
        )
    )
    return fig

