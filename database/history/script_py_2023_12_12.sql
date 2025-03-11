-- ALTER IN inventory.deposit
alter table inventory.deposit
    add hospital_id bigint;

alter table inventory.deposit
    add constraint deposit_hospital_id_fk
        foreign key (hospital_id) references public.hospital;

