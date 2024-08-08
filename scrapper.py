import requests
from bs4 import BeautifulSoup
import mysql.connector

def scrape_books():
    url = 'http://books.toscrape.com/catalogue/page-1.html'
    books = []

    while url:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        articles = soup.find_all('article', class_='product_pod')
        for article in articles:
            title = article.h3.a['title']
            price = article.find('p', class_='price_color').text
            availability = article.find('p', class_='instock availability').text.strip()
            books.append((title, price, availability))

        next_button = soup.find('li', class_='next')
        if next_button:
            next_url = next_button.a['href']
            url = 'http://books.toscrape.com/catalogue/' + next_url
        else:
            url = None

    return books

def insert_into_db(books):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Your MySQL password if any
            database="books_db"
        )
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS books (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), price VARCHAR(255), availability VARCHAR(255))")
        cursor.executemany("INSERT INTO books (title, price, availability) VALUES (%s, %s, %s)", books)
        connection.commit()
        print("Data inserted successfully")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        connection = None

    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

if __name__ == "__main__":
    books = scrape_books()
    insert_into_db(books)
