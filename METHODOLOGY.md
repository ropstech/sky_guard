# Business Case & Methodology

## Financial Impact Logic
The primary KPI for Sky-Guard is the reduction of **Unplanned Maintenance Downtime**. 

$$ROI = \frac{(AOG\_Events\_Prevented \times Cost\_per\_AOG) - System\_OPEX}{Investment}$$

### 1. Ingestion Phase
We simulate a complex MRO environment with synthetic datasets:
* **Inventory Master Data:** 5,000+ SKUs with lead-time volatility markers.
* **Risk Feed:** Real-time scraping of logistical news and port congestions.

### 2. The AI-Advisory Logic
Unlike standard BI tools, Sky-Guard doesn't just show a red chart. The AI layer acts as a **Virtual Senior Consultant**:
* **Analysis:** "Component #8821 (Turbine Blade) is below safety stock."
* **Context:** "Current strike in Singapore Port affects 80% of Asia-Europe sea freight."
* **Recommendation:** "Trigger emergency air-freight for 20 units; cost increase $5k vs. potential AOG loss of $150k. Net Benefit: $145k."

## Lessons Learned
Through this PoC, we demonstrate that **Automated Reasoning** is the next step after Data Visualization. Traditional Dashboards tell you *what* happened; Sky-Guard tells you *what to do*.