-- INSERT IN PARAMETERS
INSERT INTO public.parameter (domain, value, active, code)
VALUES ('TREATMENT_PLAN_STATE', 'INACTIVO', TRUE, 'tret_pla_ina'),
       ('TREATMENT_PLAN_STATE', 'EN CURSO', TRUE, 'tret_pla_cur'),
       ('TREATMENT_PLAN_STATE', 'SUSPENDIDO', TRUE, 'tret_pla_sus'),
       ('TREATMENT_PLAN_STATE', 'CANCELADO', TRUE, 'tret_pla_can'),
       ('TREATMENT_PLAN_STATE', 'FINALIZADO', TRUE, 'tret_pla_fin');

-- -- alter in public.treatment_plan
-- ALTER TABLE public.treatment_plan
--     DROP COLUMN codification_type;
--
-- ALTER TABLE public.treatment_plan
--     DROP COLUMN active;

-- alter in audit.audit_treatment_plan
-- ALTER TABLE audit.audit_treatment_plan
--     DROP COLUMN codification_type;
--
-- ALTER TABLE audit.audit_treatment_plan
--     DROP COLUMN active;

-- alter table audit.audit_chemotherapy
--     drop column treatment_plan_id;

-- alter table audit.audit_radiotherapy
--     drop column treatment_plan_id;
--
-- alter table audit.audit_treatment_follow_up
--     drop column treatment_plan_id;


ALTER TABLE public.treatment_plan
    ADD number bigint;

ALTER TABLE public.treatment_plan
    ADD state_id bigint;

ALTER TABLE public.treatment_plan
    ADD CONSTRAINT treatment_plan_parameter_id_fk
        FOREIGN KEY (state_id) REFERENCES public.parameter;

--AJUSTE DE NUMERACION
WITH NumeracionPorPaciente AS (SELECT id,
                                      patient_id,
                                      number,
                                      ROW_NUMBER() OVER (PARTITION BY patient_id ORDER BY id) AS nueva_numeracion
                               FROM treatment_plan)

UPDATE treatment_plan
SET number = NumeracionPorPaciente.nueva_numeracion
FROM NumeracionPorPaciente
WHERE NumeracionPorPaciente.id = treatment_plan.id;

-- Ajustes desde prod
-- INSERT INTO public.periodicity (description, active)
-- VALUES ('CADA 21 DIAS', TRUE);
-- INSERT INTO public.periodicity (description, active)
-- VALUES ('SESION DE ATAQUE (1 VEZ)', TRUE);

-- Tablas intermedias para PLAN DE TRATAMIENTO
CREATE TABLE public.follow_up_treatment_plan
(
    id                bigserial PRIMARY KEY,
    follow_up_id      bigint NOT NULL
        CONSTRAINT follow_up_treatment_plan_fk
            REFERENCES public.treatment_follow_up,
    treatment_plan_id bigint NOT NULL
        CONSTRAINT follow_up_treatment_plan_fk_1
            REFERENCES public.treatment_plan
);

CREATE TABLE public.chemotherapy_treatment_plan
(
    id                bigserial PRIMARY KEY,
    chemotherapy_id   bigint NOT NULL
        CONSTRAINT chemotherapy_treatment_plan_fk
            REFERENCES public.chemotherapy,
    treatment_plan_id bigint NOT NULL
        CONSTRAINT chemotherapy_treatment_plan_fk_1
            REFERENCES public.treatment_plan
);

ALTER TABLE public.chemotherapy_treatment_plan
    ADD num_session integer;


CREATE TABLE public.radiotherapy_treatment_plan
(
    id                bigserial PRIMARY KEY,
    radiotherapy_id   bigint NOT NULL
        CONSTRAINT radiotherapy_treatment_plan_fk
            REFERENCES public.radiotherapy,
    treatment_plan_id bigint NOT NULL
        CONSTRAINT radiotherapy_treatment_plan_fk_1
            REFERENCES public.treatment_plan
);

ALTER TABLE public.radiotherapy_treatment_plan
    ADD num_session integer;

-- Insert permissions
INSERT INTO public.permission (description)
VALUES ('follow_up_treatment_plan_list'),
       ('follow_up_treatment_plan_search'),
       ('follow_up_treatment_plan_get'),
       ('follow_up_treatment_plan_insert'),
       ('follow_up_treatment_plan_update'),
       ('follow_up_treatment_plan_delete'),
       ('radiotherapy_treatment_plan_list'),
       ('radiotherapy_treatment_plan_search'),
       ('radiotherapy_treatment_plan_get'),
       ('radiotherapy_treatment_plan_insert'),
       ('radiotherapy_treatment_plan_update'),
       ('radiotherapy_treatment_plan_delete'),
       ('chemotherapy_treatment_plan_list'),
       ('chemotherapy_treatment_plan_search'),
       ('chemotherapy_treatment_plan_get'),
       ('chemotherapy_treatment_plan_insert'),
       ('chemotherapy_treatment_plan_update'),
       ('chemotherapy_treatment_plan_delete');
--
-- -- Ajustes de id de tablas intermedias
-- INSERT INTO follow_up_treatment_plan (follow_up_id, treatment_plan_id)
-- SELECT id, treatment_plan_id
-- FROM treatment_follow_up
-- WHERE treatment_plan_id IS NOT NULL;
--
-- INSERT INTO chemotherapy_treatment_plan (chemotherapy_id, treatment_plan_id)
-- SELECT id, treatment_plan_id
-- FROM chemotherapy
-- WHERE treatment_plan_id IS NOT NULL;
--
-- INSERT INTO radiotherapy_treatment_plan (radiotherapy_id, treatment_plan_id)
-- SELECT id, treatment_plan_id
-- FROM radiotherapy
-- WHERE treatment_plan_id IS NOT NULL;
--
-- -- Alter en public.chemotherapy
-- ALTER TABLE public.chemotherapy
--     DROP CONSTRAINT chemotherapy_treatment_plan_id_fk;
--
-- ALTER TABLE public.chemotherapy
--     DROP COLUMN treatment_plan_id;
--
-- -- Alter en  public.radiotherapy
-- ALTER TABLE public.radiotherapy
--     DROP CONSTRAINT radiotherapy_treatment_plan_id_fk;
--
-- ALTER TABLE public.radiotherapy
--     DROP COLUMN treatment_plan_id;
--
--
-- -- Alter en
-- ALTER TABLE public.treatment_follow_up
--     DROP CONSTRAINT treatment_follow_up_treatment_plan_id_fk;
--
-- ALTER TABLE public.treatment_follow_up
--     DROP COLUMN treatment_plan_id;

--Ajuste de numeracion de sesion de chemotherapy
WITH che_num AS (SELECT ch.nro_session, ctp.*
                 FROM chemotherapy ch
                          JOIN chemotherapy_treatment_plan ctp ON ch.id = ctp.chemotherapy_id
                 WHERE ch.nro_session IS NOT NULL)
UPDATE chemotherapy_treatment_plan
SET num_session = che_num.nro_session
FROM che_num
WHERE che_num.id = chemotherapy_treatment_plan.id;

--Ajuste de numeracion de sesion de radiotherapy
WITH rad_num AS (SELECT rad.nro_session, rtp.*
                 FROM radiotherapy rad
                          JOIN radiotherapy_treatment_plan rtp ON rad.id = rtp.radiotherapy_id
                 WHERE rad.nro_session IS NOT NULL)
UPDATE radiotherapy_treatment_plan
SET num_session = rad_num.nro_session
FROM rad_num
WHERE rad_num.id = radiotherapy_treatment_plan.id;

-- AUDITORIA
-- CREATE OR REPLACE FUNCTION public.audit_treatment_plan() RETURNS trigger
--     SECURITY DEFINER
--     LANGUAGE plpgsql
-- AS
-- $$
--  DECLARE
--  __DELETE char(6);
--  __INSERT char(6);
--  __UPDATE char(6);
--  BEGIN
-- 	__DELETE := 'DELETE';
-- 	__INSERT := 'INSERT';
-- 	__UPDATE := 'UPDATE';
--
-- 	if ( TG_OP = __DELETE  ) then
--  		INSERT INTO audit.audit_treatment_plan(
-- 		id,
-- 		patient_id,
-- 		hospital_id,
-- 		"date",
-- 		doctor_id ,
-- 		"size",
-- 		weight,
-- 		sc,
-- 		medical_visit_observation,
-- 		cie_10_code_id,
-- 		cie_o_morphology_id,
-- 		cie_o_topography_id,
-- 		cie_o_tumor_location_id,
-- 		type_id,
-- 		number_sessions,
-- 		periodicity_id,
-- 		date_first_cycle,
-- 		date_last_cycle,
-- 		observation,
-- 		origin,
-- 		date_create,
-- 		user_create,
-- 		date_modify,
-- 		user_modify,
-- 		audit_event,
-- 		audit_date_time ,
-- 		audit_user,
-- 		audit_client_ip
--  		)
--  		values (
-- 		old.id,
-- 		old.patient_id,
-- 		old.hospital_id,
-- 		old."date",
-- 		old.doctor_id ,
-- 		old."size",
-- 		old.weight,
-- 		old.sc,
-- 		old.medical_visit_observation,
-- 		old.cie_10_code_id,
-- 		old.cie_o_morphology_id,
-- 		old.cie_o_topography_id,
-- 		old.cie_o_tumor_location_id,
-- 		old.type_id,
-- 		old.number_sessions,
-- 		old.periodicity_id,
-- 		old.date_first_cycle,
-- 		old.date_last_cycle,
-- 		old.observation,
-- 		old.origin,
-- 		old.date_create,
-- 		old.user_create,
-- 		old.date_modify,
-- 		old.user_modify,
-- 		substr(TG_OP ,1,1),
--  		current_timestamp,
--  		session_user,
--  		inet_client_addr()
--  		);
-- 		return OLD;
--
-- 	else
--
--  		INSERT INTO audit.audit_treatment_plan(
-- 		id,
-- 		patient_id,
-- 		hospital_id,
-- 		"date",
-- 		doctor_id ,
-- 		"size",
-- 		weight,
-- 		sc,
-- 		medical_visit_observation,
-- 		cie_10_code_id,
-- 		cie_o_morphology_id,
-- 		cie_o_topography_id,
-- 		cie_o_tumor_location_id,
-- 		type_id,
-- 		number_sessions,
-- 		periodicity_id,
-- 		date_first_cycle,
-- 		date_last_cycle,
-- 		observation,
-- 		origin,
-- 		date_create,
-- 		user_create,
-- 		date_modify,
-- 		user_modify,
-- 		audit_event,
-- 		audit_date_time ,
-- 		audit_user,
-- 		audit_client_ip
--  		)
--  		values (
-- 		new.id,
-- 		new.patient_id,
-- 		new.hospital_id,
-- 		new."date",
-- 		new.doctor_id ,
-- 		new."size",
-- 		new.weight,
-- 		new.sc,
-- 		new.medical_visit_observation,
-- 		new.cie_10_code_id,
-- 		new.cie_o_morphology_id,
-- 		new.cie_o_topography_id,
-- 		new.cie_o_tumor_location_id,
-- 		new.type_id,
-- 		new.number_sessions,
-- 		new.periodicity_id,
-- 		new.date_first_cycle,
-- 		new.date_last_cycle,
-- 		new.observation,
-- 		new.origin,
-- 		new.date_create,
-- 		new.user_create,
-- 		new.date_modify,
-- 		new.user_modify,
-- 		substr(TG_OP ,1,1),
--  		current_timestamp,
--  		session_user,
--  		inet_client_addr()
--  		);
-- 		return NEW;
--
-- 	end if;
--  END
--  $$;

-- CREATE OR REPLACE FUNCTION public.audit_chemotherapy() RETURNS trigger
--     SECURITY DEFINER
--     LANGUAGE plpgsql
-- AS
-- $$
--  DECLARE
--  __DELETE char(6);
--  __INSERT char(6);
--  __UPDATE char(6);
--  BEGIN
-- 	__DELETE := 'DELETE';
-- 	__INSERT := 'INSERT';
-- 	__UPDATE := 'UPDATE';
--
-- 	if ( TG_OP = __DELETE  ) then
--  		INSERT INTO audit.audit_chemotherapy(
--  		id,
-- 		"date",
-- 		patient_id,
-- 		hospital_id,
-- 		date_create,
-- 		user_create,
-- 		date_modify,
-- 		user_modify,
-- 		nro_session,
-- 		request_state_id,
-- 		observation,
-- 		session_state_id,
-- 		doctor_id,
-- 		technician,
-- 		nurse,
-- 		audit_event,
-- 		audit_date_time ,
-- 		audit_user,
-- 		audit_client_ip
--  		)
--  		values (
--  		old.id,
-- 		old."date",
-- 		old.patient_id,
-- 		old.hospital_id,
-- 		old.date_create,
-- 		old.user_create,
-- 		old.date_modify,
-- 		old.user_modify,
-- 		old.nro_session,
-- 		old.request_state_id,
-- 		old.observation,
-- 		old.session_state_id,
-- 		old.doctor_id,
-- 		old.technician,
-- 		old.nurse,
-- 		substr(TG_OP ,1,1),
--  		current_timestamp,
--  		session_user,
--  		inet_client_addr()
--  		);
-- 		return OLD;
--
-- 	else
--
--  		INSERT INTO audit.audit_chemotherapy(
-- 		id,
-- 		"date",
-- 		patient_id,
-- 		hospital_id,
-- 		date_create,
-- 		user_create,
-- 		date_modify,
-- 		user_modify,
-- 		nro_session,
-- 		request_state_id,
-- 		observation,
-- 		session_state_id,
-- 		doctor_id,
-- 		technician,
-- 		nurse,
-- 		audit_event,
-- 		audit_date_time ,
-- 		audit_user,
-- 		audit_client_ip
--  		)
--  		values (
-- 		new.id,
-- 		new."date",
-- 		new.patient_id,
-- 		new.hospital_id,
-- 		new.date_create,
-- 		new.user_create,
-- 		new.date_modify,
-- 		new.user_modify,
-- 		new.nro_session,
-- 		new.request_state_id,
-- 		new.observation,
-- 		new.session_state_id,
-- 		new.doctor_id,
-- 		new.technician,
-- 		new.nurse,
-- 		substr(TG_OP ,1,1),
--  		current_timestamp,
--  		session_user,
--  		inet_client_addr()
--  		);
-- 		return NEW;
-- 	end if;
--  END
--  $$;

-- CREATE OR REPLACE FUNCTION public.audit_radiotherapy() RETURNS trigger
--     SECURITY DEFINER
--     LANGUAGE plpgsql
-- AS
-- $$
--  DECLARE
--  __DELETE char(6);
--  __INSERT char(6);
--  __UPDATE char(6);
--  BEGIN
-- 	__DELETE := 'DELETE';
-- 	__INSERT := 'INSERT';
-- 	__UPDATE := 'UPDATE';
--
-- 	if ( TG_OP = __DELETE  ) then
--  		INSERT INTO audit.audit_radiotherapy(
-- 		id,
-- 		"date",
-- 		patient_id,
-- 		hospital_id,
-- 		date_create,
-- 		user_create,
-- 		date_modify,
-- 		user_modify,
-- 		nro_session,
-- 		observation,
-- 		session_state_id,
-- 		doctor_id,
-- 		technician,
-- 		nurse,
-- 		audit_event,
-- 		audit_date_time ,
-- 		audit_user,
-- 		audit_client_ip
--  		)
--  		values (
-- 		old.id,
-- 		old."date",
-- 		old.patient_id,
-- 		old.hospital_id,
-- 		old.date_create,
-- 		old.user_create,
-- 		old.date_modify,
-- 		old.user_modify,
-- 		old.nro_session,
-- 		old.observation,
-- 		old.session_state_id,
-- 		old.doctor_id,
-- 		old.technician,
-- 		old.nurse,
-- 		substr(TG_OP ,1,1),
--  		current_timestamp,
--  		session_user,
--  		inet_client_addr()
--  		);
-- 		return OLD;
--
-- 	else
--
--  		INSERT INTO audit.audit_radiotherapy(
-- 		id,
-- 		"date",
-- 		patient_id,
-- 		hospital_id,
-- 		date_create,
-- 		user_create,
-- 		date_modify,
-- 		user_modify,
-- 		nro_session,
-- 		observation,
-- 		session_state_id,
-- 		doctor_id,
-- 		technician,
-- 		nurse,
-- 		audit_event,
-- 		audit_date_time ,
-- 		audit_user,
-- 		audit_client_ip
--  		)
--  		values (
-- 		new.id,
-- 		new."date",
-- 		new.patient_id,
-- 		new.hospital_id,
-- 		new.date_create,
-- 		new.user_create,
-- 		new.date_modify,
-- 		new.user_modify,
-- 		new.nro_session,
-- 		new.observation,
-- 		new.session_state_id,
-- 		new.doctor_id,
-- 		new.technician,
-- 		new.nurse,
-- 		substr(TG_OP ,1,1),
--  		current_timestamp,
--  		session_user,
--  		inet_client_addr()
--  		);
-- 		return NEW;
--
-- 	end if;
--  END
--  $$;

-- CREATE OR REPLACE FUNCTION public.audit_treatment_follow_up() RETURNS trigger
--     SECURITY DEFINER
--     LANGUAGE plpgsql
-- AS
-- $$
--  DECLARE
--  __DELETE char(6);
--  __INSERT char(6);
--  __UPDATE char(6);
--  BEGIN
-- 	__DELETE := 'DELETE';
-- 	__INSERT := 'INSERT';
-- 	__UPDATE := 'UPDATE';
--
-- 	if ( TG_OP = __DELETE  ) then
--  		INSERT INTO audit.audit_treatment_follow_up(
-- 		id,
-- 		follow_up_date,
-- 		last_cancer_control_date,
-- 		type_treatment,
-- 		breast,
-- 		armpit,
-- 		suspension_treatment,
-- 		suspension_treatment_reason,
-- 		suspension_treatment_custom_reason,
-- 		congestive_heart_failure,
-- 		fevi_follow_up_date,
-- 		fevi_value,
-- 		fevi_trastuzumab_dose,
-- 		other_severe_adverse_events,
-- 		other_severe_adverse_events_detail,
-- 		other_complementary_studies,
-- 		dose_adjustment,
-- 		dose_adjustment_reason,
-- 		every_three_weeks,
-- 		weekly,
-- 		comentaries,
-- 		date_create,
-- 		user_create,
-- 		date_modify,
-- 		user_modify,
-- 		patient_id,
-- 		hospital_id,
-- 		doctor_id ,
-- 		audit_event,
-- 		audit_date_time ,
-- 		audit_user,
-- 		audit_client_ip
--  		)
--  		values (
-- 		old.id,
-- 		old.follow_up_date,
-- 		old.last_cancer_control_date,
-- 		old.type_treatment,
-- 		old.breast,
-- 		old.armpit,
-- 		old.suspension_treatment,
-- 		old.suspension_treatment_reason,
-- 		old.suspension_treatment_custom_reason,
-- 		old.congestive_heart_failure,
-- 		old.fevi_follow_up_date,
-- 		old.fevi_value,
-- 		old.fevi_trastuzumab_dose,
-- 		old.other_severe_adverse_events,
-- 		old.other_severe_adverse_events_detail,
-- 		old.other_complementary_studies,
-- 		old.dose_adjustment,
-- 		old.dose_adjustment_reason,
-- 		old.every_three_weeks,
-- 		old.weekly,
-- 		old.comentaries,
-- 		old.date_create,
-- 		old.user_create,
-- 		old.date_modify,
-- 		old.user_modify,
-- 		old.patient_id,
-- 		old.hospital_id,
-- 		old.doctor_id ,
-- 		substr(TG_OP ,1,1),
--  		current_timestamp,
--  		session_user,
--  		inet_client_addr()
--  		);
-- 		return OLD;
--
-- 	else
--
--  		INSERT INTO audit.audit_treatment_follow_up(
-- 		id,
-- 		follow_up_date,
-- 		last_cancer_control_date,
-- 		type_treatment,
-- 		breast,
-- 		armpit,
-- 		suspension_treatment,
-- 		suspension_treatment_reason,
-- 		suspension_treatment_custom_reason,
-- 		congestive_heart_failure,
-- 		fevi_follow_up_date,
-- 		fevi_value,
-- 		fevi_trastuzumab_dose,
-- 		other_severe_adverse_events,
-- 		other_severe_adverse_events_detail,
-- 		other_complementary_studies,
-- 		dose_adjustment,
-- 		dose_adjustment_reason,
-- 		every_three_weeks,
-- 		weekly,
-- 		comentaries,
-- 		date_create,
-- 		user_create,
-- 		date_modify,
-- 		user_modify,
-- 		patient_id,
-- 		hospital_id,
-- 		doctor_id ,
-- 		audit_event,
-- 		audit_date_time ,
-- 		audit_user,
-- 		audit_client_ip
--  		)
--  		values (
-- 		new.id,
-- 		new.follow_up_date,
-- 		new.last_cancer_control_date,
-- 		new.type_treatment,
-- 		new.breast,
-- 		new.armpit,
-- 		new.suspension_treatment,
-- 		new.suspension_treatment_reason,
-- 		new.suspension_treatment_custom_reason,
-- 		new.congestive_heart_failure,
-- 		new.fevi_follow_up_date,
-- 		new.fevi_value,
-- 		new.fevi_trastuzumab_dose,
-- 		new.other_severe_adverse_events,
-- 		new.other_severe_adverse_events_detail,
-- 		new.other_complementary_studies,
-- 		new.dose_adjustment,
-- 		new.dose_adjustment_reason,
-- 		new.every_three_weeks,
-- 		new.weekly,
-- 		new.comentaries,
-- 		new.date_create,
-- 		new.user_create,
-- 		new.date_modify,
-- 		new.user_modify,
-- 		new.patient_id,
-- 		new.hospital_id,
-- 		new.doctor_id ,
-- 		substr(TG_OP ,1,1),
--  		current_timestamp,
--  		session_user,
--  		inet_client_addr()
--  		);
-- 		return NEW;
--
-- 	end if;
--  END
--  $$;

-- TABLA INTERMEDIA ENTRE PACIENTE Y HOSPITAL
CREATE TABLE public.patient_hospital
(
    id          bigserial
        CONSTRAINT patient_hospital_pk
            PRIMARY KEY,
    patient_id  bigint
        CONSTRAINT patient_hospital_patient_id_fk
            REFERENCES public.patient,
    hospital_id bigint
        CONSTRAINT patient_hospital_hospital_id_fk
            REFERENCES public.hospital
);

-- POBLACION DE TABLA patient_hospital
INSERT INTO patient_hospital (patient_id, hospital_id)
SELECT id, hospital_id
FROM patient;

-- INSERCION DE PERMISOS
INSERT INTO public.permission (description)
VALUES ('patient_hospital_list'),
       ('patient_hospital_search'),
       ('patient_hospital_get'),
       ('patient_hospital_insert'),
       ('patient_hospital_update'),
       ('patient_hospital_delete');

-- Cambios en public.medical_document
alter table public.medical_document
    add hospital_id bigint;

alter table public.medical_document
    add constraint medical_document_hospital_id_fk
        foreign key (hospital_id) references public.hospital;

-- Cambios en public.patient_inclusion_criteria
alter table public.patient_inclusion_criteria
    add hospital_id bigint;

alter table public.patient_inclusion_criteria
    add constraint patient_inclusion_criteria_hospital_id_fk
        foreign key (hospital_id) references public.hospital;

-- Cambios en public.patient_exclusion_criteria
alter table public.patient_exclusion_criteria
    add hospital_id bigint;

alter table public.patient_exclusion_criteria
    add constraint patient_exclusion_criteria_hospital_id_fk
        foreign key (hospital_id) references public.hospital;

-- Cambios en public.diagnosis
alter table public.diagnosis
    add hospital_id bigint;

alter table public.diagnosis
    add constraint diagnosis_hospital_id_fk
        foreign key (hospital_id) references public.hospital;

-- Cambios en public.personal_pathological_history
alter table public.personal_pathological_history
    add hospital_id bigint;

alter table public.personal_pathological_history
    add constraint personal_pathological_history_hospital_id_fk
        foreign key (hospital_id) references public.hospital;

-- Cambios en public.medical_consultation
alter table public.medical_consultation
    add hospital_id bigint;

alter table public.medical_consultation
    add constraint medical_consultation_hospital_id_fk
        foreign key (hospital_id) references public.hospital;


-- CREATE TABLE public.medicine_chemotherapy
CREATE TABLE public.medicine_chemotherapy
(
    id              bigserial PRIMARY KEY,
    medicine_id     bigint  NOT NULL
        CONSTRAINT medicine_chemotherapy_fk
            REFERENCES public.medicine,
    chemotherapy_id bigint  NOT NULL
        CONSTRAINT medicine_chemotherapy_fk_1
            REFERENCES public.chemotherapy,
    quantity        numeric NOT NULL,
    observation     text,
    dose            numeric,
    presentation    text,
    concentration   text
);

-- Insert permissions
INSERT INTO public.permission (description)
VALUES ('medicine_chemotherapy_list'),
       ('medicine_chemotherapy_search'),
       ('medicine_chemotherapy_get'),
       ('medicine_chemotherapy_insert'),
       ('medicine_chemotherapy_update'),
       ('medicine_chemotherapy_delete');