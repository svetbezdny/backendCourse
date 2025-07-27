from abc import ABC

from src.utils.db_manager import DBManager


class BaseService(ABC): ...


class BaseDbService(BaseService):
    def __init__(self, db: DBManager) -> None:
        self.db = db
