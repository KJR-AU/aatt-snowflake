SELECT
    *,
    CASE
        WHEN age_in_months >= 300 THEN '>=25'
        WHEN age_in_months < 120 THEN '<10'
        ELSE TO_VARCHAR(ROUND(age_in_months / 12.0, 2))
    END AS subject_age
FROM {{ ref('clean_valid_age') }}