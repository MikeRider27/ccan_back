-----------------------------------------------------------------------
-- CAMBIOS EN public.patient_inclusion_criteria_adjuvant_trastuzumab --
-----------------------------------------------------------------------
ALTER TABLE public.patient_inclusion_criteria_adjuvant_trastuzumab
    DROP CONSTRAINT patient_inclusion_criteria_adjuvant_trastuzumab_parameter_id_fk;

ALTER TABLE public.patient_inclusion_criteria_adjuvant_trastuzumab
    DROP COLUMN her2_positive_id;

ALTER TABLE public.patient_inclusion_criteria_adjuvant_trastuzumab
    ADD her2_positive_id jsonb;

-----------------------------------------------------------------------
-- CAMBIOS EN public.patient_inclusion_criteria_neoadjuvant_trastuzumab --
-----------------------------------------------------------------------
ALTER TABLE public.patient_inclusion_criteria_neoadjuvant_trastuzumab
    DROP CONSTRAINT inclusion_criteria_neoadjuvant_trastuzumab_parameter_id_fk;

ALTER TABLE public.patient_inclusion_criteria_neoadjuvant_trastuzumab
    DROP COLUMN her2_positive_id;

ALTER TABLE public.patient_inclusion_criteria_neoadjuvant_trastuzumab
    ADD her2_positive_id jsonb;

-- NEW PERMISSION
INSERT INTO public.permission (description)
VALUES ('patient_inclusion_criteria_get'),
       ('patient_inclusion_criteria_update'),
       ('patient_inclusion_criteria_delete'),
       ('patient_inclusion_criteria_list'),
       ('patient_inclusion_criteria_insert'),
       ('patient_inclusion_criteria_search');

INSERT INTO public.permission (description)
VALUES ('patient_evaluation_search');

INSERT INTO public.permission (description)
VALUES ('medical_document_download');

INSERT INTO public.permission (description)
VALUES ('patient_summarize');

INSERT INTO public.permission (description)
VALUES ('menu_patient_registry'),
       ('menu_patient'),
       ('menu_patient_evaluation'),
       ('menu_parameters'),
       ('menu_menopausal_state'),
       ('menu_type_treatment'),
       ('menu_document_type'),
       ('menu_gender'),
       ('menu_periodicity'),
       ('menu_cie_10'),
       ('menu_cie_o_morphology'),
       ('menu_medicine'),
       ('menu_doctor'),
       ('menu_specialty'),
       ('menu_hospital'),
       ('menu_security'),
       ('menu_role_permission'),
       ('menu_user'),
       ('menu_inventory'),
       ('menu_manufacturer'),
       ('menu_supplier'),
       ('menu_deposit'),
       ('menu_lot'),
       ('menu_stock'),
       ('menu_deposit_movement'),
       ('menu_dispatch_medications'),
       ('menu_configuration');

INSERT INTO public.permission (description)
VALUES ('treatment_follow_up_get'),
       ('treatment_follow_up_update'),
       ('treatment_follow_up_delete'),
       ('treatment_follow_up_list'),
       ('treatment_follow_up_insert'),
       ('treatment_follow_up_search');

-- PERMISSIONS AND ROLES
-- MEDICO
-- BORRADO
DELETE
FROM role_permission rp
WHERE rp.id IN (SELECT rp.id
                FROM role
                         JOIN role_permission rp ON role.id = rp.role_id
                         JOIN permission p ON p.id = rp.permission_id
                WHERE role.description = 'MEDICO');
-- INSERCION
INSERT INTO role_permission (role_id, permission_id)
SELECT (SELECT id FROM role WHERE role.description = 'MEDICO'),
       p.id
FROM permission p
WHERE p.description IN (
                        'additional_patient_information_get',
                        'additional_patient_information_update',
                        'additional_patient_information_delete',
                        'additional_patient_information_list',
                        'additional_patient_information_insert',
                        'additional_patient_information_search',
                        'patient_view_information',
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
                        'history_get',
                        'history_update',
                        'history_delete',
                        'history_list',
                        'history_insert',
                        'history_search',
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
                        'medicine_medication_order_get',
                        'medicine_medication_order_update',
                        'medicine_medication_order_delete',
                        'medicine_medication_order_list',
                        'medicine_medication_order_insert',
                        'medicine_medication_order_search',
                        'medicine_treatment_plan_get',
                        'medicine_treatment_plan_update',
                        'medicine_treatment_plan_delete',
                        'medicine_treatment_plan_list',
                        'medicine_treatment_plan_insert',
                        'medicine_treatment_plan_search',
                        'patient_get',
                        'patient_update',
                        'patient_delete',
                        'patient_list',
                        'patient_insert',
                        'patient_search',
                        'patient_service_cedula',
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
                        'treatment_plan_list',
                        'treatment_plan_search',
                        'treatment_plan_get',
                        'treatment_plan_insert',
                        'treatment_plan_update',
                        'treatment_plan_delete',
                        'medical_consultation_list',
                        'medical_consultation_search',
                        'medical_consultation_get',
                        'medical_consultation_insert',
                        'medical_consultation_update',
                        'medical_consultation_delete',
                        'evaluation_list',
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
                        'evaluators_delete',
                        'hospital_list',
                        'menopausal_state_list',
                        'menopausal_state_search',
                        'menopausal_state_get',
                        'type_treatment_get',
                        'type_treatment_list',
                        'type_treatment_search',
                        'document_type_get',
                        'document_type_list',
                        'document_type_search',
                        'medicine_get',
                        'medicine_list',
                        'medicine_search',
                        'doctor_get',
                        'doctor_list',
                        'doctor_search',
                        'doctor_specialty_list',
                        'doctor_specialty_get',
                        'doctor_specialty_search',
                        'hospital_get',
                        'hospital_search',
                        'gender_get',
                        'gender_list',
                        'gender_search',
                        'country_get',
                        'country_list',
                        'country_search',
                        'area_get',
                        'area_list',
                        'area_search',
                        'city_get',
                        'city_list',
                        'city_search',
                        'parameter_get',
                        'parameter_list',
                        'parameter_search',
                        'patient_inclusion_criteria_get',
                        'patient_inclusion_criteria_update',
                        'patient_inclusion_criteria_delete',
                        'patient_inclusion_criteria_list',
                        'patient_inclusion_criteria_insert',
                        'patient_inclusion_criteria_search',
                        'periodicity_get',
                        'periodicity_list',
                        'periodicity_search',
                        'cie_10_get',
                        'cie_10_list',
                        'cie_10_search',
                        'cie_o_morphology_get',
                        'cie_o_morphology_list',
                        'cie_o_morphology_search',
                        'cie_o_topography_get',
                        'cie_o_topography_list',
                        'cie_o_topography_search',
                        'cie_o_tumor_location_get',
                        'cie_o_tumor_location_list',
                        'cie_o_tumor_location_search',
                        'patient_evaluation_search',
                        'user_get',
                        'user_list',
                        'user_search',
                        'user_hospital_get',
                        'user_hospital_list',
                        'user_hospital_search',
                        'role_get',
                        'role_list',
                        'role_search',
                        'role_permission_get',
                        'role_permission_list',
                        'role_permission_search',
                        'permission_get',
                        'permission_list',
                        'permission_search',
                        'menu_patient_registry',
                        'menu_patient',
                        'menu_patient_evaluation',
                        'medical_document_download',
                        'patient_summarize');

-- ENFERMERIA
-- BORRADO
DELETE
FROM role_permission rp
WHERE rp.id IN (SELECT rp.id
                FROM role
                         JOIN role_permission rp ON role.id = rp.role_id
                         JOIN permission p ON p.id = rp.permission_id
                WHERE role.description = 'ENFERMERIA');
-- INSERCION
INSERT INTO role_permission (role_id, permission_id)
SELECT (SELECT id FROM role WHERE role.description = 'ENFERMERIA'),
       p.id
FROM permission p
WHERE p.description IN (
                        'additional_patient_information_get',
                        'additional_patient_information_update',
                        'additional_patient_information_delete',
                        'additional_patient_information_list',
                        'additional_patient_information_insert',
                        'additional_patient_information_search',
                        'patient_view_information',
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
                        'history_get',
                        'history_update',
                        'history_delete',
                        'history_list',
                        'history_insert',
                        'history_search',
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
                        'medicine_medication_order_get',
                        'medicine_medication_order_update',
                        'medicine_medication_order_delete',
                        'medicine_medication_order_list',
                        'medicine_medication_order_insert',
                        'medicine_medication_order_search',
                        'medicine_treatment_plan_get',
                        'medicine_treatment_plan_update',
                        'medicine_treatment_plan_delete',
                        'medicine_treatment_plan_list',
                        'medicine_treatment_plan_insert',
                        'medicine_treatment_plan_search',
                        'patient_get',
                        'patient_update',
                        'patient_delete',
                        'patient_list',
                        'patient_insert',
                        'patient_search',
                        'patient_service_cedula',
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
                        'treatment_plan_list',
                        'treatment_plan_search',
                        'treatment_plan_get',
                        'treatment_plan_insert',
                        'treatment_plan_update',
                        'treatment_plan_delete',
                        'medical_consultation_list',
                        'medical_consultation_search',
                        'medical_consultation_get',
                        'medical_consultation_insert',
                        'medical_consultation_update',
                        'medical_consultation_delete',
                        'evaluation_list',
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
                        'evaluators_delete',
                        'hospital_list',
                        'menopausal_state_list',
                        'menopausal_state_search',
                        'menopausal_state_get',
                        'type_treatment_get',
                        'type_treatment_list',
                        'type_treatment_search',
                        'document_type_get',
                        'document_type_list',
                        'document_type_search',
                        'medicine_get',
                        'medicine_list',
                        'medicine_search',
                        'doctor_get',
                        'doctor_list',
                        'doctor_search',
                        'doctor_specialty_list',
                        'doctor_specialty_get',
                        'doctor_specialty_search',
                        'hospital_get',
                        'hospital_search',
                        'gender_get',
                        'gender_list',
                        'gender_search',
                        'country_get',
                        'country_list',
                        'country_search',
                        'area_get',
                        'area_list',
                        'area_search',
                        'city_get',
                        'city_list',
                        'city_search',
                        'parameter_get',
                        'parameter_list',
                        'parameter_search',
                        'patient_inclusion_criteria_get',
                        'patient_inclusion_criteria_update',
                        'patient_inclusion_criteria_delete',
                        'patient_inclusion_criteria_list',
                        'patient_inclusion_criteria_insert',
                        'patient_inclusion_criteria_search',
                        'periodicity_get',
                        'periodicity_list',
                        'periodicity_search',
                        'cie_10_get',
                        'cie_10_list',
                        'cie_10_search',
                        'cie_o_morphology_get',
                        'cie_o_morphology_list',
                        'cie_o_morphology_search',
                        'cie_o_topography_get',
                        'cie_o_topography_list',
                        'cie_o_topography_search',
                        'cie_o_tumor_location_get',
                        'cie_o_tumor_location_list',
                        'cie_o_tumor_location_search',
                        'patient_evaluation_search',
                        'user_get',
                        'user_list',
                        'user_search',
                        'user_hospital_get',
                        'user_hospital_list',
                        'user_hospital_search',
                        'role_get',
                        'role_list',
                        'role_search',
                        'role_permission_get',
                        'role_permission_list',
                        'role_permission_search',
                        'permission_get',
                        'permission_list',
                        'permission_search',
                        'menu_patient_registry',
                        'menu_patient',
                        'menu_patient_evaluation',
                        'medical_document_download',
                        'patient_summarize');

-- ADMINISTRADOR
-- BORRADO
DELETE
FROM role_permission rp
WHERE rp.id IN (SELECT rp.id
                FROM role
                         JOIN role_permission rp ON role.id = rp.role_id
                         JOIN permission p ON p.id = rp.permission_id
                WHERE role.description = 'ADMINISTRADOR');

DELETE
FROM role
WHERE description = 'ADMINISTRADOR';

-- INVENTARIO
-- BORRADO
DELETE
FROM role_permission rp
WHERE rp.id IN (SELECT rp.id
                FROM role
                         JOIN role_permission rp ON role.id = rp.role_id
                         JOIN permission p ON p.id = rp.permission_id
                WHERE role.description = 'INVENTARIO');
-- INSERCION
INSERT INTO role_permission (role_id, permission_id)
SELECT (SELECT id FROM role WHERE role.description = 'INVENTARIO'),
       p.id
FROM permission p
WHERE p.description IN (
                        'menu_patient_registry',
                        'menu_patient',
                        'menu_parameters',
                        'menu_medicine',
                        'treatment_plan_list',
                        'treatment_plan_search',
                        'treatment_plan_get',
                        'menu_inventory',
                        'menu_manufacturer',
                        'menu_supplier',
                        'menu_deposit',
                        'menu_lot',
                        'menu_stock',
                        'menu_deposit_movement',
                        'menu_dispatch_medications',
                        'patient_get',
                        'patient_list',
                        'patient_search',
                        'medicine_get',
                        'medicine_list',
                        'medicine_search',
                        'medicine_update',
                        'medicine_delete',
                        'medicine_insert',
                        'patient_view_information',
                        'treatment_follow_up_get',
                        'treatment_follow_up_list',
                        'treatment_follow_up_search',
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
                        'supplier_search',
                        'medical_document_get',
                        'medical_document_list',
                        'medical_document_search',
                        'medical_document_type_get',
                        'medical_document_type_list',
                        'medical_document_tyep_search',
                        'chemotherapy_get',
                        'chemotherapy_list',
                        'chemotherapy_search',
                        'radiotherapy_get',
                        'radiotherapy_list',
                        'radiotherapy_search',
                        'surgery_get',
                        'surgery_list',
                        'surgery_search',
                        'menopausal_state_get',
                        'menopausal_state_list',
                        'menopausal_state_search',
                        'committee_get',
                        'committee_list',
                        'committee_search',
                        'medical_document_download',
                        'patient_exclusion_criteria_get',
                        'patient_exclusion_criteria_list',
                        'patient_exclusion_criteria_search',
                        'patient_inclusion_criteria_adjuvant_trastuzumab_get',
                        'patient_inclusion_criteria_adjuvant_trastuzumab_list',
                        'patient_inclusion_criteria_adjuvant_trastuzumab_search',
                        'patient_inclusion_criteria_neoadjuvant_trastuzumab_list',
                        'patient_inclusion_criteria_neoadjuvant_trastuzumab_get',
                        'patient_inclusion_criteria_neoadjuvant_trastuzumab_search',
                        'patient_family_with_cancer_list',
                        'patient_family_with_cancer_get',
                        'patient_family_with_cancer_search',
                        'patient_inclusion_criteria_get',
                        'patient_inclusion_criteria_list',
                        'patient_inclusion_criteria_search',
                        'parameter_get',
                        'parameter_list',
                        'parameter_search',
                        'doctor_get',
                        'doctor_list',
                        'doctor_search',
                        'doctor_specialty_list',
                        'doctor_specialty_search',
                        'doctor_specialty_get',
                        'diagnosis_get',
                        'diagnosis_list',
                        'diagnosis_search',
                        'diagnosis_ap_get',
                        'diagnosis_ap_list',
                        'diagnosis_ap_search',
                        'type_treatment_get',
                        'type_treatment_list',
                        'type_treatment_search',
                        'patient_summarize');

-- AUDITOR
-- BORRADO
DELETE
FROM role_permission rp
WHERE rp.id IN (SELECT rp.id
                FROM role
                         JOIN role_permission rp ON role.id = rp.role_id
                         JOIN permission p ON p.id = rp.permission_id
                WHERE role.description = 'AUDITOR');
-- INSERCION
INSERT INTO role_permission (role_id, permission_id)
SELECT (SELECT id FROM role WHERE role.description = 'AUDITOR'),
       p.id
FROM permission p
WHERE p.description IN (
                        'patient_inclusion_criteria_search',
                        'patient_view_information',
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
                        'patient_search',
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
                        'menu_patient_evaluation',
                        'menu_parameters',
                        'menu_menopausal_state',
                        'menu_type_treatment',
                        'menu_document_type',
                        'menu_gender',
                        'menu_periodicity',
                        'menu_cie_10',
                        'menu_cie_o_morphology',
                        'menu_medicine',
                        'menu_doctor',
                        'menu_specialty',
                        'menu_hospital',
                        'menu_security',
                        'menu_role_permission',
                        'menu_user',
                        'menu_inventory',
                        'menu_manufacturer',
                        'menu_supplier',
                        'menu_deposit',
                        'menu_lot',
                        'menu_stock',
                        'menu_deposit_movement',
                        'menu_dispatch_medications',
                        'menu_patient_registry',
                        'menu_patient',
                        'additional_patient_information_get',
                        'additional_patient_information_list',
                        'additional_patient_information_search',
                        'area_get',
                        'area_list',
                        'area_search',
                        'patient_get',
                        'patient_list',
                        'patient_exclusion_criteria_get',
                        'patient_exclusion_criteria_list',
                        'patient_inclusion_criteria_adjuvant_trastuzumab_get',
                        'patient_inclusion_criteria_adjuvant_trastuzumab_list',
                        'patient_inclusion_criteria_neoadjuvant_trastuzumab_get',
                        'patient_inclusion_criteria_neoadjuvant_trastuzumab_list',
                        'patient_inclusion_criteria_get',
                        'patient_inclusion_criteria_list',
                        'patient_evaluation_search',
                        'chemotherapy_get',
                        'chemotherapy_list',
                        'cie_10_get',
                        'cie_10_list',
                        'cie_o_morphology_get',
                        'cie_o_morphology_list',
                        'cie_o_topography_get',
                        'cie_o_topography_list',
                        'cie_o_topography_search',
                        'cie_o_tumor_location_get',
                        'cie_o_tumor_location_list',
                        'cie_o_tumor_location_search',
                        'city_get',
                        'city_list',
                        'city_search',
                        'committee_get',
                        'committee_list',
                        'country_get',
                        'country_list',
                        'country_search',
                        'deposit_get',
                        'deposit_list',
                        'deposit_movement_get',
                        'deposit_movement_list',
                        'deposit_stock_get',
                        'diagnosis_list',
                        'diagnosis_get',
                        'diagnosis_ap_get',
                        'diagnosis_ap_list',
                        'dispatch_medications_get',
                        'dispatch_medications_list',
                        'doctor_get',
                        'doctor_list',
                        'doctor_specialty_list',
                        'treatment_plan_list',
                        'treatment_plan_search',
                        'treatment_plan_get',
                        'doctor_specialty_search',
                        'doctor_specialty_get',
                        'document_type_get',
                        'document_type_list',
                        'gender_get',
                        'gender_list',
                        'evaluation_list',
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
                        'evaluators_get',
                        'history_get',
                        'lot_get',
                        'lot_list',
                        'lot_detail_list',
                        'lot_detail_search',
                        'lot_detail_get',
                        'manufacturer_get',
                        'manufacturer_list',
                        'parameter_list',
                        'parameter_get',
                        'medical_committee_get',
                        'medical_committee_list',
                        'medical_committee_search',
                        'medical_document_get',
                        'medical_document_list',
                        'medical_document_type_get',
                        'medical_document_type_list',
                        'medical_team_get',
                        'medical_team_list',
                        'medical_team_search',
                        'medical_consultation_list',
                        'medical_consultation_search',
                        'medical_consultation_get',
                        'medication_get',
                        'medication_list',
                        'medication_search',
                        'medication_order_get',
                        'medication_order_list',
                        'medicine_get',
                        'medicine_list',
                        'medicine_medication_order_get',
                        'medicine_medication_order_list',
                        'medicine_medication_order_search',
                        'medicine_treatment_plan_list',
                        'medicine_treatment_plan_search',
                        'medicine_treatment_plan_get',
                        'periodicity_get',
                        'periodicity_list',
                        'puncture_get',
                        'puncture_list',
                        'radiotherapy_get',
                        'radiotherapy_list',
                        'stock_get',
                        'stock_list',
                        'supplier_get',
                        'supplier_list',
                        'surgery_get',
                        'surgery_list',
                        'treatment_follow_up_get',
                        'treatment_follow_up_list',
                        'treatment_follow_up_search',
                        'user_get',
                        'user_list',
                        'specialty_list',
                        'specialty_get',
                        'specialty_search',
                        'medical_document_download',
                        'patient_summarize');

-----------------------------
-- ALTER EN public.patient --
-----------------------------
-- ALTER TABLE public.patient
--     DROP COLUMN hospital_id;

ALTER TABLE public.patient
    DROP COLUMN doctor_id;

---------------------------------------------------
-- ALTER EN public.personal_pathological_history --
---------------------------------------------------
ALTER TABLE public.personal_pathological_history
    ADD patient_id integer;

ALTER TABLE public.personal_pathological_history
    ADD CONSTRAINT personal_pathological_history_patient_id_fk
        FOREIGN KEY (patient_id) REFERENCES public.patient;

----------------------------------------------------------------
-- SE RESCATA ID DE PACIENTE EN personal_pathological_history --
----------------------------------------------------------------
UPDATE personal_pathological_history pph
SET patient_id = (SELECT id FROM patient WHERE personal_pathological_history_id = pph.id);

-----------------------------
-- ALTER EN public.patient --
-----------------------------
ALTER TABLE public.patient
    DROP CONSTRAINT patient_personal_pathological_history_id_fk;

ALTER TABLE public.patient
    DROP COLUMN personal_pathological_history_id;

---------------------------------------------------
-- ALTER EN public.personal_pathological_history --
---------------------------------------------------
ALTER TABLE public.personal_pathological_history
    RENAME COLUMN main_findings TO observation;

ALTER TABLE public.personal_pathological_history
    ADD cie_10_code_id bigint;

ALTER TABLE public.personal_pathological_history
    ADD CONSTRAINT personal_pathological_history_cie_10_id_fk
        FOREIGN KEY (cie_10_code_id) REFERENCES public.cie_10;

ALTER TABLE public.personal_pathological_history
    ALTER COLUMN family_members_with_cancer TYPE varchar(20) USING family_members_with_cancer::varchar(20);

-- AJUSTE
UPDATE public.personal_pathological_history
SET family_members_with_cancer = 'yes'
WHERE family_members_with_cancer = 'true';

---------------------------------
-- INSERTS IN PUBLIC.SPECIALTY --
---------------------------------
INSERT INTO specialty (description)
VALUES ('Mastología'),
       ('Cirugía Oncológica '),
       ('Enfemería'),
       ('Psicología'),
       ('Nutrición'),
       ('Gastroenterología'),
       ('Medicina Paliativa '),
       ('Anatomía Patológica '),
       ('Bioquímica'),
       ('Cirugía General');

-----------------------------
-- ALTER EN public.patient --
-----------------------------

alter table public.patient
    drop column her2_positive;

alter table public.patient
    drop column hospital_departament_id;

------------------------------------------
-- ALTER EN public.medical_consultation --
------------------------------------------
ALTER TABLE public.medical_consultation
    ADD patient_id bigint;

ALTER TABLE public.medical_consultation
    ADD CONSTRAINT medical_consultation_patient_id_fk
        FOREIGN KEY (patient_id) REFERENCES public.patient;

--------------------------------------------------------------
-- SE RESCATA ID DE PACIENTE EN public.medical_consultation --
--------------------------------------------------------------
UPDATE medical_consultation mc
SET patient_id = (SELECT id FROM patient WHERE medical_consultation_id = mc.id);

------------------------------------------
-- ALTER EN public.public.patient --
------------------------------------------
ALTER TABLE public.patient
    DROP CONSTRAINT patient_medical_consultation_id_fk;

ALTER TABLE public.patient
    DROP COLUMN medical_consultation_id;

--------------------
-- ADD NEW PARAMS --
--------------------
INSERT INTO public.parameter (domain, value, active, code)
VALUES ('DIAGNOSIS_BY', 'OTRO', TRUE, 'OTRO');

------------------------------------------
-- ALTER EN public.medical_consultation --
------------------------------------------
ALTER TABLE public.medical_consultation
    ADD date_consultation date DEFAULT NOW();

ALTER TABLE public.medical_consultation
    ADD cie_10_id bigint;

ALTER TABLE public.medical_consultation
    ADD prescribed_medications text;

ALTER TABLE public.medical_consultation
    ADD responsible_doctor_id bigint;

ALTER TABLE public.medical_consultation
    ADD CONSTRAINT medical_consultation_cie_10_id_fk
        FOREIGN KEY (cie_10_id) REFERENCES public.cie_10;

ALTER TABLE public.medical_consultation
    ADD CONSTRAINT medical_consultation_doctor_id_fk
        FOREIGN KEY (responsible_doctor_id) REFERENCES public.doctor;

ALTER TABLE public.medical_consultation
    ADD apply_chemotherapy varchar(20);

------------------------------------
-- Cambios en public.diagnosis_ap --
------------------------------------
alter table public.diagnosis_ap
    drop column confirmed;

ALTER TABLE public.diagnosis_ap
    DROP COLUMN codification_type;

ALTER TABLE public.diagnosis_ap
    DROP CONSTRAINT diagnosis_ap_cie_10_id_fk;

ALTER TABLE public.diagnosis_ap
    DROP COLUMN cie_10_code_id;

alter table public.diagnosis_ap
    drop column re_positive;

alter table public.diagnosis_ap
    drop column re_negative;

alter table public.diagnosis_ap
    drop column rp_negative;

alter table public.diagnosis_ap
    drop column rp_positive;

alter table public.diagnosis_ap
    drop column her2_positive;

alter table public.diagnosis_ap
    drop column her2_negative;

alter table public.diagnosis_ap
    drop column ihq_3_pos;

alter table public.diagnosis_ap
    drop column ihq_2_pos_fish;

alter table public.diagnosis_ap
    drop column re_no_data;

alter table public.diagnosis_ap
    drop column rp_no_data;

alter table public.diagnosis_ap
    drop column her2_no_data;

alter table public.diagnosis_ap
    add re varchar(20);

alter table public.diagnosis_ap
    add rp varchar(20);

alter table public.diagnosis_ap
    add her2 varchar(20);

alter table public.diagnosis_ap
    add her2_positive_id bigint;

alter table public.diagnosis_ap
    drop column armpit_negative;

alter table public.diagnosis_ap
    drop column armpit_positive;

alter table public.diagnosis_ap
    drop column armpit_no_data;

alter table public.diagnosis_ap
    add armpit varchar(20);

--------------------------------------
-- CAMBIOS EN public.treatment_plan --
--------------------------------------
alter table public.treatment_plan
    drop column historical;

alter table public.treatment_plan
    drop column confirmed;

-----------------------------------------------
-- CAMBIOS EN public.medicine_treatment_plan --
-----------------------------------------------
alter table public.medicine_treatment_plan
    drop column treatment_program;

-------------------------------------------
-- CAMBIOS EN public.treatment_follow_up --
-------------------------------------------

alter table public.treatment_follow_up
    add patient_id bigint;

alter table public.treatment_follow_up
    add hospital_id bigint;

update treatment_follow_up fu
set patient_id = (SELECT patient_id
                  FROM treatment_plan
                  where id = fu.treatment_plan_id);

-- alter table public.treatment_follow_up
--     drop column treatment_plan_id;

alter table public.treatment_follow_up
    drop column trastuzumab_dose;

-----------------------------------------------
-- CREATE TABLE medicine_treatment_follow_up --
----------------------------------------------
CREATE TABLE public.medicine_treatment_follow_up
(
    id                     bigserial PRIMARY KEY,
    medicine_id            bigint  NOT NULL
        CONSTRAINT medicine_treatment_follow_up_fk
            REFERENCES public.medicine,
    treatment_follow_up_id bigint  NOT NULL
        CONSTRAINT medicine_treatment_follow_up_fk_2
            REFERENCES public.treatment_follow_up,
    quantity               numeric NOT NULL,
    observation            text,
    dose                   numeric
);

INSERT INTO public.permission (description)
VALUES ('medicine_treatment_follow_up_list'),
       ('medicine_treatment_follow_up_search'),
       ('medicine_treatment_follow_up_get'),
       ('medicine_treatment_follow_up_insert'),
       ('medicine_treatment_follow_up_update'),
       ('medicine_treatment_follow_up_delete');

-- INSERCION
select * from role;
INSERT INTO role_permission (role_id, permission_id)
SELECT (SELECT id FROM role WHERE role.description = 'MEDICO'),
       p.id
FROM permission p
WHERE p.description IN ('medicine_treatment_follow_up_list',
                        'medicine_treatment_follow_up_search',
                        'medicine_treatment_follow_up_get',
                        'medicine_treatment_follow_up_insert',
                        'medicine_treatment_follow_up_update',
                        'medicine_treatment_follow_up_delete');

INSERT INTO role_permission (role_id, permission_id)
SELECT (SELECT id FROM role WHERE role.description = 'ENFERMERIA'),
       p.id
FROM permission p
WHERE p.description IN ('medicine_treatment_follow_up_list',
                        'medicine_treatment_follow_up_search',
                        'medicine_treatment_follow_up_get',
                        'medicine_treatment_follow_up_insert',
                        'medicine_treatment_follow_up_update',
                        'medicine_treatment_follow_up_delete');

INSERT INTO role_permission (role_id, permission_id)
SELECT (SELECT id FROM role WHERE role.description = 'INVENTARIO'),
       p.id
FROM permission p
WHERE p.description IN ('medicine_treatment_follow_up_list',
                        'medicine_treatment_follow_up_search',
                        'medicine_treatment_follow_up_get');

INSERT INTO role_permission (role_id, permission_id)
SELECT (SELECT id FROM role WHERE role.description = 'AUDITOR'),
       p.id
FROM permission p
WHERE p.description IN ('medicine_treatment_follow_up_list',
                        'medicine_treatment_follow_up_search',
                        'medicine_treatment_follow_up_get');

-------------------
-- ADD NEW PARAM --
-------------------
INSERT INTO public.parameter (domain, value, active, code)
VALUES ('CHEMOTHERAPY_SESSION_STATE', 'No realizada', TRUE, 'CHEM_SES_UNREALIZED');

------------------------------------
-- CAMBIOS EN public.chemotherapy --
------------------------------------

ALTER TABLE public.chemotherapy
    ADD doctor_id integer;

ALTER TABLE public.chemotherapy
    ADD CONSTRAINT chemotherapy_doctor_id_fk
        FOREIGN KEY (doctor_id) REFERENCES public.doctor;

ALTER TABLE public.chemotherapy
    ADD technician text;

ALTER TABLE public.chemotherapy
    ADD nurse text;

-------------------
-- ADD NEW PARAM --
-------------------
INSERT INTO public.parameter (domain, value, active, code)
VALUES ('RADIOTHERAPY_SESSION_STATE', 'No realizada', TRUE, 'RADIO_SES_UNREALIZED');

------------------------------------
-- CAMBIOS EN public.radiotherapy --
------------------------------------

alter table public.radiotherapy
    add doctor_id bigint;

alter table public.radiotherapy
    add technician text;

alter table public.radiotherapy
    add nurse text;

alter table public.radiotherapy
    add constraint radiotherapy_doctor_id_fk
        foreign key (doctor_id) references public.doctor;

-------------------------------
-- CAMBIOS EN public.surgery --
-------------------------------
alter table public.surgery
    add surgical_technique text;

------------------------------------
-- CAMBIOS EN public.medical_team --
------------------------------------
alter table public.medical_team
    add nurse text;

alter table public.medical_team
    add anesthetist text;

alter table public.medical_team
    add surgical_instrumentator text;

alter table public.medical_team
    add technical text;

-----------------------------------------
-- CAMBIOS EN public.medical_committee --
-----------------------------------------
alter table public.medical_committee
    drop column priority;

---------------------------
-- ADD NEW DOCUMENT TYPE --
---------------------------
INSERT INTO public.medical_document_type (description)
VALUES ('FORMULARIO DE CRITERIOS DE INCLUSIÓN');

INSERT INTO public.medical_document_type (description)
VALUES ('FORMULARIO DE CRITERIOS DE EXCLUSIÓN');

-- SERVER DESARROLLO

