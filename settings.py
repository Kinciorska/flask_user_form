import os
import psycopg2

from celery import Celery, Task
from dotenv import load_dotenv
from flask import Flask


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# Celery settings
def celery_init_app(app: Flask):
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.Task = FlaskTask

    return celery_app


# Redis settings
REDIS_ENV_DIR = os.path.join(BASE_DIR, 'envs/.redis')

load_dotenv(REDIS_ENV_DIR)

REDIS_PROTOCOL = os.getenv('REDIS_PROTOCOL')
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_DB_NUMBER = os.getenv('REDIS_DB_NUMBER')


# Flask settings
FlASK_ENV_DIR = os.path.join(BASE_DIR, 'envs/.flask')

load_dotenv(FlASK_ENV_DIR)

SECRET_KEY = os.getenv('SECRET_KEY')
CELERY_BROKER_URL = f'{REDIS_PROTOCOL}://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_NUMBER}'
CELERY_RESULT_BACKEND = f'{REDIS_PROTOCOL}://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_NUMBER}'


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config.from_mapping(
    CELERY=dict(
        broker_url=CELERY_BROKER_URL,
        result_backend=CELERY_RESULT_BACKEND,
        task_ignore_result=True,
    ),
)
celery_app = celery_init_app(app)


# PostgreSQL settings

POSTGRES_ENV_DIR = os.path.join(BASE_DIR, 'envs/.postgres')

load_dotenv(POSTGRES_ENV_DIR)

connection = psycopg2.connect(
        host=os.getenv('POSTGRES_HOST'),
        database=os.getenv('POSTGRES_DATABASE'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD')
)
