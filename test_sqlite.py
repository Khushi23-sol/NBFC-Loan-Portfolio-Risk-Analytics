import sqlite3
from pathlib import Path
import pandas as pd

# ============================================================
# SQLITE BUSINESS ANALYTICS TEST
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DB_FILE = BASE_DIR / "Data" / "nbfc_risk_analytics.db"

conn = sqlite3.connect(DB_FILE)

print("=" * 70)
print("NBFC SQLITE BUSINESS ANALYTICS")
print("=" * 70)


# ------------------------------------------------------------
# 1. VINTAGE / COHORT ANALYSIS
# ------------------------------------------------------------

vintage_query = """
SELECT
    strftime('%Y', disbursement_date)
        || '-Q'
        || (
            (CAST(strftime('%m', disbursement_date) AS INTEGER) - 1) / 3 + 1
        ) AS disbursement_quarter,

    COUNT(*) AS loans_in_cohort,

    ROUND(SUM(loan_amount), 2) AS cohort_exposure,

    SUM(default_flag) AS defaults,

    ROUND(
        100.0 * SUM(default_flag) / COUNT(*),
        2
    ) AS cohort_default_rate_pct

FROM loan_portfolio

GROUP BY disbursement_quarter

ORDER BY disbursement_quarter;
"""

vintage = pd.read_sql_query(vintage_query, conn)

print("\n\n1. VINTAGE / COHORT ANALYSIS")
print("-" * 70)
print(vintage.to_string(index=False))


# ------------------------------------------------------------
# 2. VINTAGE BY PRODUCT
# ------------------------------------------------------------

vintage_product_query = """
SELECT

    product,

    strftime('%Y', disbursement_date)
        || '-Q'
        || (
            (CAST(strftime('%m', disbursement_date) AS INTEGER) - 1) / 3 + 1
        ) AS disbursement_quarter,

    COUNT(*) AS loans_in_cohort,

    ROUND(SUM(loan_amount), 2) AS cohort_exposure,

    SUM(default_flag) AS defaults,

    ROUND(
        100.0 * SUM(default_flag) / COUNT(*),
        2
    ) AS cohort_default_rate_pct

FROM loan_portfolio

GROUP BY
    product,
    disbursement_quarter

ORDER BY
    product,
    disbursement_quarter;
"""

vintage_product = pd.read_sql_query(
    vintage_product_query,
    conn
)

print("\n\n2. VINTAGE BY PRODUCT")
print("-" * 70)
print(vintage_product.to_string(index=False))


# ------------------------------------------------------------
# 3. COLLECTIONS PRIORITY
# ------------------------------------------------------------

collections_query = """
SELECT
    customer_id,
    product,
    city,
    loan_amount,
    days_past_due,
    credit_score,
    emi_to_income,
    ml_predicted_probability

FROM loan_portfolio

WHERE default_flag = 0
  AND days_past_due BETWEEN 1 AND 89

ORDER BY
    days_past_due DESC,
    loan_amount DESC,
    credit_score ASC

LIMIT 20;
"""

collections = pd.read_sql_query(
    collections_query,
    conn
)

print("\n\n3. COLLECTIONS PRIORITY — TOP 20")
print("-" * 70)
print(collections.to_string(index=False))


# ------------------------------------------------------------
# 4. CREATE REUSABLE COLLECTIONS VIEW
# ------------------------------------------------------------

conn.execute("DROP VIEW IF EXISTS collections_priority")

conn.execute("""
CREATE VIEW collections_priority AS

SELECT
    customer_id,
    product,
    city,
    loan_amount,
    days_past_due,
    credit_score,
    emi_to_income,
    ml_predicted_probability,
    default_flag

FROM loan_portfolio

WHERE default_flag = 0
  AND days_past_due BETWEEN 1 AND 89;
""")

conn.commit()


# ------------------------------------------------------------
# 5. VERIFY VIEW
# ------------------------------------------------------------

view_check = pd.read_sql_query(
    "SELECT COUNT(*) AS priority_loans FROM collections_priority",
    conn
)

print("\n\n4. COLLECTIONS PRIORITY VIEW")
print("-" * 70)
print(view_check.to_string(index=False))


conn.close()

print("\n" + "=" * 70)
print("SQLITE BUSINESS ANALYTICS TEST COMPLETE")
print("=" * 70)