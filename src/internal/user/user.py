from internal.shared.entity import Entity
from internal.user.user_query_builder import UserQueryBuilder
from internal.sequrity.sequrity import ISecurityService, Security

from typing import List


class User(Entity):
    id: int
    email: str
    username: str
    password: str
    userpic_id: str

    def __init__(self, db_response=None):
        super().__init__()
        if db_response is None:
            self.id = None
            self.email = None
            self.username = None
            self.password = None
            self.userpic_id = None
        else:
            self.id = int(db_response[0])
            self.email = db_response[1]
            self.username = db_response[2]
            self.password = db_response[3]
            self.userpic_id = db_response[4]

    def reset_password(self, new_password):
        security: ISecurityService = Security()
        hashed = security.hash_string(new_password)
        self.password = hashed

    def validate_password(self, given_password) -> bool:
        security: ISecurityService = Security()
        hashed = security.hash_string(given_password)
        return self.password == hashed

    def save(self):
        if self.id is None:
            self.reset_password(self.password)
            query = UserQueryBuilder().insert(
                self.username,
                self.email,
                self.password)
            response = self.database.execute_query(query)
            self.id = int(response[0][0])
        else:
            self.reset_password(self.password)
            query = UserQueryBuilder().update(
                self.id,
                self.username,
                self.email,
                self.password,
                self.userpic_id)
            response = self.database.execute_query(query, fetch_response=False)

    def delete(self):
        if self.id is None:
            return
        query = UserQueryBuilder().delete(self.id)
        self.database.execute_query(query, fetch_response=False)

    @staticmethod
    def find(id) -> 'User':
        query = UserQueryBuilder().select(id)
        dbresponse = User.get_storage_gateway().execute_query(query)        
        return User(dbresponse[0]) if len(dbresponse) > 0 else None

    @staticmethod
    def find_by_username(username) -> 'User':
        query = UserQueryBuilder().select_by_username(username)
        dbresponse = User.get_storage_gateway().execute_query(query)
        return User(dbresponse[0]) if len(dbresponse) > 0 else None

    @staticmethod
    def find_by_email(email) -> 'User':
        query = UserQueryBuilder().select_by_email(email)
        dbresponse = User.get_storage_gateway().execute_query(query)
        return User(dbresponse[0]) if len(dbresponse) > 0 else None


    def __dict__(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'userpic_id': self.userpic_id
        }
