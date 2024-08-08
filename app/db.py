from mysql.connector import pooling

def get_connection_pool():
    pool = pooling.MySQLConnectionPool(
        pool_name="mypool",
        pool_size=5,
        host="localhost",
        user="root",
        password="",  # Your MySQL password if any
        database="books_db",
        charset='utf8mb4',
        collation='utf8mb4_general_ci'
    )
    return pool

pool = get_connection_pool()
