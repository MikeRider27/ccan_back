-- CREATE TABLE public.treatment_plan
CREATE TABLE public.treatment_plan
(
    -- Datos Generales
    id                        bigserial PRIMARY KEY,
    patient_id                bigint REFERENCES public.patient (id)               NOT NULL,
    hospital_id               bigint REFERENCES public.hospital (id)              NOT NULL,
    date                      timestamp(0)                                        NOT NULL,
    historical                boolean      DEFAULT FALSE                          NOT NULL,
    -- Consulta
    doctor_id                 bigint REFERENCES public.doctor (id)                NOT NULL,
    size                      numeric,
    weight                    numeric,
    sc                        numeric,
    medical_visit_observation text,
    -- Diagnostico Medico
    codification_type         varchar(10),
    confirmed                 boolean,
    cie_10_code_id            bigint REFERENCES public.cie_10 (id),
    cie_o_morphology_id       bigint REFERENCES public.cie_o_morphology (id),
    cie_o_topography_id       bigint REFERENCES public.cie_o_topography (id),
    cie_o_tumor_location_id   bigint REFERENCES public.cie_o_tumor_location (id),
    -- Plan de tratamiento
    type_id                   bigint REFERENCES public.type_treatment (id)        NOT NULL,
    number_sessions           integer                                             NOT NULL,
    periodicity_id            bigint REFERENCES public.periodicity (id)           NOT NULL,
    date_first_cycle          date,
    date_last_cycle           date,
    observation               text,
    -- Auditoria
    origin                    varchar      DEFAULT 'readiness'::character varying NOT NULL,
    date_create               timestamp(0) DEFAULT NOW()                          NOT NULL,
    user_create               varchar(30)                                         NOT NULL,
    date_modify               timestamp(0),
    user_modify               varchar(30)
);

-- PERMISOS
INSERT INTO public.permission (description)
VALUES ('treatment_plan_list'),
       ('treatment_plan_search'),
       ('treatment_plan_get'),
       ('treatment_plan_insert'),
       ('treatment_plan_update'),
       ('treatment_plan_delete');

INSERT INTO role_permission (role_id, permission_id)
SELECT (SELECT id FROM role WHERE description = 'MEDICO'),
       id
FROM permission
WHERE description IN ('treatment_plan_list', 'treatment_plan_search',
                      'treatment_plan_get', 'treatment_plan_insert', 'treatment_plan_update',
                      'treatment_plan_delete');

INSERT INTO role_permission (role_id, permission_id)
SELECT (SELECT id FROM role WHERE description = 'ADMINISTRADOR'),
       id
FROM permission
WHERE description IN ('treatment_plan_list', 'treatment_plan_search',
                      'treatment_plan_get', 'treatment_plan_insert', 'treatment_plan_update',
                      'treatment_plan_delete');

INSERT INTO role_permission (role_id, permission_id)
SELECT (SELECT id FROM role WHERE description = 'AUDITOR'),
       id
FROM permission
WHERE description IN ('treatment_plan_list', 'treatment_plan_search',
                      'treatment_plan_get');

-- ALTER TABLE (public.medicine_treatment_order --> public.medicine_treatment_plan)
ALTER TABLE public.medicine_treatment_order
    RENAME COLUMN treatment_order_id TO treatment_plan_id;

ALTER TABLE public.medicine_treatment_order
    RENAME CONSTRAINT medicine_treatment_order_pk TO medicine_treatment_plan_pk;

ALTER TABLE public.medicine_treatment_order
    DROP CONSTRAINT medicine_treatment_order_fk_1;

ALTER TABLE public.medicine_treatment_order
    RENAME TO medicine_treatment_plan;

--- BORRAR LOS DATOS DE public.medicine_treatment_plan
ALTER TABLE public.medicine_treatment_plan
    ADD CONSTRAINT medicine_treatment_plan_fk_1
        FOREIGN KEY (treatment_plan_id) REFERENCES public.treatment_plan;
----
ALTER TABLE public.medicine_treatment_plan
    ADD treatment_program boolean;

-- ALTER PERMISOS
UPDATE public.permission
SET description = 'medicine_treatment_plan_get'
WHERE description = 'medicine_treatment_order_get';

UPDATE public.permission
SET description = 'medicine_treatment_plan_update'
WHERE description = 'medicine_treatment_order_update';

UPDATE public.permission
SET description = 'medicine_treatment_plan_delete'
WHERE description = 'medicine_treatment_order_delete';

UPDATE public.permission
SET description = 'medicine_treatment_plan_list'
WHERE description = 'medicine_treatment_order_list';

UPDATE public.permission
SET description = 'medicine_treatment_plan_insert'
WHERE description = 'medicine_treatment_order_insert';

UPDATE public.permission
SET description = 'medicine_treatment_plan_search'
WHERE description = 'medicine_treatment_order_search';

-- ALTER public.medical_document
ALTER TABLE public.medical_document
    ADD tab_origin varchar(255);

COMMENT ON COLUMN public.medical_document.tab_origin IS 'Origen de la pestaña al cual pertenece el documento';

ALTER TABLE public.medical_document
    ADD study_date timestamp(0);

-- CAMBIOS EN PARAMETROS
DELETE
FROM public.parameter
WHERE domain = 'PATIENT_STATE'
  AND value = 'CANCER DE MAMA HER2';
DELETE
FROM public.parameter
WHERE domain = 'PATIENT_STATE'
  AND value = 'CANCER DE MAMA NO HER2';
DELETE
FROM public.parameter
WHERE domain = 'PATIENT_STATE'
  AND value = 'HIS';
DELETE
FROM public.parameter
WHERE domain = 'PATIENT_STATE'
  AND value = 'FALLECIDO';
DELETE
FROM public.parameter
WHERE domain = 'PATIENT_STATE'
  AND value = 'SOSPECHOSO';

INSERT INTO public.parameter (domain, value, active, code)
VALUES ('PATIENT_STATE', 'INCLUIDO (nuevo)', TRUE, 'INC_NEW'),
       ('PATIENT_STATE', 'INCLUIDO (En tratamiento)', TRUE, 'INC_TREATMENT');

-- AJUSTE DE ESTADOS
UPDATE public.patient
SET state_id = (SELECT id FROM public.parameter WHERE value = 'INCLUIDO')
WHERE TRUE;

-- SE ELIMINA EL CAMPO public.patient.photo
alter table public.patient
    drop column photo;

-- SE CAMBIA VALOR DE PARAMETRO DIFUNTO --> FALLECIDO
UPDATE public.parameter
SET value = 'FALLECIDO',
    code  = 'F'
WHERE domain = 'PATIENT_VITAL_STATE'
  AND value = 'DIFUNTO';

-- SE AGREGA VALOR FALTANTE
ALTER TABLE public.patient_inclusion_criteria_neoadjuvant_trastuzumab
    ADD determination_hormone_receptors boolean;
