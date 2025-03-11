CREATE TABLE public.treatment_request (
    id                          BIGSERIAL PRIMARY KEY,
    uuid                        UUID NOT NULL DEFAULT UUID_GENERATE_V4(),
    hospital_id                 BIGINT NOT NULL,
    patient_id                  BIGINT NOT NULL,
    protocol_id                 BIGINT,
    specialty_id                BIGINT,
    diagnosis_id                BIGINT,
    topography_id               BIGINT,
    morphology_id               BIGINT,
    stage_id                    BIGINT,
    criteria_id                 BIGINT,
    date                        TIMESTAMP WITH TIME ZONE,
    is_urgent                   BOOL,
    status                      SMALLINT DEFAULT 1,
    comment                     TEXT,
    patient_weight              DECIMAL(5,2),
    patient_height              DECIMAL(5,2),
    body_surface_area           DECIMAL(5,2),
    created_at                  TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    edited_at                   TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_user_id             BIGINT NOT NULL,
    edited_user_id              BIGINT NOT NULL,
    CONSTRAINT uq_treatment_request_uuid UNIQUE (uuid),
    FOREIGN KEY (hospital_id) REFERENCES hospital (id),
    FOREIGN KEY (patient_id) REFERENCES patient (id),
    FOREIGN KEY (protocol_id) REFERENCES parameter (id),
    FOREIGN KEY (specialty_id) REFERENCES specialty (id),
    FOREIGN KEY (diagnosis_id) REFERENCES diagnosis (id),
    FOREIGN KEY (topography_id) REFERENCES cie_o_topography (id),
    FOREIGN KEY (stage_id) REFERENCES parameter (id),
    FOREIGN KEY (morphology_id) REFERENCES cie_o_morphology (id),
    FOREIGN KEY (criteria_id) REFERENCES parameter (id),
    FOREIGN KEY (created_user_id) REFERENCES "user" (id),
    FOREIGN KEY (edited_user_id) REFERENCES "user" (id)
);

INSERT INTO permission (description) VALUES
     ('treatment_request_get'),
     ('treatment_request_list'),
     ('treatment_request_insert'),
     ('treatment_request_update'),
     ('treatment_request_delete');

CREATE TRIGGER treatment_request_audit AFTER INSERT OR UPDATE OR DELETE ON public.treatment_request FOR EACH ROW EXECUTE PROCEDURE audit.if_modified_func();


