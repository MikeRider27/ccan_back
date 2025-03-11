WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('CANCER_STAGE', 'I', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'I', 'Tumor localizado, de tamaño pequeño, sin evidencia de diseminación a ganglios linfáticos o tejidos cercanos.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'I', 'Localized tumor, small in size, with no evidence of spread to lymph nodes or nearby tissues.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('CANCER_STAGE', 'Ia', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Ia', 'Tumor muy pequeño y completamente contenido dentro del órgano de origen.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Ia', 'Very small tumor completely contained within the organ of origin.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('CANCER_STAGE', 'Ib', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Ib', 'Tumor algo más grande o múltiples focos pequeños, pero aún localizado.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Ib', 'Slightly larger tumor or multiple small foci, but still localized.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('CANCER_STAGE', 'Ic', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'Ic', 'Tumor localizado con pequeñas invasiones microscópicas fuera del órgano de origen, pero sin diseminación amplia.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'Ic', 'Localized tumor with minor microscopic invasions outside the organ of origin but no widespread dissemination.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('CANCER_STAGE', 'IIa', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'IIa', 'Tumor de tamaño moderado con diseminación limitada a áreas cercanas, sin afectación de ganglios linfáticos.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'IIa', 'Moderate-sized tumor with limited spread to nearby areas, no lymph node involvement.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('CANCER_STAGE', 'IIb', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'IIb', 'Tumor con invasión más profunda en tejidos circundantes o afectación limitada de ganglios linfáticos cercanos.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'IIb', 'Tumor with deeper invasion into surrounding tissues or limited involvement of nearby lymph nodes.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('CANCER_STAGE', 'III', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'III', 'Tumor avanzado con diseminación regional, afectando ganglios linfáticos u órganos adyacentes, pero no distante.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'III', 'Advanced tumor with regional spread, affecting lymph nodes or adjacent organs, but not distant.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('CANCER_STAGE', 'IIIa', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'IIIa', 'Diseminación a ganglios linfáticos regionales, pero sin invasión extensa a órganos vecinos.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'IIIa', 'Spread to regional lymph nodes but no extensive invasion of nearby organs.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('CANCER_STAGE', 'IIIb', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'IIIb', 'Tumor avanzado que invade estructuras vecinas importantes, como músculos o huesos cercanos.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'IIIb', 'Advanced tumor invading important nearby structures, such as muscles or nearby bones.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('CANCER_STAGE', 'IIIc', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'IIIc', 'Afectación extensa de ganglios linfáticos regionales y posible diseminación limitada a tejidos adyacentes.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'IIIc', 'Extensive involvement of regional lymph nodes and possible limited spread to adjacent tissues.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('CANCER_STAGE', 'In situ', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'In situ', 'Tumor no invasivo confinado a las células donde se originó, sin diseminación a tejidos cercanos.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'In situ', 'Non-invasive tumor confined to the cells where it originated, with no spread to nearby tissues.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('CANCER_STAGE', 'IV', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'IV', 'Tumor metastásico que ha diseminado a órganos distantes del sitio de origen.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'IV', 'Metastatic tumor that has spread to distant organs from the site of origin.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('CANCER_STAGE', 'IV M0', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'IV M0', 'Presencia de un tumor avanzado sin evidencia de metástasis distante.'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'IV M0', 'Presence of an advanced tumor with no evidence of distant metastasis.'
FROM inserted_parameter ip;

WITH inserted_parameter AS (
    INSERT INTO parameter (domain, value, active) VALUES ('CANCER_STAGE', 'IVa', TRUE) RETURNING id
)
INSERT INTO parameter_translation (parameter_id, language_code, value, description)
SELECT ip.id, 'es', 'IVa', 'Tumor metastásico limitado a un solo órgano distante o área específica (como los pulmones o el hígado).'
FROM inserted_parameter ip
UNION ALL
SELECT ip.id, 'en', 'IVa', 'Metastatic tumor limited to a single distant organ or specific area (such as the lungs or liver).'
FROM inserted_parameter ip;
