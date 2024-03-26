from bs4.element import Tag
import logging
from selenium.webdriver.common.by import By
from datetime import datetime


class Entry:
    def __init__(self, entry: Tag):
        self.valid = False
        item = entry.find_all("div", {"class", "feed_item"})[0]
        if "accordion" not in item.get("class"):
            return
        page_id = item.get("id").split("_")[-1]
        # ID
        self.item_id = item.get("item-id")
        # Address
        self.address = item.find_all("span", {"class", f"title"})[0].text.strip()
        # rooms
        self.rooms = item.find("span", {"id": f"data_rooms_{page_id}"}).text.strip()
        # floor
        self.floor = item.find("span", {"id": f"data_floor_{page_id}"}).text.strip()
        # size
        self.size = item.find("span", {"id": f"data_SquareMeter_{page_id}"}).text.strip()
        # price
        self.price = item.find_all("div", {"class", f"price"})[0].text.strip()
        # Seller type
        self.seller_type = "tivuh" if len(item.find_all("div", {"class", f"merchant_name"})) else "private"
        # Update time
        self.date = str(datetime.now())
        self.valid = True
        # logging.debug(str(self))

    def __str__(self):
        return f"Entry {self.item_id} ({self.date}):\n\taddress: {self.address}\n\trooms: {self.rooms}\n\tfloor: {self.floor}" \
               f"\n\tsize: {self.size}\n\tprice: {self.price}\n\tseller_type: {self.seller_type}"

    def get_field_tuples(self):
        # item_id, address, rooms, floor, size, price, seller_type, date
        return (self.item_id, self.address, self.rooms, self.floor, self.size, self.price, self.seller_type, self.date)