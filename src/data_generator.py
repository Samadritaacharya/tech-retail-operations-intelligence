"""Synthetic tech-retail operations data generator."""
from __future__ import annotations
import numpy as np
import pandas as pd

CATEGORIES = ["Dresses", "Shoes", "Beauty", "Accessories", "Outerwear", "Sportswear"]
BRANDS = ["Luma", "Nordlane", "Velvet Ivy", "Aster", "UrbanForm"]
REGIONS = ["Germany", "France", "Netherlands", "Italy", "Spain"]
CAMPAIGNS = ["SUMMER-SALE", "NEW-SEASON", "APP-PUSH"]


def generate_orders(n_orders: int = 6000, days: int = 180, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    end = pd.Timestamp.today().normalize()
    dates = end - pd.to_timedelta(rng.integers(0, days, n_orders), unit="D")
    category = rng.choice(CATEGORIES, n_orders, p=[.22, .18, .14, .16, .14, .16])
    brand = rng.choice(BRANDS, n_orders)
    region = rng.choice(REGIONS, n_orders, p=[.34, .22, .16, .14, .14])
    segment = rng.choice(["New", "Returning", "VIP"], n_orders, p=[.45, .42, .13])
    campaign = np.where(rng.random(n_orders) < .32, rng.choice(CAMPAIGNS, n_orders), "")
    base_price = pd.Series(category).map({"Dresses": 85, "Shoes": 95, "Beauty": 35, "Accessories": 45, "Outerwear": 130, "Sportswear": 70}).to_numpy(float)
    revenue = np.round(base_price * rng.normal(1.0, .25, n_orders) * np.where(campaign != "", 1.18, 1.0), 2)
    failed = rng.random(n_orders) < (.035 + np.where(campaign != "", .025, 0))
    cancelled = (~failed) & (rng.random(n_orders) < .025)
    status = np.where(failed, "Failed", np.where(cancelled, "Cancelled", "Delivered"))
    promised = rng.choice([2, 3, 4, 5], n_orders, p=[.25, .35, .25, .15])
    regional_delay = np.where(np.isin(region, ["Italy", "Spain"]), 1.0, 0)
    delivery = np.where(status == "Delivered", np.maximum(1, np.round(promised + regional_delay + rng.normal(0.2, 1.2, n_orders), 0)), np.nan)
    return_base = pd.Series(category).map({"Dresses": .24, "Shoes": .18, "Beauty": .06, "Accessories": .09, "Outerwear": .14, "Sportswear": .13}).to_numpy(float)
    returned = (status == "Delivered") & (rng.random(n_orders) < return_base)
    reasons = rng.choice(["Size/fit", "Quality", "Changed mind", "Late delivery", "Damaged"], n_orders)
    support = rng.random(n_orders) < (.08 + failed * .35 + returned * .18 + np.where(campaign != "", .04, 0))
    ticket_category = np.where(support, rng.choice(["WISMO", "Payment", "Return", "Product question", "Complaint"], n_orders), "")
    refund = np.where(returned, np.round(revenue * rng.uniform(.65, 1.0, n_orders), 2), 0.0)
    return pd.DataFrame({"order_id": [f"ORD{1000000+i}" for i in range(n_orders)], "order_date": dates, "product_category": category, "brand": brand, "region": region, "order_status": status, "delivery_days": delivery, "promised_delivery_days": promised, "return_flag": returned, "return_reason": np.where(returned, reasons, ""), "support_ticket_flag": support, "ticket_category": ticket_category, "inventory_level": rng.integers(5, 420, n_orders), "campaign_id": campaign, "customer_segment": segment, "revenue": revenue, "refund_amount": refund})
