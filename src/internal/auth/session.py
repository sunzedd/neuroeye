from internal.entity.entity import Entity
from internal.auth.session_query_builder import SessionQueryBuilder

from typing import List

import datetime


class Session(Entity):
    id: int
    user_id: int
    key: str
    expires_date: datetime.datetime
    is_expired: bool

    def __init__(self, dbresponse=None):
        super().__init__()
        if dbresponse is None:
            self.id = None
            self.user_id = None
            self.key = None
            self.expires_date = None
            self.is_expired = None
        else:
            self.id = dbresponse[0]
            self.user_id = dbresponse[1]
            self.expires_date = dbresponse[2]
            self.key = dbresponse[3]
            self.is_expired = bool(dbresponse[4])

    def save(self):
        if self.id is None:
            query = SessionQueryBuilder().insert(self.user_id, self.expires_date, self.key, self.is_expired)
            dbresponse = self.database.execute_query(query)
            self.id = int(dbresponse[0][0])
        else:
            query = SessionQueryBuilder().update(self.id, self.user_id, self.expires_date, self.key, self.is_expired)
            dbresponse = self.database.execute_query(query, fetch_response=False)
        
    def delete(self):
        if self.id is None:
            return
        query = SessionQueryBuilder().delete(self.id)
        self.database.execute_query(query)


    @staticmethod
    def find_by_key(key: str) -> 'Session':
        query = SessionQueryBuilder().select_all_by_key(key)
        dbresponse = Session.get_storage_gateway().execute_query(query)
        return Session(dbresponse[0]) if len(dbresponse) > 0 else None

    @staticmethod
    def find_last_valid(user_id: int) -> 'Session':
        query = SessionQueryBuilder().select_all_by_user_id__nonexpired(user_id)
        dbresponse = Session.get_storage_gateway().execute_query(query)
        return Session(dbresponse[0]) if len(dbresponse) > 0 else None

    @staticmethod
    def find_nonexpired(user_id: int) -> List['Session']:
        query = SessionQueryBuilder().select_all_by_user_id__nonexpired(user_id)
        dbresponse = Session.get_storage_gateway().execute_query(query)
        sessions = [Session(row) for row in dbresponse]
        return sessions


    def __dict__(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'expires_date': self.expires_date,
            'key': self.key,
            'is_expired': self.is_expired
        }
