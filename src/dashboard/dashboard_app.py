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

# Page configuration
st.set_page_config(
    page_title="Sky-Guard Dashboard",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional color scheme
COLORS = {
    'primary': "#095DB1",      # Deep navy
    'secondary': '#635BFF',    # Modern purple
    'success': '#00D4AA',      # Teal green
    'warning': '#F5A623',      # Amber
    'danger': '#E94B3C',       # Coral red
    'neutral': '#697386',      # Cool gray
    'background': '#F6F9FC',   # Light gray-blue
    'chart_palette': ['#635BFF', '#00D4AA', '#F5A623', '#E94B3C', '#0A2540']
}

# Custom CSS for professional styling
st.markdown(f"""
<style>
    .main-header {{
        font-size: 2.2rem;
        font-weight: 600;
        color: {COLORS['primary']};
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }}
    .subtitle {{
        font-size: 1rem;
        color: {COLORS['neutral']};
        font-weight: 400;
    }}
    .metric-label {{
        font-size: 0.875rem;
        color: {COLORS['neutral']};
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
    }}
    .status-operational {{
        background: linear-gradient(135deg, {COLORS['success']} 0%, #00B894 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 600;
        text-align: center;
    }}
    .risk-high {{
        color: {COLORS['danger']};
        font-weight: 600;
    }}
    .risk-medium {{
        color: {COLORS['warning']};
        font-weight: 600;
    }}
    .risk-low {{
        color: {COLORS['success']};
        font-weight: 600;
    }}
    div[data-testid="stMetricValue"] {{
        font-size: 1.8rem;
        font-weight: 600;
        color: {COLORS['primary']};
    }}
</style>
""", unsafe_allow_html=True)


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


def render_header():
    """Render dashboard header with branding."""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown('<p class="main-header">Sky-Guard Executive Dashboard</p>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">AI-Driven Operational Resilience for Aviation MRO</p>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="status-operational">● System Operational</div>', unsafe_allow_html=True)


def render_executive_summary(roi_data, risk_data):
    """Tab 1: Executive Summary with key metrics."""
    
    st.markdown("## Financial Performance")
    
    # ROI Metrics
    roi_metrics = roi_data['roi_metrics']
    executive_summary = roi_data['executive_summary']
    
    # Value proposition
    st.info(f"**{executive_summary['value_proposition']}**")
    
    st.markdown("")
    
    # Key metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Net Benefit",
            value=f"${roi_metrics['net_benefit_usd']/1e6:.1f}M",
            delta="First Year",
            delta_color="normal"
        )
    
    with col2:
        st.metric(
            label="ROI Ratio",
            value=f"{roi_metrics['roi_ratio']:.0f}:1",
            delta=f"{roi_metrics['roi_percentage']:.0f}%",
            delta_color="normal"
        )
    
    with col3:
        st.metric(
            label="Payback Period",
            value=f"{roi_metrics['payback_period_months']:.1f} mo",
            delta="Break-even",
            delta_color="normal"
        )
    
    with col4:
        st.metric(
            label="Risk Reduction",
            value=f"{roi_data['aog_cost_avoidance']['risk_reduction_percentage']:.0f}%",
            delta="AOG Prevention",
            delta_color="normal"
        )
    
    st.markdown("")
    st.markdown("---")
    st.markdown("")
    
    # Investment Breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Investment Structure")
        investment = roi_data['investment_breakdown']
        
        inv_data = pd.DataFrame({
            'Category': ['System Setup', 'Annual Operations', 'Mitigation Actions'],
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
            hole=0.5,
            color_discrete_sequence=COLORS['chart_palette']
        )
        fig.update_traces(
            textposition='inside',
            textinfo='percent',
            hovertemplate="<b>%{label}</b><br>€%{value:,.0f}<br>%{percent}<extra></extra>",
            marker=dict(line=dict(color='white', width=2))
        )
        fig.update_layout(
            showlegend=True,
            margin=dict(t=20, b=20, l=20, r=20),
            font=dict(size=12)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Risk Distribution")
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
                'High': COLORS['danger'],
                'Medium': COLORS['warning'],
                'Low': COLORS['success']
            }
        )
        fig.update_layout(
            showlegend=False,
            xaxis_title="",
            yaxis_title="Component Count",
            margin=dict(t=20, b=20, l=20, r=20),
            font=dict(size=12)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("")
    st.markdown("---")
    st.markdown("")
    
    # Strategic Recommendation
    st.markdown("### Strategic Recommendation")
    recommendation = executive_summary['recommendation']
    
    if "STRONG RECOMMEND" in recommendation:
        st.success(f"✓ {recommendation}")
    elif "RECOMMEND" in recommendation:
        st.info(f"→ {recommendation}")
    else:
        st.warning(f"⚠ {recommendation}")


def render_risk_analysis(risk_data, inventory_df):
    """Tab 2: Detailed risk analysis and component listing."""
    
    st.markdown("## Risk Overview")
    
    risk_summary = risk_data['summary']
    
    # Risk Overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "High-Risk Components",
            f"{risk_summary['risk_distribution']['high_risk']:,}",
            delta=f"of {risk_summary['total_components_analyzed']:,} total"
        )
    
    with col2:
        st.metric(
            "Total Financial Exposure",
            f"${risk_summary['financial_metrics']['total_exposure_usd']/1e9:.1f}B",
            delta="AOG Cost Risk"
        )
    
    with col3:
        top_category = list(risk_summary['top_risk_categories'].keys())[0]
        st.metric(
            "Top Risk Category",
            top_category,
            delta=f"{risk_summary['top_risk_categories'][top_category]} components"
        )
    
    st.markdown("")
    st.markdown("---")
    st.markdown("")
    
    # Top 20 Critical Risks
    st.markdown("### Critical Components Requiring Action")
    
    top_risks_df = pd.DataFrame(risk_data['top_risks'])
    
    # Format currency columns
    top_risks_df['Exposure'] = top_risks_df['financial_exposure_usd'].apply(
        lambda x: f"${x/1e6:.1f}M"
    )
    
    # Select and rename columns
    display_df = top_risks_df[[
        'part_number', 'category', 'criticality', 
        'current_stock', 'safety_stock', 'lead_time_days',
        'composite_risk_score', 'Exposure'
    ]].copy()
    
    display_df.columns = [
        'Part Number', 'Category', 'Criticality',
        'Stock', 'Safety Stock', 'Lead Time (days)',
        'Risk Score', 'Exposure'
    ]
    
    st.dataframe(
        display_df,
        width='stretch',
        hide_index=True
    )
    
    st.markdown("")
    st.markdown("---")
    st.markdown("")
    
    # Risk by Category and Region
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Risk by Category")
        category_risks = pd.DataFrame(
            list(risk_summary['top_risk_categories'].items()),
            columns=['Category', 'Count']
        )
        
        fig = px.bar(
            category_risks,
            y='Category',
            x='Count',
            orientation='h',
            color_discrete_sequence=[COLORS['secondary']]
        )
        fig.update_layout(
            showlegend=False,
            xaxis_title="High-Risk Components",
            yaxis_title="",
            margin=dict(t=20, b=20, l=20, r=20),
            font=dict(size=12)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Risk by Supplier Region")
        region_risks = pd.DataFrame(
            list(risk_summary['top_risk_regions'].items()),
            columns=['Region', 'Count']
        )
        
        fig = px.bar(
            region_risks,
            y='Region',
            x='Count',
            orientation='h',
            color_discrete_sequence=[COLORS['success']]
        )
        fig.update_layout(
            showlegend=False,
            xaxis_title="High-Risk Components",
            yaxis_title="",
            margin=dict(t=20, b=20, l=20, r=20),
            font=dict(size=12)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("")
    st.markdown("---")
    st.markdown("")
    
    # Interactive Data Explorer
    st.markdown("### Component Explorer")
    
    # Filters
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
            "Supplier Region",
            options=inventory_df['region'].unique(),
            default=inventory_df['region'].unique()
        )
    
    # Filter data
    filtered_df = inventory_df[
        (inventory_df['risk_level'].isin(selected_risk)) &
        (inventory_df['category'].isin(selected_category)) &
        (inventory_df['region'].isin(selected_region))
    ]
    
    st.caption(f"Showing {len(filtered_df):,} components")
    
    display_filtered = filtered_df[[
        'part_number', 'category', 'criticality', 'current_stock', 
        'safety_stock', 'risk_level', 'composite_risk_score', 
        'financial_exposure_usd', 'region'
    ]].sort_values('composite_risk_score', ascending=False).head(100)
    
    display_filtered.columns = [
        'Part Number', 'Category', 'Criticality', 'Stock',
        'Safety Stock', 'Risk Level', 'Risk Score',
        'Exposure ($)', 'Region'
    ]
    
    st.dataframe(
        display_filtered,
        width='stretch',
        hide_index=True
    )


def render_ai_recommendations(recommendations_data):
    """Tab 3: AI-generated strategic recommendations."""
    
    st.markdown("## AI-Generated Strategic Recommendations")
    
    metadata = recommendations_data['metadata']
    recommendations = recommendations_data['recommendations']
    
    st.caption(f"Model: {metadata['model_used']} • Generated {metadata['total_recommendations']} recommendations")
    
    st.markdown("")
    
    # Summary metrics
    total_exposure = sum(r['component']['financial_exposure_usd'] for r in recommendations)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "Components Analyzed",
            len(recommendations),
            delta="Top Priority Items"
        )
    
    with col2:
        st.metric(
            "Total Exposure Addressed",
            f"${total_exposure/1e6:.1f}M",
            delta="AOG Risk"
        )
    
    st.markdown("")
    st.markdown("---")
    st.markdown("")
    
    # Individual recommendations
    for idx, rec in enumerate(recommendations, 1):
        component = rec['component']
        ai_analysis = rec['ai_analysis']
        
        with st.expander(
            f"**{idx}. {component['part_number']} — {component['category']}** • "
            f"${component['financial_exposure_usd']/1e6:.1f}M exposure • "
            f"Confidence: {ai_analysis['confidence_level']}",
            expanded=(idx <= 2)
        ):
            # Root Cause
            st.markdown("#### Root Cause Analysis")
            st.markdown(ai_analysis['root_cause'])
            
            st.markdown("")
            
            # Mitigation Options
            st.markdown("#### Mitigation Options")
            
            options_df = pd.DataFrame(ai_analysis['mitigation_options'])
            
            # Format currency
            options_df['Cost'] = options_df['estimated_cost_usd'].apply(
                lambda x: f"${x:,.0f}"
            )
            
            display_options = options_df[[
                'option', 'description', 'Cost',
                'implementation_time_days', 'risk_reduction_pct'
            ]].copy()
            
            display_options.columns = [
                'Option', 'Description', 'Cost',
                'Timeline (days)', 'Risk Reduction (%)'
            ]
            
            st.dataframe(
                display_options,
                width='stretch',
                hide_index=True
            )
            
            st.markdown("")
            
            # Recommended Action
            st.markdown("#### Recommended Action")
            st.success(ai_analysis['recommended_action'])
            
            # Expected ROI
            st.markdown("#### Expected Return")
            st.info(ai_analysis['expected_roi'])


def main():
    """Main dashboard application."""
    
    # Check if data exists
    data_dir = Path('data/processed')
    required_files = ['risk_analysis.json', 'ai_recommendations.json', 'roi_analysis.json']
    
    missing_files = [f for f in required_files if not (data_dir / f).exists()]
    
    if missing_files:
        st.error(f"Missing required data files: {', '.join(missing_files)}")
        st.info("""
        **Please run the analysis pipeline first:**
        ```bash
        python src/data_generation/generate_data.py
        python src/analytics/detect_anomalies.py
        python src/ai_reasoning/ai_reasoning_engine.py
        python src/analytics/roi_calculator.py
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
        st.error(f"Error loading data: {e}")
        return
    
    # Render header
    render_header()
    
    st.markdown("")
    st.markdown("---")
    st.markdown("")
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs([
        "Financial Performance",
        "Risk Analysis",
        "AI Recommendations"
    ])
    
    with tab1:
        render_executive_summary(roi_data, risk_data)
    
    with tab2:
        render_risk_analysis(risk_data, inventory_df)
    
    with tab3:
        render_ai_recommendations(recommendations_data)
    
    # Footer
    st.markdown("")
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #697386; font-size: 0.875rem;'>
        Sky-Guard v1.0 • AI-Powered Supply Chain Intelligence • © 2026 RS Technologies, Inc.
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()