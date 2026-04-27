-- =============================================================================
-- 02_cohort_assignment.sql
-- Purpose : Assign each customer their cohort month — defined as the calendar
--           month of their very first purchase.
-- Why    : Cohort analysis groups customers by when they were "acquired".
--           Everyone who made their first purchase in, say, December 2009
--           belongs to the 2009-12 cohort, regardless of future behavior.
-- =============================================================================

DROP TABLE IF EXISTS customer_cohorts;

CREATE TABLE customer_cohorts AS

-- Step 1: Find the first purchase month for every customer
WITH first_purchase AS (
    SELECT
        CustomerID,

        -- Truncate InvoiceDate to year-month to define the cohort
        -- SQLite stores dates as text; SUBSTR extracts 'YYYY-MM' from 'YYYY-MM-DD ...'
        SUBSTR(InvoiceDate, 1, 7) AS cohort_month

    FROM clean_transactions

    -- GROUP BY customer to get one row per customer (their earliest transaction)
    GROUP BY CustomerID

    -- MIN on a 'YYYY-MM-DD' string works correctly because ISO dates sort lexicographically
    HAVING InvoiceDate = MIN(InvoiceDate)
)

-- Step 2: Join cohort info back onto every transaction for that customer
SELECT
    t.InvoiceNo,
    t.CustomerID,
    t.InvoiceDate,
    t.Revenue,

    -- The month this customer first appeared (their cohort label)
    f.cohort_month,

    -- The calendar month of the current transaction (for retention lookback)
    SUBSTR(t.InvoiceDate, 1, 7) AS transaction_month

FROM clean_transactions t

-- Every customer in clean_transactions must have a cohort month
INNER JOIN first_purchase f
    ON t.CustomerID = f.CustomerID;

-- =============================================================================
-- Sanity check: each customer should have exactly one cohort_month
-- =============================================================================

-- SELECT CustomerID, COUNT(DISTINCT cohort_month) AS cohort_count
-- FROM customer_cohorts
-- GROUP BY CustomerID
-- HAVING cohort_count > 1;
-- Expected: 0 rows (no customer should have more than one cohort)
