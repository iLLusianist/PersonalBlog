from flask import Flask, render_template, request, flash
import sqlite3

from db import db_lp, cursor_db

app = Flask(__name__, static_folder='static')
app.secret_key = 'abc'
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def index():  # put application's code here
    return render_template('index.html')
@app.route('/open_sign_in')
def open_sign_in():
    return render_template('sign_in.html')
@app.route('/open_sign_up')
def open_sign_up():
    return render_template('sign_up.html')

@app.route('/authorization', methods = ['GET', 'POST'])
def form_authorization():
    if request.method == 'POST':
        login = request.form.get('sign_in_login')
        password = request.form.get('sign_in_password')
        try:
            db_lp = sqlite3.connect('login_password.db')
            with db_lp:
                cursor_db = db_lp.cursor()
                check_query = 'SELECT * FROM passwords WHERE login = ?'
                cursor_db.execute(check_query, (login,))
                result = list(cursor_db.fetchone())
                if result[1] == int(password):
                    return render_template('index.html')
                else:
                    return render_template('sign_in.html')
        except Exception as e:
            flash(f'Error {e}')
        return render_template('sign_in.html')
    return render_template('sign_in.html')

@app.route('/registration', methods = ['GET', 'POST'])
def form_registration():
    if request.method == 'POST':
        login = request.form.get('sign_up_login')
        password = request.form.get('sign_up_password')
        repeat_password = request.form.get('sign_up_repeat_password')

        if password != repeat_password:
            flash('Пароли не совпадают')
            return render_template('sign_up.html')

        try:
            db_lp = sqlite3.connect('login_password.db')
            with db_lp:
                cursor_db = db_lp.cursor()
                check_query = 'SELECT * FROM passwords WHERE login = ?'
                cursor_db.execute(check_query, (login,))
                result = cursor_db.fetchone()


                if result is not None:
                    flash('Логин уже занят')
                    return render_template('sign_up.html')
                sql_insert = 'INSERT INTO passwords VALUES (?, ?)'
                cursor_db.execute(sql_insert, (login, password))
        except sqlite3.Error as e:
            print(f'Ошибка базы данных {e}')
        except Exception as e:
            print(f'Error {e}')
        finally:
            cursor_db.close()
            db_lp.close()

        return render_template('sign_in.html')
    else:
        return render_template('sign_up.html')


if __name__ == '__main__':
    app.run(debug=True)
