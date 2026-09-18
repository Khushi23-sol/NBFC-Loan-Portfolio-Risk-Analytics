"""
Executive Summary Generator
=============================
Auto-generates a business-narrative summary from your REAL project results
(the exact numbers from your completed analysis). This demonstrates the
ability to translate analytics into business communication - useful to
have ready as a written artifact, e.g., in your README or as a PDF to
share separately from the dashboard.
"""

summary = """
# Executive Summary — NBFC Loan Portfolio Risk & Analytics

## Portfolio Overview
The portfolio comprises 8,000 loan accounts totaling Rs 417.04 Cr in
exposure, with an overall observed default rate of 12.47% (998 defaults).
Rs 50.03 Cr of exposure (12.48% of total) is currently in 90+ Days Past
Due status.

## Key Findings

**1. Product Risk Varies Significantly**
Business Loans show the highest default rate at 15.46%, compared to
Home Loans at 10.95% - the lowest among all products. However, Home
Loans represent 59.84% of total portfolio exposure (Rs 249.55 Cr),
meaning they carry the largest absolute default exposure (Rs 26.93 Cr)
despite their lower default rate. This distinction - proportional risk
vs. absolute financial exposure - is critical for prioritizing risk
management resources.

**2. EMI Burden Is a Strong Risk Signal**
Customers in the "Very High" EMI burden band default at 21.39%, nearly
double the rate of "Low Burden" customers (11.33%). This validates
EMI-to-income ratio as a meaningful underwriting input.

**3. Credit Score Remains Predictive**
"Poor" credit band customers default at 18.83%, compared to 10.52% for
"Good" band customers - confirming credit score as a reliable risk
indicator, consistent with its 40-point weight in the risk scoring model.

**4. Employment Type Signals Risk**
Business Owners default at 15.75%, the highest among employment
categories, compared to 10.94% for Salaried customers - supporting
continued income-verification rigor for self-employed/business-owner
applicants.

**5. High-Risk Segment Requires Monitoring**
The High Risk segment (605 customers, Rs 84.09 Cr exposure) shows a
16.36% default rate - notably higher than the portfolio average of
12.47%, validating the effectiveness of the rule-based risk scoring
framework at identifying genuinely elevated-risk accounts.

## Recommended Actions
- Review underwriting criteria for Business Loans, particularly for
  Business Owner applicants with elevated EMI burden
- Prioritize monitoring of the 605 High Risk customers (Rs 84.09 Cr
  exposure), given their 16.36% default rate vs. 12.47% portfolio average
- Given Home Loan's outsized share of total exposure (59.84%), even
  small improvements in Home Loan underwriting could meaningfully
  reduce absolute portfolio risk

## Methodology Note
This analysis uses a synthetic dataset generated to reflect realistic
NBFC lending patterns; it is not based on real customer data. Risk
segmentation uses a transparent, rule-based 100-point scoring framework
(not a machine learning model), combining credit risk (40 pts), EMI
burden (35 pts), and loan-to-income ratio (25 pts) weights chosen to
reflect standard credit risk underwriting practice.
"""

with open("EXECUTIVE_SUMMARY.md", "w") as f:
    f.write(summary)

print(summary)
print("\nSaved to EXECUTIVE_SUMMARY.md")
