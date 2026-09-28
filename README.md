# Data Science Project

## Project Overview

This repository contains the code, data, models, experiments and results for the data science project.

The project is organised into separate stages of the data science workflow so that data preparation, feature engineering, modelling and evaluation remain easy to manage and reproduce.

## Repository Structure

```text
.
├── datasets/
│   └── README.md
│   └── STADIOalot-data-request.pdf
├── experimental-results/
│   └── README.md
├── experimental-setup/
│   └── README.md
├── models/
│   └── logistic_regression.py
│   └── random_forest.py
│   └── README.md
├── literature-review/
│   └── README.md
│   └── literature-review-and-dataset.pdf
├── statistical-helper-and-comparison-scripts/
│   └── README.md
├── statistical-helper-and-comparisons/
│   └── README.md
├── visualisation-scripts/
│   └── README.md
├── LICENSE
└── README.md

```

##### *Client STADIOalot : E-COOMERCE and LOGISTICS*

## Part A : Motivation

E-commerce is a growing industry where getting orders to customers efficiently and reliably is essential. For a business operating at STADIOalot’s scale, small delivery inefficiencies can quickly become significant costs, with around **4.1 million active customers and 58 million orders per year**.

However, STADIOalot’s delivery performance is declining. On-time delivery has dropped from **93% to 88%**, while failed or repeat delivery attempts have increased from **4.1% to 6.7%**. These issues increase operating costs and can negatively affect the customer experience.

Addressing this issue is important because failed deliveries require additional driver time, fuel and vehicle resources, while STADIOalot operates on a relatively thin **1.9% operating margin**. Data science methods may assist by analysing historical delivery data to predict which orders are more likely to be delayed or require a repeat delivery attempt, allowing potential problems to be identified earlier.

Therefore, this study seeks to generate evidence that may support **the prediction of delivery risk and better routing, scheduling and delivery decisions**, with the potential to reduce failed deliveries, lower delivery costs and improve the customer experience.



## Part B: Problem Statement

Despite STADIOalot’s growing number of late and repeat deliveries, it is still unclear whether these delivery problems can be predicted before they happen. Therefore, this study aims to determine whether historical delivery and logistics data can be used to predict which orders are at higher risk of being delayed or requiring another delivery attempt, helping STADIOalot make better delivery planning decisions.

## Part E: RAAIDD Log

This RAAIDD log identifies the key risks, actions, assumptions, issues, decisions and dependencies that may affect the successful completion of this project.

# RAAIDD Log

| **RAAIDD** | **Description** |
|---|---|
| **Risks** | **Unexpected possibilities that could compromise successful completion of the project.**<br><br>• Missing, incomplete or inconsistent delivery data may affect model performance.<br>• There may be too few late or failed deliveries to build a reliable predictive model.<br>• Data leakage may occur if information only known after delivery is used as a predictor.<br>• Customer, driver or location data may require anonymisation or restricted access. |
| **Actions** | **Tasks to be done throughout the project's lifecycle.**<br><br>• Obtain the required historical delivery and logistics data.<br>• Assess data quality and identify missing or inconsistent information.<br>• Clean the data and create relevant features.<br>• Develop and evaluate predictive models.<br>• Compare model performance and identify important factors affecting delivery risk.<br>• Document findings and recommendations. |
| **Assumptions** | **Conditions that are assumed to be true, but are currently unproven.**<br><br>• Sufficient historical delivery data will be available.<br>• Delivery outcomes and timestamps are recorded reliably.<br>• Historical delivery patterns contain useful information for predicting future delivery outcomes.<br>• The required data can be provided in an anonymised form. |
| **Issues** | **Problems that transpire throughout the project's lifecycle.**<br><br>• Important variables may be missing or inconsistently recorded.<br>• Some requested data may not be available from STADIOalot.<br>• Initial models may not achieve useful predictive performance. |
| **Decisions** | **Choices that are made throughout the project.**<br><br>• Define what constitutes a late or failed delivery.<br>• Select the primary prediction target.<br>• Determine which variables are appropriate for modelling.<br>• Select the most suitable modelling and evaluation approach based on the available data. |
| **Dependencies** | **Relationships between actions that indicate the chronology of completion.**<br><br>Data access must be completed before data profiling can begin. Data preprocessing depends on the results of the data profiling, while feature extraction depends on having sufficiently clean data. Model development depends on the completed feature dataset, and the final recommendations depend on model evaluation and analysis. |

# SS2
## Part B:
[Preprocessing](experimental-setup/preprocessing.MD)

[Feature Engineering](experimental-setup/feature-engineering.MD)

[Model 1 – Logistic Regression](models/model1.MD)

[Model 2 – Random Forest](models/model2.MD)

## Part C:

### Model Performance

- [Model 1 Performance](experimental-results/model1-performance.MD)
- [Model 2 Performance](experimental-results/model2-performance.MD)
- [Model Comparison](experimental-results/comparison.MD)

## Model performance

The two models were applied to the Olist public dataset using the same chronological 80/20 train-test split. The test set contained **19,294 records**.

### Model 1 – Logistic Regression

Model 1 achieved an accuracy of **56.41%**, precision of **9.11%**, recall of **86.06%**, F1-score of **16.37%**, and ROC-AUC of **0.7020**.

The model therefore identified a high proportion of the actual late deliveries, but its low precision means that many orders predicted as late were not actually late.

See [Model1Performance.MD](experimental-results/model1-performance.MD).

### Model 2 – Random Forest

Model 2 achieved an accuracy of **82.18%**, precision of **6.54%**, recall of **17.83%**, F1-score of **9.54%**, and ROC-AUC of **0.5571**.

The higher accuracy is accompanied by much lower recall, meaning that a substantial number of late deliveries were not identified.

See [Model2Performance.MD](experimental-results/model2-performance.MD).

### Comparison

| Metric | Logistic Regression | Random Forest |
|---|---:|---:|
| Accuracy | 0.5641 | 0.8218 |
| Precision | 0.0911 | 0.0654 |
| Recall | 0.8606 | 0.1783 |
| F1-score | 0.1637 | 0.0954 |
| ROC-AUC | 0.7020 | 0.5571 |

The models show a clear trade-off. Logistic Regression has higher recall, precision, F1-score and ROC-AUC, while Random Forest has higher overall accuracy.

Because the project is concerned with identifying orders at risk of late delivery, recall, F1-score and ROC-AUC should be considered alongside accuracy. The results also suggest that further work is needed to address the class imbalance and improve the predictive performance.

See [Comparison.MD](experimental-results/comparison.MD).

### Statistical comparison

McNemar's test is included in `experimental-results/comparison.py` to compare the paired predictions made by the two models on the same test orders. This provides a statistical check of whether the models differ in their classification decisions.

### Run performance calculations

```bash
python3 experimental-results/model1_performance.py
python3 experimental-results/model2_performance.py
python3 experimental-results/comparison.py
```
