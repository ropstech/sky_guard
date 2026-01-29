"""
Sky-Guard Pipeline Runner
==========================
Executes all 5 pipeline steps in the correct order.

Usage:
    uv run python src/pipeline/run_pipeline.py
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from config.logging_config import get_logger
from src.data_generation.generate_data import main as generate_main
from src.data_generation.validate_data import main as validate_main
from src.analytics.detect_anomalies import main as detect_main
from src.ai_reasoning.ai_reasoning_engine import main as ai_main
from src.analytics.roi_calculator import main as roi_main

logger = get_logger(__name__)


def main():
    """Execute all 5 pipeline steps."""
    
    logger.info("=" * 70)
    logger.info("Sky-Guard Pipeline - Starting")
    logger.info("=" * 70)
    
    # Step 1: Generate Data
    logger.info("\nStep 1/5: Generating data...")
    generate_main()
    
    # Step 2: Validate Data
    logger.info("\nStep 2/5: Validating data...")
    if not validate_main():
        logger.error("Validation failed - stopping pipeline")
        sys.exit(1)
    
    # Step 3: Detect Anomalies
    logger.info("\nStep 3/5: Detecting anomalies...")
    detect_main()
    
    # Step 4: AI Reasoning
    logger.info("\nStep 4/5: Generating AI recommendations...")
    try:
        ai_main()
    except ValueError as e:
        logger.warning(f"AI step skipped: {e}")
        logger.warning("Set OPENROUTER_API_KEY in .env to enable AI recommendations")
    
    # Step 5: Calculate ROI
    logger.info("\nStep 5/5: Calculating ROI...")
    roi_main()
    
    logger.info("\n" + "=" * 70)
    logger.info("Pipeline Complete!")
    logger.info("=" * 70)
    logger.info("\nNext: Launch dashboard with:")
    logger.info("  streamlit run src/dashboard/dashboard_app.py")


if __name__ == "__main__":
    main()