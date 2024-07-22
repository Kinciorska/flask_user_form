import phonenumbers

from celery import Celery, Task
from flask import Flask
from flask_bcrypt import Bcrypt


from flaskr import app, db
from .config import CeleryConfig
from .db import User

bcrypt = Bcrypt(app)


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(CeleryConfig)
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app


celery_app = celery_init_app(app)


celery_app.autodiscover_tasks()


__all__ = ['celery_app']


@celery_app.task(name='phone_validated_task')
def phone_validated_task(data):
    phone_number = data['phone']
    try:
        parsed_phone_number = phonenumbers.parse(phone_number, None)
        return phonenumbers.is_possible_number(parsed_phone_number)
    except phonenumbers.phonenumberutil.NumberParseException:
        return False


@celery_app.task(name='async_create_user_data_task')
def async_create_user_data_task(data):
    username = data['username']
    first_name = data['first_name']
    last_name = data['last_name']
    phone = data['phone']
    email = data['email']
    password = data['password']
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username,
                    first_name=first_name,
                    last_name=last_name,
                    phone=phone,
                    email=email,
                    password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
