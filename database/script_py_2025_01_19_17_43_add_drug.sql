CREATE TABLE public.drug
(
    id                  BIGSERIAL PRIMARY KEY,
    uuid                UUID NOT NULL DEFAULT UUID_GENERATE_V4(),
    generic_name        VARCHAR(255) NOT NULL,
    therapeutic_action  TEXT,
    category_id         BIGINT,
    status              SMALLINT DEFAULT 1,
    created_user_id     BIGINT NOT NULL,
    edited_user_id      BIGINT NOT NULL,
    created_at          TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    edited_at           TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_drug_uuid UNIQUE (uuid),
    CONSTRAINT uq_drug_generic_name UNIQUE (generic_name),
    FOREIGN KEY (category_id) REFERENCES parameter (id),
    FOREIGN KEY (created_user_id) REFERENCES "user" (id),
    FOREIGN KEY (edited_user_id) REFERENCES "user" (id)
);

INSERT INTO permission (description) VALUES
    ('drug_get'),
    ('drug_list'),
    ('drug_insert'),
    ('drug_update'),
    ('drug_delete');

CREATE TRIGGER drug_audit AFTER INSERT OR UPDATE OR DELETE ON public.drug FOR EACH ROW EXECUTE PROCEDURE audit.if_modified_func();
