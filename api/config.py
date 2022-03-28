import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv()

POSTGRES_URL = os.environ.get("POSTGRES_URL")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PW = os.environ.get("POSTGRES_PW")
POSTGRES_DB = os.environ.get("POSTGRES_DB")

print(POSTGRES_URL)
DB_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PW}@{POSTGRES_URL}/{POSTGRES_DB}"

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'abc'
    SQLALCHEMY_DATABASE_URI = DB_URL or f"psql:///{os.path.join(basedir)}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False