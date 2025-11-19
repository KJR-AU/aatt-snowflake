WITH base AS (
    SELECT RESULT_TIME,name,type,subject_age,verification_status,reported_age,time_in_seconds,actually_allowed,estimated_allowed
    FROM {{ ref('estimation_16_flags') }}
    UNION ALL
    SELECT RESULT_TIME,name,type,subject_age,verification_status,reported_age,time_in_seconds,actually_allowed_16 as actually_allowed,estimated_allowed_16 as estimated_allowed
    FROM {{ ref('estimation_0_flags') }}
)

SELECT *,
    CASE
        WHEN actually_allowed = TRUE  AND estimated_allowed = TRUE  THEN 'TP'
        WHEN actually_allowed = FALSE AND estimated_allowed = FALSE THEN 'TN'
        WHEN actually_allowed = FALSE AND estimated_allowed = TRUE  THEN 'FP'
        WHEN actually_allowed = TRUE  AND estimated_allowed = FALSE THEN 'FN'
        ELSE 'Indeterminate'
    END AS outcome
FROM base
