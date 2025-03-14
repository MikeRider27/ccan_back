--DESACTIVAR TRIGGER

--ESQUEMA INVENTORY
ALTER TABLE inventory.deposit DISABLE TRIGGER audit_deposit_all;
ALTER TABLE inventory.deposit_movement DISABLE TRIGGER audit_deposit_movement_all;
ALTER TABLE inventory.deposit_stock DISABLE TRIGGER audit_deposit_stock_all;
ALTER TABLE inventory.dispatch_medications DISABLE TRIGGER audit_dispatch_medications_all;
ALTER TABLE inventory.entries DISABLE TRIGGER audit_entries_all;
ALTER TABLE inventory.entries_deposit_stock DISABLE TRIGGER audit_entries_deposit_stock_all;
ALTER TABLE inventory.entries_lot DISABLE TRIGGER audit_entries_lot_all;
ALTER TABLE inventory.history DISABLE TRIGGER audit_history_all;
ALTER TABLE inventory.lot DISABLE TRIGGER audit_lot_all;
ALTER TABLE inventory.manufacturer DISABLE TRIGGER audit_manufacturer_all;
ALTER TABLE inventory.stock DISABLE TRIGGER audit_stock_all;
ALTER TABLE inventory.supplier DISABLE TRIGGER audit_supplier_all;

--ESQUEMA PUBLIC
ALTER TABLE public.appointment DISABLE TRIGGER audit_appointment_all;
ALTER TABLE public.appointment_type DISABLE TRIGGER audit_appointment_type_all;
ALTER TABLE public."area" DISABLE TRIGGER audit_area_all;
ALTER TABLE public.chemotherapy DISABLE TRIGGER audit_chemotherapy_all;
ALTER TABLE public.chemotherapy_treatment_plan DISABLE TRIGGER audit_chemotherapy_treatment_plan_all;
ALTER TABLE public.cie_10 DISABLE TRIGGER audit_cie_10_all;
ALTER TABLE public.cie_o_morphology DISABLE TRIGGER audit_cie_o_morphology_all;
ALTER TABLE public.cie_o_topography DISABLE TRIGGER audit_cie_o_topography_all;
ALTER TABLE public.cie_o_tumor_location DISABLE TRIGGER audit_cie_o_tumor_location_all;
ALTER TABLE public.city DISABLE TRIGGER audit_city_all;
ALTER TABLE public.committee DISABLE TRIGGER audit_committee_all;
ALTER TABLE public."configuration" DISABLE TRIGGER audit_configuration_all;
ALTER TABLE public.country DISABLE TRIGGER audit_country_all;
ALTER TABLE public.diagnosis DISABLE TRIGGER audit_diagnosis_all;
ALTER TABLE public.diagnosis_ap DISABLE TRIGGER audit_diagnosis_ap_all;
ALTER TABLE public.doctor DISABLE TRIGGER audit_doctor_all;
ALTER TABLE public.doctor_specialty DISABLE TRIGGER audit_doctor_specialty_all;
ALTER TABLE public.document_type DISABLE TRIGGER audit_document_type_all;
ALTER TABLE public.eps DISABLE TRIGGER audit_eps_all;
ALTER TABLE public.eps_hospital DISABLE TRIGGER audit_eps_hospital_all;
ALTER TABLE public.evaluation DISABLE TRIGGER audit_evaluation_all;
ALTER TABLE public.evaluators DISABLE TRIGGER audit_evaluators_all;
ALTER TABLE public.follow_up_treatment_plan DISABLE TRIGGER audit_follow_up_treatment_plan_all;
ALTER TABLE public.gender DISABLE TRIGGER audit_gender_all;
ALTER TABLE public.history_record DISABLE TRIGGER audit_history_record_all;
ALTER TABLE public.hospital DISABLE TRIGGER audit_hospital_all;
ALTER TABLE public.medical_committee DISABLE TRIGGER audit_medical_committee_all;
ALTER TABLE public.medical_consultation DISABLE TRIGGER audit_medical_consultation_all;
ALTER TABLE public.medical_document DISABLE TRIGGER audit_medical_document_all;
ALTER TABLE public.medical_document_general DISABLE TRIGGER audit_medical_document_general_all;
ALTER TABLE public.medical_document_type DISABLE TRIGGER audit_medical_document_type_all;
ALTER TABLE public.medical_monitoring DISABLE TRIGGER audit_medical_monitoring_all;
ALTER TABLE public.medical_results DISABLE TRIGGER audit_medical_results_all;
ALTER TABLE public.medical_team DISABLE TRIGGER audit_medical_team_all;
ALTER TABLE public.medication_order DISABLE TRIGGER audit_medication_order_all;
ALTER TABLE public.medicine DISABLE TRIGGER audit_medicine_all;
ALTER TABLE public.medicine_chemotherapy DISABLE TRIGGER audit_medicine_chemotherapy_all;
ALTER TABLE public.medicine_medical_consultation DISABLE TRIGGER audit_medicine_medical_consultation_all;
ALTER TABLE public.medicine_treatment_follow_up DISABLE TRIGGER audit_medicine_treatment_follow_up_all;
ALTER TABLE public.medicine_treatment_plan DISABLE TRIGGER audit_medicine_treatment_plan_all;
ALTER TABLE public.menopausal_state DISABLE TRIGGER audit_menopausal_state_all;
ALTER TABLE public."parameter" DISABLE TRIGGER audit_parameter_all;
ALTER TABLE public.patient DISABLE TRIGGER audit_patient_all;
ALTER TABLE public.patient_exclusion_criteria DISABLE TRIGGER audit_patient_exclusion_criteria_all;
ALTER TABLE public.patient_family_with_cancer DISABLE TRIGGER audit_patient_family_with_cancer_all;
ALTER TABLE public.patient_hospital DISABLE TRIGGER audit_patient_hospital_all;
ALTER TABLE public.patient_inclusion_criteria DISABLE TRIGGER audit_patient_inclusion_criteria_all;
ALTER TABLE public.patient_inclusion_criteria_adjuvant_trastuzumab DISABLE TRIGGER audit_patient_inclusion_criteria_adjuvant_trastuzumab_all;
ALTER TABLE public.patient_inclusion_criteria_neoadjuvant_trastuzumab DISABLE TRIGGER audit_patient_inclusion_criteria_neoadjuvant_trastuzumab_all;
ALTER TABLE public.periodicity DISABLE TRIGGER audit_periodicity_all;
ALTER TABLE public."permission" DISABLE TRIGGER audit_permission_all;
ALTER TABLE public.personal_pathological_history DISABLE TRIGGER audit_personal_pathological_history_all;
ALTER TABLE public.previous_studies DISABLE TRIGGER audit_previous_studies_all;
ALTER TABLE public.puncture DISABLE TRIGGER audit_puncture_all;
ALTER TABLE public.radiotherapy DISABLE TRIGGER audit_radiotherapy_all;
ALTER TABLE public.radiotherapy_treatment_plan DISABLE TRIGGER audit_radiotherapy_treatment_plan_all;
ALTER TABLE public."role" DISABLE TRIGGER audit_role_all;
ALTER TABLE public.role_permission DISABLE TRIGGER audit_role_permission_all;
ALTER TABLE public.specialty DISABLE TRIGGER audit_specialty_all;
ALTER TABLE public.surgery DISABLE TRIGGER audit_surgery_all;
ALTER TABLE public.treatment_follow_up DISABLE TRIGGER audit_treatment_follow_up_all;
ALTER TABLE public.treatment_plan DISABLE TRIGGER audit_treatment_plan_all;
ALTER TABLE public.type_treatment DISABLE TRIGGER audit_type_treatment_all;
ALTER TABLE public."user" DISABLE TRIGGER audit_user_all;
ALTER TABLE public.user_hospital DISABLE TRIGGER audit_user_hospital_all;