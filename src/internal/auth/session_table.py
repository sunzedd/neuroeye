from internal.auth.iauth import IAuthService, AuthInvalidCredentialsError
from internal.auth.session import Session
from internal.sequrity.isequrity import ISecurityService
from internal.sequrity.sequrity import Security
from internal.user.user_table import UserTable

from typing import Dict

import datetime


class SessionTable(IAuthService):
    SESSION_LIFETIME_DAYS = 1
    SESSION_LIFETIME_HOURS = 0

    @staticmethod
    def signin(username: str, password: str) -> Dict:
        user = UserTable.find_by_username(username)
        if user is None:
            raise AuthInvalidCredentialsError(f'No user with username {username}') 
        if not UserTable.validate_password(user.get('id'), password):
            raise AuthInvalidCredentialsError(f'Given password {password} is invalid') 

        session = SessionTable.create(user.get('id'))
        return {
            'session_key': session.get('key'),
            'expires_date': session.get('expires_date')
        }


    @staticmethod
    def signout(session_key: str):
        session = Session.find_by_key(session_key)
        if session is None:
            return
        session.is_expired = True
        session.save()
        
    @staticmethod
    def get_authenticated_user_id(session_key: str) -> int:
        session = Session.find_by_key(session_key)
        if session is None:
            return None
        if session.expires_date <= datetime.datetime.utcnow():
            session.is_expired = True
            session.save()
            return None
        return session.user_id

    @staticmethod
    def create(user_id: int) -> Dict:
        session_expires_date = datetime.datetime.utcnow() + datetime.timedelta(
            days=SessionTable.SESSION_LIFETIME_DAYS,
            hours=SessionTable.SESSION_LIFETIME_HOURS
        )

        security: ISecurityService = Security()

        session = Session()
        session.user_id = user_id
        session.expires_date = session_expires_date
        session.key = security.generate_random_string(length=64)
        session.is_expired = False
        session.save()
        return session.__dict__()
