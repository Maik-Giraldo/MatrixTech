import bcrypt
import random

class BcryptCrypt:
    def __init__(self):
        ...
    def encrypt(self, string: str, need: str ="string"):
        s = random.randint(5, 10)
        salt = bcrypt.gensalt(s)
        hashed = bcrypt.hashpw(bytes(str(string), encoding="utf-8"), salt)

        if need == "string":
            return hashed.decode("utf-8")
        elif need == "byte":
            return hashed
        else:
            raise Exception("need must be 'string' or 'byte'")

    def validate(self, valueStr: str, EncCompare: str):
        return bcrypt.checkpw(
            bytes(str(valueStr), encoding="utf-8"),
            bytes(str(EncCompare), encoding="utf-8")
        )