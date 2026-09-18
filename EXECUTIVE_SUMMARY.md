# NBFC Loan Portfolio Risk & Analytics
## Executive Summary

### 1. Project Overview

This project develops an end-to-end analytics and risk monitoring solution for an NBFC loan portfolio.

The solution combines:

- Python-based data processing and feature engineering
- Rule-based customer risk scoring
- Machine Learning for default probability prediction
- SQL-based portfolio and cohort analysis
- SQLite database management
- FastAPI REST APIs
- Streamlit interactive dashboard
- Collections prioritization

The objective is to transform loan-level data into actionable portfolio risk insights and provide a reusable analytics system for monitoring credit risk, delinquency, portfolio concentration, and collections priorities.

---

## 2. Portfolio Snapshot

The analytical dataset contains **8,000 loan records** representing **8,000 unique customers**.

| KPI | Value |
|---|---:|
| Total Loans | 8,000 |
| Total Customers | 8,000 |
| Total Portfolio Exposure | ₹417.04 Cr |
| Total Defaults | 998 |
| Default Rate | 12.47% |
| Average Loan Amount | ₹5.21 Lakh |
| Average Monthly Income | ₹56,390 |
| Average EMI | ₹12,541 |
| Average Interest Rate | 13.08% |
| 90+ DPD Exposure | ₹50.03 Cr |

Data quality validation identified:

- 0 missing values
- 0 duplicate records
- 0 duplicate customer IDs
- 0 invalid default/DPD relationships
- 0 unaffordable loans
- 0 loans with EMI-to-income above 50%

---

## 3. Feature Engineering

Additional analytical features were created to represent borrower affordability and loan exposure.

### EMI-to-Income Ratio

```text
EMI-to-Income = EMI / Monthly Income × 100

This metric represents the proportion of monthly income committed to the loan EMI.

Loan-to-Annual-Income Ratio
Loan-to-Annual-Income =
Loan Amount / (Monthly Income × 12)

This metric measures loan exposure relative to the borrower's annual income.

These features were used in both portfolio risk analysis and Machine Learning models.

4. Portfolio Risk Analysis

The portfolio was analyzed across multiple dimensions.

Product Risk

The portfolio contains:

Business Loan
Personal Loan
Vehicle Loan
Gold Loan
Home Loan

Observed default rates were compared across products together with loan counts and portfolio exposure.

Business Loan recorded a 15.46% default rate, while Home Loan represented the largest exposure at approximately ₹249.55 Cr.

These metrics provide visibility into product-level credit performance and portfolio concentration.

5. Credit Score Risk

Customers were grouped into credit score bands:

Poor
Fair
Good
Very Good
Excellent

The observed portfolio results were:

Credit Band	Customers	Defaults	Default Rate
Poor	1,078	203	18.83%
Fair	2,628	330	12.56%
Good	2,309	243	10.52%
Very Good	1,241	132	10.64%
Excellent	744	90	12.10%

The analysis shows differences in observed default rates across credit score segments and allows the portfolio team to examine credit-quality concentration.

6. Rule-Based Customer Risk Scoring

A rule-based risk score was developed using three dimensions:

Credit Risk — 40 Points

Points are assigned according to the customer's credit score.

EMI Burden — 35 Points

Points are assigned based on the EMI-to-income ratio.

Loan-to-Income Risk — 25 Points

Points are assigned based on the loan-to-annual-income ratio.

Total Risk Score =
Credit Risk Score
+ EMI Risk Score
+ Loan-to-Income Risk Score

Customers were classified into:

0–33    → Low Risk
34–66   → Medium Risk
67–100  → High Risk
Observed Risk Segment Results
Risk Category	Customers	Default Rate	Exposure
Low Risk	3,571	10.45%	₹96.76 Cr
Medium Risk	3,824	13.76%	₹236.19 Cr
High Risk	605	16.36%	₹84.09 Cr

The segmentation provides a rule-based framework for organizing customers according to predefined credit, affordability, and exposure thresholds.

7. Machine Learning Default Prediction

Two classification models were developed:

Logistic Regression
Random Forest

The models use borrower, loan, employment, geographic, affordability, and exposure-related features.

days_past_due was excluded from the predictive feature set to avoid using a post-disbursement delinquency indicator as a predictor of default.

Model Evaluation
Model	ROC-AUC
Logistic Regression	0.583
Random Forest	0.590

Random Forest evaluation on the held-out test set produced:

Precision for default class: 0.185
Recall for default class: 0.345

The models provide probability estimates that are used in the application for ranking loans by predicted default probability.

The current model performance should be interpreted as a baseline predictive model on the synthetic dataset rather than as a production-ready credit underwriting model.

8. ML Feature Importance

Random Forest feature importance analysis identified the following variables among the leading model features:

Feature	Importance
Credit Score	0.1815
EMI-to-Income	0.1450
Interest Rate	0.1073
Loan Amount	0.1049
Loan-to-Annual-Income	0.0982
Monthly Income	0.0978
Age	0.0706
Tenure Months	0.0407
Employment Type — Salaried	0.0372
Employment Type — Business Owner	0.0194

These importance values describe the variables that contributed most to the Random Forest's predictions in this dataset. They should not be interpreted as causal effects.

9. Geographic Risk Analysis

Default rates and portfolio exposure were analyzed across:

Mumbai
Delhi
Bengaluru
Hyderabad
Chennai
Pune
Ahmedabad
Jaipur
Kolkata
Lucknow

This enables geographic comparison of observed portfolio performance and helps identify differences in exposure and default concentration across locations.

10. Vintage / Cohort Analysis

Loan performance was analyzed by disbursement quarter.

The portfolio was grouped into quarterly cohorts from:

2023-Q1 → 2024-Q4

For each cohort, the system calculates:

Number of loans
Cohort exposure
Number of defaults
Cohort default rate

This provides a time-based view of portfolio performance and allows different loan vintages to be compared.

11. Delinquency and Collections Analysis

Loans were categorized using Days Past Due (DPD):

Current
1–30 DPD
31–60 DPD
61–89 DPD
90+ DPD

The portfolio contains approximately ₹50.03 Cr of exposure in the 90+ DPD category.

A collections-priority query was also developed for active overdue loans with 1–89 DPD.

Collections records include:

Customer ID
Product
City
Loan Amount
DPD
Credit Score
EMI-to-Income
ML Default Probability

The operational priority ordering is based on:

Higher DPD
↓
Higher Loan Amount
↓
Lower Credit Score

The ML default probability is displayed alongside these operational indicators to provide an additional risk signal.

12. SQL Analytics Layer

SQLite is used as the application database.

The SQL layer supports:

Portfolio KPI analysis
Product risk analysis
Credit score band analysis
City risk analysis
Vintage/cohort analysis
Vintage by product
Collections priority analysis
Risk-ranked loan queries

The database contains the processed loan portfolio together with ML-predicted default probabilities.

The original MySQL analysis layer is also retained separately for portfolio SQL analysis and validation.

13. FastAPI Backend

A REST API was developed using FastAPI.

The backend provides endpoints for:

/api/portfolio/summary
/api/portfolio/product-risk
/api/portfolio/credit-risk
/api/portfolio/city-risk
/api/portfolio/vintage
/api/risk/high-risk-loans
/api/collections/priority

The API supports portfolio filters for:

Product
City
Credit Band

This allows the frontend to request dynamically filtered portfolio analytics.

14. Streamlit Dashboard

A Streamlit dashboard was developed as the user-facing analytics application.

Dashboard Sections
Portfolio Overview

Displays:

Total Loans
Total Exposure
Total Defaults
Default Rate
90+ DPD Exposure
Product-wise Risk

Displays product-level default rates, exposure, loans, and defaults.

Credit Score Risk

Displays default rates and exposure across credit score bands.

Geographic Risk

Displays city-level default rates and exposure.

Vintage / Cohort Analysis

Displays quarterly portfolio performance.

ML-Predicted High-Risk Loans

Displays the top loans ranked by predicted default probability.

Machine Learning Evaluation

Displays:

Logistic Regression ROC-AUC
Random Forest ROC-AUC
Precision
Recall
Confusion Matrix
Feature Importance
Collections Priority

Displays overdue loans together with operational and ML-based risk indicators.

15. System Architecture
                 8,000 Loan Records
                         ↓
              Python Data Processing
                         ↓
              Feature Engineering
                         ↓
            ┌────────────┴────────────┐
            ↓                         ↓
    Rule-Based Risk Score       ML Prediction
                                      ↓
                           ┌──────────┴──────────┐
                           ↓                     ↓
                  Logistic Regression     Random Forest
                           ↓                     ↓
                           └──────────┬──────────┘
                                      ↓
                              Model Evaluation
                                      ↓
                              SQLite Database
                                      ↓
                                FastAPI API
                                      ↓
                                  HTTP/REST
                                      ↓
                              Streamlit Dashboard
                                      ↓
                         Portfolio Risk Monitoring
16. Key Business Insights

The analysis provides the following portfolio-level observations:

The portfolio contains ₹417.04 Cr of total loan exposure across 8,000 loans.
The observed portfolio default rate is 12.47%, with 998 recorded defaults.
Home Loan represents the largest exposure category at approximately ₹249.55 Cr.
Business Loan has an observed default rate of 15.46% in the dataset.
The 90+ DPD segment represents approximately ₹50.03 Cr of exposure.
Rule-based risk segments show different observed default rates:
Low Risk: 10.45%
Medium Risk: 13.76%
High Risk: 16.36%
Credit score, EMI-to-income ratio, interest rate, loan amount, and loan-to-annual-income were among the leading Random Forest features in this dataset.
The ML prediction layer provides a probability-based ranking that can be combined with DPD and loan exposure for collections analysis.
17. Technology Stack
Programming
Python
Data Analysis
Pandas
NumPy
Matplotlib
Machine Learning
scikit-learn
Logistic Regression
Random Forest
StandardScaler
OneHotEncoder
Database / SQL
SQLite
MySQL
Backend
FastAPI
Uvicorn
Frontend
Streamlit
BI
Power BI
18. Limitations

This project uses a synthetic loan portfolio created for analytical and demonstration purposes.

Therefore:

Model performance should not be interpreted as production credit-model performance.
Feature importance indicates model contribution, not causality.
Rule-based thresholds are predefined analytical rules.
Default predictions are not intended for real-world lending decisions without validation on actual historical lending data.
Production deployment would require model validation, monitoring, calibration, explainability, governance, and appropriate credit-risk controls.
19. Conclusion

The project demonstrates an end-to-end NBFC portfolio risk analytics workflow, beginning with loan-level data processing and feature engineering and extending through rule-based risk segmentation, machine learning prediction, SQL analytics, REST APIs, and an interactive Streamlit dashboard.

The resulting system provides a unified framework for:

Monitoring portfolio KPIs
Comparing product and geographic risk
Analyzing credit-quality segments
Studying loan vintages
Ranking predicted high-risk loans
Supporting collections prioritization

The architecture is designed to demonstrate how Python, SQL, Machine Learning, APIs, and dashboarding can be integrated into a single financial analytics application.