from sqlmodel import SQLModel, Field
from sqlalchemy import Column, BigInteger

class UserLogin(SQLModel):
    email: str 
    password: str

class UserSignup(UserLogin):
    full_name: str

class WorkerLogin(SQLModel):
    worker_id: int 
    password: str

class WorkerSignup(SQLModel):
    full_name: str
    email: str
    password: str