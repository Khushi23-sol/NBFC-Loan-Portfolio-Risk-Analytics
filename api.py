from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import sqlite3
import pandas as pd

app = FastAPI(
    title="NBFC Loan Portfolio Risk Analytics API",
    description="REST API for portfolio, risk and collections analytics",
    version="1.0.0"
)

DB_PATH = "Data/nbfc_risk_analytics.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


class LoanSubmission(BaseModel):
    """Loan-originations payload submitted by a loan officer / LOS."""
    age: int = Field(..., ge=18, le=80)
    city: str
    employment_type: str
    monthly_income: float = Field(..., gt=0)
    credit_score: int = Field(..., ge=300, le=900)
    product: str
    loan_amount: float = Field(..., gt=0)
    tenure_months: int = Field(..., ge=6, le=360)
    interest_rate: float = Field(..., ge=0, le=30)



# ============================================================
# COMMON FILTER FUNCTION
# ============================================================

def apply_filters(query, params, product=None, city=None, credit_band=None):

    if product and product != "All":
        query += " AND product = ?"
        params.append(product)

    if city and city != "All":
        query += " AND city = ?"
        params.append(city)

    if credit_band and credit_band != "All":
        query += """
        AND (
            CASE
                WHEN credit_score < 580 THEN 'Poor'
                WHEN credit_score < 670 THEN 'Fair'
                WHEN credit_score < 740 THEN 'Good'
                WHEN credit_score < 800 THEN 'Very Good'
                ELSE 'Excellent'
            END
        ) = ?
        """
        params.append(credit_band)

    return query, params


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():

    return {
        "message": "NBFC Risk Analytics API is running",
        "status": "success"
    }


# ============================================================
# 1. PORTFOLIO SUMMARY
# ============================================================

@app.get("/api/portfolio/summary")
def portfolio_summary(
    product: str = None,
    city: str = None,
    credit_band: str = None
):

    conn = get_connection()

    query = """
    SELECT
        COUNT(*) AS total_loans,

        ROUND(
            SUM(loan_amount),
            2
        ) AS total_exposure,

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

    FROM loan_portfolio

    WHERE 1 = 1
    """

    params = []

    query, params = apply_filters(
        query,
        params,
        product,
        city,
        credit_band
    )

    result = pd.read_sql_query(
        query,
        conn,
        params=params
    )

    conn.close()

    return result.to_dict(
        orient="records"
    )[0]


# ============================================================
# 2. PRODUCT-WISE RISK
# ============================================================

@app.get("/api/portfolio/product-risk")
def product_risk(
    product: str = None,
    city: str = None,
    credit_band: str = None
):

    conn = get_connection()

    query = """
    SELECT
        product,

        COUNT(*) AS total_loans,

        ROUND(
            SUM(loan_amount),
            2
        ) AS exposure,

        SUM(default_flag) AS defaults,

        ROUND(
            100.0 * SUM(default_flag) / COUNT(*),
            2
        ) AS default_rate_pct

    FROM loan_portfolio

    WHERE 1 = 1
    """

    params = []

    query, params = apply_filters(
        query,
        params,
        product,
        city,
        credit_band
    )

    query += """
    GROUP BY product
    ORDER BY default_rate_pct DESC;
    """

    result = pd.read_sql_query(
        query,
        conn,
        params=params
    )

    conn.close()

    return result.to_dict(
        orient="records"
    )


# ============================================================
# 3. CREDIT SCORE RISK
# ============================================================

@app.get("/api/portfolio/credit-risk")
def credit_risk(
    product: str = None,
    city: str = None,
    credit_band: str = None
):

    conn = get_connection()

    query = """
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

        ROUND(
            SUM(loan_amount),
            2
        ) AS exposure

    FROM loan_portfolio

    WHERE 1 = 1
    """

    params = []

    query, params = apply_filters(
        query,
        params,
        product,
        city,
        credit_band
    )

    query += """
    GROUP BY credit_band
    ORDER BY default_rate_pct DESC;
    """

    result = pd.read_sql_query(
        query,
        conn,
        params=params
    )

    conn.close()

    return result.to_dict(
        orient="records"
    )


# ============================================================
# 4. CITY-WISE RISK
# ============================================================

@app.get("/api/portfolio/city-risk")
def city_risk(
    product: str = None,
    city: str = None,
    credit_band: str = None
):

    conn = get_connection()

    query = """
    SELECT

        city,

        COUNT(*) AS total_loans,

        SUM(default_flag) AS defaults,

        ROUND(
            100.0 * SUM(default_flag) / COUNT(*),
            2
        ) AS default_rate_pct,

        ROUND(
            SUM(loan_amount),
            2
        ) AS exposure

    FROM loan_portfolio

    WHERE 1 = 1
    """

    params = []

    query, params = apply_filters(
        query,
        params,
        product,
        city,
        credit_band
    )

    query += """
    GROUP BY city
    ORDER BY default_rate_pct DESC;
    """

    result = pd.read_sql_query(
        query,
        conn,
        params=params
    )

    conn.close()

    return result.to_dict(
        orient="records"
    )


# ============================================================
# 5. VINTAGE / COHORT ANALYSIS
# ============================================================

@app.get("/api/portfolio/vintage")
def vintage_analysis(
    product: str = None,
    city: str = None,
    credit_band: str = None
):

    conn = get_connection()

    query = """
    SELECT

        strftime(
            '%Y',
            disbursement_date
        )
        || '-Q'
        ||
        (
            (
                CAST(
                    strftime(
                        '%m',
                        disbursement_date
                    ) AS INTEGER
                ) - 1
            ) / 3 + 1
        ) AS disbursement_quarter,

        COUNT(*) AS loans_in_cohort,

        ROUND(
            SUM(loan_amount),
            2
        ) AS cohort_exposure,

        SUM(default_flag) AS defaults,

        ROUND(
            100.0 * SUM(default_flag) / COUNT(*),
            2
        ) AS cohort_default_rate_pct

    FROM loan_portfolio

    WHERE 1 = 1
    """

    params = []

    query, params = apply_filters(
        query,
        params,
        product,
        city,
        credit_band
    )

    query += """
    GROUP BY disbursement_quarter
    ORDER BY disbursement_quarter;
    """

    result = pd.read_sql_query(
        query,
        conn,
        params=params
    )

    conn.close()

    return result.to_dict(
        orient="records"
    )


# ============================================================
# 6. ML HIGH-RISK LOANS
# ============================================================

@app.get("/api/risk/high-risk-loans")
def high_risk_loans(
    product: str = None,
    city: str = None,
    credit_band: str = None
):

    conn = get_connection()

    query = """
    SELECT

        customer_id,

        product,

        city,

        loan_amount,

        credit_score,

        emi_to_income,

        ml_predicted_probability

    FROM loan_portfolio

    WHERE 1 = 1
    """

    params = []

    query, params = apply_filters(
        query,
        params,
        product,
        city,
        credit_band
    )

    query += """
    ORDER BY
        ml_predicted_probability DESC
    LIMIT 20;
    """

    result = pd.read_sql_query(
        query,
        conn,
        params=params
    )

    conn.close()

    return result.to_dict(
        orient="records"
    )


# ============================================================
# 7. COLLECTIONS PRIORITY
# ============================================================

@app.get("/api/collections/priority")
def collections_priority(
    product: str = None,
    city: str = None,
    credit_band: str = None
):

    conn = get_connection()

    query = """
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
    """

    params = []

    query, params = apply_filters(
        query,
        params,
        product,
        city,
        credit_band
    )

    query += """
    ORDER BY

        days_past_due DESC,

        loan_amount DESC,

        credit_score ASC

    LIMIT 20;
    """

    result = pd.read_sql_query(
        query,
        conn,
        params=params
    )

    conn.close()

    return result.to_dict(
        orient="records"
    )

# ============================================================
# 8. LIVE LOAN SIMULATION PIPELINE
# ============================================================

@app.post("/api/pipeline/simulate-new-loans")
def simulate_new_loans(n: int = 20, seed: int = None):
    """
    Generate realistic new loans, score them with the saved Random Forest
    pipeline and existing rule-based score, then append them to both the
    analytical CSV and SQLite database.
    """
    if n < 1 or n > 500:
        raise HTTPException(
            status_code=400,
            detail="n must be between 1 and 500."
        )

    try:
        from live_loan_simulator import simulate_and_append

        result = simulate_and_append(n=n, seed=seed)

        new_df = result["new_loans"]

        return {
            "status": "success",
            "message": f"{result['added']} new loans simulated and added.",
            "loans_added": result["added"],
            "csv_total": result["csv_total"],
            "sqlite_total": result["sqlite_total"],
            "new_loans": new_df[
                [
                    "customer_id",
                    "product",
                    "city",
                    "credit_score",
                    "risk_score",
                    "risk_category",
                    "ml_predicted_probability",
                ]
            ].to_dict(orient="records"),
        }

    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Live simulation failed: {e}"
        )

# ============================================================
# 9. SINGLE LOAN ORIGINATION / AUTO-SCORING
# ============================================================

@app.post("/api/loans")
def create_loan(loan: LoanSubmission):
    """
    Accept one newly originated loan, calculate analytical features,
    apply the rule-based risk score and saved Random Forest model,
    and persist the scored loan to CSV + SQLite.

    This represents a loan officer / loan-origination-system submission.
    """
    try:
        from live_loan_simulator import score_manual_loan

        result = score_manual_loan(loan.model_dump())
        row = result["new_loans"].iloc[0]

        return {
            "status": "success",
            "message": "Loan originated, scored and added to the portfolio.",
            "customer_id": row["customer_id"],
            "csv_total": result["csv_total"],
            "sqlite_total": result["sqlite_total"],
            "loan": {
                "customer_id": row["customer_id"],
                "product": row["product"],
                "city": row["city"],
                "credit_score": int(row["credit_score"]),
                "loan_amount": float(row["loan_amount"]),
                "emi": float(row["emi"]),
                "emi_to_income": float(row["emi_to_income"]),
                "loan_to_annual_income": float(row["loan_to_annual_income"]),
                "risk_score": int(row["risk_score"]),
                "risk_category": row["risk_category"],
                "ml_predicted_probability": float(row["ml_predicted_probability"]),
            },
        }

    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Loan submission failed: {e}")

