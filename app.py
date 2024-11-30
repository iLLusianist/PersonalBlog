import sqlite3
import db

from flask import Flask, render_template, request, redirect, url_for, session

from db import blogs_table, test_blogs_table
from flask_session import Session


app = Flask(__name__, static_folder='static')
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = 'abc'
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

DATABASE_NAME = 'login_password.db'
PASSWORD_TABLE  = 'passwords'
TEST_PASSWORD_TABLE = 'test_passwords'
BLOGS_TABLE = 'blogs'
TEST_BLOGS_TABLE = 'test_blogs'


# Redirect functions
@app.route('/', methods=['GET', 'POST'])
def index():
    blogs_list = get_all_from_table(DATABASE_NAME, BLOGS_TABLE)
    logged_in = session.get('logged_in', False)
    return render_template('index.html', logged_in=logged_in, blogs_list=blogs_list)

@app.route('/open_blog', methods=['GET', 'POST'])
def open_blog():
    title = request.args.get('title')
    text = request.args.get('text')
    logged_in = session.get('logged_in', False)
    return render_template('blog.html', logged_in=logged_in, title=title, text=text)

@app.route('/open_sign_in', methods=['GET', 'POST'])
def open_sign_in():
    logged_in = session.get('logged_in', False)
    if not logged_in:
        return render_template('sign_in.html')
    else:
        return render_template('index.html', logged_in=logged_in)

@app.route('/open_sign_up', methods=['GET', 'POST'])
def open_sign_up():
    logged_in = session.get('logged_in', False)
    if not logged_in:
        return render_template('sign_up.html')
    else:
        return render_template('index.html', logged_in=logged_in)

@app.route('/open_add', methods=['GET', 'POST'])
def open_add():
    logged_in = session.get('logged_in', False)
    if not logged_in:
        return render_template('index.html', logged_in=logged_in)
    else:
        return render_template('add.html')

@app.route('/open_edit', methods=['GET', 'POST'])
def open_edit():
    title = request.args.get('title')
    text = request.args.get('text')
    logged_in = session.get('logged_in', False)
    if not logged_in:
        return render_template('index.html', logged_in=logged_in)
    else:
        return render_template('edit.html', title=title, text=text)


# POST functions
@app.route('/registration', methods=['GET', 'POST'])
def form_registration():
    if request.method == 'POST':
        # Получение вводных данных из формы
        login = request.form.get('sign_up_login')
        password = request.form.get('sign_up_password')
        repeat_password = request.form.get('sign_up_repeat_password')

        # Проверка на совпадение введенного пароля
        if password != repeat_password:
            print('Passwords do not match')
            return '<script>alert("Passwords do not match")</script>' + render_template('sign_up.html')

        # Выбор нужной таблицы (тестовой или обычной)
        table = get_table(DATABASE_NAME, PASSWORD_TABLE, TEST_PASSWORD_TABLE, request.form.get('is_test'))
        # Поиск в выбранной таблице
        result = search_first_in_table(DATABASE_NAME, table, 'login', '', login, '')
        # Очистка тестовой таблицы
        if request.form.get('test_ended'): db.blank_table(DATABASE_NAME, table)

        # Если в таблице найден / не найден нужный элемент
        if result is not None:
            print(f'Username "{login}" already taken')
            return f'<script>alert("Username {login} already taken")</script>' + render_template('sign_up.html')
        else:
            add_to_table(DATABASE_NAME, table, login, password)

            print(f'User "{login}" added successfully')
            return redirect(url_for('open_sign_in'))

@app.route('/authorization', methods=['GET', 'POST'])
def form_authorization():
    if request.method == 'POST':
        # Получение вводных данных из формы
        login = request.form.get('sign_in_login')
        password = request.form.get('sign_in_password')

        # Выбор нужной таблицы (тестовой или обычной)
        table = get_table(DATABASE_NAME, PASSWORD_TABLE, TEST_PASSWORD_TABLE, request.form.get('is_test'))
        # Поиск в выбранной таблице
        result = search_first_in_table(DATABASE_NAME, table, 'login', '', login, '')
        # Очистка тестовой таблицы
        if request.form.get('test_ended'): db.blank_table(DATABASE_NAME, table)

        # Если в таблице найден / не найден нужный элемент
        if result is None:
            print(f'Username "{login}" not found')
            return f'<script>alert("Username {login} not found")</script>' + render_template('sign_in.html')
        else:
            # Если введенный пароль совпадает / не совпадает с паролем из БД
            if str(password) != str(result[1]):
                print('Passwords do not match')
                return '<script>alert("Passwords do not match")</script>' + render_template('sign_in.html')
            else:
                session['logged_in'] = True

                print('Logged')
                return redirect(url_for('index'))

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session['logged_in'] = False
        return redirect(url_for('index'))

@app.route('/write_blog', methods=['GET', 'POST'])
def write_blog():
    if request.method == 'POST':
        # Получение вводных данных из формы
        title_text = request.form.get('add_title')
        blog_text = request.form.get('add_text')

        # Если одно из полей пустое
        if len(title_text)<1 or len(blog_text)<1:
            print(f'Title or text is empty')
            return f'<script>alert("Title or text is empty")</script>' + render_template('add.html', title=title_text, text=blog_text)
        else:
            # Выбор нужной таблицы (тестовой или обычной)
            table = get_table(DATABASE_NAME, BLOGS_TABLE, TEST_BLOGS_TABLE, request.form.get('is_test'))
            # Поиск в выбранной таблице
            result = search_first_in_table(DATABASE_NAME, table, 'title', '', title_text, '')
            # Очистка тестовой таблицы
            if request.form.get('test_ended'): db.blank_table(DATABASE_NAME, table)

            # Если в таблице найден / не найден нужный элемент
            if result is not None:
                print(f'Blog with title "{title_text}" already exists')
                return f'<script>alert("Blog with title {title_text} already exists")</script>' + render_template(
                    'add.html', title=title_text, text=blog_text)
            else:
                add_to_table(DATABASE_NAME, table, title_text, blog_text)

                print(f'Blog with title "{title_text}" successfully added to table "{table}"')
                return redirect(url_for('index'))

@app.route('/edit_blog', methods=['GET', 'POST'])
def edit_blog():
    if request.method == 'POST':
        # Получение вводных данных из формы
        logged_in = session.get('logged_in', False)
        title_text = request.form.get('edit_title')
        blog_text = request.form.get('edit_text')
        previous_title = request.args.get('title')

        print(f'Previous_title: {previous_title}')
        print(f'is logged = {logged_in}')

        if logged_in:
            # Выбор нужной таблицы (тестовой или обычной)
            table = get_table(DATABASE_NAME, blogs_table,test_blogs_table, request.form.get('is_test'))
            # Поиск в выбранной таблице
            result = search_first_in_table(DATABASE_NAME, table, 'title', '', title_text, '')
            # Очистка тестовой таблицы
            if request.form.get('test_ended'): db.blank_table(DATABASE_NAME, table)

            print(f'result: "{result}"')

            if result is not None:
                print(f'Blog with title "{title_text}" already exists')
                return f'<script>alert("Blog with title {title_text} already exists")</script>' + render_template(
                    'edit.html', title=previous_title, text=blog_text)
            else:
                update_row(DATABASE_NAME, table, 'title', title_text, previous_title)

                print(f'Blog with title "{title_text}" successfully updated in table "{table}"')
                return redirect(url_for('index'))


# Local functions
def get_table(database, table, test_table, is_test):
    db.check_database(database)
    if is_test is not None:
        print('Request from TEST')
        db.check_table(database, test_table)
        return test_table
    else:
        db.check_table(database, table)
        return table

def get_all_from_table(database, table):
    try:
        with sqlite3.connect(database) as connected_db:
            cursor_db = connected_db.cursor()
            cursor_db.execute(f'SELECT * FROM {table}')
            return cursor_db.fetchall()
    except Exception as e:
        print(f'"get_all_blogs" error: "{e}"')

def add_to_table(database, table, first_column_value, second_column_value):
    try:
        with sqlite3.connect(database) as connected_db:
            sql_insert = f'INSERT INTO {table} VALUES (?, ?)'
            cursor_db = connected_db.cursor()
            cursor_db.execute(sql_insert, (first_column_value, second_column_value))
            connected_db.commit()
    except Exception as e:
        print(f'"att_to_table" error: "{e}"')

def search_first_in_table(database, table, first_column, second_column, first_column_value, second_column_value):
    try:
        with sqlite3.connect(database) as connected_db:
            cursor_db = connected_db.cursor()
            check_query = f'SELECT * FROM {table} WHERE LOWER({first_column}) = ?'
            cursor_db.execute(check_query, (first_column_value.lower(),))
            return cursor_db.fetchone()
    except Exception as e:
        print(f'"search_first_in_table" error: "{e}"')

def update_row(database, table, column, column_value, column_condition):
    try:
        with sqlite3.connect(database) as connected_db:
            cursor_db = connected_db.cursor()
            update_query = f'UPDATE {table} SET {column} = ? WHERE {column} = ?'
            cursor_db.execute(update_query,(column_value, column_condition))
            connected_db.commit()
    except Exception as e:
        print(f'"update_row" error: "{e}"')


# Start APP
if __name__ == '__main__':
    db.run(DATABASE_NAME, PASSWORD_TABLE, TEST_PASSWORD_TABLE)
    app.run(debug=True)

