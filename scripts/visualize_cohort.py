"""
visualize_cohort.py
===================
Loads the Online Retail II dataset, runs all 4 SQL cleaning and cohort
steps via SQLite, then renders and exports a cohort retention heatmap.

Usage:
    python scripts/visualize_cohort.py

Output:
    outputs/cohort_heatmap.png
"""

import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

# =============================================================================
# CONFIG — adjust paths here if your folder layout differs
# =============================================================================

DATA_PATH    = os.path.join("data", "online_retail_II.xlsx")
OUTPUT_PATH  = os.path.join("outputs", "cohort_heatmap.png")
SQL_DIR      = "sql"

# =============================================================================
# STEP 1 — Load raw Excel data into an in-memory SQLite database
# Why in-memory: no server needed, fast for a ~1M row dataset,
# and keeps the repo clean (no .db file to manage or gitignore)
# =============================================================================

print("📥 Loading dataset — this may take 30–60 seconds for ~1M rows...")

# Read both sheets; Online Retail II has two sheets (Year 2009-2010, 2010-2011)
df_1 = pd.read_excel(DATA_PATH, sheet_name="Year 2009-2010", engine="openpyxl")
df_2 = pd.read_excel(DATA_PATH, sheet_name="Year 2010-2011", engine="openpyxl")

# Combine both years into one dataframe
df_raw = pd.concat([df_1, df_2], ignore_index=True)

print(f"   Raw rows loaded: {len(df_raw):,}")

# Normalize column names: strip spaces, lowercase for SQL compatibility
df_raw.columns = (
    df_raw.columns
    .str.strip()
    .str.replace(" ", "_")
    .str.lower()
)

# Rename to match our SQL scripts exactly
df_raw = df_raw.rename(columns={
    "invoice":      "InvoiceNo",
    "stockcode":    "StockCode",
    "description":  "Description",
    "quantity":     "Quantity",
    "invoicedate":  "InvoiceDate",
    "price":        "UnitPrice",
    "customer_id":  "CustomerID",
    "country":      "Country",
})

# Convert InvoiceDate to ISO string format 'YYYY-MM-DD HH:MM:SS'
# SQLite stores dates as text; SUBSTR() in our SQL expects this format
df_raw["InvoiceDate"] = pd.to_datetime(df_raw["InvoiceDate"]).dt.strftime("%Y-%m-%d %H:%M:%S")

# Load into SQLite in-memory database
conn = sqlite3.connect(":memory:")
df_raw.to_sql("raw_retail", conn, if_exists="replace", index=False)

print("   Data loaded into SQLite in-memory database ✅\n")

# =============================================================================
# STEP 2 — Execute SQL scripts in sequence
# Each script builds on the table created by the previous one
# =============================================================================

def run_sql_file(conn, filename):
    """Read a .sql file and execute it against the given SQLite connection."""
    filepath = os.path.join(SQL_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        sql = f.read()
    conn.executescript(sql)
    print(f"   ✅ Executed: {filename}")

print("🔧 Running SQL pipeline...")
run_sql_file(conn, "01_cleaning.sql")
run_sql_file(conn, "02_cohort_assignment.sql")
run_sql_file(conn, "03_retention_matrix.sql")
run_sql_file(conn, "04_retention_rate.sql")
print()

# =============================================================================
# STEP 3 — Load the final retention_rates table into Pandas
# =============================================================================

print("📊 Loading retention rates into Pandas...")

retention_df = pd.read_sql(
    "SELECT cohort_month, period_number, retention_rate FROM retention_rates",
    conn
)

print(f"   Cohorts found     : {retention_df['cohort_month'].nunique()}")
print(f"   Max period number : {retention_df['period_number'].max()}")
print()

conn.close()  # Done with SQLite — free the memory

# =============================================================================
# STEP 4 — Pivot into a matrix for heatmap rendering
# Rows = cohort months, Columns = period numbers (0, 1, 2, ...)
# Values = retention rate (%)
# =============================================================================

cohort_pivot = retention_df.pivot_table(
    index="cohort_month",
    columns="period_number",
    values="retention_rate"
)

# Sort cohorts chronologically (they should already be, but be explicit)
cohort_pivot = cohort_pivot.sort_index()

print("Cohort retention matrix (first 5 cohorts, first 6 periods):")
print(cohort_pivot.iloc[:5, :6].to_string())
print()

# =============================================================================
# STEP 5 — Plot the cohort retention heatmap
# Design choices:
#   - Diverging annotation: period 0 always 100%, so we mask it differently
#   - YlOrRd colormap: intuitive — green/yellow = high retention, red = churn
#   - Annotated cells: exact % values help recruiters read the chart directly
# =============================================================================

print("🎨 Rendering heatmap...")

fig, ax = plt.subplots(figsize=(18, 8))

# Create a mask for period 0 so we can style it separately
# Period 0 is always 100% — visually separating it avoids misleading the eye
mask_period0 = cohort_pivot.copy()
mask_period0.loc[:, :] = False
mask_period0.iloc[:, 0] = True   # True = masked (hidden from main heatmap)

# Main heatmap — all periods except period 0
sns.heatmap(
    cohort_pivot,
    mask=mask_period0.values,    # hide period 0 from color scale
    annot=True,                  # show numbers in each cell
    fmt=".1f",                   # 1 decimal place
    cmap="YlOrRd_r",             # reversed: yellow = high (good), red = low (churn)
    linewidths=0.4,
    linecolor="#e0e0e0",
    cbar_kws={"label": "Retention Rate (%)", "shrink": 0.6},
    vmin=0,
    vmax=100,
    ax=ax,
    annot_kws={"size": 7.5}
)

# Overlay period 0 separately in a neutral color to signal "baseline"
sns.heatmap(
    cohort_pivot,
    mask=~mask_period0.values,   # only show period 0
    annot=True,
    fmt=".1f",
    cmap=["#4a90d9"],            # flat blue — signals "this is always 100%"
    linewidths=0.4,
    linecolor="#e0e0e0",
    cbar=False,                  # no extra colorbar for this layer
    vmin=100,
    vmax=100,
    ax=ax,
    annot_kws={"size": 7.5, "color": "white", "weight": "bold"}
)

# --- Labels & formatting ---
ax.set_title(
    "Customer Cohort Retention — Online Retail II (2009–2011)",
    fontsize=15,
    fontweight="bold",
    pad=16
)
ax.set_xlabel("Months Since First Purchase (Period)", fontsize=11, labelpad=10)
ax.set_ylabel("Cohort (First Purchase Month)", fontsize=11, labelpad=10)

# Rotate x-axis labels for readability
ax.set_xticklabels(ax.get_xticklabels(), rotation=0, fontsize=8.5)
ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=8.5)

# Add a subtitle / caption
fig.text(
    0.5, -0.02,
    "Values show % of cohort customers still active N months after first purchase.  "
    "Blue = acquisition month (always 100%).  Yellow–Red scale = retention strength.",
    ha="center",
    fontsize=8.5,
    color="#555555"
)

plt.tight_layout()

# =============================================================================
# STEP 6 — Export
# =============================================================================

os.makedirs("outputs", exist_ok=True)
plt.savefig(OUTPUT_PATH, dpi=150, bbox_inches="tight")
print(f"\n✅ Heatmap saved to: {OUTPUT_PATH}")
plt.show()
