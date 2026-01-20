# Project Sky-Guard: AI-Driven Operational Resilience in Aviation MRO
> **Minimizing AOG (Aircraft on Ground) Costs through Automated Supply Chain Intelligence.**

## 1. Executive Summary
In high-stakes industries like Aviation and Defense, a single missing component can lead to **Aircraft on Ground (AOG)** events costing up to **$150,000 per day**. Project Sky-Guard is a Technical Proof of Concept (PoC) designed to bridge the gap between fragmented ERP data and real-time global risk factors. 

By leveraging **Python-based automation** and **LLM-driven reasoning**, Sky-Guard identifies supply chain anomalies before they escalate, providing C-level executives with actionable strategic recommendations to protect EBITDA and operational integrity.

## 2. The Problem
* **Data Silos:** Critical inventory data is often trapped in legacy ERP systems without external risk context.
* **Delayed Reaction:** Manual monitoring of geopolitical or logistical shocks (e.g., port strikes, weather) is too slow for modern MRO requirements.
* **Information Overload:** Procurement teams are flooded with alerts but lack prioritized, financial-impact-based action plans.

## 3. The Solution (PoC Scope)
Sky-Guard orchestrates a 4-stage pipeline:
1. **Data Ingestion:** Merging internal inventory levels with external risk signals.
2. **Anomaly Detection:** Identifying "At-Risk" components using statistical outlier detection.
3. **AI Reasoning:** Using LLMs (via OpenRouter) to evaluate unstructured data and generate strategic mitigation plans.
4. **Insight Delivery:** High-fidelity Streamlit dashboard for real-time Executive decision-making.

## 4. Technical Stack
* **Language:** Python 3.11+
* **Intelligence:** OpenRouter API (DeepSeek-V3 / Llama 3)
* **Framework:** Streamlit (UI), Pandas (Data Engineering)
* **Automation:** GitHub Actions (PoC Orchestration)