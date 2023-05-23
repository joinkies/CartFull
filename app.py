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

    if type(request_data) == list:
        for i in request_data:
            sql_query = """INSERT INTO users (uID, accID) VALUES (?, ?)"""
            cursor.execute(sql_query, (i['uID'], i['accID']))
    elif type(request_data) == dict:
        sql_query = """INSERT INTO users (uID, accID) VALUES (?, ?)"""
        cursor.execute(sql_query, (request_data['uID'], request_data['accID']))
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
    query = f"""INSERT INTO {super_market} (gID, gProductName, gPrice, gPPKG, gStock) VALUES (?, ?, ?, ?, ?)"""

    if type(data) == list:
        for i in data:
            conn.execute(query, (i['gID'], i['gProductName'], i['gPrice'], 'null', i['gStock']))
    elif type(data) == dict:
        cursor.execute(query, (data['gID'], data['gProductName'], data['gPrice'], 'null', data['gStock']))
    else:
        return {"Message": "Items failed to add"}, 200
    conn.commit()
    return {"Message": "Items Added"}, 201


if __name__ == "__main__":
    app.run(debug=True)
