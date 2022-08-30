from offer import Offer
from settings import telegram_api_address, bot_api_token
from loguru import logger
import requests

class SendingOfferError:
    pass

def send_offer(offer: Offer):
    resp = requests.post(f'http://{telegram_api_address}/offer', json={
        'token': bot_api_token,
        'url': offer.url,
        'title': offer.title,
        'description': offer.description,
        'price': offer.price,
        'img_url': offer.photo,
        'id': ''
    }, timeout=1)

    if resp.status_code != 200:
        logger.error('Error of sending offer')
        raise SendingOfferError