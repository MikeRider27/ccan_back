WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('SCHEME_PERIODICITY', 'WEEK', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', '7', 'Semanal.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', '7', 'Weekly.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('SCHEME_PERIODICITY', '28D', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', '28', '28 días.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', '28', '28 days.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('SCHEME_PERIODICITY', '01D', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', '1', '1 día.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', '1', '1 day.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('SCHEME_PERIODICITY', '15D', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', '15', '15 días.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', '15', '15 days.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('SCHEME_PERIODICITY', '21D', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', '21', '21 días.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', '21', '21 days.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('SCHEME_PERIODICITY', 'CON', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', '0', 'Concurrente.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', '0', 'Concurrent.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('SCHEME_PERIODICITY', '15D', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', '15', 'Quincenal.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', '15', 'Biweekly.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('SCHEME_PERIODICITY', 'QUA', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', '90', 'Trimestral.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', '90', 'Quarterly.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('SCHEME_PERIODICITY', '42D', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', '42', '42 días.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', '42', '42 days.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('SCHEME_PERIODICITY', 'E6W', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', '42', 'Cada 6 semanas.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', '42', 'Every 6 weeks.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('SCHEME_PERIODICITY', '14D', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', '14', 'Cada 14 días.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', '14', 'Every 14 days.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('SCHEME_PERIODICITY', 'MON', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', '30', 'Mensual.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', '30', 'Monthly.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('SCHEME_PERIODICITY', 'E2M', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', '60', 'Cada 2 meses.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', '60', 'Every 2 months.'
FROM inserted_parameter ip;
