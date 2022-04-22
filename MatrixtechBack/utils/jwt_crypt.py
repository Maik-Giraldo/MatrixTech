from ast import literal_eval as to_dict
import datetime
import jwt

class JwtCrypt:
    def encrypt(self, data: dict, time: int =60)-> str:
        try:
            return jwt.encode({
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=time),
                "data": str(data),
                "iat": datetime.datetime.utcnow()
            }, "2167352sdbcjhsbs", algorithm="HS256")
        except Exception as e:
            print(e)
            raise Exception("Error encrypt jwt")

    def decrypt(self, encoded_jwt: str)-> dict:
        try:
            return to_dict(jwt.decode(encoded_jwt, "2167352sdbcjhsbs", algorithms=["HS256"])['data'])
        except jwt.ExpiredSignatureError as e:
            raise Exception("JWT expired")
        except jwt.InvalidTokenError as e:
            raise Exception("Invalid JWT")
        except Exception as e:
            print(e)
            raise Exception("Error decrypt jwt")