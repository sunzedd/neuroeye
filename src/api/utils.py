from typing import Dict
from internal.auth.session_table import SessionTable
from internal.user.user_table import UserTable
from internal.media.image_table import ImageTable

from typing import Dict


def get_current_user(cookies):
    session_key = cookies.get('session_key', None)
    if not session_key:
        return (False, {})
    user_id = SessionTable.get_authenticated_user_id(session_key)
    if user_id:
        user = UserTable.find(user_id)
        userpic_url = ImageTable.get_url(user.get('userpic_id'))
        user['userpic_url'] = userpic_url
        return (True, user)
    return (False, {})
