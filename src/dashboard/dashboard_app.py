"""
Sky-Guard: Executive Dashboard
===============================

Business Purpose:
    Interactive web interface for C-level executives to visualize:
    - Financial ROI and business case
    - High-risk components requiring action
    - AI-generated strategic recommendations
    
    Replaces static PowerPoint slides with live, data-driven insights.
    
Usage:
    streamlit run src/dashboard/dashboard_app.py
    
    Then open browser at: http://localhost:8501
"""

import streamlit as st
import pandas as pd
import json
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu

# Page configuration
st.set_page_config(
    page_title="Sky-Guard Dashboard",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)


class DashboardData:
    """Loads and caches all analysis data."""
    
    def __init__(self, data_dir='data/processed'):
        self.data_dir = Path(data_dir)
    
    @st.cache_data
    def load_risk_analysis(_self):
        """Load risk analysis results."""
        with open(_self.data_dir / 'risk_analysis.json', 'r') as f:
            return json.load(f)
    
    @st.cache_data
    def load_recommendations(_self):
        """Load AI recommendations."""
        with open(_self.data_dir / 'ai_recommendations.json', 'r') as f:
            return json.load(f)
    
    @st.cache_data
    def load_roi_analysis(_self):
        """Load ROI analysis."""
        with open(_self.data_dir / 'roi_analysis.json', 'r') as f:
            return json.load(f)
    
    @st.cache_data
    def load_enriched_inventory(_self):
        """Load full enriched inventory data."""
        return pd.read_csv(_self.data_dir / 'enriched_inventory_with_risks.csv')


def render_sidebar(risk_data, roi_data):
    """Sidebar with professional navigation and key metrics."""
    
    with st.sidebar:
        # Branding (Logo/Title Area)
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
        st.markdown("### Navigation")

        # Navigation with Icons (The Upgrade)
        # Icons originate from Bootstrap Icons: https://icons.getbootstrap.com/
        page = option_menu(
            menu_title=None,  # Hide title
            options=["Financial Performance", "Risk Analysis", "AI Recommendations", "Settings"],
            icons=["graph-up-arrow", "shield-exclamation", "cpu", "sliders"], 
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"color": "#DA7758", "font-size": "16px"}, 
                "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#141413"},
                "nav-link-selected": {"background-color": "#7C4937"},
            }
        )
        
        st.markdown("---")
        
        # KPI Section inside an expander or dedicated container for cleaner look
        st.markdown("### Quick Stats")
        
        roi_metrics = roi_data['roi_metrics']
        risk_summary = risk_data['summary']
        
        # Using columns inside sidebar for compact metric view
        c1, c2 = st.columns(2)
        with c1:
            st.metric("ROI Ratio", f"{roi_metrics['roi_ratio']:.0f}:1")
            st.metric("Net Benefit", f"${roi_metrics['net_benefit_usd']/1e6:.0f}M")
        with c2:
            st.metric("High-Risk Items", f"{risk_summary['risk_distribution']['high_risk']:,}")

        st.markdown("---")
        
        # System Status
        st.markdown("### System Status")
        st.success("Operational", icon=":material/check_circle:")

        st.markdown("---")
        
        # Subtle Footer
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


def render_financial_performance(roi_data, risk_data):
    """Page 1: Financial Performance."""
    
    st.title("Financial Performance")
    
    roi_metrics = roi_data['roi_metrics']
    executive_summary = roi_data['executive_summary']
    
    # Value proposition banner
    st.info(f"**{executive_summary['value_proposition']}**", icon=":material/celebration:")
    
    st.markdown("")
    
    # Key metrics
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
    
    # Charts
    col1, col2 = st.columns(2)
    
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
            hole=0.6
        )
        fig.update_traces(
            textposition='inside',
            textinfo='percent',
            hovertemplate="<b>%{label}</b><br>$%{value:,.0f}<br>%{percent}<extra></extra>"
        )
        fig.update_layout(
            showlegend=True,
            margin=dict(t=10, b=10, l=10, r=10),
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)
    
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
                'High': "#7D2D26",
                'Medium': "#81530A",
                'Low': "#058168"
            }
        )
        fig.update_layout(
            showlegend=False,
            xaxis_title="",
            yaxis_title="Component Count",
            margin=dict(t=10, b=10, l=10, r=10),
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Recommendation
    st.subheader("Strategic Recommendation")
    recommendation = executive_summary['recommendation']
    
    if "STRONG RECOMMEND" in recommendation:
        st.success(f"{recommendation}", icon=":material/check:")
    elif "RECOMMEND" in recommendation:
        st.info(f"ℹ️ {recommendation}")
    else:
        st.warning(f"⚠️ {recommendation}")


def render_risk_analysis(risk_data, inventory_df):
    """Page 2: Risk Analysis."""
    
    st.title("Risk Analysis")
    
    risk_summary = risk_data['summary']
    
    # Overview metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "High-Risk Components",
            f"{risk_summary['risk_distribution']['high_risk']:,}",
            delta=f"of {risk_summary['total_components_analyzed']:,} total"
        )
    
    with col2:
        st.metric(
            "Total Exposure",
            f"${risk_summary['financial_metrics']['total_exposure_usd']/1e9:.1f}B",
            delta="AOG Cost Risk"
        )
    
    with col3:
        top_category = list(risk_summary['top_risk_categories'].keys())[0]
        st.metric(
            "Top Risk Category",
            top_category,
            delta=f"{risk_summary['top_risk_categories'][top_category]} items"
        )
    
    st.markdown("---")
    
    # Critical components table
    st.subheader("Critical Components Requiring Action")
    
    top_risks_df = pd.DataFrame(risk_data['top_risks'])
    
    top_risks_df['Exposure'] = top_risks_df['financial_exposure_usd'].apply(
        lambda x: f"${x/1e6:.1f}M"
    )
    
    display_df = top_risks_df[[
        'part_number', 'category', 'criticality', 
        'current_stock', 'safety_stock', 'lead_time_days',
        'composite_risk_score', 'Exposure'
    ]].copy()
    
    display_df.columns = [
        'Part Number', 'Category', 'Criticality',
        'Stock', 'Safety Stock', 'Lead Time',
        'Risk Score', 'Exposure'
    ]
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=400
    )
    
    st.markdown("---")
    
    # Risk breakdown charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Risk by Category")
        
        category_data = pd.DataFrame(
            list(risk_summary['top_risk_categories'].items()),
            columns=['Category', 'Count']
        ).sort_values('Count', ascending=True)
        
        fig = px.bar(
            category_data,
            y='Category',
            x='Count',
            orientation='h'
        )
        fig.update_layout(
            showlegend=False,
            xaxis_title="High-Risk Components",
            yaxis_title="",
            margin=dict(t=10, b=10, l=10, r=10),
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Risk by Region")
        
        region_data = pd.DataFrame(
            list(risk_summary['top_risk_regions'].items()),
            columns=['Region', 'Count']
        ).sort_values('Count', ascending=True)
        
        fig = px.bar(
            region_data,
            y='Region',
            x='Count',
            orientation='h'
        )
        fig.update_layout(
            showlegend=False,
            xaxis_title="High-Risk Components",
            yaxis_title="",
            margin=dict(t=10, b=10, l=10, r=10),
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Interactive explorer
    st.subheader("Component Explorer")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_risk = st.multiselect(
            "Risk Level",
            options=inventory_df['risk_level'].unique(),
            default=['High']
        )
    
    with col2:
        selected_category = st.multiselect(
            "Category",
            options=inventory_df['category'].unique(),
            default=inventory_df['category'].unique()
        )
    
    with col3:
        selected_region = st.multiselect(
            "Region",
            options=inventory_df['region'].unique(),
            default=inventory_df['region'].unique()
        )
    
    filtered_df = inventory_df[
        (inventory_df['risk_level'].isin(selected_risk)) &
        (inventory_df['category'].isin(selected_category)) &
        (inventory_df['region'].isin(selected_region))
    ]
    
    st.caption(f"Showing {len(filtered_df):,} of {len(inventory_df):,} components")
    
    display_filtered = filtered_df[[
        'part_number', 'category', 'criticality', 'current_stock', 
        'safety_stock', 'risk_level', 'composite_risk_score', 
        'financial_exposure_usd', 'region'
    ]].sort_values('composite_risk_score', ascending=False).head(100)
    
    display_filtered.columns = [
        'Part', 'Category', 'Criticality', 'Stock',
        'Safety', 'Risk', 'Score', 'Exposure', 'Region'
    ]
    
    st.dataframe(
        display_filtered,
        use_container_width=True,
        hide_index=True,
        height=400
    )


def render_ai_recommendations(recommendations_data):
    """Page 3: AI Recommendations."""
    
    st.title("AI-Powered Recommendations")
    
    metadata = recommendations_data['metadata']
    recommendations = recommendations_data['recommendations']
    
    st.caption(f"🤖 Model: {metadata['model_used']} • {metadata['total_recommendations']} recommendations generated")
    
    # Summary
    total_exposure = sum(r['component']['financial_exposure_usd'] for r in recommendations)
    
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
    
    # Recommendations
    for idx, rec in enumerate(recommendations, 1):
        component = rec['component']
        ai = rec['ai_analysis']
        
        with st.expander(
            f"**{idx}. {component['part_number']}** — {component['category']} • "
            f"${component['financial_exposure_usd']/1e6:.1f}M • "
            f"Confidence: {ai['confidence_level']}",
            expanded=(idx <= 2)
        ):
            st.markdown("#### Root Cause")
            st.write(ai['root_cause'])
            
            st.markdown("#### Mitigation Options")
            
            options_df = pd.DataFrame(ai['mitigation_options'])
            options_df['Cost'] = options_df['estimated_cost_usd'].apply(lambda x: f"${x:,.0f}")
            
            display = options_df[[
                'option', 'description', 'Cost',
                'implementation_time_days', 'risk_reduction_pct'
            ]].copy()
            
            display.columns = ['Option', 'Description', 'Cost', 'Timeline (days)', 'Risk Reduction (%)']
            
            st.dataframe(display, use_container_width=True, hide_index=True)
            
            st.markdown("#### Recommended Action")
            st.success(ai['recommended_action'])
            
            st.markdown("#### Expected ROI")
            st.info(ai['expected_roi'])


def render_settings():
    """Page 4: Settings."""
    
    st.title("Settings")
    
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
    
    st.subheader("Regenerate Data")
    
    if st.button("🔄 Generate New Dataset"):
        st.info("Run: `uv run python src/data_generation/generate_data.py`")
    
    if st.button("🔍 Validate Data"):
        st.info("Run: `uv run python src/data_generation/validate_data.py`")
    
    if st.button("📊 Run Analysis"):
        st.info("Run: `uv run python src/analytics/detect_anomalies.py`")
    
    st.markdown("---")
    
    st.subheader("About")
    st.write("**Sky-Guard v1.0**")
    st.write("AI-Driven Operational Resilience for Aviation MRO")
    st.caption("© 2026 RS Technologies, Inc.")


def main():
    """Main dashboard application."""
    
    # Check data availability
    data_dir = Path('data/processed')
    required_files = ['risk_analysis.json', 'ai_recommendations.json', 'roi_analysis.json']
    
    missing = [f for f in required_files if not (data_dir / f).exists()]
    
    if missing:
        st.error(f"❌ Missing: {', '.join(missing)}")
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
    
    # Load data
    data = DashboardData()
    
    try:
        risk_data = data.load_risk_analysis()
        recommendations_data = data.load_recommendations()
        roi_data = data.load_roi_analysis()
        inventory_df = data.load_enriched_inventory()
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        return
    
    # Sidebar navigation
    page = render_sidebar(risk_data, roi_data)
    
    # Render selected page
    if page == "Financial Performance":
        render_financial_performance(roi_data, risk_data)
    elif page == "Risk Analysis":
        render_risk_analysis(risk_data, inventory_df)
    elif page == "AI Recommendations":
        render_ai_recommendations(recommendations_data)
    elif page == "Settings":
        render_settings()


if __name__ == "__main__":
    main()