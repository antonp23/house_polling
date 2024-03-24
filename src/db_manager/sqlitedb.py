import sqlite3
import os


class SQLiteDB:
    def __init__(self, path):
        self.path = os.path.join(path, "test.db")
        self.con = sqlite3.connect(self.path)
        self.cur = self.con.cursor()
        print("Creating table")
        cur = self.cur
        cur.execute("CREATE TABLE if not exists movie(title, year, score)")
        cur.execute("""
            INSERT INTO movie VALUES
                ('Monty Python and the Holy Grail', 1975, 8.2),
                ('And Now for Something Completely Different', 1971, 7.5)
        """)
        self.con.commit()
        print("Fetching results")
        res = cur.execute("SELECT score FROM movie")
        print(res.fetchall())

if __name__ == "__main__":
    db = SQLiteDB("../../resources/db")


