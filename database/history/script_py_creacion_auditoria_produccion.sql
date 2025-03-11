-------------------------------Creación del esquema audit------------------------------------

CREATE SCHEMA audit AUTHORIZATION postgres;

--------------------------------------Esquema PUBLIC-----------------------------------------
----------------------------------------Tabla area-------------------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_area (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 NULL,
description varchar(100) NULL,
country_id int8 NULL,
area_number int4 NULL
);

---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_area()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_area SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_area SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;
 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_area_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.area
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_area();

 
----------------------------------------Tabla chemotherapy-----------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_chemotherapy (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 NULL,
"date" timestamp(0) NULL,
patient_id int8 NULL,
hospital_id int8 NULL,
date_create timestamp(0) NULL,
user_create varchar(30) NULL,
date_modify timestamp(0) NULL,
user_modify varchar(30) NULL,
nro_session int4 NULL,
request_state_id int8 NULL,
observation text NULL,
session_state_id int8 NULL,
doctor_id int4 NULL,
technician text NULL,
nurse text NULL
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_chemotherapy()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_chemotherapy SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_chemotherapy SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_chemotherapy_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.chemotherapy
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_chemotherapy();
 
 

----------------------------------------Tabla chemotherapy_treatment_plan-----------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_chemotherapy_treatment_plan (
audit_event character(1) null,
audit_user varchar(30) null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 NULL,
chemotherapy_id int8 NULL,
treatment_plan_id int8 NULL,
num_session int4 NULL
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_chemotherapy_treatment_plan()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_chemotherapy_treatment_plan SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_chemotherapy_treatment_plan SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_chemotherapy_treatment_plan_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.chemotherapy_treatment_plan
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_chemotherapy_treatment_plan();
 
 
----------------------------------------Tabla cie_10-----------------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_cie_10 (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 null,
code varchar(50) null,
description_es varchar(500) null,
description_en varchar(500) NULL
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_cie_10()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_cie_10 SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_cie_10 SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_cie_10_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.cie_10
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_cie_10();
  
 
 ----------------------------------------Tabla cie_o_morphology------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_cie_o_morphology (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 null,
term_en text null,
term_es text NULL,
code varchar(100) NULL
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_cie_o_morphology()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_cie_o_morphology SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_cie_o_morphology SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_cie_o_morphology_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.cie_o_morphology
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_cie_o_morphology();
  
 
 ----------------------------------------Tabla cie_o_topography------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_cie_o_topography (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 null,
code varchar(100) null,
description_es varchar(100) null,
description_en varchar(100) NULL,
gender_id int8 null
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_cie_o_topography()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_cie_o_topography SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_cie_o_topography SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_cie_o_topography_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.cie_o_topography
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_cie_o_topography();
  
 
 ----------------------------------------Tabla cie_o_tumor_location--------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_cie_o_tumor_location (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 null,
code varchar(100) null,
description_es varchar(100) null,
description_en varchar(100) NULL,
cie_o_topography_id int8 null
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_cie_o_tumor_location()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_cie_o_tumor_location SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_cie_o_tumor_location SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_cie_o_tumor_location_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.cie_o_tumor_location
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_cie_o_tumor_location();
  
 
----------------------------------------Tabla city-------------------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_city (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 null,
description varchar(100) null,
area_id int8 null
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_city()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_city SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_city SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_city_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.city
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_city();
  

----------------------------------------Tabla committee--------------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_committee (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 null,
patient_id int8 null,
hospital_id int8 null,
"date" timestamp(0) null,
observation text NULL,
date_create timestamp(0) null,
user_create varchar(30) NULL ,
date_modify timestamp(0) NULL,
user_modify varchar(30) NULL
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_committee()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_committee SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_committee SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_committee_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.committee
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_committee();
  
 
----------------------------------------Tabla configuration----------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------
 
create table audit.public_configuration (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 null,
"name" varchar(100) NULL,
value varchar(50) NULL,
code varchar(50) NULL
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_configuration()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_configuration SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_configuration SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_configuration_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public."configuration"
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_configuration();
  
 
----------------------------------------Tabla country----------------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_country (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 null,
code varchar(3) null,
description varchar(100) null,
nationality varchar(100) null
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_country()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_country SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_country SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_country_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.country
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_country();
 
 
----------------------------------------Tabla diagnosis-------------------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_diagnosis (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 null,
patient_id int8 null,
"date" timestamp(0) null,
codification_type varchar(10) NULL,
cie_10_code_id int8 NULL,
cie_o_morphology_id int8 NULL,
cie_o_topography_id int8 NULL,
cie_o_tumor_location_id int8 NULL,
date_create timestamp(0) null,
user_create varchar(30) NULL,
date_modify timestamp(0) NULL,
user_modify varchar(30) NULL,
hospital_id int8 NULL
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_diagnosis()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_diagnosis SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_diagnosis SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_diagnosis_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.diagnosis
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_diagnosis();	
  
 
----------------------------------------Tabla diagnosis_ap-------------------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_diagnosis_ap (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 null,
observation text NULL,
"date" timestamp(0) null,
tumor_size numeric null,
patient_id int8 null,
hospital_id int8 NULL,
armpit_node_number int4 NULL,
date_create timestamp(0) null,
user_create varchar(30) NULL,
date_modify timestamp(0) NULL,
user_modify varchar(30) NULL,
doctor_id int8 NULL,
cie_o_morphology_id int8 NULL,
cie_o_topography_id int8 NULL,
cie_o_tumor_location_id int8 NULL,
re varchar(20) NULL,
rp varchar(20) NULL,
her2 varchar(20) NULL,
her2_positive_id int8 NULL,
armpit varchar(20) NULL,
general_report text NULL,
origin varchar(30) NULL,
dx_presuntivo text NULL,
material text NULL,
diagnostico text NULL,
clasificacion text NULL,
macroscopia text NULL,
microscopia text NULL
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_diagnosis_ap()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_diagnosis_ap SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_diagnosis_ap SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_diagnosis_ap_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.diagnosis_ap
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_diagnosis_ap();	
  
 
 
----------------------------------------Tabla doctor-------------------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_doctor (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 NULL,
firstname varchar(200) NULL,
lastname varchar(200) NULL,
registry_number varchar(50) NULL,
document_number varchar(50) NULL,
date_create timestamp(0) NULL,
user_create varchar(30) NULL ,
date_modify timestamp(0) NULL,
user_modify varchar(30) NULL,
origin varchar(30) NULL
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_doctor()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_doctor SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_doctor SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_doctor_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.doctor
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_doctor();	
  
 
----------------------------------------Tabla doctor_specialty-------------------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_doctor_specialty (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 null,
doctor_id int8 null,
specialty_id int8 null
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_doctor_specialty()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_doctor_specialty SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_doctor_specialty SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_doctor_specialty_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.doctor_specialty
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_doctor_specialty();	

 
 
----------------------------------------Tabla document_type-------------------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_document_type (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 NULL,
description varchar(100) NULL,
code varchar(20) NULL
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_document_type()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_document_type SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_document_type SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_document_type_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.document_type
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_document_type();	

 
 
----------------------------------------Tabla evaluation-------------------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_evaluation (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 null,
patient_id int8 NULL,
date_start timestamp(0) NULL,
date_end timestamp(0) NULL,
observation text NULL,
date_create timestamp(0) null,
user_create varchar(30) NULL,
date_modify timestamp(0) NULL,
user_modify varchar(30) NULL,
approved bool NULL,
evaluation_state varchar(10) NULL
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_evaluation()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_evaluation SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_evaluation SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_evaluation_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.evaluation
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_evaluation();
  
 
----------------------------------------Tabla evaluators-------------------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_evaluators (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 null,
evaluation_id int8 null,
evaluator_id int8 null
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_evaluators()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_evaluators SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_evaluators SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_evaluators_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.evaluators
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_evaluators();
 

----------------------------------------Tabla follow_up_treatment_plan-------------------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_follow_up_treatment_plan (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id bigint null,
follow_up_id int8 NULL,
treatment_plan_id int8 null
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_follow_up_treatment_plan()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_follow_up_treatment_plan SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_follow_up_treatment_plan SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_follow_up_treatment_plan_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.follow_up_treatment_plan
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_follow_up_treatment_plan();
 
 
----------------------------------------Tabla gender-------------------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_gender (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 NULL,
description varchar(100) NULL,
code varchar(20) NULL
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_gender()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_gender SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_gender SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_gender_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.gender
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_gender();
  
 
----------------------------------------Tabla hospital-------------------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_hospital (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 NULL,
description varchar(100) NULL,
country_id int8 NULL,
date_create timestamp(0) NULL,
user_create varchar(30) NULL,
date_modify timestamp(0) NULL,
user_modify varchar(30) NULL,
"system" bool NULL
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_hospital()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_hospital SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_hospital SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_hospital_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.hospital
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_hospital();
  
 
----------------------------------------Tabla medical_committee-------------------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_medical_committee (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 null,
committee_id int8 null,
doctor_id int8 null
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_medical_committee()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_medical_committee SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_medical_committee SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_medical_committee_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.medical_committee
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_medical_committee();
  
 
----------------------------------------Tabla medical_consultation-------------------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_medical_consultation (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 NULL,
date_first_diagnosis date NULL,
diagnosis_by_id int8 NULL,
observation text NULL,
date_create timestamp(0) NULL,
user_create varchar(30) NULL,
date_modify timestamp(0) NULL,
user_modify varchar(30) NULL,
patient_id int8 NULL,
date_consultation date NULL,
cie_10_id int8 NULL,
responsible_doctor_id int8 NULL,
apply_chemotherapy varchar(20) NULL,
hospital_id int8 NULL,
origin varchar(30) NULL
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_medical_consultation()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_medical_consultation SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_medical_consultation SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_medical_consultation_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.medical_consultation
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_medical_consultation();
  
 
----------------------------------------Tabla medical_document-------------------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_medical_document (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 null,
medical_document_type_id int8 null,
description text null,
"path" text null,
patient_id int8 null,
modulo varchar(255) NULL,
study_date timestamp(0) NULL,
date_create timestamp(0) null,
user_create varchar(30) NULL,
date_modify timestamp(0) NULL,
user_modify varchar(30) NULL,
origen_id int8 NULL,
hospital_id int8 NULL
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_medical_document()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_medical_document SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_medical_document SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_medical_document_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.medical_document
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_medical_document();
  
 
----------------------------------------Tabla medical_document_type-------------------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_medical_document_type (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 NULL,
description varchar(500) NULL,
orden int4 NULL,
code varchar(20) NULL
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_medical_document_type()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_medical_document_type SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_medical_document_type SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_medical_document_type_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.medical_document_type
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_medical_document_type();
  
 
----------------------------------------Tabla medical_team-------------------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_medical_team (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 null,
surgery_id int8 NULL,
doctor_id int8 NULL,
rol varchar(100) NULL,
nurse text NULL,
anesthetist text NULL,
surgical_instrumentator text NULL,
technical text NULL
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_medical_team()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_medical_team SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_medical_team SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_medical_team_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.medical_team
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_medical_team();
  
 
----------------------------------------Tabla medication_order-------------------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_medication_order (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 NULL,
observation text NULL,
"date" timestamp(0) NULL,
patient_id int8 null,
doctor_id int8 NULL,
previous bool null,
hospital_id int8 NULL
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_medication_order()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_medication_order SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_medication_order SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_medication_order_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.medication_order
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_medication_order();
  
 
 
----------------------------------------Tabla medicine---------------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_medicine (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 NULL,
description varchar(200) NULL,
code varchar(100) NULL,
concentration varchar NULL,
pharmaceutical_form varchar NULL,
via_admin varchar(100) NULL,
presentation varchar(200) NULL,
code_dgc varchar(100) NULL,
state bpchar(1) NULL,
date_create timestamp(0) NULL,
user_create varchar(30) NULL,
date_modify timestamp(0) NULL,
user_modify varchar(30) NULL,
stock_control bool NULL,
generic_name varchar(200) NULL
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_medicine()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_medicine SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_medicine SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_medicine_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.medicine
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_medicine();
 
 
 
----------------------------------------Tabla medicine_chemotherapy---------------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_medicine_chemotherapy (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id bigint null,
medicine_id int8 NULL,
chemotherapy_id int8 NULL,
quantity numeric NULL,
observation text NULL,
dose numeric NULL,
presentation text NULL,
concentration text NULL
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_medicine_chemotherapy()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_medicine_chemotherapy SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_medicine_chemotherapy SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_medicine_chemotherapy_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.medicine_chemotherapy
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_medicine_chemotherapy();
 
 
 
 ----------------------------------------Tabla medicine_medical_consultation-----------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_medicine_medical_consultation (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 null,
medicine_id int8 null,
medical_consultation_id int8 null,
quantity numeric null,
observation text NULL,
dose numeric NULL,
presentation text NULL,
concentration text NULL
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_medicine_medical_consultation()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_medicine_medical_consultation SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_medicine_medical_consultation SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_medicine_medical_consultation_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.medicine_medical_consultation
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_medicine_medical_consultation();
  
 
----------------------------------------Tabla medicine_treatment_follow_up----------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_medicine_treatment_follow_up (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 null,
medicine_id int8 null,
treatment_follow_up_id int8 null,
quantity numeric null,
observation text NULL,
dose numeric NULL,
presentation text NULL,
concentration text NULL,
deposit_stock_id int8 NULL
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_medicine_treatment_follow_up()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_medicine_treatment_follow_up SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_medicine_treatment_follow_up SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_medicine_treatment_follow_up_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.medicine_treatment_follow_up
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_medicine_treatment_follow_up();
  
 
 
----------------------------------------Tabla medicine_treatment_plan-------------------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_medicine_treatment_plan (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 null,
medicine_id int8 null,
treatment_plan_id int8 null,
quantity numeric null,
observation text NULL,
dose numeric NULL,
presentation text NULL,
concentration text NULL
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_medicine_treatment_plan()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_medicine_treatment_plan SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_medicine_treatment_plan SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_medicine_treatment_plan_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.medicine_treatment_plan
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_medicine_treatment_plan();
  
 
 
----------------------------------------Tabla menopausal_state-------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_menopausal_state (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 null,
description varchar(50) null,
code varchar(20) NULL
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_menopausal_state()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_menopausal_state SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_menopausal_state SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_menopausal_state_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.menopausal_state
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_menopausal_state();
  
 
 
----------------------------------------Tabla parameter--------------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_parameter (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 null,
"domain" varchar(100) null,
value varchar(255) null,
active bool null,
code varchar(20) NULL
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_parameter()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_parameter SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_parameter SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_parameter_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public."parameter"
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_parameter();
  
 
 
----------------------------------------Tabla patient-------------------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_patient (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 null,
firstname text null,
lastname text null,
document_number text NULL,
state_id int8 null,
birthdate date null,
address varchar(500) NULL,
gender_id int8 NULL,
document_type_id int8 null,
country_id int8 NULL,
area_id int8 NULL,
city_id int8 NULL,
phone varchar(100) NULL,
nationality_id int8 NULL,
hospital_id int8 null,
vital_state_id int8 null,
date_create timestamp(0) null,
user_create varchar(30) NULL,
date_modify timestamp(0) NULL,
user_modify varchar(30) NULL,
registration_date date null,
civil_status_id int8 NULL,
responsible_firstname text NULL,
responsible_lastname text NULL,
responsible_relationship text NULL,
responsible_phone varchar(50) NULL,
number_card int4 NULL,
origin varchar(30) NULL
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_patient()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_patient SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_patient SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_patient_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.patient
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_patient();
  
 
 
----------------------------------------Tabla patient_exclusion_criteria---------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_patient_exclusion_criteria (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 null,
patient_id int8 null,
distant_metastatic bool NULL,
life_expectancy_greater_5_comorbidities bool NULL,
fevi_less_50 bool NULL,
ecog_eq_greater_2 bool NULL,
congestive_ic bool NULL,
ischemic_heart_disease bool NULL,
arritmia_inestable bool NULL,
valve_disease bool NULL,
uncontrolled_hta bool NULL,
doxorubicin_greater_360mg_by_m2 bool NULL,
epirrubicina_greater_720mg_by_m2 bool NULL,
pregnancy bool NULL,
lactation bool NULL,
date_create timestamp(0) null,
user_create varchar(30) NULL,
date_modify timestamp(0) NULL,
user_modify varchar(30) NULL,
hospital_id int8 NULL
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_patient_exclusion_criteria()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_patient_exclusion_criteria SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_patient_exclusion_criteria SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_patient_exclusion_criteria_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.patient_exclusion_criteria
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_patient_exclusion_criteria();
  
 
----------------------------------------Tabla patient_family_with_cancer-------------------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_patient_family_with_cancer (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 null,
personal_pathological_history_id int8 NULL,
family_id int8 NULL,
family_vital_state_id int8 NULL
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_patient_family_with_cancer()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_patient_family_with_cancer SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_patient_family_with_cancer SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_patient_family_with_cancer_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.patient_family_with_cancer
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_patient_family_with_cancer();
 
 
 
----------------------------------------Tabla patient_hospital-------------------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_patient_hospital (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id bigint null,
patient_id int8 NULL,
hospital_id int8 NULL
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_patient_hospital()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_patient_hospital SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_patient_hospital SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_patient_hospital_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.patient_hospital
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_patient_hospital();
  
 
 
----------------------------------------Tabla patient_inclusion_criteria-------------------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_patient_inclusion_criteria (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 null,
patient_id int8 null,
treatment_type varchar(30) NULL,
patient_inclusion_criteria_adjuvant_id int8 NULL,
patient_inclusion_criteria_neoadjuvant_id int8 NULL,
has_signed_informed_consent bool NULL,
patient_received_document bool NULL,
consent_obtained_through_dialogue bool NULL,
has_received_sufficient_sufficient bool NULL,
has_asked_questions_and_can_continue_asking bool NULL,
informed_receive_permanent_continuous_information bool NULL,
information_received_clear_complete bool NULL,
received_information_understandable_language bool NULL,
treatment_hospital_id int8 NULL,
date_create timestamp(0) null,
user_create varchar(30) NULL,
date_modify timestamp(0) NULL,
user_modify varchar(30) NULL,
doctor_id int8 NULL,
specialty_id int8 NULL,
hospital_id int8 NULL
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_patient_inclusion_criteria()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_patient_inclusion_criteria SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_patient_inclusion_criteria SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_patient_inclusion_criteria_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.patient_inclusion_criteria
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_patient_inclusion_criteria();
  
 
 
---------------------Tabla patient_inclusion_criteria_adjuvant_trastuzumab-------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_patient_inclusion_criteria_adjuvant_trastuzumab (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 null,
patient_id int8 null,
diagnosed_invasive_adenocarcinoma bool NULL,
adenocarcinoma_completely_resected bool NULL,
tumor_diameter_greater_10mm bool NULL,
adjuvant_trastuzumab_her2_positive bool NULL,
determination_hormone_receptors bool NULL,
absolute_neutrophils_eq_greater_1500_ul bool NULL,
platelets_eq_greater_90000_mm3 bool NULL,
renal_hepatic_appropriate bool NULL,
date_create timestamp(0) null,
user_create varchar(30) NULL,
date_modify timestamp(0) NULL,
user_modify varchar(30) NULL,
her2_positive_id jsonb NULL
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_patient_inclusion_criteria_adjuvant_trastuzumab()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_patient_inclusion_criteria_adjuvant_trastuzumab SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_patient_inclusion_criteria_adjuvant_trastuzumab SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_patient_inclusion_criteria_adjuvant_trastuzumab_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.patient_inclusion_criteria_adjuvant_trastuzumab
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_patient_inclusion_criteria_adjuvant_trastuzumab();
  
 
 
---------------------Tabla patient_inclusion_criteria_neoadjuvant_trastuzumab----------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_patient_inclusion_criteria_neoadjuvant_trastuzumab (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 null,
patient_id int8 null,
diagnosed_invasive_adenocarcinoma bool NULL,
neoadjuvant_trastuzumab_her2_positive bool NULL,
tumor_eq_ge_2cm bool NULL,
positive_axilla bool NULL,
marked_tumor_bed bool NULL,
blood_count_renal_hepatic_appropriate bool NULL,
determination_hormone_receptors bool NULL,
date_create timestamp(0) null,
user_create varchar(30) NULL,
date_modify timestamp(0) NULL,
user_modify varchar(30) NULL,
her2_positive_id jsonb NULL,
tumor_size_diameter_determined_by varchar(30) NULL,
positive_armpit_determined_by varchar(30) null
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_patient_inclusion_criteria_neoadjuvant_trastuzumab()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_patient_inclusion_criteria_neoadjuvant_trastuzumab SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_patient_inclusion_criteria_neoadjuvant_trastuzumab SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_patient_inclusion_criteria_neoadjuvant_trastuzumab_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.patient_inclusion_criteria_neoadjuvant_trastuzumab
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_patient_inclusion_criteria_neoadjuvant_trastuzumab();
  
 
 
----------------------------------------Tabla periodicity------------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_periodicity (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 null,
description varchar(100) null,
active bool NULL,
code varchar(20) NULL
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_periodicity()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_periodicity SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_periodicity SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_periodicity_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.periodicity
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_periodicity();
  
 
 
----------------------------------------Tabla permission-------------------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_permission (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 null,
description varchar(100) null
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_permission()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_permission SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_permission SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_permission_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public."permission"
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_permission();
  
 
 
----------------------------------------Tabla personal_pathological_history------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_personal_pathological_history (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 null,
family_members_with_cancer varchar(20) NULL,
observation text NULL,
app_funtional_class_nyha_id int8 NULL,
app_ischemic_heart_disease bool null,
app_heart_failure bool null,
app_arrhythmia bool null,
app_heart_others bool NULL,
app_heart_others_input text NULL,
menopausal_state_id int8 NULL,
app_menopausal_others text NULL,
fevi_percentage int4 NULL,
fevi_date timestamp(0) NULL,
date_create timestamp(0) null,
user_create varchar(30) NULL,
date_modify timestamp(0) NULL,
user_modify varchar(30) NULL,
patient_id int4 NULL,
cie_10_code_id int8 NULL,
hospital_id int8 null
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_personal_pathological_history()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_personal_pathological_history SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_personal_pathological_history SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_personal_pathological_history_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.personal_pathological_history
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_personal_pathological_history();
  
 
 
----------------------------------------Tabla puncture---------------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_puncture (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 null,
patient_id int8 null,
"date" timestamp(0) null,
observation text NULL,
doctor_id int8 null,
hospital_id int8 NULL,
date_create timestamp(0) null,
user_create varchar(30) NULL,
date_modify timestamp(0) NULL,
user_modify varchar(30) NULL
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_puncture()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_puncture SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_puncture SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_puncture_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.puncture
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_puncture();
  
 
 
----------------------------------------Tabla radiotherapy-----------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_radiotherapy (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 null,
"date" timestamp(0) null,
patient_id int8 null,
hospital_id int8 NULL,
date_create timestamp(0) null,
user_create varchar(30) NULL,
date_modify timestamp(0) NULL,
user_modify varchar(30) NULL,
nro_session int8 NULL,
observation text NULL,
session_state_id int8 NULL,
doctor_id int8 NULL,
technician text NULL,
nurse text NULL
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_radiotherapy()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_radiotherapy SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_radiotherapy SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_radiotherapy_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.radiotherapy
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_radiotherapy();
  
 
----------------------------------------Tabla radiotherapy_treatment_plan-----------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_radiotherapy_treatment_plan(
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id bigint null,
radiotherapy_id int8 NULL,
treatment_plan_id int8 NULL,
num_session int4 NULL
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_radiotherapy_treatment_plan()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_radiotherapy_treatment_plan SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_radiotherapy_treatment_plan SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_radiotherapy_treatment_plan_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.radiotherapy_treatment_plan
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_radiotherapy_treatment_plan();

 
----------------------------------------Tabla role-------------------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_role (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 null,
description varchar(100) null,
date_create timestamp(0) null,
user_create varchar(30) NULL,
date_modify timestamp(0) NULL,
user_modify varchar(30) NULL
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_role()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_role SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_role SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_role_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public."role"
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_role();
  
 
 
----------------------------------------Tabla role_permission-------------------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_role_permission (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 null,
role_id int8 null,
permission_id int8 null
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_role_permission()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_role_permission SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_role_permission SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_role_permission_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.role_permission
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_role_permission();
  
 
 
----------------------------------------Tabla specialty-------------------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_specialty (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 null,
description varchar(300) NULL,
origin varchar(30) NULL
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_specialty()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_specialty SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_specialty SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_specialty_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.specialty
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_specialty();
  
 
 
----------------------------------------Tabla surgery-------------------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_surgery (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 null,
patient_id int8 null,
"date" timestamp(0) NULL,
observation text NULL,
hospital_id int8 NULL,
date_create timestamp(0) null,
user_create varchar(30) NULL,
date_modify timestamp(0) NULL,
user_modify varchar(30) NULL,
surgical_technique text NULL
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_surgery()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_surgery SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_surgery SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_surgery_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.surgery
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_surgery();
  
 
 
----------------------------------------Tabla treatment_follow_up-------------------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_treatment_follow_up (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 NULL,
follow_up_date date NULL,
last_cancer_control_date date NULL,
type_treatment varchar(30) NULL,
breast varchar(30) NULL,
armpit bool NULL,
suspension_treatment bool NULL,
suspension_treatment_reason text NULL,
congestive_heart_failure bool NULL,
fevi_follow_up_date date NULL,
fevi_value int4 NULL,
fevi_trastuzumab_dose int4 NULL,
other_severe_adverse_events bool NULL,
other_severe_adverse_events_detail text NULL,
other_complementary_studies text NULL,
dose_adjustment bool NULL,
dose_adjustment_reason varchar(100) NULL,
comentaries text NULL,
suspension_treatment_custom_reason text NULL,
date_create timestamp(0) NULL,
user_create varchar(30) NULL,
date_modify timestamp(0) NULL,
user_modify varchar(30) NULL,
patient_id int8 NULL,
hospital_id int8 NULL,
doctor_id int8 NULL
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_treatment_follow_up()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_treatment_follow_up SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_treatment_follow_up SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_treatment_follow_up_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.treatment_follow_up
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_treatment_follow_up();
  
 
----------------------------------------Tabla treatment_plan-------------------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_treatment_plan (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 null,
patient_id int8 null,
hospital_id int8 null,
"date" timestamp(0) null,
doctor_id int8 null,
"size" numeric NULL,
weight numeric NULL,
sc numeric NULL,
medical_visit_observation text NULL,
cie_10_code_id int8 NULL,
cie_o_morphology_id int8 NULL,
cie_o_topography_id int8 NULL,
cie_o_tumor_location_id int8 NULL,
type_id int8 null,
number_sessions int4 null,
periodicity_id int8 null,
date_first_cycle date NULL,
date_last_cycle date NULL,
observation text NULL,
origin varchar null,
date_create timestamp(0) null,
user_create varchar(30) null,
date_modify timestamp(0) NULL,
user_modify varchar(30) NULL,
"number" int8 NULL,
state_id int8 NULL
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_treatment_plan()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_treatment_plan SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_treatment_plan SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_treatment_plan_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.treatment_plan
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_treatment_plan();
  
 
 
----------------------------------------Tabla type_treatment-------------------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_type_treatment (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 null,
description varchar(100) null,
code varchar(20) NULL
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_type_treatment()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_type_treatment SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_type_treatment SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_type_treatment_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.type_treatment
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_type_treatment();
  
 
 
----------------------------------------Tabla user-------------------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_user (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 null,
"user" varchar(100) null,
state varchar(1) null,
"password" varchar(255) null,
firstname varchar(100) NULL,
lastname varchar(100) NULL,
administrator bool null,
email varchar(50) NULL,
date_create timestamp(0) null,
user_create varchar(30) NULL,
date_modify timestamp(0) NULL,
user_modify varchar(30) NULL
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_user()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_user SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_user SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_user_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public."user"
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_user();
  
 
 
----------------------------------------Tabla user_hospital-------------------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.public_user_hospital (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 null,
user_id int8 null,
role_id int8 null,
hospital_id int8 null
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION public.audit_user_hospital()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_user_hospital SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_user_hospital SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;

 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_user_hospital_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.user_hospital
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_user_hospital();




-------------------------------------Esquema INVENTORY---------------------------------------
---------------------------------------Tabla deposit-----------------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.inventory_deposit (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 NULL,
code varchar(50) NULL,
"name" varchar(100) NULL,
description varchar(500) NULL,
city varchar(20) NULL,
address varchar(100) NULL,
email varchar(20) NULL,
phone varchar(30) NULL,
date_create timestamp(0) NULL,
user_create varchar(30) NULL,
date_modify timestamp(0) NULL,
user_modify varchar(30) NULL,
hospital_id int8 NULL,
type_id int8 NULL
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION inventory.audit_deposit()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.inventory_deposit SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.inventory_deposit SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;
 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_deposit_all
  AFTER INSERT OR UPDATE OR DELETE
  ON inventory.deposit
  FOR EACH ROW
  EXECUTE PROCEDURE inventory.audit_deposit();


---------------------------------------Tabla deposit_movement-----------------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.inventory_deposit_movement (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 NULL,
deposit_stock_in_id int8 NULL,
deposit_stock_out_id int8 NULL,
quantity float8 NULL,
date_create timestamp(0) NULL,
user_create varchar(30) NULL
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION inventory.audit_deposit_movement()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.inventory_deposit_movement SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.inventory_deposit_movement SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;
 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_deposit_movement_all
  AFTER INSERT OR UPDATE OR DELETE
  ON inventory.deposit_movement
  FOR EACH ROW
  EXECUTE PROCEDURE inventory.audit_deposit_movement();


  ---------------------------------------Tabla deposit_stock-----------------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.inventory_deposit_stock (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 NULL,
deposit_id int8 NULL,
stock_id int8 NULL,
quantity float8 NULL
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION inventory.audit_deposit_stock()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.inventory_deposit_stock SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.inventory_deposit_stock SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;
 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_deposit_stock_all
  AFTER INSERT OR UPDATE OR DELETE
  ON inventory.deposit_stock
  FOR EACH ROW
  EXECUTE PROCEDURE inventory.audit_deposit_stock();



  ---------------------------------------Tabla dispatch_medications-----------------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.inventory_dispatch_medications (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 NULL,
deposit_stock_id int8 NULL,
patient_id int8 NULL,
medicine_id int8 NULL,
quantity float8 NULL,
origin varchar(30) NULL,
date_create timestamp(0) NULL,
user_create varchar(30) NULL,
"date" timestamp NULL
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION inventory.audit_dispatch_medications()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.inventory_dispatch_medications SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.inventory_dispatch_medications SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;
 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_dispatch_medications_all
  AFTER INSERT OR UPDATE OR DELETE
  ON inventory.dispatch_medications
  FOR EACH ROW
  EXECUTE PROCEDURE inventory.audit_dispatch_medications();



  ---------------------------------------Tabla entries-----------------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.inventory_entries (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 NULL,
deposit_id int8 NULL,
medicine_id int8 NULL,
description varchar(500) NULL,
expiration_date date NULL,
quantity float8 NULL,
manufacturer_id int8 NULL,
manufacturing_date timestamp(0) NULL,
supplier_id int8 NULL,
storage_conditions varchar(500) NULL,
observation varchar(500) NULL,
"date" date NULL,
origin varchar(30) NULL
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION inventory.audit_entries()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.inventory_entries SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.inventory_entries SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;
 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_entries_all
  AFTER INSERT OR UPDATE OR DELETE
  ON inventory.entries
  FOR EACH ROW
  EXECUTE PROCEDURE inventory.audit_entries();



  ---------------------------------------Tabla entries_deposit_stock-----------------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.inventory_entries_deposit_stock (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 NULL,
entries_id int8 NULL,
deposit_stock_id int8 NULL
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION inventory.audit_entries_deposit_stock()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.inventory_entries_deposit_stock SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.inventory_entries_deposit_stock SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;
 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_entries_deposit_stock_all
  AFTER INSERT OR UPDATE OR DELETE
  ON inventory.entries_deposit_stock
  FOR EACH ROW
  EXECUTE PROCEDURE inventory.audit_entries_deposit_stock();



  ---------------------------------------Tabla entries_lot-----------------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.inventory_entries_lot (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 NULL,
lot_id int8 NULL,
entries_id int8 NULL
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION inventory.audit_entries_lot()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.inventory_entries_lot SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.inventory_entries_lot SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;
 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_entries_lot_all
  AFTER INSERT OR UPDATE OR DELETE
  ON inventory.entries_lot
  FOR EACH ROW
  EXECUTE PROCEDURE inventory.audit_entries_lot();



  ---------------------------------------Tabla history-----------------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.inventory_history (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 NULL,
orig_deposit_stock_id int8 NULL,
quantity float8 NULL,
event_id int8 NULL,
description varchar(500) NULL,
date_create timestamp(0) NULL,
user_create varchar(30) NULL,
dest_deposit_stock_id int8 NULL,
origin varchar(30) NULL,
"date" timestamp NULL,
observation text NULL,
balance float8 NULL,
original_quantity float8 NULL
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION inventory.audit_history()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.inventory_history SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.inventory_history SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;
 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_history_all
  AFTER INSERT OR UPDATE OR DELETE
  ON inventory.history
  FOR EACH ROW
  EXECUTE PROCEDURE inventory.audit_history();



  ---------------------------------------Tabla lot-----------------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.inventory_lot (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 NULL,
num_lot varchar(50) NULL,
date_create timestamp(0) NULL,
user_create varchar(30) NULL,
date_modify timestamp(0) NULL,
user_modify varchar(30) NULL,
origin varchar(30) NULL,
"date" timestamp(0) NULL
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION inventory.audit_lot()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.inventory_lot SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.inventory_lot SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;
 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_lot_all
  AFTER INSERT OR UPDATE OR DELETE
  ON inventory.lot
  FOR EACH ROW
  EXECUTE PROCEDURE inventory.audit_lot();



  ---------------------------------------Tabla manufacturer-----------------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.inventory_manufacturer (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 NULL,
"name" varchar(100) NULL,
county_id int8 NULL,
state_id int8 NULL,
date_create timestamp(0) NULL,
user_create varchar(30) NULL,
date_modify timestamp(0) NULL,
user_modify varchar(30) NULL
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION inventory.audit_manufacturer()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.inventory_manufacturer SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.inventory_manufacturer SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;
 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_manufacturer_all
  AFTER INSERT OR UPDATE OR DELETE
  ON inventory.manufacturer
  FOR EACH ROW
  EXECUTE PROCEDURE inventory.audit_manufacturer();




  ---------------------------------------Tabla stock-----------------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.inventory_stock (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 NULL,
medicine_id int8 NULL,
quantity float8 NULL,
state_id int8 NULL
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION inventory.audit_stock()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.inventory_stock SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.inventory_stock SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;
 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_stock_all
  AFTER INSERT OR UPDATE OR DELETE
  ON inventory.stock
  FOR EACH ROW
  EXECUTE PROCEDURE inventory.audit_stock();



  ---------------------------------------Tabla supplier-----------------------------------------
---------------------------Creación de las tablas de auditoría-------------------------------

create table audit.inventory_supplier (
audit_event character(1) null,
audit_user varchar(30)null,
audit_date_time timestamp with time zone null,
audit_client_ip inet,
id int8 NULL,
"name" varchar(100) NULL,
county_id int8 NULL,
address varchar(100) NULL,
phone varchar(100) NULL,
email varchar(20) NULL,
description varchar(500) NULL,
state_id int8 NULL,
date_create timestamp(0) NULL,
user_create varchar(30) NULL,
date_modify timestamp(0) NULL,
user_modify varchar(30) NULL
);


---------------------Creación de los trigger functions para auditoría------------------------

CREATE OR REPLACE FUNCTION inventory.audit_supplier()
  RETURNS trigger AS
$BODY$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.inventory_supplier SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.inventory_supplier SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;
 
-----------------------------Creación del trigger de audit-----------------------------------
CREATE TRIGGER audit_supplier_all
  AFTER INSERT OR UPDATE OR DELETE
  ON inventory.supplier
  FOR EACH ROW
  EXECUTE PROCEDURE inventory.audit_supplier();



