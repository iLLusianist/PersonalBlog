import sqlite3
import os
from sqlite3 import connect

password_table  = 'users'
test_password_table = 'test_users'
blogs_table = 'blogs'
test_blogs_table = 'test_blogs'

def run(database, _password_table, _test_password_table):
    check_database(database)
    check_table(database, _password_table)
    check_table(database, test_password_table)

def check_database(database):
    try:
        if not os.path.exists(database):
            print(f'Database "{database}" not found')
            create_database(database)
    except Exception as e:
        print(f'"check_database" error {e}')

def create_database(database):
    try:
        connected_db = sqlite3.connect(database)
        print(f'Database "{database}" connected')
        connected_db.close()
    except Exception as e:
        print(f'"create_database" error {e}')

def check_table(database, table):
    try:
        connected_db = connect(database)
        cursor_db = connected_db.cursor()
        cursor_db.execute(f'SELECT name FROM sqlite_master WHERE type = "table" AND name = "{table}"')
        result = cursor_db.fetchone()
        if result is None:
            print(f'Table "{table}" not found')
            create_table(database, table)
        print(f'Table "{table}" is exists')
        connected_db.close()
    except Exception as e:
        print(f'"check_table" error {e}')

def make_sql_create(table):
    sql_create = ''
    if table == password_table or table == test_password_table:
        sql_create = f"""
                CREATE TABLE IF NOT EXISTS {table} (
                    login TEXT PRIMARY KEY,
                    password INTEGER NOT NULL,
                    status TEXT
                );
                """
    elif table == blogs_table or table == test_blogs_table:
        sql_create = f"""
                CREATE TABLE IF NOT EXISTS {table} (
                    title TEXT PRIMARY KEY,
                    text TEXT,
                    created_at TEXT,
                    updated_at TEXT
                );
                """
    print(f'Table "{table}" created')
    return sql_create

def create_table(database, table):
    try:
        connected_db = sqlite3.connect(database)
        cursor_db = connected_db.cursor()
        sql_create = make_sql_create(table)
        if len(sql_create) > 0:
            cursor_db.execute(sql_create)
            connected_db.commit()
            print(f'Table "{table}" created')
        cursor_db.close()
        connected_db.close()
    except Exception as e:
        print(f'"create_table" error {e}')

def blank_table(database, table):
    connected_db = sqlite3.connect(database)
    cursor_db = connected_db.cursor()
    cursor_db.execute(f'DELETE FROM {table}')
    connected_db.commit()
    connected_db.close()