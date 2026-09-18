-- ============================================================
-- NBFC LOAN PORTFOLIO RISK ANALYTICS
-- SQLite BUSINESS SQL LAYER
-- ============================================================


-- ============================================================
-- 1. PORTFOLIO SUMMARY
-- ============================================================

SELECT
    COUNT(*) AS total_loans,
    ROUND(SUM(loan_amount), 2) AS total_exposure,
    SUM(default_flag) AS total_defaults,
    ROUND(
        100.0 * SUM(default_flag) / COUNT(*),
        2
    ) AS default_rate_pct,
    ROUND(
        SUM(
            CASE
                WHEN days_past_due >= 90
                THEN loan_amount
                ELSE 0
            END
        ),
        2
    ) AS exposure_90_plus_dpd
FROM loan_portfolio;


-- ============================================================
-- 2. DEFAULT RATE BY PRODUCT
-- ============================================================

SELECT
    product,
    COUNT(*) AS total_loans,
    ROUND(SUM(loan_amount), 2) AS exposure,
    SUM(default_flag) AS defaults,
    ROUND(
        100.0 * SUM(default_flag) / COUNT(*),
        2
    ) AS default_rate_pct
FROM loan_portfolio
GROUP BY product
ORDER BY default_rate_pct DESC;


-- ============================================================
-- 3. DEFAULT RATE BY CREDIT SCORE BAND
-- ============================================================

SELECT
    CASE
        WHEN credit_score < 580 THEN 'Poor'
        WHEN credit_score < 670 THEN 'Fair'
        WHEN credit_score < 740 THEN 'Good'
        WHEN credit_score < 800 THEN 'Very Good'
        ELSE 'Excellent'
    END AS credit_band,

    COUNT(*) AS total_loans,
    SUM(default_flag) AS defaults,

    ROUND(
        100.0 * SUM(default_flag) / COUNT(*),
        2
    ) AS default_rate_pct,

    ROUND(SUM(loan_amount), 2) AS exposure

FROM loan_portfolio

GROUP BY credit_band

ORDER BY default_rate_pct DESC;


-- ============================================================
-- 4. CITY-WISE DEFAULT RATE
-- ============================================================

SELECT
    city,
    COUNT(*) AS total_loans,
    SUM(default_flag) AS defaults,

    ROUND(
        100.0 * SUM(default_flag) / COUNT(*),
        2
    ) AS default_rate_pct,

    ROUND(SUM(loan_amount), 2) AS exposure

FROM loan_portfolio

GROUP BY city

ORDER BY default_rate_pct DESC;


-- ============================================================
-- 5. VINTAGE / COHORT ANALYSIS
-- ============================================================

SELECT

    strftime('%Y', disbursement_date)
        || '-Q'
        || (
            (
                CAST(strftime('%m', disbursement_date) AS INTEGER) - 1
            ) / 3 + 1
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


-- ============================================================
-- 6. VINTAGE ANALYSIS BY PRODUCT
-- ============================================================

SELECT

    product,

    strftime('%Y', disbursement_date)
        || '-Q'
        || (
            (
                CAST(strftime('%m', disbursement_date) AS INTEGER) - 1
            ) / 3 + 1
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


-- ============================================================
-- 7. COLLECTIONS PRIORITY LIST
-- ============================================================
-- Active loans showing early delinquency.
-- 1-89 DPD and not yet defaulted.
-- Higher DPD first, then higher exposure,
-- then lower credit score.

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


-- ============================================================
-- 8. COLLECTIONS PRIORITY VIEW
-- ============================================================

DROP VIEW IF EXISTS collections_priority;

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