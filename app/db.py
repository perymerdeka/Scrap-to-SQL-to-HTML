
from mysql.connector import pooling

def get_connection_pool():
    pool = pooling.MySQLConnectionPool(
        pool_name="my_pool",
        pool_size=5,
        host="localhost",
        database='books_db',
        user='root',
        password=''
    )

    return pool

pool = get_connection_pool()
