# Sky-Guard Technical Guide

> **Complete setup instructions, architecture documentation, and troubleshooting guide for developers and consultants.**

---

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Running the Pipeline](#running-the-pipeline)
5. [Dashboard Usage](#dashboard-usage)
6. [Architecture Deep Dive](#architecture-deep-dive)
7. [API Reference](#api-reference)
8. [Troubleshooting](#troubleshooting)
9. [Production Deployment](#production-deployment)

---

## System Requirements

### Minimum Specifications
- **OS:** macOS 11+, Ubuntu 20.04+, Windows 10+ (WSL2 recommended)
- **Python:** 3.11 or higher
- **Network:** Internet connection for API calls

### Recommended Tools
- **Terminal:** iTerm2 (Mac), Windows Terminal, or VS Code integrated terminal
- **IDE:** VS Code, PyCharm, or Cursor
- **Package Manager:** [uv](https://github.com/astral-sh/uv) 

---

## Installation

### Step 1: Clone Repository

```bash
git clone https://github.com/ropstech/sky_guard.git
cd sky_guard
```

### Step 2: Install uv (if not already installed)

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

**Alternative (pip):**
```bash
pip install uv
```

### Step 3: Install Dependencies

```bash
# Create virtual environment and install all dependencies
uv sync
```

This command:
- Creates a `.venv/` directory
- Installs all packages from `pyproject.toml`
- Sets up the project as an editable package

### Step 4: Verify Installation

```bash
# Activate virtual environment (if not auto-activated)
source .venv/bin/activate  # macOS/Linux
# OR
.venv\Scripts\activate     # Windows

# Check Python version
python --version  # Should show 3.11+

# Verify packages
uv pip list
```

---

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```bash
# Logging Configuration
SKYGUARD_LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL

# OpenRouter API Configuration
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxx  # Get from https://openrouter.ai/keys
OPENROUTER_MODEL=xiaomi/mimo-v2-flash:free  # Or: anthropic/claude-4-sonnet

# Optional: Data Paths
SKYGUARD_DATA_DIR=data/raw
SKYGUARD_OUTPUT_DIR=data/processed
```

### Get OpenRouter API Key

1. Visit [openrouter.ai](https://openrouter.ai)
2. Sign up (free tier available)
3. Navigate to [API Keys](https://openrouter.ai/keys)
4. Create new key
5. Use the current Top Tier Free Models or add $5-10 credits (sufficient for PoC testing)


---

## Running the Pipeline

### Full Pipeline Execution

Run all stages in sequence:

```bash
# 1. Generate synthetic MRO data (5,000 components, 150 suppliers)
uv run python src/data_generation/generate_data.py

# 2. Validate data quality against business rules
uv run python src/data_generation/validate_data.py

# 3. Detect anomalies and calculate risk scores
uv run python src/analytics/detect_anomalies.py

# 4. Generate AI-powered recommendations (requires API key)
uv run python src/ai_reasoning/ai_reasoning_engine.py

# 5. Calculate ROI metrics
uv run python src/analytics/roi_calculator.py

# 6. Launch interactive dashboard
uv run streamlit run src/dashboard/dashboard_app.py
```

### Expected Outputs

After each step, check these locations:

| Step | Output Location | Description |
|------|----------------|-------------|
| 1 | `data/raw/inventory_master.csv` | 5,000 component records |
| 1 | `data/raw/supplier_network.csv` | 150 supplier profiles |
| 1 | `data/raw/risk_events.csv` | 50-100 external risk events |
| 2 | `data/raw/validation_report.json` | Data quality results |
| 3 | `data/processed/risk_analysis.json` | Top 20 critical risks |
| 3 | `data/processed/enriched_inventory_with_risks.csv` | Full risk dataset |
| 4 | `data/processed/ai_recommendations.json` | LLM-generated strategies |
| 5 | `data/processed/roi_analysis.json` | Financial metrics |

### Individual Module Execution

Run specific modules independently:

```bash
# Only generate data (useful for testing with different parameters)
uv run python src/data_generation/generate_data.py

# Only run anomaly detection (requires existing data)
uv run python src/analytics/detect_anomalies.py

# Only calculate ROI (requires risk analysis + recommendations)
uv run python src/analytics/roi_calculator.py
```

---

## Dashboard Usage

### Starting the Dashboard

```bash
uv run streamlit run src/dashboard/dashboard_app.py
```

**Access:** Browser automatically opens at `http://localhost:8501`


### Dashboard Shortcuts

```bash
# Stop dashboard
Ctrl + C

# Run on different port
streamlit run src/dashboard/dashboard_app.py --server.port 8502

# Run without browser auto-open
streamlit run src/dashboard/dashboard_app.py --server.headless true
```

---

## Architecture Deep Dive

### Data Flow

```
┌─────────────────┐
│ Data Generation │
│  (Synthetic)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Validation    │
│ (Business Rules)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────┐
│Anomaly Detection│◄─────┤Supplier Data │
│  (Multi-Factor) │      └──────────────┘
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────┐
│  AI Reasoning   │◄─────┤OpenRouter API│
│  (LLM-Powered)  │      └──────────────┘
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ ROI Calculator  │
│  (Financial)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Dashboard    │
│   (Streamlit)   │
└─────────────────┘
```

### Module Breakdown

#### **analytics/detect_anomalies.py**
- **Purpose:** Multi-factor risk scoring
- **Inputs:** Inventory CSV, Supplier CSV
- **Outputs:** Risk analysis JSON, enriched inventory CSV
- **Algorithm:**
  ```python
  composite_risk = (inventory_risk * supplier_multiplier)
  financial_exposure = aog_cost_per_day * estimated_outage_days
  ```

#### **ai_reasoning/ai_reasoning_engine.py**
- **Purpose:** Generate strategic recommendations
- **Inputs:** Risk analysis JSON
- **Outputs:** AI recommendations JSON
- **Key Features:**
  - Robust JSON parsing (3 fallback strategies)
  - Graceful error handling
  - Cost-benefit analysis

#### **analytics/roi_calculator.py**
- **Purpose:** Quantify financial impact
- **Inputs:** Risk analysis + AI recommendations
- **Outputs:** ROI analysis JSON
- **Formula:**
  ```
  ROI = (AOG_Costs_Avoided - System_Investment) / System_Investment
  ```

---

## API Reference

### OpenRouter Integration

**Endpoint:** `https://openrouter.ai/api/v1/chat/completions`

**Request Format:**
```python
{
    "model": "xiaomi/mimo-v2-flash:free",
    "messages": [
        {"role": "user", "content": "Your prompt here"}
    ],
    "temperature": 0.3,
    "max_tokens": 1500
}
```

**Headers:**
```python
{
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}
```

**Supported Models:**
- `xiaomi/mimo-v2-flash:free` - Currently Free and enough for Demo
- `anthropic/claude-4-sonnet` - High quality
- `meta-llama/llama-3-70b` - Open-source alternative

### Error Handling

**Scenario 1: LLM returns malformed JSON**
- **Solution:** 3-tier fallback parsing
  1. Direct parse
  2. Remove markdown blocks
  3. Fix unquoted keys with regex

**Scenario 2: API rate limit**
- **Solution:** Reduce `max_components` parameter
- **Alternative:** Switch to cheaper model

---

## Troubleshooting

### Common Issues

#### **Issue: `ModuleNotFoundError: No module named 'config'`**

**Cause:** Package not installed in editable mode

**Solution:**
```bash
pip install -e .
```

---

#### **Issue: `OPENROUTER_API_KEY not found`**

**Cause:** Missing or incorrectly named `.env` file

**Solution:**
```bash
# Check if .env exists
ls -la .env

# If not, copy template
cp .env.example .env

# Edit and add your key
nano .env  # or open in VS Code
```

---

#### **Issue: `FileNotFoundError: risk_analysis.json`**

**Cause:** Pipeline steps run out of order

**Solution:** Run steps 1-3 before step 4:
```bash
uv run python src/data_generation/generate_data.py
uv run python src/analytics/detect_anomalies.py
uv run python src/ai_reasoning/ai_reasoning_engine.py
```

---

#### **Issue: Dashboard shows "Missing required data files"**

**Cause:** Not all pipeline steps completed

**Solution:** Verify all files exist:
```bash
ls -lh data/processed/
# Should show:
# - risk_analysis.json
# - ai_recommendations.json
# - roi_analysis.json
# - enriched_inventory_with_risks.csv
```

---

#### **Issue: ROI shows unrealistic values (e.g., 3000:1)**

**Cause:** Synthetic data needs calibration

**Solution:** Regenerate data (already calibrated in current version):
```bash
uv run python src/data_generation/generate_data.py
```

---

### Logs & Debugging

**Log Location:** `logs/skyguard_YYYYMMDD_HHMMSS.log`

**Viewing logs:**
```bash
# View latest log
tail -f logs/skyguard_*.log

# Search for errors
grep -i error logs/skyguard_*.log
```

**Increase log verbosity:**
```bash
# In .env
SKYGUARD_LOG_LEVEL=DEBUG
```

---

## Production Deployment

### Scalability Considerations

For enterprise deployment, see **[SCALABILITY.md](SCALABILITY.md)**.

**Key Changes:**
- Replace synthetic data with ERP connectors (SAP, Oracle)
- Deploy Streamlit on Cloud Run / AWS ECS
- Use Vertex AI for private LLM instances
- Implement proper secret management (GCP Secret Manager)
- Add authentication/authorization (OAuth2)

### Performance Benchmarks

**Current PoC:**
- Data generation: ~5 seconds
- Anomaly detection: ~2 seconds
- AI recommendations (5 components): ~15 seconds
- Dashboard load: <1 second

**Expected Production:**
- Real-time data sync: <10 seconds
- Risk analysis (50K components): ~30 seconds
- Dashboard response: <500ms

---

## Additional Resources

**Internal Documentation:**
- [METHODOLOGY.md](METHODOLOGY.md) - Business logic & ROI formula
- [SCALABILITY.md](SCALABILITY.md) - Enterprise architecture

**External Links:**
- [Streamlit Docs](https://docs.streamlit.io)
- [OpenRouter API Docs](https://openrouter.ai/docs)
- [Plotly Python Docs](https://plotly.com/python/)

---

## Support

For technical questions or issues:

1. Check this guide first
2. Review logs in `logs/` directory
3. Search [GitHub Issues](https://github.com/ropstech/sky_guard/issues)

---

<div align="center">
  <strong>Sky-Guard Technical Guide v1.0</strong> • 2026
</div>