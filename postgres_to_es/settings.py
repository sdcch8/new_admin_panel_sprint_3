from pydantic import BaseSettings, Field


class PostgresDSL(BaseSettings):
    dbname: str = Field('movies_database', env='DB_NAME')
    user: str = Field('app', env='DB_USER')
    password: str = Field('123qwe', env='DB_PASSWORD')
    host: str = Field('localhost', env='DB_HOST')
    port: int = Field(5432, env='DB_PORT')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


class ElasticDSL(BaseSettings):
    hosts: str = Field('http://localhost:9200', env='ELASTIC_SERVER')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


class Settings(BaseSettings):
    STARTUP_DELAY: int = 60
    UPDATE_INTERVAL: int = 60
    BATCH_SIZE: int = 500

    POSTGRES_DSL: PostgresDSL = PostgresDSL()
    ELASTIC_DSL: ElasticDSL = ElasticDSL()

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
