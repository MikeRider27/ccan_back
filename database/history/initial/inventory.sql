CREATE SCHEMA inventory;

CREATE TABLE inventory.manufacturer
(
    id          bigserial PRIMARY KEY,
    name        varchar(100)                                 NOT NULL,
    county_id   bigserial
        CONSTRAINT manufacturer_country REFERENCES public.country,
    state_id    bigint                                       NOT NULL
        CONSTRAINT manufacturer_state REFERENCES public.parameter,
    date_create timestamp(0) WITHOUT TIME ZONE DEFAULT NOW() NOT NULL,
    user_create varchar(30)                                  NOT NULL,
    date_modify timestamp(0) WITHOUT TIME ZONE,
    user_modify varchar(30)
);

CREATE TABLE inventory.supplier
(
    id          bigserial PRIMARY KEY,
    name        varchar(100)                                 NOT NULL,
    county_id   bigserial
        CONSTRAINT supplier_country REFERENCES public.country,
    address     varchar(100),
    phone       varchar(100),
    email       varchar(20),
    description varchar(500),
    state_id    bigint                                       NOT NULL
        CONSTRAINT supplier_state REFERENCES public.parameter,
    date_create timestamp(0) WITHOUT TIME ZONE DEFAULT NOW() NOT NULL,
    user_create varchar(30)                                  NOT NULL,
    date_modify timestamp(0) WITHOUT TIME ZONE,
    user_modify varchar(30)
);

CREATE TABLE inventory.deposit
(
    id          bigserial PRIMARY KEY,
    code        varchar(50)                                  NOT NULL,
    name        varchar(100)                                 NOT NULL,
    description varchar(500),
    city        varchar(20),
    address     varchar(100),
    email       varchar(20),
    phone       varchar(30),
    date_create timestamp(0) WITHOUT TIME ZONE DEFAULT NOW() NOT NULL,
    user_create varchar(30)                                  NOT NULL,
    date_modify timestamp(0) WITHOUT TIME ZONE,
    user_modify varchar(30)
);

CREATE TABLE inventory.lot
(
    id          bigserial PRIMARY KEY,
    num_lot     varchar(50)                                  NOT NULL,
    date_create timestamp(0) WITHOUT TIME ZONE DEFAULT NOW() NOT NULL,
    user_create varchar(30)                                  NOT NULL,
    date_modify timestamp(0) WITHOUT TIME ZONE,
    user_modify varchar(30)
);

CREATE TABLE inventory.lot_detail
(
    id                 bigserial PRIMARY KEY,
    lot_id             bigint           NOT NULL
        CONSTRAINT stock_medicine_lote REFERENCES inventory.lot,
    deposit_id         bigint           NOT NULL
        CONSTRAINT stock_medicine_deposit REFERENCES inventory.deposit,
    medicine_id        bigint           NOT NULL
        CONSTRAINT stock_medicine_medicine REFERENCES public.medicine,
    description        varchar(500),
    expiration_date    timestamp(0) WITHOUT TIME ZONE,
    quantity           double precision NOT NULL,
    manufacturer_id    bigint
        CONSTRAINT lot_detail_manufacturer REFERENCES inventory.manufacturer,
    manufacturing_date timestamp(0) WITHOUT TIME ZONE,
    supplier_id        bigint
        CONSTRAINT lot_detail_supplier REFERENCES inventory.supplier,
    storage_conditions varchar(500),
    observation        varchar(500)
);

CREATE TABLE inventory.stock
(
    id          bigserial PRIMARY KEY,
    medicine_id bigint UNIQUE    NOT NULL
        CONSTRAINT stock_medicine_medicine REFERENCES public.medicine,
    quantity    double precision NOT NULL,
    state_id    bigint           NOT NULL
        CONSTRAINT stock_medicine_state REFERENCES public.parameter
);


CREATE TABLE inventory.deposit_stock
(
    id         bigserial PRIMARY KEY,
    deposit_id bigserial        NOT NULL
        CONSTRAINT stock_medicine_deposit REFERENCES inventory.deposit,
    stock_id   bigserial        NOT NULL
        CONSTRAINT deposit_stock_stock REFERENCES inventory.stock,
    quantity   double precision NOT NULL,
    CONSTRAINT deposit_stock_unique UNIQUE (deposit_id, stock_id)
);

CREATE TABLE inventory.deposit_movement
(
    id                   bigserial PRIMARY KEY,
    deposit_stock_in_id  bigint                                       NOT NULL
        CONSTRAINT deposit_movement_deposit_stock_in REFERENCES inventory.deposit_stock,
    deposit_stock_out_id bigint                                       NOT NULL
        CONSTRAINT deposit_movement_deposit_stock_out REFERENCES inventory.deposit_stock,
    quantity             double precision                             NOT NULL,
    date_create          timestamp(0) WITHOUT TIME ZONE DEFAULT NOW() NOT NULL,
    user_create          varchar(30)                                  NOT NULL
);

CREATE TABLE inventory.dispatch_medications
(
    id                bigserial PRIMARY KEY,
    deposit_stock_id  bigint                                       NOT NULL
        CONSTRAINT dispatch_medications_deposit_stock REFERENCES inventory.deposit_stock,
    patient_id        bigint                                       NOT NULL
        CONSTRAINT dispatch_medications_patient REFERENCES public.patient,
    medicine_id       bigint
        CONSTRAINT dispatch_medications_medicine REFERENCES public.medicine,
    treatment_program boolean                                      NOT NULL,
    quantity          double precision                             NOT NULL,
    origin            varchar(30)                                  NOT NULL,
    date_create       timestamp(0) WITHOUT TIME ZONE DEFAULT NOW() NOT NULL,
    user_create       varchar(30)                                  NOT NULL
);

CREATE TABLE inventory.history
(
    id               bigserial PRIMARY KEY,
    deposit_stock_id bigint                                       NOT NULL
        CONSTRAINT history_deposit_stock REFERENCES inventory.deposit_stock,
    quantity         double precision                             NOT NULL,
    event_id         bigint                                       NOT NULL
        CONSTRAINT history_event REFERENCES public.parameter,
    description      varchar(500),
    date_create      timestamp(0) WITHOUT TIME ZONE DEFAULT NOW() NOT NULL,
    user_create      varchar(30)                                  NOT NULL
);

--------------
-- ADD DATA --
--------------
INSERT INTO public.parameter (domain, value, active, code)
VALUES
       ('STOCK_STATE', 'ACTIVE', TRUE, 'A'),
       ('STOCK_STATE', 'INACTIVE', TRUE, 'I'),
       ('MANUFACTURER_STATE', 'ACTIVE', TRUE, 'A'),
       ('MANUFACTURER_STATE', 'INACTIVE', TRUE, 'I'),
       ('SUPPLIER_STATE', 'ACTIVE', TRUE, 'A'),
       ('SUPPLIER_STATE', 'INACTIVE', TRUE, 'I'),
       ('STOCK_HISTORY_EVENT', 'Add by Lot', TRUE, 'ADD_BY_LOTE'),
       ('STOCK_HISTORY_EVENT', 'Remove by Lot', TRUE, 'REMOVE_BY_LOTE'),
       ('STOCK_HISTORY_EVENT', 'Stock Adjustment', TRUE, 'AJUST_STOCK'),
       ('STOCK_HISTORY_EVENT', 'Deposit Movement', TRUE, 'DEPOSIT_MOV'),
       ('STOCK_HISTORY_EVENT', 'Medicine dispensed to patient', TRUE, 'DISPENSE_PAT'),
       ('STOCK_HISTORY_EVENT', 'Revert medicine dispensed to patient', TRUE, 'DISPENSE_REVERT')
;
