from internal.sequrity.isequrity import ISecurityService

import hashlib
import random, string

class Security(ISecurityService):
    def hash_string(self, plain: str) -> str:
        hashed = hashlib.sha256(plain.encode('utf-8'))
        return hashed.hexdigest()

    def generate_random_string(self, length: int=30) -> str:
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))
