import abc
import json
import logging
from functools import wraps
from time import sleep
from typing import Any

log = logging.getLogger(__name__)


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10) -> None:
    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            sleep_time = start_sleep_time
            n = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as error:
                    if sleep_time < border_sleep_time:
                        sleep_time = min(start_sleep_time * (factor ** n),
                                         border_sleep_time)
                    else:
                        sleep_time = border_sleep_time
                    n += 1
                    log.exception(error)
                    sleep(sleep_time)
        return inner
    return func_wrapper


class BaseStorage:
    @abc.abstractmethod
    def save_state(self, state: dict) -> None:
        """Сохранить состояние в постоянное хранилище"""
        pass

    @abc.abstractmethod
    def retrieve_state(self) -> dict:
        """Загрузить состояние локально из постоянного хранилища"""
        pass


class JsonFileStorage(BaseStorage):
    def __init__(self, file_path: str | None = None):
        self.file_path = file_path

    def save_state(self, state: dict) -> None:
        try:
            with open(self.file_path, "w") as f:
                f.write(json.dumps(state))
        except Exception as error:
            log.exception(error)

    def retrieve_state(self) -> dict:
        try:
            with open(self.file_path, "r") as f:
                return json.loads(f.read())
        except FileNotFoundError:
            return {}


class State:
    def __init__(self, storage: JsonFileStorage):
        self.storage = storage
        self.state = {}

    def set_state(self, key: str, value: Any) -> None:
        self.state[key] = value
        self.storage.save_state(self.state)

    def get_state(self, key: str) -> Any:
        self.state = self.storage.retrieve_state()
        return self.state.get(key)


def get_persons_by_role(row: dict, role: str) -> list:
    return [person['person_name'] for person
            in row['persons']
            if person['person_role'] == role]


def get_persons_ids_by_role(row: dict, role: str) -> list[dict]:
    return [person for person in row['persons']
            if person['person_role'] == role]
