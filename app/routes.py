from flask import Blueprint, render_template, request, redirect, url_for, g, flash
from flask_login import login_user, login_required, logout_user, current_user
from .forms import LoginForm, RegistrationForm
from .models import User
from .db import pool
import mysql.connector

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    search_query = request.form.get('search_query') if request.method == 'POST' else ''
    try:
        cursor = g.db.cursor(dictionary=True)
        if search_query:
            query = "SELECT * FROM books WHERE title LIKE %s"
            cursor.execute(query, (f"%{search_query}%",))
        else:
            cursor.execute("SELECT * FROM books")
        books = cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        books = []
    finally:
        cursor.close()
    return render_template('index.html', books=books, search_query=search_query)

@main.route('/delete/<int:book_id>', methods=['POST'])
@login_required
def delete_book(book_id):
    try:
        cursor = g.db.cursor()
        cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
        g.db.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
    return redirect(url_for('main.index'))

@main.route('/add', methods=['POST'])
@login_required
def add_book():
    title = request.form['title']
    price = request.form['price']
    availability = request.form['availability']
    try:
        cursor = g.db.cursor()
        cursor.execute("INSERT INTO books (title, price, availability) VALUES (%s, %s, %s)", (title, price, availability))
        g.db.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
    return redirect(url_for('main.index'))

@main.route('/update', methods=['POST'])
@login_required
def update_book():
    book_id = request.form['id']
    new_title = request.form['title']
    new_price = request.form['price']
    new_availability = request.form['availability']
    try:
        cursor = g.db.cursor()
        cursor.execute("UPDATE books SET title = %s, price = %s, availability = %s WHERE id = %s", (new_title, new_price, new_availability, book_id))
        g.db.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
    return redirect(url_for('main.index'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
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

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        try:
            connection = pool.get_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            connection.commit()
            cursor.close()
            connection.close()
            flash('You have successfully registered! Please log in.', 'success')
            return redirect(url_for('main.login'))
        except mysql.connector.Error as err:
            flash(f"Error: {err}", 'danger')
    return render_template('register.html', form=form)
