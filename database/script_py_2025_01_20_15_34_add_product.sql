CREATE TABLE public.product
(
    id                      BIGSERIAL PRIMARY KEY,
    uuid                    UUID NOT NULL DEFAULT UUID_GENERATE_V4(),
    hospital_id             BIGINT NOT NULL,
    medicine_id             BIGINT,
    drug_id                 BIGINT,
    code                    VARCHAR(15) NOT NULL,
    description             VARCHAR(255),
    concentration           DECIMAL(10,2),
    concentration_unit_id   BIGINT,
    quantity                DECIMAL(10,2),
    quantity_unit_id        BIGINT,
    type_id                 BIGINT,
    status                  SMALLINT DEFAULT 1,
    premedication           TEXT,
    medication              TEXT,
    postmedication          TEXT,
    dose_limit              DECIMAL(10,2) DEFAULT 0,
    dose_unit_id            BIGINT,
    contraindications       TEXT,
    created_user_id         BIGINT NOT NULL,
    edited_user_id          BIGINT NOT NULL,
    created_at              TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    edited_at               TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_product_uuid UNIQUE (uuid),
    CONSTRAINT uq_hospital_id_code UNIQUE (hospital_id, code),
    FOREIGN KEY (hospital_id) REFERENCES hospital (id),
    FOREIGN KEY (medicine_id) REFERENCES medicine (id),
    FOREIGN KEY (drug_id) REFERENCES drug (id),
    FOREIGN KEY (concentration_unit_id) REFERENCES parameter (id),
    FOREIGN KEY (quantity_unit_id) REFERENCES parameter (id),
    FOREIGN KEY (type_id) REFERENCES parameter (id),
    FOREIGN KEY (dose_unit_id) REFERENCES parameter (id),
    FOREIGN KEY (created_user_id) REFERENCES "user" (id),
    FOREIGN KEY (edited_user_id) REFERENCES "user" (id)
);

INSERT INTO permission (description) VALUES
    ('product_get'),
    ('product_list'),
    ('product_insert'),
    ('product_update'),
    ('product_delete');

CREATE TRIGGER product_audit AFTER INSERT OR UPDATE OR DELETE ON public.product FOR EACH ROW EXECUTE PROCEDURE audit.if_modified_func();
