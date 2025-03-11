--------------------------------
-- CREATE TABLE public.module --
--------------------------------
CREATE TABLE public.module (
	id serial NOT NULL,
	description varchar(100) NOT NULL,
	date_create timestamp(0) DEFAULT now() NOT NULL,
	user_create varchar(30) DEFAULT 'readiness'::character varying NULL,
	date_modify timestamp(0) NULL,
	user_modify varchar(30) NULL,
	CONSTRAINT module_pk PRIMARY KEY (id)
);

--------------------------------------
-- CREATE TABLE audit.public_module --
--------------------------------------
CREATE TABLE audit.public_module (
	audit_event bpchar(1) NULL,
	audit_user varchar(30) NULL,
	audit_date_time timestamptz NULL,
	audit_client_ip inet NULL,
	id int8 NULL,
	description varchar(100) NULL,
	date_create timestamp(0) NULL,
	user_create varchar(30) NULL,
	date_modify timestamp(0) NULL,
	user_modify varchar(30) NULL
);

-------------------------------------
-- AUDIT OPTIONS FOR public.module --
-------------------------------------
CREATE FUNCTION public.audit_module() RETURNS trigger
    SECURITY DEFINER
    LANGUAGE plpgsql
AS
$$
 DECLARE
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then
 		INSERT INTO audit.public_module SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;
	else
 		INSERT INTO audit.public_module SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if;
 END
 $$;

CREATE TRIGGER audit_module_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.module
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_module();

-------------------------------------------
-- CREATE TABLE public.module_permission --
-------------------------------------------
CREATE TABLE public.module_permission (
	id serial NOT NULL,
	module_id int8 NOT NULL,
	permission_id int8 NOT NULL,
	CONSTRAINT modulo_permiso_pk PRIMARY KEY (id),
	CONSTRAINT module_permission_pk UNIQUE (module_id, permission_id)
);

ALTER TABLE public.module_permission ADD CONSTRAINT modulo_permiso_fk FOREIGN KEY (permission_id) REFERENCES public."permission"(id);
ALTER TABLE public.module_permission ADD CONSTRAINT modulo_permiso_fk_1 FOREIGN KEY (module_id) REFERENCES public."module"(id);

-------------------------------------------------
-- CREATE TABLE audit.public_module_permission --
-------------------------------------------------
CREATE TABLE audit.public_module_permission (
	audit_event bpchar(1) NULL,
	audit_user varchar(30) NULL,
	audit_date_time timestamptz NULL,
	audit_client_ip inet NULL,
	id int8 NULL,
	module_id int8 NULL,
	permission_id int8 NULL
);

-------------------------------------
-- AUDIT OPTIONS FOR public.module --
-------------------------------------
CREATE FUNCTION public.audit_module_permission() RETURNS trigger
    SECURITY DEFINER
    LANGUAGE plpgsql
AS
$$
 DECLARE
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then
 		INSERT INTO audit.public_module_permission SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;
	else
 		INSERT INTO audit.public_module_permission SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if;
 END
 $$;

CREATE TRIGGER audit_module_permission_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.module_permission
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_module_permission();

-------------------------------------
-- CREATE TABLE public.module_role --
-------------------------------------
CREATE TABLE public.module_role (
	id serial NOT NULL,
	module_id int8 NOT NULL,
	role_id int8 NOT NULL,
	CONSTRAINT modulo_rol_pk PRIMARY KEY (id)
);

ALTER TABLE public.module_role ADD CONSTRAINT modulo_rol_fk FOREIGN KEY (module_id) REFERENCES public."module"(id);
ALTER TABLE public.module_role ADD CONSTRAINT modulo_rol_fk_2 FOREIGN KEY (role_id) REFERENCES public."role"(id);

-------------------------------------------
-- CREATE TABLE audit.public_module_role --
-------------------------------------------
CREATE TABLE audit.public_module_role (
	audit_event bpchar(1) NULL,
	audit_user varchar(30) NULL,
	audit_date_time timestamptz NULL,
	audit_client_ip inet NULL,
	id int8 NULL,
	module_id int8 NULL,
	role_id int8 NULL
);

-------------------------------------
-- AUDIT OPTIONS FOR public.module --
-------------------------------------
CREATE FUNCTION public.audit_module_role() RETURNS trigger
    SECURITY DEFINER
    LANGUAGE plpgsql
AS
$$
 DECLARE
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then
 		INSERT INTO audit.public_module_role SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;
	else
 		INSERT INTO audit.public_module_role SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if;
 END
 $$;

CREATE TRIGGER audit_module_role_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.module_role
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_module_role();

---------------------
-- ADD PERMISSIONS --
---------------------
INSERT INTO public."permission" (description)
VALUES ('module_permission_list'),
       ('module_permission_search'),
       ('module_permission_get'),
       ('module_permission_insert'),
       ('module_permission_update'),
       ('module_permission_delete'),
       ('module_role_list'),
       ('module_role_search'),
       ('module_role_get'),
       ('module_role_insert'),
       ('module_role_update'),
       ('module_role_delete'),
       ('module_list'),
       ('module_search'),
       ('module_get'),
       ('module_insert'),
       ('module_update'),
       ('module_delete'),
       ('menu_module');

-------------------------------
-- ALTER IN public.user_role --
-------------------------------
ALTER TABLE public.user_hospital RENAME TO user_role;
ALTER TABLE audit.public_user_hospital RENAME TO public_user_role;

-----------------------------
-- ALTER PERMISSIONS NAMES --
-----------------------------
UPDATE public."permission"
SET description='user_role_get'
WHERE description='user_hospital_get';
UPDATE public."permission"
SET description='user_role_update'
WHERE description='user_hospital_update';
UPDATE public."permission"
SET description='user_role_delete'
WHERE description='user_hospital_delete';
UPDATE public."permission"
SET description='user_role_list'
WHERE description='user_hospital_list';
UPDATE public."permission"
SET description='user_role_insert'
WHERE description='user_hospital_insert';
UPDATE public."permission"
SET description='user_role_search'
WHERE description='user_hospital_search';


------------------------------
-- CONFIGURACIÓN DE MÓDULOS --
------------------------------

