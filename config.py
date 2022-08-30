from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    PRIVATE_KEY = os.getenv('PRIVATE_KEY')
    DB_URI = os.getenv('DB_URI')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'root')
    ADMIN_LOGIN = os.getenv('ADMIN_LOGIN', 'admin')
