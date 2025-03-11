INSERT INTO parameter (domain, value, active, code)
VALUES
    ('MESSAGE_STATE', 'NUEVO', true, 'nue'),
    ('MESSAGE_STATE', 'LEIDO', true, 'lei'),
    ('MESSAGE_STATE', 'RESPONDIDO', true, 'res'),
    ('MESSAGE_STATE', 'DEMORADO', true, 'dem');


CREATE SEQUENCE message_id_seq;

CREATE TABLE message
(
    id  bigint  DEFAULT NEXTVAL('message_id_seq'::regclass)
        NOT NULL CONSTRAINT message_pk PRIMARY KEY,
    asunto TEXT NOT NULL,
    mensaje TEXT NOT NULL,
    fecha_mensaje timestamp(0) DEFAULT NOW(),
    emisor_id BIGINT NOT NULL,
    FOREIGN KEY (emisor_id) REFERENCES "user"(id)
);

ALTER TABLE "message"
    OWNER TO postgres;

CREATE SEQUENCE notificacion_id_seq;

CREATE TABLE notificaciones
(
    id  bigint  DEFAULT NEXTVAL('notificacion_id_seq'::regclass)
        NOT NULL CONSTRAINT notificaciones_pk PRIMARY KEY,
    user_id BIGINT NOT NULL,
    message_id BIGINT NOT NULL,
    leida BOOLEAN,
    FOREIGN KEY (user_id) REFERENCES "user"(id),
    FOREIGN KEY (message_id) REFERENCES "message"(id)
);

ALTER TABLE "notificaciones"
    OWNER TO postgres;


CREATE SEQUENCE destinatarios_id_seq;

CREATE TABLE destinatarios
(
    id  bigint  DEFAULT NEXTVAL('destinatarios_id_seq'::regclass)
        NOT NULL CONSTRAINT destinatarios_pk PRIMARY KEY,
    estado_id BIGINT,
    message_id BIGINT NOT NULL,
    destinatarios_id BIGINT NOT NULL,
    FOREIGN KEY (estado_id) REFERENCES "parameter"(id),
    FOREIGN KEY (destinatarios_id) REFERENCES "user"(id),
    FOREIGN KEY (message_id) REFERENCES "message"(id)
);

ALTER TABLE "destinatarios"
    OWNER TO postgres;

----------------------------------
ALTER TABLE message
ADD COLUMN isBorrado BOOLEAN DEFAULT FALSE;

ALTER TABLE destinatarios
ADD COLUMN isBorrado BOOLEAN DEFAULT FALSE;