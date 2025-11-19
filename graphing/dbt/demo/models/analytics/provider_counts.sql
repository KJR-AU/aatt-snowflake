SELECT
    NAME, COUNT(*) AS provider_count,
FROM {{ ref('all_eligible_results') }}
GROUP BY NAME