"""
Live loan simulator for the NBFC Risk Analytics project.

Generates realistic new loans, calculates analytical features, applies the
existing rule-based risk formula, scores the loans with the already-trained
Random Forest pipeline, and appends the results to both CSV and SQLite.

The original raw dataset (Data/loan_portfolio.csv) is never modified.
"""

from pathlib import Path
from datetime import date

import joblib
import numpy as np
import pandas as pd
import sqlite3

BASE_DIR = Path(__file__).resolve().parent
ML_DATA_PATH = BASE_DIR / "Data" / "loan_portfolio_with_ml.csv"
DB_PATH = BASE_DIR / "Data" / "nbfc_risk_analytics.db"
MODEL_PATH = BASE_DIR / "models" / "rf_risk_pipeline.joblib"

PRODUCTS = {
    "Business Loan": (300_000, 2_500_000, 35_000, 160_000, 12.0, 17.0, [12, 24, 36, 48, 60]),
    "Personal Loan": (100_000, 1_500_000, 25_000, 140_000, 11.0, 18.0, [12, 24, 36, 48, 60]),
    "Vehicle Loan": (200_000, 2_000_000, 25_000, 130_000, 9.0, 15.0, [24, 36, 48, 60, 72]),
    "Gold Loan": (100_000, 1_000_000, 20_000, 120_000, 10.0, 16.0, [12, 24, 36]),
    "Home Loan": (1_500_000, 15_000_000, 45_000, 250_000, 7.5, 11.5, [60, 120, 180, 240, 300]),
}

CITIES = [
    "Mumbai", "Delhi", "Bengaluru", "Hyderabad", "Chennai",
    "Pune", "Kolkata", "Ahmedabad", "Jaipur", "Lucknow"
]

EMPLOYMENT_TYPES = ["Salaried", "Self-employed", "Business Owner"]


def calculate_emi(principal, annual_rate, months):
    monthly_rate = annual_rate / 12 / 100
    if monthly_rate == 0:
        return principal / months
    return principal * monthly_rate * (1 + monthly_rate) ** months / (
        (1 + monthly_rate) ** months - 1
    )


def credit_points(score):
    if score < 580:
        return 40
    if score < 670:
        return 30
    if score < 740:
        return 20
    if score < 800:
        return 10
    return 0


def emi_points(emi_pct):
    if emi_pct < 15:
        return 0
    if emi_pct < 25:
        return 10
    if emi_pct < 35:
        return 25
    return 35


def lti_points(lti):
    if lti < 0.5:
        return 0
    if lti < 1:
        return 5
    if lti < 2:
        return 10
    if lti < 3:
        return 20
    return 25


def rule_based_risk_score(credit_score, emi_pct, lti):
    score = (
        credit_points(credit_score)
        + emi_points(emi_pct)
        + lti_points(lti)
    )
    if score <= 33:
        category = "Low"
    elif score <= 66:
        category = "Medium"
    else:
        category = "High"
    return int(score), category


def _next_customer_ids(existing_ids, n):
    numeric = (
        pd.Series(existing_ids, dtype="string")
        .str.extract(r"(\d+)$", expand=False)
        .dropna()
        .astype(int)
    )
    start = int(numeric.max()) + 1 if not numeric.empty else 100001
    return [f"CUST{start + i}" for i in range(n)]


def generate_new_loans(n=20, seed=None):
    if n < 1 or n > 500:
        raise ValueError("n must be between 1 and 500.")

    if not ML_DATA_PATH.exists():
        raise FileNotFoundError(f"Missing {ML_DATA_PATH}")

    rng = np.random.default_rng(seed)

    existing = pd.read_csv(ML_DATA_PATH)
    customer_ids = _next_customer_ids(existing["customer_id"], n)

    rows = []

    product_names = list(PRODUCTS.keys())
    product_probs = [0.18, 0.35, 0.10, 0.15, 0.22]

    for customer_id in customer_ids:
        product = rng.choice(product_names, p=product_probs)
        low_loan, high_loan, low_income, high_income, low_rate, high_rate, tenures = PRODUCTS[product]

        age = int(rng.integers(22, 61))
        monthly_income = float(rng.integers(low_income, high_income + 1))
        credit_score = int(np.clip(rng.normal(680, 75), 350, 900))
        loan_amount = float(rng.integers(low_loan, high_loan + 1))
        tenure_months = int(rng.choice(tenures))
        interest_rate = float(rng.uniform(low_rate, high_rate))
        emi = float(calculate_emi(loan_amount, interest_rate, tenure_months))

        employment_type = str(
            rng.choice(
                EMPLOYMENT_TYPES,
                p=[0.55, 0.30, 0.15]
            )
        )
        city = str(rng.choice(CITIES))

        emi_to_income = emi / monthly_income * 100
        loan_to_annual_income = loan_amount / (monthly_income * 12)

        risk_score, risk_category = rule_based_risk_score(
            credit_score,
            emi_to_income,
            loan_to_annual_income,
        )

        rows.append(
            {
                "customer_id": customer_id,
                "age": age,
                "city": city,
                "employment_type": employment_type,
                "monthly_income": round(monthly_income, 2),
                "credit_score": credit_score,
                "product": product,
                "loan_amount": round(loan_amount, 2),
                "tenure_months": tenure_months,
                "interest_rate": round(interest_rate, 2),
                "emi": round(emi, 2),
                "disbursement_date": date.today().isoformat(),
                "days_past_due": 0,
                # A newly simulated loan has no observed default yet.
                "default_flag": 0,
                "emi_to_income": round(emi_to_income, 4),
                "loan_to_annual_income": round(loan_to_annual_income, 4),
                "risk_score": risk_score,
                "risk_category": risk_category,
            }
        )

    new_df = pd.DataFrame(rows)

    # Score using the saved preprocessing + Random Forest pipeline.
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Saved model not found at {MODEL_PATH}. "
            "Run `python ml_risk_model.py` once before simulating new loans."
        )

    model = joblib.load(MODEL_PATH)

    model_features = [
        "age",
        "monthly_income",
        "credit_score",
        "loan_amount",
        "tenure_months",
        "interest_rate",
        "emi_to_income",
        "loan_to_annual_income",
        "product",
        "employment_type",
        "city",
    ]

    new_df["ml_predicted_probability"] = model.predict_proba(
        new_df[model_features]
    )[:, 1]

    new_df["ml_predicted_probability"] = new_df[
        "ml_predicted_probability"
    ].round(6)

    return new_df



def score_manual_loan(loan_data):
    """Build, score, and persist one loan submitted by a loan-originations system."""
    if not ML_DATA_PATH.exists():
        raise FileNotFoundError(f"Missing {ML_DATA_PATH}")

    existing = pd.read_csv(ML_DATA_PATH)
    customer_id = _next_customer_ids(existing["customer_id"], 1)[0]

    product = loan_data["product"]
    if product not in PRODUCTS:
        raise ValueError(f"Unsupported product: {product}")

    age = int(loan_data["age"])
    monthly_income = float(loan_data["monthly_income"])
    credit_score = int(loan_data["credit_score"])
    loan_amount = float(loan_data["loan_amount"])
    tenure_months = int(loan_data["tenure_months"])
    interest_rate = float(loan_data["interest_rate"])
    employment_type = str(loan_data["employment_type"])
    city = str(loan_data["city"])

    emi = float(calculate_emi(loan_amount, interest_rate, tenure_months))
    emi_to_income = emi / monthly_income * 100
    loan_to_annual_income = loan_amount / (monthly_income * 12)

    if emi > monthly_income:
        raise ValueError("Calculated EMI cannot exceed monthly income.")
    if emi_to_income > 45:
        raise ValueError("EMI-to-income ratio must not exceed 45% for this demo.")

    risk_score, risk_category = rule_based_risk_score(
        credit_score, emi_to_income, loan_to_annual_income
    )

    new_df = pd.DataFrame([{
        "customer_id": customer_id,
        "age": age,
        "city": city,
        "employment_type": employment_type,
        "monthly_income": round(monthly_income, 2),
        "credit_score": credit_score,
        "product": product,
        "loan_amount": round(loan_amount, 2),
        "tenure_months": tenure_months,
        "interest_rate": round(interest_rate, 2),
        "emi": round(emi, 2),
        "disbursement_date": date.today().isoformat(),
        "days_past_due": 0,
        # Newly originated loan: no observed default yet.
        "default_flag": 0,
        "emi_to_income": round(emi_to_income, 4),
        "loan_to_annual_income": round(loan_to_annual_income, 4),
        "risk_score": risk_score,
        "risk_category": risk_category,
    }])

    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Saved model not found at {MODEL_PATH}. Run ml_risk_model.py first.")

    model = joblib.load(MODEL_PATH)
    model_features = [
        "age", "monthly_income", "credit_score", "loan_amount",
        "tenure_months", "interest_rate", "emi_to_income",
        "loan_to_annual_income", "product", "employment_type", "city"
    ]

    new_df["ml_predicted_probability"] = model.predict_proba(
        new_df[model_features]
    )[:, 1].round(6)

    result = append_new_loans(new_df)
    return result


def append_new_loans(new_df):
    if new_df.empty:
        raise ValueError("No loans to append.")

    if not ML_DATA_PATH.exists():
        raise FileNotFoundError(f"Missing {ML_DATA_PATH}")
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"Missing {DB_PATH}. Run `python build_sqlite.py` first."
        )

    existing = pd.read_csv(ML_DATA_PATH)

    # Make the rule-based score a persistent part of the live analytical
    # dataset. Older project snapshots may not have these two columns yet.
    if "risk_score" not in existing.columns or "risk_category" not in existing.columns:
        existing["risk_score"], existing["risk_category"] = zip(
            *existing.apply(
                lambda r: rule_based_risk_score(
                    r["credit_score"],
                    r["emi_to_income"],
                    r["loan_to_annual_income"],
                ),
                axis=1,
            )
        )

    # Align the new records to the analytical dataset schema.
    missing_columns = [
        c for c in existing.columns
        if c not in new_df.columns
    ]
    if missing_columns:
        raise ValueError(
            f"New loan schema is missing columns: {missing_columns}"
        )

    new_df = new_df.reindex(columns=existing.columns)

    if new_df["customer_id"].duplicated().any():
        raise ValueError("Duplicate customer IDs generated.")

    if set(new_df["customer_id"]).intersection(existing["customer_id"]):
        raise ValueError("Generated customer IDs already exist.")

    combined = pd.concat([existing, new_df], ignore_index=True)
    combined.to_csv(ML_DATA_PATH, index=False)

    # Keep SQLite synchronized with the CSV analytical dataset.
    conn = sqlite3.connect(DB_PATH, timeout=30)
    try:
        db_count_before = conn.execute(
            "SELECT COUNT(*) FROM loan_portfolio"
        ).fetchone()[0]

        # Add rule-based risk columns to older SQLite snapshots if needed.
        db_columns = [
            row[1]
            for row in conn.execute(
                "PRAGMA table_info(loan_portfolio)"
            ).fetchall()
        ]

        if "risk_score" not in db_columns:
            conn.execute("ALTER TABLE loan_portfolio ADD COLUMN risk_score INTEGER")
            conn.execute("UPDATE loan_portfolio SET risk_score = CASE "
                         "WHEN credit_score < 580 THEN 40 "
                         "WHEN credit_score < 670 THEN 30 "
                         "WHEN credit_score < 740 THEN 20 "
                         "WHEN credit_score < 800 THEN 10 ELSE 0 END "
                         "+ CASE "
                         "WHEN emi_to_income < 15 THEN 0 "
                         "WHEN emi_to_income < 25 THEN 10 "
                         "WHEN emi_to_income < 35 THEN 25 ELSE 35 END "
                         "+ CASE "
                         "WHEN loan_to_annual_income < 0.5 THEN 0 "
                         "WHEN loan_to_annual_income < 1 THEN 5 "
                         "WHEN loan_to_annual_income < 2 THEN 10 "
                         "WHEN loan_to_annual_income < 3 THEN 20 ELSE 25 END")
            db_columns.append("risk_score")

        if "risk_category" not in db_columns:
            conn.execute("ALTER TABLE loan_portfolio ADD COLUMN risk_category TEXT")
            conn.execute("UPDATE loan_portfolio SET risk_category = CASE "
                         "WHEN risk_score <= 33 THEN 'Low' "
                         "WHEN risk_score <= 66 THEN 'Medium' "
                         "ELSE 'High' END")
            db_columns.append("risk_category")

        expected_columns = list(existing.columns)
        if db_columns != expected_columns:
            raise ValueError(
                "SQLite schema does not match the analytical CSV schema."
            )

        new_df.to_sql(
            "loan_portfolio",
            conn,
            if_exists="append",
            index=False,
        )

        db_count_after = conn.execute(
            "SELECT COUNT(*) FROM loan_portfolio"
        ).fetchone()[0]

        expected = db_count_before + len(new_df)
        if db_count_after != expected:
            raise RuntimeError(
                f"SQLite row-count validation failed: "
                f"expected {expected}, got {db_count_after}"
            )

        conn.commit()

    except Exception:
        conn.rollback()
        # CSV was already written; restore it from the pre-append data.
        existing.to_csv(ML_DATA_PATH, index=False)
        raise
    finally:
        conn.close()

    return {
        "added": len(new_df),
        "csv_total": len(combined),
        "sqlite_total": db_count_after,
        "new_loans": new_df,
    }


def simulate_and_append(n=20, seed=None):
    new_df = generate_new_loans(n=n, seed=seed)
    result = append_new_loans(new_df)

    return {
        "added": result["added"],
        "csv_total": result["csv_total"],
        "sqlite_total": result["sqlite_total"],
        "new_loans": result["new_loans"],
    }


if __name__ == "__main__":
    result = simulate_and_append(n=20, seed=42)

    print("=" * 70)
    print("LIVE LOAN SIMULATION COMPLETE")
    print("=" * 70)
    print(f"Loans added  : {result['added']}")
    print(f"CSV total    : {result['csv_total']}")
    print(f"SQLite total : {result['sqlite_total']}")
    print("\nNew loans:")
    print(
        result["new_loans"][
            [
                "customer_id",
                "product",
                "city",
                "credit_score",
                "emi_to_income",
                "risk_score",
                "risk_category",
                "ml_predicted_probability",
            ]
        ].to_string(index=False)
    )
