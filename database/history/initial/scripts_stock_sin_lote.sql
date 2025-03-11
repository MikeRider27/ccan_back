alter table inventory.lot_detail
    rename to entries;
alter table inventory.entries
    drop constraint stock_medicine_lote;

create table inventory.entries_lot_stock
(
    id         bigint not null
        constraint entries_lot_stock_pk
            primary key,
    lot_id     bigint,
    stock_id   bigint,
    entries_id bigint
);
alter table inventory.entries_lot_stock
    add constraint entries_lot_stock_entries_id_fk
        foreign key (entries_id) references inventory.entries;

alter table inventory.entries_lot_stock
    add constraint entries_lot_stock_lot_id_fk
        foreign key (lot_id) references inventory.lot;

alter table inventory.entries_lot_stock
    add constraint entries_lot_stock_stock_id_fk
        foreign key (stock_id) references inventory.stock;

alter table inventory.entries_lot_stock
    rename constraint entries_lot_stock_pk to entries_lot_pk;

alter table inventory.entries_lot_stock
    drop constraint entries_lot_stock_stock_id_fk;

alter table inventory.entries_lot_stock
    drop column stock_id;

alter table inventory.entries_lot_stock
    rename to entries_lot;

alter table inventory.entries_lot
    rename constraint entries_lot_stock_entries_id_fk to entries_lot_entries_id_fk;

alter table inventory.entries_lot
    rename constraint entries_lot_stock_lot_id_fk to entries_lot_lot_id_fk;
create table inventory.entries_deposit_stock
(
    id               bigint
        constraint entries_deposit_stock_pk
            primary key,
    entries_id       bigint,
    deposit_stock_id bigint
);


alter table inventory.entries_deposit_stock
    add constraint entries_deposit_stock_deposit_stock_id_fk
        foreign key (deposit_stock_id) references inventory.deposit_stock;

alter table inventory.entries_deposit_stock
    add constraint entries_deposit_stock_entries_id_fk
        foreign key (entries_id) references inventory.entries;


-- INSERT PERMISSIONS
INSERT INTO public.permission (description)
VALUES ('entries_deposit_stock_list'),
       ('entries_deposit_stock_search'),
       ('entries_deposit_stock_get'),
       ('entries_deposit_stock_insert'),
       ('entries_deposit_stock_update'),
       ('entries_deposit_stock_delete');

-- INSERT PERMISSIONS
INSERT INTO public.permission (description)
VALUES ('entries_lot_list'),
       ('entries_lot_search'),
       ('entries_lot_get'),
       ('entries_lot_insert'),
       ('entries_lot_update'),
       ('entries_lot_delete');

create sequence inventory.entries_lot_seq
    as integer;

alter table inventory.entries_lot
    alter column id set default nextval('inventory.entries_lot_seq'::regclass);

create sequence inventory.entries_deposit_stock_seq;
alter table inventory.entries_deposit_stock
    alter column id set default nextval('inventory.entries_deposit_stock_seq'::regclass);

--------------------------------
-- ALTER EN inventory.entries --
--------------------------------
alter table inventory.entries
    drop column lot_id;

------------------------------------
-- ALTER EN inventory.entries_lot --
------------------------------------
alter table inventory.entries_lot
    alter column lot_id set not null;

alter table inventory.entries_lot
    alter column entries_id set not null;

------------------------------
-- ALTER EN public.medicine --
------------------------------
alter table public.medicine
    add control boolean default false not null;

alter table public.medicine
    rename column control to stock_control;

---------------------------------------------
-- ALETR EN inventory.dispatch_medications --
---------------------------------------------
alter table inventory.dispatch_medications
    add date timestamp;

--------------------------------------------------
-- ALTER EN public.medicine_treatment_follow_up --
--------------------------------------------------
alter table public.medicine_treatment_follow_up
    add deposit_stock_id bigint;

alter table public.medicine_treatment_follow_up
    add constraint medicine_treatment_follow_up_deposit_stock_id_fk
        foreign key (deposit_stock_id) references inventory.deposit_stock;

---------------------------------------------
-- ALTER EN inventory.dispatch_medications --
---------------------------------------------
alter table inventory.dispatch_medications
    drop column treatment_program;

-- ADD IN PARAMETER
INSERT INTO public.parameter (domain, value, active, code)
VALUES ('STOCK_HISTORY_EVENT', 'Add by Entry', TRUE, 'ADD_BY_ENTRY');

INSERT INTO public.parameter (domain, value, active, code)
VALUES ('STOCK_HISTORY_EVENT', 'Delete by Entry', TRUE, 'REMOVE_BY_ENTRY');
INSERT INTO public.parameter (domain, value, active, code)
VALUES ('STOCK_HISTORY_EVENT', 'Delete by Medicine Treatment FollowUp', TRUE, 'REMOVE_BY_M_T_F_U');

INSERT INTO public.parameter (domain, value, active, code)
VALUES ('STOCK_HISTORY_EVENT', 'Add by Medicine Treatment FollowUp', TRUE, 'ADD_BY_M_T_F_U');
alter table inventory.entries
    add date timestamp;