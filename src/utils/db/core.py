import sqlite3



connection = sqlite3.connect('my_database.db')


class DatabaseManager:
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.cur = self.conn.cursor()


    def create_tables(self):
        self.query(
            'CREATE TABLE IF NOT EXISTS users('
            'id INTEGER PRIMARY KEY AUTOINCREMENT, '
            'user_id INTEGER, '
            'first_name text, '
            'last_name text, '
            'username text, '
            'first_entry TIMESTAMP DEFAULT CURRENT_TIMESTAMP, )'
        )


    def query(self, sql, params=None):
        try:
            if params is None:
                self.cur.execute(sql)
            else:
                self.cur.execute(sql, params)
        except sqlite3.Error as e:
            print()
        self.conn.commit()


    def __del__(self):
        self.conn.close()