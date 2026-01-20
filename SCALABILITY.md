# From PoC to Enterprise Production

## Architectural Transition
To deploy Sky-Guard in a Tier-1 Organization (e.g., Lufthansa Technik, Airbus), we transition from a local PoC to a **Cloud-Native Data Mesh Architecture**.

| Phase | PoC (Current) | Enterprise Production (Target) |
| :--- | :--- | :--- |
| **Orchestration** | GitHub Actions | **Google Cloud Composer (Managed Airflow)** |
| **Data Warehouse** | Parquet / DuckDB | **Google BigQuery** (Serverless Data Warehouse) |
| **AI Layer** | OpenRouter (Public) | **Vertex AI** (Private LLM Instances / Finetuned Models) |
| **Computing** | Streamlit Cloud | **Google Cloud Run** (Auto-scaling Containerized UI) |
| **Security** | Manual Keys | **GCP Secret Manager** & IAM Role-based access |

## Strategic Roadmap
1. **Pilot Phase:** Integration of one specific MRO Hub (e.g., Hamburg Base).
2. **Scaling:** Connecting global ERP instances via Pub/Sub messaging.
3. **Advanced Features:** Integration of Digital Twins to simulate "What-if" supply chain scenarios.