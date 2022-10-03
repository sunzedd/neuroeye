from internal.auth.session_table import SessionTable

from flask.views import MethodView
from flask import request, redirect, make_response, url_for


class SignOutEndpoint(MethodView):
    def get(self):
        session_key = request.cookies.get('session_key')
        if session_key:
            SessionTable.signout(session_key)

        response = make_response(redirect(url_for('about')))
        response.delete_cookie('session_key')
        return response
