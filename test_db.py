import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
print(f"Подключаюсь к: {DATABASE_URL}")

try:
    conn = psycopg2.connect(DATABASE_URL)
    print("✅ Подключение успешно!")

    with conn.cursor() as cur:
        cur.execute("SELECT 1")
        print("✅ Запрос выполнен")

    conn.close()
except Exception as e:
    print(f"❌ Ошибка: {e}")