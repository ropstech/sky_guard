"""
Sky-Guard Dashboard: Animation Utilities
=========================================
Custom CSS animations and interactive effects.

Usage:
    from utils.animations import inject_custom_css, create_animated_metric
    
    inject_custom_css()  # Call once at app start
    create_animated_metric("ROI", "$1.2M", end_value=1200000)
"""

import streamlit as st
import streamlit.components.v1 as components


def inject_custom_css():
    """
    Inject custom CSS for smooth animations and hover effects.
    
    Should be called once in main dashboard_app.py after st.set_page_config().
    
    Features:
    - Page fade-in transitions
    - Metric card hover effects
    - Expander hover animations
    - Button hover effects
    - Chart fade-in animations
    - Pulse effect for critical metrics
    """
    
    st.markdown("""
    <style>
    /* ================================================================ */
    /* PHASE 2: ANIMATED DATA TRANSITIONS                              */
    /* ================================================================ */
    
    /* Smooth page transitions */
    .main .block-container {
        animation: fadeIn 0.5s ease-in;
    }
    
    @keyframes fadeIn {
        from { 
            opacity: 0; 
            transform: translateY(10px); 
        }
        to { 
            opacity: 1; 
            transform: translateY(0); 
        }
    }
    
    /* Metric card hover effects */
    [data-testid="stMetricValue"] {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    [data-testid="metric-container"]:hover [data-testid="stMetricValue"] {
        transform: scale(1.05);
        color: #DA7758;
    }
    
    /* Metric delta animation */
    [data-testid="stMetricDelta"] {
        transition: all 0.3s ease;
    }
    
    [data-testid="metric-container"]:hover [data-testid="stMetricDelta"] {
        transform: translateX(3px);
    }
    
    /* Expander hover animation */
    .streamlit-expanderHeader {
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background-color: rgba(218, 119, 88, 0.1) !important;
        border-left: 3px solid #DA7758;
        padding-left: 8px;
    }
    
    /* Button hover effects */
    .stButton > button {
        transition: all 0.3s ease;
        border: 1px solid rgba(218, 119, 88, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(218, 119, 88, 0.3);
        border-color: #DA7758;
        background-color: rgba(218, 119, 88, 0.1);
    }
    
    /* Dataframe hover effect */
    [data-testid="stDataFrame"] {
        transition: all 0.3s ease;
    }
    
    [data-testid="stDataFrame"]:hover {
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
        transform: translateY(-2px);
    }
    
    /* Info/Success/Warning box animations */
    .stAlert {
        animation: slideIn 1.0s ease-out;
    }
    
    @keyframes slideIn {
        from { 
            opacity: 0; 
            transform: translateX(-20px); 
        }
        to { 
            opacity: 1; 
            transform: translateX(0); 
        }
    }
    
    /* Staggered chart animations */
    .js-plotly-plot {
        animation: chartFadeIn 0.6s ease-out;
    }
    
    @keyframes chartFadeIn {
        from { 
            opacity: 0; 
            transform: scale(0.95); 
        }
        to { 
            opacity: 1; 
            transform: scale(1); 
        }
    }
    
    /* Pulse animation for critical metrics */
    .pulse-critical {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    /* Subheader fade-in with delay */
    h3 {
        animation: fadeIn 0.6s ease-in 0.2s both;
    }
    
    /* Stagger animation for columns */
    [data-testid="column"]:nth-child(1) {
        animation: fadeIn 0.5s ease-in 0.1s both;
    }
    
    [data-testid="column"]:nth-child(2) {
        animation: fadeIn 0.5s ease-in 0.2s both;
    }
    
    [data-testid="column"]:nth-child(3) {
        animation: fadeIn 0.5s ease-in 0.3s both;
    }
    
    [data-testid="column"]:nth-child(4) {
        animation: fadeIn 0.5s ease-in 0.4s both;
    }
    </style>
    """, unsafe_allow_html=True)


def create_animated_metric(
    label: str, 
    value: str, 
    delta: str = None, 
    end_value: float = None, 
    duration: int = 2000,
    is_critical: bool = False
):
    """
    Create an animated metric card with count-up effect.
    
    Args:
        label: Metric label (e.g., "Net Benefit")
        value: Display value as string (e.g., "$1.2M")
        delta: Delta text (e.g., "First Year")
        end_value: Numeric value for count-up animation
        duration: Animation duration in milliseconds
        is_critical: Apply pulse effect if True
        
    Example:
        >>> create_animated_metric(
        ...     label="Net Benefit",
        ...     value="$1164M",
        ...     delta="First Year",
        ...     end_value=1164000000,
        ...     duration=2000
        ... )
    """
    
    # If no animation value provided, use standard metric
    if end_value is None:
        st.metric(label, value, delta)
        return
    
    # Generate unique ID for this metric
    metric_id = label.replace(' ', '-').lower()
    critical_class = "pulse-critical" if is_critical else ""
    
    # Determine formatting based on value magnitude
    if end_value >= 1_000_000_000:
        format_type = "billions"
    elif end_value >= 1_000_000:
        format_type = "millions"
    elif end_value >= 1_000:
        format_type = "thousands"
    else:
        format_type = "number"
    
    html = f"""
    <div style="
        padding: 10px; 
        margin-bottom: 10px;
        border-radius: 8px;
        transition: all 0.3s ease;
    " 
    onmouseover="this.style.backgroundColor='rgba(218, 119, 88, 0.05)'"
    onmouseout="this.style.backgroundColor='transparent'">
        
        <div style="
            font-size: 0.875rem; 
            color: #888; 
            margin-bottom: 5px;
            font-weight: 500;
        ">
            {label}
        </div>
        
        <div id="metric-{metric_id}" 
             class="{critical_class}"
             style="
                 font-size: 2rem; 
                 font-weight: 600; 
                 color: white;
                 transition: all 0.3s ease;
             ">
            {value}
        </div>
        
        {f'''<div style="
            font-size: 0.875rem; 
            color: #DA7758; 
            margin-top: 5px;
            font-weight: 500;
        ">{delta}</div>''' if delta else ''}
    </div>
    
    <script>
    (function() {{
        const element = document.getElementById('metric-{metric_id}');
        const endValue = {end_value};
        const duration = {duration};
        const formatType = '{format_type}';
        const startTime = Date.now();
        
        function formatValue(val) {{
            if (formatType === 'billions') {{
                return '$' + (val / 1000000000).toFixed(1) + 'B';
            }} else if (formatType === 'millions') {{
                return '$' + (val / 1000000).toFixed(1) + 'M';
            }} else if (formatType === 'thousands') {{
                return (val / 1000).toFixed(0) + 'k';
            }} else {{
                return Math.round(val).toLocaleString();
            }}
        }}
        
        function animate() {{
            const elapsed = Date.now() - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            // Easing function (ease-out-cubic for smooth deceleration)
            const eased = 1 - Math.pow(1 - progress, 3);
            const current = eased * endValue;
            
            element.textContent = formatValue(current);
            
            if (progress < 1) {{
                requestAnimationFrame(animate);
            }} else {{
                // Ensure final value is exact
                element.textContent = formatValue(endValue);
            }}
        }}
        
        // Start animation
        animate();
    }})();
    </script>
    """
    
    components.html(html, height=120)


def apply_chart_animations(fig, transition_duration: int = 2000):
    """
    Apply smooth transition animations to Plotly charts.
    
    Args:
        fig: Plotly figure object
        transition_duration: Animation duration in milliseconds
        
    Returns:
        Modified figure with animations
        
    Example:
        >>> fig = px.bar(...)
        >>> fig = apply_chart_animations(fig)
        >>> st.plotly_chart(fig)
    """
    
    fig.update_layout(
        transition={
            'duration': transition_duration,
            'easing': 'cubic-in-out'
        },
        # Enhanced hover interactions
        hovermode='closest',
        hoverlabel=dict(
            bgcolor='#1E1F20',
            font_size=13,
            font_family="sans-serif",
            bordercolor='#DA7758'
        )
    )
    
    # Add hover effects to all traces
    if hasattr(fig, 'data'):
        for trace in fig.data:
            if hasattr(trace, 'marker'):
                # Smooth hover transitions
                trace.update(
                    hoverlabel=dict(
                        font=dict(color='white')
                    )
                )
    
    return fig