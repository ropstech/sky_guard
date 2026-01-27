"""
Sky-Guard Dashboard: Settings Page
===================================
Data pipeline management and system information.

Usage:
    from pages.settings import render_settings
    
    render_settings()
"""

import streamlit as st
import json
from pathlib import Path


def render_settings():
    """
    Render Settings page.
    
    Displays:
    - Last data generation timestamp
    - Regenerate data buttons
    - About information
    """
    
    st.title("Settings")
    
    # ========================================================================
    # DATA PIPELINE
    # ========================================================================
    st.subheader("Data Pipeline")
    
    st.write("**Last Data Generation:**")
    
    try:
        summary_path = Path('data/raw/generation_summary.json')
        
        if summary_path.exists():
            with open(summary_path, 'r') as f:
                summary = json.load(f)
            st.code(summary['generation_timestamp'])
        else:
            st.warning("No data generated yet")
            
    except Exception as e:
        st.error(f"Error loading summary: {e}")
    
    st.markdown("---")
    
    # ========================================================================
    # REGENERATE DATA
    # ========================================================================
    st.subheader("Regenerate Data")
    
    if st.button("🔄 Generate New Dataset"):
        st.info("Run: `uv run python src/data_generation/generate_data.py`")
    
    if st.button("🔍 Validate Data"):
        st.info("Run: `uv run python src/data_generation/validate_data.py`")
    
    if st.button("📊 Run Analysis"):
        st.info("Run: `uv run python src/analytics/detect_anomalies.py`")
    
    st.markdown("---")
    
    # ========================================================================
    # ABOUT
    # ========================================================================
    st.subheader("About")
    
    st.write("**Sky-Guard v1.0**")
    st.write("AI-Driven Operational Resilience for Aviation MRO")
    st.caption("© 2026 RS Technologies, Inc.")