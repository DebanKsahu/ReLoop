from sqlmodel import SQLModel, Field

class Token(SQLModel):
    access_token: str
    token_type: str