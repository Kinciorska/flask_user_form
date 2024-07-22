import os
import psycopg2

from dotenv import load_dotenv


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

POSTGRES_ENV_DIR = os.path.join(BASE_DIR, 'envs/.postgres')

load_dotenv(POSTGRES_ENV_DIR)

FLASK_ENV_DIR = os.path.join(BASE_DIR, 'envs/.postgres')

load_dotenv(FLASK_ENV_DIR)

RABBITMQ_ENV_DIR = os.path.join(BASE_DIR, 'envs/.rabbitmq')

load_dotenv(RABBITMQ_ENV_DIR)

PROTOCOL = os.getenv('RABBITMQ_PROTOCOL')
USER = os.getenv('RABBITMQ_USER')
PASSWORD = os.getenv('RABBITMQ_PASSWORD')
HOST = os.getenv('RABBITMQ_HOST')
PORT = os.getenv('RABBITMQ_PORT')
VHOST = os.getenv('RABBITMQ_DEFAULT_VHOST')

CELERY_BROKER_URL = f"{PROTOCOL}://{USER}:{PASSWORD}@{HOST}:{PORT}"
CELERY_RESULT_BACKEND = 'rpc://'


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY")
    CELERY_BROKER_URL = CELERY_BROKER_URL
    CELERY_RESULT_BACKEND = CELERY_RESULT_BACKEND


class CeleryConfig(object):
    broker_url = CELERY_BROKER_URL
    result_backend = CELERY_RESULT_BACKEND
