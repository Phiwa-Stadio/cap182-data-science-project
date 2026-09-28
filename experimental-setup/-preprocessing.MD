# Part B – Preprocessing

**Script:** `experimental-setup/preprocessing.py`

## Purpose
Clean the Olist data and prepare a single order-level dataset for modelling.

## Techniques
- Convert relevant date fields to datetime.
- Keep delivered orders with a known delivery date so the late-delivery outcome can be established.
- Remove duplicate order-item records.
- Join order, customer, product, seller and payment information.
- Aggregate item, seller and payment information to one row per order.
- Fill missing categorical values with `Unknown`.
- Leave numerical imputation to the modelling pipelines.

## Leakage prevention
Information only known after delivery is not used as a predictor. This includes the actual delivery date, carrier delivery date, final order status and customer reviews. The actual delivery date is retained only to create the target.

## Input
Place the Olist CSV files in `datasets/olist/`.

## Run
From the repository root:

```bash
python experimental-setup/preprocessing.py
```

## Output
`datasets/processed/olist_clean_order_level.csv`
