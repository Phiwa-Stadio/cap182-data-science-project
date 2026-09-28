from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "datasets" / "processed" / "olist_clean_order_level.csv"
OUTPUT = ROOT / "datasets" / "processed" / "olist_model_ready.csv"


def main() -> None:
    if not INPUT.exists():
        raise FileNotFoundError(
            "Processed dataset not found. Run experimental-setup/preprocessing.py first."
        )

    dates = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_estimated_delivery_date",
        "order_delivered_customer_date",
    ]

    df = pd.read_csv(INPUT, parse_dates=dates)

    df["late_delivery"] = (
        df["order_delivered_customer_date"]
        > df["order_estimated_delivery_date"]
    ).astype(int)

    purchase = df["order_purchase_timestamp"]

    df["purchase_hour"] = purchase.dt.hour
    df["purchase_day_of_week"] = purchase.dt.dayofweek
    df["purchase_month"] = purchase.dt.month
    df["is_weekend"] = purchase.dt.dayofweek.isin([5, 6]).astype(int)

    df["approval_delay_hours"] = (
        df["order_approved_at"] - purchase
    ).dt.total_seconds() / 3600.0

    df["estimated_delivery_days"] = (
        df["order_estimated_delivery_date"]
        - purchase.dt.normalize()
    ).dt.total_seconds() / 86400.0

    df["freight_ratio"] = (
        df["total_freight_value"]
        / df["total_order_value"].replace(0, np.nan)
    )

    df["value_per_item"] = (
        df["total_order_value"]
        / df["item_count"].replace(0, np.nan)
    )

    df["seller_customer_same_state"] = (
        df["seller_state"] == df["customer_state"]
    ).astype(int)

    keep = [
        "order_id",
        "order_purchase_timestamp",
        "customer_state",
        "seller_state",
        "seller_customer_same_state",
        "main_product_category",
        "main_payment_type",
        "purchase_hour",
        "purchase_day_of_week",
        "purchase_month",
        "is_weekend",
        "approval_delay_hours",
        "estimated_delivery_days",
        "item_count",
        "number_of_sellers",
        "total_order_value",
        "total_freight_value",
        "average_item_price",
        "average_product_weight_g",
        "total_payment_value",
        "average_installments",
        "payment_count",
        "freight_ratio",
        "value_per_item",
        "late_delivery",
    ]

    df[keep].replace([np.inf, -np.inf], np.nan).to_csv(
        OUTPUT, index=False
    )

    print(f"Saved {len(df):,} modelling records to {OUTPUT}")
    print(df["late_delivery"].value_counts().sort_index())


if __name__ == "__main__":
    main()
