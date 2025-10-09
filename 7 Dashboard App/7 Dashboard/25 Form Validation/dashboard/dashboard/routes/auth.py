from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash

from dashboard.extensions import db
from dashboard.models import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    error_message = ''

    if request.method == 'POST':
        email_address = request.form.get('email_address')
        password = request.form.get('password')
        remember_me = True if request.form.get('remember_me') == 'on' else False
        
        user = User.query.filter_by(email_address=email_address).first()

        if not user or not check_password_hash(user.password_hash, password):
            error_message = 'Could not login. Please check credentials.'

        if not error_message:    
            login_user(user, remember=remember_me)
            return redirect(url_for('main.index'))

    return render_template('login.html', error_message=error_message)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    error_message = ''

    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email_address = request.form.get('email_address')
        password1 = request.form.get('password')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email_address=email_address).first()

        if user:
            error_message = 'Email already exists. Please log in.'

        passwords_match = password1 == password2

        if not error_message and not passwords_match:
            error_message = 'Passwords do not match!'

        if not error_message:
            user = User(
                name=first_name + ' ' + last_name,
                email_address=email_address,
                password=password1
            )

            db.session.add(user)
            db.session.commit()

            return redirect(url_for('auth.login'))            

    return render_template('register.html', error_message=error_message)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))