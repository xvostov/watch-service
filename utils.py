import requests
from loguru import logger

import time


def stopwatch(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        logger.info(f'Функция {func.__name__} отработала за {int(time.time() - start_time)} секунд')
        return result

    return wrapper