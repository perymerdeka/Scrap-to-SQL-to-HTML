
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from app.db import pool
from app.users.forms import LoginForm, RegistrationForm
from app.users.models import User

users_bp = Blueprint('users', __name__)

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            connection = pool.get_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            cursor.close()
            connection.close()
            if user and user['password'] == password:
                user_obj = User(user['id'], user['username'], user['password'])
                login_user(user_obj)
                return redirect(url_for('main.index'))
            else:
                flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@users_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.login'))

@users_bp.route('/register')
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        pass
    
    return render_template ('register.html', form=form)
