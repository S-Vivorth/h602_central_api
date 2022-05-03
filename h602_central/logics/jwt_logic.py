import jwt


class JwtLogic:

    @staticmethod
    def encode(payload, secret, algorithm='HS256'):
        encoded_string = jwt.encode(payload, secret, algorithm=algorithm)
        return encoded_string

    @staticmethod
    def decode(encoded_string, secret, algorithm=['HS256']):
        payload = jwt.decode(encoded_string, secret, algorithms=algorithm)
        return payload


default = JwtLogic()
