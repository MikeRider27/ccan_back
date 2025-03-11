CREATE TABLE public.treatment_scheme_product (
    id                          BIGSERIAL PRIMARY KEY,
    uuid                        UUID NOT NULL DEFAULT UUID_GENERATE_V4(),
    treatment_scheme_id         BIGINT NOT NULL,
    product_id                  BIGINT NOT NULL,
    administration_route_id     BIGINT,
    calculation_type_id         BIGINT,
    frequency_id                BIGINT,
    note                        TEXT,
    adjustable                  BOOL,
    adjust_comment              BOOL,
    status                      SMALLINT DEFAULT 1,
    loading_dose                DECIMAL(10,2),
    session_dose                DECIMAL(10,2),
    infusion_dose               DECIMAL(10,2),
    index                       SMALLINT,
    created_user_id             BIGINT NOT NULL,
    edited_user_id              BIGINT NOT NULL,
    created_at                  TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    edited_at                   TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_treatment_scheme_product_uuid UNIQUE (uuid),
    FOREIGN KEY (treatment_scheme_id) REFERENCES treatment_scheme (id),
    FOREIGN KEY (product_id) REFERENCES product (id),
    FOREIGN KEY (administration_route_id) REFERENCES parameter (id),
    FOREIGN KEY (calculation_type_id) REFERENCES parameter (id),
    FOREIGN KEY (frequency_id) REFERENCES parameter (id),
    FOREIGN KEY (created_user_id) REFERENCES "user" (id),
    FOREIGN KEY (edited_user_id) REFERENCES "user" (id)
);

INSERT INTO permission (description) VALUES
     ('treatment_scheme_product_get'),
     ('treatment_scheme_product_list'),
     ('treatment_scheme_product_insert'),
     ('treatment_scheme_product_update'),
     ('treatment_scheme_product_delete');

CREATE TRIGGER treatment_scheme_product_audit AFTER INSERT OR UPDATE OR DELETE ON public.treatment_scheme_product FOR EACH ROW EXECUTE PROCEDURE audit.if_modified_func();


