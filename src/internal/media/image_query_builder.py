from internal.storage.postgres.sql_util import SQL


class ImageQueryBuilder:
    def __init__(self):
        self.TABLE_NAME = "trpo_image"
        self.COLUMN = {
            "id": "id",
            "url": "url"
        }

    def select_all_by_id(self, id) -> str:
        return ('SELECT id, url FROM ' + self.TABLE_NAME + ' ' +
                'WHERE id={}')\
                    .format(SQL.from_any(id))

    def insert(self, url: str) -> str:
        return ('INSERT INTO ' + self.TABLE_NAME + '(' + self.COLUMN['url'] + ') ' + 
                'VALUES ({}) RETURNING id')\
                    .format(SQL.from_any(url))

    def update(self, id: int, url: str) -> str:
        return ('UPDATE ' + self.TABLE_NAME + ' '
                'SET url={} ' +
                'WHERE id={}')\
                    .format(
                        SQL.from_any(url),
                        SQL.from_any(id))

    def delete(self, id: int) -> str:
        return ('DELETE FROM ' + self.TABLE_NAME + ' WHERE id={}')\
            .format(SQL.from_any(id))
