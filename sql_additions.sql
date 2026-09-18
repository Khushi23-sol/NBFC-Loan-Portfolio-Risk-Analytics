-- ============================================================
-- ADDITIONAL SQL QUERIES: Vintage Analysis & Collections Priority
-- ============================================================
-- These ADD to your existing nbfc_risk_analysis.sql file - append
-- them there, don't replace your existing queries/views.
-- Written for MySQL syntax to match your existing database.

-- ------------------------------------------------------------
-- 1. VINTAGE / COHORT ANALYSIS
-- ------------------------------------------------------------
-- Groups loans by the QUARTER they were disbursed, then checks the
-- default rate within each cohort. This answers: "Is underwriting
-- quality improving or worsening over time?" - a real credit risk
-- technique, distinct from just looking at overall portfolio default rate.

SELECT
    CONCAT(YEAR(application_date), '-Q', QUARTER(application_date)) AS disbursement_quarter,
    COUNT(*) AS loans_in_cohort,
    SUM(loan_amount) AS cohort_exposure,
    ROUND(100.0 * SUM(default_flag) / COUNT(*), 2) AS cohort_default_rate_pct
FROM loan_portfolio
GROUP BY disbursement_quarter
ORDER BY disbursement_quarter;

-- Interpretation guide: if cohort_default_rate_pct is trending UP across
-- more recent quarters, underwriting standards may be loosening over time
-- (a real early-warning signal for a credit risk team).


-- ------------------------------------------------------------
-- 2. COLLECTIONS PRIORITY LIST
-- ------------------------------------------------------------
-- Ranks currently-active (non-defaulted) loans by a combination of
-- risk score and exposure - this is the "who should collections call
-- first" list, a genuinely actionable business output.

SELECT
    customer_id,
    loan_type,
    city,
    loan_amount,
    days_past_due,
    credit_score
FROM loan_portfolio
WHERE default_flag = 0
  AND days_past_due BETWEEN 1 AND 89  -- already showing early delinquency signs, not yet 90+ (default)
ORDER BY
    days_past_due DESC,   -- most overdue first
    loan_amount DESC       -- among equally overdue, prioritize larger exposure
LIMIT 20;


-- ------------------------------------------------------------
-- 3. VINTAGE ANALYSIS BY LOAN PRODUCT (combines vintage + product risk)
-- ------------------------------------------------------------
-- A more advanced version: does default rate by cohort vary by product?
-- (e.g., maybe Business Loan underwriting loosened, but Home Loan didn't)

SELECT
    loan_type,
    CONCAT(YEAR(application_date), '-Q', QUARTER(application_date)) AS disbursement_quarter,
    COUNT(*) AS loans_in_cohort,
    ROUND(100.0 * SUM(default_flag) / COUNT(*), 2) AS cohort_default_rate_pct
FROM loan_portfolio
GROUP BY loan_type, disbursement_quarter
ORDER BY loan_type, disbursement_quarter;


-- ------------------------------------------------------------
-- 4. HIGH-RISK + HIGH-EXPOSURE COMBINED PRIORITY VIEW
-- ------------------------------------------------------------
-- Creates a reusable view combining your existing risk category with
-- the collections logic above - useful for the Power BI dashboard too.

CREATE OR REPLACE VIEW collections_priority AS
SELECT
    customer_id,
    loan_type,
    city,
    loan_amount,
    days_past_due,
    credit_score,
    default_flag
FROM loan_portfolio
WHERE default_flag = 0
  AND days_past_due BETWEEN 1 AND 89
ORDER BY days_past_due DESC, loan_amount DESC;

-- Usage: SELECT * FROM collections_priority LIMIT 20;
