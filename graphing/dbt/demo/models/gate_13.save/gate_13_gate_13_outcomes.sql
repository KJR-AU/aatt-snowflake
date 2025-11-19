SELECT *,
    CASE
        WHEN actually_allowed = TRUE  AND estimated_allowed = TRUE  THEN 'TP'
        WHEN actually_allowed = FALSE AND estimated_allowed = FALSE THEN 'TN'
        WHEN actually_allowed = FALSE AND estimated_allowed = TRUE  THEN 'FP'
        WHEN actually_allowed = TRUE  AND estimated_allowed = FALSE THEN 'FN'
        ELSE 'Indeterminate'
    END AS outcome
FROM {{ ref('gate_13_no_gate_age_flags') }}
