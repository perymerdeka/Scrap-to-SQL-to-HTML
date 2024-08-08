import mysql.connector

connection = mysql.connector.connect(host="localhost", user="root", passwd="", database="test")

if connection.is_connected():
    print('Connected')
else:
    print('Not Connected')

connection.close()