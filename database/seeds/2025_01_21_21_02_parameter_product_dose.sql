WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('PRODUCT_UNIT_DOSE', 'MG', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'mg', 'Miligramos.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'mg', 'Milligrams.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('PRODUCT_UNIT_DOSE', 'G', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'g', 'Gramos.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'g', 'Grams.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('PRODUCT_UNIT_DOSE', 'MG_KG', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'mg/kg', 'Miligramos por kilogramo de peso.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'mg/kg', 'Milligrams per kilogram of weight.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('PRODUCT_UNIT_DOSE', 'MG_MA_2', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'mg/mÂ²', 'Miligramos por metro cuadrado de superficie corporal, estándar en oncología.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'mg/mÂ²', 'Milligrams per square meter of body surface area, standard in oncology.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('PRODUCT_UNIT_DOSE', 'UI_KG', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'UI/kg', 'Unidades internacionales por kilogramo.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'UI/kg', 'International units per kilogram.'
FROM inserted_parameter ip;
