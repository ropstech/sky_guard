"""
Sky-Guard Dashboard: Sidebar Component
=======================================
Navigation and quick stats sidebar.

Usage:
    from components.sidebar import render_sidebar
    
    page = render_sidebar(risk_data, roi_data)
"""

import streamlit as st
from streamlit_option_menu import option_menu


def render_sidebar(risk_data: dict, roi_data: dict) -> str:
    """
    Render sidebar with navigation and key metrics.
    
    Args:
        risk_data: Risk analysis data
        roi_data: ROI analysis data
        
    Returns:
        str: Selected page name
    """
    
    with st.sidebar:
        # ====================================================================
        # BRANDING
        # ====================================================================
        st.markdown(
            """
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
            
            <div style="text-align: left; margin-bottom: 20px;">
                <i class="fa-solid fa-plane-lock" style="font-size: 2.5rem; color: #DA7758; margin-bottom: 10px; font-family: 'Font Awesome 6 Free'; font-weight: 900;"></i>
                <h1 style="margin-bottom: 0;">Sky-Guard</h1>
                <p style="font-size: 0.8em; color: gray;">AI-Driven MRO Intelligence</p>
            </div>
            """, 
            unsafe_allow_html=True
        )

        st.markdown("---")
        
        # ====================================================================
        # NAVIGATION
        # ====================================================================
        st.markdown("### Navigation")

        page = option_menu(
            menu_title=None,
            options=[
                "Financial Performance", 
                "Risk Analysis", 
                "AI Recommendations", 
                "Settings"
            ],
            icons=[
                "graph-up-arrow", 
                "shield-exclamation", 
                "cpu", 
                "sliders"
            ], 
            default_index=0,
            styles={
                "container": {
                    "padding": "0!important", 
                    "background-color": "transparent"
                },
                "icon": {
                    "color": "#DA7758", 
                    "font-size": "16px"
                }, 
                "nav-link": {
                    "font-size": "16px", 
                    "text-align": "left", 
                    "margin": "0px", 
                    "--hover-color": "#141413"
                },
                "nav-link-selected": {
                    "background-color": "#7C4937"
                },
            }
        )
        
        st.markdown("---")
        
        # ====================================================================
        # QUICK STATS
        # ====================================================================
        st.markdown("### Quick Stats")
        
        roi_metrics = roi_data['roi_metrics']
        risk_summary = risk_data['summary']
        
        c1, c2 = st.columns(2)
        
        with c1:
            st.metric(
                "ROI Ratio", 
                f"{roi_metrics['roi_ratio']:.0f}:1"
            )
            st.metric(
                "Net Benefit", 
                f"${roi_metrics['net_benefit_usd']/1e6:.0f}M"
            )
        
        with c2:
            st.metric(
                "High-Risk Items", 
                f"{risk_summary['risk_distribution']['high_risk']:,}"
            )

        st.markdown("---")
        
        # ====================================================================
        # SYSTEM STATUS
        # ====================================================================
        st.markdown("### System Status")
        st.success("Operational", icon=":material/check_circle:")

        st.markdown("---")
        
        # ====================================================================
        # FOOTER
        # ====================================================================
        st.markdown(
            """
            <div style="font-size: 0.75em; color: #888; text-align: center;">
                Sky-Guard v1.0 Enterprise<br>
                © 2026 RS Technologies
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    return page