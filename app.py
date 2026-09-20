import os
import requests
import pandas as pd
import streamlit as st

# ============================================================
# CONFIG
# ============================================================

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="NBFC Risk Analytics",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# STYLING
# ============================================================

st.markdown(
    """
    <style>
    /* ---------- APP SHELL ---------- */
    .stApp {
        background:
            radial-gradient(circle at 8% 0%, rgba(59,130,246,.08), transparent 28%),
            radial-gradient(circle at 92% 10%, rgba(139,92,246,.07), transparent 26%);
    }

    .block-container {
        padding-top: 1.15rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }

    /* ---------- HEADER ---------- */
    .app-title {
        font-size: 2.45rem;
        font-weight: 850;
        margin-bottom: 0.1rem;
        letter-spacing: -0.9px;
        line-height: 1.15;
    }

    .app-subtitle {
        color: #9ca3af;
        font-size: 0.98rem;
        margin-bottom: 1.45rem;
    }

    /* ---------- HERO ---------- */
    .hero {
        position: relative;
        overflow: hidden;
        padding: 1.55rem 1.7rem;
        border-radius: 1.15rem;
        border: 1px solid rgba(148,163,184,.20);
        background:
            linear-gradient(135deg, rgba(37,99,235,.16), rgba(124,58,237,.08)),
            rgba(15,23,42,.38);
        box-shadow: 0 14px 35px rgba(0,0,0,.12);
        margin-bottom: 1.25rem;
    }

    .hero:after {
        content: "";
        position: absolute;
        width: 180px;
        height: 180px;
        right: -55px;
        top: -75px;
        border-radius: 50%;
        background: rgba(96,165,250,.09);
    }

    .hero h2 {
        margin: 0;
        font-size: 1.62rem;
        font-weight: 800;
        position: relative;
        z-index: 1;
    }

    .hero p {
        margin: 0.45rem 0 0;
        color: #aeb4bf;
        position: relative;
        z-index: 1;
        line-height: 1.55;
    }

    /* ---------- KPI CARDS ---------- */
    div[data-testid="stMetric"] {
        border: 1px solid rgba(148,163,184,.17);
        border-radius: 0.9rem;
        padding: 0.78rem 0.9rem;
        background: rgba(15,23,42,.30);
        box-shadow: 0 7px 20px rgba(0,0,0,.08);
    }

    div[data-testid="stMetric"] label {
        color: #9ca3af;
    }

    div[data-testid="stMetricValue"] {
        font-weight: 800;
    }

    /* ---------- SIDEBAR ---------- */
    section[data-testid="stSidebar"] {
        border-right: 1px solid rgba(148,163,184,.14);
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.2rem;
    }

    .nav-label {
        color: #64748b;
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        font-weight: 700;
        margin-bottom: 0.55rem;
    }

    .nav-link {
        display: block;
        padding: 0.68rem 0.78rem;
        margin: 0.16rem 0;
        border-radius: 0.68rem;
        text-decoration: none !important;
        color: #cbd5e1 !important;
        border: 1px solid transparent;
        font-size: 0.91rem;
        transition: all .15s ease;
    }

    .nav-link:hover {
        background: rgba(59,130,246,.08);
        border-color: rgba(96,165,250,.16);
        transform: translateX(2px);
    }

    .nav-link.active {
        background: linear-gradient(90deg, rgba(37,99,235,.22), rgba(124,58,237,.10));
        border-color: rgba(96,165,250,.25);
        color: #ffffff !important;
        font-weight: 750;
        box-shadow: inset 3px 0 0 #60a5fa;
    }

    .status-card {
        padding: 0.68rem 0.78rem;
        border-radius: 0.68rem;
        border: 1px solid rgba(148,163,184,.16);
        background: rgba(15,23,42,.24);
        margin-bottom: 0.42rem;
        font-size: 0.84rem;
    }

    /* ---------- PROFILE / INFO ---------- */
    .profile-card {
        padding: 1.25rem 1.35rem;
        border-radius: 0.95rem;
        border: 1px solid rgba(148,163,184,.18);
        background: rgba(15,23,42,.28);
        box-shadow: 0 10px 28px rgba(0,0,0,.08);
        min-height: 150px;
    }

    .small-muted {
        color: #9ca3af;
        font-size: 0.84rem;
    }

    /* ---------- TABLES ---------- */
    div[data-testid="stDataFrame"] {
        border-radius: 0.8rem;
        overflow: hidden;
        border: 1px solid rgba(148,163,184,.14);
    }

    /* ---------- BUTTONS ---------- */
    .stButton > button,
    .stLinkButton > a {
        border-radius: 0.65rem;
        font-weight: 650;
    }

    /* ---------- DIVIDERS ---------- */
    hr {
        border-color: rgba(148,163,184,.13);
    }

    /* ---------- MOBILE ---------- */
    @media (max-width: 900px) {
        .app-title {
            font-size: 1.85rem;
        }

        .hero {
            padding: 1.15rem;
        }
    }
    </style>

<style>
/* ---------- PREMIUM FINTECH / SAAS UI ---------- */
:root {
    --bg: #07111f;
    --panel: rgba(15, 28, 48, 0.82);
    --panel-2: rgba(20, 37, 61, 0.72);
    --border: rgba(148, 163, 184, 0.16);
    --text: #edf4ff;
    --muted: #91a4bd;
    --accent: #6ea8ff;
    --accent-2: #8b7cff;
}

.stApp {
    background:
        radial-gradient(circle at 8% 5%, rgba(80, 130, 255, .13), transparent 28%),
        radial-gradient(circle at 92% 10%, rgba(139, 124, 255, .11), transparent 25%),
        linear-gradient(145deg, #050b14 0%, #091525 48%, #07111f 100%);
    color: var(--text);
}

.block-container {
    max-width: 1480px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background:
        linear-gradient(180deg, rgba(7,17,31,.98), rgba(9,20,35,.98));
    border-right: 1px solid rgba(148,163,184,.12);
}
section[data-testid="stSidebar"] > div {
    padding-top: 1.2rem;
}
.nav-link {
    border: 1px solid transparent !important;
    background: transparent !important;
    border-radius: 12px !important;
    transition: all .18s ease !important;
}
.nav-link:hover {
    background: rgba(110,168,255,.08) !important;
    border-color: rgba(110,168,255,.15) !important;
    transform: translateX(2px);
}
.nav-link.active {
    background: linear-gradient(90deg, rgba(110,168,255,.16), rgba(139,124,255,.08)) !important;
    border-color: rgba(110,168,255,.22) !important;
    box-shadow: inset 3px 0 0 #6ea8ff, 0 8px 24px rgba(0,0,0,.12);
}

/* Hero */
.hero-shell {
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(148,163,184,.15);
    border-radius: 24px;
    padding: 34px 38px;
    margin-bottom: 24px;
    background:
        radial-gradient(circle at 85% 20%, rgba(139,124,255,.18), transparent 26%),
        radial-gradient(circle at 10% 90%, rgba(110,168,255,.12), transparent 25%),
        linear-gradient(135deg, rgba(20,37,61,.92), rgba(8,18,32,.96));
    box-shadow: 0 24px 70px rgba(0,0,0,.25);
}
.hero-shell:after {
    content: "";
    position: absolute;
    right: -100px;
    top: -110px;
    width: 280px;
    height: 280px;
    border-radius: 50%;
    border: 1px solid rgba(110,168,255,.12);
    box-shadow: 0 0 0 35px rgba(110,168,255,.025), 0 0 0 70px rgba(110,168,255,.018);
}
.hero-kicker {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-size: .72rem;
    font-weight: 800;
    letter-spacing: .14em;
    color: #9fc3ff;
    text-transform: uppercase;
    margin-bottom: 12px;
}
.hero-title {
    font-size: clamp(2rem, 4vw, 3.5rem);
    line-height: 1.02;
    font-weight: 850;
    letter-spacing: -.045em;
    margin: 0 0 12px;
}
.hero-sub {
    max-width: 760px;
    color: #a9bad0;
    font-size: 1rem;
    line-height: 1.65;
    margin: 0;
}
.hero-chip-row {
    display: flex;
    gap: 9px;
    flex-wrap: wrap;
    margin-top: 22px;
}
.hero-chip {
    border: 1px solid rgba(148,163,184,.16);
    background: rgba(255,255,255,.035);
    border-radius: 999px;
    padding: 7px 12px;
    color: #b9c9dc;
    font-size: .76rem;
}

/* KPI cards */
div[data-testid="stMetric"] {
    background: linear-gradient(145deg, rgba(18,35,57,.88), rgba(10,23,39,.9));
    border: 1px solid rgba(148,163,184,.14);
    border-radius: 17px;
    padding: 18px 18px 15px;
    box-shadow: 0 12px 35px rgba(0,0,0,.16);
    min-height: 122px;
    transition: transform .18s ease, border-color .18s ease;
}
div[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    border-color: rgba(110,168,255,.30);
}
div[data-testid="stMetricLabel"] {
    color: #91a4bd !important;
    font-size: .78rem !important;
    font-weight: 650 !important;
}
div[data-testid="stMetricValue"] {
    color: #f2f7ff !important;
    font-weight: 800 !important;
    letter-spacing: -.025em;
}

/* Content cards */
.ui-card {
    border: 1px solid rgba(148,163,184,.14);
    border-radius: 18px;
    padding: 20px 21px;
    background: linear-gradient(145deg, rgba(18,35,57,.76), rgba(9,21,36,.82));
    box-shadow: 0 15px 40px rgba(0,0,0,.13);
    margin-bottom: 16px;
}
.section-kicker {
    color: #7fb0ff;
    font-size: .68rem;
    font-weight: 800;
    letter-spacing: .14em;
    text-transform: uppercase;
    margin-bottom: 5px;
}
.section-title {
    font-size: 1.35rem;
    font-weight: 780;
    letter-spacing: -.025em;
    color: #edf4ff;
    margin-bottom: 4px;
}
.section-desc {
    color: #8fa4bd;
    font-size: .86rem;
    line-height: 1.5;
}

/* Dataframes */
div[data-testid="stDataFrame"] {
    border: 1px solid rgba(148,163,184,.14);
    border-radius: 15px;
    overflow: hidden;
    box-shadow: 0 12px 30px rgba(0,0,0,.10);
}

/* Inputs */
div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div,
div[data-baseweb="textarea"] > div {
    background: rgba(9,21,36,.75) !important;
    border-color: rgba(148,163,184,.16) !important;
    border-radius: 11px !important;
}
div[data-baseweb="input"] input,
div[data-baseweb="textarea"] textarea {
    color: #edf4ff !important;
}

/* Buttons */
.stButton > button, .stDownloadButton > button {
    border-radius: 11px !important;
    border: 1px solid rgba(110,168,255,.20) !important;
    background: linear-gradient(135deg, rgba(110,168,255,.16), rgba(139,124,255,.12)) !important;
    color: #eaf2ff !important;
    font-weight: 700 !important;
    transition: all .18s ease !important;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    border-color: rgba(110,168,255,.42) !important;
    transform: translateY(-1px);
    box-shadow: 0 8px 24px rgba(44,89,160,.18);
}

/* Tabs */
button[data-baseweb="tab"] {
    color: #8fa4bd !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #dceaff !important;
}

/* Alerts */
div[data-testid="stAlert"] {
    border-radius: 13px;
}

/* Scrollbars */
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: #07111f; }
::-webkit-scrollbar-thumb {
    background: rgba(125,148,180,.35);
    border-radius: 999px;
}
::-webkit-scrollbar-thumb:hover {
    background: rgba(125,148,180,.55);
}

/* Footer */
.pro-footer {
    margin-top: 44px;
    padding-top: 18px;
    border-top: 1px solid rgba(148,163,184,.10);
    color: #71849d;
    font-size: .72rem;
    display: flex;
    justify-content: space-between;
    gap: 12px;
    flex-wrap: wrap;
}

@media (max-width: 800px) {
    .block-container { padding-left: 1rem; padding-right: 1rem; }
    .hero-shell { padding: 25px 22px; border-radius: 19px; }
    .hero-title { font-size: 2.15rem; }
}
</style>


    """,
    unsafe_allow_html=True,
)

# ============================================================
# PAGE NAVIGATION
# ============================================================

PAGES = {
    "overview": "🏠 Overview",
    "origination": "📝 Loan Origination",
    "portfolio": "📊 Portfolio Risk",
    "ml": "🤖 ML Risk",
    "vintage": "📅 Vintage Analysis",
    "collections": "💰 Collections",
    "simulator": "🔄 Loan Simulator",
    "about": "ℹ️ About Project",
}

page_key = st.query_params.get("page", "overview")
if page_key not in PAGES:
    page_key = "overview"

# ============================================================
# HELPERS
# ============================================================

def api_get(endpoint, params=None, timeout=15):
    try:
        response = requests.get(
            f"{API_URL}{endpoint}",
            params=params,
            timeout=timeout,
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as exc:
        st.error("FastAPI backend is not reachable.")
        st.code(str(exc))
        return None


def api_post(endpoint, payload=None, params=None, timeout=60):
    try:
        response = requests.post(
            f"{API_URL}{endpoint}",
            json=payload,
            params=params,
            timeout=timeout,
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as exc:
        st.error("FastAPI backend request failed.")
        st.code(str(exc))
        return None


def filters_ui(prefix=""):
    c1, c2, c3 = st.columns(3)

    with c1:
        product = st.selectbox(
            "Product",
            ["All", "Business Loan", "Personal Loan", "Vehicle Loan",
             "Gold Loan", "Home Loan"],
            key=f"{prefix}filter_product",
        )

    with c2:
        city = st.selectbox(
            "City",
            ["All", "Mumbai", "Delhi", "Bengaluru", "Hyderabad",
             "Chennai", "Pune", "Kolkata", "Ahmedabad", "Jaipur", "Lucknow"],
            key=f"{prefix}filter_city",
        )

    with c3:
        credit_band = st.selectbox(
            "Credit Band",
            ["All", "Poor", "Fair", "Good", "Very Good", "Excellent"],
            key=f"{prefix}filter_credit_band",
        )

    return {
        "product": product,
        "city": city,
        "credit_band": credit_band,
    }


def ui_section(kicker, title, description=""):
    st.markdown(
        f"""
        <div class="ui-card">
            <div class="section-kicker">{kicker}</div>
            <div class="section-title">{title}</div>
            {f'<div class="section-desc">{description}</div>' if description else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )

def show_kpis(summary):
    if not summary:
        return

    cols = st.columns(5)

    cols[0].metric("Total Loans", f"{summary['total_loans']:,}")
    cols[1].metric(
        "Total Exposure",
        f"₹{summary['total_exposure'] / 10_000_000:.2f} Cr",
    )
    cols[2].metric("Total Defaults", f"{summary['total_defaults']:,}")
    cols[3].metric("Default Rate", f"{summary['default_rate_pct']:.2f}%")
    cols[4].metric(
        "90+ DPD Exposure",
        f"₹{summary['exposure_90_plus_dpd'] / 10_000_000:.2f} Cr",
    )


def display_result_card(result):
    if not result:
        return

    loan = result.get("loan", {})
    st.success(result.get("message", "Loan processed successfully."))

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Customer ID", result.get("customer_id", "—"))
    c2.metric("EMI", f"₹{loan.get('emi', 0):,.2f}")
    c3.metric(
        "Rule Risk",
        f"{loan.get('risk_score', 0)} · {loan.get('risk_category', '—')}",
    )
    c4.metric(
        "ML Default Probability",
        f"{loan.get('ml_predicted_probability', 0) * 100:.2f}%",
    )

    detail = pd.DataFrame(
        [{
            "Customer ID": loan.get("customer_id", result.get("customer_id")),
            "Product": loan.get("product"),
            "City": loan.get("city"),
            "Credit Score": loan.get("credit_score"),
            "Loan Amount (₹)": loan.get("loan_amount"),
            "EMI (₹)": loan.get("emi"),
            "EMI / Income (%)": loan.get("emi_to_income"),
            "Loan / Annual Income": loan.get("loan_to_annual_income"),
            "Rule Risk Score": loan.get("risk_score"),
            "Risk Category": loan.get("risk_category"),
            "ML Default Probability (%)":
                loan.get("ml_predicted_probability", 0) * 100,
        }]
    )

    st.dataframe(
        detail.style.format({
            "Loan Amount (₹)": "₹{:,.0f}",
            "EMI (₹)": "₹{:,.2f}",
            "EMI / Income (%)": "{:.2f}",
            "Loan / Annual Income": "{:.4f}",
            "ML Default Probability (%)": "{:.2f}",
        }),
        use_container_width=True,
        hide_index=True,
    )

    r1, r2 = st.columns(2)
    r1.metric("CSV Records", f"{result.get('csv_total', 0):,}")
    r2.metric("SQLite Records", f"{result.get('sqlite_total', 0):,}")


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("## 🏦 NBFC Risk Analytics")
    st.caption("Portfolio Intelligence Platform • v1.0")
    st.divider()

    st.markdown('<div class="nav-label">Navigation</div>', unsafe_allow_html=True)

    nav_html = []
    for key, label in PAGES.items():
        active = "active" if key == page_key else ""
        nav_html.append(
            f'<a class="nav-link {active}" href="?page={key}#top" target="_self">{label}</a>'
        )

    st.markdown("".join(nav_html), unsafe_allow_html=True)

    st.divider()
    st.markdown("### System Status")

    api_status = api_get("/", timeout=5)

    if api_status is not None:
        st.markdown(
            '<div class="status-card">🟢 <b>FastAPI</b> — Connected</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="status-card">🔴 <b>FastAPI</b> — Offline</div>',
            unsafe_allow_html=True,
        )

    db_path = "Data/nbfc_risk_analytics.db"
    model_path = "models/rf_risk_pipeline.joblib"

    st.markdown(
        f'<div class="status-card">{"🟢" if os.path.exists(db_path) else "🔴"} '
        f'<b>SQLite</b> — {"Available" if os.path.exists(db_path) else "Missing"}</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="status-card">{"🟢" if os.path.exists(model_path) else "🔴"} '
        f'<b>ML Model</b> — {"Loaded" if os.path.exists(model_path) else "Missing"}</div>',
        unsafe_allow_html=True,
    )

    st.divider()
    st.caption("Python • SQL • scikit-learn • FastAPI • SQLite • Streamlit")

# ============================================================
# TOP ANCHOR + HEADER
# ============================================================

st.markdown('<div id="top"></div>', unsafe_allow_html=True)

st.markdown(
    '<div class="app-title">🏦 NBFC Loan Portfolio Risk & Analytics</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="app-subtitle">'
    "Portfolio intelligence • Credit risk • Machine learning • Collections"
    "</div>",
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div style="
        display:inline-block;
        padding:0.35rem 0.7rem;
        border-radius:999px;
        border:1px solid rgba(96,165,250,.22);
        background:rgba(59,130,246,.08);
        color:#93c5fd;
        font-size:0.78rem;
        font-weight:650;
        margin-bottom:0.9rem;
    ">
        ● ANALYTICS PORTAL &nbsp;•&nbsp; API-DRIVEN
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# OVERVIEW
# ============================================================

if page_key == "overview":
    st.markdown(
        """
        <div class="hero">
            <h2>Executive Portfolio Overview</h2>
            <p>
                Monitor portfolio exposure, defaults, delinquency and
                portfolio risk from a single dashboard.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("🔄 Refresh Portfolio Data", use_container_width=False):
        st.rerun()

    summary = api_get("/api/portfolio/summary")
    show_kpis(summary)

    st.divider()

    product_data = api_get("/api/portfolio/product-risk")
    credit_data = api_get("/api/portfolio/credit-risk")
    city_data = api_get("/api/portfolio/city-risk")

    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Product Risk")
        if product_data:
            df = pd.DataFrame(product_data)
            st.bar_chart(df.set_index("product")[["default_rate_pct"]])

    with c2:
        st.subheader("Credit Band Risk")
        if credit_data:
            df = pd.DataFrame(credit_data)
            st.bar_chart(df.set_index("credit_band")[["default_rate_pct"]])

    st.divider()

    st.subheader("Geographic Risk")
    if city_data:
        df = pd.DataFrame(city_data)
        st.bar_chart(df.set_index("city")[["default_rate_pct"]])

    st.info(
        "Use the sidebar to move from executive overview to loan origination, "
        "portfolio risk, ML analytics and collections."
    )

# ============================================================
# LOAN ORIGINATION
# ============================================================

elif page_key == "origination":
    st.markdown(
        """
        <div class="hero">
            <h2>New Loan Origination</h2>
            <p>
                Enter a newly originated loan. The backend automatically
                calculates analytical features, applies the rule-based
                risk score and scores the loan using the saved Random Forest.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("loan_origination_form"):
        c1, c2, c3 = st.columns(3)

        with c1:
            product = st.selectbox(
                "Product",
                ["Business Loan", "Personal Loan", "Vehicle Loan",
                 "Gold Loan", "Home Loan"],
            )
            city = st.selectbox(
                "City",
                ["Mumbai", "Delhi", "Bengaluru", "Hyderabad", "Chennai",
                 "Pune", "Kolkata", "Ahmedabad", "Jaipur", "Lucknow"],
            )
            employment_type = st.selectbox(
                "Employment Type",
                ["Salaried", "Self-employed", "Business Owner"],
            )

        with c2:
            age = st.number_input("Age", 18, 80, 30, 1)
            monthly_income = st.number_input(
                "Monthly Income (₹)", 1000.0, 10_000_000.0, 60000.0, 1000.0
            )
            credit_score = st.number_input(
                "Credit Score", 300, 900, 680, 1
            )

        with c3:
            loan_amount = st.number_input(
                "Loan Amount (₹)", 10000.0, 100_000_000.0, 500000.0, 10000.0
            )
            tenure_months = st.number_input(
                "Tenure (months)", 3, 360, 48, 1
            )
            interest_rate = st.number_input(
                "Interest Rate (%)", 1.0, 40.0, 14.0, 0.25
            )

        st.caption(
            "Customer ID, EMI, EMI-to-income, LTI, risk score and ML probability "
            "are generated by the backend."
        )

        submit_loan = st.form_submit_button(
            "✅ Submit & Score Loan",
            use_container_width=True,
        )

    if submit_loan:
        payload = {
            "age": int(age),
            "city": city,
            "employment_type": employment_type,
            "monthly_income": float(monthly_income),
            "credit_score": int(credit_score),
            "product": product,
            "loan_amount": float(loan_amount),
            "tenure_months": int(tenure_months),
            "interest_rate": float(interest_rate),
        }

        result = api_post("/api/loans", payload=payload, timeout=60)

        if result:
            display_result_card(result)

# ============================================================
# PORTFOLIO RISK
# ============================================================

elif page_key == "portfolio":
    st.markdown(
        """
        <div class="hero">
            <h2>Portfolio Risk Analytics</h2>
            <p>Analyze product, credit-band and geographic risk using API-driven portfolio data.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    params = filters_ui("portfolio_")
    st.divider()

    summary = api_get("/api/portfolio/summary", params=params)
    show_kpis(summary)

    st.divider()

    product_data = api_get("/api/portfolio/product-risk", params=params)
    if product_data:
        df = pd.DataFrame(product_data)
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Default Rate by Product")
            st.bar_chart(df.set_index("product")[["default_rate_pct"]])
        with c2:
            display = df.copy()
            display["exposure"] = (display["exposure"] / 10_000_000).round(2)
            display = display.rename(columns={
                "product": "Product",
                "total_loans": "Loans",
                "exposure": "Exposure (Cr)",
                "defaults": "Defaults",
                "default_rate_pct": "Default Rate (%)",
            })
            st.dataframe(display, use_container_width=True, hide_index=True)

    st.divider()

    credit_data = api_get("/api/portfolio/credit-risk", params=params)
    if credit_data:
        df = pd.DataFrame(credit_data)
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Default Rate by Credit Band")
            st.bar_chart(df.set_index("credit_band")[["default_rate_pct"]])
        with c2:
            display = df.copy()
            display["exposure"] = (display["exposure"] / 10_000_000).round(2)
            display = display.rename(columns={
                "credit_band": "Credit Band",
                "total_loans": "Loans",
                "defaults": "Defaults",
                "default_rate_pct": "Default Rate (%)",
                "exposure": "Exposure (Cr)",
            })
            st.dataframe(display, use_container_width=True, hide_index=True)

    st.divider()

    city_data = api_get("/api/portfolio/city-risk", params=params)
    if city_data:
        df = pd.DataFrame(city_data)
        st.subheader("Geographic Risk")
        st.bar_chart(df.set_index("city")[["default_rate_pct"]])

        display = df.copy()
        display["exposure"] = (display["exposure"] / 10_000_000).round(2)
        display = display.rename(columns={
            "city": "City",
            "total_loans": "Loans",
            "defaults": "Defaults",
            "default_rate_pct": "Default Rate (%)",
            "exposure": "Exposure (Cr)",
        })
        st.dataframe(display, use_container_width=True, hide_index=True)

# ============================================================
# ML RISK
# ============================================================

elif page_key == "ml":
    st.markdown(
        """
        <div class="hero">
            <h2>Machine Learning Risk Analytics</h2>
            <p>
                Compare the baseline models, inspect the Random Forest evaluation
                and review ML-identified risk drivers.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    try:
        metrics_df = pd.read_csv("Data/ml_model_metrics.csv")
        importance_df = pd.read_csv("Data/ml_feature_importance.csv")
        confusion_df = pd.read_csv(
            "Data/ml_confusion_matrix.csv",
            index_col=0,
        )

        lr_auc = metrics_df.loc[
            metrics_df["model"] == "Logistic Regression", "roc_auc"
        ].iloc[0]
        rf_row = metrics_df.loc[
            metrics_df["model"] == "Random Forest"
        ].iloc[0]

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Logistic Regression ROC-AUC", f"{lr_auc:.3f}")
        c2.metric("Random Forest ROC-AUC", f"{rf_row['roc_auc']:.3f}")
        c3.metric("RF Precision", f"{rf_row['precision_default_class']:.3f}")
        c4.metric("RF Recall", f"{rf_row['recall_default_class']:.3f}")

        st.divider()

        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Model Comparison")
            st.bar_chart(metrics_df.set_index("model")[["roc_auc"]])
        with c2:
            st.subheader("Random Forest Confusion Matrix")
            st.dataframe(confusion_df, use_container_width=True)

        st.divider()

        st.subheader("Top ML-Identified Risk Features")
        importance_display = importance_df.head(10).copy()
        importance_display["feature"] = (
            importance_display["feature"]
            .str.replace("num__", "", regex=False)
            .str.replace("cat__", "", regex=False)
        )
        importance_display["importance"] = importance_display["importance"].round(4)

        st.bar_chart(
            importance_display.set_index("feature")[["importance"]]
        )
        st.dataframe(
            importance_display.rename(columns={
                "feature": "Feature",
                "importance": "Importance",
            }),
            use_container_width=True,
            hide_index=True,
        )

        st.divider()

        st.subheader("ML-Predicted High-Risk Loans")
        params = filters_ui("ml_")
        ml_data = api_get("/api/risk/high-risk-loans", params=params)

        if ml_data:
            ml_df = pd.DataFrame(ml_data)
            ml_df["loan_amount"] = (ml_df["loan_amount"] / 100_000).round(2)
            ml_df["ml_predicted_probability"] = (
                ml_df["ml_predicted_probability"] * 100
            ).round(2)

            ml_df = ml_df.rename(columns={
                "customer_id": "Customer ID",
                "product": "Product",
                "city": "City",
                "loan_amount": "Loan Amount (₹ Lakh)",
                "credit_score": "Credit Score",
                "emi_to_income": "EMI / Income (%)",
                "ml_predicted_probability": "ML Default Probability (%)",
            })
            st.dataframe(ml_df, use_container_width=True, hide_index=True)

    except Exception as exc:
        st.error("ML evaluation files could not be loaded.")
        st.code(str(exc))

# ============================================================
# VINTAGE
# ============================================================

elif page_key == "vintage":
    st.markdown(
        """
        <div class="hero">
            <h2>Vintage / Cohort Analysis</h2>
            <p>Track portfolio performance by disbursement quarter.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    params = filters_ui("vintage_")
    data = api_get("/api/portfolio/vintage", params=params)

    if data:
        df = pd.DataFrame(data)
        st.line_chart(
            df.set_index("disbursement_quarter")[["cohort_default_rate_pct"]]
        )

        display = df.copy()
        display["cohort_exposure"] = (
            display["cohort_exposure"] / 10_000_000
        ).round(2)

        display = display.rename(columns={
            "disbursement_quarter": "Quarter",
            "loans_in_cohort": "Loans",
            "cohort_exposure": "Exposure (Cr)",
            "defaults": "Defaults",
            "cohort_default_rate_pct": "Default Rate (%)",
        })
        st.dataframe(display, use_container_width=True, hide_index=True)

# ============================================================
# COLLECTIONS
# ============================================================

elif page_key == "collections":
    st.markdown(
        """
        <div class="hero">
            <h2>Collections Priority</h2>
            <p>Surface delinquent and higher-risk accounts for collection prioritisation.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    params = filters_ui("collections_")
    data = api_get("/api/collections/priority", params=params)

    if data:
        df = pd.DataFrame(data)
        df["loan_amount"] = (df["loan_amount"] / 100_000).round(2)
        df["ml_predicted_probability"] = (
            df["ml_predicted_probability"] * 100
        ).round(2)

        display = df.rename(columns={
            "customer_id": "Customer ID",
            "product": "Product",
            "city": "City",
            "loan_amount": "Loan Amount (₹ Lakh)",
            "days_past_due": "DPD",
            "credit_score": "Credit Score",
            "emi_to_income": "EMI / Income (%)",
            "ml_predicted_probability": "ML Default Probability (%)",
        })

        st.dataframe(display, use_container_width=True, hide_index=True)

# ============================================================
# BATCH SIMULATOR
# ============================================================

elif page_key == "simulator":
    st.markdown(
        """
        <div class="hero">
            <h2>Portfolio Loan Simulator</h2>
            <p>
                Generate a batch of realistic new loans, score them with the
                existing rule-based framework and saved Random Forest model,
                and append them to the portfolio.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.warning(
        "Simulation changes the local CSV and SQLite portfolio. Use this section "
        "for controlled testing/demo activity."
    )

    simulation_count = st.number_input(
        "Number of new loans",
        min_value=1,
        max_value=500,
        value=20,
        step=5,
    )

    confirm = st.checkbox(
        f"I understand that this will add {int(simulation_count)} new simulated loans."
    )

    if st.button(
        "🚀 Simulate New Loan Batch",
        disabled=not confirm,
        use_container_width=True,
    ):
        result = api_post(
            "/api/pipeline/simulate-new-loans",
            params={"n": int(simulation_count)},
            timeout=90,
        )

        if result:
            st.success(result.get("message", "Simulation completed."))

            c1, c2, c3 = st.columns(3)
            c1.metric("Loans Added", f"{result['loans_added']:,}")
            c2.metric("CSV Records", f"{result['csv_total']:,}")
            c3.metric("SQLite Records", f"{result['sqlite_total']:,}")

            new_df = pd.DataFrame(result.get("new_loans", []))
            if not new_df.empty:
                new_df["ml_predicted_probability"] = (
                    new_df["ml_predicted_probability"] * 100
                ).round(2)

                new_df = new_df.rename(columns={
                    "customer_id": "Customer ID",
                    "product": "Product",
                    "city": "City",
                    "credit_score": "Credit Score",
                    "risk_score": "Rule Risk Score",
                    "risk_category": "Rule Risk Category",
                    "ml_predicted_probability": "ML Default Probability (%)",
                })

                st.subheader("Newly Simulated Loans")
                st.dataframe(
                    new_df,
                    use_container_width=True,
                    hide_index=True,
                )

# ============================================================
# ABOUT
# ============================================================

elif page_key == "about":
    st.markdown(
        """
        <div class="hero">
            <h2>About the Project</h2>
            <p>
                An end-to-end NBFC portfolio analytics project combining
                Python, SQL, machine learning, FastAPI and Streamlit.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("👩‍💻 About Me")

    c1, c2 = st.columns([1, 2])

    with c1:
        st.markdown(
            """
            <div class="profile-card">
                <h3 style="margin-top:0;">Khushi Solanki</h3>
                <p><b>B.Tech Mechanical Engineering</b></p>
                <p><b>Honors in Robotics</b></p>
                <p>DJSCE, Mumbai</p>
                <p>2023–2027</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            """
            <div class="profile-card">
                <h4 style="margin-top:0;">Project Focus</h4>
                <p>
                    This project demonstrates how a mechanical engineering student
                    can apply Python, SQL, machine learning and backend development
                    to a financial analytics use case.
                </p>
                <p class="small-muted">
                    The portfolio dataset is synthetic and the application is
                    designed for analytics demonstration and interview discussion.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("")
    st.link_button(
        "🔗 View GitHub Repository",
        "https://github.com/Khushi23-sol/NBFC-Loan-Portfolio-Risk-Analytics",
    )

    st.caption(
        "LinkedIn profile link can be added here once the final portfolio URL is ready."
    )

    st.divider()

    c1, c2, c3 = st.columns(3)
    c1.metric("Data Records", "8,000+")
    c2.metric("Risk Models", "2")
    c3.metric("Backend", "FastAPI + SQLite")

    st.subheader("Technology Stack")
    st.markdown(
        """
        - **Python / Pandas** — data processing and feature engineering
        - **scikit-learn** — Logistic Regression and Random Forest
        - **SQL / SQLite** — portfolio analytics and persistence
        - **FastAPI** — REST API layer
        - **Streamlit** — interactive analytics portal
        - **Power BI** — portfolio dashboard and business reporting
        """
    )

    st.subheader("System Architecture")
    st.code(
        """8,000 Synthetic Loans
        ↓
Python Processing + Feature Engineering
        ↓
Rule-Based Risk Scoring
        +
Logistic Regression / Random Forest
        ↓
SQLite Portfolio Database
        ↓
FastAPI REST API
        ↓ HTTP
Streamlit Analytics Portal
        ↓
Executive Portfolio Insights""",
        language="text",
    )

    st.subheader("Project Highlights")
    st.markdown(
        """
        - Portfolio KPI and exposure analysis
        - Product, credit-band and city risk analysis
        - Vintage / cohort analysis
        - Collections priority analysis
        - Rule-based risk segmentation
        - Logistic Regression vs Random Forest comparison
        - ML feature importance analysis
        - API-driven new loan origination
        - Batch loan simulation
        """
    )

    st.subheader("Important Project Notes")
    st.markdown(
        """
        - The portfolio dataset is synthetic and used for analytics demonstration.
        - The rule-based risk score is a portfolio segmentation framework, not a
          regulated lending decision engine.
        - ML feature importance indicates model usage, not causal relationships.
        - New loan origination and batch simulation are demonstration workflows
          rather than connections to a live NBFC core-loan system.
        """
    )

# ============================================================
# FOOTER
# ============================================================

st.divider()
st.caption(
    "NBFC Loan Portfolio Risk & Analytics • "
    "FastAPI + SQLite + Streamlit + scikit-learn • "
    "Synthetic portfolio for analytics demonstration"
)
