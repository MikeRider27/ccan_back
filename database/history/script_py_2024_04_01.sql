-- ALTER IN inventory.history
ALTER TABLE inventory.history
    ADD dest_deposit_stock_id bigint;

ALTER TABLE inventory.history
    ADD CONSTRAINT depo
        FOREIGN KEY (dest_deposit_stock_id) REFERENCES inventory.deposit_stock;

ALTER TABLE inventory.history
    RENAME COLUMN deposit_stock_id TO orig_deposit_stock_id;

-- ADD PARAMETER
INSERT INTO public.parameter (domain, value, active, code)
VALUES ('DEPOSIT_STOCK_TYPE', 'HOSPITAL DISTRITAL', TRUE, 'HOSP_DIST'),
       ('DEPOSIT_STOCK_TYPE', 'DEPOSITO DEL NIVEL CENTRAL', TRUE, 'DEP_NIV_CENT'),
       ('DEPOSIT_STOCK_TYPE', 'FARMACIA', TRUE, 'FARM'),
       ('DEPOSIT_STOCK_TYPE', 'HOSPITAL ESPECIALIZADO', TRUE, 'HOPS_ESPEC');

-- ALTER IN inventory.deposit
ALTER TABLE inventory.deposit
    ADD type_id bigint;

ALTER TABLE inventory.deposit
    ADD CONSTRAINT deposit_parameter_id_fk
        FOREIGN KEY (type_id) REFERENCES public.parameter;

-- ALTER IN inventory.history
ALTER TABLE inventory.history
    ADD origin varchar(30);

ALTER TABLE inventory.history
    ADD date timestamp;

ALTER TABLE inventory.history
    ADD observation text;

ALTER TABLE inventory.history
    ADD balance double precision;

ALTER TABLE inventory.history
    ADD original_quantity double precision;

-- ADD NEW PARAMETERS
INSERT INTO public.parameter (domain, value, active, code)
VALUES ('STOCK_HISTORY_EVENT', 'Sync with SICIAP', TRUE, 'SYNC_SICIAP');

-- ADD NEW CONFIG
INSERT INTO public.configuration (name, value, code)
VALUES ('SCHEDULED_TASKS_TIME', '03:00', 'STT');

--ALTER IN public.medical_document_type
ALTER TABLE public.medical_document_type
    ADD code varchar(20);

-- DELETE FROM public.medical_document_type
DELETE
FROM public.medical_document_type
WHERE description = 'INITIAL_PATIENT_DOCUMENTS';

-- UPDATE in public.medical_document_type
UPDATE public.medical_document_type
SET code = 'CONSENT'
WHERE description = 'CONSENTIMIENTO INFORMADO DE TRATAMIENTO';
UPDATE public.medical_document_type
SET code = 'PATHO_ANAT'
WHERE description = 'INFORME ANATOMIA PATOLOGICA';
UPDATE public.medical_document_type
SET code = 'OTHER'
WHERE description = 'OTROS';
UPDATE public.medical_document_type
SET code = 'IM_HIST_CHEM'
WHERE description = 'INFORME DE INMUNOHISTOQUÍMICA';
UPDATE public.medical_document_type
SET code = 'IMAG_STAG '
WHERE description = 'INFORME DE ESTADIFICACION DE  IMAGENOLOGIA';
UPDATE public.medical_document_type
SET code = 'ECHOCARD'
WHERE description = 'ECOCARDIOGRAFIA';
UPDATE public.medical_document_type
SET code = 'INCL_EXCL_FORM'
WHERE description = 'FORMULARIO DE INCLUSION Y EXCLUSION';
UPDATE public.medical_document_type
SET code = 'CONSENT_DATA'
WHERE description = 'CONSENTIMIENTO DE USO DE DATOS';
UPDATE public.medical_document_type
SET code = 'INCL_FORM'
WHERE description = 'FORMULARIO DE CRITERIOS DE INCLUSIÓN';
UPDATE public.medical_document_type
SET code = 'EXCL_FORM'
WHERE description = 'FORMULARIO DE CRITERIOS DE EXCLUSIÓN';
UPDATE public.medical_document_type
SET code = 'INIT_DOSE'
WHERE description = 'FORMULARIO DE DOSIS INICIAL O EL QUE CORRESPONDA';
UPDATE public.medical_document_type
SET code = 'MAMMOGRAP'
WHERE description = 'MAMOGRAFÍA';
UPDATE public.medical_document_type
SET code = 'BREAST_ULTRASON'
WHERE description = 'ECOGRAFÍA MAMARIA';

-- ALTER IN public.document_type
ALTER TABLE public.document_type
    ADD code varchar(20);

UPDATE public.document_type
SET code = 'PROV'
WHERE description = 'PROVISORIO';

UPDATE public.document_type
SET code = 'CI'
WHERE description = 'CEDULA DE IDENTIDAD';

UPDATE public.document_type
SET code = 'PASS'
WHERE description = 'PASAPORTE';


--ALTER IN public.medical_consultation
ALTER TABLE public.medical_consultation
    ADD origin varchar(30);

--ALTER IN public.specialty
ALTER TABLE public.specialty
    ADD origin varchar(30);

--ALTER IN public.doctor
ALTER TABLE public.doctor
    ADD origin varchar(30);

-- PERMISSIONS
UPDATE public.permission
SET description = 'menu_dashboard'
WHERE description = 'general';

UPDATE public.permission
SET description = 'medical_document_type_search'
WHERE description = 'medical_document_tyep_search';

INSERT INTO public.permission (description)
VALUES ('menu_interoperability');

-- ASSIGN PERMISSION TO ROLES
INSERT INTO role_permission (role_id, permission_id)
SELECT (SELECT id FROM role WHERE description = 'AUDITOR'),
       id
FROM permission
WHERE description IN ('menu_configuration', 'menu_interoperability', 'menu_dashboard');

INSERT INTO role_permission (role_id, permission_id)
SELECT (SELECT id FROM role WHERE description = 'INVENTARIO'),
       id
FROM permission
WHERE description IN ('menu_configuration', 'menu_interoperability', 'menu_dashboard');

INSERT INTO role_permission (role_id, permission_id)
SELECT (SELECT id FROM role WHERE description = 'EVALUADOR'),
       id
FROM permission
WHERE description IN ('menu_dashboard');

INSERT INTO role_permission (role_id, permission_id)
SELECT (SELECT id FROM role WHERE description = 'MEDICO'),
       id
FROM permission
WHERE description IN ('menu_dashboard');

INSERT INTO role_permission (role_id, permission_id)
SELECT (SELECT id FROM role WHERE description = 'ENFERMERIA'),
       id
FROM permission
WHERE description IN ('menu_dashboard');

-- SELECT role_id, permission_id, COUNT(*) AS count_rows
-- FROM public.role_permission
-- GROUP BY role_id, permission_id
-- HAVING COUNT(*) > 1;

-- DELETE DUPLICATED PERMISSIONS
WITH duplicates AS (SELECT role_id,
                           permission_id,
                           ROW_NUMBER()
                           OVER (PARTITION BY role_id, permission_id ORDER BY role_id, permission_id) AS row_num
                    FROM public.role_permission)
DELETE
FROM public.role_permission
WHERE (role_id, permission_id) IN (SELECT role_id, permission_id
                                   FROM duplicates
                                   WHERE row_num > 1);

-- ADD UNIQUE CONSTRAINT
ALTER TABLE public.role_permission
    ADD CONSTRAINT role_permission_pk
        UNIQUE (role_id, permission_id);

-- DELETE OLD PERMISSIONS
DELETE
FROM role_permission
WHERE id IN (SELECT rp.id
             FROM role_permission rp
                      JOIN permission p ON p.id = rp.permission_id
             WHERE p.id IN (SELECT id
                            FROM public.permission
                            WHERE description ILIKE '%additional_%'));

DELETE
FROM public.permission
WHERE description ILIKE '%additional_%';

-- ALTER IN public.hospital
ALTER TABLE public.hospital
    ADD system boolean DEFAULT TRUE;


-----------
-- AUDIT --
-----------

--ALTER IN public.medical_document_type
ALTER TABLE audit.audit_medical_document_type
    ADD code varchar(20);


CREATE OR REPLACE FUNCTION public.audit_medical_document_type()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE NOT LEAKPROOF SECURITY DEFINER
AS $BODY$

 DECLARE
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';

	if ( TG_OP = __DELETE  ) then
 		INSERT INTO audit.audit_medical_document_type(
		id,
		description,
		orden,
        code,
		audit_event,
		audit_date_time ,
		audit_user,
		audit_client_ip
 		)
 		values (
		old.id,
		old.description,
		old.orden,
        old.code,
		substr(TG_OP ,1,1),
 		current_timestamp,
 		session_user,
 		inet_client_addr()
 		);
		return OLD;

	else

 		INSERT INTO audit.audit_medical_document_type(
		id,
		description,
		orden,
        code,
		audit_event,
		audit_date_time ,
		audit_user,
		audit_client_ip
 		)
 		values (
		new.id,
		new.description,
		new.orden,
        new.code,
		substr(TG_OP ,1,1),
 		current_timestamp,
 		session_user,
 		inet_client_addr()
 		);
		return NEW;

	end if;
 END

$BODY$;


-- ALTER IN public.document_type
ALTER TABLE audit.audit_document_type
    ADD code varchar(20);


CREATE OR REPLACE FUNCTION public.audit_document_type()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE NOT LEAKPROOF SECURITY DEFINER
AS $BODY$

 DECLARE
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';

	if ( TG_OP = __DELETE  ) then
 		INSERT INTO audit.audit_document_type(
		id,
		description,
        code,
		audit_event,
		audit_date_time ,
		audit_user,
		audit_client_ip
 		)
 		values (
		old.id,
		old.description,
        old.code,
		substr(TG_OP ,1,1),
 		current_timestamp,
 		session_user,
 		inet_client_addr()
 		);
		return OLD;

	else

 		INSERT INTO audit.audit_document_type(
		id,
		description,
        code,
		audit_event,
		audit_date_time ,
		audit_user,
		audit_client_ip
 		)
 		values (
		new.id,
		new.description,
        new.code,
		substr(TG_OP ,1,1),
 		current_timestamp,
 		session_user,
 		inet_client_addr()
 		);
		return NEW;
	end if;
 END

$BODY$;


--ALTER IN public.medical_consultation
ALTER TABLE audit.audit_medical_consultation
    ADD origin varchar(30);


CREATE OR REPLACE FUNCTION public.audit_medical_consultation()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE NOT LEAKPROOF SECURITY DEFINER
AS $BODY$

 DECLARE
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';

	if ( TG_OP = __DELETE  ) then
 		INSERT INTO audit.audit_medical_consultation(
		id,
		date_first_diagnosis,
		diagnosis_by_id,
		observation,
		date_create,
		user_create,
		date_modify,
		user_modify,
		patient_id,
		date_consultation,
		cie_10_id,
		responsible_doctor_id,
		apply_chemotherapy,
		hospital_id,
        origin,
		audit_event,
		audit_date_time ,
		audit_user,
		audit_client_ip
 		)
 		values (
		old.id,
		old.date_first_diagnosis,
		old.diagnosis_by_id,
		old.observation,
		old.date_create,
		old.user_create,
		old.date_modify,
		old.user_modify,
		old.patient_id,
		old.date_consultation,
		old.cie_10_id,
		old.responsible_doctor_id,
		old.apply_chemotherapy,
		old.hospital_id,
        old.origin,
		substr(TG_OP ,1,1),
 		current_timestamp,
 		session_user,
 		inet_client_addr()
 		);
		return OLD;

	else

 		INSERT INTO audit.audit_medical_consultation(
		id,
		date_first_diagnosis,
		diagnosis_by_id,
		observation,
		date_create,
		user_create,
		date_modify,
		user_modify,
		patient_id,
		date_consultation,
		cie_10_id,
		responsible_doctor_id,
		apply_chemotherapy,
		hospital_id,
        origin,
		audit_event,
		audit_date_time ,
		audit_user,
		audit_client_ip
 		)
 		values (
		new.id,
		new.date_first_diagnosis,
		new.diagnosis_by_id,
		new.observation,
		new.date_create,
		new.user_create,
		new.date_modify,
		new.user_modify,
		new.patient_id,
		new.date_consultation,
		new.cie_10_id,
		new.responsible_doctor_id,
		new.apply_chemotherapy,
		new.hospital_id,
        new.origin,
		substr(TG_OP ,1,1),
 		current_timestamp,
 		session_user,
 		inet_client_addr()
 		);
		return NEW;

	end if;
 END

$BODY$;

--ALTER IN public.specialty
ALTER TABLE audit.audit_specialty
    ADD origin varchar(30);


CREATE OR REPLACE FUNCTION public.audit_specialty()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE NOT LEAKPROOF SECURITY DEFINER
AS $BODY$

 DECLARE
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';

	if ( TG_OP = __DELETE  ) then
 		INSERT INTO audit.audit_specialty(
		id,
		description,
        origin,
		audit_event,
		audit_date_time ,
		audit_user,
		audit_client_ip
 		)
 		values (
		old.id,
		old.description,
        old.origin,
		substr(TG_OP ,1,1),
 		current_timestamp,
 		session_user,
 		inet_client_addr()
 		);
		return OLD;

	else

 		INSERT INTO audit.audit_specialty(
		id,
		description,
        origin,
		audit_event,
		audit_date_time ,
		audit_user,
		audit_client_ip
 		)
 		values (
		new.id,
		new.description,
        new.origin,
		substr(TG_OP ,1,1),
 		current_timestamp,
 		session_user,
 		inet_client_addr()
 		);
		return NEW;

	end if;
 END

$BODY$;

--ALTER IN public.doctor
ALTER TABLE audit.audit_doctor
    ADD origin varchar(30);


CREATE OR REPLACE FUNCTION public.audit_doctor()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE NOT LEAKPROOF SECURITY DEFINER
AS $BODY$

 DECLARE
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';

	if ( TG_OP = __DELETE  ) then
 		INSERT INTO audit.audit_doctor(
		id,
		firstname,
		lastname,
		registry_number,
		document_number,
		date_create,
		user_create,
		date_modify,
		user_modify,
        origin,
		audit_event,
		audit_date_time ,
		audit_user,
		audit_client_ip
 		)
 		values (
		old.id,
		old.firstname,
		old.lastname,
		old.registry_number,
		old.document_number,
		old.date_create,
		old.user_create,
		old.date_modify,
		old.user_modify,
        old.origin,
		substr(TG_OP ,1,1),
 		current_timestamp,
 		session_user,
 		inet_client_addr()
 		);
		return OLD;

	else

 		INSERT INTO audit.audit_doctor(
		id,
		firstname,
		lastname,
		registry_number,
		document_number,
		date_create,
		user_create,
		date_modify,
		user_modify,
        origin,
		audit_event,
		audit_date_time ,
		audit_user,
		audit_client_ip
 		)
 		values (
		new.id,
		new.firstname,
		new.lastname,
		new.registry_number,
		new.document_number,
		new.date_create,
		new.user_create,
		new.date_modify,
		new.user_modify,
        new.origin,
		substr(TG_OP ,1,1),
 		current_timestamp,
 		session_user,
 		inet_client_addr()
 		);
		return NEW;
	end if;
 END

$BODY$;



-- ALTER IN public.hospital
ALTER TABLE audit.audit_hospital
    ADD system boolean DEFAULT TRUE;



CREATE OR REPLACE FUNCTION public.audit_hospital()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE NOT LEAKPROOF SECURITY DEFINER
AS $BODY$

 DECLARE
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';

	if ( TG_OP = __DELETE  ) then
 		INSERT INTO audit.audit_hospital(
		id,
		description,
		country_id,
		date_create,
		user_create,
		date_modify,
		user_modify,
        system,
		audit_event,
		audit_date_time ,
		audit_user,
		audit_client_ip
 		)
 		values (
		old.id,
		old.description,
		old.country_id,
		old.date_create,
		old.user_create,
		old.date_modify,
		old.user_modify,
        old.system,
		substr(TG_OP ,1,1),
 		current_timestamp,
 		session_user,
 		inet_client_addr()
 		);
		return OLD;

	else

 		INSERT INTO audit.audit_hospital(
		id,
		description,
		country_id,
		date_create,
		user_create,
		date_modify,
		user_modify,
        system,
		audit_event,
		audit_date_time ,
		audit_user,
		audit_client_ip
 		)
 		values (
		new.id,
		new.description,
		new.country_id,
		new.date_create,
		new.user_create,
		new.date_modify,
		new.user_modify,
        new.system,
		substr(TG_OP ,1,1),
 		current_timestamp,
 		session_user,
 		inet_client_addr()
 		);
		return NEW;

	end if;
 END

$BODY$;

-- ALTER IN public.area
ALTER TABLE audit.audit_area DROP COLUMN nro_departamento;


CREATE OR REPLACE FUNCTION public.audit_area()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE NOT LEAKPROOF SECURITY DEFINER
AS $BODY$

 DECLARE
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then
 		INSERT INTO audit.audit_area(
 		id,
		description,
		country_id,
		area_number,
		audit_event,
		audit_date_time ,
		audit_user,
		audit_client_ip
 		)
 		values (
 		OLD.id,
		OLD.description,
		OLD.country_id,
		OLD.area_number,
		substr(TG_OP ,1,1),
 		current_timestamp,
 		session_user,
 		inet_client_addr()
 		);
		return OLD;
	else
 		INSERT INTO audit.audit_area(
		id,
		description,
		country_id,
		area_number,
		audit_event,
		audit_date_time ,
		audit_user,
		audit_client_ip
 		)
 		values (
		NEW.id,
		NEW.description,
		NEW.country_id,
		NEW.area_number,
		substr(TG_OP ,1,1),
 		current_timestamp,
 		session_user,
 		inet_client_addr()
 		);
		return NEW;
	end if;
 END

$BODY$;