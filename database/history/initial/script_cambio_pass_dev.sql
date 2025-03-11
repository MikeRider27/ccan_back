-- SE AGREGA RESTRICCION DE UNICIDAD
ALTER TABLE public."user"
    ADD UNIQUE ("user");

-- SE AGREGA PERMISO
INSERT INTO public.permission (description)
VALUES ('user_change_password');

-- SE VINCULA PERMISO CON EL ROL ADMINISTRADOR
INSERT INTO role_permission (role_id, permission_id)
SELECT (SELECT id FROM role WHERE description = 'ADMINISTRADOR'),
       id
FROM permission
WHERE description IN ('user_change_password')