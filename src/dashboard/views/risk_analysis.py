"""
Sky-Guard Dashboard: Risk Analysis Page
========================================
Comprehensive risk visualization and component explorer.

Usage:
    from pages.risk_analysis import render_risk_analysis
    
    render_risk_analysis(risk_data, inventory_df)
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from config.theme import ColorScheme


def render_risk_analysis(risk_data: dict, inventory_df: pd.DataFrame):
    """
    Render Risk Analysis page.
    
    Displays:
    - High-level risk metrics
    - Global risk distribution map
    - Critical components table
    - Risk breakdowns by category and region
    - Interactive component explorer
    
    Args:
        risk_data: Risk analysis results
        inventory_df: Full enriched inventory DataFrame
    """
    
    st.title("Risk Analysis")
    
    risk_summary = risk_data['summary']
    
    # ========================================================================
    # OVERVIEW METRICS
    # ========================================================================
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
    
    # ========================================================================
    # GLOBAL RISK MAP
    # ========================================================================
    st.subheader("Global Risk Distribution")
    
    try:
        map_fig = _render_global_risk_map(inventory_df)
        st.plotly_chart(map_fig, width='stretch')
    except Exception as e:
        st.error(f"Map rendering failed: {e}")
    
    st.markdown("---")
    
    # ========================================================================
    # CRITICAL COMPONENTS TABLE
    # ========================================================================
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
        width='stretch',
        hide_index=True,
        height=400
    )
    
    st.markdown("---")
    
    # ========================================================================
    # RISK BREAKDOWN CHARTS
    # ========================================================================
    col1, col2 = st.columns(2)
    
    # ------------------------------------------------------------------------
    # Risk by Category
    # ------------------------------------------------------------------------
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
            orientation='h',
            color='Count',
            color_continuous_scale=[
                [0, ColorScheme.SECONDARY],
                [0.5, ColorScheme.PRIMARY],
                [1, ColorScheme.RISK_HIGH]
            ]
        )
        
        fig.update_layout(
            **ColorScheme.get_plotly_layout_defaults(),
            showlegend=False,
            xaxis_title="High-Risk Components",
            yaxis_title="",
            margin=dict(t=10, b=10, l=10, r=10),
            height=350,
            coloraxis_showscale=False
        )
        
        st.plotly_chart(fig, width='stretch')

    # ------------------------------------------------------------------------
    # Risk by Region
    # ------------------------------------------------------------------------
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
            orientation='h',
            color='Count',
            color_continuous_scale=[
                [0, ColorScheme.SECONDARY],
                [0.5, ColorScheme.PRIMARY],
                [1, ColorScheme.RISK_HIGH]
            ]
        )
        
        fig.update_layout(
            **ColorScheme.get_plotly_layout_defaults(),
            showlegend=False,
            xaxis_title="High-Risk Components",
            yaxis_title="",
            margin=dict(t=10, b=10, l=10, r=10),
            height=350,
            coloraxis_showscale=False
        )
        
        st.plotly_chart(fig, width='stretch')
    
    st.markdown("---")
    
    # ========================================================================
    # INTERACTIVE COMPONENT EXPLORER
    # ========================================================================
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
    
    # Filter data
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
        width='stretch',
        hide_index=True,
        height=400
    )


def _render_global_risk_map(inventory_df: pd.DataFrame):
    """
    Internal helper: Render choropleth map of global risk distribution.
    
    Args:
        inventory_df: Full inventory DataFrame
        
    Returns:
        Plotly figure object
    """
    
    # Filter to high-risk components only
    high_risk_df = inventory_df[inventory_df['risk_level'] == 'High'].copy()
    
    if 'country_code' not in high_risk_df.columns:
        raise ValueError("country_code column not found in inventory data.")
    
    # Aggregate by country
    country_risk_counts = high_risk_df.groupby('country_code').size().reset_index(name='risk_count')
    country_regions = high_risk_df.groupby('country_code')['region'].first().reset_index()
    map_data = country_risk_counts.merge(country_regions, on='country_code', how='left')
    
    # Create choropleth
    fig = px.choropleth(
        map_data,
        locations='country_code',
        color='risk_count',
        hover_name='region',
        hover_data={
            'risk_count': ':,', 
            'country_code': True,
            'region': True
        },
        color_continuous_scale=ColorScheme.MAP_GRADIENT,
        labels={'risk_count': 'High-Risk Components'},
        projection='natural earth'
    )
    
    # Update map styling
    fig.update_geos(
        showcoastlines=True,
        coastlinecolor='#444',
        showland=True,
        landcolor=ColorScheme.BG_PRIMARY,
        showocean=True,
        oceancolor='#0D0E10',
        showcountries=True,
        countrycolor='#333'
    )
    
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor=ColorScheme.BG_SECONDARY,
        geo=dict(bgcolor=ColorScheme.BG_SECONDARY),
        height=450,
        coloraxis_colorbar=dict(
            title="Risk Level",
            tickfont=dict(color='white'),
            bgcolor=ColorScheme.BG_TERTIARY
        )
    )
    
    return fig