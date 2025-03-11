WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('SCHEME_CATEGORY', 'PALL', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Paliativo', 'Esquema diseñado para aliviar síntomas y mejorar la calidad de vida sin intención curativa.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Palliative', 'Scheme designed to relieve symptoms and improve quality of life without curative intent.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('SCHEME_CATEGORY', 'HEAL', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Curativo', 'Esquema dirigido a erradicar completamente la enfermedad..'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Healing', 'Scheme aimed at completely eradicating the disease.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('SCHEME_CATEGORY', 'ADJU', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Adyuvante', 'Administrado después del tratamiento primario para prevenir recurrencias.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Adjuvant', 'Administered after primary treatment to prevent recurrences.'
FROM inserted_parameter ip;

-- Neoadyuvante (NEOA)
WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('SCHEME_CATEGORY', 'NEOA', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Neoadyuvante', 'Administrado antes del tratamiento principal para reducir el tamaño del tumor.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Neoadjuvant', 'Administered before the main treatment to reduce tumor size.'
FROM inserted_parameter ip;

-- Mantenimiento (MAINT)
WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('SCHEME_CATEGORY', 'MAINT', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Mantenimiento', 'Diseñado para mantener la enfermedad controlada y evitar progresión.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Maintenance', 'Designed to keep the disease under control and prevent progression.'
FROM inserted_parameter ip;

-- Experimental (EXPE)
WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('SCHEME_CATEGORY', 'EXPE', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Experimental', 'Utilizado en protocolos de investigación clínica para evaluar nuevas terapias o combinaciones.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Experimental', 'Used in clinical research protocols to evaluate new therapies or combinations.'
FROM inserted_parameter ip;

-- Profiláctico (PROF)
WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('SCHEME_CATEGORY', 'PROF', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Profiláctico', 'Preventivo para reducir el riesgo de desarrollar cáncer en pacientes de alto riesgo.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Prophylactic', 'Preventive to reduce the risk of developing cancer in high-risk patients.'
FROM inserted_parameter ip;

-- Soporte (SUPP)
WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('SCHEME_CATEGORY', 'SUPP', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Soporte', 'Manejo de efectos secundarios o mejora de la tolerancia a otros tratamientos.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Support', 'Management of side effects or improvement of tolerance to other treatments.'
FROM inserted_parameter ip;
