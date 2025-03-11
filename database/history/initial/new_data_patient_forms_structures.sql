CREATE TABLE public.patient_inclusion_criteria_adjuvant_trastuzumab
(
    id                                      bigserial
        CONSTRAINT patient_inclusion_criteria_adjuvant_trastuzumab_pk
            PRIMARY KEY,
    patient_id                              bigint NOT NULL
        CONSTRAINT patient_inclusion_criteria_adjuvant_trastuzumab_patient_fk
            REFERENCES public.patient,
    diagnosed_invasive_adenocarcinoma       boolean,
    adenocarcinoma_completely_resected      boolean,
    tumor_diameter_greater_10mm             boolean,
    adjuvant_trastuzumab_her2_positive      boolean,
    determination_hormone_receptors         boolean,
    absolute_neutrophils_eq_greater_1500_ul boolean,
    platelets_eq_greater_90000_mm3          boolean,
    renal_hepatic_appropriate               boolean
);

CREATE TABLE public.patient_inclusion_criteria_neoadjuvant_trastuzumab
(
    id                                    bigserial
        CONSTRAINT patient_inclusion_criteria_neoadjuvant_trastuzumab_pk
            PRIMARY KEY,
    patient_id                            bigint NOT NULL
        CONSTRAINT patient_inclusion_criteria_neoadjuvant_trastuzumab_patient_fk
            REFERENCES public.patient,
    diagnosed_invasive_adenocarcinoma     boolean,
    her2_positive                         boolean,
    tumor_eq_ge_2cm                       boolean,
    positive_axilla                       boolean,
    marked_tumor_bed                      boolean,
    blood_count_renal_hepatic_appropriate boolean
);

CREATE TABLE public.patient_exclusion_criteria
(
    id                                                bigserial
        CONSTRAINT patient_exclusion_criteriapatient_pk
            PRIMARY KEY,
    patient_id                                        bigint NOT NULL
        CONSTRAINT patient_exclusion_criteria_patient_fk
            REFERENCES public.patient,
    distant_metastatic                                boolean,
    life_expectancy_greater_5_comorbidities           boolean,
    fevi_less_50                                      boolean,
    ecog_eq_greater_2                                 boolean,
    congestive_ic                                     boolean,
    ischemic_heart_disease                            boolean,
    arritmia_inestable                                boolean,
    valve_disease                                     boolean,
    uncontrolled_hta                                  boolean,
    doxorubicin_greater_360mg_by_m2                   boolean,
    epirrubicina_greater__720mg_by_m2                 boolean,
    pregnancy                                         boolean,
    lactation                                         boolean,
    has_signed_informed_consent                       boolean,
    patient_received_document                         boolean,
    consent_obtained_through_dialogue                 boolean,
    has_received_sufficient_sufficient                boolean,
    has_asked_questions_and_can_continue_asking       boolean,
    informed_receive_permanent_continuous_information boolean,
    information_received_clear_complete               boolean,
    received_information_understandable_language      boolean,
    treatment_hospital_id                             bigint
);

CREATE TABLE public.committee
(
    id          bigserial
        CONSTRAINT committee_pk
            PRIMARY KEY,
    patient_id  bigint       NOT NULL
        CONSTRAINT committee_patient_fk
            REFERENCES public.patient,
    hospital_id bigint       NOT NULL
        CONSTRAINT committee_hospital_fk
            REFERENCES public.hospital,
    date        timestamp(0) NOT NULL,
    observation text
);

CREATE TABLE public.medical_committee
(
    id           bigserial
        CONSTRAINT medical_committee_pk
            PRIMARY KEY,
    committee_id bigint NOT NULL
        CONSTRAINT medical_committee_committee_id_fk
            REFERENCES public.committee,
    doctor_id    bigint NOT NULL
        CONSTRAINT medical_committee_doctor_id_fk_1
            REFERENCES public.doctor,
    priority     varchar(300)
);


alter table public.patient
    alter column firstname type text using firstname::text;

alter table public.patient
    alter column lastname type text using lastname::text;

alter table public.patient
    alter column document_number type text using document_number::text;

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE OR REPLACE FUNCTION encrypt_data(data text, key text)
RETURNS text AS $$
BEGIN
    RETURN encode(pgp_sym_encrypt(data, key), 'escape');
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION decrypt_data(data text, key text)
RETURNS text AS $$
BEGIN
    RETURN pgp_sym_decrypt(decode(data, 'escape'), key);
END;
$$ LANGUAGE plpgsql;
