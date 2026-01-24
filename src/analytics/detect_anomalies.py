"""
Sky-Guard: Anomaly Detection Engine
====================================

Business Purpose:
    Identify components at risk of causing AOG events BEFORE they happen.
    
    Unlike traditional dashboards that show current status, this engine
    predicts which parts will become critical based on:
    - Stock depletion velocity
    - Supply chain vulnerabilities
    - Lead time risks
    
Technical Approach:
    Multi-factor risk scoring combining:
    1. Inventory health (stock vs. safety levels)
    2. Supplier reliability metrics
    3. Lead time volatility
    4. Financial impact (AOG cost exposure)
    
Output:
    Prioritized list of at-risk components with actionable insights.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
from datetime import datetime

from config.logging_config import get_logger

logger = get_logger(__name__)


class AnomalyDetector:
    """
    Detects supply chain anomalies using statistical analysis and business rules.
    """
    
    def __init__(self, data_dir='data/raw', output_dir='data/processed'):
        self.data_dir = Path(data_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("Anomaly Detector initialized")
        logger.info(f"Data source: {self.data_dir}")
        logger.info(f"Output destination: {self.output_dir}")
    
    def load_data(self):
        """Load inventory and supplier datasets."""
        logger.info("Loading datasets...")
        
        self.inventory = pd.read_csv(self.data_dir / 'inventory_master.csv')
        self.suppliers = pd.read_csv(self.data_dir / 'supplier_network.csv')
        
        logger.info(f"  ✓ Loaded {len(self.inventory)} inventory records")
        logger.info(f"  ✓ Loaded {len(self.suppliers)} supplier records")
    
    def calculate_inventory_risk_score(self, row):
        """
        Calculate inventory-specific risk score (0-100).
        
        Factors:
        - Stock coverage ratio (current vs. safety stock)
        - Criticality level
        - Lead time volatility
        """
        risk_score = 0
        
        # Factor 1: Stock Coverage (40 points max)
        if row['current_stock'] <= 0:
            risk_score += 40  # Out of stock = critical
        elif row['current_stock'] < row['reorder_point'] * 0.5:
            risk_score += 35  # Dangerously low
        elif row['current_stock'] < row['reorder_point']:
            risk_score += 25  # Below reorder point
        elif row['current_stock'] < row['safety_stock']:
            risk_score += 15  # Below safety stock
        
        # Factor 2: Criticality (30 points max)
        criticality_scores = {'Critical': 30, 'High': 20, 'Medium': 10, 'Low': 5}
        risk_score += criticality_scores.get(row['criticality'], 0)
        
        # Factor 3: Lead Time Volatility (30 points max)
        volatility_scores = {'High': 30, 'Medium': 15, 'Low': 5, 'Unknown': 20}
        risk_score += volatility_scores.get(row['lead_time_volatility'], 0)
        
        return min(risk_score, 100)  # Cap at 100
    
    def enrich_with_supplier_data(self):
        """
        Merge supplier risk metrics into inventory data.
        
        Business Value:
            Shows that component risk depends on supplier reliability.
            Critical part + unreliable supplier = highest risk.
        """
        logger.info("Enriching inventory with supplier risk metrics...")
        
        # Merge datasets
        self.enriched = self.inventory.merge(
            self.suppliers[['supplier_id', 'on_time_delivery_pct', 'risk_exposure', 'region', 'country', 'country_code']],
            on='supplier_id',
            how='left'
        )
        
        logger.info(f"  ✓ Enriched {len(self.enriched)} records with supplier data")
    
    def calculate_composite_risk(self):
        """
        Calculate final risk score combining inventory + supplier factors.
        
        Formula:
            Base Risk (inventory) + Supplier Risk Multiplier
        """
        logger.info("Calculating composite risk scores...")
        
        # Calculate base inventory risk
        self.enriched['inventory_risk_score'] = self.enriched.apply(
            self.calculate_inventory_risk_score, axis=1
        )
        
        # Supplier risk multiplier
        supplier_multipliers = {'High': 1.3, 'Medium': 1.1, 'Low': 1.0}
        self.enriched['supplier_multiplier'] = self.enriched['risk_exposure'].map(
            supplier_multipliers
        ).fillna(1.0)
        
        # Final composite risk
        self.enriched['composite_risk_score'] = (
            self.enriched['inventory_risk_score'] * 
            self.enriched['supplier_multiplier']
        ).clip(0, 100)
        
        # Risk classification
        self.enriched['risk_level'] = pd.cut(
            self.enriched['composite_risk_score'],
            bins=[0, 30, 60, 100],
            labels=['Low', 'Medium', 'High']
        )
        
        logger.info("  ✓ Composite risk scores calculated")
    
    def calculate_financial_exposure(self):
        """
        Calculate potential financial impact of each risk.
        
        Business Value:
            Translate technical risk into CFO language: "How much money is at stake?"
        
        Formula:
            If stock runs out, estimated AOG days = lead_time_days
            Financial Exposure = aog_cost_per_day × estimated_outage_days
        """
        logger.info("Calculating financial exposure...")
        
        # Estimate potential outage duration
        self.enriched['estimated_outage_days'] = self.enriched['lead_time_days'].fillna(30)
        
        # Calculate exposure
        self.enriched['financial_exposure_usd'] = (
            self.enriched['aog_cost_per_day'] * 
            self.enriched['estimated_outage_days']
        )
        
        # Only apply to high-risk items
        self.enriched.loc[
            self.enriched['risk_level'] != 'High', 
            'financial_exposure_usd'
        ] = 0
        
        total_exposure = self.enriched['financial_exposure_usd'].sum()
        logger.info(f"  ✓ Total financial exposure: ${total_exposure:,.0f}")
    
    def identify_top_risks(self, top_n=20):
        """
        Identify highest-priority risks for executive attention.
        
        Sorting Priority:
            1. Risk Level (High first)
            2. Financial Exposure (highest first)
            3. Composite Risk Score (highest first)
        """
        logger.info(f"Identifying top {top_n} risks...")
        
        high_risks = self.enriched[
            self.enriched['risk_level'] == 'High'
        ].sort_values(
            ['financial_exposure_usd', 'composite_risk_score'],
            ascending=False
        ).head(top_n)
        
        logger.info("=" * 70)
        logger.info(f"TOP {len(high_risks)} CRITICAL RISKS")
        logger.info("=" * 70)
        
        for idx, row in high_risks.iterrows():
            logger.info(
                f"  {row['part_number']:<20} | "
                f"Risk: {row['composite_risk_score']:.0f} | "
                f"Stock: {row['current_stock']:>4} / {row['safety_stock']:>4} | "
                f"Exposure: ${row['financial_exposure_usd']:>12,.0f}"
            )
        
        logger.info("=" * 70)
        
        return high_risks
    
    def generate_risk_summary(self):
        """
        Generate executive summary statistics.
        """
        summary = {
            'analysis_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_components_analyzed': len(self.enriched),
            'risk_distribution': {
                'high_risk': len(self.enriched[self.enriched['risk_level'] == 'High']),
                'medium_risk': len(self.enriched[self.enriched['risk_level'] == 'Medium']),
                'low_risk': len(self.enriched[self.enriched['risk_level'] == 'Low']),
            },
            'financial_metrics': {
                'total_exposure_usd': float(self.enriched['financial_exposure_usd'].sum()),
                'avg_exposure_per_high_risk_component': float(
                    self.enriched[self.enriched['risk_level'] == 'High']['financial_exposure_usd'].mean()
                ),
            },
            'top_risk_categories': self.enriched[
                self.enriched['risk_level'] == 'High'
            ]['category'].value_counts().head(5).to_dict(),
            'top_risk_regions': self.enriched[
                self.enriched['risk_level'] == 'High'
            ]['region'].value_counts().head(5).to_dict(),
        }
        
        return summary
    
    def save_results(self, top_risks):
        """
        Save risk analysis results to JSON for downstream processing.
        """
        logger.info("Saving results...")
        
        # Convert top risks to JSON-serializable format
        risk_records = top_risks[[
            'part_number', 'description', 'category', 'criticality',
            'current_stock', 'safety_stock', 'lead_time_days',
            'supplier_id', 'region', 'risk_exposure',
            'composite_risk_score', 'risk_level', 'financial_exposure_usd'
        ]].to_dict('records')
        
        summary = self.generate_risk_summary()
        
        output = {
            'summary': summary,
            'top_risks': risk_records,
        }
        
        output_file = self.output_dir / 'risk_analysis.json'
        with open(output_file, 'w') as f:
            json.dump(output, f, indent=2)
        
        logger.info(f"  ✓ Results saved to: {output_file}")
        
        # Also save full enriched dataset as CSV for further analysis
        csv_file = self.output_dir / 'enriched_inventory_with_risks.csv'
        self.enriched.to_csv(csv_file, index=False)
        logger.info(f"  ✓ Full dataset saved to: {csv_file}")
    
    def run_analysis(self, top_n=20):
        """
        Execute complete anomaly detection pipeline.
        """
        logger.info("=" * 70)
        logger.info("Sky-Guard Anomaly Detection Engine - STARTED")
        logger.info("=" * 70)
        
        self.load_data()
        self.enrich_with_supplier_data()
        self.calculate_composite_risk()
        self.calculate_financial_exposure()
        top_risks = self.identify_top_risks(top_n)
        self.save_results(top_risks)
        
        logger.info("=" * 70)
        logger.info("Anomaly Detection Complete")
        logger.info("=" * 70)
        
        # Print executive summary
        summary = self.generate_risk_summary()
        logger.info("\nEXECUTIVE SUMMARY:")
        logger.info(f"  High-Risk Components: {summary['risk_distribution']['high_risk']}")
        logger.info(f"  Total Financial Exposure: ${summary['financial_metrics']['total_exposure_usd']:,.0f}")
        logger.info(f"  Top Risk Category: {list(summary['top_risk_categories'].keys())[0] if summary['top_risk_categories'] else 'N/A'}")
        
        return top_risks


def main():
    """Entry point for anomaly detection."""
    detector = AnomalyDetector()
    detector.run_analysis(top_n=10)


if __name__ == "__main__":
    main()