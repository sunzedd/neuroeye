from internal.showcase.ishowcase import IShowcaseService
from internal.showcase.showcase import Showcase
from internal.showcase.tag import Tag

from typing import List, Dict, Any


class ShowcaseTable(IShowcaseService):
    @staticmethod
    def create(user_id: int, title: str, description: str, 
               src_img_id: int, sample_img_id: int, dst_img_id: int,
               publish: bool=False, tags: str=None) -> Dict:
        showcase = Showcase()
        showcase.title = title
        showcase.description = description
        showcase.author_id = user_id
        showcase.src_img_id = src_img_id
        showcase.sample_img_id = sample_img_id
        showcase.dst_img_id = dst_img_id
        showcase.is_published = int(publish)

        if tags is not None:            
            parsed = tags.split(' ')
            showcase.tags = []
            for tagname in parsed:
                tag = Tag()
                tag.name = tagname
                showcase.tags.append(tag)
        showcase.save()

        return showcase.__dict__()

    @staticmethod
    def find(id: int) -> Dict:
        showcase = Showcase.find(id)
        return showcase.__dict__() if showcase is not None else None

    @staticmethod
    def find_owned_by_user(user_id: int) -> List[Dict]:
        showcases = Showcase.find_by_author(user_id)
        return [s.__dict__() for s in showcases]

    @staticmethod
    def find_liked_by_user(user_id: int) -> List[Dict]:
        showcases = Showcase.find_liked_by_user(user_id)
        return [s.__dict__() for s in showcases]

    @staticmethod
    def find_last_published(limit: int=30) -> List[Dict]:
        showcases = Showcase.find_last_published()
        return [s.__dict__() for s in showcases]

    @staticmethod
    def is_liked_by_user(showcase_id: int, user_id: int) -> bool:
        showcase = Showcase.find(showcase_id)
        return showcase.is_liked_by_user(user_id)

    @staticmethod
    def publish(id: int):
        showcase = Showcase.find(id)
        if showcase is not None:
            showcase.is_published = 1
            showcase.save()

    @staticmethod
    def unpublish(id: int):
        showcase = Showcase.find(id)
        if showcase is not None:
            showcase.is_published = 0
            showcase.save()

    @staticmethod
    def like(showcase_id: int, user_id: int):
        showcase = Showcase.find(showcase_id)
        if showcase is not None:
            showcase.like(user_id)

    @staticmethod
    def unlike(showcase_id: int, user_id: int):
        showcase = Showcase.find(showcase_id)
        if showcase is not None:
            showcase.unlike(user_id)

    @staticmethod
    def delete(id: int):
        showcase = Showcase.find(id)
        if showcase is not None:
            showcase.delete()

    @staticmethod
    def increase_view_count(id: int) -> int:
        showcase = Showcase.find(id)
        if showcase is not None:
            return showcase.increase_view_count()

    @staticmethod
    def get_view_count(id: int) -> int:
        showcase = Showcase.find(id)
        if showcase is not None:
            return showcase.get_views_count()
        else:
            return 0
