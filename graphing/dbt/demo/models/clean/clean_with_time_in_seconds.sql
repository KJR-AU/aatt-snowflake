select *,
  DATE_PART('hour', VERIFICATION_TIME) * 3600
  + DATE_PART('minute', VERIFICATION_TIME) * 60
  + DATE_PART('second', VERIFICATION_TIME) AS TIME_IN_SECONDS
from {{ ref('clean_with_type') }}