"""Tech Retail Operations Intelligence Dashboard."""
from __future__ import annotations

import plotly.express as px
import streamlit as st

from src.data_generator import generate_orders
from src.analytics import compute_kpis, inventory_risk, campaign_impact, build_action_plan, export_action_plan_md

st.set_page_config(page_title="Tech Retail Operations Intelligence", page_icon="🛍️", layout="wide")

st.markdown(
    """
    <style>
    .hero {
        background: linear-gradient(135deg, #2d1238 0%, #6d2c67 55%, #d49a3a 100%);
        padding: 2rem 2.2rem;
        border-radius: 22px;
        color: white;
        margin-bottom: 1.4rem;
        box-shadow: 0 18px 55px rgba(45, 18, 56, 0.22);
    }
    .hero h1 {font-size: 2.35rem; margin: 0 0 .55rem 0; letter-spacing: -.04em;}
    .hero p {font-size: 1.02rem; max-width: 980px; color: #fff4dd; margin: 0;}
    .demo-card {
        border: 1px solid #eadce8;
        border-left: 5px solid #d49a3a;
        border-radius: 14px;
        padding: 1rem 1.1rem;
        background: #fffaf1;
        margin-bottom: 1rem;
    }
    div[data-testid="stMetric"] {
        background: #fffaf1;
        border-left: 4px solid #d49a3a;
        padding: 12px 16px;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
      <h1>🛍️ Tech Retail Operations Intelligence</h1>
      <p>Interactive e-commerce operations dashboard for failed orders, fulfillment delays, returns, support pressure, inventory risk, campaign impact and PMO action planning. Select a retail scenario, click <b>Run retail simulation</b>, and explain the end-to-end decision workflow.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

@st.cache_data
def load_data(n_orders: int, days: int, seed: int):
    return generate_orders(n_orders=n_orders, days=days, seed=seed)

def show(fig):
    st.plotly_chart(fig, width="stretch")

pages = [
    "1 Retail Operations Overview",
    "2 Order and Fulfillment Analytics",
    "3 Customer Support Trends",
    "4 Return and Refund Insights",
    "5 Inventory Risk",
    "6 Campaign Impact",
    "7 PMO Action Plan",
]

if "retail_run" not in st.session_state:
    st.session_state.retail_run = 0

with st.sidebar:
    st.header("🎛️ Live demo inputs")
    page = st.radio("Navigation", pages)
    scenario = st.selectbox(
        "Scenario preset",
        ["Balanced retail operations", "Summer sale pressure", "High returns focus", "Delivery delay focus", "Inventory risk focus"],
    )
    preset = {
        "Balanced retail operations": (6000, 180, 42),
        "Summer sale pressure": (9000, 150, 91),
        "High returns focus": (7000, 180, 133),
        "Delivery delay focus": (6500, 240, 155),
        "Inventory risk focus": (8000, 180, 204),
    }[scenario]
    n_orders = st.slider("Order volume", 1000, 12000, preset[0], step=1000)
    days = st.slider("History window in days", 60, 365, preset[1], step=30)
    seed = int(st.number_input("Simulation seed", value=preset[2], step=1))
    if st.button("🚀 Run retail simulation", width="stretch", type="primary"):
        st.session_state.retail_run += 1
    st.caption("Use this panel to demonstrate: retail signals → operational diagnosis → PMO action plan.")

st.markdown(
    f"""
    <div class="demo-card">
      <b>Current live input:</b> {scenario} · {n_orders:,} synthetic orders · {days} days · run #{st.session_state.retail_run + 1}<br>
      <span style="color:#4a3846;">Best demo flow: Overview → Fulfillment → Returns → Inventory Risk → PMO Action Plan.</span>
    </div>
    """,
    unsafe_allow_html=True,
)

effective_seed = seed + st.session_state.retail_run * 23
df = load_data(n_orders, days, effective_seed)

with st.expander("🔎 Optional filters for live explanation", expanded=False):
    f1, f2, f3 = st.columns(3)
    regions = f1.multiselect("Filter region", sorted(df["region"].unique()))
    categories = f2.multiselect("Filter category", sorted(df["product_category"].unique()))
    segments = f3.multiselect("Filter segment", sorted(df["customer_segment"].unique()))
    if regions:
        df = df[df["region"].isin(regions)]
    if categories:
        df = df[df["product_category"].isin(categories)]
    if segments:
        df = df[df["customer_segment"].isin(segments)]

k = compute_kpis(df)
delivered = df[df["order_status"] == "Delivered"]

if page.startswith("1"):
    st.subheader("Retail Operations Overview")
    c = st.columns(5)
    c[0].metric("Orders", f"{k['total_orders']:,}")
    c[1].metric("Revenue", f"€{k['revenue']:,.0f}")
    c[2].metric("Failed rate", f"{k['failed_rate']:.1%}")
    c[3].metric("Return rate", f"{k['return_rate']:.1%}")
    c[4].metric("Support rate", f"{k['support_rate']:.1%}")
    show(px.line(df.groupby("order_date").agg(orders=("order_id", "count"), revenue=("revenue", "sum")).reset_index(), x="order_date", y="orders", title="Daily order volume"))
    show(px.bar(df.groupby("region")["revenue"].sum().reset_index(), x="region", y="revenue", title="Revenue by region"))

elif page.startswith("2"):
    st.subheader("Order and Fulfillment Analytics")
    show(px.histogram(delivered, x="delivery_days", color="region", title="Delivery time distribution"))
    late = delivered.assign(late=delivered["delivery_days"] > delivered["promised_delivery_days"]).groupby("region")["late"].mean().reset_index()
    show(px.bar(late, x="region", y="late", title="Late delivery rate by region"))
    show(px.line(df.set_index("order_date").resample("W")["order_status"].apply(lambda s: (s == "Failed").mean()).reset_index(name="failed_rate"), x="order_date", y="failed_rate", title="Weekly failed-order rate"))

elif page.startswith("3"):
    st.subheader("Customer Support Trends")
    tickets = df[df["support_ticket_flag"]]
    st.metric("Support tickets", len(tickets))
    show(px.bar(tickets.groupby("ticket_category")["order_id"].count().reset_index(), x="ticket_category", y="order_id", title="Support tickets by category"))
    heat = tickets.pivot_table(index="ticket_category", columns="region", values="order_id", aggfunc="count", fill_value=0)
    show(px.imshow(heat, text_auto=True, title="Ticket category by region"))

elif page.startswith("4"):
    st.subheader("Return and Refund Insights")
    returns = df[df["return_flag"]]
    st.metric("Refund cost", f"€{returns['refund_amount'].sum():,.0f}")
    show(px.bar(df.groupby("product_category")["return_flag"].mean().reset_index(), x="product_category", y="return_flag", title="Return rate by category"))
    show(px.bar(returns.groupby("return_reason")["refund_amount"].sum().reset_index(), x="return_reason", y="refund_amount", title="Refund cost by reason"))

elif page.startswith("5"):
    st.subheader("Inventory Risk")
    inv = inventory_risk(df)
    show(px.bar(inv, x="product_category", y="days_of_cover", color="inventory_risk", title="Inventory days of cover"))
    st.dataframe(inv, width="stretch", hide_index=True)

elif page.startswith("6"):
    st.subheader("Campaign Impact")
    impact = campaign_impact(df)
    st.dataframe(impact, width="stretch", hide_index=True)
    show(px.bar(impact, x="segment", y="revenue", color="segment", title="Campaign vs baseline revenue"))
    show(px.bar(impact, x="segment", y="support_rate", color="segment", title="Campaign operational strain"))

else:
    st.subheader("PMO Action Plan")
    plan = build_action_plan(df)
    st.dataframe(plan, width="stretch", hide_index=True)
    md = export_action_plan_md(plan)
    c1, c2 = st.columns(2)
    c1.download_button("Download PMO action plan", md, file_name="retail_pmo_action_plan.md", mime="text/markdown", width="stretch")
    c2.download_button("Download action plan CSV", plan.to_csv(index=False), file_name="retail_action_plan.csv", mime="text/csv", width="stretch")
    with st.expander("Preview action plan"):
        st.markdown(md)
