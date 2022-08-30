import random
import time

import requests
from loguru import logger
from utils import stopwatch

class Requester:
    def __init__(self):
        self.ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
        self.headers = {'user-agent': self.ua,
                        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}

        self.session = requests.Session()
        self.session.headers = self.headers

        logger.debug('Requester session created')

    @stopwatch
    def get(self, url):
        time.sleep(0.5)
        resp = self.session.get(url)
        resp.raise_for_status()

        logger.info(f'Response received, with status code {resp.status_code} - {url}')
        return resp.text

# def main():
#     req = Requester()
#     req.get('http://forum.watch.ru/forumdisplay.php?f=87')
#
# if __name__ == '__main__':
#     main()