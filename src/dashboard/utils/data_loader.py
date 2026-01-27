"""
Sky-Guard Dashboard: Data Loader
=================================
Centralized data loading with caching.

Usage:
    from utils.data_loader import DashboardData
    
    data = DashboardData()
    roi_data = data.load_roi_analysis()
"""

import streamlit as st
import pandas as pd
import json
from pathlib import Path


class DashboardData:
    """
    Centralized data loader for all dashboard components.
    
    Uses Streamlit's caching mechanism to avoid redundant file I/O.
    All data is loaded from data/processed/ directory.
    """
    
    def __init__(self, data_dir='data/processed'):
        """
        Initialize data loader.
        
        Args:
            data_dir: Path to processed data directory
        """
        self.data_dir = Path(data_dir)
    
    @st.cache_data
    def load_risk_analysis(_self):
        """
        Load risk analysis results.
        
        Returns:
            dict: Risk analysis data including summary and top risks
            
        Raises:
            FileNotFoundError: If risk_analysis.json doesn't exist
        """
        file_path = _self.data_dir / 'risk_analysis.json'
        with open(file_path, 'r') as f:
            return json.load(f)
    
    @st.cache_data
    def load_recommendations(_self):
        """
        Load AI-generated recommendations.
        
        Returns:
            dict: AI recommendations with metadata
            
        Raises:
            FileNotFoundError: If ai_recommendations.json doesn't exist
        """
        file_path = _self.data_dir / 'ai_recommendations.json'
        with open(file_path, 'r') as f:
            return json.load(f)
    
    @st.cache_data
    def load_roi_analysis(_self):
        """
        Load ROI analysis results.
        
        Returns:
            dict: ROI metrics and executive summary
            
        Raises:
            FileNotFoundError: If roi_analysis.json doesn't exist
        """
        file_path = _self.data_dir / 'roi_analysis.json'
        with open(file_path, 'r') as f:
            return json.load(f)
    
    @st.cache_data
    def load_enriched_inventory(_self):
        """
        Load full enriched inventory data.
        
        Returns:
            pd.DataFrame: Complete inventory with risk scores
            
        Raises:
            FileNotFoundError: If enriched_inventory_with_risks.csv doesn't exist
        """
        file_path = _self.data_dir / 'enriched_inventory_with_risks.csv'
        return pd.read_csv(file_path)
    
    def check_data_availability(self) -> tuple[bool, list]:
        """
        Check if all required data files exist.
        
        Returns:
            tuple: (all_exist: bool, missing_files: list)
            
        Example:
            >>> data = DashboardData()
            >>> exists, missing = data.check_data_availability()
            >>> if not exists:
            >>>     print(f"Missing: {missing}")
        """
        required_files = [
            'risk_analysis.json',
            'ai_recommendations.json',
            'roi_analysis.json',
            'enriched_inventory_with_risks.csv'
        ]
        
        missing = [
            f for f in required_files 
            if not (self.data_dir / f).exists()
        ]
        
        return (len(missing) == 0, missing)