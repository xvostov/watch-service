import sys

from offer import Offer
from requester import Requester
from bs4 import BeautifulSoup
from utils import stopwatch
from loguru import logger
from loader import db_handler
import re
import telegram

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

        # viewed_links = db_handler.get_viewed_links()

        # for url in viewed_links:
        #     if url in urls_list:
        #         urls_list.remove(url)

        logger.debug(f'New urls found: {len(urls_list)}')
        return urls_list

    @stopwatch
    def get_offers(self, url: str):
        logger.debug(f'Parsing offer - {url}')
        content = self.req.get(url)
        soup = BeautifulSoup(content, 'lxml')

        viewed_ids = db_handler.get_viewed_links()

        # offer = Offer(url)
        page_title = soup.find('title').text.replace(' - Часовой форум Watch.ru', '')
        all_posts = soup.find_all('td', {'id': re.compile(r'^td_post_')})

        try:
            photo = 'http://forum.watch.ru/' + soup.find_all('a', {'href': re.compile('attachmentid')})[0].get(
                'href')
        except IndexError:
            try:
                photo = soup.find_all('img', {'src': re.compile('\.jpg$')})[0].get('src')
            except Exception:
                photo = None

            else:
                logger.debug('Photo was found')
        else:
            logger.debug('Photo was found')

        if photo:
            if 'http' not in photo:
                photo = 'http://forum.watch.ru/' + photo

        for post in all_posts:
            post_id = post.get('id').replace('td_post_', '')
            if post_id not in viewed_ids:
                offer = Offer(url)

                # Поиск цены
                try:
                    offer.price = re.search(r'цена:\s[a-z0-9\s\.\$]*', post.text.lower()).group(0).strip()
                except AttributeError:
                    logger.debug('Price was not found')

                else:
                    logger.debug(f'Price was found: {offer.price}')

                # Описание
                offer.description = post.text.replace('\n\n', '\n')
                if len(offer.description) > 650:
                    offer.description = offer.description[:650]

                if photo:
                    offer.photo = photo

                try:
                    telegram.send_offer(offer)
                except Exception:
                    pass
                else:
                    db_handler.add_to_viewed_id(post_id)

def main():
    watch = WatchScraper()
    urls_list = watch.get_offers_urls('http://forum.watch.ru/forumdisplay.php?f=192&order=desc')
    for url in urls_list:
        offer = watch.get_offers(url)
        print(offer.__dict__)

if __name__ == '__main__':
    main()