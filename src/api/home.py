from internal.showcase.showcase_table import ShowcaseTable
from internal.media.image_table import ImageTable
from internal.user.user_table import UserTable
from api.utils import require_auth

from flask.views import MethodView
from flask import request, render_template, make_response, redirect, url_for

from typing import List, Dict


def prepare_showcase_views(showcases: List[Dict]) -> List[Dict]:
    views = []
    for s in showcases:
        src_img_url = ImageTable.get_url(s.get('src_img_id'))
        sample_img_url = ImageTable.get_url(s.get('sample_img_id'))
        dst_img_url = ImageTable.get_url(s.get('dst_img_id'))
        author = UserTable.find(s.get('author_id'))
        author_userpic_url = ImageTable.get_url(author.get('userpic_id'))
        
        views.append({
            'id': s.get('id'),
            'title': s.get('title'),
            'src_img_url' : src_img_url,
            'sample_img_url' : sample_img_url,
            'dst_img_url' : dst_img_url,
            'author_id': author.get('id'),
            'author_name': author.get('username'),
            'author_userpic_url': author_userpic_url,
            'tags': s.get('tags'),
        })
    return views


class HomeEndpoint(MethodView):
    @require_auth
    def get(self):
        # query parameters
        is_liked_requested = request.args.get('liked', False)
        is_owned_requested = request.args.get('owned', False)

        showcases = []
        active_tab = None

        if is_liked_requested:
            showcases = ShowcaseTable.find_liked_by_user(request.user.get('id'))
            active_tab = 'liked'
        elif is_owned_requested:
            showcases = ShowcaseTable.find_owned_by_user(request.user.get('id'))
            active_tab = 'owned'
        else:
            showcases = ShowcaseTable.find_last_published()
            active_tab = 'last'
        showcase_views = prepare_showcase_views(showcases)

        return render_template(
            'home.html',
            active_tab=active_tab,
            current_user=request.user, 
            showcases=showcase_views
        )
