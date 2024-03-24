import logging as log

from url_config import TARGET_URLS
from src.polling.url_fetcher import URLFetcher


class Orchestrator:
    def __init__(self, target):
        self.target = target
        self.url = TARGET_URLS.get(self.target)
        assert self.url
        log.info(f"Starting Orchestrator with target: {self.target}")
        self.url_fetcher = URLFetcher(self.url)


    def run(self):
        pass


