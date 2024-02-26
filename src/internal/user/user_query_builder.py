from internal.storage.postgres.sql_util import SQL


class UserQueryBuilder:
    def __init__(self):
        self.TABLE_NAME = 'trpo_user'
        self.COLUMN = {
            'id': 'id',
            'email': 'email',
            'username': 'username',
            'password': 'password_hash',
            'userpic_id': 'userpic_id'
        }

    def select(self, id: int) -> str:
        return ('SELECT ' + SQL.from_list([self.COLUMN['id'], 
                                           self.COLUMN['email'], 
                                           self.COLUMN['username'], 
                                           self.COLUMN['password'],
                                           self.COLUMN['userpic_id']]) +
                ' FROM ' + self.TABLE_NAME + 
                ' WHERE ' + self.COLUMN['id'] + '={}')\
                    .format(SQL.from_any(id))
    
    def insert(self, username: str, email: str, password: str) -> str:
        return ('INSERT INTO ' + self.TABLE_NAME + ' (' + SQL.from_list([self.COLUMN['email'],
                                                                        self.COLUMN['username'],
                                                                        self.COLUMN['password']]) + ')' +
                ' VALUES ({}, {}, {})' +
                ' RETURNING ' + str(self.COLUMN['id']))\
                    .format(
                        SQL.from_any(email),
                        SQL.from_any(username),
                        SQL.from_any(password))

    def update(self, id: int, username: str, email: str, password: str, userpic_id: int) -> str:
        return ('UPDATE ' + self.TABLE_NAME + ' ' +
                'SET ' + self.COLUMN['email'] + '={}, ' +
                         self.COLUMN['username'] + '={}, ' +
                         self.COLUMN['password'] + '={}, ' +
                         self.COLUMN['userpic_id'] + '={} ' +
                'WHERE ' + self.COLUMN['id'] + '={}')\
                    .format(
                        SQL.from_any(email),
                        SQL.from_any(username),
                        SQL.from_any(password),
                        SQL.from_any(userpic_id),
                        SQL.from_any(id),
                    )
    
    def delete(self, id: int) -> str:
        return ('DELETE FROM ' + self.TABLE_NAME + ' WHERE ' + self.COLUMN['id'] + '={}')\
                    .format(SQL.from_any(id))

    def select_by_username(self, username: str) -> str:
        return ('SELECT ' + SQL.from_list([self.COLUMN['id'], 
                                           self.COLUMN['email'], 
                                           self.COLUMN['username'], 
                                           self.COLUMN['password'],
                                           self.COLUMN['userpic_id']]) +
                ' FROM ' + self.TABLE_NAME + 
                ' WHERE ' + self.COLUMN['username'] + '={}')\
                    .format(SQL.from_any(username))

    def select_by_email(self, email: str) -> str:
        return ('SELECT ' + SQL.from_list([self.COLUMN['id'], 
                                           self.COLUMN['email'], 
                                           self.COLUMN['username'], 
                                           self.COLUMN['password'],
                                           self.COLUMN['userpic_id']]) +
                ' FROM ' + self.TABLE_NAME + 
                ' WHERE ' + self.COLUMN['email'] + '={}')\
                    .format(SQL.from_any(email))
