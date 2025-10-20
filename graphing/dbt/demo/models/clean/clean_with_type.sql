-- models/clean/clean_with_type.sql

SELECT
    c.*,
    COALESCE(m.type, 'Internal') AS type
FROM {{ ref('clean_age') }} AS c
LEFT JOIN {{ ref('cohort_map') }} AS m
    ON c.create_user = m.create_user