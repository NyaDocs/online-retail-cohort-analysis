-- =============================================================================
-- 04_retention_rate.sql
-- Purpose : Convert the raw customer counts in the retention matrix into
--           percentage retention rates relative to each cohort's starting size.
-- Output  : Final table ready to be pivoted into a heatmap in Python.
--           Each row = one cohort × one period, with:
--             - cohort_size   : customers who joined in that cohort month
--             - active_customers : customers still active in that period
--             - retention_rate   : active / cohort_size as a percentage
-- =============================================================================

DROP TABLE IF EXISTS retention_rates;

CREATE TABLE retention_rates AS

WITH cohort_sizes AS (
    -- Pull the cohort size from period 0 (everyone was active at acquisition)
    SELECT
        cohort_month,
        active_customers AS cohort_size
    FROM retention_matrix
    WHERE period_number = 0
)

SELECT
    rm.cohort_month,
    rm.period_number,
    cs.cohort_size,
    rm.active_customers,

    -- Retention rate as a percentage, rounded to 2 decimal places
    -- We multiply by 100.0 (not 100) to force float division in SQLite
    ROUND(
        (rm.active_customers * 100.0) / cs.cohort_size,
        2
    ) AS retention_rate

FROM retention_matrix rm

-- Join cohort sizes so we always divide by the correct starting count
INNER JOIN cohort_sizes cs
    ON rm.cohort_month = cs.cohort_month

ORDER BY
    rm.cohort_month,
    rm.period_number;

-- =============================================================================
-- Final output preview: what this table looks like
-- =============================================================================
-- cohort_month | period_number | cohort_size | active_customers | retention_rate
-- -------------|---------------|-------------|------------------|---------------
-- 2009-12      | 0             | 948         | 948              | 100.00
-- 2009-12      | 1             | 948         | 362              | 38.19
-- 2009-12      | 2             | 948         | 317              | 33.44
-- ...          | ...           | ...         | ...              | ...

-- This table is what Python will read to generate the cohort heatmap.

-- =============================================================================
-- Sanity check: all period 0 rows should show 100.00% retention
-- =============================================================================

-- SELECT cohort_month, retention_rate
-- FROM retention_rates
-- WHERE period_number = 0
-- ORDER BY cohort_month;
-- Expected: every row = 100.00
