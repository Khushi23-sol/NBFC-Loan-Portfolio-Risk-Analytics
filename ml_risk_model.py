"""
NBFC Loan Portfolio Risk Analytics — ML Model Training

Trains Logistic Regression and Random Forest models on the original
synthetic loan portfolio, evaluates them, writes the ML-enriched dataset,
and saves the complete Random Forest preprocessing + model pipeline for
scoring newly simulated loans without retraining.

Important:
- `days_past_due` is intentionally excluded from ML features to avoid
  target leakage.
- The existing rule-based risk score is not replaced.
- The raw source dataset is never modified.
"""

import os
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "Data" / "loan_portfolio.csv"
OUTPUT_PATH = BASE_DIR / "Data" / "loan_portfolio_with_ml.csv"
METRICS_PATH = BASE_DIR / "Data" / "ml_model_metrics.csv"
CONFUSION_PATH = BASE_DIR / "Data" / "ml_confusion_matrix.csv"
IMPORTANCE_PATH = BASE_DIR / "Data" / "ml_feature_importance.csv"
MODEL_DIR = BASE_DIR / "models"
MODEL_PATH = MODEL_DIR / "rf_risk_pipeline.joblib"

RANDOM_STATE = 42

if not DATA_PATH.exists():
    raise FileNotFoundError(f"Could not find {DATA_PATH}")

df = pd.read_csv(DATA_PATH)

required = [
    "customer_id", "age", "city", "employment_type", "monthly_income",
    "credit_score", "product", "loan_amount", "tenure_months",
    "interest_rate", "emi", "disbursement_date", "days_past_due",
    "default_flag",
]
missing = [c for c in required if c not in df.columns]
if missing:
    raise ValueError(f"Missing required columns: {missing}")

# Recreate analytical numeric features if necessary.
if "emi_to_income" not in df.columns:
    df["emi_to_income"] = np.where(
        df["monthly_income"] > 0,
        df["emi"] / df["monthly_income"] * 100,
        np.nan,
    )

if "loan_to_annual_income" not in df.columns:
    df["loan_to_annual_income"] = np.where(
        df["monthly_income"] > 0,
        df["loan_amount"] / (df["monthly_income"] * 12),
        np.nan,
    )

numeric_features = [
    "age",
    "monthly_income",
    "credit_score",
    "loan_amount",
    "tenure_months",
    "interest_rate",
    "emi_to_income",
    "loan_to_annual_income",
]
categorical_features = ["product", "employment_type", "city"]
features = numeric_features + categorical_features

X = df[features].copy()
y = df["default_flag"].astype(int)

if X.isna().any().any():
    raise ValueError("Missing values found in model features.")

if y.nunique() != 2:
    raise ValueError("default_flag must contain exactly two classes.")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=RANDOM_STATE,
    stratify=y,
)

def make_preprocessor():
    return ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_features),
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ]
    )

logit_model = Pipeline(
    steps=[
        ("preprocess", make_preprocessor()),
        (
            "classifier",
            LogisticRegression(
                max_iter=1000,
                class_weight="balanced",
                random_state=RANDOM_STATE,
            ),
        ),
    ]
)

rf_model = Pipeline(
    steps=[
        ("preprocess", make_preprocessor()),
        (
            "classifier",
            RandomForestClassifier(
                n_estimators=300,
                max_depth=8,
                min_samples_leaf=20,
                class_weight="balanced",
                random_state=RANDOM_STATE,
                n_jobs=-1,
            ),
        ),
    ]
)

logit_model.fit(X_train, y_train)
rf_model.fit(X_train, y_train)

logit_proba = logit_model.predict_proba(X_test)[:, 1]
rf_proba = rf_model.predict_proba(X_test)[:, 1]

logit_pred = (logit_proba >= 0.50).astype(int)
rf_pred = (rf_proba >= 0.50).astype(int)

metrics_df = pd.DataFrame(
    {
        "model": ["Logistic Regression", "Random Forest"],
        "roc_auc": [
            roc_auc_score(y_test, logit_proba),
            roc_auc_score(y_test, rf_proba),
        ],
        "precision_default_class": [
            precision_score(y_test, logit_pred, zero_division=0),
            precision_score(y_test, rf_pred, zero_division=0),
        ],
        "recall_default_class": [
            recall_score(y_test, logit_pred, zero_division=0),
            recall_score(y_test, rf_pred, zero_division=0),
        ],
    }
)

report = classification_report(
    y_test,
    rf_pred,
    output_dict=True,
    zero_division=0,
)

print("\nRandom Forest classification report:")
print(classification_report(y_test, rf_pred, zero_division=0))

cm = confusion_matrix(y_test, rf_pred)
confusion_df = pd.DataFrame(
    cm,
    index=["Actual No Default", "Actual Default"],
    columns=["Predicted No Default", "Predicted Default"],
)

# Feature importance from the fitted RF pipeline.
preprocessor = rf_model.named_steps["preprocess"]
classifier = rf_model.named_steps["classifier"]
feature_names = preprocessor.get_feature_names_out()

importance_df = pd.DataFrame(
    {
        "feature": feature_names,
        "importance": classifier.feature_importances_,
    }
).sort_values("importance", ascending=False)

# Score the complete analytical dataset.
df["ml_predicted_probability"] = rf_model.predict_proba(X)[:, 1]

MODEL_DIR.mkdir(parents=True, exist_ok=True)

# Save the complete preprocessing + RF pipeline.
joblib.dump(rf_model, MODEL_PATH)

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT_PATH, index=False)
metrics_df.to_csv(METRICS_PATH, index=False)
confusion_df.to_csv(CONFUSION_PATH)
importance_df.to_csv(IMPORTANCE_PATH, index=False)

print("=" * 70)
print("ML PIPELINE COMPLETE")
print("=" * 70)
print(f"Rows scored              : {len(df):,}")
print(f"Logistic Regression AUC  : {metrics_df.iloc[0]['roc_auc']:.3f}")
print(f"Random Forest AUC        : {metrics_df.iloc[1]['roc_auc']:.3f}")
print(f"Saved ML dataset         : {OUTPUT_PATH}")
print(f"Saved model pipeline     : {MODEL_PATH}")
print("=" * 70)
