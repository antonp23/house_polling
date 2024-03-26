import sqlite3
import os
import logging

from src.polling.entry import Entry
from src.utils import setup_logger


class SQLiteDB:
    def __init__(self, path, table):
        self.path = os.path.join(path, "houses.db")
        self.table = table
        self.con = sqlite3.connect(self.path)
        cur = self.con.cursor()
        logging.info(f"Creating table {self.table}")
        cur.execute(f"CREATE TABLE if not exists {self.table}(id integer primary key, item_id, address, rooms, floor, size, price, seller_type, date, valid)")
        self.con.commit()
        logging.info("Fetching results")
        res = cur.execute(f"SELECT * FROM {self.table}")
        logging.info(f"Total entries in {self.table} - {len(res.fetchall())}")
        self.insertion_query = f''' INSERT INTO {self.table}(id, item_id, address, rooms, floor, size, price, seller_type, date, valid)
              VALUES(NULL,?,?,?,?,?,?,?,?,1) '''

    def get_matches_by_id(self, item_id):
        cur = self.con.cursor()
        cur.execute(
            f"select * from {self.table} where item_id='{item_id}'")
        results = sorted(cur.fetchall(), reverse=True, key=lambda x: x[-1])
        return results

    def add_entry(self, entry: Entry):
        cur = self.con.cursor()
        cur.execute(self.insertion_query, entry.get_field_tuples())
        self.con.commit()
        logging.info(f"Entry {entry.item_id} was successfully added!")



if __name__ == "__main__":
    setup_logger()
    db = SQLiteDB("../../resources/db", "ramot_karka")
    results = db.get_matches_by_id("kdigqsvs")
    print(results)


