WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('PRODUCT_UNIT_CONCENTRATION', 'MG_ML', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'mg/mL', 'Miligramos por mililitros, comúnmente usado para inyectables.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'mg/mL', 'Milligrams per milliliter, commonly used for injectables.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('PRODUCT_UNIT_CONCENTRATION', 'MCG_ML', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'mcg/mL', 'Microgramos por mililitro, usado para tratamientos de precisión.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'mcg/mL', 'Micrograms per milliliter, used for precision treatments.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('PRODUCT_UNIT_CONCENTRATION', 'UI_ML', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'UI/mL', 'Unidades Internacionales por mililitro, usado en soluciones hormonales.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'UI/mL', 'International units per milliliter, used in hormonal solutions.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('PRODUCT_UNIT_CONCENTRATION', 'MMOL_L', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'mmol/L', 'Milimoles por litro, utilizados para soluciones electrolíticas.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'mmol/L', 'Millimoles per liter, used for electrolyte solutions.'
FROM inserted_parameter ip;


