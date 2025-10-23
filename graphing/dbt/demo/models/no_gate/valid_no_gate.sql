SELECT
    *,
FROM {{ ref('no_gate') }}
WHERE reported_age > 0