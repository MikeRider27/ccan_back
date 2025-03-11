-- ALTER en public.patient_inclusion_criteria
ALTER TABLE public.patient_inclusion_criteria
    ADD doctor_id bigint;

ALTER TABLE public.patient_inclusion_criteria
    ADD CONSTRAINT patient_inclusion_criteria_doctor_id_fk
        FOREIGN KEY (doctor_id) REFERENCES public.doctor;

-- ALTER en public.patient_inclusion_criteria
ALTER TABLE public.patient_inclusion_criteria
    ADD specialty_id bigint;

ALTER TABLE public.patient_inclusion_criteria
    ADD CONSTRAINT patient_inclusion_criteria_doctor_specialty_id_fk
        FOREIGN KEY (specialty_id) REFERENCES public.doctor_specialty;

-- ADD VALUES EN public.parameter
INSERT INTO public.parameter (domain, value, active, code)
VALUES ('HER2_POSITVE', 'IHQ', TRUE, 'IHQ (+++)'),
       ('HER2_POSITVE', 'FISH', TRUE, 'FISH'),
       ('HER2_POSITVE', 'CISH', TRUE, 'CISH'),
       ('HER2_POSITVE', 'SICH', TRUE, 'SICH');

-- ALTER en public.patient_inclusion_criteria_adjuvant_trastuzumab
ALTER TABLE public.patient_inclusion_criteria_adjuvant_trastuzumab
    ADD her2_positive_id bigint;

ALTER TABLE public.patient_inclusion_criteria_adjuvant_trastuzumab
    ADD CONSTRAINT patient_inclusion_criteria_adjuvant_trastuzumab_parameter_id_fk
        FOREIGN KEY (her2_positive_id) REFERENCES public.parameter;

-- ALTER en public.patient_inclusion_criteria_neoadjuvant_trastuzumab
ALTER TABLE public.patient_inclusion_criteria_neoadjuvant_trastuzumab
    ADD her2_positive_id bigint;

ALTER TABLE public.patient_inclusion_criteria_neoadjuvant_trastuzumab
    ADD CONSTRAINT inclusion_criteria_neoadjuvant_trastuzumab_parameter_id_fk
        FOREIGN KEY (her2_positive_id) REFERENCES public.parameter;

ALTER TABLE public.patient_inclusion_criteria_neoadjuvant_trastuzumab
    RENAME COLUMN her2_positive TO neoadjuvant_trastuzumab_her2_positive;

-- ALTER EN public.diagnosis_ap
ALTER TABLE public.diagnosis_ap
    ADD codification_type varchar(10);

ALTER TABLE public.diagnosis_ap
    ADD confirmed boolean;

ALTER TABLE public.diagnosis_ap
    ADD cie_10_code_id bigint;

ALTER TABLE public.diagnosis_ap
    ADD cie_o_morphology_id bigint;

ALTER TABLE public.diagnosis_ap
    ADD cie_o_topography_id bigint;

ALTER TABLE public.diagnosis_ap
    ADD cie_o_tumor_location_id bigint;

ALTER TABLE public.diagnosis_ap
    ADD CONSTRAINT diagnosis_ap_cie_10_id_fk
        FOREIGN KEY (cie_10_code_id) REFERENCES public.cie_10;

ALTER TABLE public.diagnosis_ap
    ADD CONSTRAINT diagnosis_ap_cie_o_morphology_id_fk
        FOREIGN KEY (cie_o_morphology_id) REFERENCES public.cie_o_morphology;

ALTER TABLE public.diagnosis_ap
    ADD CONSTRAINT diagnosis_ap_cie_o_topography_id_fk
        FOREIGN KEY (cie_o_topography_id) REFERENCES public.cie_o_topography;

ALTER TABLE public.diagnosis_ap
    ADD CONSTRAINT diagnosis_ap_cie_o_tumor_location_id_fk
        FOREIGN KEY (cie_o_tumor_location_id) REFERENCES public.cie_o_tumor_location;

-- ADD VALUES EN public.parameter
INSERT INTO public.parameter (domain, value, active, code)
VALUES ('CHEMOTHERAPY_REQUEST_STATE', 'APROBADA', TRUE, 'CHEM_REQ_APROB'),
       ('CHEMOTHERAPY_REQUEST_STATE', 'DENEGADA', TRUE, 'CHEM_REQ_DENEG');

INSERT INTO public.parameter (domain, value, active, code)
VALUES ('CHEMOTHERAPY_SESSION_STATE', 'En curso', TRUE, 'CHEM_SES_CURSO'),
       ('CHEMOTHERAPY_SESSION_STATE', 'Pausada', TRUE, 'CHEM_SES_PAUS'),
       ('CHEMOTHERAPY_SESSION_STATE', 'Finalizada', TRUE, 'CHEM_SES_FIN');

INSERT INTO public.parameter (domain, value, active, code)
VALUES ('RADIOTHERAPY_SESSION_STATE', 'En curso', TRUE, 'RADIO_SES_CURSO'),
       ('RADIOTHERAPY_SESSION_STATE', 'Pausada', TRUE, 'RADIO_SES_PAUS'),
       ('RADIOTHERAPY_SESSION_STATE', 'Finalizada', TRUE, 'RADIO_SES_FIN');

-- ALTER EN public.chemotherapy
ALTER TABLE public.chemotherapy
    ADD nro_session integer;

ALTER TABLE public.chemotherapy
    ADD request_state_id bigint;

ALTER TABLE public.chemotherapy
    ADD observation text;

ALTER TABLE public.chemotherapy
    ADD session_state_id bigint;

ALTER TABLE public.chemotherapy
    ADD CONSTRAINT chemotherapy_parameter_id_fk
        FOREIGN KEY (request_state_id) REFERENCES public.parameter;

ALTER TABLE public.chemotherapy
    ADD CONSTRAINT chemotherapy_parameter_id_fk2
        FOREIGN KEY (session_state_id) REFERENCES public.parameter;

-- ALTER EN public.radiotherapy
ALTER TABLE public.radiotherapy
    ADD nro_session bigint;

ALTER TABLE public.radiotherapy
    ADD observation text;

ALTER TABLE public.radiotherapy
    ADD session_state_id bigint;

ALTER TABLE public.radiotherapy
    ADD CONSTRAINT radiotherapy_parameter_id_fk
        FOREIGN KEY (session_state_id) REFERENCES public.parameter;

