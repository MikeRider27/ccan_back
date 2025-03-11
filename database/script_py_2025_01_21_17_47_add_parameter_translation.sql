CREATE TABLE public.parameter_translation (
    id BIGSERIAL PRIMARY KEY,
    uuid UUID NOT NULL DEFAULT UUID_GENERATE_V4(),
    parameter_id BIGINT NOT NULL,
    language_code VARCHAR(10) NOT NULL,
    value VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_parameter_translation_parameter_id FOREIGN KEY (parameter_id) REFERENCES parameter(id) ON DELETE CASCADE
);

CREATE INDEX idx_parameter_domain ON parameter (domain);

CREATE TRIGGER parameter_translation_audit AFTER INSERT OR UPDATE OR DELETE ON public.parameter_translation FOR EACH ROW EXECUTE PROCEDURE audit.if_modified_func();

