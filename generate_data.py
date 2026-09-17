import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# ============================================================
# NBFC LOAN PORTFOLIO - SYNTHETIC DATA GENERATOR V2
# ============================================================

np.random.seed(42)

N = 8000

PRODUCTS = [
    "Personal Loan",
    "Home Loan",
    "Business Loan",
    "Gold Loan",
    "Vehicle Loan"
]

PRODUCT_WEIGHTS = [0.35, 0.20, 0.20, 0.15, 0.10]

CITIES = [
    "Mumbai", "Pune", "Delhi", "Bengaluru", "Chennai",
    "Hyderabad", "Ahmedabad", "Kolkata", "Jaipur", "Lucknow"
]

EMPLOYMENT_TYPES = [
    "Salaried",
    "Self-Employed",
    "Business Owner"
]

# Product-specific configuration
PRODUCT_CONFIG = {
    "Home Loan": {
        "loan_min": 1_500_000,
        "loan_max": 8_000_000,
        "tenures": [120, 180, 240, 300],
        "rate": (8.5, 11.5),
        "min_income": 35_000,
        "income_multiple": (2.5, 6.0)
    },

    "Business Loan": {
        "loan_min": 300_000,
        "loan_max": 5_000_000,
        "tenures": [12, 24, 36, 60],
        "rate": (11.0, 18.0),
        "min_income": 25_000,
        "income_multiple": (1.5, 4.0)
    },

    "Gold Loan": {
        "loan_min": 50_000,
        "loan_max": 1_500_000,
        "tenures": [6, 12, 18, 24],
        "rate": (9.0, 13.0),
        "min_income": 15_000,
        "income_multiple": (0.5, 2.5)
    },

    "Vehicle Loan": {
        "loan_min": 150_000,
        "loan_max": 1_200_000,
        "tenures": [24, 36, 48, 60],
        "rate": (9.5, 14.0),
        "min_income": 20_000,
        "income_multiple": (1.0, 3.0)
    },

    "Personal Loan": {
        "loan_min": 50_000,
        "loan_max": 1_000_000,
        "tenures": [12, 24, 36, 48],
        "rate": (11.5, 19.0),
        "min_income": 20_000,
        "income_multiple": (0.5, 3.0)
    }
}


def calculate_emi(principal, annual_rate, months):
    """Calculate monthly EMI using the standard reducing-balance formula."""
    
    monthly_rate = annual_rate / 12 / 100

    if monthly_rate == 0:
        return principal / months

    emi = (
        principal
        * monthly_rate
        * (1 + monthly_rate) ** months
        / ((1 + monthly_rate) ** months - 1)
    )

    return round(emi, 2)


rows = []

start_date = datetime(2023, 1, 1)


for i in range(N):

    # --------------------------------------------------------
    # 1. CUSTOMER PROFILE
    # --------------------------------------------------------

    age = int(np.clip(
        np.random.normal(38, 10),
        21,
        65
    ))

    city = np.random.choice(CITIES)

    employment_type = np.random.choice(
        EMPLOYMENT_TYPES,
        p=[0.55, 0.30, 0.15]
    )

    product = np.random.choice(
        PRODUCTS,
        p=PRODUCT_WEIGHTS
    )

    config = PRODUCT_CONFIG[product]


    # --------------------------------------------------------
    # 2. INCOME
    # --------------------------------------------------------

    monthly_income = int(np.clip(
        np.random.lognormal(mean=10.8, sigma=0.5),
        config["min_income"],
        500_000
    ))


    # --------------------------------------------------------
    # 3. CREDIT SCORE
    # --------------------------------------------------------

    credit_score = int(np.clip(
        np.random.normal(680, 90),
        300,
        900
    ))


    # --------------------------------------------------------
    # 4. LOAN TENURE & INTEREST RATE
    # --------------------------------------------------------

    tenure_months = int(
        np.random.choice(config["tenures"])
    )

    interest_rate = round(
        np.random.uniform(
            config["rate"][0],
            config["rate"][1]
        ),
        2
    )


    # --------------------------------------------------------
    # 5. AFFORDABILITY-BASED LOAN AMOUNT
    # --------------------------------------------------------

    annual_income = monthly_income * 12

    # Base loan amount linked to annual income
    income_multiple = np.random.uniform(
        config["income_multiple"][0],
        config["income_multiple"][1]
    )

    proposed_loan = annual_income * income_multiple

    # Maximum EMI burden allowed for the synthetic portfolio.
    # Most borrowers remain below 45%, while some higher-risk
    # borrowers can approach 50%.
    target_emi_ratio = np.random.uniform(0.20, 0.45)

    # Calculate maximum loan that fits the target EMI ratio
    monthly_rate = interest_rate / 12 / 100

    if monthly_rate == 0:
        max_affordable_loan = (
            monthly_income
            * target_emi_ratio
            * tenure_months
        )
    else:
        max_affordable_loan = (
            monthly_income
            * target_emi_ratio
            * (
                (1 + monthly_rate) ** tenure_months - 1
            )
            / (
                monthly_rate
                * (1 + monthly_rate) ** tenure_months
            )
        )

    # Final loan amount respects both:
    # 1. Product limits
    # 2. Borrower affordability
    upper_limit = min(
        config["loan_max"],
        max_affordable_loan
    )

    lower_limit = config["loan_min"]

    # If product minimum is too high for this borrower,
    # use a longer tenure or adjust the loan to remain realistic.
    if upper_limit < lower_limit:

        # Use the maximum affordable amount,
        # while ensuring a positive loan amount.
        loan_amount = max(
            25_000,
            int(upper_limit)
        )

    else:

        loan_amount = int(
            np.random.uniform(
                lower_limit,
                upper_limit
            )
        )


    # --------------------------------------------------------
    # 6. EMI
    # --------------------------------------------------------

    emi = calculate_emi(
        loan_amount,
        interest_rate,
        tenure_months
    )


    # --------------------------------------------------------
    # 7. RISK FEATURES
    # --------------------------------------------------------

    emi_to_income = emi / monthly_income

    loan_to_annual_income = (
        loan_amount / annual_income
    )


    # Credit risk component
    credit_risk = (
        (700 - credit_score) / 300
    )

    credit_risk = np.clip(
        credit_risk,
        0,
        1
    )


    # Affordability risk
    affordability_risk = np.clip(
        (emi_to_income - 0.20) / 0.30,
        0,
        1
    )


    # Employment risk
    employment_risk = {
        "Salaried": 0.00,
        "Self-Employed": 0.10,
        "Business Owner": 0.15
    }[employment_type]


    # Product risk
    product_risk = {
        "Home Loan": 0.00,
        "Gold Loan": 0.05,
        "Vehicle Loan": 0.08,
        "Business Loan": 0.12,
        "Personal Loan": 0.15
    }[product]


    # Combined risk score
    risk_score = (
        0.45 * credit_risk
        + 0.30 * affordability_risk
        + employment_risk
        + product_risk
        + np.random.uniform(0, 0.08)
    )

    risk_score = np.clip(
        risk_score,
        0,
        1
    )


    # --------------------------------------------------------
    # 8. DEFAULT FLAG
    # --------------------------------------------------------

    default_probability = np.clip(
        0.03 + risk_score * 0.30,
        0,
        0.50
    )

    default_flag = int(
        np.random.random() < default_probability
    )


    # --------------------------------------------------------
    # 9. DAYS PAST DUE
    # --------------------------------------------------------

    if default_flag == 1:

        dpd = int(
            np.random.uniform(90, 365)
        )

    else:

        dpd = int(
            np.random.choice(
                [0, 1, 7, 15, 30],
                p=[0.85, 0.05, 0.03, 0.03, 0.04]
            )
        )


    # --------------------------------------------------------
    # 10. DISBURSEMENT DATE
    # --------------------------------------------------------

    disbursement_date = (
        start_date
        + timedelta(
            days=int(
                np.random.uniform(0, 700)
            )
        )
    )


    # --------------------------------------------------------
    # 11. SAVE RECORD
    # --------------------------------------------------------

    rows.append({

        "customer_id":
            f"CUST{100000 + i}",

        "age":
            age,

        "city":
            city,

        "employment_type":
            employment_type,

        "monthly_income":
            monthly_income,

        "credit_score":
            credit_score,

        "product":
            product,

        "loan_amount":
            loan_amount,

        "tenure_months":
            tenure_months,

        "interest_rate":
            interest_rate,

        "emi":
            emi,

        "disbursement_date":
            disbursement_date.strftime("%Y-%m-%d"),

        "days_past_due":
            dpd,

        "default_flag":
            default_flag
    })


# ============================================================
# 12. CREATE DATAFRAME
# ============================================================

df = pd.DataFrame(rows)


# ============================================================
# 13. SAVE DATASET
# ============================================================

df.to_csv(
    "loan_portfolio.csv",
    index=False
)


# ============================================================
# 14. SUMMARY
# ============================================================

print(
    f"Generated {len(df)} records."
)

print(
    f"Default rate: "
    f"{df['default_flag'].mean() * 100:.1f}%"
)

print(
    f"Average loan amount: "
    f"₹{df['loan_amount'].mean():,.0f}"
)

print(
    f"Average monthly income: "
    f"₹{df['monthly_income'].mean():,.0f}"
)