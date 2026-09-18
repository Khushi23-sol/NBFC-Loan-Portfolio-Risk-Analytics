import streamlit as st
import requests
import pandas as pd

# ============================================================
# CONFIGURATION
# ============================================================

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="NBFC Portfolio Risk Analytics",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# HELPER FUNCTION
# ============================================================

def get_api_data(endpoint, params=None):

    try:

        response = requests.get(
            f"{API_URL}{endpoint}",
            params=params,
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:

        st.error(
            "FastAPI backend is not reachable. "
            "Please make sure the FastAPI server is running."
        )

        st.code(str(e))

        return None


# ============================================================
# TITLE
# ============================================================

st.title("NBFC Loan Portfolio Risk & Analytics")

st.caption(
    "Machine Learning • SQL Analytics • Portfolio Risk • Collections"
)


# ============================================================
# PORTFOLIO FILTERS
# ============================================================

st.subheader("Portfolio Filters")

filter_col1, filter_col2, filter_col3 = st.columns(3)


with filter_col1:

    selected_product = st.selectbox(
        "Product",
        [
            "All",
            "Business Loan",
            "Personal Loan",
            "Vehicle Loan",
            "Gold Loan",
            "Home Loan"
        ]
    )


with filter_col2:

    selected_city = st.selectbox(
        "City",
        [
            "All",
            "Mumbai",
            "Delhi",
            "Bengaluru",
            "Hyderabad",
            "Chennai",
            "Pune",
            "Kolkata",
            "Ahmedabad",
            "Jaipur",
            "Lucknow"
        ]
    )


with filter_col3:

    selected_credit_band = st.selectbox(
        "Credit Band",
        [
            "All",
            "Poor",
            "Fair",
            "Good",
            "Very Good",
            "Excellent"
        ]
    )


# Common parameters used by all filtered endpoints

filter_params = {
    "product": selected_product,
    "city": selected_city,
    "credit_band": selected_credit_band
}


st.divider()


# ============================================================
# 1. PORTFOLIO SUMMARY
# ============================================================

st.header("Portfolio Overview")

summary = get_api_data(
    "/api/portfolio/summary",
    params=filter_params
)


if summary:

    total_loans = summary["total_loans"]
    total_exposure = summary["total_exposure"]
    total_defaults = summary["total_defaults"]
    default_rate = summary["default_rate_pct"]
    exposure_90_dpd = summary["exposure_90_plus_dpd"]


    col1, col2, col3, col4, col5 = st.columns(5)


    col1.metric(
        "Total Loans",
        f"{total_loans:,}"
    )


    col2.metric(
        "Total Exposure",
        f"₹{total_exposure / 10_000_000:.2f} Cr"
    )


    col3.metric(
        "Total Defaults",
        f"{total_defaults:,}"
    )


    col4.metric(
        "Default Rate",
        f"{default_rate:.2f}%"
    )


    col5.metric(
        "90+ DPD Exposure",
        f"₹{exposure_90_dpd / 10_000_000:.2f} Cr"
    )


st.divider()


# ============================================================
# 2. PRODUCT RISK
# ============================================================

st.header("Product-wise Risk")

product_data = get_api_data(
    "/api/portfolio/product-risk",
    params=filter_params
)


if product_data:

    product_df = pd.DataFrame(product_data)


    col1, col2 = st.columns(2)


    with col1:

        st.subheader("Default Rate by Product")

        chart_data = product_df.set_index(
            "product"
        )[["default_rate_pct"]]

        st.bar_chart(chart_data)


    with col2:

        st.subheader("Product Risk Table")

        display_df = product_df.copy()

        display_df["exposure"] = (
            display_df["exposure"] / 10_000_000
        ).round(2)


        display_df = display_df.rename(
            columns={
                "product": "Product",
                "total_loans": "Loans",
                "exposure": "Exposure (Cr)",
                "defaults": "Defaults",
                "default_rate_pct": "Default Rate (%)"
            }
        )


        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )


st.divider()


# ============================================================
# 3. CREDIT RISK
# ============================================================

st.header("Credit Score Risk Analysis")

credit_data = get_api_data(
    "/api/portfolio/credit-risk",
    params=filter_params
)


if credit_data:

    credit_df = pd.DataFrame(credit_data)


    col1, col2 = st.columns(2)


    with col1:

        st.subheader("Default Rate by Credit Band")

        chart_data = credit_df.set_index(
            "credit_band"
        )[["default_rate_pct"]]

        st.bar_chart(chart_data)


    with col2:

        st.subheader("Credit Risk Table")

        display_df = credit_df.copy()

        display_df["exposure"] = (
            display_df["exposure"] / 10_000_000
        ).round(2)


        display_df = display_df.rename(
            columns={
                "credit_band": "Credit Band",
                "total_loans": "Loans",
                "defaults": "Defaults",
                "default_rate_pct": "Default Rate (%)",
                "exposure": "Exposure (Cr)"
            }
        )


        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )


st.divider()


# ============================================================
# 4. CITY RISK
# ============================================================

st.header("Geographic Risk Analysis")

city_data = get_api_data(
    "/api/portfolio/city-risk",
    params=filter_params
)


if city_data:

    city_df = pd.DataFrame(city_data)


    col1, col2 = st.columns(2)


    with col1:

        st.subheader("Default Rate by City")

        chart_data = city_df.set_index(
            "city"
        )[["default_rate_pct"]]

        st.bar_chart(chart_data)


    with col2:

        st.subheader("City Risk Table")

        display_df = city_df.copy()

        display_df["exposure"] = (
            display_df["exposure"] / 10_000_000
        ).round(2)


        display_df = display_df.rename(
            columns={
                "city": "City",
                "total_loans": "Loans",
                "defaults": "Defaults",
                "default_rate_pct": "Default Rate (%)",
                "exposure": "Exposure (Cr)"
            }
        )


        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )


st.divider()


# ============================================================
# 5. VINTAGE / COHORT ANALYSIS
# ============================================================

st.header("Vintage / Cohort Analysis")

vintage_data = get_api_data(
    "/api/portfolio/vintage",
    params=filter_params
)


if vintage_data:

    vintage_df = pd.DataFrame(vintage_data)


    chart_data = vintage_df.set_index(
        "disbursement_quarter"
    )[["cohort_default_rate_pct"]]


    st.line_chart(chart_data)


    display_df = vintage_df.copy()

    display_df["cohort_exposure"] = (
        display_df["cohort_exposure"] / 10_000_000
    ).round(2)


    display_df = display_df.rename(
        columns={
            "disbursement_quarter": "Quarter",
            "loans_in_cohort": "Loans",
            "cohort_exposure": "Exposure (Cr)",
            "defaults": "Defaults",
            "cohort_default_rate_pct": "Default Rate (%)"
        }
    )


    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )


st.divider()


# ============================================================
# 6. ML HIGH-RISK LOANS
# ============================================================

st.header("ML-Predicted High-Risk Loans")

ml_data = get_api_data(
    "/api/risk/high-risk-loans",
    params=filter_params
)


if ml_data:

    ml_df = pd.DataFrame(ml_data)


    ml_df["loan_amount"] = (
        ml_df["loan_amount"] / 100_000
    ).round(2)


    ml_df["ml_predicted_probability"] = (
        ml_df["ml_predicted_probability"] * 100
    ).round(2)


    display_df = ml_df.rename(
        columns={
            "customer_id": "Customer ID",
            "product": "Product",
            "city": "City",
            "loan_amount": "Loan Amount (₹ Lakh)",
            "credit_score": "Credit Score",
            "emi_to_income": "EMI / Income (%)",
            "ml_predicted_probability": "ML Default Probability (%)"
        }
    )


    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )


st.divider()


# ============================================================
# 7. ML MODEL EVALUATION
# ============================================================

st.header("Machine Learning Model Evaluation")

st.caption(
    "Random Forest vs Logistic Regression for loan default prediction"
)


try:

    metrics_df = pd.read_csv(
        "Data/ml_model_metrics.csv"
    )


    importance_df = pd.read_csv(
        "Data/ml_feature_importance.csv"
    )


    confusion_df = pd.read_csv(
        "Data/ml_confusion_matrix.csv",
        index_col=0
    )


    # --------------------------------------------------------
    # MODEL METRICS
    # --------------------------------------------------------

    logistic_auc = metrics_df.loc[
        metrics_df["model"] == "Logistic Regression",
        "roc_auc"
    ].iloc[0]


    rf_auc = metrics_df.loc[
        metrics_df["model"] == "Random Forest",
        "roc_auc"
    ].iloc[0]


    rf_precision = metrics_df.loc[
        metrics_df["model"] == "Random Forest",
        "precision_default_class"
    ].iloc[0]


    rf_recall = metrics_df.loc[
        metrics_df["model"] == "Random Forest",
        "recall_default_class"
    ].iloc[0]


    col1, col2, col3, col4 = st.columns(4)


    col1.metric(
        "Logistic Regression ROC-AUC",
        f"{logistic_auc:.3f}"
    )


    col2.metric(
        "Random Forest ROC-AUC",
        f"{rf_auc:.3f}"
    )


    col3.metric(
        "RF Precision",
        f"{rf_precision:.3f}"
    )


    col4.metric(
        "RF Recall",
        f"{rf_recall:.3f}"
    )


    # --------------------------------------------------------
    # MODEL COMPARISON
    # --------------------------------------------------------

    st.subheader("ROC-AUC Model Comparison")


    model_chart = metrics_df[
        ["model", "roc_auc"]
    ].set_index("model")


    st.bar_chart(model_chart)


    # --------------------------------------------------------
    # CONFUSION MATRIX
    # --------------------------------------------------------

    st.subheader("Random Forest Confusion Matrix")


    st.dataframe(
        confusion_df,
        use_container_width=True
    )


    # --------------------------------------------------------
    # FEATURE IMPORTANCE
    # --------------------------------------------------------

    st.subheader(
        "Top ML-Identified Risk Features"
    )


    importance_display = (
        importance_df
        .head(10)
        .copy()
    )


    importance_display["feature"] = (
        importance_display["feature"]
        .str.replace(
            "num__",
            "",
            regex=False
        )
        .str.replace(
            "cat__",
            "",
            regex=False
        )
    )


    importance_display["importance"] = (
        importance_display["importance"]
        .round(4)
    )


    importance_display = (
        importance_display
        .rename(
            columns={
                "feature": "Feature",
                "importance": "Importance"
            }
        )
    )


    st.bar_chart(
        importance_display.set_index(
            "Feature"
        )
    )


    st.dataframe(
        importance_display,
        use_container_width=True,
        hide_index=True
    )


except Exception as e:

    st.error(
        "ML evaluation files could not be loaded."
    )

    st.code(str(e))


st.divider()


# ============================================================
# 8. COLLECTIONS PRIORITY
# ============================================================

st.header("Collections Priority")

collections_data = get_api_data(
    "/api/collections/priority",
    params=filter_params
)


if collections_data:

    collections_df = pd.DataFrame(
        collections_data
    )


    collections_df["loan_amount"] = (
        collections_df["loan_amount"] / 100_000
    ).round(2)


    collections_df["ml_predicted_probability"] = (
        collections_df["ml_predicted_probability"] * 100
    ).round(2)


    display_df = collections_df.rename(
        columns={
            "customer_id": "Customer ID",
            "product": "Product",
            "city": "City",
            "loan_amount": "Loan Amount (₹ Lakh)",
            "days_past_due": "DPD",
            "credit_score": "Credit Score",
            "emi_to_income": "EMI / Income (%)",
            "ml_predicted_probability": "ML Default Probability (%)"
        }
    )


    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )


st.divider()


# ============================================================
# FOOTER
# ============================================================

st.caption(
    "NBFC Loan Portfolio Risk & Analytics | "
    "FastAPI + SQLite + Streamlit + scikit-learn"
)