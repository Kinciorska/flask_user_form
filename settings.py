import os
import psycopg2

from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Flask settings
FlASK_ENV_DIR = os.path.join(BASE_DIR, 'envs/.flask')

load_dotenv(FlASK_ENV_DIR)

SECRET_KEY = os.getenv('SECRET_KEY')

# PostgreSQL settings

POSTGRES_ENV_DIR = os.path.join(BASE_DIR, 'envs/.postgres')

load_dotenv(POSTGRES_ENV_DIR)

connection = psycopg2.connect(
        host=os.getenv('HOST'),
        database=os.getenv('POSTGRES_DATABASE'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD')
)
