from internal.usecase_response import UsecaseResponse
from internal.showcase.showcase_table import ShowcaseTable
from internal.media.image_table import ImageTable
from internal.user.user_table import UserTable

from typing import Dict


class GetShowcaseUsecase:
    _showcase_id: int
    _current_user_id: int
    _error_message: str
    _error_code: int
    
    _showcase: Dict
    _showcase_view_count: int
    _author: Dict
    _is_liked_by_user: bool
    _src_img_url: str
    _sample_img_url: str
    _dst_img_url: str

    def __init__(self, showcase_id: int, current_user_id: int):
        self._error_message = None
        self._error_code = None

        self._showcase_id = showcase_id
        self._current_user_id = current_user_id

    def execute(self) -> UsecaseResponse:
        self._showcase = ShowcaseTable.find(self._showcase_id)
        if not self._showcase:
            self._error_message = 'Showcase does not found'
            self._error_code=404
            return self._compose_response()
        
        author = UserTable.find(self._showcase.get('author_id'))
        if not author:
            author = {'id': -1, 'username': 'Пользователь удален'}
        else:
            author['userpic_url'] = ImageTable.get_url(author['userpic_id'])

        self._author = author
        self._showcase_view_count = ShowcaseTable.increase_view_count(self._showcase_id)
        self._is_liked_by_user = ShowcaseTable.is_liked_by_user(self._showcase_id, self._current_user_id)
        
        self._src_img_url = ImageTable.get_url(self._showcase.get('src_img_id'))
        self._sample_img_url = ImageTable.get_url(self._showcase.get('sample_img_id'))
        self._dst_img_url = ImageTable.get_url(self._showcase.get('dst_img_id'))

        return self._compose_response()

    def _compose_response(self) -> UsecaseResponse:
        if self._error_message:
            return UsecaseResponse(self._error_message, self._error_code)

        result = {
            'id': self._showcase['id'],
            'title': self._showcase['title'],
            'description': self._showcase['description'],
            'src_img_url': self._src_img_url,
            'sample_img_url': self._sample_img_url,
            'dst_img_url': self._dst_img_url,
            'author_id': self._author['id'],
            'author_name': self._author['username'],
            'author_userpic_url': self._author.get('userpic_url', None),
            'is_published': self._showcase['is_published'],
            'tags': self._showcase.get('tags'),
            'view_count': self._showcase_view_count,
            'is_liked_by_user': self._is_liked_by_user
        }

        response = UsecaseResponse()
        response.successfull_result = result
        
        return response
