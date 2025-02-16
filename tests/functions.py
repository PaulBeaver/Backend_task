import time

import psycopg2
from psycopg2.errors import OperationalError

from app.config import settings


def wait_for_postgres(max_retries=30, delay=1):
    retries = 0
    while retries < max_retries:
        try:
            conn = psycopg2.connect(
                host=settings.DB_HOST,
                port=settings.DB_PORT,
                user=settings.DB_USER,
                password=settings.DB_PASS,
                dbname=settings.DB_NAME,
            )
            conn.close()
            print("PostgreSQL is ready!")
            return
        except OperationalError as e:
            print(
                f"PostgreSQL is not ready yet. Retrying in {delay} seconds... (Attempt {retries + 1}/{max_retries})"
            )
            retries += 1
            time.sleep(delay)
            raise e

    raise RuntimeError("PostgreSQL is not available after maximum retries.")
