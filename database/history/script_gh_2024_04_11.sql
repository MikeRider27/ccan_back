-- FIX DATABASE
drop table public.treatment_order;

drop table public.additional_patient_information;

drop table public.medical_visit;

drop table public.medication;

drop table public.medicine_medication_order;

--ALTER IN public.gender
alter table public.gender
    add code varchar(20);

UPDATE public.gender
SET code        = 'F'
WHERE description = 'FEMALE';

UPDATE public.gender
SET code        = 'M'
WHERE description = 'MALE';

UPDATE public.gender
SET code        = 'SD'
WHERE description = 'N/D';

--ALTER IN public.menopausal_state
alter table public.menopausal_state
    add code varchar(20);

UPDATE public.menopausal_state
SET code        = 'PREM'
WHERE description = 'PREMENOP';

UPDATE public.menopausal_state
SET code        = 'PERIM'
WHERE description = 'PERIMENOP';

UPDATE public.menopausal_state
SET code        = 'POSTM'
WHERE description = 'POSTMENOP';

UPDATE public.menopausal_state
SET code        = 'SD'
WHERE description = 'N/D';

--ALTER IN public.periodicity
alter table public.periodicity
    add code varchar(20);

UPDATE public.periodicity
SET code = 'DAILY'
WHERE description = 'DAILY';

UPDATE public.periodicity
SET code = 'WEEKLY'
WHERE description = 'WEEKLY';

UPDATE public.periodicity
SET code = 'BIWEEKLY'
WHERE description = 'BIWEEKLY';

UPDATE public.periodicity
SET code = 'MONTHLY'
WHERE description = 'MONTHLY';

UPDATE public.periodicity
SET code = 'QUARTERLY'
WHERE description = 'QUARTERLY';

UPDATE public.periodicity
SET code = 'BIANNUAL'
WHERE description = 'SEMIANNUAL';

UPDATE public.periodicity
SET code = 'ANNUAL'
WHERE description = 'ANNUAL';

UPDATE public.periodicity
SET code = '21_DAYS'
WHERE description = 'EVERY 21 DAYS';

UPDATE public.periodicity
SET code = 'ONCE'
WHERE description = 'ATTACK SESSION (ONCE)';


--ALTER IN public.type_treatment
alter table public.type_treatment
    add code varchar(20);

UPDATE public.type_treatment
SET code        = 'RADIOTHERAPY'
WHERE description = 'RADIOTHERAPY';

UPDATE public.type_treatment
SET code        = 'CHEMOTHERAPY'
WHERE description = 'CHEMOTHERAPY';

UPDATE public.type_treatment
SET code        = 'OTHER'
WHERE description = 'OTHER';
