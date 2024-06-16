import celery
import phonenumbers

from celery import shared_task
from flask import render_template, request, redirect, send_from_directory
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect


from settings import app, connection
from forms import UserForm


bcrypt = Bcrypt(app)


csrf = CSRFProtect(app)


messages = []


@app.route("/")
def hello():
    return render_template('index.html')


@app.route("/<path:filename>")
def verify_loader(filename):
    return send_from_directory(app.static_folder, filename)


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
    cursor = connection.cursor()

    username = data['username']
    first_name = data['first_name']
    last_name = data['last_name']
    phone = data['phone']
    email = data['email']
    password = data['password']
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    cursor.execute('INSERT INTO user_info (username, first_name, last_name, phone, email, password)'
                   'VALUES (%s, %s, %s, %s, %s, %s)',
                   (username, first_name, last_name, phone, email, hashed_password)
                   )

    connection.commit()


@app.route("/user_form", methods=('GET', 'POST'))
def user_form():
    form = UserForm(request.form)
    if form.validate() and phone_validated(form.data):
        messages.clear()
        create_user_data(form.data)
        return redirect('/')
    context = {'form': form,
               'messages': messages}
    return render_template('user_form.html', **context)


@shared_task
def async_create_user_data(data):
    cursor = connection.cursor()

    username = data['username']
    first_name = data['first_name']
    last_name = data['last_name']
    phone = data['phone']
    email = data['email']
    password = data['password']
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    cursor.execute('INSERT INTO user_info (username, first_name, last_name, phone, email, password)'
                   'VALUES (%s, %s, %s, %s, %s, %s)',
                   (username, first_name, last_name, phone, email, hashed_password)
                   )

    connection.commit()


@app.route("/async_user_form", methods=('GET', 'POST'))
def async_user_form():
    form = UserForm(request.form)
    if form.validate() and phone_validated(form.data):
        messages.clear()
        async_create_user_data.delay(form.data)
        return redirect('/')
    context = {'form': form,
               'messages': messages}
    return render_template('async_user_form.html', **context)


if __name__ == "__main__":
    app.run()
