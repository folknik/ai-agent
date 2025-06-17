import psycopg2
from psycopg2 import extras
from contextlib import closing
from datetime import datetime
from typing import List, Tuple, Any

from settings.base import get_logger


logger = get_logger(__name__)


class PostgresDB:
    def __init__(self):
        self.conn_params = {
            'host': 'db',
            'port': '5432',
            'user': 'postgres',
            'password': 'postgres',
            'dbname': 'users'
        }

    def _execute_query(self, query: str) -> None:
        with closing(psycopg2.connect(**self.conn_params)) as pg_conn, closing(pg_conn.cursor()) as pg_cursor:
            pg_cursor.execute(query)
            pg_conn.commit()

    def _execute_batch(self, query: str, records: List[Tuple]) -> None:
        with closing(psycopg2.connect(**self.conn_params)) as pg_conn, closing(pg_conn.cursor()) as pg_cursor:
            extras.execute_batch(cur=pg_cursor, sql=query, argslist=records)
            pg_conn.commit()

    def _fetchall(self, query: str) -> List[Any]:
        with closing(psycopg2.connect(**self.conn_params)) as pg_conn, closing(pg_conn.cursor()) as pg_cursor:
            pg_cursor.execute(query)
            records = pg_cursor.fetchall()
            return records

    def insert_user_data(self, user_data: Tuple) -> None:
        logger.info(f"User data: {user_data}")
        query = """
            INSERT INTO users.user_requests (
                  user_id
                , chat_id
                , is_bot
                , first_name
                , last_name
                , username
                , is_premium
                , url
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);
        """
        self._execute_batch(
            query=query,
            records=[user_data]
        )
        logger.info(f"User_data with {user_data[0]} user_id successfully inserted into db.")

    def insert_chat_id(self, chat_id: int, user_id: int) -> None:
        query = """
            INSERT INTO users.chats 
                (chat_id, user_id) 
            SELECT {chat_id}, {user_id}
            WHERE
                NOT EXISTS (
                    SELECT id FROM users.chats WHERE chat_id = {chat_id}
                );
        """
        self._execute_query(
            query=query.format(chat_id=chat_id, user_id=user_id)
        )
        logger.info(f"Chat_id {chat_id} successfully inserted into db.")

    def get_all_chats(self) -> List[Tuple[int]]:
        query = "SELECT DISTINCT chat_id FROM users.chats;"
        return self._fetchall(query=query)

    def get_all_links_to_article(self) -> List[Tuple[str]]:
        query = "SELECT DISTINCT link FROM users.articles;"
        return self._fetchall(query=query)

    def insert_article(self, name: str, link: str, published_datetime: datetime) -> None:
        query = """
            INSERT INTO users.articles 
                (name, link, published_datetime) 
            SELECT '{name}', '{link}', '{published_datetime}'
            WHERE
                NOT EXISTS (
                    SELECT id FROM users.articles WHERE link = '{link}'
                );
        """
        self._execute_query(
            query=query.format(name=name, link=link, published_datetime=published_datetime)
        )
        logger.info(f"Article with {link} link successfully inserted into db.")


db = PostgresDB()
