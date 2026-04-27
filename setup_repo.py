"""
setup_repo.py
=============
Scaffolds the full local project structure for:
  "Online Retail II — Cohort Analysis & Customer Retention"

Run this script once from wherever you want the project folder to live:
    python setup_repo.py

It will create all folders and placeholder files automatically.
You do NOT need to create anything manually after running this.
"""

import os

# =============================================================================
# Project root — all files will be created inside this folder
# Change this name if you want a different local folder name
# =============================================================================
PROJECT_ROOT = "online-retail-cohort-analysis"


# =============================================================================
# Folder structure
# Each entry is a path relative to PROJECT_ROOT
# =============================================================================
FOLDERS = [
    "data",           # raw dataset goes here (gitignored)
    "sql",            # all 4 SQL scripts
    "notebooks",      # Jupyter notebook for storytelling
    "scripts",        # clean Python visualization script
    "outputs",        # exported charts and tables
]


# =============================================================================
# Files to create with starter content
# Format: { "relative/path/to/file": "file content as string" }
# =============================================================================
FILES = {

    # --- Git & environment config -------------------------------------------

    ".gitignore": """\
# Raw data (file is too large for GitHub)
data/

# Python cache
__pycache__/
*.pyc
*.pyo
.ipynb_checkpoints/

# Virtual environment
venv/
.env

# OS files
.DS_Store
Thumbs.db

# Outputs are optional — remove this line if you want to commit charts
# outputs/
""",

    "requirements.txt": """\
# Core data stack
pandas>=2.0.0
numpy>=1.24.0
openpyxl>=3.1.0       # needed to read .xlsx files with pandas

# Database
sqlalchemy>=2.0.0     # optional ORM layer for SQLite

# Visualization
matplotlib>=3.7.0
seaborn>=0.12.0

# Notebook
jupyter>=1.0.0
ipykernel>=6.0.0
""",

    # --- SQL placeholders (will be replaced by actual scripts) ---------------

    "sql/01_cleaning.sql": """\
-- 01_cleaning.sql
-- Placeholder — replace with the actual script from Claude.
""",

    "sql/02_cohort_assignment.sql": """\
-- 02_cohort_assignment.sql
-- Placeholder — replace with the actual script from Claude.
""",

    "sql/03_retention_matrix.sql": """\
-- 03_retention_matrix.sql
-- Placeholder — replace with the actual script from Claude.
""",

    "sql/04_retention_rate.sql": """\
-- 04_retention_rate.sql
-- Placeholder — replace with the actual script from Claude.
""",

    # --- Python script placeholder -------------------------------------------

    "scripts/visualize_cohort.py": """\
# visualize_cohort.py
# Placeholder — will load retention_rates from SQLite and render the heatmap.
""",

    # --- Notebook placeholder ------------------------------------------------

    "notebooks/cohort_analysis.ipynb": """\
{
 "nbformat": 4,
 "nbformat_minor": 5,
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "name": "python",
   "version": "3.10.0"
  }
 },
 "cells": [
  {
   "cell_type": "markdown",
   "id": "placeholder",
   "metadata": {},
   "source": [
    "# Online Retail II — Cohort Analysis & Customer Retention\\n",
    "**Placeholder notebook** — full version coming from Claude."
   ]
  }
 ]
}
""",

    # --- Outputs placeholder -------------------------------------------------

    "outputs/.gitkeep": """\
# This file keeps the outputs/ folder tracked by Git even when it is empty.
# Delete this comment once you have real output files here.
""",

    # --- Data placeholder ----------------------------------------------------

    "data/.gitkeep": """\
# Place online_retail_II.xlsx here after downloading from UCI.
# This folder is gitignored — do not commit the raw data file.
""",

    # --- README --------------------------------------------------------------

    "README.md": """\
# Online Retail II — Cohort Analysis & Customer Retention

## 📌 Overview
This project analyzes customer retention behavior for a UK-based online retailer
using cohort analysis on two years of transactional data (2009–2011).

## ❓ Business Question
How well does this retailer retain customers month-over-month, and where does it lose them?

## 🗂️ Dataset
- **Source:** [UCI Machine Learning Repository — Online Retail II](https://archive.ics.uci.edu/dataset/502/online+retail+ii)
- **Size:** ~1,067,371 rows × 8 columns
- **Period:** December 2009 – December 2011
- **Key columns:** `CustomerID`, `InvoiceNo`, `InvoiceDate`, `Quantity`, `UnitPrice`, `Country`

## 🔧 Methodology
1. **SQL — Cleaning:** Remove cancellations, null customers, and invalid prices/quantities
2. **SQL — Cohort Assignment:** Tag each customer with their first-purchase month
3. **SQL — Retention Matrix:** Count distinct active customers per cohort × period
4. **SQL — Retention Rates:** Calculate % retention relative to cohort starting size
5. **Python — Visualization:** Render a cohort heatmap using Seaborn + Matplotlib

## 📊 Key Findings
- *(To be filled after analysis)*

## 🛠️ Tools Used
Python · SQL (SQLite) · Pandas · Seaborn · Matplotlib · Jupyter Notebook

## 📁 Repository Structure
\`\`\`
online-retail-cohort-analysis/
├── data/                        # Raw dataset (gitignored)
├── sql/
│   ├── 01_cleaning.sql
│   ├── 02_cohort_assignment.sql
│   ├── 03_retention_matrix.sql
│   └── 04_retention_rate.sql
├── notebooks/
│   └── cohort_analysis.ipynb
├── scripts/
│   └── visualize_cohort.py
├── outputs/
│   └── cohort_heatmap.png
├── setup_repo.py
├── requirements.txt
└── README.md
\`\`\`

## ▶️ How to Run
\`\`\`bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/online-retail-cohort-analysis.git
cd online-retail-cohort-analysis

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download the dataset from UCI and place it in data/
#    https://archive.ics.uci.edu/dataset/502/online+retail+ii

# 4. Run the notebook
jupyter notebook notebooks/cohort_analysis.ipynb

# 5. Or run the standalone viz script
python scripts/visualize_cohort.py
\`\`\`

---
*Analysis by Rahmadhania · April 2026*
""",
}


# =============================================================================
# Scaffold execution — no need to edit below this line
# =============================================================================

def create_project():
    # Step 1: Create the root project folder
    os.makedirs(PROJECT_ROOT, exist_ok=True)
    print(f"\n📁 Created project root: {PROJECT_ROOT}/\n")

    # Step 2: Create all subfolders
    for folder in FOLDERS:
        path = os.path.join(PROJECT_ROOT, folder)
        os.makedirs(path, exist_ok=True)
        print(f"  ✅ Folder created: {folder}/")

    print()

    # Step 3: Create all files with their starter content
    for relative_path, content in FILES.items():
        full_path = os.path.join(PROJECT_ROOT, relative_path)

        # Ensure the parent directory exists (handles nested paths)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        # Write the file (overwrite if it already exists)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"  📄 File created:   {relative_path}")

    # Step 4: Done — print next steps
    print(f"""
{'='*60}
✅ Project scaffolded successfully!

📂 Location: ./{PROJECT_ROOT}/

Next steps:
  1. cd {PROJECT_ROOT}
  2. pip install -r requirements.txt
  3. Download online_retail_II.xlsx from UCI and place in data/
  4. Copy your SQL scripts from Claude into sql/
  5. Open notebooks/cohort_analysis.ipynb and start exploring!
{'='*60}
""")


if __name__ == "__main__":
    create_project()
