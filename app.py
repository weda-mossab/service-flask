from flask import Flask, request, jsonify 
import pymysql
import json
import py_eureka_client.eureka_client as eureka_client

# Creation of an instance named app 
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello CODABI ❤️🙋‍♀️🙋‍♂️!"

if __name__ == '__main__': 
    app.run(port="5000", debug=True)


def db_connection():
    conn = None
    try:
        conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='flask_db',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
        )
    except pymysql.Error as e :
        print(e)
    return conn

# Get all books or add a new book
@app.route('/books', methods=['GET', 'POST'])

def books():
    #ajouter la connexion BD
    conn = db_connection()
    cursor = conn.cursor()
    if request.method == "GET":
        cursor.execute("SELECT * FROM book")
        books=[
        dict(id=row['id'],author=row['author'],language=row['language'],title=row['title'])
        for row in cursor.fetchall()
        ]
    if books is not None:
        return jsonify(books)
    
    if request.method == 'POST':
        new_author = request.form['author']
        new_lang = request.form['language']
        new_title = request.form['title']
        sql = """INSERT INTO book (author, language, title) VALUES (%s, %s, %s)"""
        #question marks are used to protect against SQL injection attacks
        #the ? placeholders will be replaced by the values provided in the execute statement below
        cursor.execute(sql, (new_author, new_lang, new_title))
        #commit changes and close the database connection
        conn.commit()
        #return success message with the id of the last inserted
        #ppour confirmer notre demande nous recuperons l'ID de ce objet en utilisant l'attribut ID 
        #et retun comme une reponse
        
    return f" created successfully"

@app.route('/book/<int:id>',methods=['GET','PUT','DELETE'])

def single_books(id) :
    conn = db_connection()
    cursor = conn.cursor()
    book= None

    if request.method =='GET':
        cursor.execute("SELECT * FROM book WHERE id=%s", (id,))
        row = cursor.fetchone()
        if row:
            book = {'id': row['id'], 'author': row['author'], 'language': row['language'], 'title': row['title']}
            return jsonify(book), 200
        else:
            return "Book not found ", 40
        
    if request.method =='PUT':
        author = request.form['author']
        language = request.form['language']
        title = request.form['title']
        sql = """UPDATE book SET title=%s, author=%s, language=%s WHERE id=%s"""
        cursor.execute(sql, (title, author, language, id))
        conn.commit() 
        updated_book = {'id': id, 'author': author, 'language': language, 'title': title}
        return jsonify(updated_book)
    
    if request.method =='DELETE':
        sql= """DELETE FROM book WHERE id=%s"""
        cursor.execute(sql, (id,)) 
        conn.commit()
        return f"The book with id {id} has been deleted 👾", 200


eureka_client.init(eureka_server="http://localhost:8761/eureka",
app_name="flask_app",
instance_port=8085,
instance_host="localhost")
app.run(port="8085",debug=True) #modifier le port


