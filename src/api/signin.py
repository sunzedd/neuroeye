from internal.auth.session_table import SessionTable, AuthInvalidCredentialsError

from flask.views import MethodView
from flask import render_template
from flask import request, make_response, redirect, url_for


class SignInEndpoint(MethodView):
    def get(self):
        return render_template('signin.html')

    def post(self):
        username = request.values.get('username')
        password = request.values.get('password')

        try:
            session = SessionTable.signin(username, password)
        except AuthInvalidCredentialsError:
            return render_template('signin.html', error='Пользователя с такими данными не существует')

        response = make_response(redirect(url_for('home')))
        response.set_cookie('session_key', session.get('session_key'), expires=session.get('expires_date'))
        return response
