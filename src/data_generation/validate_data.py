"""
Sky-Guard: Data Quality Validation
===================================
Validates generated MRO datasets against business rules.
"""

import pandas as pd
from pathlib import Path
from config.logging_config import get_logger

logger = get_logger(__name__)


class DataQualityValidator:
    """Validates MRO datasets against business rules."""
    
    def __init__(self):
        self.validation_results = {}
    
    def validate_inventory(self, df):
        """Validate inventory master data."""
        logger.info(f"Validating inventory: {len(df)} records")
        
        checks = {
            'unique_parts': df['part_number'].is_unique,
            'valid_costs': (df['unit_cost_usd'] > 0).all(),
            'valid_criticality': df['criticality'].isin(['Critical', 'High', 'Medium', 'Low']).all(),
        }
        
        for check, passed in checks.items():
            status = "✓" if passed else "✗"
            logger.info(f"  {status} {check}: {'PASS' if passed else 'FAIL'}")
        
        return all(checks.values())
    
    def validate_suppliers(self, df):
        """Validate supplier network data."""
        logger.info(f"Validating suppliers: {len(df)} records")
        
        checks = {
            'unique_suppliers': df['supplier_id'].is_unique,
            'valid_otd': ((df['on_time_delivery_pct'] >= 0) & (df['on_time_delivery_pct'] <= 100)).all(),
            'valid_tier': df['tier'].isin(['Tier-1', 'Tier-2', 'Tier-3']).all(),
        }
        
        for check, passed in checks.items():
            status = "✓" if passed else "✗"
            logger.info(f"  {status} {check}: {'PASS' if passed else 'FAIL'}")
        
        return all(checks.values())
    
    def validate_risks(self, df):
        """Validate risk event feed."""
        logger.info(f"Validating risks: {len(df)} records")
        
        checks = {
            'unique_events': df['event_id'].is_unique,
            'valid_severity': df['severity'].isin(['Critical', 'High', 'Medium', 'Low']).all(),
            'valid_duration': (df['estimated_duration_days'] > 0).all(),
        }
        
        for check, passed in checks.items():
            status = "✓" if passed else "✗"
            logger.info(f"  {status} {check}: {'PASS' if passed else 'FAIL'}")
        
        return all(checks.values())
    
    def run_validation(self, data_dir='data/raw'):
        """Run complete validation suite."""
        logger.info("=" * 70)
        logger.info("Sky-Guard Data Validation")
        logger.info("=" * 70)
        
        data_path = Path(data_dir)
        
        try:
            # Load datasets
            inventory = pd.read_csv(data_path / 'inventory_master.csv')
            suppliers = pd.read_csv(data_path / 'supplier_network.csv')
            risks = pd.read_csv(data_path / 'risk_events.csv')
            
            # Run validations
            inv_valid = self.validate_inventory(inventory)
            sup_valid = self.validate_suppliers(suppliers)
            risk_valid = self.validate_risks(risks)
            
            # Overall result
            all_passed = inv_valid and sup_valid and risk_valid
            
            logger.info("=" * 70)
            if all_passed:
                logger.info("✅ Overall Validation: PASS")
            else:
                logger.error("❌ Overall Validation: FAIL")
            logger.info("=" * 70)
            
            return all_passed
            
        except FileNotFoundError as e:
            logger.error(f"Data files not found: {e}")
            logger.error("Run generate_data.py first!")
            return False


def main():
    """Entry point for validation."""
    validator = DataQualityValidator()
    return validator.run_validation()


if __name__ == "__main__":
    import sys
    sys.exit(0 if main() else 1)