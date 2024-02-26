from datetime import datetime
from typing import List

class SQL:
    @staticmethod
    def from_any(token) -> str:
        token_type = type(token)
        if token_type is str:
            return "'" + token + "'"
        elif token_type is int or token_type is float:
            return str(token)
        elif token_type is bool:
            if token_type is False:
                return "'" + "f" + "'"
            else:
                return "'" + "t" + "'"
        elif token_type is datetime:
            return SQL.from_any(token.__str__())
        elif token is None:
            return 'NULL'

    @staticmethod
    def from_list(tokens: List[str]) -> str:
        result = ''
        for token in tokens:
            result += token
            result += ', '
        return result[:-2]
