WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('PRODUCT_FREQUENCY', '24H', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', '24', 'Una vez al día.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', '24', 'Once a day.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('PRODUCT_FREQUENCY', '12H', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', '12', 'Dos veces al día.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', '12', 'Two times a day.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('PRODUCT_FREQUENCY', '08H', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', '8', 'Tres veces al día.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', '8', 'Three times a day.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('PRODUCT_FREQUENCY', '00H', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', '0', 'Según necesidad.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', '0', 'As needed.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('PRODUCT_FREQUENCY', '06H', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', '6', 'Cada 6 horas.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', '6', 'Every 6 hours.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('PRODUCT_FREQUENCY', '08H', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', '8', 'Cada 8 horas.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', '8', 'Every 8 hours.'
FROM inserted_parameter ip;
