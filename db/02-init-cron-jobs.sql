\c postgres;

-- Run every hour (xx:00)
SELECT cron.schedule_in_database(
  'cleanup-expired-messages',
  '0 * * * *',
  'DELETE FROM messages WHERE expires_at < NOW()',
  'flask_db'
);