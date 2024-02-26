from internal.auth.session_table import SessionTable
from internal.user.user_table import UserTable
from internal.media.image_table import ImageTable

from flask import (
    request as flask_request,
    url_for,
    redirect,
    make_response
)

from functools import wraps


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

def require_auth(endpoint_f):
    @wraps(endpoint_f)
    def decorated(*args, **kwargs):
        is_signedin, current_user = get_current_user(flask_request.cookies)
        if not is_signedin:
            response = make_response(redirect(url_for('signin')))
            response.delete_cookie('session_key')
            return response
        flask_request.user = current_user
        return endpoint_f(*args, **kwargs)
    return decorated
