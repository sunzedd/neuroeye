from internal.user.user import User
from internal.user.iuser import IUserService, UserAlreadyExistsError, UserDoesNotExistsError

from typing import Dict


class UserTable(IUserService):
    @staticmethod
    def create(username: str, email: str, password: str) -> Dict:
        if User.find_by_username(username) is not None:
            raise UserAlreadyExistsError()
        if User.find_by_email(email) is not None:
            raise UserAlreadyExistsError()

        user = User()
        user.username = username
        user.email = email
        user.reset_password(password)
        user.save()

        return { 'id': user.id }

    @staticmethod
    def find(id: int) -> Dict:
        user = User.find(id)
        return user.__dict__() if user is not None else None
    
    @staticmethod
    def find_by_username(username: str) -> Dict:
        user = User.find_by_username(username)
        return user.__dict__() if user is not None else None

    @staticmethod
    def update_password(id: int, new_password: str):
        user = User.find(id)
        if user is None:
            raise UserDoesNotExistsError()
        user.reset_password(new_password)
        user.save()

    @staticmethod
    def update_userpic(id: int, new_userpic_id: int) -> Dict:
        user = User.find(id)
        if user is None:
            raise UserDoesNotExistsError()
        user.userpic_id = new_userpic_id
        user.save()

    @staticmethod
    def validate_password(id: int, given_password: int) -> bool:
        user = User.find(id)
        if user is None:
            raise UserDoesNotExistsError()
        return user.validate_password(given_password)
