import sys

from offer import Offer
from requester import Requester
from bs4 import BeautifulSoup
from utils import stopwatch
from loguru import logger
from loader import db_handler
import re

class UnsuitableProductError(Exception):
    pass

class WatchScraper:
    def __init__(self):
        self.req = Requester()

    # Получает ссылки на офферы
    @stopwatch
    def get_offers_urls(self, url: str) -> list:
        urls_list = []
        last_page_title = ''

        for i in range(1, 9999):
            content = self.req.get(f'{url}&page={i}')

            soup = BeautifulSoup(content, 'lxml')

            if soup.find('title').text == last_page_title:
                logger.debug(f'Last page: {i-1}')
                break

            last_page_title = soup.find('title').text

            all_a = soup.find_all('a', {'href': re.compile(r'^showthread.php\?[a-z0-9\=\&\;]*t=')})

            for a in all_a:
                urls_list.append('http://forum.watch.ru/' + a.get('href'))

        viewed_links = db_handler.get_viewed_links()
        for url in viewed_links:
            if url in urls_list:
                urls_list.remove(url)

        logger.debug(f'New urls found: {len(urls_list)}')
        return urls_list

    @stopwatch
    def get_offer(self, url: str) -> Offer:
        logger.debug(f'Parsing offer - {url}')
        content = self.req.get(url)
        soup = BeautifulSoup(content, 'lxml')

        offer = Offer(url)

        message_body = soup.find_all('div', class_='messagebody')[0]

        try:
            offer.title = message_body.find('b').text.strip()
        except AttributeError:
            logger.warning(f'Title was not found: {offer.title}')
        else:
            logger.debug(f'Title was found: {offer.title}')

        offer.price = re.search(r'цена:* [a-z0-9\s\.\$]*', message_body.text.lower()).group(0).strip()
        logger.debug(f'Price was found: {offer.price}')

        offer.description = message_body.text.replace('\n\n', '\n')
        if len(offer.description) > 650:
            offer.description = offer.description[:500]

        logger.debug('Description was found')

        try:
            offer.photo = 'http://forum.watch.ru/' + soup.find_all('a', {'href': re.compile('attachmentid')})[0].get('href')
        except IndexError:
            try:
                offer.photo = soup.find_all('img', {'src': re.compile('\.jpg$')})[0].get('src')
            except:
                pass

            else:
                logger.debug('Photo was found')
        else:
            logger.debug('Photo was found')
        return offer


def main():
    watch = WatchScraper()
    urls_list = watch.get_offers_urls('http://forum.watch.ru/forumdisplay.php?f=192&order=desc')
    for url in urls_list:
        offer = watch.get_offer(url)
        print(offer.__dict__)

if __name__ == '__main__':
    main()