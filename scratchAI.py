import mysql.connector

try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",            # Your MySQL username
        password="",            # Your MySQL password (if any)
        database="test"  # Your database name
    )

    if connection.is_connected():
        print("Connected to MySQL database")

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    if connection.is_connected():
        connection.close()
        print("MySQL connection is closed")
