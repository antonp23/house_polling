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
        self.db = SQLiteDB("/Users/antonp/code/house_polling/resources/db", self.target)
        self.url = TARGET_URLS.get(self.target)
        assert self.url
        log.info(f"Starting Orchestrator with target: {self.target}")
        self.page_number = 1


    def run(self):
        options = Options()
        active_items = self.db.get_active_item_ids()
        options.add_argument(
            "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36")
        driver = webdriver.Chrome(options=options)
        log.info(f"[!]Loading {self.url}")
        driver.get(self.url)
        input("Please wait until all validations are finished and press any key")
        # Handle pagination
        pages_to_iterate = 1
        pagination = driver.find_elements(By.CLASS_NAME, "numbers")
        if pagination:
            pages_to_iterate = len(pagination[0].find_elements(By.TAG_NAME, "a")) + len(pagination[0].find_elements(By.TAG_NAME, "button"))
            log.info(f"[!]There are {pages_to_iterate} pages to iterate")

        active_items = active_items.difference(set(self._handle_page(driver)))
        while self.page_number <= pages_to_iterate:
            paged_url = self.url + f"&page={self.page_number}"
            log.info(f"[!]Loading {paged_url}")
            driver.get(paged_url)
            active_items = active_items.difference(set(self._handle_page(driver)))
        log.info(f"[!]After processing all items {len(active_items)} were deleted!")
        for deleted_item in active_items:
            self.db.change_status_by_item_id(deleted_item)



    def _handle_page(self, driver):
        input("Please wait until all validations are finished and press any key")
        page_content = driver.page_source
        page_handler = PageHandler(page_content, self.db)
        processed_entries = page_handler.process()
        self.page_number += 1
        return processed_entries


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
