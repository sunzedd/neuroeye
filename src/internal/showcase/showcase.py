from internal.storage.istorage import DatabaseSyncError
from internal.entity.entity import Entity
from internal.showcase.showcase_query_builder import ShowcaseQueryBuilder
from internal.showcase.tag import Tag

from typing import List



class Showcase(Entity):
    id: int
    title: str
    description: str
    src_img_id: int
    sample_img_id: int
    dst_img_id: int
    author_id: int
    is_published: int
    tags: List['Tag']

    def __init__(self, dbresponse=None, tags: List['Tag']=None):
        super().__init__()
        if dbresponse is None:
            self.id = None
            self.title = None
            self.description = None
            self.src_img_id = None
            self.sample_img_id = None
            self.dst_img_id = None
            self.author_id = None
            self.is_published = 0
            self.tags = tags
        else:
            self.id = int(dbresponse[0])
            self.title = dbresponse[1]
            self.description = dbresponse[2]
            self.src_img_id = int(dbresponse[3])
            self.sample_img_id = int(dbresponse[4])
            self.dst_img_id = int(dbresponse[5])
            self.author_id = int(dbresponse[6])
            self.is_published = int(dbresponse[7])
            self._load_tags()

    def save(self):
        if self.id is None:
            query = ShowcaseQueryBuilder().insert(
                self.title,
                self.description,
                self.src_img_id,
                self.sample_img_id,
                self.dst_img_id,
                self.author_id,
                self.is_published
            )
            dbresponse = self.database.execute_query(query)
            self.id = int(dbresponse[0][0])
            self._save_tags()
        else:
            query = ShowcaseQueryBuilder().update(
                self.id,
                self.title,
                self.description,
                self.src_img_id,
                self.sample_img_id,
                self.dst_img_id,
                self.author_id,
                self.is_published
            )
            dbresponse = self.database.execute_query(query, fetch_response=False)
            self._save_tags()

    def delete(self):
        if self.id is None:
            return
        query = ShowcaseQueryBuilder().delete(self.id)
        self.database.execute_query(query, fetch_response=False)

    def like(self, user_id: int):
        if self.id is None:
            raise DatabaseSyncError('Showcase has not been saved')
        query = ShowcaseQueryBuilder().insert_like(self.id, user_id)
        self.database.execute_query(query, fetch_response=False)

    def unlike(self, user_id: int):
        if self.id is None:
            raise DatabaseSyncError('Showcase has not been saved')
        query = ShowcaseQueryBuilder().delete_like(self.id, user_id)
        self.database.execute_query(query, fetch_response=False)

    def is_liked_by_user(self, user_id: int) -> bool:
        if self.id is None:
            return False
        query = ShowcaseQueryBuilder().select_specific_id_liked_by_user(self.id, user_id)
        dbresponse = self.database.execute_query(query)
        if len(dbresponse) == 0:
            return False
        else:
            return True
    
    def get_views_count(self) -> int:
        if self.id is None:
            return False
        query = ShowcaseQueryBuilder().select_view_count(self.id)
        dbresponse = self.database.execute_query(query)
        return 0 if len(dbresponse) == 0 else int(dbresponse[0][0])

    def increase_view_count(self) -> int:
        if self.id is None:
            return False
        view_count = self.get_views_count()
        if view_count == 0:
            query = ShowcaseQueryBuilder().insert_view_counter(self.id)
            self.database.execute_query(query, fetch_response=False)
            view_count = self.get_views_count()
        query = ShowcaseQueryBuilder().update_view_count(self.id, view_count + 1)
        self.database.execute_query(query, fetch_response=False)
        return view_count + 1

    @staticmethod
    def find(id: int) -> 'Showcase':
        query = ShowcaseQueryBuilder().select(id)
        dbresponse = Showcase.get_storage_gateway().execute_query(query)
        return Showcase(dbresponse[0]) if len(dbresponse) > 0 else None

    @staticmethod
    def find_by_author(user_id) -> List['Showcase']:
        query = ShowcaseQueryBuilder().select_by_author_id(user_id)
        dbresponse = Showcase.get_storage_gateway().execute_query(query)
        result = [Showcase(row) for row in dbresponse]
        return result

    @staticmethod
    def find_liked_by_user(user_id: int) -> List['Showcase']:
        query = ShowcaseQueryBuilder().select_liked_by_user(user_id)
        dbresponse = Showcase.get_storage_gateway().execute_query(query)
        result = [Showcase(row) for row in dbresponse]
        return result

    @staticmethod
    def find_last_published(limit=20) -> List['Showcase']:
        query = ShowcaseQueryBuilder().select_last_published(limit)
        dbresponse = Showcase.get_storage_gateway().execute_query(query)
        result = [Showcase(row) for row in dbresponse]
        return result

    def __dict__(self):
        tags = [tag.__dict__() for tag in self.tags]
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "src_img_id": self.src_img_id,
            "sample_img_id": self.sample_img_id,
            "dst_img_id": self.dst_img_id,
            "author_id": self.author_id,
            "is_published": self.is_published,
            "tags": tags
        }

    def _save_tags(self):
        if self.tags is None or len(self.tags) == 0:
            return

        for tag in self.tags:
            existing_tag = Tag.find_by_name(tag.name)
            if existing_tag is None:
                tag.save()
                tag.add_to_showcase(self.id)
            else:
                existing_tag.add_to_showcase(self.id)

    def _load_tags(self):
        if self.id is None:
            return
        self.tags = Tag.find_by_showcase(self.id)   
