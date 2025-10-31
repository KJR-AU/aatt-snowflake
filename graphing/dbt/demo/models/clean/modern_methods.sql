-- models/clean/discard_old_methods.sql

SELECT
    *
FROM {{ ref('clean_with_time_in_seconds') }}
WHERE method in ('Estimation', 'Validation')