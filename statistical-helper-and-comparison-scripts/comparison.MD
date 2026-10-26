# Model Comparison

## Related script

`experimental-results/comparison.py`

The comparison script reads the saved predictions and metrics for both models and produces a common comparison table. It also performs a paired comparison of the two classifiers using McNemar's test when both prediction files are available.

## Comparison of results

Both models were evaluated on the same 19,294 test records.

| Metric | Logistic Regression | Random Forest |
|---|---:|---:|
| Accuracy | **0.5641** | **0.8218** |
| Precision | **0.0911** | **0.0654** |
| Recall | **0.8606** | **0.1783** |
| F1-score | **0.1637** | **0.0954** |
| ROC-AUC | **0.7020** | **0.5571** |

## Comparison

The models show different performance characteristics.

Logistic Regression has:
- higher recall;
- higher precision;
- higher F1-score; and
- higher ROC-AUC.

Random Forest has:
- higher overall accuracy.

For this problem, the difference in recall is important because the model is intended to identify orders that are at risk of late delivery. The Logistic Regression model identifies more of the actual late deliveries, but it also produces many false positives, as shown by its low precision.

The Random Forest produces higher accuracy, but its low recall means that many late orders are not identified.

This demonstrates why several metrics should be considered together rather than selecting a model based only on accuracy.

## Statistical method

McNemar's test is used because both models make predictions on the same test observations. The test compares the number of cases where:
- Model 1 is correct and Model 2 is wrong; versus
- Model 2 is correct and Model 1 is wrong.

The script reports the discordant counts and the McNemar p-value when the prediction files are available.

## How to run

Make sure both model scripts have been run first:

```bash
python models/logistic-regression.py
python models/random-forest.py
```

Then run:

```bash
python experimental-results/comparison.py
```

The script expects:

```text
models/artifacts/model1/predictions.csv
models/artifacts/model1/metrics.json
models/artifacts/model2/predictions.csv
models/artifacts/model2/metrics.json
```
