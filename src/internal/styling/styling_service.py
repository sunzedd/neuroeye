from internal.styling.istyling import IStylingService
from internal.media.image_loader import ImageLoader

import tensorflow_hub as hub
import tensorflow as tf
import numpy as np
import cv2

from typing import Dict


class StylingService(IStylingService):
    _MODEL_URL = 'https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2'
    _model: object

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(StylingService, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self._model = hub.load(self._MODEL_URL)

    def stylize(self, src_img_filepath: str, sample_img_filepath: str) -> Dict:
        source_image = self._load_and_prepare_image(src_img_filepath)
        sample_image = self._load_and_prepare_image(sample_img_filepath)
        result_image = self._model(tf.constant(source_image), tf.constant(sample_image))[0]
        
        loader = ImageLoader()
        path = loader.generate_filepath_for_image()
        abs_path = loader.get_absolute_filepath(path)
        abs_path += '.jpg'
        rel_path = path + '.jpg'
        cv2.imwrite(abs_path, cv2.cvtColor(np.squeeze(result_image)*255, cv2.COLOR_BGR2RGB))
        return { 'dst_img_url': rel_path }

    def _load_and_prepare_image(self, filepath: str):
        image = tf.io.read_file(filepath)
        image = tf.image.decode_image(image, channels=3)
        image = tf.image.convert_image_dtype(image, tf.float32)
        image = image[tf.newaxis, :]
        return image
