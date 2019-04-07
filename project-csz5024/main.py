

from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3 as sql
from login import LoginForm
from parse import ParseStudent
from passlib.hash import sha256_crypt

app = Flask(__name__)

host = 'http://127.0.0.1:5000/'

#connection = sql.connect('database.db')
#connection.close()

@app.route('/')
def index():
    return render_template('index.html', url=host)
    #return render_template('index.html', error=error, url=host)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = form.username.data
        #pw = sha256_crypt.encrypt(str(form.password.data))
        pw = form.password.data
        print(user, pw)
        print(valid_login(user, pw))
        if valid_login(user, pw) == 1:
            flash('Username/Password Successfully found in Database!', 'Success')
            redirect(url_for('login'))
        elif valid_login(user, pw) == 2:
            flash('Error: Incorrect password', 'Error')
            redirect(url_for('login'))
        else:
            flash('Error: Username not found', 'Error')
            redirect(url_for('login'))
    return render_template('login.html', url=host, form=form)


def create_students():
    conn = sql.connect('database.db')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS Students(email TEXT, password TEXT, name TEXT, age INT, gender TEXT, major TEXT, street TEXT, zipcode INT);')
    ParseStudent(cur)
    conn.commit()
    cur.close()
    conn.close()
    return

#binary search?
def valid_login(username, password):
    conn = sql.connect('database.db')
    cur = conn.cursor()
    cur.execute('SELECT email, password FROM Students WHERE email=?', (username,))
    conn.commit()
    db = cur.fetchone()
    print(db)
    # user/pass not found in database
    if db is None:
        cur.close()
        conn.close()
        return 0
    elif password == db[1]:
        cur.close()
        conn.close()
        return 1
    else:
        cur.close()
        conn.close()
        return 2


def view_students():
    conn = sql.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Students;")
    for (email) in cur:
        print(email)



# def valid_name(first_name, last_name):
#     connection = sql.connect('database.db')
#     connection.execute('CREATE TABLE IF NOT EXISTS users(firstname TEXT, lastname TEXT);')
#     connection.execute('INSERT INTO users (firstname, lastname) VALUES (?,?);', (first_name, last_name))
#     connection.commit()
#     cursor = connection.execute('SELECT * FROM users;')
#     return cursor.fetchall()

if (__name__ == '__main__'):
    create_students()
    app.secret_key='test_session'
    #view_students()
    app.run(debug=True)