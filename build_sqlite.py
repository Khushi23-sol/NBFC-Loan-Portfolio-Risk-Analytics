import pandas as pd
import sqlite3
from pathlib import Path

# ============================================================
# NBFC PROJECT — BUILD SQLITE DATABASE
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

# ML-enhanced dataset
INPUT_FILE = BASE_DIR / "Data" / "loan_portfolio_with_ml.csv"

# New SQLite database
DB_FILE = BASE_DIR / "Data" / "nbfc_risk_analytics.db"

print("=" * 60)
print("BUILDING SQLITE DATABASE")
print("=" * 60)

# ------------------------------------------------------------
# 1. LOAD FINAL ANALYTICAL DATASET
# ------------------------------------------------------------

df = pd.read_csv(INPUT_FILE)

print(f"Source file : {INPUT_FILE.name}")
print(f"Rows loaded : {len(df)}")

# ------------------------------------------------------------
# 2. STANDARDIZE DATE
# ------------------------------------------------------------

if "disbursement_date" in df.columns:
    df["disbursement_date"] = pd.to_datetime(
        df["disbursement_date"],
        errors="coerce"
    ).dt.strftime("%Y-%m-%d")

# ------------------------------------------------------------
# 3. CREATE SQLITE DATABASE
# ------------------------------------------------------------

conn = sqlite3.connect(DB_FILE)

df.to_sql(
    "loan_portfolio",
    conn,
    if_exists="replace",
    index=False
)

# ------------------------------------------------------------
# 4. VERIFY DATABASE
# ------------------------------------------------------------

cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM loan_portfolio")
row_count = cursor.fetchone()[0]

cursor.execute("PRAGMA table_info(loan_portfolio)")
columns = [row[1] for row in cursor.fetchall()]

conn.close()

# ------------------------------------------------------------
# 5. DISPLAY RESULT
# ------------------------------------------------------------

print("\nSQLite database created successfully!")
print(f"Database    : {DB_FILE}")
print(f"Rows stored : {row_count}")

print("\nColumns:")
for column in columns:
    print(f" - {column}")

print("\n" + "=" * 60)
print("SQLITE BUILD COMPLETE")
print("=" * 60)