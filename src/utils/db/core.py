import sqlite3

connection = sqlite3.connect('my_database.db')


class DatabaseManager:
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.cur = self.conn.cursor()


    def create_tables(self):
        self.query(
            'CREATE TABLE IF NOT EXISTS users(id INT PRIMARY KEY AUTOINCREMENT, '
            'users_id INT, '
            'username text, '
            'date datetime)'

        )


    def query(self, arg, values=None):
        if values is None:
            self.cur.execute(arg)
        else:
            self.cur.execute(arg, values)
        self.conn.commit()


    def __del__(self):
        self.conn.close()