import logging
from datetime import datetime

from components.elasticsearch import ElasticSearch
from components.models import ESSchemaIndex
from components.postgres import Postgres
from components.postgres_queries import FIELDS, FILMWORK_QUERY
from components.utils import (JsonFileStorage, State, get_persons_by_role,
                              get_persons_ids_by_role)

log = logging.getLogger(__name__)


class ETL():
    def extract(self) -> list[dict]:
        log.info('Starting EXTRACT process')
        state = State(JsonFileStorage('state.json'))
        date_modified = (state.get_state('date_modified')
                         if state.get_state('date_modified')
                         else '1900-01-01')
        postgres = Postgres()
        postgres.connect()
        for field in FIELDS:
            for batch in postgres.execute_query(FILMWORK_QUERY,
                                                (field, date_modified)):
                yield batch
        state.set_state('date_modified',
                        datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        postgres.disconnect()
        log.info('EXTRACT process finished')

    def transform(self, batch: list[dict]) -> list[ESSchemaIndex]:
        log.info('Starting TRANSFORM process for batch')
        data = []

        for row in batch:
            es_row = ESSchemaIndex(
                id=row['id'],
                imdb_rating=row['rating'],
                genre=row['genres'],
                title=row['title'],
                description=row['description'],
                director=get_persons_by_role(row, 'director'),
                actors_names=get_persons_by_role(row, 'actor'),
                writers_names=get_persons_by_role(row, 'writer'),
                actors=get_persons_ids_by_role(row, 'actor'),
                writers=get_persons_ids_by_role(row, 'writer')
                )
            data.append(es_row)
        log.info('TRANSFORM process for batch is finished')
        return data

    def load(self, batch: list[ESSchemaIndex]) -> None:
        log.info('Starting LOAD process for batch')
        es = ElasticSearch()
        es.connect()
        es.load_data(batch)
        log.info('LOAD process for batch is finished')
