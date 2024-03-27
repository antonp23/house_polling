import sqlite3
import os
import logging
from typing import Set

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

    def get_matches_by_item_id(self, item_id):
        cur = self.con.cursor()
        cur.execute(
            f"select * from {self.table} where item_id='{item_id}'")
        results = sorted(cur.fetchall(), reverse=True, key=lambda x: x[-1])
        return results

    def get_active_item_ids(self) -> Set:
        cur = self.con.cursor()
        cur.execute(
            f"select item_id from {self.table} where valid = 1")
        matches = [item[0] for item in cur.fetchall()]
        return set(matches)

    def add_entry(self, entry: Entry):
        cur = self.con.cursor()
        cur.execute(self.insertion_query, entry.get_field_tuples())
        self.con.commit()
        logging.info(f"[*]Entry {entry.item_id} was successfully added!")

    def change_status_by_id(self, id: int, status: int = 0):
        query = f'''UPDATE {self.table} SET valid = {status} where id = {id}'''
        cur = self.con.cursor()
        cur.execute(query)
        self.con.commit()
        logging.info(f"[*]Entry {id} was disabled")

    def change_status_by_item_id(self, item_id: str, status: int = 0):
        query = f"UPDATE {self.table} SET valid = {status} where item_id = '{item_id}'"
        cur = self.con.cursor()
        cur.execute(query)
        self.con.commit()
        logging.info(f"[*]Entry {item_id} was disabled")



if __name__ == "__main__":
    item_id = "tq5xaw1l"
    setup_logger()
    db = SQLiteDB("../../resources/db", "ramot_karka")
    # items = db.get_active_item_ids()
    # print(type(items), type(list(items)[0]), items)
    results = db.get_matches_by_item_id(item_id)
    print(results)
    # db.change_status_by_item_id("kdigqsvs")
    # results = db.get_matches_by_item_id("kdigqsvs")
    # print(results)


