-- 01-init-pg_cron.sql
-- Initialize in the postgres database (where cron runs)
\c postgres;
CREATE EXTENSION IF NOT EXISTS pg_cron;
GRANT USAGE ON SCHEMA cron TO CURRENT_USER;