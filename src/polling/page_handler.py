from typing import List

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
from bs4 import BeautifulSoup
import logging
import logging as log

from src.db_manager.sqlitedb import SQLiteDB
from src.polling.entry import Entry
from src.utils import setup_logger


class PageHandler:
    def __init__(self, page_content: str, dbhandler: SQLiteDB):
        self.page = BeautifulSoup(page_content, 'html.parser')
        self.dbhandler = dbhandler


    def process(self) -> List:
        processed_entries = []
        entries = self.page.find_all("div", {"class": "feeditem"})
        log.info(f"{len(entries)} initial entries")
        correct_entries = []
        for entry in entries:
            if len(entry['class']) == 2 and "feeditem" in entry['class'] and "table" in entry['class']:
                correct_entries.append(entry)
        log.info(f"{len(correct_entries)} filtered entries")
        for entry_html in correct_entries:
            entry = Entry(entry_html)
            if entry.valid:
                processed_entries.append(entry.item_id)
                # Get possible rows
                possible_enties = self.dbhandler.get_matches_by_item_id(entry.item_id)
                if possible_enties:
                    last_price = possible_enties[0][6]
                    if entry.price != last_price:
                        self.dbhandler.change_status_by_id(possible_enties[0][0])
                        log.info(f"Price update - old price {last_price}!! : {entry}")
                        self.dbhandler.add_entry(entry)
                else:
                    log.info(f"New entry!! : {entry}")
                    self.dbhandler.add_entry(entry)
        return processed_entries


if __name__ == "__main__":
    setup_logger()

    with open("/Users/antonp/code/house_polling/resources/debug/yad2src.html") as f:
        page = f.read()
    db = SQLiteDB("../../resources/db", "ramot_karka")
    handler = PageHandler(page, db)
    handler.process()