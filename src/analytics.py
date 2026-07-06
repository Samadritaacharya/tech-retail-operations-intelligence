"""Retail operations analytics and PMO action planner."""
from __future__ import annotations
import pandas as pd


def compute_kpis(df: pd.DataFrame) -> dict:
    delivered = df[df["order_status"] == "Delivered"]
    late = delivered["delivery_days"] > delivered["promised_delivery_days"]
    return {"total_orders": len(df), "revenue": round(float(df["revenue"].sum()), 2), "failed_rate": round(float((df["order_status"] == "Failed").mean()), 4), "late_delivery_rate": round(float(late.mean()) if len(delivered) else 0, 4), "return_rate": round(float(df["return_flag"].mean()), 4), "support_rate": round(float(df["support_ticket_flag"].mean()), 4), "refund_cost": round(float(df["refund_amount"].sum()), 2)}


def inventory_risk(df: pd.DataFrame) -> pd.DataFrame:
    recent = df.groupby("product_category").agg(orders=("order_id", "count"), avg_inventory=("inventory_level", "mean"), revenue=("revenue", "sum")).reset_index()
    recent["daily_velocity"] = recent["orders"] / max((df["order_date"].max() - df["order_date"].min()).days, 1)
    recent["days_of_cover"] = recent["avg_inventory"] / recent["daily_velocity"].clip(lower=.1)
    recent["inventory_risk"] = pd.cut(recent["days_of_cover"], bins=[-1, 14, 35, 9999], labels=["High", "Medium", "Low"])
    return recent.sort_values("days_of_cover")


def campaign_impact(df: pd.DataFrame) -> pd.DataFrame:
    x = df.copy()
    x["campaign_active"] = x["campaign_id"] != ""
    out = x.groupby("campaign_active").agg(orders=("order_id", "count"), revenue=("revenue", "sum"), failed_rate=("order_status", lambda s: (s == "Failed").mean()), support_rate=("support_ticket_flag", "mean"), return_rate=("return_flag", "mean")).reset_index()
    out["segment"] = out["campaign_active"].map({True: "Campaign", False: "Baseline"})
    return out


def build_action_plan(df: pd.DataFrame) -> pd.DataFrame:
    k = compute_kpis(df)
    rows = []
    if k["failed_rate"] > .04:
        rows.append(["Checkout failure spike", f"{k['failed_rate']:.1%} failed orders", "Review payment and checkout logs", "Platform Operations", "High", "1 week"])
    if k["late_delivery_rate"] > .25:
        rows.append(["Late delivery risk", f"{k['late_delivery_rate']:.1%} late deliveries", "Escalate carrier performance review", "Fulfillment Ops", "High", "2 weeks"])
    if k["return_rate"] > .14:
        rows.append(["Return rate above target", f"{k['return_rate']:.1%} returns", "Improve sizing/product content and quality checks", "Product Operations", "Medium", "3 weeks"])
    if k["support_rate"] > .12:
        rows.append(["Support ticket pressure", f"{k['support_rate']:.1%} ticket rate", "Add proactive WISMO and return communication", "Customer Care", "Medium", "2 weeks"])
    inv = inventory_risk(df)
    for _, r in inv[inv["inventory_risk"] == "High"].head(3).iterrows():
        rows.append([f"Inventory risk: {r['product_category']}", f"{r['days_of_cover']:.1f} days cover", "Review replenishment and campaign forecast", "Merchandising", "High", "1 week"])
    if not rows:
        rows.append(["Operations stable", "No threshold breach", "Continue weekly monitoring", "Retail Ops", "Low", "4 weeks"])
    return pd.DataFrame(rows, columns=["problem", "business_impact", "suggested_action", "owner", "priority", "deadline"])


def export_action_plan_md(plan: pd.DataFrame) -> str:
    lines = ["# Tech Retail Operations PMO Action Plan", ""]
    for _, r in plan.iterrows():
        lines.append(f"- **[{r['priority']}] {r['problem']}** — {r['business_impact']}. Action: {r['suggested_action']}. Owner: {r['owner']}. Deadline: {r['deadline']}.")
    lines.append("\n_Generated from synthetic retail operations data._")
    return "\n".join(lines)
