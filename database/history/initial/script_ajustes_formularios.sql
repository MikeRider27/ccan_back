ALTER TABLE public.patient
    RENAME COLUMN app_heart_others TO app_heart_others_input;

ALTER TABLE public.patient
    ADD app_heart_others boolean DEFAULT FALSE;

alter table public.patient
    rename column app_others to app_menopausal_others;

alter table public.patient
    drop column app_funtional_class_nyha;

alter table public.patient
    add app_funtional_class_nyha_id bigint;

alter table public.patient
    add constraint patient_fk_9
        foreign key (app_funtional_class_nyha_id) references public.parameter;

--- SETEAR PRIMERO LOS STRING A NULL EN LA TABLA
alter table public.diagnosis_ap
    alter column armpit_negative type boolean using armpit_negative::boolean;

alter table public.diagnosis_ap
    alter column armpit_positive type boolean using armpit_positive::boolean;
----

alter table public.diagnosis_ap
    add armpit_no_data boolean;

alter table public.diagnosis_ap
    add re_no_data boolean;

alter table public.diagnosis_ap
    add rp_no_data boolean;

alter table public.diagnosis_ap
    add her2_no_data boolean;

alter table public.diagnosis_ap
    add armpit_node_number integer;

comment on column public.diagnosis_ap.tumor_size is 'Size in cm.';

alter table public.diagnosis_ap
    alter column tumor_size type numeric using tumor_size::numeric;

------------------------------------------------

INSERT INTO public.parameter (domain, value, active, code)
VALUES ('NYHA_FUNTIONAL_CLASS', 'I', TRUE, 'I'),
       ('NYHA_FUNTIONAL_CLASS', 'II', TRUE, 'II'),
       ('NYHA_FUNTIONAL_CLASS', 'III', TRUE, 'III'),
       ('NYHA_FUNTIONAL_CLASS', 'IV', TRUE, 'IV');
