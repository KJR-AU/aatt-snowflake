SELECT
    *,
FROM {{ ref('all_eligible_results') }}
WHERE age_gate = 0