WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('PRODUCT_ADMINISTRATION_ROUTE', 'IV', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Intravenosa', 'Administración directa al torrente sanguíneo, común para quimioterápicos y soluciones de soporte..'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Intravenous', 'Direct administration into the bloodstream, common for chemotherapy and support solutions.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('PRODUCT_ADMINISTRATION_ROUTE', 'IM', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Intramuscular', 'Inyección en el músculo, usada ocasionalmente para medicamentos como antieméticos o analgésicos.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Intramuscular', 'Injection into the muscle, occasionally used for medications such as antiemetics or pain relievers.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('PRODUCT_ADMINISTRATION_ROUTE', 'SC', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Subcutánea', 'Inyección bajo la piel, usada para factores de crecimiento y algunos biológicos como eritropoyetina.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Subcutaneous', 'Injection under the skin, used for growth factors and some biologics like erythropoietin.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('PRODUCT_ADMINISTRATION_ROUTE', 'VO', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Oral', 'Administración por vía oral, frecuente para quimioterápicos orales y medicación de soporte.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Oral', 'Administration through the mouth, common for oral chemotherapies and supportive medication.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('PRODUCT_ADMINISTRATION_ROUTE', 'IT', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Intratecal', 'Inyección en el canal espinal, utilizada en quimioterapia para tratar cánceres del sistema nervioso central.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Intrathecal', 'Injection into the spinal canal, used in chemotherapy to treat cancers of the central nervous system.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('PRODUCT_ADMINISTRATION_ROUTE', 'ID', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Intradérmica', 'Inyección en la dermis, usada para pruebas de sensibilidad o en investigaciones clínicas.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Intradermal', 'Injection into the dermis, used for sensitivity tests or in clinical research.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('PRODUCT_ADMINISTRATION_ROUTE', 'TD', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Transdérmica', 'Aplicación a través de parches, usada para analgesia prolongada o soporte hormonal.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Transdermal', 'Application via patches, used for prolonged analgesia or hormonal support.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('PRODUCT_ADMINISTRATION_ROUTE', 'IP', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Intraperitoneal', 'Administración en la cavidad peritoneal, usada en cánceres abdominales como el de ovario.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Intraperitoneal', 'Administration into the peritoneal cavity, used for abdominal cancers like ovarian cancer.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('PRODUCT_ADMINISTRATION_ROUTE', 'IVC', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Intravesical', 'Administración directa en la vejiga, usada para tratar cáncer de vejiga in situ.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Intravesical', 'Direct administration into the bladder, used to treat in situ bladder cancer.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('PRODUCT_ADMINISTRATION_ROUTE', 'IA', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Intraarterial', 'Administración directamente en arterias específicas, utilizada en terapias dirigidas como el quimioembolismo.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Intraarterial', 'Direct administration into specific arteries, used in targeted therapies like chemoembolization.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('PRODUCT_ADMINISTRATION_ROUTE', 'TOP', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Tópica', 'Aplicación directa sobre la piel o mucosas, usada en manejo paliativo, cuidado de heridas o radiodermitis.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Topical', 'Direct application to the skin or mucous membranes, used in palliative care, wound care, or radiodermatitis.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('PRODUCT_ADMINISTRATION_ROUTE', 'IL', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Intralesional', 'Inyección directa en el tumor o lesión, utilizada en ciertos casos de cáncer de piel o melanoma.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Intralesional', 'Direct injection into the tumor or lesion, used in certain cases of skin cancer or melanoma.'
FROM inserted_parameter ip;
