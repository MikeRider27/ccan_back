CREATE TABLE treatment_follow_up
(
    id                                 bigserial NOT NULL
        CONSTRAINT treatment_follow_up_pk
            PRIMARY KEY,
    treatment_plan_id                  bigint
        CONSTRAINT treatment_follow_up_treatment_plan_id_fk
            REFERENCES treatment_plan,
    follow_up_date                     date,
    last_cancer_control_date           date,
    type_treatment                     varchar(30),
    breast                             varchar(30),
    armpit                             boolean,
    suspension_treatment               varchar(30),
    suspension_treatment_reason        text,
    suspension_treatment_custom_reason text,
    congestive_heart_failure           boolean,
    fevi_follow_up_date                date,
    fevi_value                         integer,
    fevi_trastuzumab_dose              integer,
    other_severe_adverse_events        boolean,
    other_severe_adverse_events_detail text,
    other_complementary_studies        text,
    dose_adjustment                    boolean,
    dose_adjustment_reason             varchar(100),
    trastuzumab_dose                   integer,
    every_three_weeks                  boolean,
    weekly                             boolean,
    comentaries                        text,
    doctor_id                          bigint
);

ALTER TABLE treatment_follow_up
    ADD CONSTRAINT treatment_follow_up_doctor_id_fk
        FOREIGN KEY (doctor_id) REFERENCES doctor;