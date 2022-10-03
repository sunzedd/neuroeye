from internal.showcase.showcase_table import ShowcaseTable
from internal.media.image_table import ImageTable
from internal.user.user_table import UserTable
from api.utils import get_current_user

from flask.views import MethodView
from flask import render_template, request, make_response, url_for, redirect

from http import HTTPStatus

from typing import Dict


def prepare_showcase_data(showcase: Dict, author: Dict, view_count: int) -> Dict:
    src_img_url = ImageTable.get_url(showcase.get('src_img_id'))
    sample_img_url = ImageTable.get_url(showcase.get('sample_img_id'))
    dst_img_url = ImageTable.get_url(showcase.get('dst_img_id'))
    author_userpic_url = ImageTable.get_url(author.get('userpic_id'))

    return { 
        'id': showcase.get('id'),
        'title': showcase.get('title'),
        'description': showcase.get('description'),
        'src_img_url': src_img_url,
        'sample_img_url': sample_img_url,
        'dst_img_url': dst_img_url,
        'author_id': author.get('id'),
        'author_name': author.get('username'),
        'author_userpic_url': author_userpic_url,
        'is_published': showcase.get('is_published'),
        'tags': showcase.get('tags'),
        'view_count': view_count
    }

class ShowcaseEndpoint(MethodView):
    def get(self, id):
        is_authorized, current_user = get_current_user(request.cookies)
        if not is_authorized:
            response = make_response(redirect(url_for('about')))
            response.delete_cookie('session_key')
            return response

        showcase = ShowcaseTable.find(id)
        if showcase is None:
            return render_template('404.html', title='404'), 404

        author = UserTable.find(showcase.get('author_id'))

        is_liked_by_user = False
        if showcase.get('author_id') != current_user.get('id'): 
            is_liked_by_user = ShowcaseTable.is_liked_by_user(showcase.get('id'), current_user.get('id'))

        ShowcaseTable.increase_view_count(id)
        view_count = ShowcaseTable.get_view_count(id)

        showcase_view = prepare_showcase_data(showcase, author, view_count)
        return render_template(
            'showcase.html',
            current_user=current_user,
            showcase=showcase_view,
            is_liked_by_user=is_liked_by_user
        )

    def post(self, id: int):
        is_authorized, current_user = get_current_user(request.cookies)
        if not is_authorized:
            response = make_response(redirect(url_for('about')))
            response.delete_cookie('session_key')
            return response

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
                ShowcaseTable.like(id, current_user.get('id'))
                return ''
            elif action == "unlike":
                ShowcaseTable.unlike(id, current_user.get('id'))
                return ''
            else:
                return 'Error'

    def delete(self, id):
        is_authorized, current_user = get_current_user(request.cookies)
        if not is_authorized:
            response = make_response(redirect(url_for('about')))
            response.delete_cookie('session_key')
            return response

        showcase = ShowcaseTable.find(id)
        if showcase.get('author_id') == current_user.get('id'):
            ShowcaseTable.delete(id)
            return make_response(redirect(url_for('home')))
        else:
            response = make_response()
            response.status = HTTPStatus.NOT_ACCEPTABLE
            return response
