-- models/clean/discard_old_methods.sql

SELECT
    *
FROM {{ ref('clean_with_type') }}
WHERE method in ('Estimation', 'Validation')