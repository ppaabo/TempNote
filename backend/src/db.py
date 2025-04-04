import os
import psycopg
from psycopg import sql
from flask import g


def initialize_db():
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "db")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", 5432)
    with psycopg.connect(
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(
                sql.SQL(
                    """
                        CREATE TABLE IF NOT EXISTS messages (
                            msg_id uuid DEFAULT gen_random_uuid(),
                            ciphertext TEXT NOT NULL,
                            iv TEXT NOT NULL,
                            salt TEXT NOT NULL,
                            created_at TIMESTAMP DEFAULT now(),
                            expires_at TIMESTAMP NOT NULL
                        )
                        """
                )
            )
        conn.commit()


def get_db():
    if "db" not in g:
        g.db = psycopg.connect(
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST", "db"),
            port=os.getenv("POSTGRES_PORT", 5432),
        )
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


if __name__ == "__main__":
    initialize_db()
