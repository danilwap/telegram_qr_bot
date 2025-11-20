import sqlite3

from logging_config import get_logger

logger = get_logger(__name__)



from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # корень проекта
DB_PATH = BASE_DIR / "data" / "my_database.db"




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
            'first_entry TIMESTAMP DEFAULT CURRENT_TIMESTAMP)'
        )
        print('creating tables... 50%')
        self.query(
            'CREATE TABLE IF NOT EXISTS qr_generations('
            'id INTEGER PRIMARY KEY AUTOINCREMENT, '
            'user_id INTEGER, '
            'username TEXT, '
            'generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, '
            'text TEXT)'
        )
        print('creating tables... 100%')

    def query(self, sql, params=None):
        try:
            if params is None:
                self.cur.execute(sql)
            else:
                self.cur.execute(sql, params)
        except sqlite3.Error as e:
            print(e)
        self.conn.commit()


    def fetchone(self, sql, params=None):
        try:
            if params is None:
                self.cur.execute(sql)
            else:
                self.cur.execute(sql, params)
            return self.cur.fetchone()
        except sqlite3.Error as e:
            logger.error(e)

    def fetchall(self, sql, params=None):
        try:
            if params is None:
                self.cur.execute(sql)
            else:
                self.cur.execute(sql, params)
            return self.cur.fetchall()
        except sqlite3.Error as e:
            logger.error(e)

    def close(self):
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()