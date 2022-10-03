from internal.storage.istorage import IDatabaseGateway, DatabaseSyncError

import psycopg2

from typing import List


class ConnectionError(DatabaseSyncError):
    def __str__(self) -> str:
        return 'Failed to connect to database: ' + super().__str__()

class InvalidQueryError(DatabaseSyncError):
    def __str__(self) -> str:
        return 'Invalid SQL query: ' + super().__str__()


class PostgresGateway(IDatabaseGateway):
    PARAMS = {
        'user': 'sunz',
        'password': 'imwzh2cw',
        'host': '127.0.0.1',
        'port': '5432',
        'database': 'trpo_coursework'
    }

    def __init__(self):
        self.connection = psycopg2.connect(**PostgresGateway.PARAMS)
        self.cursor = self.connection.cursor()

    def execute_query(self, sql: str, fetch_response: bool=True) -> List[tuple]:
        self.cursor.execute(sql)
        self.connection.commit()
        
        if fetch_response:
            try:
                response = self.cursor.fetchall()
            except psycopg2.ProgrammingError as e:
                raise InvalidQueryError(e)
            except psycopg2.Error as e:
                raise ConnectionError(e)
            return response


