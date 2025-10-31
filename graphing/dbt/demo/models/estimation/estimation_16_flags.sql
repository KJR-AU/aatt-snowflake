WITH base AS (
    SELECT *,
        TRY_TO_NUMBER(subject_age, 10, 2) AS subject_age_num,
        reported_age AS reported_age_num
    FROM {{ ref('estimation_16_gate') }}
)

SELECT *,
    CASE
        WHEN subject_age_num >= 16 OR subject_age = '>=25' THEN TRUE
        WHEN subject_age_num < 16 OR subject_age = '<10' THEN FALSE
        ELSE NULL
    END AS actually_allowed,

    CASE
        WHEN verification_status = TRUE THEN TRUE
        WHEN verification_status = false THEN FALSE
        ELSE NULL
    END AS estimated_allowed,

FROM base
