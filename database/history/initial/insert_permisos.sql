---------------------------
-- INSERCIÓN DE PERMISOS --
---------------------------

--Aditional patient information
-- additional_patient_information_get
-- additional_patient_information_update
-- additional_patient_information_delete
-- additional_patient_information_list
-- additional_patient_information_insert
-- additional_patient_information_search
-- patient_view_information
INSERT INTO public.permission (description)
VALUES ('additional_patient_information_get'),
       ('additional_patient_information_update'),
       ('additional_patient_information_delete'),
       ('additional_patient_information_list'),
       ('additional_patient_information_insert'),
       ('additional_patient_information_search'),
       ('patient_view_information');

--Area
-- area_get
-- area_update
-- area_delete
-- area_list
-- area_insert
-- area_search
INSERT INTO public.permission (description)
VALUES ('area_get'),
       ('area_update'),
       ('area_delete'),
       ('area_list'),
       ('area_insert'),
       ('area_search');

--Chemoterapy
--- chemotherapy_get
-- chemotherapy_update
-- chemotherapy_delete
-- chemotherapy_list
-- chemotherapy_insert
-- chemotherapy_search
INSERT INTO public.permission (description)
VALUES ('chemotherapy_get'),
       ('chemotherapy_update'),
       ('chemotherapy_delete'),
       ('chemotherapy_list'),
       ('chemotherapy_insert'),
       ('chemotherapy_search');

--Cie_10
-- cie_10_get
-- cie_10_update
-- cie_10_delete
-- cie_10_list
-- cie_10_insert
-- cie_10_search
INSERT INTO public.permission (description)
VALUES ('cie_10_get'),
       ('cie_10_update'),
       ('cie_10_delete'),
       ('cie_10_list'),
       ('cie_10_insert'),
       ('cie_10_search');

--Cie_o_morfology
-- cie_o_morphology_get
-- cie_o_morphology_update
-- cie_o_morphology_delete
-- cie_o_morphology_list
-- cie_o_morphology_insert
-- cie_o_morphology_search
INSERT INTO public.permission (description)
VALUES ('cie_o_morphology_get'),
       ('cie_o_morphology_update'),
       ('cie_o_morphology_delete'),
       ('cie_o_morphology_list'),
       ('cie_o_morphology_insert'),
       ('cie_o_morphology_search');

--Cie_o_topology
-- cie_o_topography_get
-- cie_o_topography_update
-- cie_o_topography_delete
-- cie_o_topography_list
-- cie_o_topography_insert
-- cie_o_topography_search
INSERT INTO public.permission (description)
VALUES ('cie_o_topography_get'),
       ('cie_o_topography_update'),
       ('cie_o_topography_delete'),
       ('cie_o_topography_list'),
       ('cie_o_topography_insert'),
       ('cie_o_topography_search');

--Cie_o_tumor_location
-- cie_o_tumor_location_get
-- cie_o_tumor_location_update
-- cie_o_tumor_location_delete
-- cie_o_tumor_location_list
-- cie_o_tumor_location_insert
-- cie_o_tumor_location_search
INSERT INTO public.permission (description)
VALUES ('cie_o_tumor_location_get'),
       ('cie_o_tumor_location_update'),
       ('cie_o_tumor_location_delete'),
       ('cie_o_tumor_location_list'),
       ('cie_o_tumor_location_insert'),
       ('cie_o_tumor_location_search');

--City
-- city_get
-- city_update
-- city_delete
-- city_list
-- city_insert
-- city_search
INSERT INTO public.permission (description)
VALUES ('city_get'),
       ('city_update'),
       ('city_delete'),
       ('city_list'),
       ('city_insert'),
       ('city_search');

--Committee
-- committee_get
-- committee_update
-- committee_delete
-- committee_list
-- committee_insert
-- committee_search
INSERT INTO public.permission (description)
VALUES ('committee_get'),
       ('committee_update'),
       ('committee_delete'),
       ('committee_list'),
       ('committee_insert'),
       ('committee_search');

--Country
-- country_get
-- country_update
-- country_delete
-- country_list
-- country_insert
-- country_search
INSERT INTO public.permission (description)
VALUES ('country_get'),
       ('country_update'),
       ('country_delete'),
       ('country_list'),
       ('country_insert'),
       ('country_search');

--Deposit
-- deposit_get
-- deposit_update
-- deposit_delete
-- deposit_list
-- deposit_insert
-- deposit_search
INSERT INTO public.permission (description)
VALUES ('deposit_get'),
       ('deposit_update'),
       ('deposit_delete'),
       ('deposit_list'),
       ('deposit_insert'),
       ('deposit_search');

--Deposit Movement
-- deposit_movement_get
-- deposit_movement_update
-- deposit_movement_delete
-- deposit_movement_list
-- deposit_movement_insert
-- deposit_movement_search
INSERT INTO public.permission (description)
VALUES ('deposit_movement_get'),
       ('deposit_movement_update'),
       ('deposit_movement_delete'),
       ('deposit_movement_list'),
       ('deposit_movement_insert'),
       ('deposit_movement_search');

--Deposit_stock
-- deposit_stock_get
-- deposit_stock_update
-- deposit_stock_delete
-- deposit_stock_list
-- deposit_stock_insert
-- deposit_stock_search
INSERT INTO public.permission (description)
VALUES ('deposit_stock_get'),
       ('deposit_stock_update'),
       ('deposit_stock_delete'),
       ('deposit_stock_list'),
       ('deposit_stock_insert'),
       ('deposit_stock_search');

--Diagnosis
-- diagnosis_get
-- diagnosis_update
-- diagnosis_delete
-- diagnosis_list
-- diagnosis_insert
-- diagnosis_search
INSERT INTO public.permission (description)
VALUES ('diagnosis_get'),
       ('diagnosis_update'),
       ('diagnosis_delete'),
       ('diagnosis_list'),
       ('diagnosis_insert'),
       ('diagnosis_search');

--DiagnosisAp
-- diagnosis_ap_get
-- diagnosis_ap_update
-- diagnosis_ap_delete
-- diagnosis_ap_list
-- diagnosis_ap_insert
-- diagnosis_ap_search
INSERT INTO public.permission (description)
VALUES ('diagnosis_ap_get'),
       ('diagnosis_ap_update'),
       ('diagnosis_ap_delete'),
       ('diagnosis_ap_list'),
       ('diagnosis_ap_insert'),
       ('diagnosis_ap_search');

--Dispatch_medications
-- dispatch_medications_get
-- dispatch_medications_update
-- dispatch_medications_delete
-- dispatch_medications_list
-- dispatch_medications_insert
-- dispatch_medications_search
INSERT INTO public.permission (description)
VALUES ('dispatch_medications_get'),
       ('dispatch_medications_update'),
       ('dispatch_medications_delete'),
       ('dispatch_medications_list'),
       ('dispatch_medications_insert'),
       ('dispatch_medications_search');

--Doctor
-- doctor_get
-- doctor_update
-- doctor_delete
-- doctor_list
-- doctor_insert
-- doctor_search
INSERT INTO public.permission (description)
VALUES ('doctor_get'),
       ('doctor_update'),
       ('doctor_delete'),
       ('doctor_list'),
       ('doctor_insert'),
       ('doctor_search');

--Document_type
-- document_type_get
-- document_type_update
-- document_type_delete
-- document_type_list
-- document_type_insert
-- document_type_search
INSERT INTO public.permission (description)
VALUES ('document_type_get'),
       ('document_type_update'),
       ('document_type_delete'),
       ('document_type_list'),
       ('document_type_insert'),
       ('document_type_search');

--Gender
-- gender_get
-- gender_update
-- gender_delete
-- gender_list
-- gender_insert
-- gender_search
INSERT INTO public.permission (description)
VALUES ('gender_get'),
       ('gender_update'),
       ('gender_delete'),
       ('gender_list'),
       ('gender_insert'),
       ('gender_search');

--History
-- history_get
-- history_update
-- history_delete
-- history_list
-- history_insert
-- history_search
INSERT INTO public.permission (description)
VALUES ('history_get'),
       ('history_update'),
       ('history_delete'),
       ('history_list'),
       ('history_insert'),
       ('history_search');

--Hospital
-- hospital_get
-- hospital_update
-- hospital_delete
-- hospital_list
-- hospital_insert
-- hospital_search
INSERT INTO public.permission (description)
VALUES ('hospital_get'),
       ('hospital_update'),
       ('hospital_delete'),
       ('hospital_list'),
       ('hospital_insert'),
       ('hospital_search');

--Lot
-- lot_get
-- lot_update
-- lot_delete
-- lot_list
-- lot_insert
-- lot_search
INSERT INTO public.permission (description)
VALUES ('lot_get'),
       ('lot_update'),
       ('lot_delete'),
       ('lot_list'),
       ('lot_insert'),
       ('lot_search');

--Lot_detail
-- lot_detail_get
-- lot_detail_update
-- lot_detail_delete
-- lot_detail_list
-- lot_detail_insert
-- lot_detail_search
INSERT INTO public.permission (description)
VALUES ('lot_detail_get'),
       ('lot_detail_update'),
       ('lot_detail_delete'),
       ('lot_detail_list'),
       ('lot_detail_insert'),
       ('lot_detail_search');

--Manufacturer
-- manufacturer_get
-- manufacturer_update
-- manufacturer_delete
-- manufacturer_list
-- manufacturer_insert
-- manufacturer_search
INSERT INTO public.permission (description)
VALUES ('manufacturer_get'),
       ('manufacturer_update'),
       ('manufacturer_delete'),
       ('manufacturer_list'),
       ('manufacturer_insert'),
       ('manufacturer_search');

--Medical_committee
-- medical_committee_get
-- medical_committee_update
-- medical_committee_delete
-- medical_committee_list
-- medical_committee_insert
-- medical_committee_search
INSERT INTO public.permission (description)
VALUES ('medical_committee_get'),
       ('medical_committee_update'),
       ('medical_committee_delete'),
       ('medical_committee_list'),
       ('medical_committee_insert'),
       ('medical_committee_search');

--Medical_document
-- medical_document_get
-- medical_document_update
-- medical_document_delete
-- medical_document_list
-- medical_document_insert
-- medical_document_search
INSERT INTO public.permission (description)
VALUES ('medical_document_get'),
       ('medical_document_update'),
       ('medical_document_delete'),
       ('medical_document_list'),
       ('medical_document_insert'),
       ('medical_document_search');

--Medical_document_type
-- medical_document_type_get
-- medical_document_type_update
-- medical_document_type_delete
-- medical_document_type_list
-- medical_document_type_insert
-- medical_document_tyep_search
INSERT INTO public.permission (description)
VALUES ('medical_document_type_get'),
       ('medical_document_type_update'),
       ('medical_document_type_delete'),
       ('medical_document_type_list'),
       ('medical_document_type_insert'),
       ('medical_document_tyep_search');

--Medical_team
-- medical_team_get
-- medical_team_update
-- medical_team_delete
-- medical_team_list
-- medical_team_insert
-- medical_team_search
INSERT INTO public.permission (description)
VALUES ('medical_team_get'),
       ('medical_team_update'),
       ('medical_team_delete'),
       ('medical_team_list'),
       ('medical_team_insert'),
       ('medical_team_search');

--Medical_visit
-- medical_visit_get
-- medical_visit_update
-- medical_visit_delete
-- medical_visit_list
-- medical_visit_insert
-- medical_visit_search
INSERT INTO public.permission (description)
VALUES ('medical_visit_get'),
       ('medical_visit_update'),
       ('medical_visit_delete'),
       ('medical_visit_list'),
       ('medical_visit_insert'),
       ('medical_visit_search');

--Medication
-- medication_get
-- medication_update
-- medication_delete
-- medication_list
-- medication_insert
-- medication_search
INSERT INTO public.permission (description)
VALUES ('medication_get'),
       ('medication_update'),
       ('medication_delete'),
       ('medication_list'),
       ('medication_insert'),
       ('medication_search');

--Medication_order
-- medication_order_get
-- medication_order_update
-- medication_order_delete
-- medication_order_list
-- medication_order_insert
-- medication_order_search
INSERT INTO public.permission (description)
VALUES ('medication_order_get'),
       ('medication_order_update'),
       ('medication_order_delete'),
       ('medication_order_list'),
       ('medication_order_insert'),
       ('medication_order_search');

--Medicine
-- medicine_get
-- medicine_update
-- medicine_delete
-- medicine_list
-- medicine_insert
-- medicine_search
INSERT INTO public.permission (description)
VALUES ('medicine_get'),
       ('medicine_update'),
       ('medicine_delete'),
       ('medicine_list'),
       ('medicine_insert'),
       ('medicine_search');

--Medicine_medication_order
-- medicine_medication_order_get
-- medicine_medication_order_update
-- medicine_medication_order_delete
-- medicine_medication_order_list
-- medicine_medication_order_insert
-- medicine_medication_order_search
INSERT INTO public.permission (description)
VALUES ('medicine_medication_order_get'),
       ('medicine_medication_order_update'),
       ('medicine_medication_order_delete'),
       ('medicine_medication_order_list'),
       ('medicine_medication_order_insert'),
       ('medicine_medication_order_search');

--Medicine_treatment_order
-- medicine_treatment_order_get
-- medicine_treatment_order_update
-- medicine_treatment_order_delete
-- medicine_treatment_order_list
-- medicine_treatment_order_insert
-- medicine_treatment_order_search
INSERT INTO public.permission (description)
VALUES ('medicine_treatment_order_get'),
       ('medicine_treatment_order_update'),
       ('medicine_treatment_order_delete'),
       ('medicine_treatment_order_list'),
       ('medicine_treatment_order_insert'),
       ('medicine_treatment_order_search');

--Menopausal_state
-- menopausal_state_get
-- menopausal_state_update
-- menopausal_state_delete
-- menopausal_state_list
-- menopausal_state_insert
-- menopausal_state_search
INSERT INTO public.permission (description)
VALUES ('menopausal_state_get'),
       ('menopausal_state_update'),
       ('menopausal_state_delete'),
       ('menopausal_state_list'),
       ('menopausal_state_insert'),
       ('menopausal_state_search');

--Parameter
-- parameter_get
-- parameter_update
-- parameter_delete
-- parameter_list
-- parameter_insert
-- parameter_search
INSERT INTO public.permission (description)
VALUES ('parameter_get'),
       ('parameter_update'),
       ('parameter_delete'),
       ('parameter_list'),
       ('parameter_insert'),
       ('parameter_search');

--Patient
-- patient_get
-- patient_update
-- patient_delete
-- patient_list
-- patient_insert
-- patient_search
-- patient_service_cedula
INSERT INTO public.permission (description)
VALUES --('patient_get'),
--        ('patient_update'),
--        ('patient_delete'),
--        ('patient_list'),
--        ('patient_insert'),
--        ('patient_search'),
       ('patient_service_cedula');

--PatientExclusionCriteria
-- patient_exclusion_criteria_get
-- patient_exclusion_criteria_update
-- patient_exclusion_criteria_delete
-- patient_exclusion_criteria_list
-- patient_exclusion_criteria_insert
-- patient_exclusion_criteria_search
INSERT INTO public.permission (description)
VALUES ('patient_exclusion_criteria_get'),
       ('patient_exclusion_criteria_update'),
       ('patient_exclusion_criteria_delete'),
       ('patient_exclusion_criteria_list'),
       ('patient_exclusion_criteria_insert'),
       ('patient_exclusion_criteria_search');

--PatientInclusionCriteriaAdjuvantTrastuzumab
-- patient_inclusion_criteria_adjuvant_trastuzumab_get
-- patient_inclusion_criteria_adjuvant_trastuzumab_update
-- patient_inclusion_criteria_adjuvant_trastuzumab_delete
-- patient_inclusion_criteria_adjuvant_trastuzumab_list
-- patient_inclusion_criteria_adjuvant_trastuzumab_insert
-- patient_inclusion_criteria_adjuvant_trastuzumab_search
INSERT INTO public.permission (description)
VALUES ('patient_inclusion_criteria_adjuvant_trastuzumab_get'),
       ('patient_inclusion_criteria_adjuvant_trastuzumab_update'),
       ('patient_inclusion_criteria_adjuvant_trastuzumab_delete'),
       ('patient_inclusion_criteria_adjuvant_trastuzumab_list'),
       ('patient_inclusion_criteria_adjuvant_trastuzumab_insert'),
       ('patient_inclusion_criteria_adjuvant_trastuzumab_search');

--PatientInclusionCriteriaNeoadjuvantTrastuzumab
-- patient_inclusion_criteria_neoadjuvant_trastuzumab_get
-- patient_inclusion_criteria_neoadjuvant_trastuzumab_update
-- patient_inclusion_criteria_neoadjuvant_trastuzumab_delete
-- patient_inclusion_criteria_neoadjuvant_trastuzumab_list
-- patient_inclusion_criteria_neoadjuvant_trastuzumab_insert
-- patient_inclusion_criteria_neoadjuvant_trastuzumab_search
INSERT INTO public.permission (description)
VALUES ('patient_inclusion_criteria_neoadjuvant_trastuzumab_get'),
       ('patient_inclusion_criteria_neoadjuvant_trastuzumab_update'),
       ('patient_inclusion_criteria_neoadjuvant_trastuzumab_delete'),
       ('patient_inclusion_criteria_neoadjuvant_trastuzumab_list'),
       ('patient_inclusion_criteria_neoadjuvant_trastuzumab_insert'),
       ('patient_inclusion_criteria_neoadjuvant_trastuzumab_search');

--Periodicity
-- periodicity_get
-- periodicity_update
-- periodicity_delete
-- periodicity_list
-- periodicity_insert
-- periodicity_search
INSERT INTO public.permission (description)
VALUES ('periodicity_get'),
       ('periodicity_update'),
       ('periodicity_delete'),
       ('periodicity_list'),
       ('periodicity_insert'),
       ('periodicity_search');

--Permission
-- permission_get
-- permission_update
-- permission_delete
-- permission_list
-- permission_insert
-- permission_search
INSERT INTO public.permission (description)
VALUES ('permission_get'),
       ('permission_update'),
       ('permission_delete'),
       ('permission_list'),
       ('permission_insert'),
       ('permission_search');

--Puncture
-- puncture_get
-- puncture_update
-- puncture_delete
-- puncture_list
-- puncture_insert
-- puncture_search
INSERT INTO public.permission (description)
VALUES ('puncture_get'),
       ('puncture_update'),
       ('puncture_delete'),
       ('puncture_list'),
       ('puncture_insert'),
       ('puncture_search');

--Radiotherapy
-- radiotherapy_get
-- radiotherapy_update
-- radiotherapy_delete
-- radiotherapy_list
-- radiotherapy_insert
-- radiotherapy_search
INSERT INTO public.permission (description)
VALUES ('radiotherapy_get'),
       ('radiotherapy_update'),
       ('radiotherapy_delete'),
       ('radiotherapy_list'),
       ('radiotherapy_insert'),
       ('radiotherapy_search');

--Role
-- role_get
-- role_update
-- role_delete
-- role_list
-- role_insert
-- role_search
INSERT INTO public.permission (description)
VALUES ('role_get'),
       ('role_update'),
       ('role_delete'),
       ('role_list'),
       ('role_insert'),
       ('role_search');

--RolePermission
-- role_permission_get
-- role_permission_update
-- role_permission_delete
-- role_permission_list
-- role_permission_insert
-- role_permission_search
INSERT INTO public.permission (description)
VALUES ('role_permission_get'),
       ('role_permission_update'),
       ('role_permission_delete'),
       ('role_permission_list'),
       ('role_permission_insert'),
       ('role_permission_search');

--Stock
-- stock_get
-- stock_update
-- stock_delete
-- stock_list
-- stock_insert
-- stock_search
INSERT INTO public.permission (description)
VALUES ('stock_get'),
       ('stock_update'),
       ('stock_delete'),
       ('stock_list'),
       ('stock_insert'),
       ('stock_search');

--Supplier
-- supplier_get
-- supplier_update
-- supplier_delete
-- supplier_list
-- supplier_insert
-- supplier_search
INSERT INTO public.permission (description)
VALUES ('supplier_get'),
       ('supplier_update'),
       ('supplier_delete'),
       ('supplier_list'),
       ('supplier_insert'),
       ('supplier_search');

--Surgery
-- surgery_get
-- surgery_update
-- surgery_delete
-- surgery_list
-- surgery_insert
-- surgery_search
INSERT INTO public.permission (description)
VALUES ('surgery_get'),
       ('surgery_update'),
       ('surgery_delete'),
       ('surgery_list'),
       ('surgery_insert'),
       ('surgery_search');

--TreatmentOrder
-- treatment_order_get
-- treatment_order_update
-- treatment_order_delete
-- treatment_order_list
-- treatment_order_insert
-- treatment_order_search
INSERT INTO public.permission (description)
VALUES ('treatment_order_get'),
       ('treatment_order_update'),
       ('treatment_order_delete'),
       ('treatment_order_list'),
       ('treatment_order_insert'),
       ('treatment_order_search');

--TypeTreatment
-- type_treatment_get
-- type_treatment_update
-- type_treatment_delete
-- type_treatment_list
-- type_treatment_insert
-- type_treatment_search
INSERT INTO public.permission (description)
VALUES ('type_treatment_get'),
       ('type_treatment_update'),
       ('type_treatment_delete'),
       ('type_treatment_list'),
       ('type_treatment_insert'),
       ('type_treatment_search');

--User
-- user_get
-- user_update
-- user_delete
-- user_list
-- user_insert
-- user_search
INSERT INTO public.permission (description)
VALUES ('user_get'),
       ('user_update'),
       ('user_delete'),
       ('user_list'),
       ('user_insert'),
       ('user_search');

--UserHospital
-- user_hospital_get
-- user_hospital_update
-- user_hospital_delete
-- user_hospital_list
-- user_hospital_insert
-- user_hospital_search
INSERT INTO public.permission (description)
VALUES ('user_hospital_get'),
       ('user_hospital_update'),
       ('user_hospital_delete'),
       ('user_hospital_list'),
       ('user_hospital_insert'),
       ('user_hospital_search');

------------------------
-- INSERCIÓN DE ROLES --
------------------------
INSERT INTO public.role (description)
VALUES --('MEDICO'),
       --('ENFERMERIA'),
       ('ADMINISTRADOR'),
       ('AUDITOR'),
       ('INVENTARIO');

-----------------------------------
-- INSERCIÓN DE ROLES Y PERMISOS --
-----------------------------------
-- MEDICO
INSERT INTO role_permission (role_id, permission_id)
SELECT (SELECT id FROM role WHERE description = 'MEDICO'),
       id
FROM permission
WHERE description IN ('general',
                      'patient_get',
                      'patient_list',
                      'patient_update',
                      'patient_delete',
                      'patient_search',
                      'patient_insert',
                      'patient_service_cedula',
                      'additional_patient_information_get',
                      'additional_patient_information_update',
                      'additional_patient_information_delete',
                      'additional_patient_information_list',
                      'additional_patient_information_insert',
                      'additional_patient_information_search',
                      'chemotherapy_get',
                      'chemotherapy_update',
                      'chemotherapy_delete',
                      'chemotherapy_list',
                      'chemotherapy_insert',
                      'chemotherapy_search',
                      'committee_get',
                      'committee_update',
                      'committee_delete',
                      'committee_list',
                      'committee_insert',
                      'committee_search',
                      'diagnosis_get',
                      'diagnosis_update',
                      'diagnosis_delete',
                      'diagnosis_list',
                      'diagnosis_insert',
                      'diagnosis_search',
                      'diagnosis_ap_get',
                      'diagnosis_ap_update',
                      'diagnosis_ap_delete',
                      'diagnosis_ap_list',
                      'diagnosis_ap_insert',
                      'diagnosis_ap_search',
                      'doctor_get',
                      'doctor_update',
                      'doctor_delete',
                      'doctor_list',
                      'doctor_insert',
                      'doctor_search',
                      'document_type_get',
                      'document_type_update',
                      'document_type_delete',
                      'document_type_list',
                      'document_type_insert',
                      'document_type_search',
                      'history_get',
                      'history_update',
                      'history_delete',
                      'history_list',
                      'history_insert',
                      'history_search',
                      'hospital_get',
                      'hospital_list',
                      'hospital_search',
                      'medical_committee_get',
                      'medical_committee_list',
                      'medical_committee_search',
                      'medical_document_get',
                      'medical_document_update',
                      'medical_document_delete',
                      'medical_document_list',
                      'medical_document_insert',
                      'medical_document_search',
                      'medical_document_type_get',
                      'medical_document_type_update',
                      'medical_document_type_delete',
                      'medical_document_type_list',
                      'medical_document_type_insert',
                      'medical_document_tyep_search',
                      'medical_team_get',
                      'medical_team_list',
                      'medical_team_search',
                      'medical_visit_get',
                      'medical_visit_update',
                      'medical_visit_delete',
                      'medical_visit_list',
                      'medical_visit_insert',
                      'medical_visit_search',
                      'medication_get',
                      'medication_update',
                      'medication_delete',
                      'medication_list',
                      'medication_insert',
                      'medication_search',
                      'medication_order_get',
                      'medication_order_update',
                      'medication_order_delete',
                      'medication_order_list',
                      'medication_order_insert',
                      'medication_order_search',
                      'medicine_get',
                      'medicine_update',
                      'medicine_delete',
                      'medicine_list',
                      'medicine_insert',
                      'medicine_search',
                      'medicine_medication_order_get',
                      'medicine_medication_order_update',
                      'medicine_medication_order_delete',
                      'medicine_medication_order_list',
                      'medicine_medication_order_insert',
                      'medicine_medication_order_search',
                      'medicine_treatment_order_get',
                      'medicine_treatment_order_update',
                      'medicine_treatment_order_delete',
                      'medicine_treatment_order_list',
                      'medicine_treatment_order_insert',
                      'medicine_treatment_order_search',
                      'menopausal_state_get',
                      'menopausal_state_update',
                      'menopausal_state_delete',
                      'menopausal_state_list',
                      'menopausal_state_insert',
                      'menopausal_state_search',
                      'patient_exclusion_criteria_get',
                      'patient_exclusion_criteria_update',
                      'patient_exclusion_criteria_delete',
                      'patient_exclusion_criteria_list',
                      'patient_exclusion_criteria_insert',
                      'patient_exclusion_criteria_search',
                      'patient_inclusion_criteria_adjuvant_trastuzumab_get',
                      'patient_inclusion_criteria_adjuvant_trastuzumab_update',
                      'patient_inclusion_criteria_adjuvant_trastuzumab_delete',
                      'patient_inclusion_criteria_adjuvant_trastuzumab_list',
                      'patient_inclusion_criteria_adjuvant_trastuzumab_insert',
                      'patient_inclusion_criteria_adjuvant_trastuzumab_search',
                      'patient_inclusion_criteria_neoadjuvant_trastuzumab_get',
                      'patient_inclusion_criteria_neoadjuvant_trastuzumab_update',
                      'patient_inclusion_criteria_neoadjuvant_trastuzumab_delete',
                      'patient_inclusion_criteria_neoadjuvant_trastuzumab_list',
                      'patient_inclusion_criteria_neoadjuvant_trastuzumab_insert',
                      'patient_inclusion_criteria_neoadjuvant_trastuzumab_search',
                      'puncture_get',
                      'puncture_update',
                      'puncture_delete',
                      'puncture_list',
                      'puncture_insert',
                      'puncture_search',
                      'radiotherapy_get',
                      'radiotherapy_update',
                      'radiotherapy_delete',
                      'radiotherapy_list',
                      'radiotherapy_insert',
                      'radiotherapy_search',
                      'surgery_get',
                      'surgery_update',
                      'surgery_delete',
                      'surgery_list',
                      'surgery_insert',
                      'surgery_search',
                      'treatment_order_get',
                      'treatment_order_update',
                      'treatment_order_delete',
                      'treatment_order_list',
                      'treatment_order_insert',
                      'treatment_order_search',
                      'type_treatment_get',
                      'type_treatment_update',
                      'type_treatment_delete',
                      'type_treatment_list',
                      'type_treatment_insert',
                      'type_treatment_search',
                      'patient_view_information');

--ENFERMERIA

INSERT INTO role_permission (role_id, permission_id)
SELECT (SELECT id FROM role WHERE description = 'ENFERMERIA'),
       id
FROM permission
WHERE description IN ('general',
                      'patient_get',
                      'patient_list',
                      'patient_update',
                      'patient_delete',
                      'patient_search',
                      'patient_insert',
                      'patient_service_cedula',
                      'additional_patient_information_get',
                      'additional_patient_information_update',
                      'additional_patient_information_delete',
                      'additional_patient_information_list',
                      'additional_patient_information_insert',
                      'additional_patient_information_search',
                      'area_get',
                      'area_update',
                      'area_delete',
                      'area_list',
                      'area_insert',
                      'area_search',
                      'chemotherapy_get',
                      'chemotherapy_update',
                      'chemotherapy_delete',
                      'chemotherapy_list',
                      'chemotherapy_insert',
                      'chemotherapy_search',
                      'cie_10_get',
                      'cie_10_update',
                      'cie_10_delete',
                      'cie_10_list',
                      'cie_10_insert',
                      'cie_10_search',
                      'cie_o_morphology_get',
                      'cie_o_morphology_update',
                      'cie_o_morphology_delete',
                      'cie_o_morphology_list',
                      'cie_o_morphology_insert',
                      'cie_o_morphology_search',
                      'cie_o_topography_get',
                      'cie_o_topography_update',
                      'cie_o_topography_delete',
                      'cie_o_topography_list',
                      'cie_o_topography_insert',
                      'cie_o_topography_search',
                      'cie_o_tumor_location_get',
                      'cie_o_tumor_location_update',
                      'cie_o_tumor_location_delete',
                      'cie_o_tumor_location_list',
                      'cie_o_tumor_location_insert',
                      'cie_o_tumor_location_search',
                      'city_get',
                      'city_update',
                      'city_delete',
                      'city_list',
                      'city_insert',
                      'city_search',
                      'committee_get',
                      'committee_update',
                      'committee_delete',
                      'committee_list',
                      'committee_insert',
                      'committee_search',
                      'country_get',
                      'country_update',
                      'country_delete',
                      'country_list',
                      'country_insert',
                      'country_search',
                      'diagnosis_get',
                      'diagnosis_update',
                      'diagnosis_delete',
                      'diagnosis_list',
                      'diagnosis_insert',
                      'diagnosis_search',
                      'diagnosis_ap_get',
                      'diagnosis_ap_update',
                      'diagnosis_ap_delete',
                      'diagnosis_ap_list',
                      'diagnosis_ap_insert',
                      'diagnosis_ap_search',
                      'dispatch_medications_get',
                      'dispatch_medications_update',
                      'dispatch_medications_delete',
                      'dispatch_medications_list',
                      'dispatch_medications_insert',
                      'dispatch_medications_search',
                      'doctor_get',
                      'doctor_update',
                      'doctor_delete',
                      'doctor_list',
                      'doctor_insert',
                      'doctor_search',
                      'document_type_get',
                      'document_type_update',
                      'document_type_delete',
                      'document_type_list',
                      'document_type_insert',
                      'document_type_search',
                      'gender_get',
                      'gender_update',
                      'gender_delete',
                      'gender_list',
                      'gender_insert',
                      'gender_search',
                      'history_get',
                      'history_update',
                      'history_delete',
                      'history_list',
                      'history_insert',
                      'history_search',
                      'hospital_get',
                      'hospital_list',
                      'hospital_search',
                      'medical_committee_get',
                      'medical_committee_update',
                      'medical_committee_delete',
                      'medical_committee_list',
                      'medical_committee_insert',
                      'medical_committee_search',
                      'medical_document_get',
                      'medical_document_update',
                      'medical_document_delete',
                      'medical_document_list',
                      'medical_document_insert',
                      'medical_document_search',
                      'medical_document_type_get',
                      'medical_document_type_update',
                      'medical_document_type_delete',
                      'medical_document_type_list',
                      'medical_document_type_insert',
                      'medical_document_tyep_search',
                      'medical_team_get',
                      'medical_team_update',
                      'medical_team_delete',
                      'medical_team_list',
                      'medical_team_insert',
                      'medical_team_search',
                      'medical_visit_get',
                      'medical_visit_update',
                      'medical_visit_delete',
                      'medical_visit_list',
                      'medical_visit_insert',
                      'medical_visit_search',
                      'medication_get',
                      'medication_update',
                      'medication_delete',
                      'medication_list',
                      'medication_insert',
                      'medication_search',
                      'medication_order_get',
                      'medication_order_update',
                      'medication_order_delete',
                      'medication_order_list',
                      'medication_order_insert',
                      'medication_order_search',
                      'medicine_get',
                      'medicine_update',
                      'medicine_delete',
                      'medicine_list',
                      'medicine_insert',
                      'medicine_search',
                      'medicine_medication_order_get',
                      'medicine_medication_order_update',
                      'medicine_medication_order_delete',
                      'medicine_medication_order_list',
                      'medicine_medication_order_insert',
                      'medicine_medication_order_search',
                      'medicine_treatment_order_get',
                      'medicine_treatment_order_update',
                      'medicine_treatment_order_delete',
                      'medicine_treatment_order_list',
                      'medicine_treatment_order_insert',
                      'medicine_treatment_order_search',
                      'menopausal_state_get',
                      'menopausal_state_update',
                      'menopausal_state_delete',
                      'menopausal_state_list',
                      'menopausal_state_insert',
                      'menopausal_state_search',
                      'parameter_get',
                      'parameter_list',
                      'parameter_search',
                      'patient_exclusion_criteria_get',
                      'patient_exclusion_criteria_update',
                      'patient_exclusion_criteria_delete',
                      'patient_exclusion_criteria_list',
                      'patient_exclusion_criteria_insert',
                      'patient_exclusion_criteria_search',
                      'patient_inclusion_criteria_adjuvant_trastuzumab_get',
                      'patient_inclusion_criteria_adjuvant_trastuzumab_update',
                      'patient_inclusion_criteria_adjuvant_trastuzumab_delete',
                      'patient_inclusion_criteria_adjuvant_trastuzumab_list',
                      'patient_inclusion_criteria_adjuvant_trastuzumab_insert',
                      'patient_inclusion_criteria_adjuvant_trastuzumab_search',
                      'patient_inclusion_criteria_neoadjuvant_trastuzumab_get',
                      'patient_inclusion_criteria_neoadjuvant_trastuzumab_update',
                      'patient_inclusion_criteria_neoadjuvant_trastuzumab_delete',
                      'patient_inclusion_criteria_neoadjuvant_trastuzumab_list',
                      'patient_inclusion_criteria_neoadjuvant_trastuzumab_insert',
                      'patient_inclusion_criteria_neoadjuvant_trastuzumab_search',
                      'periodicity_get',
                      'periodicity_update',
                      'periodicity_delete',
                      'periodicity_list',
                      'periodicity_insert',
                      'periodicity_search',
                      'puncture_get',
                      'puncture_update',
                      'puncture_delete',
                      'puncture_list',
                      'puncture_insert',
                      'puncture_search',
                      'radiotherapy_get',
                      'radiotherapy_update',
                      'radiotherapy_delete',
                      'radiotherapy_list',
                      'radiotherapy_insert',
                      'radiotherapy_search',
                      'surgery_get',
                      'surgery_update',
                      'surgery_delete',
                      'surgery_list',
                      'surgery_insert',
                      'surgery_search',
                      'treatment_order_get',
                      'treatment_order_update',
                      'treatment_order_delete',
                      'treatment_order_list',
                      'treatment_order_insert',
                      'treatment_order_search',
                      'type_treatment_get',
                      'type_treatment_update',
                      'type_treatment_delete',
                      'type_treatment_list',
                      'type_treatment_insert',
                      'type_treatment_search',
                      'patient_view_information');

-- INVENTARIO
INSERT INTO role_permission (role_id, permission_id)
SELECT (SELECT id FROM role WHERE description = 'INVENTARIO'),
       id
FROM permission
WHERE description IN ('general',
                      'deposit_get',
                      'deposit_update',
                      'deposit_delete',
                      'deposit_list',
                      'deposit_insert',
                      'deposit_search',
                      'deposit_movement_get',
                      'deposit_movement_update',
                      'deposit_movement_delete',
                      'deposit_movement_list',
                      'deposit_movement_insert',
                      'deposit_movement_search',
                      'deposit_stock_get',
                      'deposit_stock_update',
                      'deposit_stock_delete',
                      'deposit_stock_list',
                      'deposit_stock_insert',
                      'deposit_stock_search',
                      'dispatch_medications_get',
                      'dispatch_medications_update',
                      'dispatch_medications_delete',
                      'dispatch_medications_list',
                      'dispatch_medications_insert',
                      'dispatch_medications_search',
                      'hospital_get',
                      'hospital_list',
                      'hospital_search',
                      'lot_get',
                      'lot_update',
                      'lot_delete',
                      'lot_list',
                      'lot_insert',
                      'lot_search',
                      'lot_detail_get',
                      'lot_detail_update',
                      'lot_detail_delete',
                      'lot_detail_list',
                      'lot_detail_insert',
                      'lot_detail_search',
                      'manufacturer_get',
                      'manufacturer_update',
                      'manufacturer_delete',
                      'manufacturer_list',
                      'manufacturer_insert',
                      'manufacturer_search',
                      'stock_get',
                      'stock_update',
                      'stock_delete',
                      'stock_list',
                      'stock_insert',
                      'stock_search',
                      'supplier_get',
                      'supplier_update',
                      'supplier_delete',
                      'supplier_list',
                      'supplier_insert',
                      'supplier_search');

--AUDITOR
INSERT INTO role_permission (role_id, permission_id)
SELECT (SELECT id FROM role WHERE description = 'AUDITOR'),
       id
FROM permission
WHERE description IN ('general',
                      'patient_search',
                      'chemotherapy_search',
                      'cie_10_search',
                      'cie_o_morphology_search',
                      'committee_search',
                      'deposit_search',
                      'deposit_movement_search',
                      'deposit_stock_list',
                      'deposit_stock_search',
                      'diagnosis_search',
                      'diagnosis_ap_search',
                      'dispatch_medications_search',
                      'doctor_search',
                      'document_type_search',
                      'gender_search',
                      'history_list',
                      'history_search',
                      'hospital_get',
                      'hospital_list',
                      'hospital_search',
                      'lot_search',
                      'manufacturer_search',
                      'medical_document_search',
                      'medical_document_tyep_search',
                      'medical_visit_get',
                      'medical_visit_list',
                      'medical_visit_search',
                      'medication_order_search',
                      'medicine_search',
                      'menopausal_state_get',
                      'menopausal_state_list',
                      'menopausal_state_search',
                      'parameter_search',
                      'patient_exclusion_criteria_search',
                      'patient_inclusion_criteria_adjuvant_trastuzumab_search',
                      'patient_inclusion_criteria_neoadjuvant_trastuzumab_search',
                      'periodicity_search',
                      'permission_get',
                      'permission_list',
                      'permission_search',
                      'puncture_search',
                      'radiotherapy_search',
                      'role_get',
                      'role_list',
                      'role_search',
                      'role_permission_get',
                      'role_permission_list',
                      'role_permission_search',
                      'stock_search',
                      'supplier_search',
                      'surgery_search',
                      'treatment_order_get',
                      'treatment_order_search',
                      'type_treatment_get',
                      'type_treatment_list',
                      'type_treatment_search',
                      'user_search',
                      'user_hospital_list',
                      'user_hospital_search',
                      'patient_view_information');

--ADMINISTRADOR
INSERT INTO role_permission (role_id, permission_id)
SELECT (SELECT id FROM role WHERE description = 'ADMINISTRADOR'),
       id
FROM permission;
