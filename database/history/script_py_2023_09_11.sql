-- ELIMINAR TABLAS NO USADAS
-- DROP TABLE public.treatment_order;
-- DROP TABLE public.medical_visit;
-- DROP TABLE public.diagnosis;
-- DROP TABLE public.medicine_medication_order;
-- DROP TABLE public.medication_order;
-- DROP TABLE public.medication;

-------------------------------------------------------
-- AGREGAR CAMPOS DE AUDITORIA EN TABLAS PRINCIPALES --
-------------------------------------------------------
-- public.user
alter table public."user"
    add date_create timestamp(0) default NOW() not null;

alter table public."user"
    add user_create varchar(30) default 'readiness' not null;

alter table public."user"
    add date_modify timestamp(0);

alter table public."user"
    add user_modify varchar(30);

alter table public."user"
    alter column user_create drop not null;


-- public.role
alter table public.role
    add date_create timestamp(0) default NOW() not null;

alter table public.role
    add user_create varchar(30) default 'readiness' not null;

alter table public.role
    add date_modify timestamp(0);

alter table public.role
    add user_modify varchar(30);

alter table public.role
    alter column user_create drop not null;

-- public.doctor
alter table public.doctor
    add date_create timestamp(0) default NOW() not null;

alter table public.doctor
    add user_create varchar(30) default 'readiness' not null;

alter table public.doctor
    add date_modify timestamp(0);

alter table public.doctor
    add user_modify varchar(30);

alter table public.doctor
    alter column user_create drop not null;

-- public.hospital
alter table public.hospital
    add date_create timestamp(0) default NOW() not null;

alter table public.hospital
    add user_create varchar(30) default 'readiness' not null;

alter table public.hospital
    add date_modify timestamp(0);

alter table public.hospital
    add user_modify varchar(30);

alter table public.hospital
    alter column user_create drop not null;

-- public.patient
alter table public.patient
    add date_create timestamp(0) default NOW() not null;

alter table public.patient
    add user_create varchar(30) default 'readiness' not null;

alter table public.patient
    add date_modify timestamp(0);

alter table public.patient
    add user_modify varchar(30);

alter table public.patient
    alter column user_create drop not null;

-- public.surgery
alter table public.surgery
    add date_create timestamp(0) default NOW() not null;

alter table public.surgery
    add user_create varchar(30) default 'readiness' not null;

alter table public.surgery
    add date_modify timestamp(0);

alter table public.surgery
    add user_modify varchar(30);

alter table public.surgery
    alter column user_create drop not null;

-- public.puncture
alter table public.puncture
    add date_create timestamp(0) default NOW() not null;

alter table public.puncture
    add user_create varchar(30) default 'readiness' not null;

alter table public.puncture
    add date_modify timestamp(0);

alter table public.puncture
    add user_modify varchar(30);

alter table public.puncture
    alter column user_create drop not null;

-- public.medicine
alter table public.medicine
    add date_create timestamp(0) default NOW() not null;

alter table public.medicine
    add user_create varchar(30) default 'readiness' not null;

alter table public.medicine
    add date_modify timestamp(0);

alter table public.medicine
    add user_modify varchar(30);

alter table public.medicine
    alter column user_create drop not null;

-- public.chemotherapy
alter table public.chemotherapy
    add date_create timestamp(0) default NOW() not null;

alter table public.chemotherapy
    add user_create varchar(30) default 'readiness' not null;

alter table public.chemotherapy
    add date_modify timestamp(0);

alter table public.chemotherapy
    add user_modify varchar(30);

alter table public.chemotherapy
    alter column user_create drop not null;

-- public.diagnosis_ap
alter table public.diagnosis_ap
    add date_create timestamp(0) default NOW() not null;

alter table public.diagnosis_ap
    add user_create varchar(30) default 'readiness' not null;

alter table public.diagnosis_ap
    add date_modify timestamp(0);

alter table public.diagnosis_ap
    add user_modify varchar(30);

alter table public.diagnosis_ap
    alter column user_create drop not null;

-- public.radiotherapy
alter table public.radiotherapy
    add date_create timestamp(0) default NOW() not null;

alter table public.radiotherapy
    add user_create varchar(30) default 'readiness' not null;

alter table public.radiotherapy
    add date_modify timestamp(0);

alter table public.radiotherapy
    add user_modify varchar(30);

alter table public.radiotherapy
    alter column user_create drop not null;

-- public.committee
alter table public.committee
    add date_create timestamp(0) default NOW() not null;

alter table public.committee
    add user_create varchar(30) default 'readiness' not null;

alter table public.committee
    add date_modify timestamp(0);

alter table public.committee
    add user_modify varchar(30);

alter table public.committee
    alter column user_create drop not null;

-- public.patient_exclusion_criteria
alter table public.patient_exclusion_criteria
    add date_create timestamp(0) default NOW() not null;

alter table public.patient_exclusion_criteria
    add user_create varchar(30) default 'readiness' not null;

alter table public.patient_exclusion_criteria
    add date_modify timestamp(0);

alter table public.patient_exclusion_criteria
    add user_modify varchar(30);

alter table public.patient_exclusion_criteria
    alter column user_create drop not null;

-- public.patient_inclusion_criteria_adjuvant_trastuzumab
alter table public.patient_inclusion_criteria_adjuvant_trastuzumab
    add date_create timestamp(0) default NOW() not null;

alter table public.patient_inclusion_criteria_adjuvant_trastuzumab
    add user_create varchar(30) default 'readiness' not null;

alter table public.patient_inclusion_criteria_adjuvant_trastuzumab
    add date_modify timestamp(0);

alter table public.patient_inclusion_criteria_adjuvant_trastuzumab
    add user_modify varchar(30);

alter table public.patient_inclusion_criteria_adjuvant_trastuzumab
    alter column user_create drop not null;

-- public.patient_inclusion_criteria_neoadjuvant_trastuzumab
alter table public.patient_inclusion_criteria_neoadjuvant_trastuzumab
    add date_create timestamp(0) default NOW() not null;

alter table public.patient_inclusion_criteria_neoadjuvant_trastuzumab
    add user_create varchar(30) default 'readiness' not null;

alter table public.patient_inclusion_criteria_neoadjuvant_trastuzumab
    add date_modify timestamp(0);

alter table public.patient_inclusion_criteria_neoadjuvant_trastuzumab
    add user_modify varchar(30);

alter table public.patient_inclusion_criteria_neoadjuvant_trastuzumab
    alter column user_create drop not null;

-- public.additional_patient_information
alter table public.additional_patient_information
    add date_create timestamp(0) default NOW() not null;

alter table public.additional_patient_information
    add user_create varchar(30) default 'readiness' not null;

alter table public.additional_patient_information
    add date_modify timestamp(0);

alter table public.additional_patient_information
    add user_modify varchar(30);

alter table public.additional_patient_information
    alter column user_create drop not null;

-- public.medical_document
alter table public.medical_document
    add date_create timestamp(0) default NOW() not null;

alter table public.medical_document
    add user_create varchar(30) default 'readiness' not null;

alter table public.medical_document
    add date_modify timestamp(0);

alter table public.medical_document
    add user_modify varchar(30);

alter table public.medical_document
    alter column user_create drop not null;

-- public.patient_inclusion_criteria
alter table public.patient_inclusion_criteria
    add date_create timestamp(0) default NOW() not null;

alter table public.patient_inclusion_criteria
    add user_create varchar(30) default 'readiness' not null;

alter table public.patient_inclusion_criteria
    add date_modify timestamp(0);

alter table public.patient_inclusion_criteria
    add user_modify varchar(30);

alter table public.patient_inclusion_criteria
    alter column user_create drop not null;

-- public.treatment_follow_up
alter table public.treatment_follow_up
    add date_create timestamp(0) default NOW() not null;

alter table public.treatment_follow_up
    add user_create varchar(30) default 'readiness' not null;

alter table public.treatment_follow_up
    add date_modify timestamp(0);

alter table public.treatment_follow_up
    add user_modify varchar(30);

alter table public.treatment_follow_up
    alter column user_create drop not null;

-------------------------------------
-- CREAR LA TABLA public.specialty --
-------------------------------------
CREATE TABLE public.specialty
(
    id          bigserial PRIMARY KEY,
    description varchar(300)
);

--------------------------------------------
-- CREAR LA TABLA public.doctor_specialty --
--------------------------------------------
CREATE TABLE public.doctor_specialty
(
    id           bigserial PRIMARY KEY,
    doctor_id    bigint NOT NULL
        CONSTRAINT doctor_specialty_fk_1
            REFERENCES public.doctor,
    specialty_id bigint NOT NULL
        CONSTRAINT doctor_specialty_fk
            REFERENCES public.specialty
);

---------------------------
-- INSERCIÓN DE PERMISOS --
---------------------------
INSERT INTO public.permission (description)
VALUES ('specialty_list'),
       ('specialty_search'),
       ('specialty_get'),
       ('specialty_insert'),
       ('specialty_update'),
       ('specialty_delete'),
       ('doctor_specialty_list'),
       ('doctor_specialty_search'),
       ('doctor_specialty_get'),
       ('doctor_specialty_insert'),
       ('doctor_specialty_update'),
       ('doctor_specialty_delete');

------------------------------------------------------
-- AGREGAR COLUMNA doctor_id EN public.diagnosis_ap --
------------------------------------------------------
ALTER TABLE public.diagnosis_ap
    ADD doctor_id bigint;

--------------------------------
-- AGREGAR FK A public.doctor --
--------------------------------
ALTER TABLE public.diagnosis_ap
    ADD CONSTRAINT diagnosis_ap_doctor_id_fk
        FOREIGN KEY (doctor_id) REFERENCES public.doctor;

---------------------------------------------------------
-- SE AGREGA CAMPO registration_date EN public.patient --
---------------------------------------------------------
alter table public.patient
    add registration_date date default now() not null;

------------------------------------------------------
-- SE AGREGA CAMPO ESTADO CIVIL EN public.parameter --
------------------------------------------------------
INSERT INTO public.parameter (domain, value, active, code)
VALUES ('PATIENT_CIVIL_STATUS', 'SOLTERO', true, 'SOL'),
       ('PATIENT_CIVIL_STATUS', 'CASADO', true, 'CAS'),
       ('PATIENT_CIVIL_STATUS', 'DIVORCIADO', true, 'DIV'),
       ('PATIENT_CIVIL_STATUS', 'SEPARADO', true, 'SEP'),
       ('PATIENT_CIVIL_STATUS', 'VIUDO', true, 'VIU'),
       ('PATIENT_CIVIL_STATUS', 'PAREJA DE HECHO', true, 'PAR_HEC');

-----------------------------------------------------------------------
-- SE AGREGA CAMPO DEPARTAMENTO O SERVICIO CIVIL EN public.parameter --
-----------------------------------------------------------------------
INSERT INTO public.parameter (domain, value, active, code)
VALUES ('HOSPITAL_DEPARTMENT', 'MASTOLOGÍA', true, 'MASTOLOGIA'),
       ('HOSPITAL_DEPARTMENT', 'ONCOLOGÍA', true, 'ONCOLOGIA'),
       ('HOSPITAL_DEPARTMENT', 'CIRUGÍA ONCOLÓGICA', true, 'CIR_ONCOLOGICA'),
       ('HOSPITAL_DEPARTMENT', 'NUTRICIÓN', true, 'NUTRICION'),
       ('HOSPITAL_DEPARTMENT', 'PSICOLOGÍA', true, 'PSICOLOGIA'),
       ('HOSPITAL_DEPARTMENT', 'GASTROENTEROLOGÍA', true, 'GASTROENTEROLOGIA'),
       ('HOSPITAL_DEPARTMENT', 'ANATOMÍA PATOLÓGICA', true, 'ANAT_PATOLOGICA'),
       ('HOSPITAL_DEPARTMENT', 'RADIOTERAPIA', true, 'RADIOTERAPIA');

-----------------------------
-- ALTER EN public.patient --
-----------------------------
ALTER TABLE public.patient
    ADD civil_status_id bigint;

ALTER TABLE public.patient
    ADD responsible_firstname text;

ALTER TABLE public.patient
    ADD responsible_lastname text;

ALTER TABLE public.patient
    ADD responsible_relationship text;

ALTER TABLE public.patient
    ADD responsible_phone varchar(50);

ALTER TABLE public.patient
    ADD hospital_departament_id bigint;

ALTER TABLE public.patient
    ADD number_card integer;

ALTER TABLE public.patient
    ADD her2_positive boolean;

ALTER TABLE public.patient
    ADD CONSTRAINT patient_parameter_id_fk
        FOREIGN KEY (civil_status_id) REFERENCES public.parameter;

ALTER TABLE public.patient
    ADD CONSTRAINT patient_parameter_id_fk2
        FOREIGN KEY (hospital_departament_id) REFERENCES public.parameter;

-------------------------------------------------------------
-- SE AGREGA DOMINIO DIAGNOSTICADO POR EN public.parameter --
-------------------------------------------------------------
INSERT INTO public.parameter (domain, value, active, code)
VALUES ('DIAGNOSIS_BY', 'ANATOMÍA PATOLÓGICA', true, 'ANAT_PATOLOGICA'),
       ('DIAGNOSIS_BY', 'IMAGENOLOGÍA', true, 'IMAGENOLOGIA');

------------------------------------------------
-- SE CREA TABLA public.medical_consultation --
------------------------------------------------
CREATE TABLE public.medical_consultation
(
    id                    bigserial PRIMARY KEY,
    Date_first_diagnosis  date,
    diagnosis_by_id       bigint,
    medicine_presentation text,
    observation           text,
    date_create           timestamp(0) DEFAULT NOW() NOT NULL,
    user_create           varchar(30)  DEFAULT 'readiness'::character varying,
    date_modify           timestamp(0),
    user_modify           varchar(30)
);

ALTER TABLE public.medical_consultation
    ADD CONSTRAINT medical_consultation_parameter_id_fk
        FOREIGN KEY (diagnosis_by_id) REFERENCES public.parameter;

------------------------------------------------
-- permisos de public.medical_consultation --
------------------------------------------------
INSERT INTO public.permission (description)
VALUES ('medical_consultation_list'),
       ('medical_consultation_search'),
       ('medical_consultation_get'),
       ('medical_consultation_insert'),
       ('medical_consultation_update'),
       ('medical_consultation_delete');

INSERT INTO role_permission (role_id, permission_id)
SELECT (SELECT id FROM role WHERE description = 'MEDICO'),
       id
FROM permission
WHERE description IN ('medical_consultation_list',
       'medical_consultation_search',
       'medical_consultation_get',
       'medical_consultation_insert',
       'medical_consultation_update',
       'medical_consultation_delete');

INSERT INTO role_permission (role_id, permission_id)
SELECT (SELECT id FROM role WHERE description = 'ADMINISTRADOR'),
       id
FROM permission
WHERE description IN ('medical_consultation_list',
       'medical_consultation_search',
       'medical_consultation_get',
       'medical_consultation_insert',
       'medical_consultation_update',
       'medical_consultation_delete');

-----------------------------
-- ALTER EN public.patient --
-----------------------------
ALTER TABLE public.patient
    ADD medical_consultation_id bigint;

ALTER TABLE public.patient
    ADD CONSTRAINT patient_medical_consultation_id_fk
        FOREIGN KEY (medical_consultation_id) REFERENCES public.medical_consultation;

------------------------------------------------------
-- CREAR TABLA public.personal_pathological_history --
------------------------------------------------------
CREATE TABLE public.personal_pathological_history
(
    id                          BIGSERIAL PRIMARY KEY,
    patient_id                  bigint
        CONSTRAINT personal_pathological_history_patient_fk REFERENCES public.patient,
    family_members_with_cancer  boolean,
    main_findings               text,
    app_funtional_class_nyha_id bigint
        CONSTRAINT personal_pathological_history_parameter
            REFERENCES public.parameter,
    app_ischemic_heart_disease  boolean      DEFAULT FALSE NOT NULL,
    app_heart_failure           boolean      DEFAULT FALSE NOT NULL,
    app_arrhythmia              boolean      DEFAULT FALSE NOT NULL,
    app_heart_others            boolean      DEFAULT FALSE,
    app_heart_others_input      text,
    menopausal_state_id         bigint
        CONSTRAINT personal_pathological_history_parameter_2
            REFERENCES public.menopausal_state,
    app_menopausal_others       text,
    fevi_percentage             integer,
    fevi_date                   timestamp(0),
    date_create                 timestamp(0) DEFAULT NOW() NOT NULL,
    user_create                 varchar(30)  DEFAULT 'readiness'::character varying,
    date_modify                 timestamp(0),
    user_modify                 varchar(30)
);

---------------------------------------------------
-- POBLAR LA TABLA personal_pathological_history --
---------------------------------------------------
INSERT INTO public.personal_pathological_history (patient_id, app_funtional_class_nyha_id, app_ischemic_heart_disease,
                                           app_heart_failure, app_arrhythmia, app_heart_others, app_heart_others_input,
                                           menopausal_state_id, app_menopausal_others, fevi_percentage, fevi_date)
SELECT id,
       app_funtional_class_nyha_id,
       app_ischemic_heart_disease,
       app_heart_failure,
       app_arrhythmia,
       app_heart_others,
       app_heart_others_input,
       menopausal_state_id,
       app_menopausal_others,
       fevi_percentage,
       fevi_date
FROM public.patient
ORDER BY id;

-----------------------------
-- ALTER EN public.patient --
-----------------------------
ALTER TABLE public.patient
    DROP COLUMN menopausal_state_id;

ALTER TABLE public.patient
    DROP COLUMN app_ischemic_heart_disease;

ALTER TABLE public.patient
    DROP COLUMN app_heart_failure;

ALTER TABLE public.patient
    DROP COLUMN app_arrhythmia;

ALTER TABLE public.patient
    DROP COLUMN app_menopausal_others;

ALTER TABLE public.patient
    DROP COLUMN app_heart_others_input;

ALTER TABLE public.patient
    DROP COLUMN fevi_percentage;

ALTER TABLE public.patient
    DROP COLUMN fevi_date;

ALTER TABLE public.patient
    DROP COLUMN app_heart_others;

ALTER TABLE public.patient
    DROP COLUMN app_funtional_class_nyha_id;

ALTER TABLE public.patient
    ADD personal_pathological_history_id bigint;

ALTER TABLE public.patient
    ADD CONSTRAINT patient_personal_pathological_history_id_fk
        FOREIGN KEY (personal_pathological_history_id) REFERENCES public.personal_pathological_history;

-------------------------------------
-- UPDATE MASIVO EN public.patient --
-------------------------------------
UPDATE public.patient
SET personal_pathological_history_id=pph.id
FROM (SELECT id, patient_id
      FROM public.personal_pathological_history) AS pph
WHERE patient.id=pph.patient_id;

-----------------------------
-- ALTER EN public.patient --
-----------------------------
alter table public.personal_pathological_history
    drop column patient_id;

-------------------------------------------------------------
-- SE AGREGA DOMINIO DIAGNOSTICADO POR EN public.parameter --
-------------------------------------------------------------
INSERT INTO public.parameter (domain, value, active, code)
VALUES ('FAMILIAR', 'MADRE', true, 'MADRE'),
       ('FAMILIAR', 'PADRE', true, 'PADRE'),
       ('FAMILIAR', 'ABUELO', true, 'ABUELO'),
       ('FAMILIAR', 'ABUELA', true, 'ABUELA'),
       ('FAMILIAR', 'TÍO', true, 'TIO');

INSERT INTO public.parameter (domain, value, active, code)
VALUES ('FAMILIAR_VITAL_STATE', 'VIVO', true, 'FAM_VIVO'),
       ('FAMILIAR_VITAL_STATE', 'FALLECIDO', true, 'FAM_FALLEC');

-----------------------------------------------------
-- SE CREA TABLA public.patient_family_with_cancer --
-----------------------------------------------------
CREATE TABLE public.patient_family_with_cancer
(
    id                               bigserial
        CONSTRAINT patient_family_with_cancer_pk
            PRIMARY KEY,
    personal_pathological_history_id bigint
        CONSTRAINT patient_family_with_cancer_personal_pathological_history_id_fk
            REFERENCES public.personal_pathological_history,
    family_id                        bigint
        CONSTRAINT patient_family_with_cancer_parameter_id_fk
            REFERENCES public.parameter,
    family_vital_state_id            bigint
        CONSTRAINT patient_family_with_cancer_parameter_id_fk2
            REFERENCES public.parameter
);

--=============>>>>>>>> HASTA ACA EN EL SERVER DE PRUEBAS DE CODELAB Y POSIBLEMENTE PROD
