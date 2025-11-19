select result_time, name, type, age_gate, subject_age, verification_status, reported_age,time_in_seconds
from {{ ref('all_eligible_results') }}
where method = 'Estimation'