from flask import Flask, request, render_template
# Importing necessary libraries, but we will hae to implement a login system last, as that will be the hardest to deal
import sqlite3

app = Flask(__name__)
DATA_FILE = 'cartfull.sqlite'


def get_database_connection():
    conn = sqlite3.connect(DATA_FILE)
    return conn, conn.cursor()


@app.route('/addUsers', methods=['POST'])
def add_users():
    conn, cursor = get_database_connection()
    request_data = request.get_json()
    query = """INSERT INTO users (uID, accID) VALUES (?, ?)"""

    if type(request_data) == list:
        for i in request_data:
            cursor.execute(query, (i['uID'], i['accID']))
    elif type(request_data) == dict:
        cursor.execute(query, (request_data['uID'], request_data['accID']))
    else:
        return "Failed to insert to table", 200
    conn.commit()
    return {"Message": "Users Added"}, 201


@app.route('/user/<int:user_id>', methods=['GET'])
def user_prof(user_id):
    conn, cursor = get_database_connection()
    user_query = """SELECT accID, uShopLists FROM users WHERE uID = ?"""
    cursor.execute(user_query, (user_id,))
    user = cursor.fetchall()
    return render_template('user.html', user_table=user[0])


@app.route('/viewUsers', methods=['GET'])
def view_users():
    conn, cursor = get_database_connection()

    sql_query = """SELECT * FROM users"""
    cursor.execute(sql_query)
    users = cursor.fetchall()
    return render_template('viewUsers.html', user_table=users)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/addGroceries/<string:super_market>', methods=['GET', 'POST'])
def add_groceries(super_market):
    conn, cursor = get_database_connection()
    data = request.get_json()
    query = f"""INSERT INTO {super_market} (gID, gProductName, gPrice, gPPKG, gStock, gPic) VALUES (?, ?, ?, ?, ?, ?)"""

    if type(data) == list:
        for i in data:
            conn.execute(query, (i['gID'], i['gProductName'], i['gPrice'], 'null', i['gStock'], i['gPic']))
    elif type(data) == dict:
        cursor.execute(query, (data['gID'], data['gProductName'], data['gPrice'], 'null', data['gStock'], data['gPic']))
    else:
        return {"Message": "Items failed to add"}, 200
    conn.commit()
    return {"Message": "Items Added"}, 201


@app.route('/view/<string:super_market>', methods=['GET'])
def view_catalogue_specific(super_market):
    conn, cursor = get_database_connection()

    query = f"""SELECT gProductName, gPic, gPrice  FROM {super_market}"""
    cursor.execute(query)
    items = cursor.fetchall()
    return render_template('view.html', items=items)


@app.route('/searchResults', methods=['POST'])
def show_results():
    conn, cursor = get_database_connection()
    post_data = dict(request.form)
    question = post_data['search-field']
    query = f"""SELECT * FROM newWorld WHERE gProductName
    LIKE '%{question}%'"""
    cursor.execute(query)
    data = cursor.fetchall()
    print(post_data['search-field'])
    return render_template('results.html', data=data, question=question)


if __name__ == "__main__":
    app.run(debug=True)
