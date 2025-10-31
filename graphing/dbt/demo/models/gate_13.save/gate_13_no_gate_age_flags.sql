WITH base AS (
    SELECT *,
        TRY_TO_NUMBER(subject_age, 10, 2) AS subject_age_num,
        reported_age AS reported_age_num
    FROM {{ ref('gate_13_no_gate_specified') }}
)

SELECT *,
    CASE
        WHEN subject_age_num >= 13 OR subject_age = '>=25' THEN TRUE
        WHEN subject_age_num < 13 OR subject_age = '<10' THEN FALSE
        ELSE NULL
    END AS actually_allowed,

    CASE
        WHEN reported_age_num >= 13 THEN TRUE
        WHEN reported_age_num < 13 THEN FALSE
        ELSE NULL
    END AS estimated_allowed
FROM base
