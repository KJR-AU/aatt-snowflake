-- models/marts/metrics_verification_time.sql
with src as (
  select * from {{ ref('stg_results') }}
  where verification_seconds is not null
)
select
  method_norm as method,
  count(*) as samples,
  avg(verification_seconds) as mean_seconds,
  median(verification_seconds) as median_seconds
from src
group by 1
