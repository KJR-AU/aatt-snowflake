{% set raw_rel = adapter.get_relation(
    database=target.database,
    schema=target.schema,
    identifier='RAW_RESULTS'
) %}

{% set raw_cols = adapter.get_columns_in_relation(raw_rel) %}
{% set colnames = [] %}
{% for c in raw_cols %}
  {% do colnames.append(c.name.upper()) %}
{% endfor %}

{% set has_reported_age  = 'REPORTED_AGE'  in colnames %}
{% set has_estimated_age = 'ESTIMATED_AGE' in colnames %}

with
base as (
  select * from {{ ref('stg_results') }}
),

raw_pred as (
  select
    id,
    {% if has_reported_age %}
      try_to_number(to_varchar(reported_age))  as predicted_age_years
    {% elif has_estimated_age %}
      try_to_number(to_varchar(estimated_age)) as predicted_age_years
    {% else %}
      null::float as predicted_age_years
    {% endif %}
  from {{ target.database }}.{{ target.schema }}.RAW_RESULTS
),

joined as (
  select
    b.*,
    r.predicted_age_years
  from base b
  left join raw_pred r using (id)
)

select
  *,
  case
    when predicted_age_years is not null and subject_age_years is not null
      then abs(predicted_age_years - subject_age_years)
    else null
  end as absolute_error
from joined
