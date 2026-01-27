"""
Sky-Guard Dashboard: Theme Configuration
=========================================
Centralized color scheme and theme constants.

Usage:
    from config.theme import ColorScheme
    
    fig.update_layout(
        paper_bgcolor=ColorScheme.BG_SECONDARY,
        font=dict(color='white')
    )
"""


class ColorScheme:
    """
    Zentrale Farbpalette für alle Visualisierungen.
    
    Abgeleitet von .streamlit/config.toml Theme-Settings.
    Diese Klasse wird von allen Dashboard-Components verwendet
    um ein konsistentes Look & Feel zu gewährleisten.
    """
    
    # ========================================================================
    # BRAND COLORS (from config.toml)
    # ========================================================================
    PRIMARY = "#DA7758"      # Terrakotta (Akzentfarbe)
    SECONDARY = "#7C4937"    # Dunkles Terrakotta
    
    # ========================================================================
    # SEMANTIC RISK COLORS
    # ========================================================================
    RISK_HIGH = "#7D2D26"    # Dunkles Rot
    RISK_MEDIUM = "#81530A"  # Bernstein/Gold
    RISK_LOW = "#058168"     # Jade/Teal
    
    # ========================================================================
    # BACKGROUND PALETTE
    # ========================================================================
    BG_PRIMARY = "#1A1C24"
    BG_SECONDARY = "#262624"
    BG_TERTIARY = "#1E1F20"
    
    # ========================================================================
    # NEUTRAL GRAYS
    # ========================================================================
    GRAY_LIGHT = "#7c7c7c"
    GRAY_DARK = "#404040"
    
    # ========================================================================
    # CHART-SPECIFIC PALETTES
    # ========================================================================
    INVESTMENT_PALETTE = [
        "#7C4937",  # Setup (Primary Brown)
        "#DA7758",  # Operations (Terrakotta)
        "#B85C3E",  # Mitigations (Medium)
    ]
    
    REGION_PALETTE = [
        "#7C4937",  # Asia-Pacific
        "#DA7758",  # Europe
        "#B85C3E",  # North America
        "#9D6B55",  # Middle East
    ]
    
    CATEGORY_PALETTE = [
        "#7C4937", "#DA7758", "#B85C3E", 
        "#9D6B55", "#C9886D", "#8F5944"
    ]
    
    # Map Gradient (for choropleth)
    MAP_GRADIENT = [
        [0, '#1A3D2E'],      # Dark green (low risk)
        [0.4, '#4A3A1A'],    # Dark yellow-brown
        [0.7, '#7F5C2E'],    # Medium orange-brown
        [1, '#7D2D26']       # Dark red (high risk)
    ]
    
    # ========================================================================
    # UTILITY METHODS
    # ========================================================================
    
    @classmethod
    def get_risk_color(cls, risk_level: str) -> str:
        """
        Return semantic color for risk level.
        
        Args:
            risk_level: 'High', 'Medium', or 'Low'
            
        Returns:
            Hex color code
            
        Example:
            >>> ColorScheme.get_risk_color('High')
            '#7D2D26'
        """
        mapping = {
            'High': cls.RISK_HIGH,
            'Medium': cls.RISK_MEDIUM,
            'Low': cls.RISK_LOW
        }
        return mapping.get(risk_level, cls.GRAY_LIGHT)
    
    @classmethod
    def get_plotly_layout_defaults(cls) -> dict:
        """
        Return default Plotly layout settings for consistent theming.
        
        Returns:
            Dictionary with layout parameters
            
        Example:
            >>> fig.update_layout(**ColorScheme.get_plotly_layout_defaults())
        """
        return {
            'paper_bgcolor': cls.BG_SECONDARY,
            'plot_bgcolor': cls.BG_SECONDARY,
            'font': dict(color='white'),
            'xaxis': dict(gridcolor=cls.GRAY_DARK),
            'yaxis': dict(gridcolor=cls.GRAY_DARK),
        }
    
    @classmethod
    def get_hover_label_style(cls) -> dict:
        """
        Return consistent hover label styling.
        
        Returns:
            Dictionary with hoverlabel parameters
        """
        return {
            'bgcolor': cls.BG_TERTIARY,
            'font_size': 12,
            'font_family': "sans-serif",
            'bordercolor': cls.PRIMARY
        }