--Permiso necesario para acceder al apartado de Tipo de documento medico en PY-GH-CO
INSERT INTO public."permission" (description)
VALUES ('menu_medical_document_type');

INSERT INTO role_permission (role_id, permission_id)
SELECT (SELECT id FROM role WHERE role.description = 'AUDITOR'),
       p.id
FROM permission p
WHERE p.description IN ('menu_medical_document_type');

--Permiso necesario para acceder al apartado de CIE-O Topografía en PY-GH-CO
INSERT INTO public."permission" (description)
VALUES ('menu_cie_o_topography');

INSERT INTO role_permission (role_id, permission_id)
SELECT (SELECT id FROM role WHERE role.description = 'AUDITOR'),
       p.id
FROM permission p
WHERE p.description IN ('menu_cie_o_topography');

--Permiso necesario para acceder al apartado de CIE-O Tumor Location en PY-GH-CO
INSERT INTO public."permission" (description)
VALUES ('menu_cie_o_tumor_location');

INSERT INTO role_permission (role_id, permission_id)
SELECT (SELECT id FROM role WHERE role.description = 'AUDITOR'),
       p.id
FROM permission p
WHERE p.description IN ('menu_cie_o_tumor_location');
