"""Tech Retail Operations Intelligence Dashboard."""
from __future__ import annotations

import plotly.express as px
import streamlit as st

from src.data_generator import generate_orders
from src.analytics import compute_kpis, inventory_risk, campaign_impact, build_action_plan, export_action_plan_md

st.set_page_config(
    page_title="Tech Retail Operations Intelligence",
    page_icon="◇",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get help": "https://github.com/Samadritaacharya/tech-retail-operations-intelligence",
        "Report a bug": "https://github.com/Samadritaacharya/tech-retail-operations-intelligence/issues",
        "About": "Independent retail-operations portfolio project using synthetic data.",
    },
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] {font-family: Inter, system-ui, sans-serif;}
    .stApp {
      background:
        radial-gradient(circle at 8% -4%, rgba(109,44,103,.11), transparent 31rem),
        radial-gradient(circle at 92% 4%, rgba(212,154,58,.13), transparent 31rem),
        #fbf8f4;
    }
    .block-container {max-width:1480px;padding-top:1.2rem;padding-bottom:4rem;}
    .retail-hero {position:relative;overflow:hidden;background:linear-gradient(124deg,#24102d 0%,#552252 54%,#9f6b25 100%);border-radius:28px;padding:2.55rem 2.7rem;color:white;margin-bottom:1.1rem;box-shadow:0 30px 86px rgba(45,18,56,.21);border:1px solid rgba(255,255,255,.09);}
    .retail-hero:before {content:'';position:absolute;width:480px;height:480px;border-radius:999px;right:-160px;top:-210px;background:rgba(255,224,166,.15);}
    .retail-hero:after {content:'';position:absolute;inset:auto 0 0 0;height:1px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.35),transparent);}
    .eyebrow {position:relative;z-index:1;font-size:.75rem;letter-spacing:.14em;text-transform:uppercase;font-weight:800;color:#ffe1a6;margin-bottom:.72rem;}
    .retail-hero h1 {position:relative;z-index:1;font-size:clamp(2.25rem,4.8vw,4.05rem);line-height:1;margin:0 0 .85rem;color:white;letter-spacing:-.055em;max-width:1000px;}
    .retail-hero p {position:relative;z-index:1;font-size:1.04rem;line-height:1.72;color:#f7e9ef;max-width:1010px;margin:0;}
    .chip-row {position:relative;z-index:1;display:flex;flex-wrap:wrap;gap:.45rem;margin-top:1.2rem;}
    .chip {display:inline-flex;align-items:center;gap:.4rem;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.14);border-radius:999px;padding:.36rem .7rem;color:#fff7e8;font-size:.78rem;font-weight:650;backdrop-filter:blur(12px);}
    .live-dot {width:.47rem;height:.47rem;border-radius:99px;background:#f7c76d;box-shadow:0 0 0 5px rgba(247,199,109,.12);display:inline-block;}
    .journey-strip {display:grid;grid-template-columns:repeat(5,1fr);gap:.58rem;margin:.82rem 0 1.05rem;}
    .journey-step {background:rgba(255,255,255,.86);border:1px solid #eadde6;border-radius:16px;padding:.86rem .95rem;box-shadow:0 10px 30px rgba(55,25,55,.045);}
    .journey-step strong {display:block;color:#40213f;font-size:.82rem;margin-bottom:.2rem;}
    .journey-step span {color:#7b6a77;font-size:.74rem;}
    .journey-step b {color:#aa742c;font-size:.69rem;margin-right:.25rem;}
    .context-card {background:rgba(255,255,255,.88);border:1px solid #eadde6;border-radius:18px;padding:1rem 1.12rem;margin-bottom:1rem;box-shadow:0 12px 34px rgba(55,25,55,.045);color:#695765;backdrop-filter:blur(10px);}
    .context-card strong {color:#6d2c67;}
    .context-card .muted {font-size:.86rem;color:#857581;margin-top:.3rem;}
    .section-kicker {font-size:.74rem;letter-spacing:.12em;text-transform:uppercase;color:#9a6624;font-weight:800;margin-top:1.1rem;}
    div[data-testid="stMetric"] {background:linear-gradient(180deg,#fff,#fcf8f3);border:1px solid #eadde6;border-top:3px solid #c38a34;padding:14px 16px;border-radius:16px;box-shadow:0 11px 28px rgba(55,25,55,.045);}
    div[data-testid="stMetricLabel"] {color:#786875;}
    div[data-testid="stMetricValue"] {color:#3d233c;letter-spacing:-.035em;}
    [data-testid="stSidebar"] {background:linear-gradient(180deg,#23102c 0%,#3b1939 100%);border-right:1px solid rgba(255,255,255,.08);}
    [data-testid="stSidebar"] * {color:#f8edf6;}
    [data-testid="stSidebar"] [data-baseweb="select"] > div,
    [data-testid="stSidebar"] input {background:rgba(255,255,255,.07)!important;border-color:rgba(255,255,255,.12)!important;}
    .stButton>button,.stDownloadButton>button {border-radius:12px!important;font-weight:750!important;min-height:2.65rem;transition:transform .18s ease,box-shadow .18s ease!important;}
    .stButton>button:hover,.stDownloadButton>button:hover {transform:translateY(-1px);box-shadow:0 10px 28px rgba(109,44,103,.14)!important;}
    div[data-testid="stExpander"] {background:rgba(255,255,255,.74);border:1px solid #eadde6;border-radius:14px;}
    div[data-testid="stDataFrame"] {border:1px solid #eadde6;border-radius:14px;overflow:hidden;}
    [data-testid="stAlert"] {border-radius:14px;}
    @media(max-width:950px){.journey-strip{grid-template-columns:1fr 1fr}.retail-hero{padding:2rem 1.45rem}}
    @media(max-width:560px){.journey-strip{grid-template-columns:1fr}}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="retail-hero">
      <div class="eyebrow">Commerce Operations · Customer Experience · Action Intelligence</div>
      <h1>Tech Retail Operations Intelligence</h1>
      <p>Explore how order, fulfillment, return, support, inventory and campaign signals can be converted into a concise operating narrative and an accountable PMO action plan.</p>
      <div class="chip-row">
        <span class="chip"><span class="live-dot"></span> Interactive retail simulation</span>
        <span class="chip">Fulfillment</span><span class="chip">Returns</span><span class="chip">Inventory</span><span class="chip">Campaign strain</span><span class="chip">Owner actions</span>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="journey-strip">
      <div class="journey-step"><strong><b>01</b> Demand</strong><span>Orders, revenue and campaigns</span></div>
      <div class="journey-step"><strong><b>02</b> Fulfill</strong><span>Delivery speed and failures</span></div>
      <div class="journey-step"><strong><b>03</b> Support</strong><span>Customer-contact pressure</span></div>
      <div class="journey-step"><strong><b>04</b> Protect</strong><span>Returns and inventory exposure</span></div>
      <div class="journey-step"><strong><b>05</b> Act</strong><span>Prioritized cross-functional actions</span></div>
    </div>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_data(n_orders: int, days: int, seed: int):
    return generate_orders(n_orders=n_orders, days=days, seed=seed)


def show(fig):
    fig.update_layout(
        margin=dict(l=18, r=18, t=58, b=18),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, system-ui, sans-serif", color="#6f5f6c"),
        title_font=dict(size=17, color="#3d233c"),
        legend_title_text="",
        hoverlabel=dict(font_size=13),
    )
    st.plotly_chart(fig, width="stretch", config={"displaylogo": False})


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
    st.markdown("### ◇ Retail Control Room")
    st.caption("Choose a commercial scenario and follow the operating story from demand to action.")
    page = st.radio("Workspace", pages)
    st.divider()
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
    days = st.slider("History window", 60, 365, preset[1], step=30, format="%d days")
    seed = int(st.number_input("Simulation seed", value=preset[2], step=1))
    if st.button("Run retail simulation →", width="stretch", type="primary"):
        st.session_state.retail_run += 1
    st.divider()
    st.caption("Synthetic portfolio data only. No employer, customer, transaction or personal data.")

effective_seed = seed + st.session_state.retail_run * 23
df = load_data(n_orders, days, effective_seed)

with st.expander("Filters · focus the commercial view", expanded=False):
    f1, f2, f3 = st.columns(3)
    regions = f1.multiselect("Region", sorted(df["region"].unique()))
    categories = f2.multiselect("Category", sorted(df["product_category"].unique()))
    segments = f3.multiselect("Customer segment", sorted(df["customer_segment"].unique()))
    if regions:
        df = df[df["region"].isin(regions)]
    if categories:
        df = df[df["product_category"].isin(categories)]
    if segments:
        df = df[df["customer_segment"].isin(segments)]

k = compute_kpis(df)
delivered = df[df["order_status"] == "Delivered"]
ops_risk = max(k["failed_rate"], k["return_rate"], k["support_rate"])
ops_signal = "Stable" if ops_risk < 0.08 else "Watch" if ops_risk < 0.15 else "Intervene"

st.markdown(
    f"""
    <div class="context-card"><strong>{scenario}</strong> · {n_orders:,} synthetic orders · {days} days · simulation {st.session_state.retail_run + 1} · operating signal: <strong>{ops_signal}</strong>
      <div class="muted">Recommended flow: Overview → Fulfillment → Returns → Inventory → PMO Action Plan.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

if page.startswith("1"):
    st.markdown('<div class="section-kicker">Executive commerce view</div>', unsafe_allow_html=True)
    st.subheader("Retail Operations Overview")
    c = st.columns(5)
    c[0].metric("Orders", f"{k['total_orders']:,}")
    c[1].metric("Revenue", f"€{k['revenue']:,.0f}")
    c[2].metric("Failed rate", f"{k['failed_rate']:.1%}")
    c[3].metric("Return rate", f"{k['return_rate']:.1%}")
    c[4].metric("Support rate", f"{k['support_rate']:.1%}")
    col1, col2 = st.columns([1.55, 1])
    with col1:
        show(px.line(df.groupby("order_date").agg(orders=("order_id", "count"), revenue=("revenue", "sum")).reset_index(), x="order_date", y="orders", title="Daily demand signal"))
    with col2:
        show(px.bar(df.groupby("region")["revenue"].sum().reset_index(), x="region", y="revenue", title="Revenue by region"))
    st.info(f"Operating readout: **{ops_signal}**. The highest headline pressure among failed orders, returns and support contacts is **{ops_risk:.1%}**. Use the downstream views to identify the owner and corrective lever.")

elif page.startswith("2"):
    st.markdown('<div class="section-kicker">Fulfillment experience</div>', unsafe_allow_html=True)
    st.subheader("Order & Fulfillment Analytics")
    col1, col2 = st.columns(2)
    with col1:
        show(px.histogram(delivered, x="delivery_days", color="region", title="Delivery time distribution"))
    late = delivered.assign(late=delivered["delivery_days"] > delivered["promised_delivery_days"]).groupby("region")["late"].mean().reset_index()
    with col2:
        show(px.bar(late, x="region", y="late", title="Late delivery rate by region"))
    show(px.line(df.set_index("order_date").resample("W")["order_status"].apply(lambda s: (s == "Failed").mean()).reset_index(name="failed_rate"), x="order_date", y="failed_rate", title="Weekly failed-order rate"))

elif page.startswith("3"):
    st.markdown('<div class="section-kicker">Customer friction</div>', unsafe_allow_html=True)
    st.subheader("Customer Support Trends")
    tickets = df[df["support_ticket_flag"]]
    st.metric("Support tickets", len(tickets))
    col1, col2 = st.columns(2)
    with col1:
        show(px.bar(tickets.groupby("ticket_category")["order_id"].count().reset_index(), x="ticket_category", y="order_id", title="Support demand by category"))
    heat = tickets.pivot_table(index="ticket_category", columns="region", values="order_id", aggfunc="count", fill_value=0)
    with col2:
        show(px.imshow(heat, text_auto=True, title="Support category × region"))

elif page.startswith("4"):
    st.markdown('<div class="section-kicker">Post-purchase economics</div>', unsafe_allow_html=True)
    st.subheader("Return & Refund Insights")
    returns = df[df["return_flag"]]
    st.metric("Refund cost", f"€{returns['refund_amount'].sum():,.0f}")
    col1, col2 = st.columns(2)
    with col1:
        show(px.bar(df.groupby("product_category")["return_flag"].mean().reset_index(), x="product_category", y="return_flag", title="Return rate by category"))
    with col2:
        show(px.bar(returns.groupby("return_reason")["refund_amount"].sum().reset_index(), x="return_reason", y="refund_amount", title="Refund cost by reason"))

elif page.startswith("5"):
    st.markdown('<div class="section-kicker">Stock resilience</div>', unsafe_allow_html=True)
    st.subheader("Inventory Risk")
    inv = inventory_risk(df)
    show(px.bar(inv, x="product_category", y="days_of_cover", color="inventory_risk", title="Inventory days of cover"))
    st.dataframe(inv, width="stretch", hide_index=True)

elif page.startswith("6"):
    st.markdown('<div class="section-kicker">Commercial experiment impact</div>', unsafe_allow_html=True)
    st.subheader("Campaign Impact")
    impact = campaign_impact(df)
    st.dataframe(impact, width="stretch", hide_index=True)
    col1, col2 = st.columns(2)
    with col1:
        show(px.bar(impact, x="segment", y="revenue", color="segment", title="Campaign vs baseline revenue"))
    with col2:
        show(px.bar(impact, x="segment", y="support_rate", color="segment", title="Campaign operational strain"))

else:
    st.markdown('<div class="section-kicker">Decision to execution</div>', unsafe_allow_html=True)
    st.subheader("PMO Action Plan")
    plan = build_action_plan(df)
    st.dataframe(plan, width="stretch", hide_index=True)
    md = export_action_plan_md(plan)
    c1, c2 = st.columns(2)
    c1.download_button("Download leadership action brief", md, file_name="retail_pmo_action_plan.md", mime="text/markdown", width="stretch")
    c2.download_button("Download owner action plan", plan.to_csv(index=False), file_name="retail_action_plan.csv", mime="text/csv", width="stretch")
    with st.expander("Preview action brief"):
        st.markdown(md)
