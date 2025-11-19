SELECT *
FROM {{ ref('modern_methods') }}
WHERE type in ('School', 'Mystery')