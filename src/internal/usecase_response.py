from typing import Dict

class UsecaseResponse:
    def __init__(self, error_message=None, error_code=200):
        self.error_message = None
        self.error_code = error_code
        self.successfull_result: Dict

    def is_successfull(self) -> bool:
        return self.error_message == None
