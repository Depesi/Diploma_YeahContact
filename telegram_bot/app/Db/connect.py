import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

conn = psycopg2.connect(host=os.getenv("database_host_name"),
                        port=os.getenv("database_port"),
                        database=os.getenv("database"),
                        user=os.getenv("database_user"),
                        password=os.getenv("database_password"))
print("Database opened successfully")
