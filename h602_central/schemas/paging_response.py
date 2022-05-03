from pydantic import BaseModel


class paging_response(BaseModel):
    message: str = 'success'
    code: str = '000'
    paging: dict
    data: list = []
