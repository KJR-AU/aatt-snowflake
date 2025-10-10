-- models/marts/metrics_gates.sql
with src as (
  select * from {{ ref('stg_results') }}
),
labels as (
  select
    *,
    -- truth: subject age >= gate
    (subject_age_years >= 13) as truth_13,
    (subject_age_years >= 16) as truth_16,
    (subject_age_years >= 18) as truth_18
  from src
  where subject_age_years between 0 and 100
    and verification_status_bool is not null
),
per_gate as (
  select '13' as gate,
    count(*) as samples,
    sum(iff(verification_status_bool and truth_13,1,0)) as tp,
    sum(iff(not verification_status_bool and not truth_13,1,0)) as tn,
    sum(iff(verification_status_bool and not truth_13,1,0)) as fp,
    sum(iff(not verification_status_bool and truth_13,1,0)) as fn
  from labels
  union all
  select '16',
    count(*),
    sum(iff(verification_status_bool and truth_16,1,0)),
    sum(iff(not verification_status_bool and not truth_16,1,0)),
    sum(iff(verification_status_bool and not truth_16,1,0)),
    sum(iff(not verification_status_bool and truth_16,1,0))
  from labels
  union all
  select '18',
    count(*),
    sum(iff(verification_status_bool and truth_18,1,0)),
    sum(iff(not verification_status_bool and not truth_18,1,0)),
    sum(iff(verification_status_bool and not truth_18,1,0)),
    sum(iff(not verification_status_bool and truth_18,1,0))
  from labels
),
metrics as (
  select
    gate,
    samples,
    tp, tn, fp, fn,
    (tp+tn)/nullif(samples,0) as accuracy,
    fp/nullif(fp+tn,0) as fpr,
    fn/nullif(tp+fn,0) as fnr,
    tp/nullif(tp+fn,0) as tpr,
    tn/nullif(tn+fp,0) as tnr
  from per_gate
)
select * from metrics
