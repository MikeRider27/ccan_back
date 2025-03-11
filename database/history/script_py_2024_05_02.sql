-- ALTER IN public.medicine
ALTER TABLE public.medicine
    ADD generic_name varchar(200);

-- ALTER IN audit.audit_medicine
ALTER TABLE audit.audit_medicine
    ADD generic_name varchar(200);

-- ALTER IN public.audit_medicine()
CREATE OR REPLACE FUNCTION public.audit_medicine() RETURNS trigger
    SECURITY DEFINER
    LANGUAGE plpgsql
AS
$$
DECLARE
    __DELETE char(6);
    __INSERT char(6);
    __UPDATE char(6);
BEGIN
    __DELETE := 'DELETE';
    __INSERT := 'INSERT';
    __UPDATE := 'UPDATE';

    IF (TG_OP = __DELETE) THEN
        INSERT INTO audit.audit_medicine(id,
                                         description,
                                         code,
                                         concentration,
                                         pharmaceutical_form,
                                         via_admin,
                                         presentation,
                                         code_dgc,
                                         state,
                                         date_create,
                                         user_create,
                                         date_modify,
                                         user_modify,
                                         stock_control,
                                         generic_name,
                                         audit_event,
                                         audit_date_time,
                                         audit_user,
                                         audit_client_ip)
        VALUES (old.id,
                old.description,
                old.code,
                old.concentration,
                old.pharmaceutical_form,
                old.via_admin,
                old.presentation,
                old.code_dgc,
                old.state,
                old.date_create,
                old.user_create,
                old.date_modify,
                old.user_modify,
                old.stock_control,
                old.generic_name,
                SUBSTR(TG_OP, 1, 1),
                CURRENT_TIMESTAMP,
                SESSION_USER,
                INET_CLIENT_ADDR());
        RETURN OLD;

    ELSE

        INSERT INTO audit.audit_medicine(id,
                                         description,
                                         code,
                                         concentration,
                                         pharmaceutical_form,
                                         via_admin,
                                         presentation,
                                         code_dgc,
                                         state,
                                         date_create,
                                         user_create,
                                         date_modify,
                                         user_modify,
                                         stock_control,
                                         generic_name,
                                         audit_event,
                                         audit_date_time,
                                         audit_user,
                                         audit_client_ip)
        VALUES (new.id,
                new.description,
                new.code,
                new.concentration,
                new.pharmaceutical_form,
                new.via_admin,
                new.presentation,
                new.code_dgc,
                new.state,
                new.date_create,
                new.user_create,
                new.date_modify,
                new.user_modify,
                new.stock_control,
                new.generic_name,
                SUBSTR(TG_OP, 1, 1),
                CURRENT_TIMESTAMP,
                SESSION_USER,
                INET_CLIENT_ADDR());
        RETURN NEW;

    END IF;
END
$$;


-- Alter in inventory.lot
ALTER TABLE inventory.lot
    ADD origin varchar(30);

-- Alter in inventory.entries
alter table inventory.entries
    add origin varchar(30);

alter table inventory.lot
    add date timestamp(0);
