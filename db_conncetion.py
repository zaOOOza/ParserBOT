import sqlite3


class DataBase():
    DB_LOCATION = "E:/pythonProject/NewsBot/news.db"

    def __init__(self, file='news.db'):
        self.file = file

    def __enter__(self):
        self.conn = sqlite3.connect(self.file)
        self.conn.row_factory = sqlite3.Row
        return self.conn.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if isinstance(exc_val, Exception):
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()


if __name__ == "__main__":
    with DataBase('news.db') as db:
        test = db.execute('select * from news order by rowid desc limit 1').fetchone()



