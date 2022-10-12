import logging

import psycopg2
from components.utils import backoff
from psycopg2.extras import DictCursor
from settings import BATCH_SIZE, POSTGRES_DSL

log = logging.getLogger(__name__)


class Postgres():
    def __init__(self) -> None:
        self.connection = None
        self.cursor = None

    @backoff()
    def connect(self) -> None:
        self.connection = psycopg2.connect(**POSTGRES_DSL,
                                           cursor_factory=DictCursor)
        self.cursor = self.connection.cursor()
        log.info('Postgres DB connected')

    def disconnect(self) -> None:
        self.connection.close()
        log.info('Postgres DB disconnected')

    @backoff()
    def execute_query(self, sql_query: str, params: tuple = None) -> list[dict]:
        if params:
            sql_query = self.cursor.mogrify(sql_query, params)
        try:
            self.cursor.execute(sql_query)
            while batch := self.cursor.fetchmany(BATCH_SIZE):
                yield batch
        except Exception as error:
            log.exception(error)
            self.connect()
            self.cursor.execute(sql_query)
            while batch := self.cursor.fetchmany(BATCH_SIZE):
                yield batch
