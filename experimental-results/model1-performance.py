from pathlib import Path
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    balanced_accuracy_score,
    matthews_corrcoef,
    classification_report,
)

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "models" / "artifacts" / "model1" / "predictions.csv"


def main() -> None:
    if not INPUT.exists():
        raise FileNotFoundError(
            f"Prediction file not found: {INPUT}. "
            "Run python models/logistic_regression.py first."
        )

    df = pd.read_csv(INPUT)
    y_true = df["actual_late"]
    y_pred = df["predicted_late"]
    y_prob = df["late_probability"]

    tn, fp, fn, tp = confusion_matrix(
        y_true, y_pred, labels=[0, 1]
    ).ravel()

    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall": recall_score(y_true, y_pred, zero_division=0),
        "f1": f1_score(y_true, y_pred, zero_division=0),
        "roc_auc": roc_auc_score(y_true, y_prob),
        "specificity": tn / (tn + fp) if (tn + fp) else 0.0,
        "balanced_accuracy": balanced_accuracy_score(y_true, y_pred),
        "mcc": matthews_corrcoef(y_true, y_pred),
    }

    print("\nModel 1 – Logistic Regression")
    print("=" * 40)
    for name, value in metrics.items():
        print(f"{name:20s}: {value:.4f}")

    print("\nConfusion matrix")
    print(f"TN={tn}, FP={fp}, FN={fn}, TP={tp}")

    print("\nClassification report")
    print(classification_report(y_true, y_pred, zero_division=0))


if __name__ == "__main__":
    main()
