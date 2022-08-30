import os
from loguru import logger

# logger preset
logger.add('debug.log', format="{time} {level} {message}", level="DEBUG")

# Telegram
bot_api_token = os.getenv('bot_api_token')
telegram_api_address = os.getenv('telegram_api_address')

# DataBase
db_user = os.getenv('db_user')
db_password = os.getenv('db_password')
db_host = os.getenv('db_host')
db_port = int(os.getenv('db_port'))
db_name = os.getenv('db_name')
categories_table = os.getenv('categories_table').strip()
