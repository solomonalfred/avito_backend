from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

BANNER_USER = os.environ.get("BANNER_USER")
BANNER_NAME = os.environ.get("BANNER_NAME")

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")

ADMIN_PASS = os.environ.get('ADMIN_PASS')
ADMIN_NAME = os.environ.get('ADMIN_NAME')
ADMIN_NICKNAME = os.environ.get('ADMIN_NICKNAME')