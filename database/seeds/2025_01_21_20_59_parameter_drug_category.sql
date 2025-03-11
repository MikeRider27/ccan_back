WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('DRUG_CATEGORY', 'CHEMOTHERAPY', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Quimioterapia', 'Atacan células de rápida división, incluidas las cancerosas.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Chemotherapy', 'Attack rapidly dividing cells, including cancer cells.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('DRUG_CATEGORY', 'IMMUNOTHERAPY', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Inmunoterapia', 'Estimulan el sistema inmunológico para atacar las células cancerosas.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Immunotherapy', 'Stimulate the immune system to attack cancer cells.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('DRUG_CATEGORY', 'TARGETED_THERAPY', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Terapia Dirigida', 'Atacan proteínas o genes específicos en las células tumorales.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Targeted Therapy', 'Target specific proteins or genes in tumor cells.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('DRUG_CATEGORY', 'HORMONE_THERAPY', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Hormonoterapia', 'Alteran o bloquean las hormonas necesarias para el crecimiento de ciertos tumores.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Hormone Therapy', 'Alter or block hormones needed for the growth of certain tumors.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('DRUG_CATEGORY', 'RADIO_PROTECTOR', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Radioprotector', 'Protegen tejidos sanos del daño inducido por radioterapia.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Radioprotector', 'Protect healthy tissues from radiation-induced damage.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('DRUG_CATEGORY', 'SUPPORTIVE_CARE', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Soporte', 'Alivian los efectos secundarios de los tratamientos oncológicos.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Supportive Care', 'Relieve side effects of cancer treatments.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('DRUG_CATEGORY', 'ANALGESIA', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Analgesia', 'Manejo del dolor asociado al cáncer o a los tratamientos.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Analgesia', 'Management of pain associated with cancer or treatments.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('DRUG_CATEGORY', 'ANTI_NAUSEA', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Anti-Náusea', 'Previenen o tratan náuseas y vómitos inducidos por quimioterapia o radioterapia.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Anti-Nausea', 'Prevent or treat nausea and vomiting induced by chemotherapy or radiotherapy.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('DRUG_CATEGORY', 'BISPHOSPHONATES', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Bifosfonatos', 'Previenen la pérdida ósea y el riesgo de fracturas en pacientes con metástasis óseas.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Bisphosphonates', 'Prevent bone loss and the risk of fractures in patients with bone metastases.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('DRUG_CATEGORY', 'RADIOPHARMACEUTICALS', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Radiofármacos', 'Utilizan radiación para tratar el cáncer o aliviar síntomas de metástasis óseas.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Radiopharmaceuticals', 'Use radiation to treat cancer or relieve symptoms of bone metastases.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('DRUG_CATEGORY', 'EXPERIMENTAL', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Experimental', 'Medicamentos en ensayo clínico o investigación para nuevos tratamientos.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Experimental', 'Drugs in clinical trials or research for new treatments.'
FROM inserted_parameter ip;
