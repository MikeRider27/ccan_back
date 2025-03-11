CREATE TABLE public.treatment_request_scheme (
    id                              BIGSERIAL PRIMARY KEY,
    uuid                            UUID NOT NULL DEFAULT UUID_GENERATE_V4(),
    treatment_request_id            BIGINT NOT NULL,
    treatment_scheme_id             BIGINT NOT NULL,
    base_treatment_scheme_id        BIGINT,
    previous_treatment_scheme_id    BIGINT,
    CONSTRAINT uq_treatment_request_scheme_uuid UNIQUE (uuid),
    FOREIGN KEY (treatment_request_id) REFERENCES treatment_request (id),
    FOREIGN KEY (treatment_scheme_id) REFERENCES treatment_scheme (id),
    FOREIGN KEY (base_treatment_scheme_id) REFERENCES treatment_scheme (id),
    FOREIGN KEY (previous_treatment_scheme_id) REFERENCES treatment_scheme (id)
);

INSERT INTO permission (description) VALUES
     ('treatment_request_scheme_get'),
     ('treatment_request_scheme_list'),
     ('treatment_request_scheme_insert'),
     ('treatment_request_scheme_update'),
     ('treatment_request_scheme_delete');

CREATE TRIGGER treatment_request_scheme_audit AFTER INSERT OR UPDATE OR DELETE ON public.treatment_request_scheme FOR EACH ROW EXECUTE PROCEDURE audit.if_modified_func();


