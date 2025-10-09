from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user

from dashboard.extensions import db
from dashboard.models import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email_address = request.form.get('email_address')
        password = request.form.get('password')
        remember_me = request.form.get('remember_me')
        
        user = User.query.filter_by(email_address=email_address).first()

        if not user or password != user.password_hash:
            return redirect(url_for('auth.login'))
        
        login_user(user)
        return redirect(url_for('main.index'))

    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email_address = request.form.get('email_address')
        password1 = request.form.get('password')
        password2 = request.form.get('password2')

        user = User(
            name=first_name + ' ' + last_name,
            email_address=email_address,
            password_hash=password1
        )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('auth.login'))

    return render_template('register.html')