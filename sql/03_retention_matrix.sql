-- =============================================================================
-- 03_retention_matrix.sql
-- Purpose : Build the raw cohort retention matrix — how many unique customers
--           from each cohort returned in each subsequent month (period index).
-- Output  : One row per (cohort_month, period_number) combination, with a
--           count of active customers. This is the input for rate calculation.
-- =============================================================================

DROP TABLE IF EXISTS retention_matrix;

CREATE TABLE retention_matrix AS

WITH cohort_periods AS (
    SELECT
        cohort_month,
        transaction_month,
        CustomerID,

        -- Calculate how many months after cohort month this transaction occurred
        -- We do this by converting 'YYYY-MM' strings to a numeric month offset:
        --   (year_diff * 12) + month_diff
        -- This gives us period 0 = cohort month, period 1 = one month later, etc.
        (
            -- Year component: difference in years × 12
            (CAST(SUBSTR(transaction_month, 1, 4) AS INTEGER) -
             CAST(SUBSTR(cohort_month,      1, 4) AS INTEGER)) * 12
            +
            -- Month component: difference in months
            (CAST(SUBSTR(transaction_month, 6, 2) AS INTEGER) -
             CAST(SUBSTR(cohort_month,      6, 2) AS INTEGER))
        ) AS period_number

    FROM customer_cohorts
)

SELECT
    cohort_month,
    period_number,

    -- Count distinct customers active in this cohort × period combination
    -- A customer counts once per period even if they bought multiple times
    COUNT(DISTINCT CustomerID) AS active_customers

FROM cohort_periods

GROUP BY
    cohort_month,
    period_number

-- Only include valid forward-looking periods (period 0 onward)
-- Negative values would indicate a data error in cohort assignment
HAVING period_number >= 0

ORDER BY
    cohort_month,
    period_number;

-- =============================================================================
-- Sanity check: period 0 should equal the cohort size (all customers present)
-- =============================================================================

-- SELECT cohort_month, active_customers AS cohort_size
-- FROM retention_matrix
-- WHERE period_number = 0
-- ORDER BY cohort_month;
