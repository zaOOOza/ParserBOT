import sqlite3


class DataBase(object):
    DB_LOCATION = "E:/pythonProject/NewsBot/news.db"

    def __init__(self):
        self.connection = sqlite3.connect(DataBase.DB_LOCATION)
        self.cur = self.connection.cursor()

    def __enter__(self):
        return self

    def close(self):
        self.connection.close()

    def execute(self, new_data):
        self.cur.execute(new_data)

    def executemany(self, many_data):
        self.create_table()
        self.cur.executemany('INSERT INTO news VALUES (?,?,?)', many_data)

    def create_table(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS news(
                        title,
                        link,
                        data_time)''')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cur.close()
        if isinstance(exc_val, Exception):
            self.connection.rollback()
        else:
            self.connection.commit()
        self.connection.close()


if __name__ == "__main__":
    with DataBase() as db:
        db.execute("INSERT INTO news VALUES ('test', 'test', 'test')")

