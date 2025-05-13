-- 01-init-schema.sql
CREATE TABLE IF NOT EXISTS messages (
    msg_id uuid DEFAULT gen_random_uuid(),
    ciphertext TEXT NOT NULL,
    iv TEXT NOT NULL,
    salt TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT now(),
    expires_at TIMESTAMP NOT NULL
);