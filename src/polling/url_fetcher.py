from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep


class URLFetcher:
    def __init__(self, url):
        self.url = url




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
