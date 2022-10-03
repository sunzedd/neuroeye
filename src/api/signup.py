from flask.views import MethodView

from flask import request, make_response, redirect, url_for, render_template
from internal.user.iuser import UserAlreadyExistsError

from internal.user.user_table import UserTable

class SignUpEndpoint(MethodView):
    def get(self):
        return render_template('signup.html')

    def post(self):
        username = request.values.get('username')
        email = request.values.get('email')
        password = request.values.get('password')

        try:
            UserTable.create(username, email, password)
        except UserAlreadyExistsError as e:
            return 'Ползователь уже существует'
        
        return redirect(url_for('signin'))
