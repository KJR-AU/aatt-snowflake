SELECT
    *,
    CASE
        WHEN reported_age >= 13 THEN TRUE
        ELSE FALSE
    END AS accepted
FROM {{ ref('valid_no_gate') }}