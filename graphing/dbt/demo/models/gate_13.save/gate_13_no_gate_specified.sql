SELECT *
FROM {{ ref('gate_13_all') }}
WHERE
    AGE_GATE = 0 
    AND REPORTED_AGE > 0