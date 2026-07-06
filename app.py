"""Tech Retail Operations Intelligence Dashboard."""
from __future__ import annotations
import plotly.express as px
import streamlit as st
from src.data_generator import generate_orders
from src.analytics import compute_kpis, inventory_risk, campaign_impact, build_action_plan, export_action_plan_md

st.set_page_config(page_title="Tech Retail Operations Intelligence", page_icon="🛍️", layout="wide")
st.title("Tech Retail Operations Intelligence Dashboard")
st.caption("Synthetic e-commerce operations analytics for fulfillment, returns, support, inventory and PMO action planning.")

@st.cache_data
def load_data(n_orders: int, days: int, seed: int):
    return generate_orders(n_orders=n_orders, days=days, seed=seed)

def show(fig):
    st.plotly_chart(fig, width="stretch")

pages = ["1 Retail Operations Overview", "2 Order and Fulfillment Analytics", "3 Customer Support Trends", "4 Return and Refund Insights", "5 Inventory Risk", "6 Campaign Impact", "7 PMO Action Plan"]
with st.sidebar:
    page = st.radio("Navigation", pages)
    n_orders = st.slider("Orders", 1000, 12000, 6000, step=1000)
    days = st.slider("History days", 60, 365, 180, step=30)
    seed = int(st.number_input("Random seed", value=42, step=1))
    st.caption("All data is synthetic.")

df = load_data(n_orders, days, seed)
k = compute_kpis(df)
delivered = df[df["order_status"] == "Delivered"]

if page.startswith("1"):
    c = st.columns(5)
    c[0].metric("Orders", f"{k['total_orders']:,}")
    c[1].metric("Revenue", f"€{k['revenue']:,.0f}")
    c[2].metric("Failed rate", f"{k['failed_rate']:.1%}")
    c[3].metric("Return rate", f"{k['return_rate']:.1%}")
    c[4].metric("Support rate", f"{k['support_rate']:.1%}")
    show(px.line(df.groupby("order_date").agg(orders=("order_id", "count"), revenue=("revenue", "sum")).reset_index(), x="order_date", y="orders", title="Daily order volume"))
    show(px.bar(df.groupby("region")["revenue"].sum().reset_index(), x="region", y="revenue", title="Revenue by region"))

elif page.startswith("2"):
    show(px.histogram(delivered, x="delivery_days", color="region", title="Delivery time distribution"))
    late = delivered.assign(late=delivered["delivery_days"] > delivered["promised_delivery_days"]).groupby("region")["late"].mean().reset_index()
    show(px.bar(late, x="region", y="late", title="Late delivery rate by region"))
    show(px.line(df.set_index("order_date").resample("W")["order_status"].apply(lambda s: (s == "Failed").mean()).reset_index(name="failed_rate"), x="order_date", y="failed_rate", title="Weekly failed-order rate"))

elif page.startswith("3"):
    tickets = df[df["support_ticket_flag"]]
    st.metric("Support tickets", len(tickets))
    show(px.bar(tickets.groupby("ticket_category")["order_id"].count().reset_index(), x="ticket_category", y="order_id", title="Support tickets by category"))
    heat = tickets.pivot_table(index="ticket_category", columns="region", values="order_id", aggfunc="count", fill_value=0)
    show(px.imshow(heat, text_auto=True, title="Ticket category by region"))

elif page.startswith("4"):
    returns = df[df["return_flag"]]
    st.metric("Refund cost", f"€{returns['refund_amount'].sum():,.0f}")
    show(px.bar(df.groupby("product_category")["return_flag"].mean().reset_index(), x="product_category", y="return_flag", title="Return rate by category"))
    show(px.bar(returns.groupby("return_reason")["refund_amount"].sum().reset_index(), x="return_reason", y="refund_amount", title="Refund cost by reason"))

elif page.startswith("5"):
    inv = inventory_risk(df)
    show(px.bar(inv, x="product_category", y="days_of_cover", color="inventory_risk", title="Inventory days of cover"))
    st.dataframe(inv, width="stretch", hide_index=True)

elif page.startswith("6"):
    impact = campaign_impact(df)
    st.dataframe(impact, width="stretch", hide_index=True)
    show(px.bar(impact, x="segment", y="revenue", color="segment", title="Campaign vs baseline revenue"))
    show(px.bar(impact, x="segment", y="support_rate", color="segment", title="Campaign operational strain"))

else:
    plan = build_action_plan(df)
    st.dataframe(plan, width="stretch", hide_index=True)
    md = export_action_plan_md(plan)
    st.download_button("Download PMO action plan", md, file_name="retail_pmo_action_plan.md", mime="text/markdown")
    st.download_button("Download action plan CSV", plan.to_csv(index=False), file_name="retail_action_plan.csv", mime="text/csv")
    with st.expander("Preview action plan"):
        st.markdown(md)
