from internal.storage.istorage import IDatabaseGateway
from internal.storage.postgres.postgres_gateway import PostgresGateway

from abc import ABC


class Entity(ABC):
    database: IDatabaseGateway

    def __init__(self):
        self.database = Entity.get_storage_gateway()

    @staticmethod
    def get_storage_gateway():
        return PostgresGateway()
