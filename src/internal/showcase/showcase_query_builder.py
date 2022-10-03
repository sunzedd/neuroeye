from internal.storage.postgres.sql_util import SQL


class ShowcaseQueryBuilder:
    def __init__(self):
        self.TABLE_NAME = 'trpo_showcase'
        self.USER_LIKES_SHOWCASE_TABLE_NAME = 'trpo_user_has_favourite_showcase'
        self.COLUMN = {
            'id': 'id',
            'title': 'title',
            'description': 'description',
            'src_img_id': 'src_img_id',
            'sample_img_id': 'sample_img_id',
            'dst_img_id': 'dst_img_id',
            'author_id': 'author_id',
            'is_published': 'is_published'
        }

    def select(self, id: int) -> str:
        return ('SELECT id, title, description, src_img_id, sample_img_id, dst_img_id, author_id, is_published FROM ' + self.TABLE_NAME + ' '
                        'WHERE id={}').\
                            format(SQL.from_any(id))

    def insert(self, title: str, description: str, 
                src_img_id: int, sample_img_id: int, dst_img_id: int, 
                author_id: int, is_published: int) -> str:
                return ('INSERT INTO ' + self.TABLE_NAME + '(title, description, src_img_id, sample_img_id, dst_img_id, author_id, is_published) ' + 
                        'VALUES({}, {}, {}, {}, {}, {}, {}) RETURNING id')\
                        .format(
                            SQL.from_any(title),
                            SQL.from_any(description),
                            SQL.from_any(src_img_id),
                            SQL.from_any(sample_img_id),
                            SQL.from_any(dst_img_id),
                            SQL.from_any(author_id),
                            SQL.from_any(is_published))

    def update(self, id: int, title: str, description: str, 
                src_img_id: int, sample_img_id: int, dst_img_id: int, 
                author_id: int, is_published: int) -> str:
                return ('UPDATE ' + self.TABLE_NAME + ' '
                        'SET title={}, description={}, src_img_id={}, sample_img_id={}, dst_img_id={}, author_id={}, is_published={} ' + 
                        'WHERE id={}')\
                            .format(
                            SQL.from_any(title),
                            SQL.from_any(description),
                            SQL.from_any(src_img_id),
                            SQL.from_any(sample_img_id),
                            SQL.from_any(dst_img_id),
                            SQL.from_any(author_id),
                            SQL.from_any(is_published),
                            SQL.from_any(id))

    def delete(self, id: int) -> str:
        return ('DELETE FROM ' + self.TABLE_NAME + ' ' + 'WHERE id={}').format(SQL.from_any(id))

    def select_last_published(self, limit=20) -> str:
        return ('SELECT id, title, description, src_img_id, sample_img_id, dst_img_id, author_id, is_published ' +
                'FROM ' + self.TABLE_NAME + ' '
                'WHERE is_published=1 ' + 
                'ORDER BY -id ' +
                'LIMIT {}')\
                    .format(SQL.from_any(limit))

    def select_by_author_id(self, user_id: int) -> str:
        return ('SELECT id, title, description, src_img_id, sample_img_id, dst_img_id, author_id, is_published ' +
                'FROM ' + self.TABLE_NAME + ' '
                'WHERE author_id={}')\
                    .format(SQL.from_any(user_id))

    def select_liked_by_user(self, user_id: int) -> str:
        return ('SELECT id, title, description, src_img_id, sample_img_id, dst_img_id, author_id, is_published FROM ' +
                self.TABLE_NAME + ' ' 
                'JOIN ' + self.USER_LIKES_SHOWCASE_TABLE_NAME + ' ' + 
                'ON showcase_id=id ' + 
                'AND user_id={}')\
                    .format(user_id)

    def insert_like(self, showcase_id: int, user_id: int) -> str:
        return ('INSERT INTO ' + self.USER_LIKES_SHOWCASE_TABLE_NAME + ' ' +
                '(showcase_id, user_id) VALUES ({}, {})')\
                    .format(SQL.from_any(showcase_id), SQL.from_any(user_id))

    def delete_like(self, showcase_id: int, user_id: int) -> str:
        return ('DELETE FROM ' + self.USER_LIKES_SHOWCASE_TABLE_NAME + ' ' + 
                'WHERE showcase_id={} AND user_id={}')\
                    .format(SQL.from_any(showcase_id), SQL.from_any(user_id))
    
    def select_specific_id_liked_by_user(self, showcase_id: int, user_id: int) -> str:
        return ('SELECT showcase_id FROM ' + self.USER_LIKES_SHOWCASE_TABLE_NAME + ' ' + 
                'WHERE showcase_id={} AND user_id={}')\
                    .format(SQL.from_any(showcase_id), SQL.from_any(user_id))
    
    def insert_view_counter(self, showcase_id) -> str:
        return f'INSERT INTO trpo_showcase_view_count (showcase_id) VALUES ({SQL.from_any(showcase_id)})'

    def select_view_count(self, showcase_id: int) -> str:
        return f'SELECT view_count FROM trpo_showcase_view_count WHERE showcase_id={SQL.from_any(showcase_id)}'

    def update_view_count(self, showcase_id: int, new_count: int) -> str:
        return f'UPDATE trpo_showcase_view_count SET view_count={SQL.from_any(new_count)} WHERE showcase_id={SQL.from_any(showcase_id)}'

