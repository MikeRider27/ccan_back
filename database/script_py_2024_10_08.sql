-- Agregación de la columna uuid para la tabla patient
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

ALTER TABLE public.patient
ADD COLUMN uuid UUID NOT NULL DEFAULT uuid_generate_v4();

ALTER TABLE audit.public_patient
    ADD uuid UUID;


----------------------------------------------------------------------------------
-- TRUNCAR TODAS LAS TABLAS DEL ESQUEMA INVENTORY Y REINICIAR LOS SECUENCIADORES --
-- DO
-- $$
-- DECLARE
--     table_name text;
-- BEGIN
--     -- Iterar sobre todas las tablas del esquema 'tu_esquema'
--     FOR table_name IN
--         SELECT tablename FROM pg_tables WHERE schemaname = 'inventory'
--     LOOP
--         -- Ejecutar TRUNCATE en cada tabla, reiniciar las secuencias automáticamente
--         EXECUTE 'TRUNCATE TABLE ' || 'inventory.' || table_name || ' RESTART IDENTITY CASCADE';
--     END LOOP;
-- END
-- $$;
----------------------------------------------------------------------------------

-- Borrar las columnas creadas anteriormente para reemplazarlas
-- por una relacion directa a la tabla, FK a lot
-- ALTER TABLE inventory.dispatch_medications
-- DROP COLUMN num_lot;
--
-- ALTER TABLE audit.inventory_dispatch_medications
-- DROP COLUMN num_lot;
--
-- ALTER TABLE inventory.deposit_movement
-- DROP COLUMN num_lot;
--
-- ALTER TABLE audit.inventory_deposit_movement
-- DROP COLUMN num_lot;
--
-- ALTER TABLE inventory.entries
-- DROP COLUMN num_lot;
--
-- ALTER TABLE audit.inventory_entries
-- DROP COLUMN num_lot;


-- ALTER IN inventory.dispatch_medications
ALTER TABLE inventory.dispatch_medications
    ADD COLUMN lote_id BIGINT;
ALTER TABLE inventory.dispatch_medications
ADD CONSTRAINT fk_lote
FOREIGN KEY (lote_id)
REFERENCES inventory.lot(id);

-- ALTER IN audit.inventory_dispatch_medications
ALTER TABLE audit.inventory_dispatch_medications
    ADD COLUMN lote_id BIGINT;


-- ALTER IN inventory.deposit_movement
ALTER TABLE inventory.deposit_movement
    ADD COLUMN lote_id BIGINT;
ALTER TABLE inventory.deposit_movement
ADD CONSTRAINT fk_lote
FOREIGN KEY (lote_id)
REFERENCES inventory.lot(id);

-- ALTER IN audit.inventory_deposit_movement
ALTER TABLE audit.inventory_deposit_movement
    ADD COLUMN lote_id BIGINT;


-- ALTER IN inventory.entries
ALTER TABLE inventory.entries
    ADD COLUMN lote_id BIGINT;
ALTER TABLE inventory.entries
ADD CONSTRAINT fk_lote
FOREIGN KEY (lote_id)
REFERENCES inventory.lot(id);

-- ALTER IN audit.inventory_entries
ALTER TABLE audit.inventory_entries
    ADD COLUMN lote_id BIGINT;


-- Tabla Deposit-Lot
CREATE SEQUENCE deposit_lot_id_seq;
CREATE TABLE inventory.deposit_lot
(
    id                  bigint DEFAULT NEXTVAL('deposit_lot_id_seq'::regclass)
        NOT NULL
        CONSTRAINT deposit_lot_pk PRIMARY KEY,
    deposit_stock_id BIGINT,
    FOREIGN KEY (deposit_stock_id) REFERENCES "inventory"."deposit_stock"(id),
    lote_id BIGINT,
    FOREIGN KEY (lote_id) REFERENCES "inventory"."lot"(id),
    medicine_id BIGINT,
    FOREIGN KEY (medicine_id) REFERENCES "medicine"(id),
    quantity INT
);
ALTER TABLE inventory.deposit_lot
    OWNER TO postgres;

-- Audit de Deposit-Lot
CREATE TABLE audit.inventory_deposit_lot(
	audit_event bpchar(1) NULL,
	audit_user varchar(30) NULL,
	audit_date_time timestamptz NULL,
	audit_client_ip inet NULL,
	id BIGINT,
    deposit_stock_id BIGINT,
    lote_id BIGINT,
    medicine_id BIGINT,
    quantity INT
);

CREATE FUNCTION inventory.audit_deposit_lot() RETURNS trigger
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
 		INSERT INTO audit.inventory_deposit_lot SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),OLD.*;
		return OLD;
	else
 		INSERT INTO audit.inventory_deposit_lot SELECT substr(TG_OP ,1,1),session_user,current_timestamp,inet_client_addr(),NEW.*;
		return NEW;
	end if;
 END
 $$;

CREATE TRIGGER audit_deposit_lot
  AFTER INSERT OR UPDATE OR DELETE
  ON inventory.deposit_lot
  FOR EACH ROW
  EXECUTE PROCEDURE inventory.audit_deposit_lot();



-- Nuevos permisos para la nueva tabla
INSERT INTO public."permission" (description)
VALUES ('deposit_lot_get'),
       ('deposit_lot_update'),
       ('deposit_lot_delete'),
       ('deposit_lot_list'),
       ('deposit_lot_insert'),
       ('deposit_lot_search');

-- INSERCION PERMISSION TO ROLE
INSERT INTO role_permission (role_id, permission_id)
SELECT (SELECT id FROM role WHERE role.description = 'AUDITOR'),
       p.id
FROM permission p
WHERE p.description IN (
                        'deposit_lot_get',
                        'deposit_lot_list',
                        'deposit_lot_search'
                        );

INSERT INTO role_permission (role_id, permission_id)
SELECT (SELECT id FROM role WHERE role.description = 'INVENTARIO'),
       p.id
FROM permission p
WHERE p.description IN (
                        'deposit_lot_get',
                        'deposit_lot_update',
                        'deposit_lot_delete',
                        'deposit_lot_list',
                        'deposit_lot_insert',
                        'deposit_lot_search'
                        );

-- Se agrega el campo origin a deposit
ALTER TABLE inventory.deposit
    ADD origin varchar(30);

ALTER TABLE audit.inventory_deposit
    ADD origin varchar(30);
