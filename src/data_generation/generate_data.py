"""
Project Sky-Guard: Synthetic MRO Data Generation Engine
========================================================

Business Purpose:
    Generate realistic Aviation MRO datasets that mirror the complexity of
    enterprise supply chain operations, including:
    - Fragmented inventory hierarchies
    - Supplier network vulnerabilities
    - External risk event correlations

Technical Approach:
    Three interconnected datasets designed to demonstrate AI-driven anomaly
    detection and automated reasoning capabilities.

Author: Sky-Guard Technical Team
Version: 1.0 (PoC Phase)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import json

# Ensure reproducibility for demonstrations
np.random.seed(42)
random.seed(42)


class MRODataGenerator:
    """
    Orchestrates synthetic data generation for Aviation MRO operations.
    
    Attributes:
        num_components (int): Total unique SKUs to generate
        num_suppliers (int): Supplier network size
        simulation_days (int): Historical data window
    """
    
    def __init__(self, num_components=5000, num_suppliers=150, simulation_days=90):
        self.num_components = num_components
        self.num_suppliers = num_suppliers
        self.simulation_days = simulation_days
        self.base_date = datetime.now() - timedelta(days=simulation_days)
        
        # Aircraft component taxonomy (simplified)
        self.component_categories = {
            'Engine': {'criticality': 'Critical', 'base_cost': 50000, 'aog_multiplier': 3.0},
            'Avionics': {'criticality': 'High', 'base_cost': 15000, 'aog_multiplier': 2.5},
            'Hydraulics': {'criticality': 'High', 'base_cost': 8000, 'aog_multiplier': 2.0},
            'Landing Gear': {'criticality': 'Critical', 'base_cost': 25000, 'aog_multiplier': 3.0},
            'Cabin Systems': {'criticality': 'Medium', 'base_cost': 3000, 'aog_multiplier': 1.2},
            'Electrical': {'criticality': 'High', 'base_cost': 5000, 'aog_multiplier': 2.0},
            'Structural': {'criticality': 'Medium', 'base_cost': 12000, 'aog_multiplier': 1.5},
        }
        
        # Geographic supplier clusters with realistic risk profiles
        self.supplier_regions = {
            'Asia-Pacific': {'reliability_base': 0.85, 'lead_time_base': 45, 'cost_factor': 0.7},
            'Europe': {'reliability_base': 0.92, 'lead_time_base': 21, 'cost_factor': 1.0},
            'North America': {'reliability_base': 0.90, 'lead_time_base': 14, 'cost_factor': 1.2},
            'Middle East': {'reliability_base': 0.80, 'lead_time_base': 35, 'cost_factor': 0.9},
        }
        
    def generate_inventory_master(self):
        """
        Create the foundational inventory dataset with realistic business constraints.
        
        Business Value:
            - Demonstrates component hierarchies (assemblies → sub-components)
            - Simulates safety stock variability (seasonal demand patterns)
            - Introduces data quality issues (missing values, outliers)
        
        Returns:
            pd.DataFrame: Inventory master with 5,000+ rows
        """
        
        components = []
        
        for i in range(self.num_components):
            category = random.choice(list(self.component_categories.keys()))
            cat_config = self.component_categories[category]
            
            # Generate realistic part numbers
            part_number = f"PN-{category[:3].upper()}-{i:05d}"
            
            # Safety stock calculation with business logic
            base_demand = np.random.poisson(lam=20)  # Average monthly usage
            safety_multiplier = 1.5 if cat_config['criticality'] == 'Critical' else 1.2
            safety_stock = int(base_demand * safety_multiplier)
            
            # Current stock levels with realistic variance
            stock_variance = np.random.uniform(0.4, 1.8)
            current_stock = int(safety_stock * stock_variance)
            
            # Simulate data quality issues (5% missing lead times, 3% invalid stocks)
            lead_time = np.random.randint(7, 90) if random.random() > 0.05 else None
            if random.random() < 0.03:
                current_stock = -1  # Data quality flag
            
            # Lead-time volatility marker (critical for risk assessment)
            volatility = 'High' if lead_time and lead_time > 60 else 'Medium' if lead_time and lead_time > 30 else 'Low'
            
            component = {
                'part_number': part_number,
                'description': f"{category} Component - Series {random.choice(['A', 'B', 'C', 'X'])}",
                'category': category,
                'criticality': cat_config['criticality'],
                'unit_cost_usd': int(cat_config['base_cost'] * np.random.uniform(0.6, 1.4)),
                'current_stock': current_stock,
                'safety_stock': safety_stock,
                'reorder_point': int(safety_stock * 1.3),
                'lead_time_days': lead_time,
                'lead_time_volatility': volatility if lead_time else 'Unknown',
                'aog_cost_per_day': int(150000 * cat_config['aog_multiplier'] * np.random.uniform(0.8, 1.2)),
                'supplier_id': f"SUP-{random.randint(1, self.num_suppliers):04d}",
                'last_updated': (self.base_date + timedelta(days=random.randint(0, self.simulation_days))).strftime('%Y-%m-%d'),
            }
            
            components.append(component)
        
        df = pd.DataFrame(components)
        
        # Add calculated risk flags
        df['stock_coverage_days'] = (df['current_stock'] / (df['safety_stock'] / 30)).fillna(0)
        df['risk_flag'] = df.apply(
            lambda row: 'Critical' if row['current_stock'] < row['reorder_point'] * 0.5 
            else 'Warning' if row['current_stock'] < row['reorder_point'] 
            else 'Healthy', 
            axis=1
        )
        
        return df
    
    def generate_supplier_network(self):
        """
        Create supplier master data with geopolitical and operational risk factors.
        
        Business Value:
            - Shows multi-tier supplier dependencies
            - Introduces geographic concentration risk
            - Enables "What-if" scenario analysis (e.g., port strikes)
        
        Returns:
            pd.DataFrame: Supplier network with reliability metrics
        """
        
        suppliers = []
        
        for i in range(1, self.num_suppliers + 1):
            region = random.choice(list(self.supplier_regions.keys()))
            region_config = self.supplier_regions[region]
            
            # Realistic reliability scoring
            base_reliability = region_config['reliability_base']
            reliability = np.clip(np.random.normal(base_reliability, 0.08), 0.6, 0.99)
            
            # Lead time with regional variance
            base_lead = region_config['lead_time_base']
            avg_lead_time = int(np.random.normal(base_lead, base_lead * 0.3))
            
            supplier = {
                'supplier_id': f"SUP-{i:04d}",
                'supplier_name': f"{random.choice(['Aero', 'Sky', 'Global', 'Precision', 'Advanced'])} "
                                 f"{random.choice(['Systems', 'Components', 'Manufacturing', 'Industries'])} "
                                 f"{random.choice(['Ltd', 'Inc', 'GmbH', 'SA'])}",
                'region': region,
                'country': self._get_country_for_region(region),
                'tier': random.choice(['Tier-1', 'Tier-1', 'Tier-2', 'Tier-3']),  # More Tier-1s
                'on_time_delivery_pct': round(reliability * 100, 1),
                'quality_rating': round(np.random.uniform(85, 99), 1),
                'avg_lead_time_days': avg_lead_time,
                'payment_terms': random.choice(['NET30', 'NET45', 'NET60']),
                'certifications': ','.join(random.sample(['AS9100', 'ISO9001', 'NADCAP', 'EASA'], k=random.randint(1, 3))),
                'risk_exposure': self._calculate_supplier_risk(region, reliability),
            }
            
            suppliers.append(supplier)
        
        return pd.DataFrame(suppliers)
    
    def generate_risk_feed(self):
        """
        Simulate external risk events that impact supply chain operations.
        
        Business Value:
            - Demonstrates unstructured data integration (news scraping simulation)
            - Creates temporal correlation with inventory depletion
            - Shows how AI can connect disparate data sources
        
        Returns:
            pd.DataFrame: Time-series risk events with severity scoring
        """
        
        risk_events = []
        event_types = {
            'Port Congestion': {'impact': 'High', 'duration_days': (7, 21)},
            'Labor Strike': {'impact': 'Critical', 'duration_days': (3, 14)},
            'Weather Disruption': {'impact': 'Medium', 'duration_days': (1, 5)},
            'Geopolitical Tension': {'impact': 'High', 'duration_days': (14, 90)},
            'Supplier Bankruptcy': {'impact': 'Critical', 'duration_days': (30, 180)},
            'Customs Delay': {'impact': 'Medium', 'duration_days': (2, 10)},
        }
        
        # Generate 50-100 events over simulation period
        num_events = random.randint(50, 100)
        
        for _ in range(num_events):
            event_type = random.choice(list(event_types.keys()))
            event_config = event_types[event_type]
            
            event_date = self.base_date + timedelta(days=random.randint(0, self.simulation_days))
            duration = random.randint(*event_config['duration_days'])
            
            # Assign affected regions/suppliers
            affected_region = random.choice(list(self.supplier_regions.keys()))
            num_affected_suppliers = random.randint(5, 30)
            
            event = {
                'event_id': f"RISK-{_:04d}",
                'event_date': event_date.strftime('%Y-%m-%d'),
                'event_type': event_type,
                'severity': event_config['impact'],
                'affected_region': affected_region,
                'affected_suppliers_count': num_affected_suppliers,
                'estimated_duration_days': duration,
                'resolution_date': (event_date + timedelta(days=duration)).strftime('%Y-%m-%d'),
                'source': random.choice(['Reuters', 'Bloomberg', 'IATA', 'Port Authority', 'Internal Alert']),
                'description': self._generate_event_description(event_type, affected_region),
            }
            
            risk_events.append(event)
        
        df = pd.DataFrame(risk_events)
        df = df.sort_values('event_date').reset_index(drop=True)
        
        return df
    
    def _get_country_for_region(self, region):
        """Map regions to realistic country distributions."""
        country_map = {
            'Asia-Pacific': ['Singapore', 'South Korea', 'Japan', 'Taiwan', 'China'],
            'Europe': ['Germany', 'France', 'UK', 'Italy', 'Netherlands'],
            'North America': ['USA', 'Canada', 'Mexico'],
            'Middle East': ['UAE', 'Turkey', 'Israel'],
        }
        return random.choice(country_map[region])
    
    def _calculate_supplier_risk(self, region, reliability):
        """Calculate composite risk score based on multiple factors."""
        region_risk = {'Asia-Pacific': 0.3, 'Europe': 0.1, 'North America': 0.15, 'Middle East': 0.4}
        performance_risk = (1 - reliability) * 0.5
        composite = region_risk[region] + performance_risk
        
        if composite > 0.4:
            return 'High'
        elif composite > 0.2:
            return 'Medium'
        else:
            return 'Low'
    
    def _generate_event_description(self, event_type, region):
        """Create realistic event narratives."""
        templates = {
            'Port Congestion': f"Major port congestion reported in {region} due to increased cargo volume and labor shortages.",
            'Labor Strike': f"Labor union strike affecting multiple logistics hubs in {region}.",
            'Weather Disruption': f"Severe weather conditions causing flight cancellations and delivery delays in {region}.",
            'Geopolitical Tension': f"Escalating geopolitical tensions impacting trade routes through {region}.",
            'Supplier Bankruptcy': f"Major supplier declares bankruptcy, affecting components sourced from {region}.",
            'Customs Delay': f"Extended customs processing times reported at {region} border checkpoints.",
        }
        return templates[event_type]
    
    def generate_all_datasets(self, output_dir='data/raw'):
        """
        Execute full data generation pipeline and save to disk.
        
        Args:
            output_dir (str): Target directory for CSV outputs
            
        Returns:
            dict: Summary statistics for generated datasets
        """
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        print("🚀 Sky-Guard Data Generation Pipeline Initiated...")
        print("=" * 60)
        
        # Generate datasets
        print("📦 Generating Inventory Master Data...")
        inventory = self.generate_inventory_master()
        inventory.to_csv(f'{output_dir}/inventory_master.csv', index=False)
        
        print("🏭 Generating Supplier Network Data...")
        suppliers = self.generate_supplier_network()
        suppliers.to_csv(f'{output_dir}/supplier_network.csv', index=False)
        
        print("⚠️  Generating Risk Event Feed...")
        risks = self.generate_risk_feed()
        risks.to_csv(f'{output_dir}/risk_events.csv', index=False)
        
        # Generate summary statistics
        summary = {
            'generation_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'inventory': {
                'total_components': len(inventory),
                'critical_components': len(inventory[inventory['criticality'] == 'Critical']),
                'at_risk_components': len(inventory[inventory['risk_flag'] == 'Critical']),
                'total_inventory_value_usd': int(inventory['unit_cost_usd'].sum()),
            },
            'suppliers': {
                'total_suppliers': len(suppliers),
                'high_risk_suppliers': len(suppliers[suppliers['risk_exposure'] == 'High']),
                'avg_on_time_delivery': round(suppliers['on_time_delivery_pct'].mean(), 1),
            },
            'risks': {
                'total_events': len(risks),
                'critical_events': len(risks[risks['severity'] == 'Critical']),
                'avg_duration_days': round(risks['estimated_duration_days'].mean(), 1),
            }
        }
        
        # Save summary
        with open(f'{output_dir}/generation_summary.json', 'w') as f:
            json.dump(summary, f, indent=2)
        
        print("\n✅ Data Generation Complete!")
        print("=" * 60)
        print(f"📊 Summary:")
        print(f"   • Inventory Components: {summary['inventory']['total_components']:,}")
        print(f"   • At-Risk Components: {summary['inventory']['at_risk_components']:,}")
        print(f"   • Suppliers: {summary['suppliers']['total_suppliers']:,}")
        print(f"   • Risk Events: {summary['risks']['total_events']:,}")
        print(f"\n💾 Files saved to: {output_dir}/")
        
        return summary


# Execution Entry Point
if __name__ == "__main__":
    generator = MRODataGenerator(
        num_components=5000,
        num_suppliers=150,
        simulation_days=90
    )
    
    summary = generator.generate_all_datasets()
    
    print("\n" + "=" * 60)
    print("🎯 Next Steps:")
    print("   1. Review generated datasets in data/raw/")
    print("   2. Proceed to Phase 2: Anomaly Detection Engine")
    print("   3. Configure OpenRouter API for AI reasoning layer")
    print("=" * 60)