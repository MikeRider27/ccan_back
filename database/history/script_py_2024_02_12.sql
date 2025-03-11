-- ALTER IN public.diagnosis_ap
alter table public.diagnosis_ap
    add dx_presuntivo text;

alter table public.diagnosis_ap
    add material text;

alter table public.diagnosis_ap
    add diagnostico text;

alter table public.diagnosis_ap
    add clasificacion text;

alter table public.diagnosis_ap
    add macroscopia text;

alter table public.diagnosis_ap
    add microscopia text;
