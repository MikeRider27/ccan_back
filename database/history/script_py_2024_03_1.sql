-- ALTER IN public.patient_inclusion_criteria_neoadjuvant_trastuzumab
alter table public.patient_inclusion_criteria_neoadjuvant_trastuzumab
    add tumor_size_diameter_determined_by varchar(30);

alter table public.patient_inclusion_criteria_neoadjuvant_trastuzumab
    add positive_armpit_determined_by varchar(30);

-- ADD PARAMETERS
INSERT INTO public.medical_document_type (description, orden)
VALUES ('MAMOGRAFÍA', NULL);

INSERT INTO public.medical_document_type (description, orden)
VALUES ('ECOGRAFÍA MAMARIA', NULL);