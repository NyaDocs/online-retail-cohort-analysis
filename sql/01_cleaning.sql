-- =============================================================================
-- 01_cleaning.sql
-- Purpose : Filter raw Online Retail II data down to a clean, analysis-ready
--           table of valid transactions.
-- Approach: We exclude cancellations, missing customers, and zero/negative
--           prices because they distort revenue and cohort calculations.
-- =============================================================================

-- Drop the cleaned table if it already exists so we can re-run safely
DROP TABLE IF EXISTS clean_transactions;

-- Create the cleaned table from the raw source table (assumed name: raw_retail)
CREATE TABLE clean_transactions AS
SELECT
    InvoiceNo,
    StockCode,
    Description,
    Quantity,
    InvoiceDate,
    UnitPrice,
    CustomerID,
    Country,

    -- Derive a Revenue column here so every downstream query can use it directly
    ROUND(Quantity * UnitPrice, 2) AS Revenue

FROM raw_retail

WHERE
    -- 1. Remove cancellations: invoices starting with 'C' are returns/reversals
    --    These would create negative revenue and mess up first-purchase detection
    InvoiceNo NOT LIKE 'C%'

    -- 2. Remove rows with no CustomerID: we cannot build customer-level cohorts
    --    without knowing who the customer is (~25% of rows are affected)
    AND CustomerID IS NOT NULL
    AND CustomerID != ''

    -- 3. Remove zero or negative unit prices: likely internal transfers or errors
    AND UnitPrice > 0

    -- 4. Remove zero or negative quantities: additional safety net beyond the
    --    'C' prefix check (some bad rows slip through without the C prefix)
    AND Quantity > 0;

-- =============================================================================
-- Quick sanity check: review row counts before and after cleaning
-- Run these SELECT statements manually to validate your filter results
-- =============================================================================

-- Total raw rows
-- SELECT COUNT(*) AS raw_row_count FROM raw_retail;

-- Cleaned rows
-- SELECT COUNT(*) AS clean_row_count FROM clean_transactions;

-- Unique customers in cleaned data
-- SELECT COUNT(DISTINCT CustomerID) AS unique_customers FROM clean_transactions;

-- Date range covered
-- SELECT MIN(InvoiceDate) AS earliest, MAX(InvoiceDate) AS latest
-- FROM clean_transactions;
