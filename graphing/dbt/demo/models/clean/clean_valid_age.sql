-- models/clean/clean_valid_age.sql

SELECT
    *
FROM {{ ref('raw_data') }}
WHERE age_in_months > 0
