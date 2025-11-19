select *
from {{ ref('estimation_only') }}
where age_gate = 0 and reported_age > 0