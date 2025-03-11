ALTER TABLE message
ADD COLUMN id_hospital INTEGER;

--ALTER TABLE PUBLIC.MESSAGE
ALTER TABLE public.message
    ADD patient_id bigint;

ALTER TABLE public.message
    ADD CONSTRAINT message_patient_id_fk
        FOREIGN KEY (patient_id) REFERENCES public.patient;


-- ADD NEW PERMISSIONS --
INSERT INTO public."permission" (description)
VALUES  ('menu_message'),
        ('message_get'),
        ('message_update'),
        ('message_delete'),
        ('message_list'),
        ('message_insert'),
        ('message_search'),
        ('inbox_get'),
        ('inbox_update'),
        ('inbox_delete'),
        ('inbox_list'),
        ('inbox_insert'),
        ('inbox_search'),
        ('notificaciones_get'),
        ('notificaciones_update'),
        ('notificaciones_list'),
        ('notificaciones_insert'),
        ('notificaciones_search');

-- INSERCION PERMISSION TO ROLE
INSERT INTO role_permission (role_id, permission_id)
SELECT (SELECT id FROM role WHERE role.description = 'AUDITOR'),
       p.id
FROM permission p
WHERE p.description IN (
                        'menu_message',
                        'message_get',
                        'message_update',
                        'message_delete',
                        'message_list',
                        'message_insert',
                        'message_search',
                        'inbox_get',
                        'inbox_update',
                        'inbox_delete',
                        'inbox_list',
                        'inbox_insert',
                        'inbox_search',
                        'notificaciones_get',
                        'notificaciones_update',
                        'notificaciones_list',
                        'notificaciones_insert',
                        'notificaciones_search'
                        );

INSERT INTO role_permission (role_id, permission_id)
SELECT (SELECT id FROM role WHERE role.description = 'INVENTARIO'),
       p.id
FROM permission p
WHERE p.description IN (
                        'menu_message',
                        'message_get',
                        'message_update',
                        'message_delete',
                        'message_list',
                        'message_insert',
                        'message_search',
                        'inbox_get',
                        'inbox_update',
                        'inbox_delete',
                        'inbox_list',
                        'inbox_insert',
                        'inbox_search',
                        'notificaciones_get',
                        'notificaciones_update',
                        'notificaciones_list',
                        'notificaciones_insert',
                        'notificaciones_search'
                        );

INSERT INTO role_permission (role_id, permission_id)
SELECT (SELECT id FROM role WHERE role.description = 'EVALUADOR'),
       p.id
FROM permission p
WHERE p.description IN (
                        'menu_message',
                        'message_get',
                        'message_update',
                        'message_delete',
                        'message_list',
                        'message_insert',
                        'message_search',
                        'inbox_get',
                        'inbox_update',
                        'inbox_delete',
                        'inbox_list',
                        'inbox_insert',
                        'inbox_search',
                        'notificaciones_get',
                        'notificaciones_update',
                        'notificaciones_list',
                        'notificaciones_insert',
                        'notificaciones_search'
                        );

INSERT INTO role_permission (role_id, permission_id)
SELECT (SELECT id FROM role WHERE role.description = 'MEDICO'),
       p.id
FROM permission p
WHERE p.description IN (
                        'menu_message',
                        'message_get',
                        'message_update',
                        'message_delete',
                        'message_list',
                        'message_insert',
                        'message_search',
                        'inbox_get',
                        'inbox_update',
                        'inbox_delete',
                        'inbox_list',
                        'inbox_insert',
                        'inbox_search',
                        'notificaciones_get',
                        'notificaciones_update',
                        'notificaciones_list',
                        'notificaciones_insert',
                        'notificaciones_search'
                        );

INSERT INTO role_permission (role_id, permission_id)
SELECT (SELECT id FROM role WHERE role.description = 'ENFERMERIA'),
       p.id
FROM permission p
WHERE p.description IN (
                        'menu_message',
                        'message_get',
                        'message_update',
                        'message_delete',
                        'message_list',
                        'message_insert',
                        'message_search',
                        'inbox_get',
                        'inbox_update',
                        'inbox_delete',
                        'inbox_list',
                        'inbox_insert',
                        'inbox_search',
                        'notificaciones_get',
                        'notificaciones_update',
                        'notificaciones_list',
                        'notificaciones_insert',
                        'notificaciones_search'
                        );
