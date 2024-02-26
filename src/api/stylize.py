from internal.media.image_loader import ImageLoader
from internal.styling.styling_service import IStylingService, StylingService
from api.utils import require_auth

from flask.views import MethodView
from flask import render_template, request, make_response, url_for, redirect


class StylizeEndpoint(MethodView):
    @require_auth
    def get(self):
        return render_template('stylize.html', current_user=request.user)

    @require_auth
    def post(self):
        source_image = request.files['input_src_img']
        sample_image = request.files['input_sample_img']

        loader = ImageLoader()
        source_image_url = loader.upload_image(source_image)
        sample_image_url = loader.upload_image(sample_image)
        
        styling_service: IStylingService = StylingService()
        styling_response = styling_service.stylize(
            ImageLoader.get_absolute_filepath(source_image_url),
            ImageLoader.get_absolute_filepath(sample_image_url))

        return render_template('styling_result.html', 
            current_user=request.user,
            result={
                'src_img_url': source_image_url,
                'sample_img_url': sample_image_url,
                'dst_img_url': styling_response['dst_img_url']
            })

    @require_auth
    def delete(self):
        raise NotImplementedError()
