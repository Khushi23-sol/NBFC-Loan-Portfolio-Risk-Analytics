"""
ML Probability-of-Default Model (Addition to the Rule-Based Risk Score)
==========================================================================
This ADDS a trained ML model alongside your existing rule-based risk score
- it does not replace it. In interviews, you can now say: "I built a
rule-based scoring system first for transparency and explainability, then
validated it by training an ML model and comparing performance."

IMPORTANT: Run this AFTER your existing generate_data.py / notebook has
created loan_portfolio.csv. This reads that same file - column names below
match your documented schema exactly:
customer_id, age, city, employment_type, monthly_income, credit_score,
loan_amount, loan_type, tenure_months, interest_rate, emi, days_past_due,
default_flag, disbursement_date, emi_to_income, loan_to_annual_income

If your actual CSV has slightly different column names, adjust the
`features` list below to match.
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, classification_report, precision_score, recall_score

# --- Load your existing data ---
df = pd.read_csv("Data/loan_portfolio.csv")  # adjust path if running from a different folder

# If emi_to_income / loan_to_annual_income aren't already columns, compute them
# (they should already exist per your project - this is just a safety check)
if "emi_to_income" not in df.columns:
    df["emi_to_income"] = df["emi"] / df["monthly_income"] * 100
if "loan_to_annual_income" not in df.columns:
    df["loan_to_annual_income"] = df["loan_amount"] / (df["monthly_income"] * 12)

# --- Define features and target ---
features = [
    "age",
    "monthly_income",
    "credit_score",
    "loan_amount",
    "tenure_months",
    "interest_rate",
    "product",
    "employment_type",
    "city",
    "emi_to_income",
    "loan_to_annual_income"
]
target = "default_flag"

X = df[features]
y = df[target]

numeric_features = ["age", "monthly_income", "credit_score", "loan_amount", "tenure_months",
                     "interest_rate", "emi_to_income", "loan_to_annual_income"]
categorical_features = ["product", "employment_type", "city"]

preprocessor = ColumnTransformer([
    ("num", StandardScaler(), numeric_features),
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# --- Model 1: Logistic Regression (interpretable baseline) ---
logit_model = Pipeline([
    ("preprocess", preprocessor),
    ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced")),
])
logit_model.fit(X_train, y_train)
logit_proba = logit_model.predict_proba(X_test)[:, 1]
logit_auc = roc_auc_score(y_test, logit_proba)

# --- Model 2: Random Forest (more powerful, non-linear) ---
rf_model = Pipeline([
    ("preprocess", preprocessor),
    ("classifier", RandomForestClassifier(
        n_estimators=300, max_depth=8, min_samples_leaf=20,
        class_weight="balanced", random_state=42
    )),
])
rf_model.fit(X_train, y_train)
rf_proba = rf_model.predict_proba(X_test)[:, 1]
rf_auc = roc_auc_score(y_test, rf_proba)
rf_pred = rf_model.predict(X_test)

print("=" * 60)
print("ML PROBABILITY-OF-DEFAULT MODEL RESULTS")
print("=" * 60)
print(f"\nLogistic Regression ROC-AUC: {logit_auc:.3f}")
print(f"Random Forest ROC-AUC:       {rf_auc:.3f}")
print(f"\nPrecision (Random Forest, Default class): {precision_score(y_test, rf_pred):.3f}")
print(f"Recall (Random Forest, Default class):    {recall_score(y_test, rf_pred):.3f}")

print("\nFull Classification Report (Random Forest):")
print(classification_report(y_test, rf_pred, target_names=["No Default", "Default"]))

# --- Feature Importance ---
feature_names = (numeric_features +
                  list(rf_model.named_steps["preprocess"]
                       .named_transformers_["cat"]
                       .get_feature_names_out(categorical_features)))
importances = rf_model.named_steps["classifier"].feature_importances_
importance_df = pd.DataFrame({"feature": feature_names, "importance": importances}) \
    .sort_values("importance", ascending=False).head(10)
print("\nTop 10 ML-Identified Risk Drivers:")
print(importance_df.to_string(index=False))

# ------------------------------------------------------------
# SCORE ALL 8,000 LOANS WITH TRAINED RANDOM FOREST
# ------------------------------------------------------------

df["ml_predicted_probability"] = rf_model.predict_proba(X)[:, 1]

# Save ML-enhanced dataset
df.to_csv(
    "Data/loan_portfolio_with_ml.csv",
    index=False
)

print("\nML probabilities generated for all loans.")
print(
    "Probability coverage:",
    df["ml_predicted_probability"].notna().sum(),
    "/",
    len(df)
)

# --- Compare ML model against your existing rule-based score ---
if "risk_score" in df.columns or "customer_risk_score" in df.columns:
    score_col = "risk_score" if "risk_score" in df.columns else "customer_risk_score"
    test_indices = X_test.index
    rule_scores = df.loc[test_indices, score_col]
    correlation = np.corrcoef(rule_scores, rf_proba)[0, 1]
    print(f"\nCorrelation between rule-based score and ML predicted probability: {correlation:.3f}")
    print("(A positive correlation validates that your rule-based logic captures similar risk signal as the ML model)")
else:
    print("\nNote: rule-based risk_score column not found in this CSV - "
          "add it to df before running this comparison, or run this after your "
          "notebook has computed and saved it.")

# --- Save ML predictions alongside existing data ---
df.loc[X_test.index, "ml_predicted_probability"] = rf_proba
df.to_csv("Data/loan_portfolio_with_ml.csv", index=False)
print("\nSaved Data/loan_portfolio_with_ml.csv with ML predictions added.")
