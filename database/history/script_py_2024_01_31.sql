-- ALTER IN public.diagnosis_ap
alter table public.diagnosis_ap
    alter column tumor_size drop not null;

-- ALTER IN public.treatment_follow_up
alter table public.treatment_follow_up
    drop column every_three_weeks;

alter table public.treatment_follow_up
    drop column weekly;

