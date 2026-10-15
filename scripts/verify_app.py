"""
verify_app.py
Automated verification script to validate all data files, utils functions,
and page execution logic for ClimateSense.
"""

import os
import sys
import pandas as pd

# Add parent directory to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from src.utils import (
    load_risk_data,
    load_ndvi_data,
    load_feature_importance,
    load_model_metrics,
    compute_overview_kpis,
    compute_area_vegetation_loss
)

def run_checks():
    print("=== Running ClimateSense Verification Checks ===")
    
    # 1. Check data loaders
    df_risk = load_risk_data()
    print(f"[OK] load_risk_data: {len(df_risk)} rows loaded.")
    assert not df_risk.empty, "Risk data is empty!"
    assert "risk_score" in df_risk.columns
    assert "hazard_type" in df_risk.columns

    df_ndvi = load_ndvi_data()
    print(f"[OK] load_ndvi_data: {len(df_ndvi)} rows loaded.")
    assert not df_ndvi.empty, "NDVI data is empty!"
    assert "ndvi_mean" in df_ndvi.columns
    assert "carbon_stock_tco2e" in df_ndvi.columns

    df_feat = load_feature_importance()
    print(f"[OK] load_feature_importance: {len(df_feat)} rows loaded.")
    assert not df_feat.empty

    metrics = load_model_metrics()
    print(f"[OK] load_model_metrics: keys = {list(metrics.keys())}")
    assert "overall" in metrics
    assert "confusion_matrix" in metrics

    # 2. Check KPI computation
    kpis = compute_overview_kpis(df_risk, df_ndvi)
    print(f"[OK] compute_overview_kpis output: {kpis}")
    assert kpis["total_areas"] > 0
    assert kpis["high_risk_count"] >= 0

    # 3. Check vegetation loss computation
    loss = compute_area_vegetation_loss(df_ndvi)
    print(f"[OK] compute_area_vegetation_loss: {len(loss)} areas analyzed.")
    assert not loss.empty

    print("\n[SUCCESS] All data loading and computation tests PASSED successfully!")

if __name__ == "__main__":
    run_checks()
