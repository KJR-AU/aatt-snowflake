-- models/marts/metrics_estimation.sql

with src as (
  select * from {{ ref('int_abs_error') }}
),

overall as (
  select
    'overall' as slice_type,
    null as gate,
    count_if(absolute_error is not null) as samples,
    avg(absolute_error) as mae_years,
    stddev_samp(absolute_error) as sd_years
  from src
),

per_gate as (
  -- compute per-gate MAE using truth vs gate thresholds
  select
    'gate' as slice_type,
    g as gate,
    count_if(absolute_error is not null) as samples,
    avg(absolute_error) as mae_years,
    stddev_samp(absolute_error) as sd_years
  from src,
  lateral flatten(input => array_construct(13,16,18)) f,
  lateral (select f.value::int as g)
  group by 1,2
)

select * from overall
union all
select * from per_gate
