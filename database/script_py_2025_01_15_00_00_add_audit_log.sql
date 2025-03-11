CREATE TABLE audit.logged_actions (
    schema_name TEXT NOT NULL,
    table_name TEXT NOT NULL,
    user_name TEXT,
    action_ts TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    action TEXT NOT NULL CHECK (ACTION IN ('I','D','U')),
    original_data TEXT,
    new_data TEXT,
    query TEXT,
    client_ip INET
) WITH (FILLFACTOR=100);

CREATE INDEX logged_actions_schema_table_idx
    ON audit.logged_actions(((schema_name||'.'||table_name)::TEXT));
CREATE INDEX logged_actions_action_ts_idx
    ON audit.logged_actions(action_ts);
CREATE INDEX logged_actions_action_idx
    ON audit.logged_actions(action);

CREATE OR REPLACE FUNCTION audit.if_modified_func() RETURNS trigger AS $body$
DECLARE
    v_old_data TEXT;
    v_new_data TEXT;
    v_user_name TEXT;
BEGIN
    v_user_name := COALESCE(CURRENT_SETTING('myapp.current_username', true), SESSION_USER);
    IF (TG_OP = 'UPDATE') THEN
        v_old_data := row_to_json(OLD.*);
        v_new_data := row_to_json(NEW.*);
        INSERT INTO audit.logged_actions (schema_name, table_name, user_name, action, original_data, new_data, query, client_ip)
        VALUES (TG_TABLE_SCHEMA::TEXT, TG_TABLE_NAME::TEXT, v_user_name, SUBSTRING(TG_OP, 1, 1), v_old_data, v_new_data, CURRENT_QUERY(), INET_CLIENT_ADDR());
        RETURN NEW;
    ELSIF (TG_OP = 'DELETE') THEN
        v_old_data := row_to_json(OLD.*);
        INSERT INTO audit.logged_actions (schema_name, table_name, user_name, action, original_data, query, client_ip)
        VALUES (TG_TABLE_SCHEMA::TEXT, TG_TABLE_NAME::TEXT, v_user_name, SUBSTRING(TG_OP, 1, 1), v_old_data, CURRENT_QUERY(), INET_CLIENT_ADDR());
        RETURN OLD;
    ELSIF (TG_OP = 'INSERT') THEN
        v_new_data := row_to_json(NEW.*);
        INSERT INTO audit.logged_actions (schema_name, table_name, user_name, action, new_data, query, client_ip)
        VALUES (TG_TABLE_SCHEMA::TEXT, TG_TABLE_NAME::TEXT, v_user_name, SUBSTRING(TG_OP, 1, 1), v_new_data, CURRENT_QUERY(), INET_CLIENT_ADDR());
        RETURN NEW;
    ELSE
        RAISE WARNING '[AUDIT.IF_MODIFIED_FUNC] - Other action occurred: %, at %', TG_OP, NOW();
        RETURN NULL;
    END IF;

EXCEPTION
    WHEN data_exception THEN
        RAISE WARNING '[AUDIT.IF_MODIFIED_FUNC] - UDF ERROR [DATA EXCEPTION] - SQLSTATE: %, SQLERRM: %', SQLSTATE,SQLERRM;
        RETURN NULL;
    WHEN unique_violation THEN
        RAISE WARNING '[AUDIT.IF_MODIFIED_FUNC] - UDF ERROR [UNIQUE] - SQLSTATE: %, SQLERRM: %', SQLSTATE,SQLERRM;
        RETURN NULL;
    WHEN others THEN
        RAISE WARNING '[AUDIT.IF_MODIFIED_FUNC] - UDF ERROR [OTHER] - SQLSTATE: %, SQLERRM: %', SQLSTATE,SQLERRM;
        RETURN NULL;
END;
$body$
    LANGUAGE plpgsql
    SECURITY DEFINER
    SET search_path = pg_catalog, audit;
