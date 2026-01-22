"""
Sky-Guard: ROI Calculator
==========================

Business Purpose:
    Translate technical risk mitigation into CFO-language: dollars saved.
    
    Quantifies:
    - AOG costs avoided through proactive intervention
    - Investment required (system OPEX + mitigation actions)
    - Net benefit and ROI ratio
    
    Critical for executive buy-in: "Is this worth the investment?"
    
Output:
    Executive-ready financial summary demonstrating business case for Sky-Guard.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List

from config.logging_config import get_logger

logger = get_logger(__name__)


class ROICalculator:
    """
    Calculates financial return on investment for Sky-Guard system.
    """
    
    def __init__(self, data_dir='data/processed'):
        self.data_dir = Path(data_dir)
        
        # System operational costs (annual estimates for PoC)
        self.system_costs = {
            'platform_licenses': 80000,   # Cloud infrastructure, API costs
            'personnel_training': 50000,  # One-time training
            'ongoing_maintenance': 40000, # Annual maintenance
        }
        
        logger.info("ROI Calculator initialized")
    
    def load_data(self):
        """Load risk analysis and AI recommendations."""
        logger.info("Loading analysis data...")
        
        # Load risk analysis
        risk_file = self.data_dir / 'risk_analysis.json'
        with open(risk_file, 'r') as f:
            self.risk_data = json.load(f)
        
        # Load AI recommendations
        rec_file = self.data_dir / 'ai_recommendations.json'
        with open(rec_file, 'r') as f:
            self.recommendations = json.load(f)
        
        logger.info(f"  ✓ Loaded risk data and {len(self.recommendations['recommendations'])} recommendations")
    
    def calculate_total_system_investment(self) -> Dict:
        """
        Calculate total cost of implementing and operating Sky-Guard.
        
        Components:
        - Initial setup (one-time)
        - Annual operating costs
        - Mitigation action costs (from AI recommendations)
        """
        
        logger.info("Calculating system investment costs...")
        
        # One-time costs
        one_time_costs = self.system_costs['personnel_training']
        
        # Annual recurring costs
        annual_costs = (
            self.system_costs['platform_licenses'] +
            self.system_costs['ongoing_maintenance']
        )
        
        # Extract mitigation costs from AI recommendations
        mitigation_costs = []
        for rec in self.recommendations['recommendations']:
            ai_analysis = rec['ai_analysis']
            
            # Get cost of recommended action
            # Parse from mitigation options
            if 'mitigation_options' in ai_analysis and ai_analysis['mitigation_options']:
                # Find the recommended option (usually first or lowest cost for immediate action)
                recommended_option = ai_analysis['mitigation_options'][0]
                mitigation_costs.append(recommended_option.get('estimated_cost_usd', 0))
        
        total_mitigation_costs = sum(mitigation_costs)
        
        investment_breakdown = {
            'one_time_setup': one_time_costs,
            'annual_operating_costs': annual_costs,
            'mitigation_action_costs': total_mitigation_costs,
            'total_first_year_investment': one_time_costs + annual_costs + total_mitigation_costs
        }
        
        logger.info(f"  Total First-Year Investment: ${investment_breakdown['total_first_year_investment']:,.0f}")
        
        return investment_breakdown
    
    def calculate_aog_cost_avoidance(self) -> Dict:
        """
        Calculate AOG costs that would have occurred without Sky-Guard intervention.
        
        Methodology:
        - High-risk components have X% probability of causing AOG
        - Without intervention, assume 30% of high-risk items lead to AOG
        - Sky-Guard recommendations reduce this to 5% (conservative estimate)
        """
        
        logger.info("Calculating AOG cost avoidance...")
        
        # Get total financial exposure from risk analysis
        total_exposure = self.risk_data['summary']['financial_metrics']['total_exposure_usd']
        high_risk_count = self.risk_data['summary']['risk_distribution']['high_risk']
        
        # Realistic assumptions based on industry data
        baseline_aog_probability = 0.08  # 8% of high-risk items cause AOG without intervention
        with_skyguard_probability = 0.02  # 2% still slip through despite recommendations
        
        # Calculate expected AOG costs
        baseline_aog_cost = total_exposure * baseline_aog_probability
        with_skyguard_aog_cost = total_exposure * with_skyguard_probability
        
        # Cost avoidance
        aog_costs_avoided = baseline_aog_cost - with_skyguard_aog_cost
        
        avoidance_breakdown = {
            'total_risk_exposure': total_exposure,
            'high_risk_components': high_risk_count,
            'baseline_expected_aog_cost': baseline_aog_cost,
            'with_skyguard_expected_aog_cost': with_skyguard_aog_cost,
            'aog_costs_avoided': aog_costs_avoided,
            'risk_reduction_percentage': ((baseline_aog_probability - with_skyguard_probability) / baseline_aog_probability) * 100
        }
        
        logger.info(f"  AOG Costs Avoided: ${aog_costs_avoided:,.0f}")
        logger.info(f"  Risk Reduction: {avoidance_breakdown['risk_reduction_percentage']:.0f}%")
        
        return avoidance_breakdown
    
    def calculate_roi_metrics(self, investment: Dict, avoidance: Dict) -> Dict:
        """
        Calculate final ROI metrics for executive presentation.
        
        Key Metrics:
        - Net Benefit (savings - investment)
        - ROI Ratio (return / investment)
        - Payback Period (months to break even)
        - NPV (if multi-year projection)
        """
        
        logger.info("Calculating ROI metrics...")
        
        total_investment = investment['total_first_year_investment']
        total_savings = avoidance['aog_costs_avoided']
        
        net_benefit = total_savings - total_investment
        roi_ratio = total_savings / total_investment if total_investment > 0 else 0
        roi_percentage = (net_benefit / total_investment) * 100 if total_investment > 0 else 0
        
        # Payback period (simplified: assumes linear benefit accrual)
        # In reality, AOG avoidance is probabilistic, so this is conservative
        monthly_benefit = total_savings / 12
        payback_months = total_investment / monthly_benefit if monthly_benefit > 0 else float('inf')
        
        roi_metrics = {
            'total_investment_usd': total_investment,
            'total_savings_usd': total_savings,
            'net_benefit_usd': net_benefit,
            'roi_ratio': roi_ratio,
            'roi_percentage': roi_percentage,
            'payback_period_months': payback_months,
            'break_even_date': self._calculate_break_even_date(payback_months)
        }
        
        logger.info(f"  Net Benefit: ${net_benefit:,.0f}")
        logger.info(f"  ROI Ratio: {roi_ratio:.1f}:1")
        logger.info(f"  ROI Percentage: {roi_percentage:.0f}%")
        logger.info(f"  Payback Period: {payback_months:.1f} months")
        
        return roi_metrics
    
    def _calculate_break_even_date(self, months: float) -> str:
        """Calculate approximate break-even date."""
        from datetime import datetime, timedelta
        
        if months == float('inf'):
            return "Never (investment > savings)"
        
        break_even = datetime.now() + timedelta(days=int(months * 30))
        return break_even.strftime('%Y-%m-%d')
    
    def generate_executive_summary(self, investment: Dict, avoidance: Dict, roi: Dict) -> Dict:
        """
        Create executive summary for C-level presentation.
        
        Structure:
        - One-sentence value proposition
        - Key financial metrics
        - Risk mitigation impact
        - Recommendation
        """
        
        summary = {
            'value_proposition': (
                f"Sky-Guard prevents ${avoidance['aog_costs_avoided']:,.0f} in AOG costs "
                f"with ${investment['total_first_year_investment']:,.0f} investment, "
                f"delivering {roi['roi_ratio']:.1f}:1 return."
            ),
            'key_metrics': {
                'investment_required': investment['total_first_year_investment'],
                'aog_costs_avoided': avoidance['aog_costs_avoided'],
                'net_benefit': roi['net_benefit_usd'],
                'roi_ratio': roi['roi_ratio'],
                'payback_period_months': roi['payback_period_months']
            },
            'risk_impact': {
                'high_risk_components_identified': avoidance['high_risk_components'],
                'risk_reduction_percentage': avoidance['risk_reduction_percentage'],
                'total_exposure_managed': avoidance['total_risk_exposure']
            },
            'recommendation': self._generate_recommendation(roi['roi_ratio'])
        }
        
        return summary
    
    def _generate_recommendation(self, roi_ratio: float) -> str:
        """Generate investment recommendation based on ROI."""
        if roi_ratio > 10:
            return "STRONG RECOMMEND: Exceptional ROI justifies immediate implementation."
        elif roi_ratio > 5:
            return "RECOMMEND: High ROI supports business case for deployment."
        elif roi_ratio > 2:
            return "CONSIDER: Positive ROI, evaluate against alternative investments."
        else:
            return "REVIEW: ROI below threshold, reassess assumptions or scope."
    
    def save_results(self, investment: Dict, avoidance: Dict, roi: Dict, summary: Dict):
        """Save ROI analysis results."""
        logger.info("Saving ROI analysis...")
        
        output = {
            'analysis_metadata': {
                'calculation_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'analysis_scope': f"{len(self.recommendations['recommendations'])} components analyzed"
            },
            'investment_breakdown': investment,
            'aog_cost_avoidance': avoidance,
            'roi_metrics': roi,
            'executive_summary': summary
        }
        
        output_file = self.data_dir / 'roi_analysis.json'
        
        with open(output_file, 'w') as f:
            json.dump(output, f, indent=2)
        
        logger.info(f"  ✓ ROI analysis saved to: {output_file}")
    
    def print_executive_report(self, summary: Dict):
        """Print executive summary to console."""
        logger.info("\n" + "=" * 70)
        logger.info("SKY-GUARD ROI ANALYSIS - EXECUTIVE SUMMARY")
        logger.info("=" * 70)
        
        logger.info(f"\n{summary['value_proposition']}")
        
        logger.info("\n" + "-" * 70)
        logger.info("KEY FINANCIAL METRICS")
        logger.info("-" * 70)
        metrics = summary['key_metrics']
        logger.info(f"  Investment Required:    ${metrics['investment_required']:>15,.0f}")
        logger.info(f"  AOG Costs Avoided:      ${metrics['aog_costs_avoided']:>15,.0f}")
        logger.info(f"  Net Benefit:            ${metrics['net_benefit']:>15,.0f}")
        logger.info(f"  ROI Ratio:              {metrics['roi_ratio']:>15.1f}:1")
        logger.info(f"  Payback Period:         {metrics['payback_period_months']:>15.1f} months")
        
        logger.info("\n" + "-" * 70)
        logger.info("RISK MITIGATION IMPACT")
        logger.info("-" * 70)
        impact = summary['risk_impact']
        logger.info(f"  High-Risk Components:   {impact['high_risk_components_identified']:>15,}")
        logger.info(f"  Risk Reduction:         {impact['risk_reduction_percentage']:>14.0f}%")
        logger.info(f"  Total Exposure Managed: ${impact['total_exposure_managed']:>15,.0f}")
        
        logger.info("\n" + "-" * 70)
        logger.info(f"RECOMMENDATION: {summary['recommendation']}")
        logger.info("-" * 70)
        
        logger.info("\n" + "=" * 70)
    
    def run_analysis(self):
        """Execute complete ROI analysis."""
        logger.info("=" * 70)
        logger.info("Sky-Guard ROI Calculator - STARTED")
        logger.info("=" * 70)
        
        self.load_data()
        investment = self.calculate_total_system_investment()
        avoidance = self.calculate_aog_cost_avoidance()
        roi = self.calculate_roi_metrics(investment, avoidance)
        summary = self.generate_executive_summary(investment, avoidance, roi)
        
        self.save_results(investment, avoidance, roi, summary)
        self.print_executive_report(summary)
        
        logger.info("\n" + "=" * 70)
        logger.info("ROI Analysis Complete")
        logger.info("=" * 70)
        
        return summary


def main():
    """Entry point for ROI calculation."""
    try:
        calculator = ROICalculator()
        calculator.run_analysis()
    except FileNotFoundError as e:
        logger.error(f"Required data not found: {e}")
        logger.error("Please run detect_anomalies.py and ai_reasoning_engine.py first.")
        return 1
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())