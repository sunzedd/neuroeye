from internal.showcase.showcase_table import ShowcaseTable
from internal.media.image_table import ImageTable
from api.utils import require_auth

from flask.views import MethodView
from flask import request, make_response, url_for, redirect


class StylingResultEndpoint(MethodView):
    @require_auth
    def post(self):
        title = request.values.get('showcase_title', None)
        description = request.values.get('showcase_description', None)
        should_publish = bool(request.values.get('publish', False))
        tags = request.values.get('showcase_tags', "")

        src_img_url = request.values['src_img_url']
        sample_img_url = request.values['sample_img_url']
        dst_img_url = request.values['dst_img_url']

        src_img_id = ImageTable.create(src_img_url)
        sample_img_id = ImageTable.create(sample_img_url)
        dst_img_id = ImageTable.create(dst_img_url)

        showcase = ShowcaseTable.create(
            request.user.get('id'),
            title,
            description,
            src_img_id.get('id'),
            sample_img_id.get('id'),
            dst_img_id.get('id'),
            should_publish,
            tags
        )

        return redirect(f"showcase/{showcase.get('id')}")
