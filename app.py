from flask import Flask, request, render_template, session
import sqlite3

app = Flask(__name__)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE']='filesystem'
session(app)


@app.route('/newUsers', methods=['POST'])
def new_users():
    conn = sqlite3.connect('cartfull.sqlite')
    cursor = conn.cursor()
    request_data = request.get_json()

    if type(request_data) == list:
        for i in request_data:
            new_user = {
                "uID": i['uID'],
                "uAccID": i['uAccID']
            }
            sql_query = """INSERT INTO users (uID, uAccID) VALUES (?, ?)"""
            cursor.execute(sql_query, (new_user['uID'], new_user['uAccID']))
    elif type(request_data) == dict:
        new_user = {
            "uID": request_data['uID'],
            "uAccID": request_data['uAccID']
        }
        sql_query = """INSERT INTO users (uID, uAccID) VALUES (?, ?)"""
        cursor.execute(sql_query, (new_user['uID'], new_user['uAccID']))
    else:
        return "Failed to insert to table", 200
    conn.commit()
    return {"Message": "Users Added"}, 201


@app.route('/user/<int:user_id>', methods=['GET'])
def user_prof(user_id):
    conn = sqlite3.connect('cartfull.sqlite')
    cursor = conn.cursor()
    user_query = """SELECT uAccID, uShopLists FROM users WHERE uID = ?"""
    cursor.execute(user_query, (user_id,))
    user = cursor.fetchall()
    return render_template('user.html', user_table=user)


@app.route('/viewUsers', methods=['GET'])
def view_users():
    conn = sqlite3.connect('cartfull.sqlite')
    cursor = conn.cursor()

    sql_query = """SELECT * FROM users"""
    cursor.execute(sql_query)
    users = cursor.fetchall()
    return render_template('viewUsers.html', user_table=users)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
