import time

from watch import WatchScraper, UnsuitableProductError
from loader import db_handler
from loguru import logger

import telegram

def main():
    watch = WatchScraper()

    while True:
        categories = db_handler.get_categories()
        time.sleep(1)
        for url in categories:
            offers_urls = watch.get_offers_urls(url[0])
            if offers_urls:
                for offer_url in offers_urls:
                    try:
                        watch.get_offers(offer_url)
                    except UnsuitableProductError:
                        logger.debug(f'Will be skipped - {offer_url}')

                    time.sleep(3)
            else:
                time.sleep(5)

if __name__ == '__main__':
    main()