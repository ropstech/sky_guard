"""
Sky-Guard Dashboard: AI Recommendations Page
=============================================
AI-generated mitigation strategies for high-risk components.

Usage:
    from pages.ai_recommendations import render_ai_recommendations
    
    render_ai_recommendations(recommendations_data)
"""

import streamlit as st
import pandas as pd


def render_ai_recommendations(recommendations_data: dict):
    """
    Render AI Recommendations page.
    
    Displays:
    - Model metadata
    - Summary metrics
    - Expandable recommendations with:
      - Root cause analysis
      - Mitigation options
      - Recommended actions
      - Expected ROI
    
    Args:
        recommendations_data: AI recommendations with metadata
    """
    
    st.title("AI-Powered Recommendations")
    
    metadata = recommendations_data['metadata']
    recommendations = recommendations_data['recommendations']
    
    # ========================================================================
    # METADATA
    # ========================================================================
    st.caption(
        f"🤖 Model: {metadata['model_used']} • "
        f"{metadata['total_recommendations']} recommendations generated"
    )
    
    # ========================================================================
    # SUMMARY METRICS
    # ========================================================================
    total_exposure = sum(
        r['component']['financial_exposure_usd'] 
        for r in recommendations
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "Components Analyzed",
            len(recommendations),
            delta="Top Priority"
        )
    
    with col2:
        st.metric(
            "Total Exposure",
            f"${total_exposure/1e6:.1f}M",
            delta="AOG Risk"
        )
    
    st.markdown("---")
    
    # ========================================================================
    # RECOMMENDATIONS
    # ========================================================================
    for idx, rec in enumerate(recommendations, 1):
        component = rec['component']
        ai = rec['ai_analysis']
        
        with st.expander(
            f"**{idx}. {component['part_number']}** — {component['category']} • "
            f"${component['financial_exposure_usd']/1e6:.1f}M • "
            f"Confidence: {ai['confidence_level']}",
            expanded=(idx <= 2)  # First 2 expanded by default
        ):
            # ----------------------------------------------------------------
            # Root Cause
            # ----------------------------------------------------------------
            st.markdown("#### Root Cause")
            st.write(ai['root_cause'])
            
            # ----------------------------------------------------------------
            # Mitigation Options
            # ----------------------------------------------------------------
            st.markdown("#### Mitigation Options")
            
            options_df = pd.DataFrame(ai['mitigation_options'])
            options_df['Cost'] = options_df['estimated_cost_usd'].apply(
                lambda x: f"${x:,.0f}"
            )
            
            display = options_df[[
                'option', 'description', 'Cost',
                'implementation_time_days', 'risk_reduction_pct'
            ]].copy()
            
            display.columns = [
                'Option', 'Description', 'Cost', 
                'Timeline (days)', 'Risk Reduction (%)'
            ]
            
            st.dataframe(display, width='stretch', hide_index=True)
            
            # ----------------------------------------------------------------
            # Recommended Action
            # ----------------------------------------------------------------
            st.markdown("#### Recommended Action")
            st.success(ai['recommended_action'])
            
            # ----------------------------------------------------------------
            # Expected ROI
            # ----------------------------------------------------------------
            st.markdown("#### Expected ROI")
            st.info(ai['expected_roi'])