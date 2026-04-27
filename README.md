# Online Retail II — Cohort Analysis & Customer Retention

## 📌 Overview
This project analyzes two years of transactional data from a UK-based online retailer to understand how well the business retains customers over time. Using cohort analysis, we track what percentage of customers from each monthly acquisition group return in subsequent months — and identify where the retailer loses them.

## ❓ Business Question
**How well does this UK online retailer retain customers month-over-month, and where does it lose them?**

Retention is a core metric for any e-commerce business. Acquiring a new customer costs significantly more than retaining an existing one. If most customers leave after their first purchase, that signals a problem with product experience, communication, or loyalty strategy — not just acquisition volume.

## 🗂️ Dataset
- **Source:** [UCI Machine Learning Repository — Online Retail II](https://archive.ics.uci.edu/dataset/502/online+retail+ii)
- **Size:** ~1,067,371 rows × 8 columns (two sheets: 2009–2010 and 2010–2011)
- **Domain:** UK-based non-store online retailer selling gift-ware; customer base includes both retail consumers and wholesalers
- **Key columns:**

| Column | Description |
|--------|-------------|
| `Invoice` | Transaction ID — codes starting with `C` indicate cancellations |
| `CustomerID` | Unique customer identifier (~25% missing) |
| `InvoiceDate` | Date and time of transaction |
| `Quantity` | Units purchased per line item |
| `Price` | Unit price in GBP (£) |
| `Country` | Customer's country of residence |

## 🔧 Methodology

```
Raw Data (Excel)
    │
    ▼  SQL — 01_cleaning.sql
    Remove cancellations (Invoice starting with 'C'),
    null CustomerIDs, zero/negative prices and quantities
    │
    ▼  SQL — 02_cohort_assignment.sql
    Assign each customer their cohort month
    (= month of first purchase)
    │
    ▼  SQL — 03_retention_matrix.sql
    Count distinct active customers per cohort × period
    │
    ▼  SQL — 04_retention_rate.sql
    Calculate % retention relative to each cohort's starting size
    │
    ▼  Python — visualize_cohort.py / cohort_analysis.ipynb
    Pivot matrix → cohort heatmap + supporting charts
```

All analytical logic lives in SQL (SQLite-compatible). Python is used exclusively for visualization.

## 📊 Key Findings

> ⚠️ **Update with actual numbers after running the notebook locally.**

1. **Steep Month-1 churn:** The largest drop in retention occurs between Period 0 (acquisition) and Period 1, with most cohorts retaining only ~[X]% of customers after the first month.
2. **Retention stabilizes after Month 3:** Customers who return for a second or third purchase show significantly higher long-term loyalty — the curve flattens around Period 3–4.
3. **Strongest retention cohort:** The [YYYY-MM] cohort outperforms others over time — worth investigating what drove that period (promotions, product mix, seasonality).
4. **Seasonal acquisition spikes:** Cohort sizes peak in Q4, reflecting holiday gifting demand — but larger cohorts do not necessarily retain better.
5. **Wholesaler effect:** Given that many customers are B2B wholesalers, retained customers likely represent high-value bulk buyers, meaning the revenue impact of retention is higher than the % numbers suggest.

## 🛠️ Tools Used
`Python` · `SQL (SQLite)` · `Pandas` · `NumPy` · `Seaborn` · `Matplotlib` · `Jupyter Notebook` · `openpyxl`

## 📁 Repository Structure
```
online-retail-cohort-analysis/
│
├── data/
│   └── online_retail_II.xlsx        # raw data — download from UCI (gitignored)
│
├── sql/
│   ├── 01_cleaning.sql              # filter cancellations, nulls, bad values
│   ├── 02_cohort_assignment.sql     # tag each transaction with cohort month
│   ├── 03_retention_matrix.sql      # count active customers per cohort × period
│   └── 04_retention_rate.sql        # calculate % retention per cohort
│
├── notebooks/
│   └── cohort_analysis.ipynb        # end-to-end storytelling notebook
│
├── scripts/
│   └── visualize_cohort.py          # standalone Python visualization script
│
├── outputs/
│   ├── cohort_heatmap.png           # main cohort retention heatmap
│   ├── monthly_overview.png         # monthly customers and revenue
│   ├── cohort_sizes.png             # new customers acquired per month
│   └── avg_retention_curve.png      # average retention decay curve
│
├── setup_repo.py                    # scaffolds this folder structure locally
├── requirements.txt                 # Python dependencies
└── README.md
```

## ▶️ How to Run

**1. Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/online-retail-cohort-analysis.git
cd online-retail-cohort-analysis
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Download the dataset**

Download `online_retail_II.xlsx` from [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/502/online+retail+ii) and place it in the `data/` folder.

```
data/
└── online_retail_II.xlsx
```

**4a. Run the Jupyter Notebook** *(recommended — full storytelling)*
```bash
jupyter notebook notebooks/cohort_analysis.ipynb
```

**4b. Or run the standalone script** *(quick chart output)*
```bash
python scripts/visualize_cohort.py
```

Output charts will be saved to the `outputs/` folder automatically.

---

> **Note on SQL dialect:** All SQL scripts are written in SQLite-compatible syntax using `SUBSTR()` for date parsing. To run on PostgreSQL or BigQuery, replace `SUBSTR(date, 1, 7)` with `TO_CHAR(date, 'YYYY-MM')` or `FORMAT_DATE('%Y-%m', date)` respectively.

---

*Analysis by Rahmadhania · April 2026*
