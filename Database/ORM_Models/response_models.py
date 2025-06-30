from sqlmodel import SQLModel
from Utils.enums import ResponseType

class SimpleResponse(SQLModel):
    response_type: ResponseType
    message: str