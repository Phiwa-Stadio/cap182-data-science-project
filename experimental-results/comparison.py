from pathlib import Path
import json
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)
from statsmodels.stats.contingency_tables import mcnemar

ROOT = Path(__file__).resolve().parents[1]

PATHS = {
    "logistic": ROOT / "models" / "artifacts" / "model1" / "predictions.csv",
    "random_forest": ROOT / "models" / "artifacts" / "model2" / "predictions.csv",
}


def metric_row(df):
    return {
        "Accuracy": accuracy_score(df["actual_late"], df["predicted_late"]),
        "Precision": precision_score(df["actual_late"], df["predicted_late"], zero_division=0),
        "Recall": recall_score(df["actual_late"], df["predicted_late"], zero_division=0),
        "F1": f1_score(df["actual_late"], df["predicted_late"], zero_division=0),
        "ROC-AUC": roc_auc_score(df["actual_late"], df["late_probability"]),
    }


def main() -> None:
    for name, path in PATHS.items():
        if not path.exists():
            raise FileNotFoundError(
                f"Missing {name} prediction file: {path}. "
                "Run both model scripts first."
            )

    m1 = pd.read_csv(PATHS["logistic"])
    m2 = pd.read_csv(PATHS["random_forest"])

    # Ensure the paired observations refer to the same test orders.
    merged = m1.merge(
        m2,
        on="order_id",
        suffixes=("_m1", "_m2"),
        validate="one_to_one",
    )

    if not (merged["actual_late_m1"] == merged["actual_late_m2"]).all():
        raise ValueError("The two prediction files do not share the same actual labels.")

    results = pd.DataFrame(
        {
            "Logistic Regression": metric_row(
                merged.rename(
                    columns={
                        "actual_late_m1": "actual_late",
                        "predicted_late_m1": "predicted_late",
                        "late_probability_m1": "late_probability",
                    }
                )
            ),
            "Random Forest": metric_row(
                merged.rename(
                    columns={
                        "actual_late_m2": "actual_late",
                        "predicted_late_m2": "predicted_late",
                        "late_probability_m2": "late_probability",
                    }
                )
            ),
        }
    )

    print("\nModel comparison")
    print(results.round(4).to_string())

    # McNemar test on paired classifications.
    correct_m1 = (
        merged["predicted_late_m1"] == merged["actual_late_m1"]
    )
    correct_m2 = (
        merged["predicted_late_m2"] == merged["actual_late_m2"]
    )

    table = [
        [
            int((correct_m1 & correct_m2).sum()),
            int((correct_m1 & ~correct_m2).sum()),
        ],
        [
            int((~correct_m1 & correct_m2).sum()),
            int((~correct_m1 & ~correct_m2).sum()),
        ],
    ]

    test = mcnemar(table, exact=False, correction=True)

    print("\nMcNemar paired comparison")
    print(f"Model 1 correct / Model 2 wrong: {table[0][1]}")
    print(f"Model 1 wrong / Model 2 correct: {table[1][0]}")
    print(f"Chi-square statistic: {test.statistic:.4f}")
    print(f"p-value: {test.pvalue:.6f}")

    print("\nInterpretation guide:")
    print("- p < 0.05: statistically significant difference in paired classifications.")
    print("- p >= 0.05: no statistically significant difference detected by this test.")


if __name__ == "__main__":
    main()
