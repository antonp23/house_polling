import logging as log

from src.db_manager.sqlitedb import SQLiteDB
from url_config import TARGET_URLS
from src.polling.page_handler import PageHandler
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep



class Orchestrator:
    # TODO: refactor
    def __init__(self, target):
        self.target = target
        self.db = SQLiteDB("../../resources/db", self.target)
        self.url = TARGET_URLS.get(self.target)
        assert self.url
        log.info(f"Starting Orchestrator with target: {self.target}")
        self.page_handler = PageHandler(self.url, self.db)


    def run(self):
        pass

if __name__ == "__main__":
    print("testing started")
    driver = webdriver.Chrome()
    driver.get("https://www.saucedemo.com/")
    # sleep(3)
    title = driver.title
    remove_btns = driver.find_elements(By.CLASS_NAME, "form_input")
    for btns in remove_btns:
        print(btns.text, btns.id, btns.id)
    while True:
        sleep(1)
