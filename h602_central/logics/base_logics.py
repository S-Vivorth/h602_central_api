from h602_central.logics.settings_logic import settings_logic
from h602_central.logics import jwt_logic
from fastapi import HTTPException, Request


class base_logics:

    def validate_tokens(token: str, qe_token: str):
        if (token and qe_token) is not None:
            client_token = settings_logic.get('client_token')
            if token == client_token:
                secret_code = settings_logic.get('secret_code')
                try:
                    qe_token_decode = jwt_logic.default.decode(qe_token, secret_code)
                except:
                    raise HTTPException(status_code=405, detail='Invalid qe_token')
                if {"qb_id", "qb_file_name", "computer_cpu", "computer_name"} <= qe_token_decode.keys():
                    return
                else:
                    raise HTTPException(status_code=405,
                                        detail={'message': 'Invalid qe_token', 'code': "405", "data": {}})
            else:
                raise HTTPException(status_code=401, detail='Unauthorized')
        else:
            raise HTTPException(status_code=401, detail='Token cannot be empty')

    def validate_support_token(request: Request):
        token = request.headers.get('token')
        support_token = settings_logic.get('support_token')
        if token is not None:
            if token == support_token:
                return
            else:
                raise HTTPException(status_code=401, detail='Invalid token')
        else:
            raise HTTPException(status_code=401, detail='Token cannot be empty')

    def raise_exception(status_code: int, message: str):
        raise HTTPException(status_code=status_code, detail={
            "message": "Invalid company_id",
            "code": str(status_code),
            "data": {}
        })

    def copy(from_obj, to_obj, ignores=[]):
        """copy all properties from one oject to another object in the same sqlalchemy class.
        :param from_obj: source object that will copy attribue to destination object.
        :param to_obj: destination object tha will copy from source object.
        :param ignores: list of columns that will not override value from source object to destination object.
        """
        for key in [k for k in from_obj.__table__.columns.keys() if k not in ignores]:
            setattr(to_obj, key, getattr(from_obj, key))

            # fix .ext for ExtMixin
        # because .ext is just declare in ExtMixin not in .columns schema
        # we need to for copy it if source object contain that
        if hasattr(from_obj, 'ext'):
            to_obj.ext = from_obj.ext

        return to_obj
