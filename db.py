import pymysql

# Creation of a connection
# We will use the connect function
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='flask_db',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor)

cursor = conn.cursor()

# sql_query: to create our table
sql_query = """CREATE TABLE book (
    id integer PRIMARY KEY,
    author text NOT NULL, 
    language text NOT NULL,
    title text NOT NULL
)"""

cursor.execute(sql_query) # Execution of the query

# Closing the connection
conn.close()
