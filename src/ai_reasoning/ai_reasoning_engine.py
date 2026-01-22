"""
Sky-Guard: AI Reasoning Engine
================================

Business Purpose:
    Transform technical risk data into executive-level strategic recommendations.
    
    Think of this as a "Virtual Senior Supply Chain Consultant" that:
    - Analyzes risk patterns
    - Considers external factors (port strikes, weather)
    - Generates specific action plans with ROI calculations
    
Technical Approach:
    Uses OpenRouter API (LLM) to:
    1. Interpret structured risk data
    2. Incorporate unstructured context (risk events)
    3. Generate human-readable recommendations
    
Output:
    For each high-risk component:
    - Root cause analysis
    - 2-3 mitigation options
    - Cost-benefit analysis
    - Recommended action with confidence score
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional
import requests
from dotenv import load_dotenv

from config.logging_config import get_logger

logger = get_logger(__name__)

# Load environment variables
load_dotenv()


class AIReasoningEngine:
    """
    Generates strategic recommendations using LLM reasoning.
    """
    
    def __init__(self, data_dir='data/processed'):
        self.data_dir = Path(data_dir)
        
        # Load API credentials
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        self.model = os.getenv('OPENROUTER_MODEL')
        
        if not self.api_key:
            raise ValueError(
                "OPENROUTER_API_KEY not found in environment. "
                "Please set it in your .env file."
            )
        
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        
        logger.info("AI Reasoning Engine initialized")
        logger.info(f"Model: {self.model}")
    
    def load_risk_data(self):
        """Load risk analysis results from Step 1."""
        logger.info("Loading risk analysis data...")
        
        risk_file = self.data_dir / 'risk_analysis.json'
        
        if not risk_file.exists():
            raise FileNotFoundError(
                f"Risk analysis not found: {risk_file}\n"
                "Please run detect_anomalies.py first."
            )
        
        with open(risk_file, 'r') as f:
            self.risk_data = json.load(f)
        
        logger.info(f"  ✓ Loaded {len(self.risk_data['top_risks'])} high-risk components")
    
    def build_prompt(self, component: Dict, context: Optional[Dict] = None) -> str:
        """
        Build structured prompt for LLM analysis.
        
        Prompt Engineering Best Practices:
        - Clear role definition
        - Structured output format
        - Specific constraints (cost limits, timelines)
        - Request for reasoning chain
        """
        
        prompt = f"""You are a Senior Supply Chain Consultant for an Aviation MRO organization.

COMPONENT ANALYSIS REQUEST:

Component Details:
- Part Number: {component['part_number']}
- Description: {component['description']}
- Category: {component['category']}
- Criticality: {component['criticality']}

Current Situation:
- Current Stock: {component['current_stock']} units
- Safety Stock: {component['safety_stock']} units
- Lead Time: {component['lead_time_days']} days
- Supplier Region: {component['region']}
- Supplier Risk: {component['risk_exposure']}

Financial Impact:
- AOG Cost Exposure: ${component['financial_exposure_usd']:,.0f}
- Risk Score: {component['composite_risk_score']:.0f}/100

TASK:
Provide a strategic recommendation to mitigate this risk. Consider:
1. Root cause (why is this component at risk?)
2. Potential mitigation options (emergency orders, alternate suppliers, inventory adjustment)
3. Cost-benefit analysis for each option
4. Your recommended action with confidence level

OUTPUT FORMAT (JSON):
{{
  "root_cause": "Brief explanation of why this is at risk",
  "mitigation_options": [
    {{
      "option": "Option name",
      "description": "What to do",
      "estimated_cost_usd": 0,
      "implementation_time_days": 0,
      "risk_reduction_pct": 0
    }}
  ],
  "recommended_action": "Which option to choose and why",
  "confidence_level": "High/Medium/Low",
  "expected_roi": "Cost savings vs. investment"
}}

Respond ONLY with valid JSON, no additional text."""

        return prompt
    
    def call_llm(self, prompt: str) -> Dict:
        """
        Make API call to OpenRouter.
        
        Best Practices:
        - Timeout handling
        - Rate limiting consideration
        - Error logging
        - Response validation
        """
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://sky-guard.example.com",  # Optional: for analytics
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.3,  # Lower = more consistent/conservative recommendations
            "max_tokens": 1000,
        }
        
        try:
            logger.debug("Calling OpenRouter API...")
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            response.raise_for_status()
            
            result = response.json()
            
            # Extract content from response
            content = result['choices'][0]['message']['content']
            
            # Parse JSON from response
            # Remove markdown code blocks if present
            content = content.strip()
            if content.startswith('```json'):
                content = content[7:]  # Remove ```json
            if content.startswith('```'):
                content = content[3:]  # Remove ```
            if content.endswith('```'):
                content = content[:-3]  # Remove trailing ```
            
            recommendation = json.loads(content.strip())
            
            logger.debug("  ✓ API call successful")
            
            return recommendation
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {e}")
            logger.error(f"Raw response: {content}")
            raise
    
    def generate_recommendations(self, max_components: int = 5):
        """
        Generate recommendations for top N high-risk components.
        
        Note: Limited to avoid excessive API costs during PoC phase.
        In production, this would process all high-risk items.
        """
        
        logger.info("=" * 70)
        logger.info(f"Generating AI Recommendations for Top {max_components} Risks")
        logger.info("=" * 70)
        
        recommendations = []
        
        top_risks = self.risk_data['top_risks'][:max_components]
        
        for idx, component in enumerate(top_risks, 1):
            logger.info(f"\n[{idx}/{len(top_risks)}] Analyzing: {component['part_number']}")
            
            try:
                # Build prompt
                prompt = self.build_prompt(component)
                
                # Get LLM recommendation
                recommendation = self.call_llm(prompt)
                
                # Enrich with component metadata
                full_recommendation = {
                    'component': {
                        'part_number': component['part_number'],
                        'description': component['description'],
                        'category': component['category'],
                        'financial_exposure_usd': component['financial_exposure_usd'],
                    },
                    'ai_analysis': recommendation
                }
                
                recommendations.append(full_recommendation)
                
                logger.info(f"  ✓ Recommendation generated")
                logger.info(f"    Action: {recommendation['recommended_action'][:60]}...")
                
            except Exception as e:
                logger.error(f"  ✗ Failed to generate recommendation: {e}")
                continue
        
        logger.info("\n" + "=" * 70)
        logger.info(f"Generated {len(recommendations)} recommendations")
        logger.info("=" * 70)
        
        return recommendations
    
    def save_recommendations(self, recommendations: List[Dict]):
        """
        Save AI-generated recommendations to file.
        """
        logger.info("Saving recommendations...")
        
        output = {
            'metadata': {
                'model_used': self.model,
                'total_recommendations': len(recommendations),
                'risk_summary': self.risk_data['summary']
            },
            'recommendations': recommendations
        }
        
        output_file = self.data_dir / 'ai_recommendations.json'
        
        with open(output_file, 'w') as f:
            json.dump(output, f, indent=2)
        
        logger.info(f"  ✓ Recommendations saved to: {output_file}")
    
    def print_executive_summary(self, recommendations: List[Dict]):
        """
        Print executive summary of recommendations.
        """
        logger.info("\n" + "=" * 70)
        logger.info("EXECUTIVE SUMMARY - AI RECOMMENDATIONS")
        logger.info("=" * 70)
        
        total_exposure = sum(
            r['component']['financial_exposure_usd'] 
            for r in recommendations
        )
        
        logger.info(f"\nTotal Financial Exposure Analyzed: ${total_exposure:,.0f}")
        logger.info(f"Components Reviewed: {len(recommendations)}")
        
        logger.info("\nTop Recommended Actions:")
        for idx, rec in enumerate(recommendations[:3], 1):
            comp = rec['component']
            ai = rec['ai_analysis']
            logger.info(
                f"\n{idx}. {comp['part_number']} - {comp['category']}"
            )
            logger.info(f"   Exposure: ${comp['financial_exposure_usd']:,.0f}")
            logger.info(f"   Action: {ai['recommended_action'][:80]}...")
            logger.info(f"   Confidence: {ai['confidence_level']}")
        
        logger.info("\n" + "=" * 70)
    
    def run_analysis(self, max_components: int = 5):
        """
        Execute complete AI reasoning pipeline.
        """
        logger.info("=" * 70)
        logger.info("Sky-Guard AI Reasoning Engine - STARTED")
        logger.info("=" * 70)
        
        self.load_risk_data()
        recommendations = self.generate_recommendations(max_components)
        self.save_recommendations(recommendations)
        self.print_executive_summary(recommendations)
        
        logger.info("\n" + "=" * 70)
        logger.info("AI Reasoning Complete")
        logger.info("=" * 70)
        
        return recommendations


def main():
    """Entry point for AI reasoning."""
    try:
        engine = AIReasoningEngine()
        engine.run_analysis(max_components=5)  # Limit to 5 for cost control
    except ValueError as e:
        logger.error(str(e))
        logger.error("\nSetup Instructions:")
        logger.error("1. Get API key from: https://openrouter.ai/keys")
        logger.error("2. Add to .env file: OPENROUTER_API_KEY=your_key_here")
        return 1
    except FileNotFoundError as e:
        logger.error(str(e))
        return 1
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())