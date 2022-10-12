import os

from dotenv import load_dotenv

load_dotenv()

UPDATE_INTERVAL = 60
BATCH_SIZE = 500

POSTGRES_DSL = {
    'dbname': os.environ.get('POSTGRES_DB'),
    'user': os.environ.get('POSTGRES_USER'),
    'password': os.environ.get('POSTGRES_PASSWORD'),
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port': os.environ.get('DB_PORT', 5432),
}

ELASTICSEARCH_DSL = {
    'hosts': [
        f"http://{os.environ.get('ELASTIC_HOST', 'localhost')}:"
        f"{os.environ.get('ELASTIC_PORT', 9200)}"
    ],
    'basic_auth': (
        os.environ.get('ELASTIC_USER'),
        os.environ.get('ELASTIC_PASSWORD')
    )
}
