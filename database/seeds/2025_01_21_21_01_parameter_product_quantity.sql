WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('PRODUCT_UNIT_QUANTITY', 'VIAL', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Vial', 'Recipiente para reconstitución de líquido o polvo.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Vial', 'Container for liquid or powder reconstitution.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('PRODUCT_UNIT_QUANTITY', 'AMPOULE', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Ampolla', 'Solución líquida inyectable lista para usar.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Ampoule', 'Ready-to-use liquid solution for injection.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('PRODUCT_UNIT_QUANTITY', 'BOTTLE', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Frasco', 'Frasco para soluciones orales o jarabes.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Bottle', 'Bottle for oral solutions or syrups.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('PRODUCT_UNIT_QUANTITY', 'TUBE', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Tubo', 'Tubo para cremas o geles tópicos.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Tube', 'Tube for topical creams or gels.'
FROM inserted_parameter ip;
