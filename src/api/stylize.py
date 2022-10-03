from internal.showcase.showcase_table import ShowcaseTable
from internal.media.image_table import ImageTable
from internal.media.image_loader import ImageLoader
from internal.user.user_table import UserTable
from internal.styling.styling_service import IStylingService, StylingService
from api.utils import get_current_user

from flask.views import MethodView
from flask import render_template, request, make_response, url_for, redirect


class StylizeEndpoint(MethodView):
    def get(self):
        is_authorized, current_user = get_current_user(request.cookies)
        if not is_authorized:
            response = make_response(redirect(url_for('about')))
            response.delete_cookie('session_key')
            return response

        return render_template('stylize.html', current_user=current_user)

    def post(self):
        is_authorized, current_user = get_current_user(request.cookies)
        if not is_authorized:
            response = make_response(redirect(url_for('about')))
            response.delete_cookie('session_key')
            return response
        
        source_image = request.files['input_src_img']
        sample_image = request.files['input_sample_img']

        loader = ImageLoader()
        source_image_url = loader.upload_image(source_image)
        sample_image_url = loader.upload_image(sample_image)
        
        styling_service: IStylingService = StylingService()
        styling_response = styling_service.stylize(
            ImageLoader.get_absolute_filepath(source_image_url),
            ImageLoader.get_absolute_filepath(sample_image_url))

        return render_template(
            'styling_result.html', 
            current_user=current_user,
            result={
                'src_img_url': source_image_url,
                'sample_img_url': sample_image_url,
                'dst_img_url': styling_response['dst_img_url']
            }
        )


    def delete(self):
        is_authorized, current_user = get_current_user(request.cookies)
        if not is_authorized:
            response = make_response(redirect(url_for('about')))
            response.delete_cookie('session_key')
            return response
