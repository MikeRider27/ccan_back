-- CAMBIOS EN ESTADO DE PACIENTE
INSERT INTO public.parameter (domain, value, active, code)
VALUES ('PATIENT_STATE', 'REVISIÓN', TRUE, 'REV');

-- ALTER EN public.evaluation
alter table public.evaluation
    add evaluation_state varchar(10);

UPDATE public.evaluation eval
SET evaluation_state = (CASE WHEN eval.approved THEN 'approved' ELSE 'excluded' END)
WHERE TRUE;

alter table public.evaluation
    drop column approved;
