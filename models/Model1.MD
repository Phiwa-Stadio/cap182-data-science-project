# Part B – Model 1: Logistic Regression

**Script:** `models/logistic-regression.py`

## Technique
Logistic Regression is used as the baseline binary classification model.

## Hyperparameters

| Parameter | Value |
|---|---|
| `C` | 1.0 |
| `solver` | `liblinear` |
| `max_iter` | 1000 |
| `class_weight` | `balanced` |
| `random_state` | 42 |

## Modelling pipeline
Numerical variables are median-imputed and standardised. Categorical variables are imputed using the most frequent value and one-hot encoded.

The model uses an 80/20 chronological split, with earlier orders used for training and later orders used for testing.

## Evaluation
Accuracy, precision, recall, F1-score and ROC-AUC.

## Run

```bash
python models/logistic-regression.py
```

## Output
Results are written to `models/artifacts/model1/`.
