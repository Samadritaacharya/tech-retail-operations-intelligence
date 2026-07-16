# Tech Retail Operations Intelligence Dashboard

An e-commerce operations intelligence application for order and fulfillment analytics, support trends, return/refund insights, inventory-risk scoring, campaign-impact analysis, and prioritized PMO action planning.

[![Python CI](https://github.com/Samadritaacharya/tech-retail-operations-intelligence/actions/workflows/ci.yml/badge.svg)](https://github.com/Samadritaacharya/tech-retail-operations-intelligence/actions/workflows/ci.yml)

**Live application:** [tech-retail-operations-intelligence.streamlit.app](https://tech-retail-operations-intelligence.streamlit.app/)  
**Validation evidence:** [VALIDATION_REPORT.md](VALIDATION_REPORT.md)  
**Portfolio owner:** [Samadrita Acharya](https://www.linkedin.com/in/samadrita-acharya-a07266184/)

## Recruiter quick view

| Area | Evidence in this project |
|---|---|
| Business problem | Retail teams must connect checkout, fulfillment, returns, support, inventory, and campaign signals to operational decisions. |
| Product solution | A seven-page Streamlit dashboard simulating a European fashion e-commerce operation. |
| Analytics | Revenue, failures, delays, returns, refunds, support demand, inventory days of cover, and campaign impact. |
| PMO value | Automatically generated actions with business impact, owner, priority, and deadline. |
| Business/technical bridge | Converts operational data into management-ready recommendations rather than isolated charts. |
| Engineering | Modular Python, automated tests, GitHub Actions, Docker support, and documented validation. |
| Data/privacy | All orders, customer signals, campaigns, and brands are synthetic. |

## Business problem

Digital retail teams see many operational signals every day: failed checkouts, late deliveries, return spikes, support tickets, inventory pressure, and campaign side effects. The challenge is converting those signals into a prioritized response with clear ownership and expected business impact.

## Solution

The application simulates a European fashion e-commerce operation and provides:

- revenue, order, checkout-failure, delay, return, and support KPIs
- regional fulfillment and delivery-performance analysis
- customer-support demand and category trends
- return reasons and refund-cost analysis
- inventory days-of-cover risk scoring
- campaign-versus-baseline impact analysis
- PMO action plans with problem, impact, owner, priority, and deadline
- downloadable Markdown and CSV outputs

## Two-minute recruiter demo

1. Open the [live app](https://tech-retail-operations-intelligence.streamlit.app/).
2. Select **Summer sale pressure**, **High returns focus**, or **Inventory risk focus**.
3. Click **Run retail simulation**.
4. Review the order, revenue, and fulfillment KPIs.
5. Explain the return, support, inventory, or campaign insight.
6. Finish with the prioritized PMO action plan and ownership model.

## Dashboard pages

| # | Page | Decision supported |
|---|---|---|
| 1 | Retail Operations Overview | What is happening across revenue and operations? |
| 2 | Order & Fulfillment Analytics | Where are delivery delays and failures concentrated? |
| 3 | Customer Support Trends | Which customer issues are increasing demand? |
| 4 | Return & Refund Insights | Which products and reasons drive return cost? |
| 5 | Inventory Risk | Which categories face stock-out or excess-stock risk? |
| 6 | Campaign Impact | Did campaign growth create operational pressure? |
| 7 | PMO Action Plan | What should happen next, by whom, and by when? |

## Validation status

The repository includes a documented pre-publication validation report:

- `10/10` pytest tests passed
- `7/7` Streamlit pages rendered with Streamlit AppTest
- Streamlit server started successfully
- health endpoint returned `200 ok`
- synthetic data generation, KPI logic, inventory risk, campaign impact, and PMO planning were verified

See [VALIDATION_REPORT.md](VALIDATION_REPORT.md) for the recorded validation scope. GitHub Actions now reruns the test suite for future changes.

## Technology stack

`Python` · `Streamlit` · `Pandas` · `NumPy` · `Plotly` · `pytest` · `GitHub Actions` · `Docker`

## Run locally

```bash
git clone https://github.com/Samadritaacharya/tech-retail-operations-intelligence.git
cd tech-retail-operations-intelligence
python -m venv .venv
```

```bash
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate
```

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pytest -q
python -m streamlit run app.py
```

## Skills demonstrated

Retail technology · e-commerce operations · product operations · fulfillment analytics · customer-support analysis · returns/refunds · inventory risk · campaign impact · KPI design · PMO action planning · data storytelling · Python engineering

## Why this project is relevant to my profile

This project supports my target direction in tech retail, product operations, digital transformation, and technical project management. It demonstrates how I connect technical analytics with operational priorities, stakeholder ownership, and structured delivery actions.

## CV / LinkedIn project description

> Built a tested Tech Retail Operations Intelligence Dashboard using Python, Streamlit, Pandas, and Plotly to analyze synthetic e-commerce data across orders, fulfillment delays, returns, support demand, inventory risk, and campaign impact, then generate prioritized PMO actions with owners and deadlines.

## Responsible portfolio use

All orders, brands, campaigns, regions, and customer signals are synthetic. The project is independent and contains no real retailer, brand, employer, client, customer, or personal data.
