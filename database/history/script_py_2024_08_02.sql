ALTER TABLE public.hospital
    ADD COLUMN hospital_codigo varchar;

-- En audit
ALTER TABLE audit.public_hospital
    ADD COLUMN hospital_codigo varchar;

-- Agregar codigos de interoperabilidad a hospitales de CCAN
UPDATE public.hospital
SET hospital_codigo = '0011000.00020226'
WHERE description = 'INSTITUTO NACIONAL DEL CANCER';

UPDATE public.hospital
SET hospital_codigo = '0018000.00300204'
WHERE description = 'HOSPITAL MATERNO INFANTIL SAN PABLO';

UPDATE public.hospital
SET hospital_codigo = '0011000.00060245'
WHERE description = 'HOSPITAL NACIONAL DE ITAUGUA';

UPDATE public.hospital
SET hospital_codigo = '0018000.00300803'
WHERE description = 'HOSPITAL DE CLINICAS';


-- Eliminar registros de public.medical_consultation para volver a migrar de forma correcta
-- BACKUP DE DATOS ANTES DE LA ELIMINACION
SELECT *
FROM public.medical_consultation
WHERE origin = 'HIS';

SELECT *
FROM public.medicine_medical_consultation
WHERE medical_consultation_id IN (SELECT id
                                  FROM public.medical_consultation
                                  WHERE origin = 'HIS');
--------------------------
-- DELETE
-- Delete from public.medicine_medical_consultation
DELETE
FROM public.medicine_medical_consultation
WHERE id IN (SELECT id
             FROM public.medicine_medical_consultation
             WHERE medical_consultation_id IN (SELECT id
                                               FROM public.medical_consultation
                                               WHERE origin = 'HIS'));

-- Delete from public.medical_consultation
DELETE
FROM public.medical_consultation
WHERE id IN (SELECT id
             FROM public.medical_consultation
             WHERE origin = 'HIS');