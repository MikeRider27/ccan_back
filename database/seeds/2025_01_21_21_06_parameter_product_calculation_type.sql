WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('PRODUCT_CALCULATION_TYPE', 'BSA', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Superficie Corporal', 'Se calcula en función de la superficie corporal del paciente (m²) usando fórmulas como Mosteller o DuBois.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Body Surface', 'It is calculated based on the patient''s body surface area (m²) using formulas such as Mosteller or DuBois.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('PRODUCT_CALCULATION_TYPE', 'BWT', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Peso Corporal', 'Se calcula en función de la superficie corporal del paciente (m²) usando fórmulas como Mosteller o DuBois.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Body Weight', 'It is determined based on the patient''s weight in kg and the recommended dose in mg/kg.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('PRODUCT_CALCULATION_TYPE', 'RENAL', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Función Renal', 'Se ajusta la dosis con la fórmula de Calvert para medicamentos eliminados por el riñón, como Carboplatino.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Renal Function', 'The dose is adjusted using the Calvert formula for drugs eliminated by the kidney, such as Carboplatin.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('PRODUCT_CALCULATION_TYPE', 'AUC', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Área Bajo la Curva', 'Depende de la función renal y se usa para ciertos fármacos como el Carboplatino.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Area Under the Curve', 'Depends on renal function and is used for certain drugs like Carboplatin.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('PRODUCT_CALCULATION_TYPE', 'FDO', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Dosis Fija', 'Se administra en una dosis estándar sin ajuste por peso o superficie corporal.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Fixed Dose', 'It is administered as a standard dose without adjustment for weight or body surface area.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('PRODUCT_CALCULATION_TYPE', 'TOX', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Dosis Ajustada por Toxicidad', 'La dosis se modifica en función de la respuesta del paciente y la toxicidad observada en ciclos previos.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Dose Adjusted by Toxicity', 'The dose is modified based on the patient''s response and the toxicity observed in previous cycles.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('PRODUCT_CALCULATION_TYPE', 'FGEN', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Dosis Ajustada por Farmacogenética', 'Se ajusta según la genética del paciente, como en el caso de la 6-mercaptopurina con mutaciones TPMT.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Dose Adjusted by Pharmacogenetics', 'It is adjusted according to the patient''s genetics, as in the case of 6-mercaptopurine with TPMT mutations.'
FROM inserted_parameter ip;
