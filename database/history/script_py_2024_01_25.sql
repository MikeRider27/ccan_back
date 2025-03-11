-- ADD NEW PERMISSIONS --
INSERT INTO public."permission" (description)
VALUES ('menu_country'),
       ('menu_parameter'),
       ('menu_area'),
       ('menu_city');

-- ALTER IN public.area --
-- ALTER TABLE public.area
--     RENAME COLUMN nro_departamento TO area_number;
ALTER TABLE public.area
    ADD area_number integer;

-- ALTER IN public.diagnosis
ALTER TABLE public.diagnosis
    ADD CONSTRAINT diagnosis_pk
        PRIMARY KEY (id);

-- ADD NEW PERMISSIONS --
INSERT INTO public."permission" (description)
VALUES ('patient_incl_excl_report');

INSERT INTO role_permission (role_id, permission_id)
SELECT (SELECT id FROM role WHERE description = 'MEDICO'),
       id
FROM permission
WHERE description IN ('patient_incl_excl_report');

INSERT INTO role_permission (role_id, permission_id)
SELECT (SELECT id FROM role WHERE description = 'ENFERMERIA'),
       id
FROM permission
WHERE description IN ('patient_incl_excl_report');

INSERT INTO role_permission (role_id, permission_id)
SELECT (SELECT id FROM role WHERE description = 'EVALUADOR'),
       id
FROM permission
WHERE description IN ('patient_incl_excl_report');