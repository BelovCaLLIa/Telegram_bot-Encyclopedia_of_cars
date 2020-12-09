import os

from dotenv import load_dotenv

# Явное указание из какого файла брать переменные
dotenv_path = os.path.join(os.path.dirname(__file__), 'e.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# Токен моего бота
TOKEN = os.getenv("TOKEN")
# Chat id
admin_id = os.getenv("ADMIN_ID")
# ip докера-a
host = os.getenv("HOST")
PG_USER = os.getenv("PG_USER")
PG_PASS = os.getenv("PG_PASS")
