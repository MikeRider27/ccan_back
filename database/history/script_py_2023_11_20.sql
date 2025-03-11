-- CAMBIO DE DESCRIPCION DE TIPO DE DOCUMENTO
UPDATE medical_document_type
SET description = 'INFORME DE INMUNOHISTOQUÍMICA'
WHERE description = 'INFORME DE IHQ';

UPDATE medical_document_type
SET description = 'CONSENTIMIENTO DE USO DE DATOS'
WHERE description = 'CONSENTIMIENTO DE USO DE DATOS PERSONALES';

-- CAMBIOS EN public.medical_document
alter table public.medical_document
    drop column title;

alter table public.medical_document
    alter column description drop not null;

-- CAMBIOS EN public.medical_document
alter table public.medical_document
    rename column tab_origin to modulo;

comment on column public.medical_document.modulo is 'Módulo al cual pertenece el documento.';

alter table public.medical_document
    add origen_id bigint;

comment on column public.medical_document.origen_id is 'Id del modulo de origen del documento.';

-- CREATE TABLE public.configuration
CREATE TABLE public.configuration
(
    id    bigserial
        CONSTRAINT configuration_pk
            PRIMARY KEY,
    name  varchar(100),
    value varchar(50),
    code  varchar(50)
);

--  ADD CONFIGURATION
INSERT INTO configuration (name, "value", code)
VALUES ('INTEROPERABILITY_SERVICES', 'ACTIVE', 'IS');
INSERT INTO configuration (name, "value", code)
VALUES ('INTEROPERABILITY_PATIENT_DATA', 'ACTIVE', 'IPD');

--  DELETE PARAM
DELETE
FROM public.parameter
WHERE domain = 'AUTOCOMPLETE_SERVICE_STATE';


-- CREATE TABLE public.diagnosis
CREATE TABLE public.diagnosis
(
    id                      bigserial,
    patient_id              bigserial
        CONSTRAINT diagnosis_patient_id_fk
            REFERENCES public.patient,
    date                    timestamp(0),
    codification_type       varchar(10),
    cie_10_code_id          bigint
        CONSTRAINT diagnosis_cie_10_id_fk
            REFERENCES public.cie_10,
    cie_o_morphology_id     bigint
        CONSTRAINT diagnosis_cie_o_morphology_id_fk
            REFERENCES public.cie_o_morphology,
    cie_o_topography_id     bigint
        CONSTRAINT diagnosis_cie_o_topography_id_fk
            REFERENCES public.cie_o_topography,
    cie_o_tumor_location_id bigint
        CONSTRAINT diagnosis_cie_o_tumor_location_id_fk
            REFERENCES public.cie_o_tumor_location,
    date_create             timestamp(0) DEFAULT NOW() NOT NULL,
    user_create             varchar(30)  DEFAULT 'readiness'::character varying,
    date_modify             timestamp(0),
    user_modify             varchar(30)
);

-- PERMISOS
INSERT INTO public.permission (description)
VALUES
-- ('diagnosis_list'),
--        ('diagnosis_search'),
--        ('diagnosis_get'),
--        ('diagnosis_insert'),
--        ('diagnosis_update'),
--        ('diagnosis_delete')
('medicine_medical_consultation_list'),
('medicine_medical_consultation_search'),
('medicine_medical_consultation_get'),
('medicine_medical_consultation_insert'),
('medicine_medical_consultation_update'),
('medicine_medical_consultation_delete'),
('configuration_list'),
('configuration_search'),
('configuration_get'),
('configuration_insert'),
('configuration_update'),
('configuration_delete');

-- INSERCION
select * from role;
INSERT INTO role_permission (role_id, permission_id)
SELECT (SELECT id FROM role WHERE role.description = 'MEDICO'),
       p.id
FROM permission p
WHERE p.description IN ('diagnosis_list',
                        'diagnosis_search',
                        'diagnosis_get',
                        'diagnosis_insert',
                        'diagnosis_update',
                        'diagnosis_delete');

INSERT INTO role_permission (role_id, permission_id)
SELECT (SELECT id FROM role WHERE role.description = 'ENFERMERIA'),
       p.id
FROM permission p
WHERE p.description IN ('diagnosis_list',
                        'diagnosis_search',
                        'diagnosis_get',
                        'diagnosis_insert',
                        'diagnosis_update',
                        'diagnosis_delete');

INSERT INTO role_permission (role_id, permission_id)
SELECT (SELECT id FROM role WHERE role.description = 'INVENTARIO'),
       p.id
FROM permission p
WHERE p.description IN ('diagnosis_list',
                        'diagnosis_search',
                        'diagnosis_get');

INSERT INTO role_permission (role_id, permission_id)
SELECT (SELECT id FROM role WHERE role.description = 'AUDITOR'),
       p.id
FROM permission p
WHERE p.description IN ('diagnosis_list',
                        'diagnosis_search',
                        'diagnosis_get');

-- ALTER EN public.diagnosis_ap
ALTER TABLE public.diagnosis_ap
    ADD general_report text;

-- ALTER EN public.medical_consultation
alter table public.medical_consultation
    drop column medicine_presentation;

alter table public.medical_consultation
    drop column prescribed_medications;

-- CREATE TABLE public.medicine_medical_consultation
CREATE TABLE public.medicine_medical_consultation
(
    id                      bigserial PRIMARY KEY,
    medicine_id             bigint  NOT NULL
        CONSTRAINT medicine_medical_consultation_fk
            REFERENCES public.medicine,
    medical_consultation_id bigint  NOT NULL
        CONSTRAINT medicine_medical_consultation_fk_1
            REFERENCES public.medical_consultation,
    quantity                numeric NOT NULL,
    observation             text,
    dose                    numeric,
    presentation             text,
    concentration           text
);

-- ALTER EN public.medicine_treatment_plan
alter table public.medicine_treatment_plan
    add presentation text;

alter table public.medicine_treatment_plan
    add concentration text;

-- ALTER EN medicine_treatment_follow_up
alter table public.medicine_treatment_follow_up
    add presentation text;

alter table public.medicine_treatment_follow_up
    add concentration text;

-- CAMBIOS EN ESTADO DE PACIENTE
UPDATE public.parameter
SET value = 'EN TRATAMIENTO'
WHERE domain = 'PATIENT_STATE'
  AND value = 'INCLUIDO (En tratamiento)';

UPDATE public.parameter
SET code = 'TREATMENT'
WHERE domain = 'PATIENT_STATE'
  AND code = 'INC_TREATMENT';

UPDATE public.parameter
SET code = 'INCL'
WHERE domain = 'PATIENT_STATE'
  AND code = 'I';

UPDATE public.parameter
SET code = 'EXCL'
WHERE domain = 'PATIENT_STATE'
  AND code = 'E';

INSERT INTO public.parameter (domain, value, active, code)
VALUES ('PATIENT_STATE', 'SOSPECHOZO', TRUE, 'SOSP'),
       ('PATIENT_STATE', 'EVALUCIÓN', TRUE, 'EVAL'),
       ('PATIENT_STATE', 'FINALIZADO', TRUE, 'FIN'),
       ('PATIENT_STATE', 'FALLECIDO', TRUE, 'FALLEC');

-- SE CORRIGE ESTADOS EN PRODUCCIÓN
UPDATE public.patient
SET state_id = (SELECT id FROM  public.parameter WHERE value = 'SOSPECHOZO' AND domain = 'PATIENT_STATE')
WHERE id IN (SELECT id
             FROM public.patient
             WHERE state_id IN (SELECT id
                                FROM  public.parameter
                                WHERE domain = 'PATIENT_STATE'
                                  AND value IN
                                      ('NO APLICA',
                                       'EN ANATOMIA PATOLOGICA',
                                       'CANCER DE MAMA SIN IHQ CONFIRMADO',
                                       'INCLUIDO (nuevo)')));

-- SE ELIMINAN ESTADOS INNECESARIOS
DELETE
FROM public.parameter
WHERE ID IN (SELECT id
             FROM parameter
             WHERE domain = 'PATIENT_STATE'
               AND value IN
                   ('NO APLICA',
                    'EN ANATOMIA PATOLOGICA',
                    'CANCER DE MAMA SIN IHQ CONFIRMADO',
                    'INCLUIDO (nuevo)'));

--ALTER EN public.evaluation
alter table public.evaluation
    add approved bool;

--ALTER EN public.treatment_plan
alter table public.treatment_plan
    add active bool;

-- ALTER EN public.treatment_follow_up
alter table public.treatment_follow_up
    add treatment_plan_id bigint;

alter table public.treatment_follow_up
    add constraint treatment_follow_up_treatment_plan_id_fk
        foreign key (treatment_plan_id) references public.treatment_plan;

-- ALTER EN public.chemotherapy
alter table public.chemotherapy
    add treatment_plan_id bigint;

alter table public.chemotherapy
    add constraint chemotherapy_treatment_plan_id_fk
        foreign key (treatment_plan_id) references public.treatment_plan;


-- ALTER EN public.radiotherapy
alter table public.radiotherapy
    add treatment_plan_id bigint;

alter table public.radiotherapy
    add constraint radiotherapy_treatment_plan_id_fk
        foreign key (treatment_plan_id) references public.treatment_plan;


-- ALTER EN public.medical_document_type
alter table public.medical_document_type
    add orden integer;

UPDATE public.medical_document_type
SET orden = 1
WHERE description = 'INFORME ANATOMIA PATOLOGICA';

UPDATE public.medical_document_type
SET orden = 2
WHERE description = 'INFORME DE INMUNOHISTOQUÍMICA';

UPDATE public.medical_document_type
SET orden = 3
WHERE description = 'INFORME DE ESTADIFICACION DE  IMAGENOLOGIA';

UPDATE public.medical_document_type
SET orden = 4
WHERE description = 'ECOCARDIOGRAFIA';

UPDATE public.medical_document_type
SET orden = 5
WHERE description = 'FORMULARIO DE CRITERIOS DE INCLUSIÓN';

UPDATE public.medical_document_type
SET orden = 6
WHERE description = 'FORMULARIO DE CRITERIOS DE EXCLUSIÓN';

UPDATE public.medical_document_type
SET orden = 7
WHERE description = 'CONSENTIMIENTO INFORMADO DE TRATAMIENTO';

UPDATE public.medical_document_type
SET orden = 8
WHERE description = 'CONSENTIMIENTO DE USO DE DATOS';

-- ALTER EN public.patient
alter table public.patient
    add origin varchar(30);

alter table public.diagnosis_ap
    add origin varchar(30);
