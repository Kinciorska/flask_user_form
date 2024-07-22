import phonenumbers

from celery import shared_task
from flask import render_template, request, redirect, jsonify
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect

from flaskr import app, db
from .worker import phone_validated_task, async_create_user_data_task

from .forms import UserForm
from .db import User


bcrypt = Bcrypt(app)

csrf = CSRFProtect(app)


messages = []


@app.route("/test/")
def hello_world():
    return jsonify(hello="world")


@app.route("/")
def hello():
    return render_template('index.html')


def phone_validated(data):
    phone_number = data['phone']
    try:
        parsed_phone_number = phonenumbers.parse(phone_number, None)
        return phonenumbers.is_possible_number(parsed_phone_number)
    except phonenumbers.phonenumberutil.NumberParseException:
        messages.append({'title': "Error",
                         'content': "Phone number must be in format +00 123456789,"
                                    " and must have a valid country code."})
        return False


def create_user_data(data):
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


@app.route("/user_form/", methods=('GET', 'POST'))
def user_form():
    form = UserForm(request.form)
    if form.validate() and phone_validated(form.data):
        messages.clear()
        create_user_data(form.data)
        return redirect('/')
    context = {'form': form,
               'messages': messages}
    return render_template('user_form.html', **context)


@app.route("/async_user_form/", methods=('GET', 'POST'))
def async_user_form():
    form = UserForm(request.form)
    if form.validate() and phone_validated_task.delay(form.data):
        messages.clear()
        async_create_user_data_task.delay(form.data)
        return redirect('/')
    context = {'form': form,
               'messages': messages}
    return render_template('async_user_form.html', **context)
