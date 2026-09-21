from hashlib import sha256


class GenerateHashService:
    def __init__(self):
        pass

    def __call__(self, email: str, password: str):
        return sha256((email + password).encode()).digest().hex()
