import logging

import psycopg2
from components.utils import backoff
from psycopg2.extras import DictCursor
from settings import Settings

log = logging.getLogger(__name__)


class Postgres:
    @backoff()
    def __init__(self) -> None:
        self.connection = psycopg2.connect(**Settings().POSTGRES_DSL.dict(),
                                           cursor_factory=DictCursor)
        self.cursor = self.connection.cursor()
        log.info('Postgres DB connected')

    @backoff()
    def execute_query(self, sql_query: str,
                      params: tuple = None) -> list[dict]:
        if params:
            sql_query = self.cursor.mogrify(sql_query, params)

        self.cursor.execute(sql_query)
        while batch := self.cursor.fetchmany(Settings().BATCH_SIZE):
            yield batch

