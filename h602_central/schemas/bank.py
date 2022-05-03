from pydantic import BaseModel


class Bank(BaseModel):
    id: int
    name: str
    logo: str
