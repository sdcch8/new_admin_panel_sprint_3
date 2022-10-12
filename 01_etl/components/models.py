from pydantic import BaseModel, Field


class ESPerson(BaseModel):
    id: str = Field(alias="person_id")
    name: str = Field(alias="person_name")


class ESSchemaIndex(BaseModel):
    id: str
    imdb_rating: float | None
    genre: list[str]
    title: str
    description: str | None
    director: list[str]
    actors_names: list[str]
    writers_names: list[str]
    actors: list[ESPerson]
    writers: list[ESPerson]
