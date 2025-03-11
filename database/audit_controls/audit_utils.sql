-- SELECT TRIGGERS ENABLED/DISABLED
SELECT 
		nspname AS schema_name,
		relname AS table_name,
		tgname AS trigger_name,
		tgenabled AS is_enabled
FROM pg_trigger t
JOIN pg_class c ON t.tgrelid = c.oid
JOIN pg_namespace n ON c.relnamespace = n.oid
WHERE 
tgname like '%audit_%'
--and tgenabled = 'D' -- para saber si estan desactivados
--and tgenabled = 'O' -- para saber si estan activos
order by 1;
