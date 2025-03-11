-- Audits y triggers para PY-CO-GH

--Table PY-GH
CREATE TABLE audit.public_message
(
    audit_event     char,
    audit_user      varchar(30),
    audit_date_time timestamp WITH TIME ZONE,
    audit_client_ip inet,
    id              bigint,
    asunto        text,
    mensaje       text,
    fecha_mensaje timestamp(0) DEFAULT NOW(),
    emisor_id     bigint,
    isborrado     boolean      DEFAULT FALSE,
    id_hospital   integer,
    patient_id    bigint
);

--Table CO
CREATE TABLE audit.public_message
(
    audit_event     char,
    audit_user      varchar(30),
    audit_date_time timestamp WITH TIME ZONE,
    audit_client_ip inet,
    id              bigint,
    asunto        text,
    mensaje       text,
    fecha_mensaje timestamp(0) DEFAULT NOW(),
    emisor_id     bigint,
    isborrado     boolean      DEFAULT FALSE,
    role_type     text,
    id_entidad   integer,
    patient_id    bigint
);

-- PY-CO-GH
CREATE FUNCTION audit_message() RETURNS trigger
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
	if ( TG_OP = __DELETE  ) then
 		INSERT INTO audit.public_message SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;
	else
 		INSERT INTO audit.public_message SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if;
 END
 $$;

-- PY-CO-GH
CREATE TRIGGER audit_message_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.message
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_message();

-- PY-CO-GH
CREATE TABLE audit.public_destinatarios
(
    audit_event      char,
    audit_user       varchar(30),
    audit_date_time  timestamp WITH TIME ZONE,
    audit_client_ip  inet,
    id               bigint,
    message_id       bigint,
    destinatarios_id bigint,
    estado_id        bigint,
    isborrado        boolean DEFAULT FALSE
);

-- PY-CO-GH
CREATE FUNCTION audit_destinatarios() RETURNS trigger
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
	if ( TG_OP = __DELETE  ) then
 		INSERT INTO audit.public_destinatarios SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;
	else
 		INSERT INTO audit.public_destinatarios SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if;
 END
 $$;

-- PY-CO-GH
CREATE TRIGGER audit_destinatarios_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.destinatarios
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_destinatarios();


-- PY-CO-GH
CREATE TABLE audit.public_notificaciones
(
    audit_event     char,
    audit_user      varchar(30),
    audit_date_time timestamp WITH TIME ZONE,
    audit_client_ip inet,
    id              bigint,
    user_id         bigint,
    message_id      bigint,
    leida           boolean
);

-- PY-CO-GH
CREATE FUNCTION audit_notificaciones() RETURNS trigger
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
	if ( TG_OP = __DELETE  ) then
 		INSERT INTO audit.public_notificaciones SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;
	else
 		INSERT INTO audit.public_notificaciones SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if;
 END
 $$;

-- PY-CO-GH
CREATE TRIGGER audit_notificaciones_all
  AFTER INSERT OR UPDATE OR DELETE
  ON public.notificaciones
  FOR EACH ROW
  EXECUTE PROCEDURE public.audit_notificaciones();