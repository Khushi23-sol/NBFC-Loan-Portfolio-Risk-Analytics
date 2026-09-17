# NBFC Loan Portfolio Risk & Analytics

## Project Overview

This project analyzes an NBFC loan portfolio to identify credit risk, affordability risk, delinquency patterns, portfolio concentration, and default exposure.

The project follows an end-to-end analytics workflow using **Python, SQL, and Power BI**.

---

## Business Problem

NBFCs need to continuously monitor their loan portfolio to identify customers and segments that may create higher credit losses.

This project focuses on answering key business questions:

- Which loan products have higher default risk?
- How does credit score relate to default rates?
- Which customers have higher EMI affordability risk?
- How does loan-to-income exposure vary across customers?
- Which employment and city segments show higher risk?
- How much portfolio exposure is currently in 90+ DPD?
- Which customer risk segments require closer monitoring?
- Where is the portfolio most concentrated?

---

## Objectives

1. Analyze overall portfolio exposure and default performance.
2. Identify high-risk loan products and customer segments.
3. Analyze credit score, EMI burden, and loan-to-income risk.
4. Study delinquency using Days Past Due (DPD).
5. Build a rule-based customer risk segmentation model.
6. Validate portfolio data quality using SQL.
7. Develop an interactive Power BI risk dashboard.

---

## Dataset

The project uses a synthetic NBFC loan portfolio containing:

- **8,000** loan/customer records
- Customer demographics
- Employment information
- Monthly income
- Credit score
- Loan amount
- Loan type
- Tenure
- Interest rate
- EMI
- Days Past Due (DPD)
- Default flag
- Application date

---

## Tools & Technologies

- Python
- Pandas
- NumPy
- Matplotlib
- MySQL
- SQL
- Power BI
- JupyterLab
- Git & GitHub

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
Risk Segmentation
       ↓
SQL Risk Analysis
       ↓
Power BI Dashboard
       ↓
Business Insights
```

---

## Portfolio KPIs

| KPI | Value |
|---|---:|
| Total Customers | 8,000 |
| Total Portfolio Exposure | ₹417.04 Cr |
| Average Loan Amount | ₹5.21 Lakh |
| Average Monthly Income | ₹56,390 |
| Average EMI | ₹12,541 |
| Total Defaults | 998 |
| Default Rate | 12.47% |
| Default Exposure | ₹50.03 Cr |
| 90+ DPD Exposure | ₹50.03 Cr |
| High-Risk Customers | 605 |
| High-Risk Exposure | ₹84.09 Cr |
| High-Risk Default Rate | 16.36% |
| High-Risk Default Exposure | ₹11.55 Cr |

---

## Risk Analysis

### 1. Loan Product Risk

The portfolio was analyzed across:

- Personal Loan
- Home Loan
- Business Loan
- Vehicle Loan
- Gold Loan

Business Loans showed the highest observed default rate among the loan products at approximately **15.46%**.

Home Loans represented the largest share of total portfolio exposure.

### 2. Credit Risk

Customers were grouped into:

- Poor
- Fair
- Good
- Very Good
- Excellent

The analysis compares customer volume, exposure, defaults, default rate, and default exposure across credit risk bands.

### 3. EMI Burden

Customers were segmented using the EMI-to-income ratio:

- Low Burden
- Moderate
- High
- Very High

The **Very High EMI Burden** segment showed the highest observed default rate.

### 4. Loan-to-Income Analysis

Loan-to-annual-income ratios were grouped into:

- <0.5x
- 0.5–1x
- 1–2x
- 2–3x
- 3x+

This analysis helps identify customers with relatively high loan exposure compared with annual income.

### 5. Employment Risk

The portfolio was analyzed across:

- Salaried
- Self-employed
- Business Owner

Business Owners showed the highest observed default rate among the employment segments.

### 6. Geographic Risk

Default rates and portfolio exposure were compared across major cities including:

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

Customers were categorized using Days Past Due:

- Current
- 1–30 DPD
- 31–60 DPD
- 61–89 DPD
- 90+ DPD

The portfolio contains approximately **₹50.03 Cr** of exposure in the 90+ DPD category.

---

## Customer Risk Scoring

A rule-based risk score was developed using three dimensions.

### Credit Risk — 40 Points

Based on credit score.

### EMI Burden — 35 Points

Based on EMI-to-income ratio.

### Loan-to-Income — 25 Points

Based on loan amount relative to annual income.

### Total Risk Score

```text
Risk Score = Credit Risk Score
           + EMI Risk Score
           + LTI Risk Score
```

Customers were classified into:

```text
0–33   → Low Risk
34–66  → Medium Risk
67–100 → High Risk
```

### Risk Segment Results

| Risk Category | Customers | Default Rate | Exposure |
|---|---:|---:|---:|
| Low Risk | 3,571 | 10.45% | ₹96.76 Cr |
| Medium Risk | 3,824 | 13.76% | ₹236.19 Cr |
| High Risk | 605 | 16.36% | ₹84.09 Cr |

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

Reusable SQL views were created for:

- Customer Risk Scores
- Portfolio KPIs
- Product Risk Summary
- Employment Risk Summary
- DPD Risk Summary
- City Risk Summary

---

## Power BI Dashboard

The Power BI dashboard contains two analytical pages.

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

Interactive slicers are available for:

- Loan Type
- Risk Category
- Employment Type
- City

### Page 2 — Risk Deep Dive & Customer Segmentation

Includes:

- Credit Risk Analysis
- EMI Burden Analysis
- Loan-to-Income Analysis
- Risk Category Exposure
- Default Exposure by Risk Category
- Customer Risk Distribution by Loan Type

---

## Data Quality Validation

The final dataset passed the following checks:

- **8,000** total records
- **8,000** unique customers
- **0** missing values
- **0** duplicate customer IDs
- **0** invalid default/DPD records
- **0** unaffordable loans
- **0** high EMI burden records above 50%

---

## Key Business Insights

- The portfolio has **₹417.04 Cr** of total exposure.
- The observed default rate is **12.47%**.
- **₹50.03 Cr** of exposure is associated with 90+ DPD.
- Business Loans have the highest observed default rate among loan products.
- Home Loans account for the largest share of portfolio exposure.
- Very High EMI Burden customers show elevated default rates.
- High-risk customers represent **605 customers** with **₹84.09 Cr** exposure.
- High-risk customers have a **16.36%** default rate.
- Medium-risk customers represent the largest exposure among the three risk segments.

---

## Project Structure

```text
NBFC PROJECT/
│
├── Data/
│   └── loan_portfolio.csv
│
├── Notebooks/
│   └── NBFC_Loan_Portfolio_Risk_Analytics.ipynb
│
├── SQL/
│   └── nbfc_risk_analysis.sql
│
├── generate_data.py
├── NBFC_Loan_Portfolio_Risk_Analytics.pbix
├── README.md
└── .gitignore
```

---

## How to Run

### Python

Open:

```text
Notebooks/NBFC_Loan_Portfolio_Risk_Analytics.ipynb
```

Ensure the dataset is available at:

```text
Data/loan_portfolio.csv
```

Run all notebook cells.

### SQL

Open:

```text
SQL/nbfc_risk_analysis.sql
```

Run the SQL script in MySQL Workbench after importing the dataset.

### Power BI

Open:

```text
NBFC_Loan_Portfolio_Risk_Analytics.pbix
```

Refresh the data if required.

---

## Project Outcome

The project demonstrates an end-to-end financial risk analytics workflow combining:

**Python → SQL → Power BI**

It converts raw loan-level data into portfolio KPIs, risk segments, delinquency analysis, and interactive business intelligence dashboards.

---

## Author

**Khushi Solanki**

B.Tech Mechanical Engineering  
Honors in Robotics  
DJSCE, Mumbai
