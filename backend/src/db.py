import os
import time
import psycopg
from psycopg import sql
from flask import g
import logging

logger = logging.getLogger(__name__)


def initialize_db():
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", 5432)

    # Check for required environment variables
    required = {
        "POSTGRES_USER": POSTGRES_USER,
        "POSTGRES_PASSWORD": POSTGRES_PASSWORD,
        "POSTGRES_DB": POSTGRES_DB,
    }
    missing_vars = [key for key, value in required.items() if value is None]

    if missing_vars:
        error_msg = f"Missing required environment variables: {', '.join(missing_vars)}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    max_retries = 5
    retry_delay = 3
    for attempt in range(max_retries):
        try:
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
            logging.info(f"Database connection established on attempt {attempt + 1}")
            return
        except Exception as e:
            logging.warning(f"Database connection attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                logging.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
    raise Exception("Failed to connect to database after multiple attempts")


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
