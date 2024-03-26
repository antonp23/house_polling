import os
import sys
from datetime import datetime
import logging as log


def setup_logger(mode=log.DEBUG):
    TIMESTAMP = datetime.now().strftime('%Y-%m-%d_%H.%M.%S')
    # LOG_FILE_PATH = f"logs/{os.path.basename(__file__).replace('.py', '')}_{TIMESTAMP}.log"
    LOG_FORMAT = '%(asctime)s [%(module)s] [%(threadName)s] [%(levelname)s] %(message)s'
    LOG_FORMAT = '%(asctime)s [%(module)s] [%(levelname)s] %(message)s'
    log.basicConfig(format=LOG_FORMAT,
                    datefmt='%Y/%m/%d %H:%M:%S',
                    level=log.DEBUG,
                    handlers=[
                        log.StreamHandler(sys.stdout),
                        # log.FileHandler(LOG_FILE_PATH)
                    ])