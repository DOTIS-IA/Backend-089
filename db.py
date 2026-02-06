import os
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "port": os.getenv("DB_PORT")
}

@contextmanager
def get_db_connection():
    """Context manager para conexiones a PostgreSQL"""
    
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def test_connection():
    """Probar conexión a la base de datos"""
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print("Conexión exitosa a PostgreSQL")
            print(f"Versión: {version[0]}")
            return True
    except Exception as e:
        print(f"Error de conexión: {e}")
        return False

if __name__ == "__main__":
    test_connection()