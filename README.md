# NBFC Loan Portfolio Risk & Analytics

## Project Overview

This project is an end-to-end **NBFC loan portfolio, credit risk, machine learning, collections, and portfolio analytics platform** built using **Python, SQL, scikit-learn, FastAPI, SQLite, Streamlit, and Power BI**.

The project uses an **8,000-record synthetic NBFC loan portfolio** and combines portfolio analytics, transparent rule-based risk segmentation, ML-based default prediction, SQL business analysis, collections prioritization, API-driven analytics, loan origination, and a live loan simulation workflow.

> **Important:** The dataset is synthetic and is intended for analytics, modeling, and application demonstration. ML results should not be interpreted as production credit-performance estimates.

---

## Business Problem

NBFCs need to continuously monitor loan portfolios to understand exposure, credit quality, affordability, delinquency, concentration, and collection priorities.

This project focuses on questions such as:

- Which loan products have higher observed default rates?
- How does credit quality relate to observed defaults?
- Which borrowers have higher affordability or loan-to-income exposure?
- Which employment and city segments show different observed risk levels?
- How much exposure is associated with 90+ DPD?
- Which accounts should collections teams prioritize?
- How does portfolio performance vary by origination vintage?
- Can ML models identify patterns associated with default?
- Can these analytics be exposed through a reusable API and business-facing dashboard?

---

## Objectives

1. Analyze overall portfolio exposure and default performance.
2. Identify risk patterns across products and borrower segments.
3. Analyze credit score, EMI burden, and loan-to-income exposure.
4. Study delinquency using Days Past Due (DPD).
5. Build a transparent rule-based customer risk segmentation framework.
6. Build Logistic Regression and Random Forest default prediction models.
7. Evaluate models using ROC-AUC, precision, recall, confusion matrix, and feature importance.
8. Store ML-enriched portfolio data in SQLite for application analytics.
9. Expose portfolio, risk, vintage, collections, and loan workflows through FastAPI.
10. Build an interactive Streamlit application that consumes the API over HTTP.
11. Support collections prioritization using DPD, exposure, credit score, and ML probability.
12. Provide loan origination and new-loan simulation capabilities for application demonstration.
13. Retain the original MySQL and Power BI analytical layers as supporting deliverables.

---

## Dataset

The project uses a synthetic NBFC loan portfolio containing:

- **8,000** loan/customer records
- Customer demographics
- Employment information
- Monthly and annual income information
- Credit score
- Loan amount
- Loan type
- Tenure
- Interest rate
- EMI
- Days Past Due (DPD)
- Default flag
- Application/disbursement date

### Data Quality

The final analytical dataset passed the following checks:

- **8,000** total records
- **8,000** unique customers
- **0** missing values
- **0** duplicate customer IDs
- **0** invalid default/DPD relationships
- **0** unaffordable loans
- **0** records with EMI-to-income above 50%

---

## Tools & Technologies

- Python
- Pandas
- NumPy
- Matplotlib
- scikit-learn
- Logistic Regression
- Random Forest
- SQLite
- MySQL
- FastAPI
- Uvicorn
- Streamlit
- Power BI
- JupyterLab
- Git & GitHub

---

## Project Architecture

```text
                    8,000 Synthetic Loans
                             |
                             v
                 Python / Pandas Processing
                             |
                  +----------+----------+
                  |                     |
                  v                     v
          Feature Engineering    Rule-Based Risk
                                      Scoring
                  |                     |
                  +----------+----------+
                             |
                             v
                    ML Risk Prediction
                  +----------+----------+
                  |                     |
                  v                     v
        Logistic Regression      Random Forest
                  |                     |
                  +----------+----------+
                             |
                             v
              ROC-AUC / Precision / Recall /
              Confusion Matrix / Importance
                             |
                             v
                       SQLite Database
                             |
             +---------------+----------------+
             |               |                |
             v               v                v
       Portfolio Risk   Vintage/Cohort   Collections
             |               |                |
             +---------------+----------------+
                             |
                             v
                         FastAPI
                             |
                         HTTP/JSON
                             |
                             v
                       Streamlit UI
                             |
                             v
                  Business Risk Insights
```

---

## Project Workflow

```text
Synthetic Dataset
       ↓
Data Quality Validation
       ↓
Feature Engineering
       ↓
Portfolio KPI Analysis
       ↓
Rule-Based Risk Scoring
       ↓
Machine Learning
   ├── Logistic Regression
   └── Random Forest
       ↓
Model Evaluation
   ├── ROC-AUC
   ├── Precision / Recall
   ├── Confusion Matrix
   └── Feature Importance
       ↓
ML-Enriched Portfolio
       ↓
SQLite Analytics Layer
       ↓
FastAPI REST API
       ↓ HTTP / JSON
Streamlit Application
       ↓
Portfolio Risk + Collections + Loan Workflows
       ↓
Power BI Analytical Dashboard
```

---

## Portfolio KPIs

| KPI | Value |
|---|---:|
| Total Loans | 8,000 |
| Total Portfolio Exposure | ₹417.04 Cr |
| Average Loan Amount | ₹5.21 Lakh |
| Average Monthly Income | ₹56,390 |
| Average EMI | ₹12,541 |
| Total Defaults | 998 |
| Default Rate | 12.47% |
| 90+ DPD Exposure | ₹50.03 Cr |
| High-Risk Customers | 605 |
| High-Risk Exposure | ₹84.09 Cr |
| High-Risk Default Rate | 16.36% |
| High-Risk Default Exposure | ₹11.55 Cr |

---

## Feature Engineering

Two important analytical features are created:

### EMI-to-Income Ratio

```text
emi_to_income = monthly_emi / monthly_income
```

This represents the share of monthly income committed to EMI payments.

### Loan-to-Annual-Income Ratio

```text
loan_to_annual_income = loan_amount / annual_income
```

This normalizes loan exposure against annual income.

These features are used in portfolio analysis and ML modeling.

---

## Risk Analysis

### 1. Loan Product Risk

The portfolio contains:

- Personal Loan
- Home Loan
- Business Loan
- Vehicle Loan
- Gold Loan

Observed default rates:

| Product | Default Rate |
|---|---:|
| Business Loan | 15.46% |
| Personal Loan | 12.42% |
| Vehicle Loan | 11.96% |
| Gold Loan | 11.01% |
| Home Loan | 10.95% |

Home Loans represent the largest share of total portfolio exposure.

> These are observed rates within the synthetic portfolio, not claims about real-world borrower populations.

### 2. Credit Risk

Customers are grouped into:

- Poor
- Fair
- Good
- Very Good
- Excellent

The analysis compares customer volume, exposure, defaults, default rate, and default exposure across credit bands.

### 3. EMI Burden

Customers are segmented using the EMI-to-income ratio:

- Low
- Moderate
- High
- Very High

The project uses this segmentation to analyze affordability-related portfolio patterns.

### 4. Loan-to-Income Analysis

Loan-to-annual-income ratios are grouped into:

- <0.5x
- 0.5–1x
- 1–2x
- 2–3x
- 3x+

### 5. Employment Risk

The portfolio is analyzed across:

- Salaried
- Self-employed
- Business Owner

Observed default rates:

| Employment Type | Default Rate |
|---|---:|
| Business Owner | 15.75% |
| Self-employed | 13.64% |
| Salaried | 10.94% |

### 6. Geographic Risk

Default rates and exposure are compared across:

- Mumbai
- Delhi
- Bengaluru
- Hyderabad
- Chennai
- Pune
- Ahmedabad
- Jaipur
- Kolkata
- Lucknow

### 7. Delinquency / DPD Analysis

Customers are categorized using Days Past Due:

- Current
- 1–30 DPD
- 31–60 DPD
- 61–89 DPD
- 90+ DPD

The portfolio contains approximately **₹50.03 Cr** of exposure in the 90+ DPD category.

### 8. Vintage / Cohort Analysis

Quarterly origination vintages are analyzed using:

- Loan count
- Exposure
- Default count
- Default rate

This adds a time-based portfolio view alongside product, credit, employment, and geography analysis.

---

## Customer Risk Scoring

A transparent rule-based score was developed using three dimensions.

### Credit Score Component — 40 Points

| Credit Band | Points |
|---|---:|
| Poor | 40 |
| Fair | 30 |
| Good | 20 |
| Very Good | 10 |
| Excellent | 0 |

### EMI Burden Component — 35 Points

| EMI Band | Points |
|---|---:|
| Low | 0 |
| Moderate | 10 |
| High | 25 |
| Very High | 35 |

### Loan-to-Income Component — 25 Points

| LTI Band | Points |
|---|---:|
| <0.5x | 0 |
| 0.5–1x | 5 |
| 1–2x | 10 |
| 2–3x | 20 |
| 3x+ | 25 |

### Total Risk Score

```text
Risk Score = Credit Risk Score
           + EMI Risk Score
           + LTI Risk Score
```

Customers are classified into:

```text
0–33   → Low Risk
34–66  → Medium Risk
67–100 → High Risk
```

### Observed Risk Segment Results

| Risk Category | Customers | Default Rate | Exposure | Default Exposure |
|---|---:|---:|---:|---:|
| Low Risk | 3,571 | 10.45% | ₹96.76 Cr | ₹9.44 Cr |
| Medium Risk | 3,824 | 13.76% | ₹236.19 Cr | ₹29.04 Cr |
| High Risk | 605 | 16.36% | ₹84.09 Cr | ₹11.55 Cr |

> This is a transparent analytical segmentation framework, not a calibrated probability-of-default scorecard.

---

## Machine Learning Default Prediction

Two classification models are implemented:

- Logistic Regression
- Random Forest

The feature set uses borrower, loan, employment, geographic, affordability, and exposure-related variables.

`days_past_due` is excluded from the predictive feature set to avoid using a post-disbursement delinquency indicator as a predictor of default.

### Model Results

| Model | ROC-AUC |
|---|---:|
| Logistic Regression | 0.583 |
| Random Forest | 0.590 |

Random Forest test-set metrics:

- Precision for default class: **0.185**
- Recall for default class: **0.345**

These are baseline results on synthetic data rather than production credit-model validation.

### Top ML Features

| Feature | Importance |
|---|---:|
| Credit Score | 0.1815 |
| EMI-to-Income | 0.1450 |
| Interest Rate | 0.1073 |
| Loan Amount | 0.1049 |
| Loan-to-Annual-Income | 0.0982 |
| Monthly Income | 0.0978 |
| Age | 0.0706 |
| Tenure Months | 0.0407 |
| Employment Type — Salaried | 0.0372 |
| Employment Type — Business Owner | 0.0194 |

Feature importance describes model contribution and should not be interpreted as causality.

The trained Random Forest pipeline is persisted at:

```text
models/rf_risk_pipeline.joblib
```

---

## SQLite Analytics Layer

SQLite is used as the application database for the ML-enriched loan portfolio.

Database:

```text
Data/nbfc_risk_analytics.db
```

Business analytics include:

- Portfolio KPIs
- Product risk
- Credit-band risk
- City risk
- Vintage/cohort analysis
- High-risk loan queries
- Collections prioritization

The original MySQL layer is retained for SQL analysis and reusable portfolio/risk views.

---

## FastAPI Backend

FastAPI exposes the analytics and operational workflows through REST endpoints.

### Portfolio endpoints

```text
GET /api/portfolio/summary
GET /api/portfolio/product-risk
GET /api/portfolio/credit-risk
GET /api/portfolio/city-risk
GET /api/portfolio/vintage
```

### Risk and collections endpoints

```text
GET /api/risk/high-risk-loans
GET /api/collections/priority
```

### Operational endpoints

```text
POST /api/pipeline/simulate-new-loans
POST /api/loans
```

Portfolio analytics support filters for:

- Product
- City
- Credit Band

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

---

## Streamlit Application

The Streamlit application is the primary interactive frontend and communicates with FastAPI over HTTP.

### Application Pages

#### 1. Overview

- Portfolio KPIs
- Product risk
- Credit risk
- City analytics

#### 2. Loan Origination

- Submit a new loan through the FastAPI backend
- Calculate/assign the relevant risk information

#### 3. Portfolio Risk

- Filtered portfolio analytics
- Product risk
- Credit-band risk
- City risk

#### 4. ML Risk

- ML model metrics
- Confusion matrix
- Feature importance
- High-risk loan view

#### 5. Vintage

- Quarterly cohort analysis
- Exposure and default trends

#### 6. Collections

- Priority overdue accounts
- DPD and exposure indicators
- Credit and ML risk signals

#### 7. Loan Simulator

- Simulate new-loan scenarios
- Send simulated portfolio data through the API pipeline

#### 8. About

- Project information
- Technology stack
- Architecture
- Project limitations

---

## Collections Priority

The collections module focuses on active overdue loans with **1–89 DPD**.

Displayed indicators include:

- Customer ID
- Product
- City
- Loan Amount
- DPD
- Credit Score
- EMI-to-Income
- ML Default Probability

The operational ordering uses:

```text
Higher DPD
↓
Higher Loan Amount
↓
Lower Credit Score
```

ML default probability is displayed as an additional predictive risk signal.

> This is an analytical prioritization workflow for the project, not a production collections policy.

---

## Loan Origination & Simulation

The API-driven application includes two workflows beyond static reporting:

### Loan Origination

```text
Streamlit Loan Form
        ↓
POST /api/loans
        ↓
FastAPI Validation / Processing
        ↓
Loan Response
```

### New Loan Simulation

```text
Simulation Input
        ↓
POST /api/pipeline/simulate-new-loans
        ↓
Analytics Pipeline
        ↓
Risk / Portfolio Output
```

These workflows demonstrate how the analytics layer can be extended from reporting into application-style functionality.

---

## SQL Analysis

MySQL was used for:

- Data validation
- Portfolio KPI calculations
- Product risk analysis
- Credit risk analysis
- EMI burden analysis
- Employment risk analysis
- City risk analysis
- DPD analysis
- Customer risk segmentation
- Portfolio concentration analysis
- Risk priority analysis
- KPI reconciliation

Reusable SQL views include:

- Customer Risk Scores
- Portfolio KPIs
- Product Risk Summary
- Employment Risk Summary
- DPD Risk Summary
- City Risk Summary

SQLite provides the application-facing analytical database.

---

## Power BI Dashboard

The Power BI report is retained as an additional BI deliverable.

### Page 1 — Executive Portfolio Overview

Includes:

- Total Customers
- Portfolio Exposure
- Default Rate
- Default Exposure
- 90+ DPD Exposure
- Exposure by Loan Type
- Default Rate by Loan Type
- Customer Risk Distribution
- DPD Analysis
- Employment Risk
- City Risk

### Page 2 — Risk Deep Dive & Customer Segmentation

Includes:

- Credit Risk Analysis
- EMI Burden Analysis
- Loan-to-Income Analysis
- Risk Category Exposure
- Default Exposure by Risk Category
- Customer Risk Distribution by Loan Type

The Power BI report is available as:

```text
NBFC_Loan_Portfolio_Risk_Analytics.pbix
```

---

## Notebook

The main notebook is:

```text
Notebooks/NBFC_Loan_Portfolio_Risk_Analytics.ipynb
```

It covers:

- Data loading
- Data quality checks
- Validation
- Derived metrics
- Feature engineering
- Portfolio KPIs
- Product analysis
- Credit risk
- EMI burden
- Loan-to-income analysis
- Employment analysis
- City analysis
- DPD analysis
- Rule-based risk scoring
- Segment analysis
- Visualizations
- Business insights
- Conclusion

---

## Project Structure

```text
NBFC PROJECT/
│
├── Data/
│   ├── loan_portfolio.csv
│   ├── loan_portfolio_with_ml.csv
│   ├── ml_model_metrics.csv
│   ├── ml_confusion_matrix.csv
│   ├── ml_feature_importance.csv
│   └── nbfc_risk_analytics.db
│
├── Notebooks/
│   └── NBFC_Loan_Portfolio_Risk_Analytics.ipynb
│
├── SQL/
│   ├── nbfc_risk_analysis.sql
│   ├── sql_additions.sql
│   └── sqlite_risk_analysis.sql
│
├── Screenshots/
│   ├── dashboard_page_1.png
│   └── dashboard_page_2.png
│
├── models/
│   └── rf_risk_pipeline.joblib
│
├── generate_data.py
├── ml_risk_model.py
├── live_loan_simulator.py
├── build_sqlite.py
├── api.py
├── app.py
├── generate_executive_summary.py
├── EXECUTIVE_SUMMARY.md
├── NBFC_Loan_Portfolio_Risk_Analytics.pbix
├── README.md
└── .gitignore
```

---

## How to Run

### 1. Open the project

```powershell
cd "C:\Users\KHUSHI\Documents\NBFC PROJECT"
```

### 2. Run the ML pipeline

```powershell
python ml_risk_model.py
```

This generates/updates the ML-enriched loan portfolio and model outputs used by the application.

### 3. Build the SQLite database

```powershell
python build_sqlite.py
```

### 4. Start FastAPI

```powershell
python -m uvicorn api:app --reload
```

FastAPI:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

### 5. Start Streamlit

Open another PowerShell window:

```powershell
cd "C:\Users\KHUSHI\Documents\NBFC PROJECT"
python -m streamlit run app.py
```

The Streamlit application will open in the browser.

Both FastAPI and Streamlit should be running for the complete API-driven application.

### Existing Notebook / MySQL / Power BI

The original notebook, MySQL SQL analysis, and Power BI dashboard are retained as supporting analytical deliverables.

---

## Executive Summary

A business-oriented executive summary is included in:

```text
EXECUTIVE_SUMMARY.md
```

It summarizes portfolio exposure, observed risk patterns, ML outputs, and business-facing insights from the project.

---

## Key Business Insights

- The portfolio contains **₹417.04 Cr** of total exposure.
- The observed default rate is **12.47%**.
- **₹50.03 Cr** of exposure is associated with 90+ DPD.
- Business Loans have the highest observed default rate among the modeled loan products.
- Home Loans account for the largest share of portfolio exposure.
- High-risk customers represent **605 customers** with **₹84.09 Cr** exposure.
- High-risk customers have a **16.36%** observed default rate.
- Medium-risk customers represent the largest exposure among the three rule-based risk segments.
- ML outputs provide an additional predictive signal alongside transparent business-rule segmentation.

---

## Business Value Demonstrated

The project demonstrates an end-to-end workflow relevant to:

- Credit Risk Analytics
- Portfolio Monitoring
- Lending Analytics
- Collections Analytics
- Business Intelligence
- Machine Learning
- API Development
- Data Engineering
- Decision Support

It combines technical implementation with business-oriented financial risk analysis.

---

## Limitations

### Synthetic Data

The portfolio is synthetic and does not represent a real NBFC customer population or actual credit performance.

### ML Interpretation

The ML models demonstrate a classification workflow. Their performance should not be treated as production-grade credit-model validation.

### Rule-Based Score

The risk score is a transparent analytical segmentation framework and is not a regulatory or production credit scorecard.

### Feature Importance

Feature importance indicates how the model uses variables; it does not establish causality.

### Production Deployment

A production lending system would require additional controls such as authentication, authorization, model governance, monitoring, data privacy controls, audit logging, validation, calibration, and robust deployment infrastructure.

---

## Future Scope

- Model calibration and threshold optimization
- Hyperparameter tuning and cross-validation
- Explainable AI using SHAP
- Probability of Default calibration
- Loss Given Default and Expected Loss modelling
- Automated high-risk alerts
- Authentication and role-based API access
- Cloud deployment
- Live loan-servicing data integration
- Model monitoring and drift detection

---

## Author

**Khushi Solanki**

B.Tech Mechanical Engineering  
Honors in Robotics  
Dwarkadas J. Sanghvi College of Engineering, Mumbai  
2023–2027

### Technologies Demonstrated

**Python • Pandas • NumPy • scikit-learn • SQL • SQLite • MySQL • FastAPI • Streamlit • Power BI • Git & GitHub • Credit Risk Analytics • Machine Learning • Business Analytics**

---

## Repository

[NBFC Loan Portfolio & Credit Risk Analytics](https://github.com/Khushi23-sol/NBFC-Loan-Portfolio-Risk-Analytics)
