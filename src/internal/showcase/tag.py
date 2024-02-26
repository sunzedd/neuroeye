from internal.entity.entity import Entity
from internal.showcase.tag_query_builder import TagQueryBuilder

from typing import List


class Tag(Entity):
    id: int
    name: str

    def __init__(self, dbresponse=None):
        super().__init__()
        if dbresponse is None:
            self.id = None
            self.name = None
        else:
            self.id = int(dbresponse[0])
            self.name = dbresponse[1]

    def save(self):
        if self.id is None:
            query = TagQueryBuilder().insert(self.name)
            dbresponse = self.database.execute_query(query)
            self.id = int(dbresponse[0][0])
        else:
            query = TagQueryBuilder().update(self.id, self.name)
            dbresponse = self.database.execute_query(query, fetch_response=False)

    def delete(self):
        if self.id is None:
            return
        query = TagQueryBuilder().delete(self.id)
        self.database.execute_query(query, fetch_response=False)

    def add_to_showcase(self, showcase_id: int):
        query = TagQueryBuilder().select_tagid_by_linked_showcase(showcase_id, self.id)
        dbresponse = Tag.get_storage_gateway().execute_query(query)
        if len(dbresponse) == 0:
            query = TagQueryBuilder().link_tag_to_showcase(showcase_id, self.id)
            dbresponse = Tag.get_storage_gateway().execute_query(query, False)

    @staticmethod
    def find(id: int) -> 'Tag' or None:
        query = TagQueryBuilder().select(id)
        dbresponse = Tag.get_storage_gateway().execute_query(query)
        return Tag(dbresponse[0]) if len(dbresponse) > 0 else None

    @staticmethod
    def find_by_name(name: str) -> 'Tag' or None:
        query = TagQueryBuilder().select_by_name(name)
        dbresponse = Tag.get_storage_gateway().execute_query(query)
        return Tag(dbresponse[0]) if len(dbresponse) > 0 else None

    @staticmethod
    def find_by_showcase(showcase_id: int) -> List['Tag']:
        query = TagQueryBuilder().select_tags_belonging_to_showcase(showcase_id)
        dbresponse = Tag.get_storage_gateway().execute_query(query)
        tags = [Tag(row) for row in dbresponse]
        return tags


    def __dict__(self):
        return {
            "id": self.id,
            "name": self.name
        }
