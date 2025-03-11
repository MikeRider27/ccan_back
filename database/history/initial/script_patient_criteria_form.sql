create table public.patient_inclusion_criteria
(
    id                                        bigserial
        constraint patient_inclusion_exclusion_criteria_pk
            primary key,
    patient_id                                bigint not null
        constraint patient_inclusion_exclusion_criteria_patient_id_fk
            references patient,
    treatment_type                            varchar(30),
    patient_inclusion_criteria_adjuvant_id    bigint
        constraint patient_inclusion_exclusion_criteria_adjuvant_id_fk
            references patient_inclusion_criteria_adjuvant_trastuzumab,
    patient_inclusion_criteria_neoadjuvant_id bigint
        constraint patient_inclusion_exclusion_criteria_neoadjuvant_id_fk
            references patient_inclusion_criteria_neoadjuvant_trastuzumab,
    has_signed_informed_consent               boolean,
    patient_received_document                         boolean,
    consent_obtained_through_dialogue                 boolean,
    has_received_sufficient_sufficient                boolean,
    has_asked_questions_and_can_continue_asking       boolean,
    informed_receive_permanent_continuous_information boolean,
    information_received_clear_complete               boolean,
    received_information_understandable_language      boolean,
    treatment_hospital_id                             bigint
);
-- Se elimina campos de la tabla patient criteria exclusion

alter table public.patient_exclusion_criteria
    drop column has_signed_informed_consent;

alter table public.patient_exclusion_criteria
    drop column patient_received_document;

alter table public.patient_exclusion_criteria
    drop column consent_obtained_through_dialogue;

alter table public.patient_exclusion_criteria
    drop column has_received_sufficient_sufficient;

alter table public.patient_exclusion_criteria
    drop column has_asked_questions_and_can_continue_asking;

alter table public.patient_exclusion_criteria
    drop column informed_receive_permanent_continuous_information;

alter table public.patient_exclusion_criteria
    drop column information_received_clear_complete;

alter table public.patient_exclusion_criteria
    drop column received_information_understandable_language;

alter table public.patient_exclusion_criteria
    drop column treatment_hospital_id;