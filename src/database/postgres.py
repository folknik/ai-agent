import psycopg2
from contextlib import closing

from utils.base import get_logger


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

    def insert_user_data(self, user_data: dict) -> None:
        logger.info(f"User data: \n{user_data}")
        query = """
            INSERT INTO users.user_requests (
                  user_id
                , is_bot
                , first_name
                , last_name
                , username
                , is_premium
                , url
            ) VALUES (
                  {user_id}
                , {is_bot}
                , '{first_name}'
                , '{last_name}'
                , '{username}'
                , {is_premium}
                , '{url}'
            );
        """
        self._execute_query(
            query=query.format(**user_data)
        )
        logger.info("User_data successfully inserted into db.")
