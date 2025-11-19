WITH base AS (
    SELECT *,
        TRY_TO_NUMBER(subject_age, 10, 2) AS subject_age_num,
        reported_age AS reported_age_num
    FROM {{ ref('estimation_0_gate') }}
)

SELECT *,
    CASE
        WHEN subject_age_num >= 13 OR subject_age = '>=25' THEN TRUE
        WHEN subject_age_num < 13 OR subject_age = '<10' THEN FALSE
        ELSE NULL
    END AS actually_allowed_13,

    CASE
        WHEN reported_age_num >= 13 THEN TRUE
        WHEN reported_age_num < 13 THEN FALSE
        ELSE NULL
    END AS estimated_allowed_13,

    CASE
        WHEN subject_age_num >= 16 OR subject_age = '>=25' THEN TRUE
        WHEN subject_age_num < 16 OR subject_age = '<10' THEN FALSE
        ELSE NULL
    END AS actually_allowed_16,

    CASE
        WHEN reported_age_num >= 16 THEN TRUE
        WHEN reported_age_num < 16 THEN FALSE
        ELSE NULL
    END AS estimated_allowed_16,

    CASE
        WHEN subject_age_num >= 18 OR subject_age = '>=25' THEN TRUE
        WHEN subject_age_num < 18 OR subject_age = '<10' THEN FALSE
        ELSE NULL
    END AS actually_allowed_18,

    CASE
        WHEN reported_age_num >= 18 THEN TRUE
        WHEN reported_age_num < 18 THEN FALSE
        ELSE NULL
    END AS estimated_allowed_18
FROM base
