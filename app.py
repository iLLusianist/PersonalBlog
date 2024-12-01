import sqlite3
import db

from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session


app = Flask(__name__, static_folder='static')
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = 'abc'
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

DATABASE_NAME = 'Personal_Blog.db'
USERS_TABLE  = 'users'
TEST_USERS_TABLE = 'test_users'
BLOGS_TABLE = 'blogs'
TEST_BLOGS_TABLE = 'test_blogs'
USER_STATUS = {
    'user': 'User',
    'admin': 'Admin'
}


# Redirect functions
@app.route('/', methods=['GET', 'POST'])
def index():
    db.check_table(DATABASE_NAME, BLOGS_TABLE)
    blogs_list = get_all_from_table(DATABASE_NAME, BLOGS_TABLE)

    login = session.get('login')

    if login is not None:
        logged_in = session.get('logged_in', False)
        check_status(session.get('login'))
        is_admin = session.get('is_admin', False)
    else:
        logged_in = False
        is_admin = False

    return render_template('index.html', logged_in=logged_in, is_admin=is_admin, blogs_list=blogs_list)

@app.route('/open_blog', methods=['GET', 'POST'])
def open_blog():
    title = request.args.get('title')
    text = request.args.get('text')
    logged_in = session.get('logged_in', False)
    check_status(session.get('login'))
    is_admin = session.get('is_admin', False)
    if logged_in:
        return render_template('blog.html', logged_in=logged_in, is_admin=is_admin, title=title, text=text)
    else:
        return redirect(url_for('index'))

@app.route('/open_sign_in', methods=['GET', 'POST'])
def open_sign_in():
    logged_in = session.get('logged_in', False)
    if not logged_in:
        return render_template('sign_in.html')
    else:
        return redirect(url_for('index'))

@app.route('/open_sign_up', methods=['GET', 'POST'])
def open_sign_up():
    logged_in = session.get('logged_in', False)
    if not logged_in:
        return render_template('sign_up.html')
    else:
        return redirect(url_for('index'))

@app.route('/open_add', methods=['GET', 'POST'])
def open_add():
    check_status(session.get('login'))
    is_admin = session.get('is_admin', False)
    if is_admin:
        return render_template('add.html')
    else:
        return redirect(url_for('index'))

@app.route('/open_edit', methods=['GET', 'POST'])
def open_edit():
    title = request.args.get('title')
    text = request.args.get('text')
    check_status(session.get('login'))
    is_admin = session.get('is_admin', False)
    if is_admin:
        return render_template('edit.html', title=title, text=text)
    else:
        return redirect(url_for('index'))

@app.route('/open_admin', methods=['GET', 'POST'])
def open_admin():
    check_status(session.get('login'))
    is_admin = session.get('is_admin', False)
    if is_admin:
        return render_template('admin.html', user_status=USER_STATUS)
    else:
        return redirect(url_for('index'))


# POST functions
@app.route('/registration', methods=['GET', 'POST'])
def registration():
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
        table = get_table(DATABASE_NAME, USERS_TABLE, TEST_USERS_TABLE, request.form.get('is_test'))
        # Поиск в выбранной таблице
        result = search_first_in_table(DATABASE_NAME, table,{'login': login})

        # Если в таблице найден / не найден нужный элемент
        if result is not None:
            # Очистка тестовой таблицы
            if request.form.get('test_ended'): db.blank_table(DATABASE_NAME, table)

            print(f'Username "{login}" already taken')
            return f'<script>alert("Username {login} already taken")</script>' + render_template('sign_up.html')
        else:
            hashed_password = generate_password_hash(password)
            add_to_table(DATABASE_NAME, table, login, hashed_password, USER_STATUS['user'])

            # Очистка тестовой таблицы
            if request.form.get('test_ended'): db.blank_table(DATABASE_NAME, table)

            print(f'User "{login}" added successfully with status "{USER_STATUS["user"]}"')
            return redirect(url_for('open_sign_in'))

@app.route('/authorization', methods=['GET', 'POST'])
def authorization():
    if request.method == 'POST':
        # Получение вводных данных из формы
        login = request.form.get('sign_in_login')
        password = request.form.get('sign_in_password')

        # Выбор нужной таблицы (тестовой или обычной)
        table = get_table(DATABASE_NAME, USERS_TABLE, TEST_USERS_TABLE, request.form.get('is_test'))
        # Поиск в выбранной таблице
        result = search_first_in_table(DATABASE_NAME, table, {'login': login})
        # Очистка тестовой таблицы
        if request.form.get('test_ended'): db.blank_table(DATABASE_NAME, table)

        # Если в таблице найден / не найден нужный элемент
        if result is None:
            print(f'Username "{login}" not found')
            return f'<script>alert("Username {login} not found")</script>' + render_template('sign_in.html')
        else:
            # Если введенный пароль совпадает / не совпадает с паролем из БД
            if not check_password_hash(str(result[1]), password):
                print('Passwords do not match')
                return '<script>alert("Passwords do not match")</script>' + render_template('sign_in.html')
            else:
                session['logged_in'] = True
                session['login'] = login

                print(f'"{login}" logged')
                return redirect(url_for('index'))

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session['logged_in'] = False
        session['login'] = None
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
            return f'<script>alert("Title or text is empty")</script>' + render_template('add.html', title=title_text,
                                                                                         text=blog_text)
        else:
            # Выбор нужной таблицы (тестовой или обычной)
            table = get_table(DATABASE_NAME, BLOGS_TABLE, TEST_BLOGS_TABLE, request.form.get('is_test'))
            # Поиск в выбранной таблице
            result = search_first_in_table(DATABASE_NAME, table, {'title': title_text})
            # Очистка тестовой таблицы
            if request.form.get('test_ended'): db.blank_table(DATABASE_NAME, table)

            # Если в таблице найден / не найден нужный элемент
            if result is not None:
                print(f'Blog with title "{title_text}" already exists')
                return f'<script>alert("Blog with title {title_text} already exists")</script>' + render_template(
                    'add.html', title=title_text, text=blog_text)
            else:
                add_to_table(DATABASE_NAME, table, title_text, blog_text, '', '')

                print(f'Blog with title "{title_text}" successfully added to table "{table}"')
                return redirect(url_for('index'))

@app.route('/edit_blog', methods=['GET', 'POST'])
def edit_blog():
    if request.method == 'POST':
        # Получение вводных данных из формы
        new_title = request.form.get('edit_title')
        new_text = request.form.get('edit_text')
        previous_title = request.args.get('title')

        # Выбор нужной таблицы (тестовой или обычной)
        table = get_table(DATABASE_NAME, BLOGS_TABLE, TEST_BLOGS_TABLE, request.form.get('is_test'))

        # Если заголовок изменен
        if previous_title != new_title:
            # Поиск в выбранной таблице
            result = search_first_in_table(DATABASE_NAME, table, {'title': new_title})

            if result is not None:
                # Очистка тестовой таблицы
                if request.form.get('test_ended'): db.blank_table(DATABASE_NAME, table)

                print(f'Blog with title "{new_title}" already exists')
                return f'<script>alert("Blog with title {new_title} already exists")</script>' + render_template(
                    'edit.html', title=previous_title, text=new_text)
            else:
                # Обновление столбцов 'title' и 'text'
                update_row(DATABASE_NAME, table, ['title', new_title, 'title', previous_title])
                update_row(DATABASE_NAME, table, ['text', new_text, 'title', new_title])
        else:
            # Обновление столбца 'text'
            update_row(DATABASE_NAME, table, ['text', new_text, 'title', previous_title])

        # Очистка тестовой таблицы
        if request.form.get('test_ended'): db.blank_table(DATABASE_NAME, table)

        print(f'Blog with title "{new_title}" successfully updated in table "{table}"')
        return redirect(url_for('index'))

@app.route('/make_admin', methods=['GET', 'POST'])
def make_admin():
    if request.method == 'POST':
        # Получение вводных данных из формы
        user = request.form.get('admin_input')
        status = request.form.get('user_status')

        if len(user) < 1:
            print('User is empty')
            return f'<script>alert("User is empty")</script>' + render_template('admin.html', user_status=USER_STATUS)
        else:
            # Выбор нужной таблицы (тестовой или обычной)
            table = get_table(DATABASE_NAME, USERS_TABLE, TEST_USERS_TABLE, request.form.get('is_test'))
            # Поиск в выбранной таблице
            result = search_first_in_table(DATABASE_NAME, table, {'login': user})

            if result is None:
                # Очистка тестовой таблицы
                if request.form.get('test_ended'): db.blank_table(DATABASE_NAME, table)

                print(f'User "{user}" not found')
                return f'<script>alert("User {user} not found")</script>' + render_template('admin.html',
                                                                                            user_status=USER_STATUS)
            else:
                result_list = list(result)

                if result_list[2] != USER_STATUS.get(status):
                    update_row(DATABASE_NAME, USERS_TABLE, ['status', USER_STATUS.get(status), 'login', user])
                    print(f'Status "{list(result)[2]}" for user "{user}" updated to "{status}"')
                else:
                    print(f'User "{user}" already have status "{status}"')
                    return (f'<script>alert("User {user} already have status {status}")</script>' +
                            render_template('admin.html', user_status=USER_STATUS))
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
        print(f'"get_all_from_table" error: "{e}"')

def add_to_table(database, table, *values):
    try:
        with sqlite3.connect(database) as connected_db:
            placeholder = ', '.join('?' for _ in values)
            sql_insert = f'INSERT INTO {table} VALUES ({placeholder})'
            cursor_db = connected_db.cursor()
            cursor_db.execute(sql_insert, values)
            connected_db.commit()
    except Exception as e:
        print(f'"att_to_table" error: "{e}"')

def search_first_in_table(database, table, conditions):
    try:
        with sqlite3.connect(database) as connected_db:
            cursor_db = connected_db.cursor()

            where_clauses = []
            params = []

            for column, value in conditions.items():
                where_clauses.append(f'LOWER({column}) = ?')
                params.append(value.lower())

            check_query = query = f'SELECT * FROM {table} WHERE {" AND ".join(where_clauses)}'
            cursor_db.execute(check_query, params)
            return cursor_db.fetchone()
    except Exception as e:
        print(f'"search_first_in_table" error: "{e}"')

def update_row(database, table, to_update):
    '''
    :param database: Database to update
    :param table: Table to update
    :param to_update: Updated column, New value, Conditional column, Conditional value
    :return:
    '''

    try:
        with sqlite3.connect(database) as connected_db:
            cursor_db = connected_db.cursor()
            update_query = f'UPDATE {table} SET {to_update[0]} = ? WHERE {to_update[2]} = ?'
            cursor_db.execute(update_query,(to_update[1], to_update[3]))
            connected_db.commit()
    except Exception as e:
        print(f'"update_row" error: "{e}"')

def check_status(login):
    table = get_table(DATABASE_NAME, USERS_TABLE, TEST_USERS_TABLE, None)
    result = search_first_in_table(DATABASE_NAME, table, {'login': login, 'status': USER_STATUS['admin']})
    if result is None:
        session['is_admin'] = False
    else:
        session['is_admin'] = True


# Start APP
if __name__ == '__main__':
    db.run(DATABASE_NAME)
    app.run(debug=True)

