# Tech Retail Operations Intelligence Dashboard

[![Python CI](https://github.com/Samadritaacharya/tech-retail-operations-intelligence/actions/workflows/ci.yml/badge.svg)](https://github.com/Samadritaacharya/tech-retail-operations-intelligence/actions/workflows/ci.yml)

**An e-commerce operations intelligence application connecting order, fulfillment, support, returns, inventory, campaign, and prioritization signals into one operational decision workflow.**

[**Open live app →**](https://tech-retail-operations-intelligence.streamlit.app/) · [Validation evidence](VALIDATION_REPORT.md) · [Source](https://github.com/Samadritaacharya/tech-retail-operations-intelligence)

> All orders, brands, campaigns, regions, and customer signals are synthetic. No confidential retailer, employer, client, customer, or personal data is used.

## What it does

- revenue, order, checkout-failure, delay, return, and support KPIs
- regional fulfillment and delivery-performance analysis
- customer-support demand and category trends
- return-reason and refund-cost analysis
- inventory days-of-cover risk scoring
- campaign-versus-baseline impact analysis
- prioritized action plans with problem, impact, owner, priority, and deadline
- downloadable Markdown and CSV outputs

## Dashboard pages

| # | Page | Decision supported |
|---|---|---|
| 1 | Retail Operations Overview | What is happening across revenue and operations? |
| 2 | Order & Fulfillment Analytics | Where are delivery delays and failures concentrated? |
| 3 | Customer Support Trends | Which issues are increasing demand? |
| 4 | Return & Refund Insights | Which products and reasons drive return cost? |
| 5 | Inventory Risk | Which categories face stock-out or excess-stock risk? |
| 6 | Campaign Impact | Did campaign growth create operational pressure? |
| 7 | Action Plan | What should happen next, by whom, and by when? |

## Verification snapshot

The recorded validation includes:

- `10/10` pytest tests passed
- `7/7` Streamlit pages rendered with Streamlit AppTest
- Streamlit health endpoint returned `200 ok`
- synthetic data generation, KPI logic, inventory risk, campaign impact, and action planning verified

GitHub Actions reruns the automated checks on future changes. See [VALIDATION_REPORT.md](VALIDATION_REPORT.md) for scope and limitations.

## Technology

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

## Design principle

Retail operations becomes actionable when teams can connect commercial signals to fulfillment, support, returns, inventory, and campaign pressure—and then assign the next response with clear ownership.
