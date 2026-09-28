# Part B – Feature Engineering

**Script:** `experimental-setup/feature-engineering.py`

## Purpose
Create variables that could reasonably be available before the delivery outcome and may help predict late delivery.

## Target
`late_delivery = 1` when actual customer delivery is later than the estimated delivery date; otherwise `0`.

The actual delivery date is used only to create this target and is then removed from the model inputs.

## Features
- Purchase hour, day of week and month
- Weekend indicator
- Approval delay in hours
- Estimated delivery time in days
- Number of items
- Number of sellers
- Total order value
- Total freight value
- Average item price
- Average product weight
- Payment count and instalments
- Freight-to-order-value ratio
- Value per item
- Customer and seller state
- Same-state seller/customer indicator
- Main product category
- Main payment type

## Run

```bash
python experimental-setup/feature-engineering.py
```

## Output
`datasets/processed/olist_model_ready.csv`
