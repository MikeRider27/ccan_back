-- ALTER IN inventory.history
alter table inventory.history
    add num_lot varchar(50);

-- ALTER IN audit.inventory_history
alter table audit.inventory_history
    add num_lot varchar(50);

-- ALTER IN inventory.dispatch_medications
alter table inventory.dispatch_medications
    add num_lot varchar(50);

-- ALTER IN audit.inventory_dispatch_medications
alter table audit.inventory_dispatch_medications
    add num_lot varchar(50);

-- ALTER IN inventory.deposit_movement
alter table inventory.deposit_movement
    add num_lot varchar(50);

-- ALTER IN audit.inventory_deposit_movement
alter table audit.inventory_deposit_movement
    add num_lot varchar(50);

-- ALTER IN inventory.entries
alter table inventory.entries
    add num_lot varchar(50);

-- ALTER IN audit.inventory_entries
alter table audit.inventory_entries
    add num_lot varchar(50);

-- ALTER IN public.patient
alter table public.patient
    alter column birthdate drop not null;