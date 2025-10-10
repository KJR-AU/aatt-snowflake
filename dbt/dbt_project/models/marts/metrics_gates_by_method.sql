with src as (
  select * from {{ ref('stg_results') }}
  where subject_age_years between 0 and 100 and verification_status_bool is not null
),
calc as (
  select method_norm,
         iff(subject_age_years>=13,1,0) as truth_13,
         iff(subject_age_years>=16,1,0) as truth_16,
         iff(subject_age_years>=18,1,0) as truth_18,
         iff(verification_status_bool,1,0) as pred
  from src
),
g13 as (
  select method_norm, '13' as gate,
         count(*) samples,
         sum(iff(pred=1 and truth_13=1,1,0)) tp,
         sum(iff(pred=0 and truth_13=0,1,0)) tn,
         sum(iff(pred=1 and truth_13=0,1,0)) fp,
         sum(iff(pred=0 and truth_13=1,1,0)) fn
  from calc group by 1
),
g16 as (
  select method_norm, '16' gate, count(*) samples,
         sum(iff(pred=1 and truth_16=1,1,0)) tp,
         sum(iff(pred=0 and truth_16=0,1,0)) tn,
         sum(iff(pred=1 and truth_16=0,1,0)) fp,
         sum(iff(pred=0 and truth_16=1,1,0)) fn
  from calc group by 1
),
g18 as (
  select method_norm, '18' gate, count(*) samples,
         sum(iff(pred=1 and truth_18=1,1,0)) tp,
         sum(iff(pred=0 and truth_18=0,1,0)) tn,
         sum(iff(pred=1 and truth_18=0,1,0)) fp,
         sum(iff(pred=0 and truth_18=1,1,0)) fn
  from calc group by 1
),
unioned as (
  select * from g13 union all select * from g16 union all select * from g18
)
select method_norm, gate, samples, tp, tn, fp, fn,
       (tp+tn)/nullif(samples,0) accuracy,
       fp/nullif(fp+tn,0) fpr,
       fn/nullif(tp+fn,0) fnr,
       tp/nullif(tp+fn,0) tpr,
       tn/nullif(tn+fp,0) tnr
from unioned
