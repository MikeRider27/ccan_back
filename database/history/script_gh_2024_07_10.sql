-- INSERT INTO public.medical_document_type GH
INSERT INTO public.medical_document_type (description, orden, code)
VALUES ('COLPOSCOPY', NULL, 'COLPOSCOPY');
INSERT INTO public.medical_document_type (description, orden, code)
VALUES ('CHEST XRAY', NULL, 'CHEST_XRAY');
INSERT INTO public.medical_document_type (description, orden, code)
VALUES ('BLOOD LFT', NULL, 'BLOOD_LFT');
INSERT INTO public.medical_document_type (description, orden, code)
VALUES ('BLOOD UREA CREATININE', NULL, 'BLOOD_UREA_CREAT');
INSERT INTO public.medical_document_type (description, orden, code)
VALUES ('FNAC', NULL, 'FNAC');
INSERT INTO public.medical_document_type (description, orden, code)
VALUES ('TRUCUT HISTOLOGY', NULL, 'TRUCUT_HISTOLOGY');
INSERT INTO public.medical_document_type (description, orden, code)
VALUES ('OTHER BIOPSY HISTOLOGY', NULL, 'OTHER_BIOP_HIST');
INSERT INTO public.medical_document_type (description, orden, code)
VALUES ('CHEST CT', NULL, 'CHEST_CT');
INSERT INTO public.medical_document_type (description, orden, code)
VALUES ('BLOOD FBC', NULL, 'BLOOD_FBC');

-- INSERT INTO public.parameter
INSERT INTO public.parameter (domain, value, active, code)
VALUES ('SITE_MASS', 'ANTERIOR LIP', TRUE, 'ANT_LIP'),
       ('SITE_MASS', 'POSTERIOR LIP', TRUE, 'POS_LIP');

INSERT INTO public.parameter (domain, value, active, code)
VALUES ('EXTENSIONS', 'PARAMETRIUM', TRUE, 'PARAMETRIUM'),
       ('EXTENSIONS', 'URINARY BLADDER', TRUE, 'URI_BLADD'),
       ('EXTENSIONS', 'UTERUS', TRUE, 'UTERUS'),
       ('EXTENSIONS', 'URETERS', TRUE, 'URETERS'),
       ('EXTENSIONS', 'LYMPHNODES', TRUE, 'LYMPHNODES');

INSERT INTO public.parameter (domain, value, active, code)
VALUES ('CHEST_XRAY', 'NORMAL', TRUE, 'NORMAL'),
       ('CHEST_XRAY', 'METASTATIC', TRUE, 'METASTATIC'),
       ('CHEST_XRAY', 'SUSPICIOUS', TRUE, 'SUSPICIOUS');

INSERT INTO public.parameter (domain, value, active, code)
VALUES ('BLOOD_FBC', 'HB', TRUE, 'HB'),
       ('BLOOD_FBC', 'WBC TOTAL AND NEUTROPHIL COUNT', TRUE, 'WBC_NEUT_COUNT'),
       ('BLOOD_FBC', 'PLATELETS', TRUE, 'PLATELETS');

INSERT INTO public.parameter (domain, value, active, code)
VALUES ('ECOG', '0', TRUE, 'ECOG_0'),
       ('ECOG', '1', TRUE, 'ECOG_1'),
       ('ECOG', '2', TRUE, 'ECOG_2'),
       ('ECOG', '3', TRUE, 'ECOG_3'),
       ('ECOG', '4', TRUE, 'ECOG_4'),
       ('ECOG', '5', TRUE, 'ECOG_5');

INSERT INTO public.parameter (domain, value, active, code)
VALUES ('BIRADS', '0', TRUE, 'BIRADS_0'),
       ('BIRADS', '1', TRUE, 'BIRADS_1'),
       ('BIRADS', '2', TRUE, 'BIRADS_2'),
       ('BIRADS', '3', TRUE, 'BIRADS_3'),
       ('BIRADS', '4', TRUE, 'BIRADS_4'),
       ('BIRADS', '5', TRUE, 'BIRADS_5'),
       ('BIRADS', '6', TRUE, 'BIRADS_6');

INSERT INTO public.parameter (domain, value, active, code)
VALUES ('MORPHOLOGY', 'INVASIVE CARCINOMA, NST', TRUE, 'IC_NST'),
       ('MORPHOLOGY', 'INVASIVE LOBULAR CARCINOMA', TRUE, 'ILC'),
       ('MORPHOLOGY', 'INVASIVE MUCINOUS CARCINOMA', TRUE, 'IMC'),
       ('MORPHOLOGY', 'OTHERS (SPECIFY)', TRUE, 'OTHERS');

INSERT INTO public.parameter (domain, value, active, code)
VALUES ('HORMONE_RECEPTOR_STATUS', 'POSITIVE', TRUE, 'HRS_POS'),
       ('HORMONE_RECEPTOR_STATUS', 'NEGATIVE', TRUE, 'HRS_NEG');

INSERT INTO public.parameter (domain, value, active, code)
VALUES ('HER_2_NEU', '1+', TRUE, 'HER_2_NEU_1'),
       ('HER_2_NEU', '2+', TRUE, 'HER_2_NEU_2'),
       ('HER_2_NEU', '3+', TRUE, 'HER_2_NEU_3');

INSERT INTO public.parameter (domain, value, active, code)
VALUES ('CHEST_CT', 'NORMAL', TRUE, 'NORMAL'),
       ('CHEST_CT', 'METASTATIC', TRUE, 'METASTATIC'),
       ('CHEST_CT', 'SUSPICIOUS', TRUE, 'SUSPICIOUS');

INSERT INTO public.parameter (domain, value, active, code)
VALUES ('USG_LIVER', 'NORMAL', TRUE, 'NORMAL'),
       ('USG_LIVER', 'METASTATIC', TRUE, 'METASTATIC'),
       ('USG_LIVER', 'SUSPICIOUS', TRUE, 'SUSPICIOUS');

INSERT INTO public.parameter (domain, value, active, code)
VALUES ('STAGE_BREAST_LOCATION', 'LEFT', TRUE, 'BREAST_LOCAT_LEFT'),
       ('STAGE_BREAST_LOCATION', 'RIGHT', TRUE, 'BREAST_LOCAT_RIGHT');

INSERT INTO public.parameter (domain, value, active, code)
VALUES ('STAGE_BREAST_T', 'Tx', TRUE, 'STAGE_BREAST_Tx'),
       ('STAGE_BREAST_T', 'Tis', TRUE, 'STAGE_BREAST_Tis'),
       ('STAGE_BREAST_T', 'T1', TRUE, 'STAGE_BREAST_T1'),
       ('STAGE_BREAST_T', 'T2', TRUE, 'STAGE_BREAST_T2'),
       ('STAGE_BREAST_T', 'T3', TRUE, 'STAGE_BREAST_T3'),
       ('STAGE_BREAST_T', 'T4a', TRUE, 'STAGE_BREAST_T4a'),
       ('STAGE_BREAST_T', 'T4b', TRUE, 'STAGE_BREAST_T4b'),
       ('STAGE_BREAST_T', 'T4c', TRUE, 'STAGE_BREAST_T4c'),
       ('STAGE_BREAST_T', 'T4d', TRUE, 'STAGE_BREAST_T4d');

INSERT INTO public.parameter (domain, value, active, code)
VALUES ('STAGE_BREAST_N', 'Nx', TRUE, 'STAGE_BREAST_Nx'),
       ('STAGE_BREAST_N', 'N0', TRUE, 'STAGE_BREAST_N0'),
       ('STAGE_BREAST_N', 'N1', TRUE, 'STAGE_BREAST_N1'),
       ('STAGE_BREAST_N', 'N2', TRUE, 'STAGE_BREAST_N2'),
       ('STAGE_BREAST_N', 'N3', TRUE, 'STAGE_BREAST_N3');

INSERT INTO public.parameter (domain, value, active, code)
VALUES ('STAGE_BREAST_M', 'Mx', TRUE, 'STAGE_BREAST_Mx'),
       ('STAGE_BREAST_M', 'M0', TRUE, 'STAGE_BREAST_M0'),
       ('STAGE_BREAST_M', 'M1', TRUE, 'STAGE_BREAST_M1');

--CREATE TABLE PUBLIC.CERVIX_FORM
CREATE TABLE public.cervix_form
(
    id                                 bigserial
        CONSTRAINT cervix_form_pk
            PRIMARY KEY,
    patient_id                         bigint
        CONSTRAINT cervix_form_patient_id_fk
            REFERENCES public.patient,
    -- Commons fields
    departament                        text,
    parity                             boolean,
    residential_address                text,
    pmhx                               text,
    presenting_complaint               text,
    main_physical_clinical_findings    text,
    performance_status_ecog_id         bigint,
    treatment_decision                 text,
    -- Especific fields
    colposcopy_date                    timestamp(0),
    colposcopy_report_id               bigint,
    cervical_biopsy_date               timestamp(0),
    cervical_biopsy_histology          text,
    cervical_biopsy_morphology         text,
    cervical_biopsy_grade              text,
    usg_pelvis_abdomen_date            timestamp(0),
    usg_pelvis_abdomen_site_of_mass_id bigint,
    usg_pelvis_abdomen_size_of_mass    text,
    usg_pelvis_abdomen_extensions_id   bigint,
    chest_xray_date                    timestamp(0),
    chest_xray_report_id               bigint,
    chest_xray_summary_id              bigint,
    pelvic_mri_date                    timestamp(0),
    pelvic_mri_site_of_mass_id         bigint,
    pelvic_mri_size_of_mass            text,
    pelvic_mri_extensions_id           bigint,
    blood_date                         timestamp(0),
    blood_fbc_id                       bigint,
    blood_fbc                          text,
    blood_lft_report_id                bigint,
    blood_urea_creatinine_report_id    bigint,
    stage_figo_date                    timestamp(0),
    stage_figo_id                      bigint,
    -- Audit Fields
    date_create                        timestamp(0) DEFAULT NOW() NOT NULL,
    user_create                        varchar(30)  DEFAULT 'ccan'::character varying,
    date_modify                        timestamp(0),
    user_modify                        varchar(30)
);

--CREATE TABLE PUBLIC.BREAST_FORM
CREATE TABLE public.breast_form
(
    id                                      bigserial
        CONSTRAINT breast_form_pk
            PRIMARY KEY,
    patient_id                              bigint
        CONSTRAINT breast_form_patient_id_fk
            REFERENCES public.patient,
    -- Commons fields
    departament                             text,
    residential_address                     text,
    parity                                  boolean,
    pmhx                                    text,
    presenting_complaint                    text,
    main_physical_clinical_findings         text,
    performance_status_ecog_id              bigint,
    treatment_decision                      text,
    -- Especific fields
    mammogram_date                          timestamp(0),
    mammogram_birads_id                     bigint,
    mammogram_report_id                     bigint,
    usg_breast_date                         timestamp(0),
    usg_breast_birads_id                    bigint,
    usg_breast_report_id                    bigint,
    fnac_date                               timestamp(0),
    fnac_report_id                          bigint,
    fnac_summary                            text,
    trucut_date                             timestamp(0),
    trucut_histology_report_id              bigint,
    trucut_morphology_id                    bigint,
    trucut_others                           text,
    trucut_grade                            text,
    trucut_hormone_receptor_status_id       bigint,
    trucut_her2_neu_id                      bigint,
    other_biopsy_date                       timestamp(0),
    other_biopsy_histology_report_id        bigint,
    other_biopsy_morphology_id              bigint,
    other_biopsy_others                     text,
    other_biopsy_grade                      text,
    other_biopsy_hormone_receptor_status_id bigint,
    other_biopsy_her2_neu_id                bigint,
    chest_xray_date                         timestamp(0),
    chest_xray_report_id                    bigint,
    chest_xray_summary_id                   bigint,
    chest_ct_date                           timestamp(0),
    chest_ct_report_id                      bigint,
    chest_ct_summary_id                     bigint,
    usg_liver_date                          timestamp(0),
    usg_liver_summary_id                    bigint,
    blood_date                              timestamp(0),
    blood_fbc_id                            bigint,
    blood_fbc                               text,
    blood_fbc_report_id                     bigint,
    blood_lft_report_id                     bigint,
    blood_urea_creatinine_report_id         bigint,
    bone_scan_date                          timestamp(0),
    bone_scan_summary                       text,
    -- Audit Fields
    date_create                             timestamp(0) DEFAULT NOW() NOT NULL,
    user_create                             varchar(30)  DEFAULT 'ccan'::character varying,
    date_modify                             timestamp(0),
    user_modify                             varchar(30)
);

-- INSERT INTO public.permission
INSERT INTO public.permission (description)
VALUES ('cervix_form_list'),
       ('cervix_form_search'),
       ('cervix_form_get'),
       ('cervix_form_insert'),
       ('cervix_form_update'),
       ('cervix_form_delete'),
       ('breast_form_list'),
       ('breast_form_search'),
       ('breast_form_get'),
       ('breast_form_insert'),
       ('breast_form_update'),
       ('breast_form_delete');

INSERT INTO public.permission (description)
VALUES ('cervix_breast_header_form_get');

--ALTER TABLE PUBLIC.PATIENT_FAMILY_WITH_CANCER
ALTER TABLE public.patient_family_with_cancer
    ADD cancer_type text;

-----------------------------------------------------------------------------------------------------------------------
--STAGE (FIGO)
INSERT INTO public.parameter (domain, value, active, code)
VALUES ('STAGE_FIGO', 'Stage 0 - Carcinoma in situ, CIN', TRUE, 'STAGE_0'),
       ('STAGE_FIGO', 'Stage I - Invasive carcinoma confined to the cervix', TRUE, 'STAGE_I'),
       ('STAGE_FIGO', 'Stage II - Extension beyond cervix but not to sidewall', TRUE, 'STAGE_II'),
       ('STAGE_FIGO', 'Stage III - Extension to pelvic wall and/or lower of vagina; hydronephrosis', TRUE, 'STAGE_III'),
       ('STAGE_FIGO', 'Stage IV - Extension beyond true pelvis or involving bladder or rectum', TRUE, 'STAGE_IV');

INSERT INTO public.parameter (domain, value, active, code)
VALUES ('STAGE_FIGO_I', 'IA - Diagnosed only by microscopy', TRUE, 'STAGE_IA'),
       ('STAGE_FIGO_I', 'IB - Clinically visible or microscopic lesion >IA2', TRUE, 'STAGE_IB');

INSERT INTO public.parameter (domain, value, active, code)
VALUES ('STAGE_FIGO_IA', 'IA1 - Micro-invasive carcinoma with stromal invasion < 3 mm depth, < 7 mm width', TRUE, 'STAGE_IA1'),
       ('STAGE_FIGO_IA', 'IA2 - Micro-invasive carcinoma with stromal invasion < 5 mm depth, < 7 mm width', TRUE, 'STAGE_IA2');

INSERT INTO public.parameter (domain, value, active, code)
VALUES ('STAGE_FIGO_IB', 'IB1 - Clinical lesion < 4 cm', TRUE, 'STAGE_IB1'),
       ('STAGE_FIGO_IB', 'IB2 - Clinical lesion > 4 cm', TRUE, 'STAGE_IB2');

INSERT INTO public.parameter (domain, value, active, code)
VALUES ('STAGE_FIGO_II', 'IIA - Involvement of the upper two-thirds of the vagina', TRUE, 'STAGE_IIA'),
       ('STAGE_FIGO_II', 'IIB - Parametrial involvement', TRUE, 'STAGE_IIB');

INSERT INTO public.parameter (domain, value, active, code)
VALUES ('STAGE_FIGO_III', 'IIIA - Involvement of the lower third of the vagina', TRUE, 'STAGE_IIIA'),
       ('STAGE_FIGO_III', 'IIIB - Pelvic sidewall involvement; hydronephrosis', TRUE, 'STAGE_IIIB');

INSERT INTO public.parameter (domain, value, active, code)
VALUES ('STAGE_FIGO_IV', 'IVA - Involvement of the bladder or rectal mucosa', TRUE, 'STAGE_IVA'),
       ('STAGE_FIGO_IV', 'IVB - Spread outside the true pelvis or metastasis to distant organs', TRUE, 'STAGE_IVB');

-- ALTER TABLE PUBLIC.CERVIX_FORM
ALTER TABLE public.cervix_form
    ADD stage_figo_i_id bigint;

ALTER TABLE public.cervix_form
    ADD stage_figo_ia_id bigint;

ALTER TABLE public.cervix_form
    ADD stage_figo_ib_id bigint;

ALTER TABLE public.cervix_form
    ADD stage_figo_ii_id bigint;

ALTER TABLE public.cervix_form
    ADD stage_figo_iii_id bigint;

ALTER TABLE public.cervix_form
    ADD stage_figo_iv_id bigint;

-- ALTER TABLE PUBLIC.BREAST_FORM
ALTER TABLE public.breast_form
    ADD stage_breast_location_id bigint;

ALTER TABLE public.breast_form
    ADD stage_breast_date timestamp(0);

ALTER TABLE public.breast_form
    ADD stage_breast_t_id bigint;

ALTER TABLE public.breast_form
    ADD stage_breast_n_id bigint;

ALTER TABLE public.breast_form
    ADD stage_breast_m_id bigint;