from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "datasets" / "olist"
OUT = ROOT / "datasets" / "processed"
OUT.mkdir(parents=True, exist_ok=True)


def read_csv(name: str) -> pd.DataFrame:
    path = RAW / name
    if not path.exists():
        raise FileNotFoundError(
            f"Missing required Olist file: {path}\n"
            f"Download the dataset and place the CSV files in {RAW}"
        )
    return pd.read_csv(path)


def mode_value(series: pd.Series) -> str:
    values = series.dropna()
    return str(values.mode().iloc[0]) if not values.empty else "Unknown"


def main() -> None:
    orders = read_csv("olist_orders_dataset.csv")
    customers = read_csv("olist_customers_dataset.csv")
    items = read_csv("olist_order_items_dataset.csv")
    products = read_csv("olist_products_dataset.csv")
    sellers = read_csv("olist_sellers_dataset.csv")
    payments = read_csv("olist_order_payments_dataset.csv")
    translations = read_csv("product_category_name_translation.csv")

    for column in [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]:
        orders[column] = pd.to_datetime(orders[column], errors="coerce")
    # Historical labels require a known customer delivery outcome.
    orders = orders.loc[
        orders["order_status"].eq("delivered")
        & orders["order_delivered_customer_date"].notna()
    ].copy()

    items = items.drop_duplicates()

    items = items.merge(
        products[
            ["product_id", "product_category_name", "product_weight_g"]
        ],
        on="product_id",
        how="left",
    )

    items = items.merge(
        translations,
        on="product_category_name",
        how="left",
    )

    items = items.merge(
        sellers[["seller_id", "seller_state"]],
        on="seller_id",
        how="left",
    )

    items["product_category"] = (
        items["product_category_name_english"]
        .fillna(items["product_category_name"])
        .fillna("Unknown")
    )

    item_agg = items.groupby("order_id", as_index=False).agg(
        item_count=("order_item_id", "count"),
        number_of_sellers=("seller_id", "nunique"),
        total_order_value=("price", "sum"),
        total_freight_value=("freight_value", "sum"),
        average_item_price=("price", "mean"),
        average_product_weight_g=("product_weight_g", "mean"),
        main_product_category=("product_category", mode_value),
        seller_state=("seller_state", mode_value),
    )

    payment_agg = payments.groupby("order_id", as_index=False).agg(
        total_payment_value=("payment_value", "sum"),
        average_installments=("payment_installments", "mean"),
        payment_count=("payment_sequential", "count"),
        main_payment_type=("payment_type", mode_value),
    )

    customer_level = customers[
        ["customer_id", "customer_unique_id", "customer_state"]
    ].drop_duplicates("customer_id")

    clean = (
        orders[
            [
                "order_id",
                "customer_id",
                "order_purchase_timestamp",
                "order_approved_at",
                "order_estimated_delivery_date",
                "order_delivered_customer_date",
            ]
        ]
        .merge(customer_level, on="customer_id", how="left")
        .merge(item_agg, on="order_id", how="left")
        .merge(payment_agg, on="order_id", how="left")
    )

    for column in [
        "customer_state",
        "seller_state",
        "main_product_category",
        "main_payment_type",
    ]:
        clean[column] = clean[column].fillna("Unknown").astype(str)

    for column in [
        "item_count",
        "number_of_sellers",
        "total_order_value",
        "total_freight_value",
        "average_item_price",
        "average_product_weight_g",
        "total_payment_value",
        "average_installments",
        "payment_count",
    ]:
        clean[column] = pd.to_numeric(clean[column], errors="coerce")

    output = OUT / "olist_clean_order_level.csv"
    clean.to_csv(output, index=False)
    print(f"Saved {len(clean):,} order-level records to {output}")


if __name__ == "__main__":
    main()
