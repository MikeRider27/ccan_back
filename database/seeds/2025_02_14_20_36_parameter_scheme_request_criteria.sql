WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('SCHEME_REQUEST_CRITERIA', 'ADY', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Adyuvante', 'Tratamiento administrado después de la cirugía primaria para eliminar cualquier célula cancerosa restante y reducir el riesgo de recurrencia.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Adjuvant', 'Treatment given after primary surgery to kill any remaining cancer cells and reduce the risk of recurrence.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('SCHEME_REQUEST_CRITERIA', 'NAD', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Neoadyuvante', 'Tratamiento administrado antes de la cirugía primaria para reducir el tamaño del tumor, facilitar la operación y mejorar las posibilidades de éxito.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Neoadjuvant', 'Treatment given before primary surgery to reduce the size of the tumor, make the operation easier and improve the chances of success..'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('SCHEME_REQUEST_CRITERIA', 'PAL', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Paliativo', 'Tratamiento destinado a aliviar los síntomas y mejorar la calidad de vida del paciente en casos en los que la cura ya no es posible.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Palliative', 'Treatment aimed at relieving symptoms and improving the quality of life when a cure is no longer achievable.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('SCHEME_REQUEST_CRITERIA', 'MET', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Metastásico', 'Tratamiento dirigido a controlar tumores metastásicos, que se han diseminado a otras partes del cuerpo.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Metastatic', 'Treatment targeting control of metastatic tumors that have spread to other parts of the body.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('SCHEME_REQUEST_CRITERIA', 'ADEX', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Adyuvancia Extendida', 'Tratamiento adicional después de la adyuvancia inicial, como medidas preventivas adicionales, para reducir aún más el riesgo de recurrencia.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Extended Adjuvant', 'Additional treatment following initial adjuvant therapy to further reduce the risk of recurrence.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('SCHEME_REQUEST_CRITERIA', 'MTN', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Mantenimiento', 'Tratamiento de bajo nivel que se administra durante un tiempo prolongado para mantener el control del cáncer y evitar su progresión.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Maintenance', 'Low-level treatment administered over an extended period to maintain cancer control and prevent progression.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('SCHEME_REQUEST_CRITERIA', 'TD', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Dirigida', 'Tratamiento que ataca específicamente las células cancerosas con mecanismos que las identifican y las matan mientras se minimizan los efectos en las células normales.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Targeted', 'Treatment that specifically attacks cancer cells using mechanisms that identify and kill them while minimizing effects on normal cells.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('SCHEME_REQUEST_CRITERIA', 'IMM', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Inmunoterapia', 'Tratamiento que aprovecha el sistema inmunológico del paciente para atacar las células cancerosas, como los inhibidores de puntos de control inmunitarios.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Immunotherapy', 'Treatment that leverages the patient''s immune system to target cancer cells, such as immune checkpoint inhibitors.'
FROM inserted_parameter ip;