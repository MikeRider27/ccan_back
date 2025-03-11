WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('PROTOCOL_TYPE', 'CH', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'CAM', 'Cambio'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'CH', 'Change'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('PROTOCOL_TYPE', 'ST', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'INI', 'Inicio'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'ST', 'Start'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('PROTOCOL_TYPE', 'MAINT', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'MAN', 'Mantenimiento'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'MAINT', 'Maintenance'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('PROTOCOL_TYPE', 'FOLL', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'SEG', 'Seguimiento'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'FOLL', 'Seguimiento'
FROM inserted_parameter ip;
