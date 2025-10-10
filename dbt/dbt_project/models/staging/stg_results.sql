-- models/staging/stg_results.sql

with raw as (
  select * from {{ target.database }}.{{ target.schema }}.RAW_RESULTS
),

typed as (
  select
    id,
    custom_id,
    create_user,
    try_to_timestamp_ntz(to_varchar(result_time)) as result_time,
    name,
    method,
    case method
      when 'AE' then 'Estimation'
      when 'AV' then 'Verification'
      when 'AI' then 'Inference'
      else method
    end as method_norm,
    try_to_number(to_varchar(age_gate)) as age_gate,
    subject_id,
    try_to_date(to_varchar(date_of_birth)) as date_of_birth,
    try_to_number(to_varchar(age_in_months)) as age_in_months_num,
    country_of_birth_subject,
    country_of_birth_mother,
    country_of_birth_father,
    origin,

    /* verification flag (raw) */
    case
      when upper(coalesce(to_varchar(verification_status), '')) in ('TRUE','T','1','Y','YES') then true
      when upper(coalesce(to_varchar(verification_status), '')) in ('FALSE','F','0','N','NO') then false
      else null
    end as verification_status_bool_raw,

    /* keep original text so we can parse seconds later */
    to_varchar(verification_time) as verification_time,

    /* subject age in years (raw):
       1) use age_in_months when present,
       2) else derive from date_of_birth + result_time
    */
    coalesce(
      case when age_in_months_num is not null then age_in_months_num / 12.0 end,
      case
        when date_of_birth is not null and result_time is not null
        then datediff(month, date_of_birth, result_time) / 12.0
      end
    ) as subject_age_years_raw

  from raw
),

calc as (
  select
    *,
    case
      when '{{ env_var("INVERT_VERIFICATION_FLAG","false") }}' ilike 'true'
      then not verification_status_bool_raw
      else verification_status_bool_raw
    end as verification_status_bool
  from typed
)

select
  id,
  custom_id,
  create_user,
  result_time,
  name,
  method,
  method_norm,
  age_gate,
  subject_id,
  date_of_birth,
  age_in_months_num,
  country_of_birth_subject,
  country_of_birth_mother,
  country_of_birth_father,
  origin,

  /* clamp to a sensible range */
  case
    when subject_age_years_raw between 0 and 110 then subject_age_years_raw
    else null
  end as subject_age_years,

  verification_status_bool,

  /* parse hh:mm:ss(.fff) → total seconds */
  case
    when verification_time is null then null
    else
      split_part(verification_time, ':', 1)::int * 3600 +
      split_part(verification_time, ':', 2)::int * 60 +
      split_part(verification_time, ':', 3)::float
  end as verification_seconds

from calc
