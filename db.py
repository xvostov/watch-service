from typing import List, Tuple
from settings import db_host, db_port, db_user, db_password, db_name, categories_table
from loguru import logger
import pymysql


class DataBaseHandler:
    def __init__(self):
        logger.debug('Сonnecting to a remote database')
        self.mysql_connection = pymysql.connect(host=db_host,
                                                port=db_port,
                                                user=db_user,
                                                password=db_password,
                                                database=db_name,
                                                charset='utf8mb4')
        self.mysql_cursor = self.mysql_connection.cursor()
        self.mysql_connection.autocommit(True)

        # Проверка и создание отсутствующих таблицы
        logger.debug('Checking the om "watch_viewed_ids" table')
        self.mysql_cursor.execute("""
        CREATE TABLE IF NOT EXISTS watch_viewed_links (
        url	VARCHAR(200) NOT NULL UNIQUE)""")

        logger.debug(f'Checking the om {categories_table} table')
        self.mysql_cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {categories_table} (
        url	VARCHAR(255) NOT NULL UNIQUE)""")

    def get_viewed_ids(self) -> List:
        logger.debug('Getting viewed links')
        while True:
            try:
                self.mysql_cursor.execute("SELECT url FROM watch_viewed_ids")
                resp = self.mysql_cursor.fetchall()
            except pymysql.err.OperationalError:
                self.mysql_connection.ping(True)

            else:
                break
        logger.debug('Viewed ids received')
        return [d[0] for d in resp]

    def add_to_viewed_id(self, post_id: str):
        logger.debug(f'Adding to viewed links - {post_id}')
        while True:
            try:
                self.mysql_cursor.execute("INSERT INTO watch_viewed_ids VALUES(%s)", (post_id,))
                self.mysql_connection.commit()
            except pymysql.err.OperationalError:
                self.mysql_connection.ping(True)

            except pymysql.err.IntegrityError:
                break
            else:
                break
        logger.debug('The id has been added to viewed links')

    def get_categories(self) -> List:
        self.mysql_connection.ping(True)

        logger.debug('Getting categories')
        self.mysql_cursor.execute(f"SELECT url FROM {categories_table}")
        resp = self.mysql_cursor.fetchall()
        logger.debug('Categories received')
        return [d for d in resp]


if __name__ == '__main__':
    db = DataBaseHandler()
    print(db.get_categories())
