"""Tests for retail data generation, analytics and PMO action planning."""
import pandas as pd
import pytest
from src.data_generator import generate_orders, CATEGORIES, CAMPAIGNS
from src.analytics import compute_kpis, inventory_risk, campaign_impact, build_action_plan, export_action_plan_md

@pytest.fixture(scope="module")
def df():
    return generate_orders(n_orders=4000, days=120, seed=7)

def test_generator_columns(df):
    expected={"order_id","order_date","product_category","brand","region","order_status","delivery_days","promised_delivery_days","return_flag","return_reason","support_ticket_flag","ticket_category","inventory_level","campaign_id","customer_segment","revenue","refund_amount"}
    assert expected.issubset(df.columns)
    assert df["order_id"].is_unique
    assert set(df["product_category"].unique()).issubset(set(CATEGORIES))

def test_generator_reproducible():
    pd.testing.assert_frame_equal(generate_orders(n_orders=500, seed=3), generate_orders(n_orders=500, seed=3))

def test_delivery_and_returns_consistency(df):
    delivered=df[df["order_status"]=="Delivered"]
    assert delivered["delivery_days"].notna().all()
    assert df[df["order_status"]!="Delivered"]["delivery_days"].isna().all()
    assert not df[df["return_flag"] & (df["order_status"]!="Delivered")].shape[0]
    assert (df.loc[~df["return_flag"],"refund_amount"]==0).all()
    assert (df.loc[df["return_flag"],"refund_amount"]>0).all()

def test_campaigns_present_and_lift(df):
    tagged=df[df["campaign_id"]!=""]
    assert set(tagged["campaign_id"].unique()).issubset(set(CAMPAIGNS))
    assert len(tagged)>0

def test_kpis(df):
    k=compute_kpis(df)
    assert k["total_orders"]==len(df)
    for key in ("failed_rate","late_delivery_rate","return_rate","support_rate"):
        assert 0 <= k[key] <= 1
    assert k["revenue"]>0

def test_inventory_risk(df):
    inv=inventory_risk(df)
    assert {"product_category","days_of_cover","inventory_risk"}.issubset(inv.columns)
    assert len(inv)>0

def test_campaign_impact(df):
    impact=campaign_impact(df)
    assert {"segment","revenue","failed_rate","support_rate"}.issubset(impact.columns)
    assert set(impact["segment"]).issubset({"Campaign","Baseline"})

def test_action_plan(df):
    plan=build_action_plan(df)
    assert not plan.empty
    assert {"problem","business_impact","suggested_action","owner","priority","deadline"}.issubset(plan.columns)

def test_markdown_export(df):
    md=export_action_plan_md(build_action_plan(df))
    assert md.startswith("# Tech Retail Operations PMO Action Plan")
    assert "synthetic" in md.lower()

def test_dresses_return_more_than_beauty(df):
    rates=df.groupby("product_category")["return_flag"].mean()
    assert rates["Dresses"] > rates["Beauty"]
