import os
from dotenv import load_dotenv


load_dotenv()

dbconfig = {
    "host":"localhost",
    "port":3306,
    "user": "root",
    "password": "",
    "database": "db_sujhavmitra"
}

JWT_SECRET = os.getenv("JWT_SECRET")
