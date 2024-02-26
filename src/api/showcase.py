from internal.showcase.showcase_table import ShowcaseTable
from internal.showcase.usecase.get_showcase_usecase import GetShowcaseUsecase
from api.utils import require_auth

from flask.views import MethodView
from flask import render_template, request, make_response, url_for, redirect

from http import HTTPStatus



class ShowcaseEndpoint(MethodView):
    @require_auth
    def get(self, id):
        usecase = GetShowcaseUsecase(id, request.user['id'])
        result = usecase.execute()

        response = None
        if not result.is_successfull():
            if result.error_code == 404:
                return render_template('404.html', title='404'), 404
            else:
                response = redirect('home', error=result.error_message)
        else:
            response = render_template(
                'showcase.html', 
                current_user=request.user,
                showcase=result.successfull_result)
        return response

    @require_auth
    def post(self, id: int):
        body = request.get_json(force=True)
        if "action" in body:
            action = body["action"]
            if action == "publish":
                ShowcaseTable.publish(id)
                return ''
            elif action == "unpublish":
                ShowcaseTable.unpublish(id)
                return ''
            elif action == "like":
                ShowcaseTable.like(id, request.user.get('id'))
                return ''
            elif action == "unlike":
                ShowcaseTable.unlike(id, request.user.get('id'))
                return ''
            else:
                return 'Error'

    @require_auth
    def delete(self, id):
        showcase = ShowcaseTable.find(id)
        if showcase.get('author_id') == request.user.get('id'):
            ShowcaseTable.delete(id)
            return make_response(redirect(url_for('home')))
        else:
            response = make_response()
            response.status = HTTPStatus.NOT_ACCEPTABLE
            return response
