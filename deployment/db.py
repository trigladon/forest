import os

from configuration.db import conn

__all__ = (
    'main'
)


def sql_folder_path():
    return os.path.join(os.path.dirname(__file__), 'sql')


def file_content(name):
    path = os.path.join(sql_folder_path(), name)
    if os.path.isfile(path):
        return open(path, 'r').read()


def execute_commit(sql):
    conn.execute(sql)
    conn.commit()


def data(file_name='data.sql'):
    insert_data_sql = file_content(file_name)
    if insert_data_sql:
        execute_commit(insert_data_sql)


def table(file_name='table.sql'):
    create_table_sql = file_content(file_name)
    if create_table_sql:
        execute_commit(create_table_sql)


def main():
    table()
    data()


if __name__ == '__main__':
    main()
