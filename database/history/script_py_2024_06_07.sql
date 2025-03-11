--Actualización de descripción de user_create solicitado por incidencia Jira: https://emendez84.atlassian.net/browse/SOP-20

update public.diagnosis_ap set user_create='Interoperabilidad' where user_create = 'scheduled_tasks';

update inventory.deposit set user_create='Interoperabilidad' where user_create = 'scheduled_tasks';

update inventory.lot set user_create='Interoperabilidad' where user_create = 'scheduled_tasks';

update inventory.history set user_create='Interoperabilidad' where user_create = 'scheduled_tasks';

update public.doctor set user_create='Interoperabilidad' where user_create = 'scheduled_tasks';

update public.medical_consultation set user_create='Interoperabilidad' where user_create = 'scheduled_tasks';

update inventory.dispatch_medications set user_create='Interoperabilidad' where user_create = 'scheduled_tasks';