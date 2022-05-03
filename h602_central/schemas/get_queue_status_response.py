from pydantic import BaseModel

class get_queue_status_response(BaseModel):
    status: int
    total_record: int
    type: int
    data: str