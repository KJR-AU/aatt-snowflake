SELECT *
FROM {{ ref('gate_13_all') }}
WHERE
    AGE_GATE = 13 
