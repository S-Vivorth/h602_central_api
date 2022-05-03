
from pydantic import BaseModel

class data(BaseModel):
    queue_id: str
    total_record: int
class queue_response(BaseModel):
    message: str
    code: str
    data: data


