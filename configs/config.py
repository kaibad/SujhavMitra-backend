import os
from dotenv import load_dotenv


load_dotenv()

dbconfig = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "3306"),
    "username": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "db_sujhavmitra")
}

JWT_SECRET = os.getenv("JWT_SECRET")