-- INSERT PERMISSIONS
INSERT INTO public.permission (description)
VALUES ('menu_report'),
       ('report_download'),
       ('report_indicator_1_get'),
       ('report_indicator_2_get'),
       ('report_donation_medications_get');

-- INSERT PERMISSIONS TO ALL ROLES
INSERT INTO public.role_permission (role_id, permission_id)
SELECT r.id, p.id
FROM role r,
     permission p
WHERE p.description IN ('menu_report', 'report_download', 'report_indicator_1_get', 'report_indicator_2_get',
                        'report_donation_medications_get');

-- AJUSTES
-- ALTER IN public.medical_document_type
ALTER TABLE public.medical_document_type
    ADD active boolean DEFAULT TRUE;

-- ALTER IN audit.public_medical_document_type
ALTER TABLE audit.public_medical_document_type
    ADD active boolean;

UPDATE public.medical_document_type
SET active = FALSE
WHERE code IN ('INIT_DOSE',
               'COLPOSCOPY',
               'CHEST_XRAY',
               'BLOOD_LFT',
               'BLOOD_UREA_CREAT',
               'FNAC',
               'TRUCUT_HISTOLOGY',
               'OTHER_BIOP_HIST',
               'CHEST_CT',
               'BLOOD_FBC'
    );