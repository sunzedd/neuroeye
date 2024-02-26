from site import abs_paths
from internal.sequrity.isequrity import ISecurityService
from internal.sequrity.sequrity import Security

from typing import Any
import os


class ImageLoader:
    ABS_UPLOAD_PATH = '/home/sunz/uni/neuroeye/static/uploads/'
    REL_UPLOAD_PATH = 'uploads/'

    security: ISecurityService

    def __init__(self):
        self.security = Security()

    def upload_image(self, image: Any) -> str:
        '''
            Returns relative filepath of uploaded image.
        '''
        relative_path = self.generate_filepath_for_image()
        abs_path = self.get_absolute_filepath(relative_path)
        image.save(abs_path)
        return relative_path

        # with open(abs_path, 'w') as file:
            # for chunk in image.chunks():
                # file.write(chunk)
        # return relative_path

    def generate_filepath_for_image(self) -> str:
        '''
            Returns relative filepath.
        '''
        filename = self.security.generate_random_string()
        return self.REL_UPLOAD_PATH + filename

    def delete_image(self, relative_filepath: str):
        abs_filepath = ImageLoader.get_absolute_filepath(relative_filepath)
        os.remove(abs_filepath)

    @staticmethod
    def get_absolute_filepath(relative: str) -> str:
        cleaned = relative.split('/')[1]
        return ImageLoader.ABS_UPLOAD_PATH + cleaned
