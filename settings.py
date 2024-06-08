import os
import psycopg2

from celery import Celery
from dotenv import load_dotenv
from flask import Flask

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# Rabbitmq settings

RABBITMQ_ENV_DIR = os.path.join(BASE_DIR, 'envs/.rabbitmq')

load_dotenv(RABBITMQ_ENV_DIR)

PROTOCOL = os.getenv('RABBITMQ_PROTOCOL')
USER = os.getenv('RABBITMQ_USER')
PASSWORD = os.getenv('RABBITMQ_PASSWORD')
HOST = os.getenv('RABBITMQ_HOST')
PORT = os.getenv('RABBITMQ_PORT')
VHOST = os.getenv('RABBITMQ_DEFAULT_VHOST')


# Celery settings

CELERY_BROKER_URL = f"{PROTOCOL}://{USER}:{PASSWORD}@{HOST}:{PORT}"

celery_app = Celery(
    'tasks',
    broker=CELERY_BROKER_URL,
    backend='rpc://'
)

celery_app.autodiscover_tasks()

__all__ = ('celery_app',)


# Flask settings

FlASK_ENV_DIR = os.path.join(BASE_DIR, 'envs/.flask')

load_dotenv(FlASK_ENV_DIR)

app = Flask(__name__)

SECRET_KEY = os.getenv('SECRET_KEY')

app.config['SECRET_KEY'] = SECRET_KEY


# PostgreSQL settings

POSTGRES_ENV_DIR = os.path.join(BASE_DIR, 'envs/.postgres')

load_dotenv(POSTGRES_ENV_DIR)

connection = psycopg2.connect(
        host=os.getenv('POSTGRES_HOST'),
        database=os.getenv('POSTGRES_DATABASE'),
        user=os.getenv('POSTGRES_NON_ROOT_USER'),
        password=os.getenv('POSTGRES_NON_ROOT_PASSWORD')
)
