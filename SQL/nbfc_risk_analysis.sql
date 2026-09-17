CREATE DATABASE nbfc_risk_analytics;
USE nbfc_risk_analytics;
CREATE TABLE loan_portfolio (
    customer_id VARCHAR(20) PRIMARY KEY,
    age INT,
    city VARCHAR(50),
    employment_type VARCHAR(50),
    monthly_income DECIMAL(12,2),
    credit_score INT,
    loan_amount DECIMAL(14,2),
    loan_type VARCHAR(50),
    tenure_months INT,
    interest_rate DECIMAL(5,2),
    emi DECIMAL(14,2),
    days_past_due INT,
    default_flag TINYINT,
    application_date DATE,
    emi_to_income DECIMAL(6,2),
    loan_to_annual_income DECIMAL(6,2)
);

USE nbfc_risk_analytics;

SELECT COUNT(*) AS total_records
FROM loan_portfolio;

SELECT *
FROM loan_portfolio
LIMIT 10;

SELECT
    MIN(age) AS min_age,
    MAX(age) AS max_age,
    MIN(credit_score) AS min_credit_score,
    MAX(credit_score) AS max_credit_score,
    MIN(loan_amount) AS min_loan,
    MAX(loan_amount) AS max_loan
FROM loan_portfolio;

SELECT
    COUNT(*) AS total_records,
    SUM(customer_id IS NULL) AS missing_customer_id,
    SUM(age IS NULL) AS missing_age,
    SUM(city IS NULL) AS missing_city,
    SUM(monthly_income IS NULL) AS missing_income,
    SUM(credit_score IS NULL) AS missing_credit_score,
    SUM(loan_amount IS NULL) AS missing_loan_amount,
    SUM(emi IS NULL) AS missing_emi,
    SUM(default_flag IS NULL) AS missing_default_flag
FROM loan_portfolio;

SELECT
    customer_id,
    COUNT(*) AS record_count
FROM loan_portfolio
GROUP BY customer_id
HAVING COUNT(*) > 1;

SELECT
    default_flag,
    MIN(days_past_due) AS min_dpd,
    MAX(days_past_due) AS max_dpd,
    COUNT(*) AS record_count
FROM loan_portfolio
GROUP BY default_flag;

SELECT
    customer_id,
    default_flag,
    days_past_due
FROM loan_portfolio
WHERE
    (default_flag = 1 AND days_past_due < 90)
    OR
    (default_flag = 0 AND days_past_due >= 90);
    
SELECT
    COUNT(*) AS unaffordable_loans
FROM loan_portfolio
WHERE emi > monthly_income;    

SELECT
    COUNT(*) AS high_emi_burden_loans
FROM loan_portfolio
WHERE (emi / monthly_income) * 100 > 50;

SELECT
    MAX(
        loan_amount / (monthly_income * 12)
    ) AS max_loan_to_annual_income
FROM loan_portfolio;

SELECT
    loan_type,
    COUNT(*) AS total_loans,
    SUM(default_flag) AS default_count,
    ROUND(
        SUM(default_flag) / COUNT(*) * 100,
        2
    ) AS default_rate
FROM loan_portfolio
GROUP BY loan_type
ORDER BY default_rate DESC;

SELECT
    loan_type,
    COUNT(*) AS total_loans,
    SUM(loan_amount) AS total_exposure,
    SUM(
        CASE
            WHEN default_flag = 1
            THEN loan_amount
            ELSE 0
        END
    ) AS default_exposure
FROM loan_portfolio
GROUP BY loan_type
ORDER BY default_exposure DESC;

SELECT
    loan_type,

    COUNT(*) AS total_loans,

    SUM(default_flag) AS default_count,

    SUM(loan_amount) AS total_exposure,

    SUM(
        CASE
            WHEN default_flag = 1
            THEN loan_amount
            ELSE 0
        END
    ) AS default_exposure,

    ROUND(
        SUM(default_flag) / COUNT(*) * 100,
        2
    ) AS default_rate,

    ROUND(
        SUM(
            CASE
                WHEN default_flag = 1
                THEN loan_amount
                ELSE 0
            END
        )
        / SUM(loan_amount) * 100,
        2
    ) AS default_exposure_ratio

FROM loan_portfolio

GROUP BY loan_type

ORDER BY default_rate DESC;

SELECT
    CASE
        WHEN credit_score <= 579 THEN 'Poor'
        WHEN credit_score <= 669 THEN 'Fair'
        WHEN credit_score <= 739 THEN 'Good'
        WHEN credit_score <= 799 THEN 'Very Good'
        ELSE 'Excellent'
    END AS credit_risk_band,

    COUNT(*) AS loan_count,

    SUM(default_flag) AS default_count,

    SUM(loan_amount) AS total_exposure,

    SUM(
        CASE
            WHEN default_flag = 1
            THEN loan_amount
            ELSE 0
        END
    ) AS default_exposure,

    ROUND(
        SUM(default_flag) / COUNT(*) * 100,
        2
    ) AS default_rate,

    ROUND(
        SUM(
            CASE
                WHEN default_flag = 1
                THEN loan_amount
                ELSE 0
            END
        )
        / SUM(loan_amount) * 100,
        2
    ) AS default_exposure_ratio

FROM loan_portfolio

GROUP BY
    CASE
        WHEN credit_score <= 579 THEN 'Poor'
        WHEN credit_score <= 669 THEN 'Fair'
        WHEN credit_score <= 739 THEN 'Good'
        WHEN credit_score <= 799 THEN 'Very Good'
        ELSE 'Excellent'
    END

ORDER BY default_exposure_ratio DESC;

SELECT
    CASE
        WHEN (emi / monthly_income) * 100 <= 20
            THEN 'Low Burden'
        WHEN (emi / monthly_income) * 100 <= 30
            THEN 'Moderate'
        WHEN (emi / monthly_income) * 100 <= 40
            THEN 'High'
        ELSE 'Very High'
    END AS emi_burden_band,

    COUNT(*) AS loan_count,

    SUM(default_flag) AS default_count,

    SUM(loan_amount) AS total_exposure,

    SUM(
        CASE
            WHEN default_flag = 1
            THEN loan_amount
            ELSE 0
        END
    ) AS default_exposure,

    ROUND(
        SUM(default_flag) / COUNT(*) * 100,
        2
    ) AS default_rate,

    ROUND(
        SUM(
            CASE
                WHEN default_flag = 1
                THEN loan_amount
                ELSE 0
            END
        )
        / SUM(loan_amount) * 100,
        2
    ) AS default_exposure_ratio

FROM loan_portfolio

GROUP BY
    CASE
        WHEN (emi / monthly_income) * 100 <= 20
            THEN 'Low Burden'
        WHEN (emi / monthly_income) * 100 <= 30
            THEN 'Moderate'
        WHEN (emi / monthly_income) * 100 <= 40
            THEN 'High'
        ELSE 'Very High'
    END

ORDER BY default_exposure_ratio DESC;

SELECT
    employment_type,
    COUNT(*) AS total_loans,
    SUM(default_flag) AS default_count,
    SUM(loan_amount) AS total_exposure,
    SUM(CASE
        WHEN default_flag = 1 THEN loan_amount
        ELSE 0
    END) AS default_exposure,
    ROUND(
        SUM(CASE
            WHEN default_flag = 1 THEN loan_amount
            ELSE 0
        END)
        / SUM(loan_amount) * 100,
        2
    ) AS default_exposure_ratio
FROM loan_portfolio
GROUP BY employment_type
ORDER BY default_exposure DESC;

SELECT
    city,
    COUNT(*) AS total_loans,
    SUM(default_flag) AS default_count,
    SUM(loan_amount) AS total_exposure,
    ROUND(
        SUM(default_flag) / COUNT(*) * 100,
        2
    ) AS default_rate
FROM loan_portfolio
GROUP BY city
ORDER BY default_rate DESC;

SELECT
    CASE
        WHEN days_past_due = 0 THEN 'Current'
        WHEN days_past_due BETWEEN 1 AND 30 THEN '1-30 DPD'
        WHEN days_past_due BETWEEN 31 AND 60 THEN '31-60 DPD'
        WHEN days_past_due BETWEEN 61 AND 89 THEN '61-89 DPD'
        ELSE '90+ DPD'
    END AS dpd_category,

    COUNT(*) AS loan_count,

    SUM(loan_amount) AS total_exposure,

    ROUND(
        COUNT(*) / (SELECT COUNT(*) FROM loan_portfolio) * 100,
        2
    ) AS portfolio_percentage

FROM loan_portfolio

GROUP BY
    CASE
        WHEN days_past_due = 0 THEN 'Current'
        WHEN days_past_due BETWEEN 1 AND 30 THEN '1-30 DPD'
        WHEN days_past_due BETWEEN 31 AND 60 THEN '31-60 DPD'
        WHEN days_past_due BETWEEN 61 AND 89 THEN '61-89 DPD'
        ELSE '90+ DPD'
    END

ORDER BY
    portfolio_percentage DESC;

SELECT
    CASE
        WHEN credit_score <= 579 THEN 'Poor'
        WHEN credit_score <= 669 THEN 'Fair'
        WHEN credit_score <= 739 THEN 'Good'
        WHEN credit_score <= 799 THEN 'Very Good'
        ELSE 'Excellent'
    END AS credit_risk_band,

    COUNT(*) AS loan_count,

    SUM(default_flag) AS default_count,

    SUM(loan_amount) AS total_exposure,

    SUM(
        CASE
            WHEN default_flag = 1 THEN loan_amount
            ELSE 0
        END
    ) AS default_exposure,

    ROUND(
        SUM(default_flag) / COUNT(*) * 100,
        2
    ) AS default_rate,

    ROUND(
        SUM(
            CASE
                WHEN default_flag = 1 THEN loan_amount
                ELSE 0
            END
        ) / SUM(loan_amount) * 100,
        2
    ) AS default_exposure_ratio

FROM loan_portfolio

GROUP BY
    CASE
        WHEN credit_score <= 579 THEN 'Poor'
        WHEN credit_score <= 669 THEN 'Fair'
        WHEN credit_score <= 739 THEN 'Good'
        WHEN credit_score <= 799 THEN 'Very Good'
        ELSE 'Excellent'
    END

ORDER BY default_exposure DESC;

SELECT
    CASE
        WHEN monthly_income < 25000 THEN '<25K'
        WHEN monthly_income < 50000 THEN '25K-50K'
        WHEN monthly_income < 100000 THEN '50K-1L'
        WHEN monthly_income < 200000 THEN '1L-2L'
        ELSE '2L+'
    END AS income_band,

    COUNT(*) AS loan_count,

    SUM(default_flag) AS default_count,

    SUM(loan_amount) AS total_exposure,

    ROUND(
        SUM(default_flag) / COUNT(*) * 100,
        2
    ) AS default_rate

FROM loan_portfolio

GROUP BY
    CASE
        WHEN monthly_income < 25000 THEN '<25K'
        WHEN monthly_income < 50000 THEN '25K-50K'
        WHEN monthly_income < 100000 THEN '50K-1L'
        WHEN monthly_income < 200000 THEN '1L-2L'
        ELSE '2L+'
    END

ORDER BY default_rate DESC;

SELECT
    employment_type,

    COUNT(*) AS total_loans,

    SUM(default_flag) AS default_count,

    SUM(loan_amount) AS total_exposure,

    SUM(
        CASE
            WHEN default_flag = 1 THEN loan_amount
            ELSE 0
        END
    ) AS default_exposure,

    ROUND(
        SUM(default_flag) / COUNT(*) * 100,
        2
    ) AS default_rate,

    ROUND(
        SUM(
            CASE
                WHEN default_flag = 1 THEN loan_amount
                ELSE 0
            END
        ) / SUM(loan_amount) * 100,
        2
    ) AS default_exposure_ratio

FROM loan_portfolio
GROUP BY employment_type
ORDER BY default_exposure DESC;

WITH risk_scores AS (
    SELECT
        customer_id,

        CASE
            WHEN credit_score <= 579 THEN 40
            WHEN credit_score <= 669 THEN 30
            WHEN credit_score <= 739 THEN 20
            WHEN credit_score <= 799 THEN 10
            ELSE 0
        END AS credit_risk_score,

        CASE
            WHEN (emi / monthly_income) * 100 <= 20 THEN 0
            WHEN (emi / monthly_income) * 100 <= 30 THEN 10
            WHEN (emi / monthly_income) * 100 <= 40 THEN 25
            ELSE 35
        END AS emi_risk_score,

        CASE
            WHEN loan_amount / (monthly_income * 12) < 0.5 THEN 0
            WHEN loan_amount / (monthly_income * 12) < 1 THEN 5
            WHEN loan_amount / (monthly_income * 12) < 2 THEN 10
            WHEN loan_amount / (monthly_income * 12) < 3 THEN 20
            ELSE 25
        END AS lti_risk_score,

        default_flag

    FROM loan_portfolio
)

SELECT
    CASE
        WHEN credit_risk_score
             + emi_risk_score
             + lti_risk_score <= 33
            THEN 'Low Risk'

        WHEN credit_risk_score
             + emi_risk_score
             + lti_risk_score <= 66
            THEN 'Medium Risk'

        ELSE 'High Risk'
    END AS customer_risk_category,

    COUNT(*) AS customers,
    SUM(default_flag) AS defaults,

    ROUND(
        SUM(default_flag) * 100.0 / COUNT(*),
        2
    ) AS default_rate_percent

FROM risk_scores

GROUP BY customer_risk_category

ORDER BY
    CASE customer_risk_category
        WHEN 'Low Risk' THEN 1
        WHEN 'Medium Risk' THEN 2
        WHEN 'High Risk' THEN 3
    END;
    
WITH risk_scores AS (
    SELECT
        customer_id,
        loan_type,
        loan_amount,

        CASE
            WHEN credit_score <= 579 THEN 40
            WHEN credit_score <= 669 THEN 30
            WHEN credit_score <= 739 THEN 20
            WHEN credit_score <= 799 THEN 10
            ELSE 0
        END AS credit_risk_score,

        CASE
            WHEN (emi / monthly_income) * 100 <= 20 THEN 0
            WHEN (emi / monthly_income) * 100 <= 30 THEN 10
            WHEN (emi / monthly_income) * 100 <= 40 THEN 25
            ELSE 35
        END AS emi_risk_score,

        CASE
            WHEN loan_amount / (monthly_income * 12) < 0.5 THEN 0
            WHEN loan_amount / (monthly_income * 12) < 1 THEN 5
            WHEN loan_amount / (monthly_income * 12) < 2 THEN 10
            WHEN loan_amount / (monthly_income * 12) < 3 THEN 20
            ELSE 25
        END AS lti_risk_score,

        default_flag

    FROM loan_portfolio
),

classified AS (
    SELECT
        *,
        CASE
            WHEN credit_risk_score
                 + emi_risk_score
                 + lti_risk_score <= 33
                THEN 'Low Risk'

            WHEN credit_risk_score
                 + emi_risk_score
                 + lti_risk_score <= 66
                THEN 'Medium Risk'

            ELSE 'High Risk'
        END AS customer_risk_category

    FROM risk_scores
)

SELECT
    loan_type,
    customer_risk_category,

    COUNT(*) AS customers,

    ROUND(
        SUM(loan_amount) / 10000000,
        2
    ) AS total_exposure_cr,

    SUM(default_flag) AS defaults,

    ROUND(
        SUM(default_flag) * 100.0 / COUNT(*),
        2
    ) AS default_rate_percent

FROM classified

GROUP BY
    loan_type,
    customer_risk_category

ORDER BY
    loan_type,
    CASE customer_risk_category
        WHEN 'Low Risk' THEN 1
        WHEN 'Medium Risk' THEN 2
        WHEN 'High Risk' THEN 3
    END;
    
WITH risk_scores AS (
    SELECT
        customer_id,
        loan_amount,

        CASE
            WHEN credit_score <= 579 THEN 40
            WHEN credit_score <= 669 THEN 30
            WHEN credit_score <= 739 THEN 20
            WHEN credit_score <= 799 THEN 10
            ELSE 0
        END AS credit_risk_score,

        CASE
            WHEN (emi / monthly_income) * 100 <= 20 THEN 0
            WHEN (emi / monthly_income) * 100 <= 30 THEN 10
            WHEN (emi / monthly_income) * 100 <= 40 THEN 25
            ELSE 35
        END AS emi_risk_score,

        CASE
            WHEN loan_amount / (monthly_income * 12) < 0.5 THEN 0
            WHEN loan_amount / (monthly_income * 12) < 1 THEN 5
            WHEN loan_amount / (monthly_income * 12) < 2 THEN 10
            WHEN loan_amount / (monthly_income * 12) < 3 THEN 20
            ELSE 25
        END AS lti_risk_score,

        default_flag

    FROM loan_portfolio
),

classified AS (
    SELECT
        *,
        CASE
            WHEN credit_risk_score
                 + emi_risk_score
                 + lti_risk_score <= 33
                THEN 'Low Risk'

            WHEN credit_risk_score
                 + emi_risk_score
                 + lti_risk_score <= 66
                THEN 'Medium Risk'

            ELSE 'High Risk'
        END AS customer_risk_category

    FROM risk_scores
)

SELECT
    customer_risk_category,

    ROUND(
        SUM(loan_amount) / 10000000,
        2
    ) AS total_exposure_cr,

    ROUND(
        SUM(
            CASE
                WHEN default_flag = 1
                THEN loan_amount
                ELSE 0
            END
        ) / 10000000,
        2
    ) AS default_exposure_cr,

    ROUND(
        SUM(
            CASE
                WHEN default_flag = 1
                THEN loan_amount
                ELSE 0
            END
        ) * 100.0
        / SUM(loan_amount),
        2
    ) AS default_exposure_ratio_percent

FROM classified

GROUP BY customer_risk_category

ORDER BY
    CASE customer_risk_category
        WHEN 'Low Risk' THEN 1
        WHEN 'Medium Risk' THEN 2
        WHEN 'High Risk' THEN 3
    END;

SELECT
    DATE_FORMAT(application_date, '%Y-%m') AS month,
    COUNT(*) AS customers,
    ROUND(
        SUM(loan_amount) / 10000000,
        2
    ) AS total_exposure_cr,
    SUM(default_flag) AS defaults,
    ROUND(
        SUM(default_flag) * 100.0 / COUNT(*),
        2
    ) AS default_rate_percent
FROM loan_portfolio
GROUP BY
    DATE_FORMAT(application_date, '%Y-%m')
ORDER BY
    month;
    

SELECT
    CASE
        WHEN credit_score <= 579 THEN 'Poor'
        WHEN credit_score <= 669 THEN 'Fair'
        WHEN credit_score <= 739 THEN 'Good'
        WHEN credit_score <= 799 THEN 'Very Good'
        ELSE 'Excellent'
    END AS credit_score_band,

    COUNT(*) AS customers,

    SUM(default_flag) AS defaults,

    ROUND(
        SUM(default_flag) * 100.0 / COUNT(*),
        2
    ) AS default_rate_percent,

    ROUND(
        SUM(loan_amount) / 10000000,
        2
    ) AS total_exposure_cr

FROM loan_portfolio

GROUP BY
    CASE
        WHEN credit_score <= 579 THEN 'Poor'
        WHEN credit_score <= 669 THEN 'Fair'
        WHEN credit_score <= 739 THEN 'Good'
        WHEN credit_score <= 799 THEN 'Very Good'
        ELSE 'Excellent'
    END

ORDER BY
    CASE credit_score_band
        WHEN 'Poor' THEN 1
        WHEN 'Fair' THEN 2
        WHEN 'Good' THEN 3
        WHEN 'Very Good' THEN 4
        WHEN 'Excellent' THEN 5
    END;

SELECT
    CASE
        WHEN (emi / monthly_income) * 100 <= 20
            THEN 'Low Burden'

        WHEN (emi / monthly_income) * 100 <= 30
            THEN 'Moderate'

        WHEN (emi / monthly_income) * 100 <= 40
            THEN 'High'

        ELSE 'Very High'
    END AS emi_burden_band,

    COUNT(*) AS customers,

    SUM(default_flag) AS defaults,

    ROUND(
        SUM(default_flag) * 100.0 / COUNT(*),
        2
    ) AS default_rate_percent,

    ROUND(
        SUM(loan_amount) / 10000000,
        2
    ) AS total_exposure_cr

FROM loan_portfolio

GROUP BY
    CASE
        WHEN (emi / monthly_income) * 100 <= 20
            THEN 'Low Burden'

        WHEN (emi / monthly_income) * 100 <= 30
            THEN 'Moderate'

        WHEN (emi / monthly_income) * 100 <= 40
            THEN 'High'

        ELSE 'Very High'
    END

ORDER BY
    CASE emi_burden_band
        WHEN 'Low Burden' THEN 1
        WHEN 'Moderate' THEN 2
        WHEN 'High' THEN 3
        WHEN 'Very High' THEN 4
    END;
    
SELECT
    CASE
        WHEN loan_amount / (monthly_income * 12) < 0.5
            THEN '<0.5x'

        WHEN loan_amount / (monthly_income * 12) < 1
            THEN '0.5-1x'

        WHEN loan_amount / (monthly_income * 12) < 2
            THEN '1-2x'

        WHEN loan_amount / (monthly_income * 12) < 3
            THEN '2-3x'

        ELSE '3x+'
    END AS lti_band,

    COUNT(*) AS customers,

    SUM(default_flag) AS defaults,

    ROUND(
        SUM(default_flag) * 100.0 / COUNT(*),
        2
    ) AS default_rate_percent,

    ROUND(
        SUM(loan_amount) / 10000000,
        2
    ) AS total_exposure_cr

FROM loan_portfolio

GROUP BY
    CASE
        WHEN loan_amount / (monthly_income * 12) < 0.5
            THEN '<0.5x'

        WHEN loan_amount / (monthly_income * 12) < 1
            THEN '0.5-1x'

        WHEN loan_amount / (monthly_income * 12) < 2
            THEN '1-2x'

        WHEN loan_amount / (monthly_income * 12) < 3
            THEN '2-3x'

        ELSE '3x+'
    END

ORDER BY
    CASE lti_band
        WHEN '<0.5x' THEN 1
        WHEN '0.5-1x' THEN 2
        WHEN '1-2x' THEN 3
        WHEN '2-3x' THEN 4
        WHEN '3x+' THEN 5
    END;
    
SELECT
    employment_type,

    COUNT(*) AS customers,

    SUM(default_flag) AS defaults,

    ROUND(
        SUM(default_flag) * 100.0 / COUNT(*),
        2
    ) AS default_rate_percent,

    ROUND(
        SUM(loan_amount) / 10000000,
        2
    ) AS total_exposure_cr

FROM loan_portfolio

GROUP BY
    employment_type

ORDER BY
    default_rate_percent DESC;
   
SELECT
    tenure_months,

    COUNT(*) AS customers,

    SUM(default_flag) AS defaults,

    ROUND(
        SUM(default_flag) * 100.0 / COUNT(*),
        2
    ) AS default_rate_percent,

    ROUND(
        SUM(loan_amount) / 10000000,
        2
    ) AS total_exposure_cr

FROM loan_portfolio

GROUP BY
    tenure_months

ORDER BY
    tenure_months;
   
SELECT
    CASE
        WHEN days_past_due = 0
            THEN 'Current'

        WHEN days_past_due BETWEEN 1 AND 30
            THEN '1-30 DPD'

        WHEN days_past_due BETWEEN 31 AND 60
            THEN '31-60 DPD'

        WHEN days_past_due BETWEEN 61 AND 89
            THEN '61-89 DPD'

        ELSE '90+ DPD'
    END AS dpd_category,

    COUNT(*) AS customers,

    ROUND(
        SUM(loan_amount) / 10000000,
        2
    ) AS total_exposure_cr,

    SUM(default_flag) AS defaults,

    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM loan_portfolio),
        2
    ) AS portfolio_share_percent

FROM loan_portfolio

GROUP BY
    CASE
        WHEN days_past_due = 0
            THEN 'Current'

        WHEN days_past_due BETWEEN 1 AND 30
            THEN '1-30 DPD'

        WHEN days_past_due BETWEEN 31 AND 60
            THEN '31-60 DPD'

        WHEN days_past_due BETWEEN 61 AND 89
            THEN '61-89 DPD'

        ELSE '90+ DPD'
    END

ORDER BY
    CASE dpd_category
        WHEN 'Current' THEN 1
        WHEN '1-30 DPD' THEN 2
        WHEN '31-60 DPD' THEN 3
        WHEN '61-89 DPD' THEN 4
        WHEN '90+ DPD' THEN 5
    END;
    
WITH product_metrics AS (
    SELECT
        loan_type,

        COUNT(*) AS customers,

        SUM(default_flag) AS defaults,

        SUM(loan_amount) AS total_exposure,

        SUM(default_flag) * 100.0 / COUNT(*)
            AS default_rate

    FROM loan_portfolio

    GROUP BY loan_type
),

benchmarks AS (
    SELECT
        *,
        (SELECT
            SUM(default_flag) * 100.0 / COUNT(*)
         FROM loan_portfolio) AS portfolio_default_rate,

        (SELECT
            SUM(loan_amount) / COUNT(DISTINCT loan_type)
         FROM loan_portfolio) AS average_product_exposure

    FROM product_metrics
)

SELECT
    loan_type,
    customers,

    ROUND(
        total_exposure / 10000000,
        2
    ) AS total_exposure_cr,

    ROUND(
        default_rate,
        2
    ) AS default_rate_percent,

    ROUND(
        portfolio_default_rate,
        2
    ) AS portfolio_default_rate_percent,

    ROUND(
        average_product_exposure / 10000000,
        2
    ) AS average_product_exposure_cr,

    CASE
        WHEN default_rate > portfolio_default_rate
             AND total_exposure > average_product_exposure
            THEN 'Top Priority'

        WHEN default_rate > portfolio_default_rate
             AND total_exposure <= average_product_exposure
            THEN 'Risk Priority'

        WHEN default_rate <= portfolio_default_rate
             AND total_exposure > average_product_exposure
            THEN 'Concentration Priority'

        ELSE 'Lower Priority'
    END AS risk_priority

FROM benchmarks

ORDER BY
    CASE risk_priority
        WHEN 'Top Priority' THEN 1
        WHEN 'Risk Priority' THEN 2
        WHEN 'Concentration Priority' THEN 3
        ELSE 4
    END,
    default_rate DESC;

WITH risk_scores AS (
    SELECT
        customer_id,
        city,
        loan_amount,

        CASE
            WHEN credit_score <= 579 THEN 40
            WHEN credit_score <= 669 THEN 30
            WHEN credit_score <= 739 THEN 20
            WHEN credit_score <= 799 THEN 10
            ELSE 0
        END AS credit_risk_score,

        CASE
            WHEN (emi / monthly_income) * 100 <= 20 THEN 0
            WHEN (emi / monthly_income) * 100 <= 30 THEN 10
            WHEN (emi / monthly_income) * 100 <= 40 THEN 25
            ELSE 35
        END AS emi_risk_score,

        CASE
            WHEN loan_amount / (monthly_income * 12) < 0.5 THEN 0
            WHEN loan_amount / (monthly_income * 12) < 1 THEN 5
            WHEN loan_amount / (monthly_income * 12) < 2 THEN 10
            WHEN loan_amount / (monthly_income * 12) < 3 THEN 20
            ELSE 25
        END AS lti_risk_score

    FROM loan_portfolio
),

classified AS (
    SELECT
        *,
        CASE
            WHEN credit_risk_score
                 + emi_risk_score
                 + lti_risk_score <= 33
                THEN 'Low Risk'

            WHEN credit_risk_score
                 + emi_risk_score
                 + lti_risk_score <= 66
                THEN 'Medium Risk'

            ELSE 'High Risk'
        END AS customer_risk_category

    FROM risk_scores
)

SELECT
    city,

    COUNT(*) AS total_customers,

    SUM(
        CASE
            WHEN customer_risk_category = 'High Risk'
            THEN 1
            ELSE 0
        END
    ) AS high_risk_customers,

    ROUND(
        SUM(
            CASE
                WHEN customer_risk_category = 'High Risk'
                THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS high_risk_customer_percent,

    ROUND(
        SUM(loan_amount) / 10000000,
        2
    ) AS total_exposure_cr,

    ROUND(
        SUM(
            CASE
                WHEN customer_risk_category = 'High Risk'
                THEN loan_amount
                ELSE 0
            END
        ) / 10000000,
        2
    ) AS high_risk_exposure_cr

FROM classified

GROUP BY city

ORDER BY
    high_risk_customer_percent DESC;
    
WITH risk_scores AS (
    SELECT
        customer_id,
        loan_type,
        loan_amount,
        default_flag,

        CASE
            WHEN credit_score <= 579 THEN 40
            WHEN credit_score <= 669 THEN 30
            WHEN credit_score <= 739 THEN 20
            WHEN credit_score <= 799 THEN 10
            ELSE 0
        END AS credit_risk_score,

        CASE
            WHEN (emi / monthly_income) * 100 <= 20 THEN 0
            WHEN (emi / monthly_income) * 100 <= 30 THEN 10
            WHEN (emi / monthly_income) * 100 <= 40 THEN 25
            ELSE 35
        END AS emi_risk_score,

        CASE
            WHEN loan_amount / (monthly_income * 12) < 0.5 THEN 0
            WHEN loan_amount / (monthly_income * 12) < 1 THEN 5
            WHEN loan_amount / (monthly_income * 12) < 2 THEN 10
            WHEN loan_amount / (monthly_income * 12) < 3 THEN 20
            ELSE 25
        END AS lti_risk_score

    FROM loan_portfolio
),

classified AS (
    SELECT
        *,
        
        CASE
            WHEN credit_risk_score
                 + emi_risk_score
                 + lti_risk_score <= 33
                THEN 'Low Risk'

            WHEN credit_risk_score
                 + emi_risk_score
                 + lti_risk_score <= 66
                THEN 'Medium Risk'

            ELSE 'High Risk'
        END AS customer_risk_category

    FROM risk_scores
)

SELECT
    customer_risk_category,

    COUNT(*) AS priority_customers,

    ROUND(
        SUM(loan_amount) / 10000000,
        2
    ) AS total_exposure_cr,

    SUM(default_flag) AS defaults,

    ROUND(
        SUM(default_flag) * 100.0 / COUNT(*),
        2
    ) AS default_rate_percent,

    ROUND(
        SUM(
            CASE
                WHEN default_flag = 1
                THEN loan_amount
                ELSE 0
            END
        ) / 10000000,
        2
    ) AS default_exposure_cr

FROM classified

WHERE customer_risk_category = 'High Risk'
  AND loan_amount >= 1000000

GROUP BY
    customer_risk_category;
    
WITH risk_scores AS (
    SELECT
        customer_id,
        loan_amount,
        days_past_due,

        CASE
            WHEN credit_score <= 579 THEN 40
            WHEN credit_score <= 669 THEN 30
            WHEN credit_score <= 739 THEN 20
            WHEN credit_score <= 799 THEN 10
            ELSE 0
        END AS credit_risk_score,

        CASE
            WHEN (emi / monthly_income) * 100 <= 20 THEN 0
            WHEN (emi / monthly_income) * 100 <= 30 THEN 10
            WHEN (emi / monthly_income) * 100 <= 40 THEN 25
            ELSE 35
        END AS emi_risk_score,

        CASE
            WHEN loan_amount / (monthly_income * 12) < 0.5 THEN 0
            WHEN loan_amount / (monthly_income * 12) < 1 THEN 5
            WHEN loan_amount / (monthly_income * 12) < 2 THEN 10
            WHEN loan_amount / (monthly_income * 12) < 3 THEN 20
            ELSE 25
        END AS lti_risk_score

    FROM loan_portfolio
),

classified AS (
    SELECT
        *,
        
        CASE
            WHEN credit_risk_score
                 + emi_risk_score
                 + lti_risk_score <= 33
                THEN 'Low Risk'

            WHEN credit_risk_score
                 + emi_risk_score
                 + lti_risk_score <= 66
                THEN 'Medium Risk'

            ELSE 'High Risk'
        END AS customer_risk_category

    FROM risk_scores
),

priority_accounts AS (
    SELECT *
    FROM classified
    WHERE customer_risk_category = 'High Risk'
      AND loan_amount >= 1000000
)

SELECT

    COUNT(*) AS priority_customers,

    ROUND(
        SUM(loan_amount) / 10000000,
        2
    ) AS priority_exposure_cr,

    SUM(
        CASE
            WHEN days_past_due >= 90
            THEN 1
            ELSE 0
        END
    ) AS severe_dpd_customers,

    ROUND(
        SUM(
            CASE
                WHEN days_past_due >= 90
                THEN loan_amount
                ELSE 0
            END
        ) / 10000000,
        2
    ) AS severe_dpd_exposure_cr,

    ROUND(
        SUM(
            CASE
                WHEN days_past_due >= 90
                THEN loan_amount
                ELSE 0
            END
        ) * 100.0
        / SUM(loan_amount),
        2
    ) AS severe_dpd_exposure_share_percent

FROM priority_accounts;

SELECT
    loan_type,

    COUNT(*) AS customers,

    SUM(default_flag) AS defaults,

    ROUND(
        SUM(loan_amount) / 10000000,
        2
    ) AS total_exposure_cr,

    ROUND(
        SUM(
            CASE
                WHEN default_flag = 1
                THEN loan_amount
                ELSE 0
            END
        ) / 10000000,
        2
    ) AS default_exposure_cr,

    ROUND(
        SUM(default_flag) * 100.0 / COUNT(*),
        2
    ) AS default_rate_percent,

    ROUND(
        SUM(
            CASE
                WHEN default_flag = 1
                THEN loan_amount
                ELSE 0
            END
        ) * 100.0 / SUM(loan_amount),
        2
    ) AS default_exposure_ratio_percent

FROM loan_portfolio

GROUP BY
    loan_type

ORDER BY
    default_exposure_cr DESC;
    
WITH risk_scores AS (
    SELECT
        customer_id,
        loan_amount,
        days_past_due,

        CASE
            WHEN credit_score <= 579 THEN 40
            WHEN credit_score <= 669 THEN 30
            WHEN credit_score <= 739 THEN 20
            WHEN credit_score <= 799 THEN 10
            ELSE 0
        END AS credit_risk_score,

        CASE
            WHEN (emi / monthly_income) * 100 <= 20 THEN 0
            WHEN (emi / monthly_income) * 100 <= 30 THEN 10
            WHEN (emi / monthly_income) * 100 <= 40 THEN 25
            ELSE 35
        END AS emi_risk_score,

        CASE
            WHEN loan_amount / (monthly_income * 12) < 0.5 THEN 0
            WHEN loan_amount / (monthly_income * 12) < 1 THEN 5
            WHEN loan_amount / (monthly_income * 12) < 2 THEN 10
            WHEN loan_amount / (monthly_income * 12) < 3 THEN 20
            ELSE 25
        END AS lti_risk_score

    FROM loan_portfolio
),

classified AS (
    SELECT
        *,
        
        CASE
            WHEN credit_risk_score
                 + emi_risk_score
                 + lti_risk_score <= 33
                THEN 'Low Risk'

            WHEN credit_risk_score
                 + emi_risk_score
                 + lti_risk_score <= 66
                THEN 'Medium Risk'

            ELSE 'High Risk'
        END AS customer_risk_category

    FROM risk_scores
)

SELECT
    customer_risk_category,

    COUNT(*) AS customers,

    SUM(
        CASE
            WHEN days_past_due = 0
            THEN 1
            ELSE 0
        END
    ) AS current_customers,

    SUM(
        CASE
            WHEN days_past_due BETWEEN 1 AND 30
            THEN 1
            ELSE 0
        END
    ) AS dpd_1_30_customers,

    SUM(
        CASE
            WHEN days_past_due >= 90
            THEN 1
            ELSE 0
        END
    ) AS dpd_90_plus_customers,

    ROUND(
        SUM(
            CASE
                WHEN days_past_due >= 90
                THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS dpd_90_plus_percent,

    ROUND(
        SUM(
            CASE
                WHEN days_past_due >= 90
                THEN loan_amount
                ELSE 0
            END
        ) / 10000000,
        2
    ) AS dpd_90_plus_exposure_cr

FROM classified

GROUP BY
    customer_risk_category

ORDER BY
    CASE customer_risk_category
        WHEN 'Low Risk' THEN 1
        WHEN 'Medium Risk' THEN 2
        WHEN 'High Risk' THEN 3
    END;
    
WITH product_exposure AS (
    SELECT
        loan_type,
        SUM(loan_amount) AS total_exposure
    FROM loan_portfolio
    GROUP BY loan_type
),

product_share AS (
    SELECT
        loan_type,
        total_exposure,

        total_exposure
        / SUM(total_exposure) OVER() AS exposure_share

    FROM product_exposure
)

SELECT
    loan_type,

    ROUND(
        total_exposure / 10000000,
        2
    ) AS total_exposure_cr,

    ROUND(
        exposure_share * 100,
        2
    ) AS exposure_share_percent,

    ROUND(
        exposure_share * exposure_share,
        4
    ) AS squared_share,

    ROUND(
        SUM(exposure_share * exposure_share) OVER(),
        4
    ) AS portfolio_hhi

FROM product_share

ORDER BY
    exposure_share DESC;

WITH ranked_customers AS (
    SELECT
        customer_id,
        loan_amount,
        default_flag,

        NTILE(10) OVER (
            ORDER BY loan_amount DESC
        ) AS exposure_decile

    FROM loan_portfolio
)

SELECT
    CASE
        WHEN exposure_decile = 1
            THEN 'Top 10%'
        ELSE 'Bottom 90%'
    END AS customer_group,

    COUNT(*) AS customers,

    ROUND(
        SUM(loan_amount) / 10000000,
        2
    ) AS total_exposure_cr,

    ROUND(
        SUM(loan_amount) * 100.0 /
        (SELECT SUM(loan_amount) FROM loan_portfolio),
        2
    ) AS portfolio_exposure_share_percent,

    SUM(default_flag) AS defaults,

    ROUND(
        SUM(default_flag) * 100.0 / COUNT(*),
        2
    ) AS default_rate_percent,

    ROUND(
        SUM(
            CASE
                WHEN default_flag = 1
                THEN loan_amount
                ELSE 0
            END
        ) / 10000000,
        2
    ) AS default_exposure_cr

FROM ranked_customers

GROUP BY
    CASE
        WHEN exposure_decile = 1
            THEN 'Top 10%'
        ELSE 'Bottom 90%'
    END

ORDER BY
    CASE customer_group
        WHEN 'Top 10%' THEN 1
        ELSE 2
    END;
    
SELECT
    DATE_FORMAT(application_date, '%Y-%m') AS vintage_month,

    COUNT(*) AS customers,

    ROUND(
        SUM(loan_amount) / 10000000,
        2
    ) AS total_exposure_cr,

    SUM(default_flag) AS defaults,

    ROUND(
        SUM(default_flag) * 100.0 / COUNT(*),
        2
    ) AS default_rate_percent,

    ROUND(
        SUM(
            CASE
                WHEN default_flag = 1
                THEN loan_amount
                ELSE 0
            END
        ) / 10000000,
        2
    ) AS default_exposure_cr

FROM loan_portfolio

GROUP BY
    DATE_FORMAT(application_date, '%Y-%m')

ORDER BY
    vintage_month;
    
SELECT
    'Total Customers' AS check_name,
    8000 AS expected_value,
    COUNT(*) AS actual_value,
    CASE
        WHEN COUNT(*) = 8000
        THEN 'PASS'
        ELSE 'FAIL'
    END AS status
FROM loan_portfolio

UNION ALL

SELECT
    'Total Exposure (Cr)' AS check_name,
    417.04 AS expected_value,
    ROUND(
        SUM(loan_amount) / 10000000,
        2
    ) AS actual_value,
    CASE
        WHEN ROUND(
            SUM(loan_amount) / 10000000,
            2
        ) = 417.04
        THEN 'PASS'
        ELSE 'FAIL'
    END AS status
FROM loan_portfolio

UNION ALL

SELECT
    'Total Defaults' AS check_name,
    998 AS expected_value,
    SUM(default_flag) AS actual_value,
    CASE
        WHEN SUM(default_flag) = 998
        THEN 'PASS'
        ELSE 'FAIL'
    END AS status
FROM loan_portfolio

UNION ALL

SELECT
    'Default Exposure (Cr)' AS check_name,
    50.03 AS expected_value,
    ROUND(
        SUM(
            CASE
                WHEN default_flag = 1
                THEN loan_amount
                ELSE 0
            END
        ) / 10000000,
        2
    ) AS actual_value,
    CASE
        WHEN ROUND(
            SUM(
                CASE
                    WHEN default_flag = 1
                    THEN loan_amount
                    ELSE 0
                END
            ) / 10000000,
            2
        ) = 50.03
        THEN 'PASS'
        ELSE 'FAIL'
    END AS status
FROM loan_portfolio;

CREATE OR REPLACE VIEW customer_risk_scores AS

SELECT
    customer_id,
    loan_type,
    loan_amount,
    days_past_due,
    default_flag,

    CASE
        WHEN credit_score <= 579 THEN 40
        WHEN credit_score <= 669 THEN 30
        WHEN credit_score <= 739 THEN 20
        WHEN credit_score <= 799 THEN 10
        ELSE 0
    END AS credit_risk_score,

    CASE
        WHEN (emi / monthly_income) * 100 <= 20 THEN 0
        WHEN (emi / monthly_income) * 100 <= 30 THEN 10
        WHEN (emi / monthly_income) * 100 <= 40 THEN 25
        ELSE 35
    END AS emi_risk_score,

    CASE
        WHEN loan_amount / (monthly_income * 12) < 0.5 THEN 0
        WHEN loan_amount / (monthly_income * 12) < 1 THEN 5
        WHEN loan_amount / (monthly_income * 12) < 2 THEN 10
        WHEN loan_amount / (monthly_income * 12) < 3 THEN 20
        ELSE 25
    END AS lti_risk_score,

    (
        CASE
            WHEN credit_score <= 579 THEN 40
            WHEN credit_score <= 669 THEN 30
            WHEN credit_score <= 739 THEN 20
            WHEN credit_score <= 799 THEN 10
            ELSE 0
        END

        +

        CASE
            WHEN (emi / monthly_income) * 100 <= 20 THEN 0
            WHEN (emi / monthly_income) * 100 <= 30 THEN 10
            WHEN (emi / monthly_income) * 100 <= 40 THEN 25
            ELSE 35
        END

        +

        CASE
            WHEN loan_amount / (monthly_income * 12) < 0.5 THEN 0
            WHEN loan_amount / (monthly_income * 12) < 1 THEN 5
            WHEN loan_amount / (monthly_income * 12) < 2 THEN 10
            WHEN loan_amount / (monthly_income * 12) < 3 THEN 20
            ELSE 25
        END
    ) AS risk_score,

    CASE
        WHEN
            (
                CASE
                    WHEN credit_score <= 579 THEN 40
                    WHEN credit_score <= 669 THEN 30
                    WHEN credit_score <= 739 THEN 20
                    WHEN credit_score <= 799 THEN 10
                    ELSE 0
                END
                +
                CASE
                    WHEN (emi / monthly_income) * 100 <= 20 THEN 0
                    WHEN (emi / monthly_income) * 100 <= 30 THEN 10
                    WHEN (emi / monthly_income) * 100 <= 40 THEN 25
                    ELSE 35
                END
                +
                CASE
                    WHEN loan_amount / (monthly_income * 12) < 0.5 THEN 0
                    WHEN loan_amount / (monthly_income * 12) < 1 THEN 5
                    WHEN loan_amount / (monthly_income * 12) < 2 THEN 10
                    WHEN loan_amount / (monthly_income * 12) < 3 THEN 20
                    ELSE 25
                END
            ) <= 33
            THEN 'Low Risk'

        WHEN
            (
                CASE
                    WHEN credit_score <= 579 THEN 40
                    WHEN credit_score <= 669 THEN 30
                    WHEN credit_score <= 739 THEN 20
                    WHEN credit_score <= 799 THEN 10
                    ELSE 0
                END
                +
                CASE
                    WHEN (emi / monthly_income) * 100 <= 20 THEN 0
                    WHEN (emi / monthly_income) * 100 <= 30 THEN 10
                    WHEN (emi / monthly_income) * 100 <= 40 THEN 25
                    ELSE 35
                END
                +
                CASE
                    WHEN loan_amount / (monthly_income * 12) < 0.5 THEN 0
                    WHEN loan_amount / (monthly_income * 12) < 1 THEN 5
                    WHEN loan_amount / (monthly_income * 12) < 2 THEN 10
                    WHEN loan_amount / (monthly_income * 12) < 3 THEN 20
                    ELSE 25
                END
            ) <= 66
            THEN 'Medium Risk'

        ELSE 'High Risk'
    END AS customer_risk_category

FROM loan_portfolio;


SELECT
    customer_risk_category,

    COUNT(*) AS customers,

    ROUND(
        SUM(loan_amount) / 10000000,
        2
    ) AS total_exposure_cr,

    SUM(default_flag) AS defaults,

    ROUND(
        SUM(default_flag) * 100.0 / COUNT(*),
        2
    ) AS default_rate_percent,

    ROUND(
        SUM(
            CASE
                WHEN default_flag = 1
                THEN loan_amount
                ELSE 0
            END
        ) / 10000000,
        2
    ) AS default_exposure_cr

FROM customer_risk_scores

GROUP BY
    customer_risk_category

ORDER BY
    CASE customer_risk_category
        WHEN 'Low Risk' THEN 1
        WHEN 'Medium Risk' THEN 2
        WHEN 'High Risk' THEN 3
    END;
    
-- ============================================
-- STEP 57: EXECUTIVE PORTFOLIO KPI SUMMARY
-- ============================================

SELECT

    COUNT(*) AS total_customers,

    ROUND(
        SUM(loan_amount) / 10000000,
        2
    ) AS total_exposure_cr,

    ROUND(
        AVG(loan_amount),
        2
    ) AS average_loan,

    ROUND(
        AVG(monthly_income),
        2
    ) AS average_monthly_income,

    ROUND(
        AVG(emi),
        2
    ) AS average_emi,

    SUM(default_flag) AS total_defaults,

    ROUND(
        SUM(default_flag) * 100.0 / COUNT(*),
        2
    ) AS default_rate_percent,

    ROUND(
        SUM(
            CASE
                WHEN default_flag = 1
                THEN loan_amount
                ELSE 0
            END
        ) / 10000000,
        2
    ) AS default_exposure_cr,

    ROUND(
        SUM(
            CASE
                WHEN days_past_due >= 90
                THEN loan_amount
                ELSE 0
            END
        ) / 10000000,
        2
    ) AS dpd_90_plus_exposure_cr

FROM loan_portfolio;

-- ============================================
-- STEP 58: CREATE PORTFOLIO KPI VIEW
-- ============================================

CREATE OR REPLACE VIEW portfolio_kpis AS

SELECT

    COUNT(*) AS total_customers,

    ROUND(
        SUM(loan_amount) / 10000000,
        2
    ) AS total_exposure_cr,

    ROUND(
        AVG(loan_amount),
        2
    ) AS average_loan,

    ROUND(
        AVG(monthly_income),
        2
    ) AS average_monthly_income,

    ROUND(
        AVG(emi),
        2
    ) AS average_emi,

    SUM(default_flag) AS total_defaults,

    ROUND(
        SUM(default_flag) * 100.0 / COUNT(*),
        2
    ) AS default_rate_percent,

    ROUND(
        SUM(
            CASE
                WHEN default_flag = 1
                THEN loan_amount
                ELSE 0
            END
        ) / 10000000,
        2
    ) AS default_exposure_cr,

    ROUND(
        SUM(
            CASE
                WHEN days_past_due >= 90
                THEN loan_amount
                ELSE 0
            END
        ) / 10000000,
        2
    ) AS dpd_90_plus_exposure_cr

FROM loan_portfolio;

-- ============================================
-- STEP 60: PRODUCT RISK SUMMARY VIEW
-- ============================================

CREATE OR REPLACE VIEW product_risk_summary AS

SELECT
    loan_type,

    COUNT(*) AS customers,

    SUM(default_flag) AS defaults,

    ROUND(
        SUM(loan_amount) / 10000000,
        2
    ) AS total_exposure_cr,

    ROUND(
        SUM(default_flag) * 100.0 / COUNT(*),
        2
    ) AS default_rate_percent,

    ROUND(
        SUM(
            CASE
                WHEN default_flag = 1
                THEN loan_amount
                ELSE 0
            END
        ) / 10000000,
        2
    ) AS default_exposure_cr

FROM loan_portfolio

GROUP BY loan_type;

SELECT *
FROM product_risk_summary;

SELECT *
FROM product_risk_summary
ORDER BY default_rate_percent DESC;

-- STEP 62: EMPLOYMENT RISK SUMMARY VIEW

CREATE OR REPLACE VIEW employment_risk_summary AS
SELECT
    employment_type,
    COUNT(*) AS customers,
    SUM(default_flag) AS defaults,
    ROUND(SUM(loan_amount) / 10000000, 2) AS total_exposure_cr,
    ROUND(SUM(default_flag) * 100.0 / COUNT(*), 2) AS default_rate_percent,
    ROUND(
        SUM(CASE WHEN default_flag = 1 THEN loan_amount ELSE 0 END) / 10000000,
        2
    ) AS default_exposure_cr
FROM loan_portfolio
GROUP BY employment_type;

SELECT *
FROM employment_risk_summary;

-- STEP 63: DPD RISK SUMMARY VIEW

CREATE OR REPLACE VIEW dpd_risk_summary AS
SELECT
    CASE
        WHEN days_past_due = 0 THEN 'Current'
        WHEN days_past_due BETWEEN 1 AND 30 THEN '1-30 DPD'
        WHEN days_past_due BETWEEN 31 AND 60 THEN '31-60 DPD'
        WHEN days_past_due BETWEEN 61 AND 89 THEN '61-89 DPD'
        WHEN days_past_due >= 90 THEN '90+ DPD'
    END AS dpd_category,

    COUNT(*) AS customers,

    SUM(default_flag) AS defaults,

    ROUND(SUM(loan_amount) / 10000000, 2) AS total_exposure_cr,

    ROUND(
        SUM(default_flag) * 100.0 / COUNT(*),
        2
    ) AS default_rate_percent,

    ROUND(
        SUM(CASE WHEN default_flag = 1 THEN loan_amount ELSE 0 END)
        / 10000000,
        2
    ) AS default_exposure_cr

FROM loan_portfolio
GROUP BY
    CASE
        WHEN days_past_due = 0 THEN 'Current'
        WHEN days_past_due BETWEEN 1 AND 30 THEN '1-30 DPD'
        WHEN days_past_due BETWEEN 31 AND 60 THEN '31-60 DPD'
        WHEN days_past_due BETWEEN 61 AND 89 THEN '61-89 DPD'
        WHEN days_past_due >= 90 THEN '90+ DPD'
    END;
    

-- STEP 64: CITY RISK SUMMARY VIEW

CREATE OR REPLACE VIEW city_risk_summary AS
SELECT
    city,

    COUNT(*) AS customers,

    SUM(default_flag) AS defaults,

    ROUND(
        SUM(loan_amount) / 10000000,
        2
    ) AS total_exposure_cr,

    ROUND(
        SUM(default_flag) * 100.0 / COUNT(*),
        2
    ) AS default_rate_percent,

    ROUND(
        SUM(
            CASE
                WHEN default_flag = 1
                THEN loan_amount
                ELSE 0
            END
        ) / 10000000,
        2
    ) AS default_exposure_cr

FROM loan_portfolio
GROUP BY city;

SELECT *
FROM city_risk_summary
ORDER BY default_rate_percent DESC;

SELECT user, host, plugin
FROM mysql.user
WHERE user = 'root';