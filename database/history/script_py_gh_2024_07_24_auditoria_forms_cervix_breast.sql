CREATE TABLE audit.public_breast_form (
	audit_event bpchar(1) NULL,
	audit_user varchar(30) NULL,
	audit_date_time timestamptz NULL,
	audit_client_ip inet NULL,
	id int8 NULL,
	patient_id int8 NULL,
	departament text NULL,
	residential_address text NULL,
	parity bool NULL,
	pmhx text NULL,
	presenting_complaint text NULL,
	main_physical_clinical_findings text NULL,
	performance_status_ecog_id int8 NULL,
	treatment_decision text NULL,
	mammogram_date timestamp(0) NULL,
	mammogram_birads_id int8 NULL,
	mammogram_report_id int8 NULL,
	usg_breast_date timestamp(0) NULL,
	usg_breast_birads_id int8 NULL,
	usg_breast_report_id int8 NULL,
	fnac_date timestamp(0) NULL,
	fnac_report_id int8 NULL,
	fnac_summary text NULL,
	trucut_date timestamp(0) NULL,
	trucut_histology_report_id int8 NULL,
	trucut_morphology_id int8 NULL,
	trucut_others text NULL,
	trucut_grade text NULL,
	trucut_hormone_receptor_status_id int8 NULL,
	trucut_her2_neu_id int8 NULL,
	other_biopsy_date timestamp(0) NULL,
	other_biopsy_histology_report_id int8 NULL,
	other_biopsy_morphology_id int8 NULL,
	other_biopsy_others text NULL,
	other_biopsy_grade text NULL,
	other_biopsy_hormone_receptor_status_id int8 NULL,
	other_biopsy_her2_neu_id int8 NULL,
	chest_xray_date timestamp(0) NULL,
	chest_xray_report_id int8 NULL,
	chest_xray_summary_id int8 NULL,
	chest_ct_date timestamp(0) NULL,
	chest_ct_report_id int8 NULL,
	chest_ct_summary_id int8 NULL,
	usg_liver_date timestamp(0) NULL,
	usg_liver_summary_id int8 NULL,
	blood_date timestamp(0) NULL,
	blood_fbc_id int8 NULL,
	blood_fbc text NULL,
	blood_fbc_report_id int8 NULL,
	blood_lft_report_id int8 NULL,
	blood_urea_creatinine_report_id int8 NULL,
	bone_scan_date timestamp(0) NULL,
	bone_scan_summary text NULL,
	date_create timestamp(0) NULL,
	user_create varchar(30) NULL,
	date_modify timestamp(0) NULL,
	user_modify varchar(30) NULL,
	stage_breast_location_id int8 NULL,
	stage_breast_date timestamp(0) NULL,
	stage_breast_t_id int8 NULL,
	stage_breast_n_id int8 NULL,
	stage_breast_m_id int8 NULL
);

CREATE TABLE audit.public_cervix_form (
	audit_event bpchar(1) NULL,
	audit_user varchar(30) NULL,
	audit_date_time timestamptz NULL,
	audit_client_ip inet NULL,
	id int8 NULL,
	patient_id int8 NULL,
	departament text NULL,
	parity bool NULL,
	residential_address text NULL,
	pmhx text NULL,
	presenting_complaint text NULL,
	main_physical_clinical_findings text NULL,
	performance_status_ecog_id int8 NULL,
	treatment_decision text NULL,
	colposcopy_date timestamp(0) NULL,
	colposcopy_report_id int8 NULL,
	cervical_biopsy_date timestamp(0) NULL,
	cervical_biopsy_histology text NULL,
	cervical_biopsy_morphology text NULL,
	cervical_biopsy_grade text NULL,
	usg_pelvis_abdomen_date timestamp(0) NULL,
	usg_pelvis_abdomen_site_of_mass_id int8 NULL,
	usg_pelvis_abdomen_size_of_mass text NULL,
	usg_pelvis_abdomen_extensions_id int8 NULL,
	chest_xray_date timestamp(0) NULL,
	chest_xray_report_id int8 NULL,
	chest_xray_summary_id int8 NULL,
	pelvic_mri_date timestamp(0) NULL,
	pelvic_mri_site_of_mass_id int8 NULL,
	pelvic_mri_size_of_mass text NULL,
	pelvic_mri_extensions_id int8 NULL,
	blood_date timestamp(0) NULL,
	blood_fbc_id int8 NULL,
	blood_fbc text NULL,
	blood_lft_report_id int8 NULL,
	blood_urea_creatinine_report_id int8 NULL,
	stage_figo_date timestamp(0) NULL,
	stage_figo_id int8 NULL,
	date_create timestamp(0) NULL,
	user_create varchar(30) NULL,
	date_modify timestamp(0) NULL,
	user_modify varchar(30) NULL,
	stage_figo_i_id int8 NULL,
	stage_figo_ia_id int8 NULL,
	stage_figo_ib_id int8 NULL,
	stage_figo_ii_id int8 NULL,
	stage_figo_iii_id int8 NULL,
	stage_figo_iv_id int8 NULL
);

CREATE OR REPLACE FUNCTION public.audit_breast_form()
 RETURNS trigger
 LANGUAGE plpgsql
 SECURITY DEFINER
AS $function$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_breast_form SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_breast_form SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $function$
;



CREATE OR REPLACE FUNCTION public.audit_cervix_form()
 RETURNS trigger
 LANGUAGE plpgsql
 SECURITY DEFINER
AS $function$
 DECLARE 
 __DELETE char(6);
 __INSERT char(6);
 __UPDATE char(6);
 BEGIN   
	__DELETE := 'DELETE';
	__INSERT := 'INSERT';
	__UPDATE := 'UPDATE';
	if ( TG_OP = __DELETE  ) then 
 		INSERT INTO audit.public_cervix_form SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;	
	else    
 		INSERT INTO audit.public_cervix_form SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if; 
 END
 $function$
;



create trigger audit_breast_form_all after
insert or delete or update 
on public.breast_form for each row execute function audit_breast_form();


create trigger audit_cervix_form_all after
insert or delete or update 
on public.cervix_form for each row execute function audit_cervix_form();

