from pydantic import BaseModel
from h602_central.schemas.register_request import register_request


class register_response(BaseModel):

    message: str
    code: str
    data: register_request

