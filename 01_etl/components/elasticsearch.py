import logging

from components.utils import backoff
from elasticsearch import Elasticsearch, helpers
from settings import ELASTICSEARCH_DSL

log = logging.getLogger(__name__)


class ElasticSearch():
    def __init__(self) -> None:
        self.client = None

    @backoff()
    def connect(self) -> None:
        self.client = Elasticsearch(**ELASTICSEARCH_DSL)

    @backoff()
    def load_data(self, batch: list) -> None:
        data = [{'_index': 'movies', '_id': row.id, '_source': row.dict()}
                for row in batch]
        try:
            success, errors = helpers.bulk(self.client, data, stats_only=True)
            log.info(f'{success} rows successfully executed, '
                     f'{errors} rows with errors')
        except Exception as error:
            log.exception(error)
            self.connect()
            helpers.bulk(self.client, data, stats_only=True)
            log.info(f'{success} rows successfully executed, '
                     f'{errors} rows with errors')
