from internal.storage.postgres.sql_util import SQL


class TagQueryBuilder:
    def __init__(self):
        self.TABLE_NAME = 'trpo_tag'
        self.SHOWCASE_HAS_TAG_TABLE_NAME = 'trpo_showcase_has_tag'
        self.COLUMN = {
            'id': 'id',
            'name': 'name'
        }


    def select(self, id: int) -> str:
        return ("SELECT " + SQL.from_list([self.COLUMN["id"], self.COLUMN["name"]]) + " "
                "FROM " + self.TABLE_NAME + " " + 
                "WHERE " + self.COLUMN["id"] + "={}")\
                    .format(SQL.from_any(id))

    def select_by_name(self, name: str) -> str:
        return ("SELECT " + SQL.from_list([self.COLUMN["id"], self.COLUMN["name"]]) + " "
                "FROM " + self.TABLE_NAME + " " +
                "WHERE " + self.COLUMN["name"] + "={}")\
                    .format(SQL.from_any(name))

    def insert(self, name: str) -> str:
        return ('INSERT INTO ' + self.TABLE_NAME + ' (' + self.COLUMN['name'] + ')' +
                ' VALUES ({})' +
                ' RETURNING ' + self.COLUMN['id'])\
                    .format(SQL.from_any(name))

    def update(self, id: int, name: str) -> str:
        return ('UPDATE ' + self.TABLE_NAME + ' ' +
                'SET ' + self.COLUMN['name'] + '={}, ' +
                'WHERE ' + self.COLUMN['id'] + '={}')\
                    .format(
                        SQL.from_any(name),
                        SQL.from_any(id))

    def delete(self, id: int) -> str:
        return ('DELETE FROM ' + self.TABLE_NAME + ' WHERE ' + self.COLUMN['id'] + '={}')\
            .format(SQL.from_any(id))
        
    def select_tags_belonging_to_showcase(self, showcase_id: int) -> str:
        return ('SELECT ' + self.COLUMN['id'] + ', ' + self.COLUMN['name'] + ' ' 
                'FROM ' + self.TABLE_NAME + ' ' +
                'JOIN ' + self.SHOWCASE_HAS_TAG_TABLE_NAME + ' ' + 
                'ON ' + self.COLUMN['id'] + '=tag_id ' +
                'WHERE showcase_id={}')\
                    .format(SQL.from_any(showcase_id))

    def link_tag_to_showcase(self, showcase_id: int,  tag_id: int) -> str:
        return ('INSERT INTO ' + self.SHOWCASE_HAS_TAG_TABLE_NAME + '(showcase_id, tag_id) ' + 
                'VALUES ({}, {})')\
                    .format(
                        SQL.from_any(showcase_id),
                        SQL.from_any(tag_id))

    def select_tagid_by_linked_showcase(self, showcase_id: int, tag_id: int) -> str:
        return ('SELECT tag_id ' +
                'FROM ' + self.SHOWCASE_HAS_TAG_TABLE_NAME + ' ' + 
                'WHERE showcase_id={} AND tag_id={}')\
                    .format(
                        SQL.from_any(showcase_id),
                        SQL.from_any(tag_id))
