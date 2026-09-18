import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    roc_auc_score,
    precision_score,
    recall_score,
    confusion_matrix
)

# ============================================================
# 1. LOAD DATA
# ============================================================

DATA_PATH = "Data/loan_portfolio.csv"

df = pd.read_csv(DATA_PATH)

# ============================================================
# 2. FEATURE ENGINEERING
# ============================================================

df["emi_to_income"] = (
    df["emi"] / df["monthly_income"]
)

df["loan_to_annual_income"] = (
    df["loan_amount"] /
    (df["monthly_income"] * 12)
)

# ============================================================
# 3. FEATURES & TARGET
# ============================================================

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

categorical_features = [
    "product",
    "employment_type",
    "city"
]

numeric_features = [
    "age",
    "monthly_income",
    "credit_score",
    "loan_amount",
    "tenure_months",
    "interest_rate",
    "emi_to_income",
    "loan_to_annual_income"
]

# ============================================================
# 4. PREPROCESSING
# ============================================================

numeric_transformer = Pipeline(
    steps=[
        (
            "scaler",
            StandardScaler()
        )
    ]
)

categorical_transformer = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="most_frequent")
        ),
        (
            "onehot",
            OneHotEncoder(
                handle_unknown="ignore",
                sparse_output=False
            )
        )
    ]
)

preprocessor = ColumnTransformer(
    transformers=[
        (
            "num",
            numeric_transformer,
            numeric_features
        ),
        (
            "cat",
            categorical_transformer,
            categorical_features
        )
    ]
)

# ============================================================
# 5. TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# ============================================================
# 6. MODELS
# ============================================================

logistic_model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        (
            "model",
            LogisticRegression(
                max_iter=1000,
                class_weight="balanced"
            )
        )
    ]
)

random_forest_model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        (
            "model",
            RandomForestClassifier(
                n_estimators=300,
                max_depth=8,
                min_samples_leaf=20,
                class_weight="balanced",
                random_state=42
            )
        )
    ]
)

# ============================================================
# 7. TRAIN MODELS
# ============================================================

logistic_model.fit(X_train, y_train)

random_forest_model.fit(X_train, y_train)

# ============================================================
# 8. PREDICTIONS
# ============================================================

logistic_probability = (
    logistic_model.predict_proba(X_test)[:, 1]
)

rf_probability = (
    random_forest_model.predict_proba(X_test)[:, 1]
)

rf_prediction = (
    random_forest_model.predict(X_test)
)

# ============================================================
# 9. MODEL METRICS
# ============================================================

logistic_auc = roc_auc_score(
    y_test,
    logistic_probability
)

rf_auc = roc_auc_score(
    y_test,
    rf_probability
)

rf_precision = precision_score(
    y_test,
    rf_prediction,
    zero_division=0
)

rf_recall = recall_score(
    y_test,
    rf_prediction,
    zero_division=0
)

# ============================================================
# 10. SAVE MODEL COMPARISON
# ============================================================

metrics_df = pd.DataFrame({
    "model": [
        "Logistic Regression",
        "Random Forest"
    ],
    "roc_auc": [
        logistic_auc,
        rf_auc
    ],
    "precision_default_class": [
        None,
        rf_precision
    ],
    "recall_default_class": [
        None,
        rf_recall
    ]
})

metrics_df.to_csv(
    "Data/ml_model_metrics.csv",
    index=False
)

# ============================================================
# 11. CONFUSION MATRIX
# ============================================================

cm = confusion_matrix(
    y_test,
    rf_prediction
)

confusion_df = pd.DataFrame(
    cm,
    index=[
        "Actual No Default",
        "Actual Default"
    ],
    columns=[
        "Predicted No Default",
        "Predicted Default"
    ]
)

confusion_df.to_csv(
    "Data/ml_confusion_matrix.csv"
)

# ============================================================
# 12. RANDOM FOREST FEATURE IMPORTANCE
# ============================================================

rf_preprocessor = (
    random_forest_model
    .named_steps["preprocessor"]
)

rf_model = (
    random_forest_model
    .named_steps["model"]
)

feature_names = (
    rf_preprocessor
    .get_feature_names_out()
)

importance_df = pd.DataFrame({
    "feature": feature_names,
    "importance": rf_model.feature_importances_
})

importance_df = (
    importance_df
    .sort_values(
        "importance",
        ascending=False
    )
    .reset_index(drop=True)
)

importance_df.to_csv(
    "Data/ml_feature_importance.csv",
    index=False
)

# ============================================================
# 13. DISPLAY RESULTS
# ============================================================

print("\n" + "=" * 60)
print("ML MODEL EVALUATION")
print("=" * 60)

print(
    f"\nLogistic Regression ROC-AUC: "
    f"{logistic_auc:.3f}"
)

print(
    f"Random Forest ROC-AUC: "
    f"{rf_auc:.3f}"
)

print(
    f"\nRandom Forest Precision: "
    f"{rf_precision:.3f}"
)

print(
    f"Random Forest Recall: "
    f"{rf_recall:.3f}"
)

print("\nConfusion Matrix:")
print(confusion_df)

print("\nTop 10 Random Forest Risk Drivers:")
print(
    importance_df.head(10).to_string(
        index=False
    )
)

print("\nSaved files:")
print("Data/ml_model_metrics.csv")
print("Data/ml_confusion_matrix.csv")
print("Data/ml_feature_importance.csv")

print("\nML evaluation completed successfully.")