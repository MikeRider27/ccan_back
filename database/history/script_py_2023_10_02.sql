------------------------------------
-- CREATE TABLE public.evaluation --
------------------------------------
CREATE TABLE public.evaluation
(
    id          bigserial
        CONSTRAINT evaluation_pk
            PRIMARY KEY,
    patient_id  bigint
        CONSTRAINT evaluation_patient_id_fk
            REFERENCES public.patient,
    date_start  timestamp(0),
    date_end    timestamp(0),
    observation text,
    date_create timestamp(0) DEFAULT NOW() NOT NULL,
    user_create varchar(30)  DEFAULT 'readiness'::character varying,
    date_modify timestamp(0),
    user_modify varchar(30)
);

------------------------------------
-- CREATE TABLE public.evaluators --
------------------------------------
CREATE TABLE public.evaluators
(
    id            bigserial
        CONSTRAINT evaluators_pk
            PRIMARY KEY,
    evaluation_id bigint    NOT NULL
        CONSTRAINT evaluators_evaluation_id_fk
            REFERENCES public.evaluation,
    evaluator_id  bigserial NOT NULL
        CONSTRAINT evaluators_user_id_fk
            REFERENCES public."user",
    CONSTRAINT evaluators_pk2
        UNIQUE (evaluation_id, evaluator_id)
);

------------------------
-- INSERT PERMISSIONS --
------------------------

INSERT INTO permission (description)
VALUES ('evaluation_list'),
       ('evaluation_search'),
       ('evaluation_get'),
       ('evaluation_insert'),
       ('evaluation_update'),
       ('evaluation_delete'),
       ('patient_family_with_cancer_list'),
       ('patient_family_with_cancer_search'),
       ('patient_family_with_cancer_get'),
       ('patient_family_with_cancer_insert'),
       ('patient_family_with_cancer_update'),
       ('patient_family_with_cancer_delete'),
       ('personal_pathological_history_list'),
       ('personal_pathological_history_search'),
       ('personal_pathological_history_get'),
       ('personal_pathological_history_insert'),
       ('personal_pathological_history_update'),
       ('personal_pathological_history_delete'),
       ('evaluators_list'),
       ('evaluators_search'),
       ('evaluators_get'),
       ('evaluators_insert'),
       ('evaluators_update'),
       ('evaluators_delete');

--AUDITOR
INSERT INTO role_permission (role_id, permission_id)
SELECT (SELECT id FROM role WHERE description = 'AUDITOR'),
       id
FROM permission
WHERE description IN ('evaluation_list',
                      'evaluation_search',
                      'evaluation_get',
                      'patient_family_with_cancer_list',
                      'patient_family_with_cancer_search',
                      'patient_family_with_cancer_get',
                      'personal_pathological_history_list',
                      'personal_pathological_history_search',
                      'personal_pathological_history_get',
                      'evaluators_list',
                      'evaluators_search',
                      'evaluators_get');

--MEDICO
INSERT INTO role_permission (role_id, permission_id)
SELECT (SELECT id FROM role WHERE description = 'MEDICO'),
       id
FROM permission
WHERE description IN ('evaluation_list',
                      'evaluation_search',
                      'evaluation_get',
                      'evaluation_insert',
                      'evaluation_update',
                      'evaluation_delete',
                      'patient_family_with_cancer_list',
                      'patient_family_with_cancer_search',
                      'patient_family_with_cancer_get',
                      'patient_family_with_cancer_insert',
                      'patient_family_with_cancer_update',
                      'patient_family_with_cancer_delete',
                      'personal_pathological_history_list',
                      'personal_pathological_history_search',
                      'personal_pathological_history_get',
                      'personal_pathological_history_insert',
                      'personal_pathological_history_update',
                      'personal_pathological_history_delete',
                      'evaluators_list',
                      'evaluators_search',
                      'evaluators_get',
                      'evaluators_insert',
                      'evaluators_update',
                      'evaluators_delete');

-- ENFERMERIA
INSERT INTO role_permission (role_id, permission_id)
SELECT (SELECT id FROM role WHERE description = 'ENFERMERIA'),
       id
FROM permission
WHERE description IN ('evaluation_list',
                      'evaluation_search',
                      'evaluation_get',
                      'evaluation_insert',
                      'evaluation_update',
                      'evaluation_delete',
                      'patient_family_with_cancer_list',
                      'patient_family_with_cancer_search',
                      'patient_family_with_cancer_get',
                      'patient_family_with_cancer_insert',
                      'patient_family_with_cancer_update',
                      'patient_family_with_cancer_delete',
                      'personal_pathological_history_list',
                      'personal_pathological_history_search',
                      'personal_pathological_history_get',
                      'personal_pathological_history_insert',
                      'personal_pathological_history_update',
                      'personal_pathological_history_delete',
                      'evaluators_list',
                      'evaluators_search',
                      'evaluators_get',
                      'evaluators_insert',
                      'evaluators_update',
                      'evaluators_delete');

-- ADMINISTRADOR
INSERT INTO role_permission (role_id, permission_id)
SELECT (SELECT id FROM role WHERE description = 'ADMINISTRADOR'),
       id
FROM permission
WHERE description IN ('evaluation_list',
                      'evaluation_search',
                      'evaluation_get',
                      'evaluation_insert',
                      'evaluation_update',
                      'evaluation_delete',
                      'patient_family_with_cancer_list',
                      'patient_family_with_cancer_search',
                      'patient_family_with_cancer_get',
                      'patient_family_with_cancer_insert',
                      'patient_family_with_cancer_update',
                      'patient_family_with_cancer_delete',
                      'personal_pathological_history_list',
                      'personal_pathological_history_search',
                      'personal_pathological_history_get',
                      'personal_pathological_history_insert',
                      'personal_pathological_history_update',
                      'personal_pathological_history_delete',
                      'evaluators_list',
                      'evaluators_search',
                      'evaluators_get',
                      'evaluators_insert',
                      'evaluators_update',
                      'evaluators_delete');

-- INVENTARIO
INSERT INTO role_permission (role_id, permission_id)
SELECT (SELECT id FROM role WHERE description = 'INVENTARIO'),
       id
FROM permission
WHERE description IN ('evaluation_list',
                      'evaluation_search',
                      'evaluation_get',
                      'evaluation_insert',
                      'evaluation_update',
                      'evaluation_delete',
                      'patient_family_with_cancer_list',
                      'patient_family_with_cancer_search',
                      'patient_family_with_cancer_get',
                      'patient_family_with_cancer_insert',
                      'patient_family_with_cancer_update',
                      'patient_family_with_cancer_delete',
                      'personal_pathological_history_list',
                      'personal_pathological_history_search',
                      'personal_pathological_history_get',
                      'personal_pathological_history_insert',
                      'personal_pathological_history_update',
                      'personal_pathological_history_delete',
                      'evaluators_list',
                      'evaluators_search',
                      'evaluators_get',
                      'evaluators_insert',
                      'evaluators_update',
                      'evaluators_delete');
---------------------------