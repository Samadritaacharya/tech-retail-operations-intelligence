# Tech Retail Operations Intelligence Dashboard

**An e-commerce operations intelligence dashboard** for order and fulfillment analytics, support trends, return/refund insights, inventory risk scoring, campaign impact analysis and an automatically generated PMO action plan.

> 🔗 **Live demo:** _add your Streamlit Cloud link here after deployment_

---

## Business problem

Digital retail teams see many operational signals every day: failed checkouts, late deliveries, return spikes, support tickets, inventory risk and campaign side-effects. The challenge is converting these signals into a prioritized action plan with owners, deadlines and business impact.

## Solution

This project simulates a European fashion e-commerce operation using synthetic data and turns it into decision-ready intelligence:

- revenue, order, failure, delay, return and support KPIs
- fulfillment analytics by region
- customer support trend analysis
- return and refund insights by category and reason
- inventory days-of-cover risk scoring
- campaign impact analysis
- PMO action plan with problem, business impact, owner, priority and deadline
- Markdown and CSV exports

## Dashboard pages

| # | Page | What it shows |
|---|------|---------------|
| 1 | Retail Operations Overview | KPIs, daily order volume and revenue by region |
| 2 | Order and Fulfillment Analytics | Delivery distribution, late-rate and failure trends |
| 3 | Customer Support Trends | Ticket categories and support heatmap |
| 4 | Return and Refund Insights | Return rate, reasons and refund cost |
| 5 | Inventory Risk | Days-of-cover scoring by category |
| 6 | Campaign Impact | Campaign vs baseline revenue and operational strain |
| 7 | PMO Action Plan | Auto-generated prioritized action plan and exports |

## Tech stack

`Python` · `Streamlit` · `Pandas` · `NumPy` · `Plotly` · `pytest` · `Docker`

## Validation status

Tested before publication:

- `10/10` pytest tests passed
- `7/7` Streamlit pages rendered successfully
- Streamlit app booted successfully
- Health endpoint returned `200 ok`

## How to run locally

```bash
git clone https://github.com/Samadritaacharya/tech-retail-operations-intelligence.git
cd tech-retail-operations-intelligence
pip install -r requirements.txt
streamlit run app.py
```

Run tests:

```bash
pytest -v
```

## Deploy to Streamlit Cloud

Use:

```text
Repository: Samadritaacharya/tech-retail-operations-intelligence
Branch: main
Main file path: app.py
```

## Why this project is relevant to my target roles

This project supports my target direction in tech retail, product operations, digital transformation and technical project management. It is relevant for companies such as fashion-tech, e-commerce, retail platforms and business-technology teams where operations data must become clear action.

Relevant target roles:

- Product Operations Analyst
- Junior Project Manager / PMO Analyst
- Retail Technology Analyst
- Digital Transformation Associate
- Business Technology Analyst
- E-commerce Operations Analyst

## CV bullet

> Built a Tech Retail Operations Intelligence Dashboard using Python, Streamlit, Pandas and Plotly to analyze synthetic e-commerce data across orders, fulfillment delays, returns, support tickets, inventory risk, campaign impact and PMO action planning.

## Disclaimer

All orders, brands, campaigns, regions and customer signals are synthetic. No real retailer, brand, employer, client or customer data is used.

---

**Samadrita Acharya** · [LinkedIn](https://www.linkedin.com/in/samadrita-acharya-a07266184/) · [GitHub](https://github.com/Samadritaacharya)
