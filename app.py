from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)
DATABASE = 'database.db'


def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT)")
    conn.commit()
    conn.close()


@app.route('/users', methods=['GET'])
def get_users():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    
    user_list = []
    for user in users:
        user_dict = {'id': user[0], 'name': user[1], 'email': user[2]}
        user_list.append(user_dict)
    
    return jsonify(user_list)


@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data['name']
    email = data['email']
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'User created successfully'})


if __name__ == '__main__':
    create_table()
    app.run()
