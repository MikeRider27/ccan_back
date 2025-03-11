CREATE TABLE public.treatment_scheme (
    id                                      BIGSERIAL PRIMARY KEY,
    uuid                                    UUID NOT NULL DEFAULT UUID_GENERATE_V4(),
    hospital_id                             BIGINT NOT NULL,
    name                                    VARCHAR(255) NOT NULL,
    description                             TEXT,
    periodicity_id                          BIGINT,
    series_count                            SMALLINT,
    pre_medication                          TEXT,
    medication                              TEXT,
    post_medication                         TEXT,
    category_id                             BIGINT, -- only present when represents a "base scheme"
    notes                                   TEXT,
    administration_time                     SMALLINT,
    preparation_instructions                TEXT,
    status                                  SMALLINT DEFAULT 1,
    type                                    SMALLINT DEFAULT 1, -- 1 for "base schema", 2 for "treatment request schema"
    created_user_id                         BIGINT NOT NULL,
    edited_user_id                          BIGINT NOT NULL,
    created_at                              TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    edited_at                               TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_treatment_scheme_uuid UNIQUE (uuid),
    FOREIGN KEY (hospital_id) REFERENCES hospital (id),
    FOREIGN KEY (periodicity_id) REFERENCES parameter (id),
    FOREIGN KEY (category_id) REFERENCES parameter (id),
    FOREIGN KEY (created_user_id) REFERENCES "user" (id),
    FOREIGN KEY (edited_user_id) REFERENCES "user" (id)
);

INSERT INTO permission (description) VALUES
     ('treatment_scheme_get'),
     ('treatment_scheme_list'),
     ('treatment_scheme_insert'),
     ('treatment_scheme_update'),
     ('treatment_scheme_delete');

CREATE TRIGGER treatment_scheme_audit AFTER INSERT OR UPDATE OR DELETE ON public.treatment_scheme FOR EACH ROW EXECUTE PROCEDURE audit.if_modified_func();
