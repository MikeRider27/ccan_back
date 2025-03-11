UPDATE medical_document_type
SET description = 'CONSENTIMIENTO INFORMADO DE TRATAMIENTO'
WHERE id = 1;

INSERT INTO medical_document_type (description)
VALUES ('INFORME DE IHQ'),
       ('INFORME DE ESTADIFICACION DE  IMAGENOLOGIA'),
       ('ECOCARDIOGRAFIA');

alter table public.medicine_medication_order
    add dose numeric;

alter table public.medicine_treatment_order
    add dose numeric;
