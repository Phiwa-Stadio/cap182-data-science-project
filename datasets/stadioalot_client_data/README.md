# STADIOalot — Late & Failed Delivery: Raw Logistics Extract

Four years of raw delivery records (September 2022 to August 2026), successful and unsuccessful. Customer, driver and vehicle identifiers are anonymised. Join `order_id` between Table 1 and the rest; Tables 2-6 are keyed on `delivery_id`, so an order with multiple attempts has multiple rows there. Datetimes are `yyyy-MM-dd HH:mm:ss`; distances are km, durations minutes, values ZAR.

## Files

### `1_orders_deliveries.csv`
One row per order, with the final delivery outcome. Contains the target.  
Rows: 6,296

| Column | Description |
|---|---|
| `order_id` | String |
| `order_date` | Datetime |
| `dispatch_date` | Datetime |
| `promised_delivery` | Datetime |
| `delivery_date` | Datetime |
| `delivery_status` | Categorical |
| `delivery_attempt` | Integer |
| `delivery_outcome` | Categorical |
| `delivery_duration_minutes` | Integer |
| `late_delivery` | Integer |
| `repeat_delivery` | Integer |
| `order_value` | Numeric |
| `item_count` | Integer |
| `product_category` | Categorical |
| `delivery_type` | Categorical |
| `customer_id` | String |

### `2_delivery_route.csv`
One row per delivery attempt, with route, vehicle, traffic and weather context.  
Rows: 8,779

| Column | Description |
|---|---|
| `delivery_id` | String |
| `order_id` | String |
| `route_id` | String |
| `driver_id` | String |
| `vehicle_id` | String |
| `dc_id` | Categorical |
| `delivery_area` | String |
| `delivery_latitude` | Numeric |
| `delivery_longitude` | Numeric |
| `route_distance_km` | Numeric |
| `actual_distance_km` | Numeric |
| `planned_duration_minutes` | Integer |
| `actual_duration_minutes` | Integer |
| `stop_number` | Integer |
| `route_start` | Datetime |
| `delivery_window` | Categorical |
| `traffic_condition` | Categorical |
| `weather_condition` | Categorical |

### `3_customer_delivery_history.csv`
Customer history as at each delivery attempt (point-in-time).  
Rows: 8,779

| Column | Description |
|---|---|
| `delivery_id` | String |
| `order_id` | String |
| `customer_id` | String |
| `customer_tenure_months` | Integer |
| `previous_orders` | Integer |
| `previous_failures` | Integer |
| `previous_late_deliveries` | Integer |
| `preferred_delivery_time` | Categorical |
| `address_type` | Categorical |
| `previous_address_issues` | Integer |

### `4_driver_vehicle.csv`
Driver and vehicle attributes as at each delivery attempt (point-in-time).  
Rows: 8,779

| Column | Description |
|---|---|
| `delivery_id` | String |
| `driver_id` | String |
| `vehicle_id` | String |
| `driver_experience_months` | Integer |
| `driver_deliveries` | Integer |
| `driver_late_rate` | Numeric |
| `driver_failed_rate` | Numeric |
| `vehicle_type` | Categorical |
| `vehicle_capacity_kg` | Integer |
| `vehicle_load_kg` | Integer |

### `5_operational_time.csv`
Calendar, peak-period and route-load context per delivery attempt.  
Rows: 8,779

| Column | Description |
|---|---|
| `delivery_id` | String |
| `order_id` | String |
| `day_of_week` | Categorical |
| `month` | Integer |
| `public_holiday` | Integer |
| `peak_period` | Integer |
| `orders_on_route` | Integer |
| `orders_per_driver` | Integer |
| `warehouse_processing_time_minutes` | Numeric |

### `6_data_quality_reference.csv`
Record provenance, missingness explanations, cancellation and return reasons.  
Rows: 8,951

| Column | Description |
|---|---|
| `order_id` | String |
| `delivery_id` | String |
| `record_timestamp` | Datetime |
| `data_source` | Categorical |
| `missing_reason` | Categorical |
| `cancellation_reason` | Categorical |
| `return_reason` | Categorical |

## Data quality notes

This is an extract from live operational systems and has **not** been cleaned. Expect:

- Missing values in optional / conditionally-populated fields
- Inconsistent casing and stray whitespace in some free-text and categorical fields
- A small number of duplicate records
- Occasional out-of-range or implausible values from data-capture errors
- Some date fields captured in inconsistent formats

**Target:** `late_delivery` in `1_orders_deliveries.csv` (1 = delivered after the promised time, or never successfully delivered). `repeat_delivery` is a secondary target.

**Point-in-time guarantee — this was the specific request.** `previous_orders`, `previous_failures`, `previous_late_deliveries`, `previous_address_issues`, `driver_deliveries`, `driver_late_rate` and `driver_failed_rate` are all computed from records **strictly before** the delivery on that row. They do not include the current delivery or anything after it. That is why Tables 3 and 4 are keyed on `delivery_id` rather than on customer or driver — the values change from delivery to delivery.

**Leakage warning:** `actual_distance_km`, `actual_duration_minutes`, `delivery_date`, `delivery_status`, `delivery_outcome`, `delivery_duration_minutes`, `delivery_attempt` and the return reasons in Table 6 are all only known after the attempt.

**Known gaps:** GPS coordinates are missing on ~6% of deliveries, traffic on ~9% and weather on ~12% (third-party feeds started mid-history). `missing_reason` in Table 6 records why, where the source system captured it. Cancelled orders have no dispatch, delivery or attempt data by definition.

_Synthetic data supplied for the CAP182 capstone project. Not real client data._