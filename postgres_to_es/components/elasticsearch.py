import logging

from elasticsearch import Elasticsearch, helpers

from components.elasticsearch_index import MOVIES_INDEX
from components.utils import backoff
from settings import Settings

log = logging.getLogger(__name__)


class ElasticSearch:
    @backoff()
    def __init__(self) -> None:
        self.client = Elasticsearch(**Settings().ELASTIC_DSL.dict())
        self.check_index()

    def check_index(self):
        if not self.client.indices.exists(index='movies'):
            self.client.indices.create(index='movies', body=MOVIES_INDEX)

    @backoff()
    def load_data(self, batch: list) -> None:
        data = [{'_index': 'movies', '_id': row.id, '_source': row.dict()}
                for row in batch]

        success, errors = helpers.bulk(self.client, data, stats_only=True)
        log.info(f'{success} rows successfully executed, '
                 f'{errors} rows with errors')
