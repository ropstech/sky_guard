"""
Sky-Guard Dashboard: Financial Performance Page
================================================
Executive-level ROI and financial metrics.

Usage:
    from pages.financial_performance import render_financial_performance
    
    render_financial_performance(roi_data, risk_data)
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from config.theme import ColorScheme


def render_financial_performance(roi_data: dict, risk_data: dict):
    """
    Render Financial Performance page.
    
    Displays:
    - Executive summary banner
    - Key financial metrics (ROI, Net Benefit, Payback)
    - Investment structure visualization
    - Risk distribution chart
    - Strategic recommendation
    
    Args:
        roi_data: ROI analysis results
        risk_data: Risk analysis results
    """
    
    st.title("Financial Performance")
    
    roi_metrics = roi_data['roi_metrics']
    executive_summary = roi_data['executive_summary']
    
    # ========================================================================
    # VALUE PROPOSITION BANNER
    # ========================================================================
    st.success(
        f"**{executive_summary['value_proposition']}**", 
        icon=":material/celebration:"
    )
    
    st.markdown("")
    
    # ========================================================================
    # KEY METRICS
    # ========================================================================
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Net Benefit",
            value=f"${roi_metrics['net_benefit_usd']/1e6:.1f}M",
            delta="First Year"
        )
    
    with col2:
        st.metric(
            label="ROI Ratio",
            value=f"{roi_metrics['roi_ratio']:.0f}:1",
            delta=f"+{roi_metrics['roi_percentage']:.0f}%"
        )
    
    with col3:
        payback_months = roi_metrics['payback_period_months']
        if payback_months < 1:
            payback_display = f"{payback_months*30:.0f} days"
        else:
            payback_display = f"{payback_months:.1f} mo"
        
        st.metric(
            label="Payback Period",
            value=payback_display,
            delta="Break-even"
        )
    
    with col4:
        st.metric(
            label="Risk Reduction",
            value=f"{roi_data['aog_cost_avoidance']['risk_reduction_percentage']:.0f}%",
            delta="AOG Prevention"
        )
    
    st.markdown("---")
    
    # ========================================================================
    # CHARTS
    # ========================================================================
    col1, col2 = st.columns(2)
    
    # ------------------------------------------------------------------------
    # Investment Structure Pie Chart
    # ------------------------------------------------------------------------
    with col1:
        st.subheader("Investment Structure")
        investment = roi_data['investment_breakdown']
        
        inv_data = pd.DataFrame({
            'Category': ['System Setup', 'Operations', 'Mitigations'],
            'Amount': [
                investment['one_time_setup'],
                investment['annual_operating_costs'],
                investment['mitigation_action_costs']
            ]
        })
        
        fig = px.pie(
            inv_data,
            values='Amount',
            names='Category',
            hole=0.6,
            color_discrete_sequence=ColorScheme.INVESTMENT_PALETTE
        )
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent',
            hovertemplate="<b>%{label}</b><br>$%{value:,.0f}<br>%{percent}<extra></extra>",
            marker=dict(
                line=dict(color=ColorScheme.BG_PRIMARY, width=2)
            )
        )
        
        fig.update_layout(
            **ColorScheme.get_plotly_layout_defaults(),
            showlegend=True,
            margin=dict(t=10, b=10, l=10, r=10),
            height=350,
            legend=dict(
                font=dict(color='white'),
                bgcolor=ColorScheme.BG_TERTIARY
            )
        )
        
        st.plotly_chart(fig, width='stretch')
    
    # ------------------------------------------------------------------------
    # Risk Distribution Bar Chart
    # ------------------------------------------------------------------------
    with col2:
        st.subheader("Risk Distribution")
        risk_summary = risk_data['summary']
        
        risk_dist = pd.DataFrame({
            'Risk Level': ['High', 'Medium', 'Low'],
            'Components': [
                risk_summary['risk_distribution']['high_risk'],
                risk_summary['risk_distribution']['medium_risk'],
                risk_summary['risk_distribution']['low_risk']
            ]
        })
        
        fig = px.bar(
            risk_dist,
            x='Risk Level',
            y='Components',
            color='Risk Level',
            color_discrete_map={
                'High': ColorScheme.RISK_HIGH,
                'Medium': ColorScheme.RISK_MEDIUM,
                'Low': ColorScheme.RISK_LOW
            }
        )
        
        fig.update_layout(
            **ColorScheme.get_plotly_layout_defaults(),
            showlegend=False,
            xaxis_title="",
            yaxis_title="Component Count",
            margin=dict(t=10, b=10, l=10, r=10),
            height=350
        )
        
        st.plotly_chart(fig, width='stretch')
    
    st.markdown("---")
    
    # ========================================================================
    # STRATEGIC RECOMMENDATION
    # ========================================================================
    st.subheader("Strategic Recommendation")
    recommendation = executive_summary['recommendation']
    
    if "STRONG RECOMMEND" in recommendation:
        st.info(f"{recommendation}", icon=":material/check:")
    elif "RECOMMEND" in recommendation:
        st.info(f"{recommendation}")
    else:
        st.warning(f"⚠️ {recommendation}")