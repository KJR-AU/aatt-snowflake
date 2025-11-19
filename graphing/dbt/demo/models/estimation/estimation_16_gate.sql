select *
from {{ ref('estimation_only') }}
where age_gate = 16 and
      verification_status IS NOT NULL and
      (
        reported_age IS NULL or
        ( verification_status = TRUE and reported_age >= 16 ) or
        ( verification_status = FALSE AND reported_age < 16 )
      )