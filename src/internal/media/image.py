from internal.shared.entity import Entity
from internal.media.image_query_builder import ImageQueryBuilder

from typing import List


class Image(Entity):
    id: int
    url: str

    def __init__(self, dbresponse=None):
        super().__init__()
        if dbresponse is None:
            self.id = None
            self.url = None
        else:
            self.id = int(dbresponse[0])
            self.url = dbresponse[1]
    
    def save(self):
        if self.id is None:
            query = ImageQueryBuilder().insert(self.url)
            response = self.database.execute_query(query)
            self.id = int(response[0][0])
        else:
            query = ImageQueryBuilder().update(self. id, self.url)
            self.database.execute_query(query, fetch_response=False)

    def delete(self):
        if self.id is None:
            return
        query = ImageQueryBuilder().delete(self.id)
        self.database.execute_query(query, fetch_response=False)

    @staticmethod
    def find(id: int) -> 'Image' or None:
        query = ImageQueryBuilder().select_all_by_id(id)
        response = Image.get_storage_gateway().execute_query(query)
        return Image(response[0]) if len(response) > 0 else None

    def __dict__(self):
        return { 
            'id': self.id,
            'url': self.url
        }
