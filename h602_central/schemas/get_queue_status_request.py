
from pydantic import BaseModel

class get_queue_status_request(BaseModel):
    queue_id: int
    type: int