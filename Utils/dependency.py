from sqlmodel import Session
from fastapi.security import OAuth2PasswordBearer
from Database.Engine import engine

def get_session():
    with Session(engine) as session:
        yield session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")