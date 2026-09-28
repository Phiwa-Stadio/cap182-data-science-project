from pathlib import Path
import json
import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "datasets" / "processed" / "olist_model_ready.csv"
OUT = ROOT / "models" / "artifacts" / "model1"
OUT.mkdir(parents=True, exist_ok=True)

CAT = [
    "customer_state",
    "seller_state",
    "main_product_category",
    "main_payment_type",
]

NUM = [
    "seller_customer_same_state",
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
]


def main() -> None:
    if not DATA.exists():
        raise FileNotFoundError(
            "Run the preprocessing and feature engineering scripts first."
        )

    df = pd.read_csv(DATA, parse_dates=["order_purchase_timestamp"])
    df = df.sort_values("order_purchase_timestamp").reset_index(drop=True)

    cut = int(len(df) * 0.80)
    train, test = df.iloc[:cut], df.iloc[cut:]

    X_train, y_train = train[CAT + NUM], train["late_delivery"]
    X_test, y_test = test[CAT + NUM], test["late_delivery"]

    prep = ColumnTransformer(
        [
            (
                "num",
                Pipeline([
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scale", StandardScaler()),
                ]),
                NUM,
            ),
            (
                "cat",
                Pipeline([
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("onehot", OneHotEncoder(handle_unknown="ignore")),
                ]),
                CAT,
            ),
        ]
    )

    model = Pipeline(
        [
            ("preprocessor", prep),
            ("classifier", LogisticRegression(
                C=1.0,
                solver="liblinear",
                max_iter=1000,
                class_weight="balanced",
                random_state=42,
            )),
        ]
    )

    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    prob = model.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": accuracy_score(y_test, pred),
        "precision": precision_score(y_test, pred, zero_division=0),
        "recall": recall_score(y_test, pred, zero_division=0),
        "f1": f1_score(y_test, pred, zero_division=0),
        "roc_auc": roc_auc_score(y_test, prob),
        "train_rows": len(train),
        "test_rows": len(test),
    }

    (OUT / "metrics.json").write_text(
        json.dumps(metrics, indent=2),
        encoding="utf-8",
    )

    pd.DataFrame({
        "order_id": test["order_id"],
        "actual_late": y_test,
        "predicted_late": pred,
        "late_probability": prob,
    }).to_csv(OUT / "predictions.csv", index=False)

    joblib.dump(model, OUT / "logistic_regression.joblib")

    print("Model 1 – Logistic Regression")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
