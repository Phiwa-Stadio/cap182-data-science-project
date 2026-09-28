# Part B – Model 2: Random Forest

**Script:** `models/random-forest.py`

## Technique
Random Forest is used as the second model. It is an ensemble of decision trees and can capture non-linear relationships between order and logistics variables.

## Hyperparameters

| Parameter | Value |
|---|---|
| `n_estimators` | 300 |
| `max_depth` | 15 |
| `min_samples_split` | 5 |
| `min_samples_leaf` | 2 |
| `max_features` | `sqrt` |
| `class_weight` | `balanced` |
| `random_state` | 42 |
| `n_jobs` | -1 |

## Modelling pipeline
Numerical variables are median-imputed. Categorical variables are imputed using the most frequent value and one-hot encoded. Scaling is not required for Random Forest.

The same 80/20 chronological split as Model 1 is used.

## Evaluation
Accuracy, precision, recall, F1-score and ROC-AUC.

## Run

```bash
python models/random-forest.py
```

## Output
Results are written to `models/artifacts/model2/`.
