from internal.user.user_table import UserTable
from internal.media.image_table import ImageTable
from api.utils import require_auth

from flask.views import MethodView
from flask import request, render_template, make_response, redirect, url_for


class UserpageEndpoint(MethodView):
    @require_auth
    def get(self):
        return render_template('userpage.html', current_user=request.user)

    @require_auth
    def post(self):
        password = request.values.get('password', None)
        repeated_password = request.values.get('repeated_password', None)
        new_userpic = request.files.get('input_userpic', None)

        if password is not None and repeated_password is not None:
            if len(password) > 0 and len(repeated_password) > 0:
                if password == repeated_password:
                    UserTable.update_password(request.user.get('id'), password)

        if new_userpic is not None:
            new_userpic = ImageTable.create_from_file(new_userpic)
            UserTable.update_userpic(request.user.get('id'), new_userpic.get('id'))
                
        return redirect(url_for('userpage'))
