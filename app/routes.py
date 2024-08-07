from flask import Blueprint, render_template, request, redirect, url_for, g
import mysql.connector

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
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
