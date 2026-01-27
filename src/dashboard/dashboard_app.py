"""
Sky-Guard: Executive Dashboard - REFACTORED
============================================
Clean, modular architecture for maintainability and scalability.

Directory Structure:
    config/
        theme.py            - ColorScheme and theme constants
    utils/
        data_loader.py      - DashboardData class
    components/
        sidebar.py          - Navigation sidebar
    views/
        financial_performance.py
        risk_analysis.py
        ai_recommendations.py
        settings.py

Usage:
    streamlit run src/dashboard/dashboard_app.py
"""

import streamlit as st

# Import modular components
from utils.data_loader import DashboardData
from utils.animations import inject_custom_css
from components.sidebar import render_sidebar
from views.financial_performance import render_financial_performance
from views.risk_analysis import render_risk_analysis
from views.ai_recommendations import render_ai_recommendations
from views.settings import render_settings


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Sky-Guard Dashboard",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom CSS for animations
inject_custom_css()


def main():
    """
    Main application entry point.
    
    Orchestrates:
    1. Data availability check
    2. Data loading
    3. Sidebar navigation
    4. Page routing
    """
    
    # ========================================================================
    # DATA AVAILABILITY CHECK
    # ========================================================================
    data = DashboardData()
    data_exists, missing_files = data.check_data_availability()
    
    if not data_exists:
        st.error(f"❌ Missing: {', '.join(missing_files)}")
        st.info("""
        **Run the pipeline:**
        ```bash
        uv run python src/data_generation/generate_data.py
        uv run python src/analytics/detect_anomalies.py
        uv run python src/ai_reasoning/ai_reasoning_engine.py
        uv run python src/analytics/roi_calculator.py
        ```
        """)
        return
    
    # ========================================================================
    # LOAD DATA
    # ========================================================================
    try:
        risk_data = data.load_risk_analysis()
        recommendations_data = data.load_recommendations()
        roi_data = data.load_roi_analysis()
        inventory_df = data.load_enriched_inventory()
        
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        return
    
    # ========================================================================
    # SIDEBAR NAVIGATION
    # ========================================================================
    selected_page = render_sidebar(risk_data, roi_data)
    
    # ========================================================================
    # PAGE ROUTING
    # ========================================================================
    if selected_page == "Financial Performance":
        render_financial_performance(roi_data, risk_data)
        
    elif selected_page == "Risk Analysis":
        render_risk_analysis(risk_data, inventory_df)
        
    elif selected_page == "AI Recommendations":
        render_ai_recommendations(recommendations_data)
        
    elif selected_page == "Settings":
        render_settings()


if __name__ == "__main__":
    main()