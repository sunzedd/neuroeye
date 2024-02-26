from internal.storage.postgres.sql_util import SQL

import datetime


class SessionQueryBuilder:
    def __init__(self):
        self.TABLE_NAME = "trpo_session"
        self.COLUMN = {
            "id": "id",
            "user_id": "user_id",
            "expires_date": "expires_date",
            "key": "key",
            "is_expired": "is_expired"
        }

    def select_all_by_user_id(self, user_id: int) -> str:
        return ('SELECT * FROM ' + self.TABLE_NAME +
                ' WHERE ' + self.COLUMN['user_id'] + "={}")\
                    .format(SQL.from_any(user_id))

    def select_all_by_key(self, key: str) -> str:
        return ('SELECT * FROM ' + self.TABLE_NAME +
                ' WHERE ' + self.COLUMN['key'] + '={}')\
                    .format(SQL.from_any(key))

    def select_all_by_user_id__nonexpired(self, user_id: int) -> str:
        return ('SELECT * FROM ' + self.TABLE_NAME +
                ' WHERE ' + self.COLUMN['user_id'] + "={}" +
                ' AND ' + self.COLUMN["is_expired"] + "=0")\
                    .format(SQL.from_any(user_id))

    def insert(self, user_id: int, expires_date: datetime.datetime, key: str, is_expired: bool) -> str:
        return ('INSERT INTO ' + self.TABLE_NAME + ' (' + SQL.from_list([self.COLUMN['user_id'],
                                                                        self.COLUMN['expires_date'],
                                                                        self.COLUMN['key'],
                                                                        self.COLUMN['is_expired']]) + ')' + 
                   ' VALUES ({}, {}, {}, {}) RETURNING ' + self.COLUMN['id'])\
                    .format(
                        SQL.from_any(user_id),
                        SQL.from_any(expires_date),
                        SQL.from_any(key),
                        SQL.from_any(int(is_expired)))

    def update(self, id: int, user_id: int, expires_date: datetime.datetime, key: str, is_expired: bool) -> str:
        return ('UPDATE ' + self.TABLE_NAME + ' ' +
                   'SET ' + self.COLUMN['user_id'] + '={}, ' +
                            self.COLUMN['expires_date'] + '={}, ' +
                            self.COLUMN['key'] + '={}, ' +
                            self.COLUMN['is_expired'] + '={} ' +
                   'WHERE ' + self.COLUMN['id'] + '={}')\
                    .format(
                        SQL.from_any(user_id),
                        SQL.from_any(expires_date),
                        SQL.from_any(key),
                        SQL.from_any(int(is_expired)),
                        SQL.from_any(id))

    def delete(self, id: int) -> str:
        return ('DELETE FROM ' + self.TABLE_NAME + ' WHERE id={}').format(SQL.from_any(id))
