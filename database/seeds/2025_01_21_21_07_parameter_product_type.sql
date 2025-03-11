WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('PRODUCT_TYPE', 'MED', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Medicación', 'Productos que contienen fármacos para fines terapéuticos.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Medication', 'Products containing drugs for therapeutic purposes.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('PRODUCT_TYPE', 'CON', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Suministros médicos', 'Consumibles utilizados en entornos de atención médica (ej. jeringas, guantes).'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Medical supplies', 'Consumables used in healthcare settings (e.g. syringes, gloves).'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('PRODUCT_TYPE', 'MAT', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Material', 'Materiales de laboratorio o reactivos utilizados en pruebas.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Material', 'Laboratory materials or reagents used in tests.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('PRODUCT_TYPE', 'EQP', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Equipo', 'Dispositivos médicos o instrumentos utilizados para diagnóstico o tratamiento.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Equipment', 'Medical devices or instruments used for diagnosis or treatment.'
FROM inserted_parameter ip;

