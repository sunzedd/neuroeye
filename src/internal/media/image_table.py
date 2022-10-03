from internal.media.imedia import IMediaService
from internal.media.image import Image
from internal.media.image import ImageQueryBuilder
from internal.media.image_loader import ImageLoader

from typing import Dict, Any


class ImageTable(IMediaService):
    @staticmethod
    def create(url: str) -> Dict:
        image = Image()
        image.url = url
        image.save()
        return image.__dict__()

    @staticmethod
    def create_from_file(image: Any) -> Dict:
        loader = ImageLoader()
        rel_filepath = loader.upload_image(image)
        
        image = Image()
        image.url = rel_filepath
        image.save()
        return image.__dict__()

    @staticmethod
    def find_image(id: int) -> Dict:
        image = Image.find(id)
        return image.__dict__() if image is not None else None

    @staticmethod
    def delete_image(id: int):
        image = Image.find(id)
        if image is None:
            return
        image.delete()

    @staticmethod
    def get_url(id: int):
        image = Image.find(id)
        return image.url if image is not None else None
